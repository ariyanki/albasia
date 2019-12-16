from app import app
from flask import render_template, request, redirect, url_for, session, flash, json
from app.libraries.util import Util as util, web_permission_checker
from app.models.user import User as UserModel
from app.libraries.validator import MyValidator
from datetime import datetime
import uuid

class User():
    def __init__(self):

        @app.route('/signin', methods=['GET','POST'])
        def signin():
            #if user already logged in, then redirect to main page
            if 'profile' in session:
                if session['profile'] is not None:
                    return redirect(util.my_url_for(url_for('main')))

            #sigin button click
            if request.method == 'POST':
                args = request.form
                
                validator = MyValidator()
                dovalidate = validator.wrp_validate(args, {
                    'username': {'type': 'string', 'required': True, 'empty': False},
                    'password': {'type': 'string', 'required': True, 'empty': False}
                    })
                if(dovalidate['status'] is False):
                    return render_template('/user/signin.html',errmsg="Not valid username or password.")

                user = UserModel.getByUsername(args['username'])

                if user is not None:
                    password = util.generate_password(args['username'],args['password'],user.password_salt)
                    if password != user.password:
                        return render_template('/user/signin.html',errmsg="Not valid username or password.")
                        
                else:
                    return render_template('/user/signin.html',errmsg="Not valid username or password.")
                
                last_loggedin = {
                    'last_loggedin_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                    'is_loggedin': 1
                }
                result = UserModel.doUpdate(user.id, last_loggedin)
                
                data = {
                    'uid': user.id,
                    'fullname': user.fullname,
                    'phonenumber': user.phonenumber,
                    'email': user.email
                }

                session['profile'] = data
                return redirect(util.my_url_for(url_for('main')))
            else:
                return render_template('/user/signin.html')

        @app.route('/signout')
        @web_permission_checker
        def signout():
            session['profile'] = None
            session['menu_filter_role_id'] = None
            session.pop('_flashes', None)
            return redirect('/')

        @app.route('/user', methods=['GET','POST'])
        @web_permission_checker
        def user_list():
            #defaul value on page load
            args={}
            args['username']=''
            search = None

            if request.method == "POST":
                args = request.form.to_dict()
                if args['username'] != '':
                    args['q'] =" username like '%%"+args['username']+"%%' "
            
            result = UserModel.getList(args)
            
            return render_template('user/list.html', current_user=session['profile'], data_list=result)

        @app.route('/user/add', methods=['GET','POST'])
        @web_permission_checker
        def user_add():
            if request.method == "POST":
                #get form input
                args = request.form.to_dict()

                #validate form input
                validator = MyValidator()
                dovalidate = validator.wrp_validate(args, UserModel.addNewValidation)
                if(dovalidate['status'] is False):
                    errmsg = util.validate_message_to_dict(dovalidate['messages'])
                    #print(errmsg)
                    return render_template('/user/form.html',errmsg=errmsg,edit_data=args)
                
                #insert database
                args['created_by'] = session['profile']['uid']
                args['password_salt'] = str(uuid.uuid4())
                args['password'] = util.generate_password(args['username'],args['password'],args['password_salt'])
                result = UserModel.addNew(args)

                return redirect(util.my_url_for(url_for('user_list')))

            return render_template('/user/form.html',errmsg={},edit_data={})

        @app.route('/user/edit', methods=['GET','POST'])
        @web_permission_checker
        def user_edit():
            qargs = request.args.to_dict()
            if request.method == "POST":
                #get form input
                args = request.form.to_dict()
                
                #validate form input
                validator = MyValidator()
                dovalidate = validator.wrp_validate(args, UserModel.updateValidation)
                if(dovalidate['status'] is False):
                    errmsg = util.validate_message_to_dict(dovalidate['messages'])
                    #print(errmsg)
                    return render_template('/user/form.html',errmsg=errmsg,edit_data=args)
                
                #update database
                args['updated_by'] = session['profile']['uid']
                result = UserModel.doUpdate(qargs['id'],args)
                
                return redirect(util.my_url_for(url_for('user_list')))
            else:
                args = UserModel.getById(qargs['id'])

            return render_template('/user/form.html',errmsg={},edit_data=args)

        @app.route('/user/change_password', methods=['GET','POST'])
        @web_permission_checker
        def user_change_password():
            qargs = request.args.to_dict()
            if request.method == "POST":
                #get form input
                args = request.form.to_dict()
                
                #validate form input
                validator = MyValidator()
                dovalidate = validator.wrp_validate(args, UserModel.changePasswordValidation)
                if(dovalidate['status'] is False):
                    errmsg = util.validate_message_to_dict(dovalidate['messages'])
                    #print(errmsg)
                    return render_template('/user/form_change_password.html',errmsg=errmsg,edit_data=args)
                
                user = UserModel.getById(qargs['id'])
                #update database
                args['updated_by'] = session['profile']['uid']
                args['password_salt'] = str(uuid.uuid4())
                args['password'] = util.generate_password(user.username,args['password'],args['password_salt'])
                result = UserModel.doUpdate(qargs['id'],args)
                
                return redirect(util.my_url_for(url_for('user_list')))
            
            return render_template('/user/form_change_password.html',errmsg={},edit_data={})

        @app.route('/user/delete', methods=['GET','POST'])
        @web_permission_checker
        def user_delete():
            UserModel.doDelete(request.args['id'])
            return redirect(util.my_url_for(url_for('user_list')))
