class VariableConstant(object):
    DATA_NOT_FOUND_MESSAGE = 'Data Not Found'
    USER_STATUS_BLOCKED = 0

    USER_BLOCKED_RESPONSE = {
        'title':'Error',
        'body':'User Blocked',
        'status_code':422
    }

    USER_LOGIN_FAILED_RESPONSE = {
        'title':'Error',
        'body':'Login Failed, check your username & password',
        'status_code':422
    }

    DATA_NOT_FOUND_RESPONSE = {
        'title':'Error',
        'body':'Data not found.',
        'status_code':422
    }