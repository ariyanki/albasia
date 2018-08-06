import hashlib,sys,uuid

if len(sys.argv)>1:
	un = sys.argv[1]
	pw = sys.argv[2]
	salt = str(uuid.uuid4())

	un_bytes = un.encode('utf-8')
	pw_bytes = pw.encode('utf-8')
	salt_bytes = salt.encode('utf-8')
	hash = hashlib.sha256(un_bytes + pw_bytes + salt_bytes).hexdigest()

	print("username:"+ un)
	print("password:"+ pw)
	print("salt: "+ salt)
	print("hash password: "+hash)
else:
	print("Command: python generate_password.py <username> <password>")