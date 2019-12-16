import re
from cerberus import Validator
from werkzeug.datastructures import FileStorage

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

