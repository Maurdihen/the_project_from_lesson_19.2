from flask import request
from flask_restx import Namespace, Resource

from container import user_service
from app.dao.model.user import UserSchema
from helpers.decorators import admin_reguired

user_ns = Namespace("users")
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route("/")
class UsersViews(Resource):
    def get(self):
        users = user_service.get_all()

        return users_schema.dump(users), 200
    def post(self):
        data = request.json
        user_service.create(data)

        return "", 201

@user_ns.route("/<int:uid>")
class UserViews(Resource):
    @admin_reguired
    def delete(self, uid):
        user_service.delete(uid)

        return "", 204