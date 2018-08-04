from app.models.base_model import CrudBase

class User(CrudBase):
    __table__ = 'user'
    __primary_key__ = 'id'
    __incrementing__ = True
    __columns__ = [
        'id', 
        'fullname', 
        'phonenumber',
        'email', 
        'created_by', 
        'updated_at', 
        'updated_by',
        'created_at', 
        'status'
        ]

    __add_new_fillable__ = [
        'username',
        'password',
        'fullname', 
        'phonenumber',
        'email'
        'created_by'
        ]

    __update_fillable__ = [
        'username',
        'fullname', 
        'phonenumber',
        'email', 
        'updated_by'
        ]

    srcRawQry = ""
    srcQryBind = []
    addNewSchema = {
        'username': {'type': 'string', 'required': True, 'empty': False},
        'password': {'type': 'string', 'required': True, 'empty': False},
        'fullname': {'type': 'string', 'required': True, 'empty': False},
        'phonenumber': {'type': 'string', 'required': True, 'empty': False},
        'email': {'type': 'string', 'required': True, 'empty': False, 'email': True}
    }
    updateSchema = {
        'username': {'type': 'string', 'required': True, 'empty': False},
        'fullname': {'type': 'string', 'required': True, 'empty': False},
        'phonenumber': {'type': 'string', 'required': True, 'empty': False},
        'email': {'type': 'string', 'required': True, 'empty': False, 'email': True}
    }

    # Override parent method for spesific search query
    @classmethod
    def getByUsername(self, username):
        result = self.where('username', username).first()
        return result