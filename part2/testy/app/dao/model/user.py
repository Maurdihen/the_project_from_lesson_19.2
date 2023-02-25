from setup_db import db
from marshmallow import Schema, fields

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

class UserSchema(Schema):
    id = fields.Int()
    user_name = fields.Str()
    password = fields.Str()
    role = fields.Str()