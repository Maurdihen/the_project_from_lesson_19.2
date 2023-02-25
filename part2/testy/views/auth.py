from flask import request
from flask_restx import Namespace, Resource

from container import auth_service

auth_ns = Namespace("auth")

@auth_ns.route("/")
class AuthsViews(Resource):
    def post(self):
        data = request.json
        if None in [data.get("username", None), data.get("password", None)]:
            return "", 400
        tokens = auth_service.generate_token(data.get("username", None), data.get("password", None))

        return tokens, 201

    def put(self):
        data = request.json
        token = data.get("refresh_token")

        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201