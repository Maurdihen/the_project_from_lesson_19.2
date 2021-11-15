import jwt

def check_token(token, secret, algorithms):
	try:
	    result = jwt.decode(token, secret, algorithms=algorithms)
	    return result	
	except Exception as e:
	    return False