from app import app
from flask import render_template, request, redirect, url_for, session, flash, json
from app.libraries.util import Util as util, web_permission_checker
from app.models.user import User as UserModel

class User():
    def __init__(self):

        @app.route('/signin', methods=['GET','POST'])
        def signin():
            if UserModel.getById(1) is None:
                return redirect(util.my_url_for(url_for('user_add')))

            if 'profile' in session:
                if session['profile'] is not None:
                    return redirect(util.my_url_for(url_for('main')))

            if request.method == 'POST':
                return redirect(util.my_url_for(url_for('main')))
            else:
                return render_template('signin.html')

        @app.route('/user/add', methods=['GET','POST'])
        @web_permission_checker
        def user_add():
            return render_template('/user/form.html')
        

