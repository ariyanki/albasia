import logging
import json
import pprint

from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims

from app import api, jwt, app
from app.libraries.validator import MyValidator

from var_dump import var_dump
import datetime
from app.variable_constant import VariableConstant as VariableConstant
from app.libraries.util import Util as util, permission_checker

class BaseApi(Resource):

    def response(self,args):
        # convert datetime to string to prevent object of type
        # datetime is not json
        # serializable
        def myconverter(o):
            if isinstance(o, datetime.datetime):
                return o.__str__()
            if isinstance(o, datetime.date):
                return o.__str__()

        data=None
        if 'data' in args:
            args['data'] = json.dumps(args['data'], default=myconverter)
            data = json.loads(args['data'])

        if 'title' not in args:
            args['title']='Info'
            args['body']='Success'

        if 'status_code' not in args:
            args['status_code']=200

        response_data = {
            'message': {
                'title': args['title'],
                'body': args['body']
            },
            'data': data
        }

        if (request.method == "GET") or (request.method == "DELETE"):
            request_data = ''
        else:
            request_data = request.get_json()

        exclude_request_data = ['/api/v1/user/login','/api/v1/user/register']

        if request.path in exclude_request_data:
            request_data = ''

        claims = get_jwt_claims()

        error_data = {
            'endpoint': request.method + " " + request.path,
            'status_code': args['status_code'],
            'user_claim': claims,
            'request': request_data,
            'response': response_data
        }
        if args['status_code'] != 200:
            app.logger.error('ERROR API RESPONSE',error_data)
        else:
            app.logger.info('API ACCESS',error_data)

        res = api.make_response(response_data, args['status_code'])
        return res

    def response_plain(self,args):
        # convert datetime to string to prevent object of type
        # datetime is not json
        # serializable
        def myconverter(o):
            if isinstance(o, datetime.datetime):
                return o.__str__()
            if isinstance(o, datetime.date):
                return o.__str__()
            if isinstance(o, decimal.Decimal):
                return float(o)
        data=None
        if 'data' in args:
            args['data'] = json.dumps(args['data'], default=myconverter)
            data = json.loads(args['data'])
        if 'status_code' not in args:
            args['status_code']=200

        response_data = data

        if (request.method == "GET") or (request.method == "DELETE"):
            request_data = ''
        else:
            request_data = request.get_json()

        exclude_request_data = ['/api/v1/user/login','/api/v1/user/register']

        if request.path in exclude_request_data:
            request_data = ''

        claims = get_jwt_claims()

        error_data = {
            'endpoint': request.method + " " + request.path,
            'status_code': args['status_code'],
            'user_claim': claims,
            'request': request_data,
            'response': response_data
        }
        if args['status_code'] != 200:
            app.logger.error('ERROR API RESPONSE',error_data)
        else:
            app.logger.info('API ACCESS',error_data)

        res = api.make_response(response_data, args['status_code'])
        return res

    def response_html(self,args):
        if 'status_code' not in args:
            args['status_code']=200

        log_data = {
            'args': args
        }
        app.logger.info('HTML ACCESS',log_data)

        return make_response(render_template(args['template_path'],data=args['data']), args['status_code'],{'Content-Type': 'text/html'})

class BaseList(BaseApi, Resource):

    def __init__(self, Model):
        self.Orm = Model

    @jwt_required
    @permission_checker
    def post(self, id=None):
        args = request.get_json()
        result = self.Orm.getList(args)
        del result['args']
        return self.response({'data':result})

class BaseCrud(BaseApi, Resource):

    def __init__(self, Model):
        self.Orm = Model

    @jwt_required
    @permission_checker
    def get(self, id=None):
        result = self.Orm.getById(id)
        if (result is not None):
            result = result.serialize()
        else:
            return self.response(VariableConstant.DATA_NOT_FOUND_RESPONSE)

        return self.response({"data":result})

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
        result = self.Orm.addNew(args)
        return self.response({"data":result.serialize()})

    @jwt_required
    @permission_checker
    def put(self, id):
        args = request.get_json()
        validator = MyValidator()
        dovalidate = validator.wrp_validate(args, self.Orm.updateValidation)
        if(dovalidate['status'] is False):
            return self.response({
                'title':'Error',
                'body':dovalidate['messages'],
                'status_code':422
            })
        claims = get_jwt_claims()
        args['updated_by'] = claims['uid']
        me = self.Orm.find(id)
        if (me is not None):
            result = self.Orm.doUpdate(id, args)
            return self.response({"data":result.serialize()})
        else:
            return self.response(VariableConstant.DATA_NOT_FOUND_RESPONSE)

    @jwt_required
    @permission_checker
    def delete(self, id):
        me = self.Orm.find(id)
        if (me is not None):
            me.delete()
            return self.response({"data":"Deleted"})
        else:
            return self.response(VariableConstant.DATA_NOT_FOUND_RESPONSE)
