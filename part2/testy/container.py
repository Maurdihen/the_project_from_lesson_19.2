from service.user import UserService
from app.dao.user import UserDAO
from setup_db import db
from service.auth import AuthService

user_dao = UserDAO(db.session)
user_service = UserService(user_dao)

auth_service = AuthService(user_service)