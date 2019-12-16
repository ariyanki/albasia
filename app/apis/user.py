from flask import Blueprint, request, json
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, \
    jwt_required, create_access_token, create_refresh_token, \
    get_jwt_claims, get_jwt_identity, get_raw_jwt, \
    jwt_refresh_token_required, get_jti
from app.apis.base_api import BaseApi, BaseList, BaseCrud
from app import jwt, app, cache, db, revoked_store
from app.variable_constant import VariableConstant
from app.libraries.validator import MyValidator
from app.models.user import User as UserModel
from app.libraries.util import Util as util, permission_checker
from datetime import datetime
import uuid

userapi = Blueprint('userapi', __name__)
api = Api(userapi)

class Login(BaseApi, Resource):
    def __init__(self):
        super(Login, self).__init__()

    def post(self):
        args = request.get_json()
        validator = MyValidator()
        dovalidate = validator.wrp_validate(args, {
            'username': {'type': 'string', 'required': True, 'empty': False},
            'password': {'type': 'string', 'required': True, 'empty': False}
            })
        if(dovalidate['status'] is False):
            return self.response({
            	'title':'Error',
            	'body':dovalidate['messages'],
            	'status_code':422
            })

        user = UserModel.getByUsername(args['username']).serialize()
        
        # Check Max Login Attempt Mode
        max_login_attempt = int(app.config['MAX_LOGIN_ATTEMPT'])
        if user is not None:

            if user['login_attempt'] >= max_login_attempt or user['status'] == VariableConstant.USER_STATUS_BLOCKED:
                return self.response(VariableConstant.USER_BLOCKED_RESPONSE)

            password = util.generate_password(args['username'],args['password'],user['password_salt'])
            if password != user['password']:
                app.logger.error('ERROR LOGIN : ', {'msg': 'Wrong Username or Password'})

                # Auto Increment Login Attempt
                la = UserModel.incrementLoginAttempt(user['id'])
                if (user['login_attempt'] + 1) >= max_login_attempt:
                    # Block user
                    UserModel.doUpdate(
                        user['id'],
                        {
                            'status': VariableConstant.USER_STATUS_BLOCKED,
                            'isloggedin': 0,
                            'login_attempt': 0
                        })
                    return self.response(VariableConstant.USER_BLOCKED_RESPONSE)
                    
                return self.response(VariableConstant.USER_LOGIN_FAILED_RESPONSE)
        else:
            app.logger.error('ERROR LOGIN : ', {'msg': 'User Not Found '})
            return self.response(VariableConstant.USER_LOGIN_FAILED_RESPONSE)

        user['access_token'] = create_access_token(identity=args['username'])
        user['refresh_token'] = create_refresh_token(identity=args['username'])

        access_jti = get_jti(encoded_token=user['access_token'])
        refresh_jti = get_jti(encoded_token=user['refresh_token'])
        revoked_store.set(access_jti, 'false', app.config['JWT_ACCESS_TOKEN_EXPIRES'] * 1.2)
        revoked_store.set(refresh_jti, 'false', app.config['JWT_REFRESH_TOKEN_EXPIRES'] * 1.2)

        #update last logged in
        UserModel.doUpdate(user['id'],{
        	'last_loggedin_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
        	'is_loggedin': 1
        })

        del user['password']
        del user['password_salt']

        return self.response({'data':user})

    @jwt.user_claims_loader
    def add_claims_to_access_token(identity):
        user = UserModel.getByUsername(identity)
        return {
            'username': identity,
            'uid': user.id
        }

## Use base List
class ViewList(BaseList, Resource):
    def __init__(self):
        super(ViewList, self).__init__(UserModel)

## without base list
class ViewListWithoutBaseList(BaseApi, Resource):
    def __init__(self):
        self.Orm = UserModel

    @jwt_required
    @permission_checker
    def post(self, id=None):
        args = request.get_json()
        result = self.Orm.getList(args)
        del result['args']

        retval = []
        for a in result['data']:
            del a['password']
            del a['password_salt']
            retval.append(a)

        result['data']=retval
        return self.response({'data':result})

class AddNew(BaseCrud, Resource):
    def __init__(self):
        super(AddNew, self).__init__(UserModel)

    #Override post method to add different logic
    @jwt_required
    @permission_checker
    def post(self):
        args = request.get_json()
        validator = MyValidator()
        dovalidate = validator.wrp_validate(args, self.Orm.addNewValidation)
        if(dovalidate['status'] is False):
            return self.response({
                'title':'Error',
                'body':dovalidate['messages'],
                'status_code':422
            })

        claims = get_jwt_claims()
        args['created_by'] = claims['uid']
        args['password_salt'] = str(uuid.uuid4())
        args['password'] = util.generate_password(args['username'],args['password'],args['password_salt'])
        result = self.Orm.addNew(args)
        return self.response({"data":result.serialize()})

class GetEditDelete(BaseCrud, Resource):
    def __init__(self):
        super(GetEditDelete, self).__init__(UserModel)

api.add_resource(Login, '/login')
api.add_resource(ViewList, '/list')
api.add_resource(ViewListWithoutBaseList, '/list_without_base_list')
api.add_resource(GetEditDelete, '/<string:id>')
api.add_resource(AddNew, '/')
