from app import app
from flask import render_template, request, redirect, url_for, session, flash, json
from app.libraries.util import Util as util, web_permission_checker
from app.models.user import User as UserModel
from app.libraries.validator import MyValidator
from datetime import datetime

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
                    print(password)
                    print(user.password)
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

        @app.route('/user/list')
        @web_permission_checker
        def user_list():
            return render_template('/user/list.html')

        # @app.route('/user/add', methods=['GET','POST'])
        # @web_permission_checker
        # def user_add():
        #     if request.method == "POST":
        #         args = request.form.to_dict()
        #         validator = MyValidator()
        #         dovalidate = validator.wrp_validate(args, UserModel.addNewSchema)
        #         if(dovalidate['status'] is False):
        #             errmsg = util.validate_message_to_dict(dovalidate['messages'])
        #             flash('Check required fields','error')
        #             return render_template('user/form.html',errmsg=errmsg,edit_data=None)
                    
        #         profile=session['profile']
        #         args['created_by'] = profile['uid']
        #         try:
        #             result = RoleModel.addNew(args)
        #             flash('Data Successfully Added','success')
        #             return redirect(util.my_url_for(url_for('master_role_with_datatables_orator')))
        #         except Exception as e:
        #             err= util.read_exception_data(e)
        #             errmsg = ','.join(err['message'])
        #             if 'Duplicate' in errmsg or 'UNIQUE' in errmsg:
        #                 flash('Data failed to add due to duplicate record', 'error')
        #             else:
        #                 flash(errmsg, 'error')
        #             # flash(err['message'][-1], 'error')

        #     return render_template('/user/form.html')
        

