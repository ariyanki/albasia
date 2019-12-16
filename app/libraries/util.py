from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import hashlib
import base64

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

    @staticmethod
    def validate_message_to_dict(validate_message):
        err={}
        for a in validate_message:
            msg=a.split(" : ")
            err[msg[0]]=msg[1]
        return err

    @staticmethod
    def generate_password(un, pw, salt):
        un_bytes = un.encode('utf-8')
        pw_bytes = pw.encode('utf-8')
        salt_bytes = salt.encode('utf-8')
        return hashlib.sha256(un_bytes + pw_bytes + salt_bytes).hexdigest()

def web_permission_checker(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        #permission checking for web access
        return function(*args, **kwargs)
    return wrapper


def permission_checker(function):
    def wrapper(*args, **kwargs):
        #permission checking for api access
        return function(*args, **kwargs)
    return wrapper