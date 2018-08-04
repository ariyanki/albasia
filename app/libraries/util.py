from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

class Util(object):
	
    @staticmethod
    def my_url_for(url):
        url_root = request.url_root
        url_root = url_root[:-1]
        arr_url = url_root.split(",")
        url_main = url_root+url
        if len(arr_url) > 1:
            for a in arr_url:
                if "https" in a:
                    url_main = a + url
        return url_main

def web_permission_checker(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        env = os.environ.get('FLASK_ENV', 'development')
        # if env != 'testing':
        #     if 'profile' not in session or ('profile' in session and session['profile'] is None):
        #         # return redirect(url_for('login'))
        #         return redirect(Util.my_url_for(url_for('login')))
        #     else:
        #         # allow all user access /main & /logout
        #         role_id = session['profile']['role_id']
        #         if(request.path=='/main' or request.path=='/logout'):
        #             allowed = 1
        #         # allow sadmin all path
        #         elif(VariableConstant.ROLE_ID_SADM == role_id):
        #             allowed = 1  
        #         else:
        #             # allowed = 1
        #             allowed = PymenuModel.check_allowed_menu(role_id, request.path)
                                      
        #         # disallowed 
        #         if(allowed<1):
        #             abort(403)
        return function(*args, **kwargs)
    return wrapper