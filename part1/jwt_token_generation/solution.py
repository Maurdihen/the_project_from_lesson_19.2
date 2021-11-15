import jwt

secret = 's3cR$eT'
algo = 'HS256'

data = {
        "username": "Skypro",
        "role": "admin"
        }

access_token = jwt.encode(data, secret, algorithm=algo)