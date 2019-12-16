import logging
from var_dump import var_dump
'''
Invalid Response Exception (422)
'''
class InvalidResponseException(Exception):
	code = None
	description = None
	messages = []

	def __init__(self, description=None, response=None):
		self.messages = []
		Exception.__init__(self)
		if description is not None:
			self.description = description
			if isinstance(description, list):
				for msg in description:
					self.messages.append(str(msg))
			else:
				self.messages.append(str(description))
		self.code = response

	def get_description(self, environ=None):
		return u'%s' % escape(self.description)

	def get_body(self, environ=None):
		body = {
			'message': {
				'title': 'Error',
				'body': self.messages
			}
		}
		return body

	def get_code(self):
		return self.code

class GeneralResponseException(Exception):

	def __init__(self, title='Error',body='Error',code=422):
		
		Exception.__init__(self)
		
		self.title = title
		self.body = body
		self.code = code

	def get_body(self, environ=None):
		body = {
	        'message': {
	            'title': self.title,
	            'body': self.body
	        }
        }
		return body

	def get_code(self):
		return self.code

class ConnectionTimeoutException(Exception):

	def __init__(self):
		Exception.__init__(self)

	def get_body(self, environ=None):
		body = {
	        'message': {
	            'title': 'Error',
	            'body': 'Connection Timeout'
	        }
        }
		return body

	def get_code(self):
		return 422
