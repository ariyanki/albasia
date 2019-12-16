from app.models.base_model import CrudBase

class User(CrudBase):
    #What is the table for this Model
    __table__ = 'user'

    #What is the primary key for this table
    __primary_key__ = 'id'
    
    #Define which columns can be added.
    __add_new_fillable__ = [
        'username',
        'password',
        'password_salt',
        'fullname', 
        'phonenumber',
        'email',
        'status',
        'is_loggedin',
        'login_attempt',
        'created_by'
        ]

    #Define which columns can be updated.
    __update_fillable__ = [
        'username',
        'password',
        'password_salt',
        'fullname', 
        'phonenumber',
        'email',
        'status',
        'is_loggedin',
        'login_attempt',
        'last_loggedin_at',
        'updated_by'
        ]

    #Define form input validation
    addNewValidation = {
        'username': {'type': 'string', 'required': True, 'empty': False},
        'password': {'type': 'string', 'required': True, 'empty': False},
        'fullname': {'type': 'string', 'required': True, 'empty': False},
        'phonenumber': {'type': 'string', 'required': True, 'empty': False},
        'email': {'type': 'string', 'required': True, 'empty': False, 'email': True}
    }
    updateValidation = {
        'fullname': {'type': 'string', 'required': True, 'empty': False},
        'phonenumber': {'type': 'string', 'required': True, 'empty': False},
        'email': {'type': 'string', 'required': True, 'empty': False, 'email': True}
    }
    changePasswordValidation = {
        'password': {'type': 'string', 'required': True, 'empty': False},
    }

    # Override parent method for spesific search query
    @classmethod
    def getByUsername(self, username):
        result = self.where('username', username).first()
        return result

    @classmethod
    def incrementLoginAttempt(self, uid):
        result = self.where('id', uid).increment('login_attempt')
        return result

