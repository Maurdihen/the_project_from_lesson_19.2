import json

def jsonwrap(x):
    def wrapper():
        r = x()
        return json.dumps(r)
    return wrapper
