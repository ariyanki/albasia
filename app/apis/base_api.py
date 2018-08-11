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
        # args={'data':data,'title':title,'body':body,'status_code':status_code}
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

        if args['status_code'] != 200:
            #write log if not 200
            if (request.method == "GET") or (request.method == "DELETE"):
                request_data = ''
            else:
                request_data = request.get_json()

            claims = get_jwt_claims()

            error_data = {
                'endpoint': request.method + " " + request.path,
                'status_code': args['status_code'],
                'user_claim': claims,
                'request': request_data,
                'response': response_data
            }
            app.logger.error('ERROR API RESPONSE',error_data)

        res = api.make_response(response_data, args['status_code'])
        return res

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
