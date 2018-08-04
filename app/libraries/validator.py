import re
from cerberus import Validator
# from var_dump import var_dump
from werkzeug.datastructures import FileStorage
from datetime import datetime

from app import app, config, db
from app.libraries.util import Util as util

class MyValidator(Validator):

    def __init__(self, *args, **kwargs):
        if 'additional_context' in kwargs:
            self.additional_context = kwargs['additional_context']
        super(MyValidator, self).__init__(*args, **kwargs)

    """
    Validate URL
    """

    def _validate_isurl(self, isurl, field, value):
        """ Validate URL.

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        valid = re.match("([a-z]([a-z]|\d|\+|-|\.)*):(\/\/(((([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?((\[(|(v[\da-f]{1,}\.(([a-z]|\d|-|\.|_|~)|[!\$&'\(\)\*\+,;=]|:)+))\])|((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|(([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=])*)(:\d*)?)(\/(([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*|(\/((([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)|((([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)|((([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)){0})(\?((([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\xE000-\xF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\x00A0-\xD7FF\xF900-\xFDCF\xFDF0-\xFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?", value)
        if valid is None:
            self._error(field, "Invalid URL format")

    """
    Validate Machine name format
    """

    def _validate_ismachinename(self, ismachinename, field, value):
        """ Validate URL.

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        valid = re.match("^[a-z0-9_]+$", value)
        if valid is None:
            self._error(field, "Invalid machine name format")

    """
    Validate phone number format
    """

    def _validate_isphonenumber(self, isphonenumber, field, value):
        """ Validate URL.

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        valid = re.match("^(\+?62|08)[0-9]{7,12}$", value)
        if valid is None:
            self._error(
                field, "Invalid phone number format start with (+62 or 08), length 9-14 chars")

    """
    Type Validator : File
    """

    def _validate_type_file(self, value):
        if isinstance(value, FileStorage):
            return True
        return False

    """
    Email validator
    """

    def _validate_email(self, email, field, value):
        """ Validate Email.

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        valid = re.match(
            "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value)
        if valid is None:
            self._error(field, "Invalid email format")
    
    """
    Datetime validator
    """
    def _validate_datetime(self, dtformat, field, value):
        # format reference: https://www.tutorialspoint.com/python/time_strptime.htm
        try:
            check= datetime.strptime(value, dtformat)
        except ValueError as e:
            app.logger.error('MyValidator\_validate_datetime\Error:', {
                'field': field,
                'value': value,
                'error' : util.read_exception_data(e)
            })
            self._error(field, "Invalid datetime format, should be "+str(dtformat))
        except Exception as e:
            app.logger.error('MyValidator\_validate_datetime\Error:', util.read_exception_data(e))
            raise e

    """
    Check existing field value on DB Table - validator
    >> implementation: 
    >> - single value >>> {'type': 'string', 'exists':'table,field'}
    >> - multipile values >>> {'type': 'list', 'exists':'table,field'}
    """
    def _validate_exists(self, exists, field, value):
        try:
            check_field=field
            table= None
            if(',' in exists):
                table,check_field = exists.strip().split(",")
            else:
                table=exists.strip()

            if(type(value) == list):
                check= db.table(table).where_in(check_field, value).count()
            elif (type(value) == str):
                check= db.table(table).where(check_field, value.strip()).count()
            else:
                check= db.table(table).where(check_field, value).count()

            if(check == 0):
                if(type(value) == list):
                    self._error(field, "'"+",".join(str(x) for x in value)+"' value is not exists on database")
                else:
                    self._error(field, "'"+str(value)+"' value is not exists on database")
        except Exception as e:
            app.logger.error('MyValidator\_validate_exists\Error', util.read_exception_data(e))
            raise e

    """
    Check unique field value on DB Table - validator
    >> implementation: 
    >> {'type': 'string', 'unique':'table,field'}
    """
    def _validate_unique(self, unique, field, value):
        try:
            check_field=field
            table= None
            if(',' in unique):
                table,check_field = unique.strip().split(",")
            else:
                table=unique.strip()
        
            if (type(value) == str):
                check= db.table(table).where(check_field, value.strip()).count()
            else:
                check= db.table(table).where(check_field, value).count()

            if(check > 0):
                self._error(field, "'"+str(value)+"' value is already exists, please use another value")
        except Exception as e:
            app.logger.error('MyValidator\_validate_unique\Error', util.read_exception_data(e))
            raise e

    """
    Check file_ext on input File - validator
    >> implementation: 
    >> {'type': 'file', 'file_ext': ['JPG','PNG','MP4']}
    """
    def _validate_file_ext(self, file_ext, field, value):
        try:
            if isinstance(value, FileStorage):
                filename= value.filename.strip()
                filename= filename.lower()
                found_counter=0
                if type(file_ext) is list:
                    # check for multiple extension
                    for ext in file_ext:
                        if filename.endswith('.'+ext.lower()):
                            found_counter += 1
                else:
                    # check for 1 file-extension 
                    if filename.endswith('.'+file_ext.lower()):
                        found_counter += 1
                        
                if found_counter == 0:
                    if type(file_ext) is list:
                        self._error(field, " file extension must be one of these values ("+','.join(file_ext)+")")
                    else:
                        self._error(field, " file extension must be "+file_ext+")")
            else:
                self._error(field, " must be file type")
        except Exception as e:
            app.logger.error('MyValidator\_validate_file_ext\Error', util.read_exception_data(e))
            raise e

    """
    Wrapper validate
    Validate and return messages if not TRUE
    """

    def wrp_validate(self, document, schema=None, update=False, normalize=True):
        # schema = { 'rp': { 'type': 'integer' }, 'q': { 'type': 'string' }, 'f': { 'type': 'dict' } }
        # v = Validator()
        self.schema = schema
        self.normalized(document, schema)
        if self.validate(document) is False:
            numsg = []
            for attr, msgs in self.errors.items():
                for msg in msgs:
                    numsg.append(str(attr) + ' : ' + str(msg))
            return {'status': False, 'messages': numsg}
        else:
            return {'status': True, 'messages': []}

