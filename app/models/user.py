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
        'longitude', 
        'latitude',
        'photo_filename', 
        'created_by', 
        'updated_at', 
        'updated_by',
        'created_at', 
        'status', 
        'is_loggedin', 
        'last_loggedin_at',
        'access_source',
        'last_access_source',
        'login_attempt'
        ]

    __add_new_fillable__ = [
        'fullname', 
        'phonenumber',
        'email', 
        'longitude', 
        'latitude', 
        'photo_filename',
        'created_by'
        ]

    __update_fillable__ = [
        'fullname', 
        'phonenumber',
        'email', 
        'longitude', 
        'latitude', 
        'photo_filename',
        'updated_by'
        ]

    srcRawQry = ""
    srcQryBind = []
    addNewSchema = {
        'username': {'type': 'string', 'required': True, 'empty': False, 'unique': 'user,username'},
        'password': {'type': 'string', 'required': True, 'empty': False},
        'fullname': {'type': 'string', 'required': True, 'empty': False},
        'phonenumber': {'type': 'string', 'required': True, 'empty': False},
        'email': {
            'type': 'string', 'required': True, 'empty': False, 'email': True},
        'longitude': {'type': 'string', 'required': False},
        'latitude': {'type': 'string', 'required': False},
        'area_id': {'type': 'integer', 'required': True, 'empty': False, 'exists':'marea,id'},
        'cluster_id': {'type': 'integer', 'required': True, 'empty': False, 'exists':'mcluster,id'},
        'upline_user_id': {'type': 'integer', 'required': False},
        'use_pin': {'type': 'integer', 'required': False, 'allowed': [0,1]},
        'is_loggedin': {'type': 'integer', 'required': False},
        'is_password_changed': {'type': 'integer', 'required': False},
        'photo_filename': {'type': 'string', 'required': False},
        'kredit': {'type': 'integer', 'required': False},
        'piggy_current_token': {'type': 'string', 'required': False},
        'fcm_token': {'type': 'string', 'required': False},
        'otp': {'type': 'string', 'required': False},
        'upline_margin_percentage': {'type': 'integer', 'required': False},
        'login_attempt': {'type': 'integer', 'required': False},
        'status': {'type': 'integer', 'required': False, 'allowed': [0,1]},
        'upline_margin': {'type': 'integer', 'required': False},
        'plafon_status': {'type': 'integer', 'required': False, 'allowed': [0,1,2,3,4,5]},
        'address': {'type': 'string', 'required': False},
        'postal_code': {'type': 'string', 'required': False}
    }
    updateSchema = {
        'fullname': {'type': 'string', 'required': True, 'empty': False},
        'phonenumber': {'type': 'string', 'required': True, 'empty': False},
        'email': {
            'type': 'string', 'required': True, 'empty': False, 'email': True},
        'longitude': {'type': 'string', 'required': False},
        'latitude': {'type': 'string', 'required': False},
        'area_id': {'type': 'integer', 'required': True, 'empty': False},
        'cluster_id': {'type': 'integer', 'required': True, 'empty': False},
        'upline_user_id': {'type': 'integer', 'required': False},
        'use_pin': {'type': 'integer', 'required': False, 'allowed': [0,1]},
        'is_loggedin': {'type': 'integer', 'required': False, 'allowed': [0,1]},
        'is_password_changed': {'type': 'integer', 'required': False, 'allowed': [0,1]},
        'photo_filename': {'type': 'string', 'required': False},
        'kredit': {'type': 'integer', 'required': False},
        'piggy_current_token': {'type': 'string', 'required': False},
        'fcm_token': {'type': 'string', 'required': False},
        'otp': {'type': 'string', 'required': False},
        'upline_margin_percentage': {'type': 'integer', 'required': False},
        'login_attempt': {'type': 'integer', 'required': False},
        'status': {'type': 'integer', 'required': False, 'allowed': [0,1]},
        'upline_margin': {'type': 'integer', 'required': False},
        'plafon_status': {'type': 'integer', 'required': False, 'allowed': [0,1,2,3,4,5]},
        'address': {'type': 'string', 'required': False},
        'postal_code': {'type': 'string', 'required': False}
    }



    # Override parent method for spesific search query
    @classmethod
    def getByUsername(self, username):
        result = self.where('username', username).first()
        return result