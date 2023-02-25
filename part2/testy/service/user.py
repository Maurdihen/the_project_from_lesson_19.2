import hashlib
import base64
import hmac

from app.dao.user import UserDAO
from helpers.consatans import PWD_ITERATIONS, PWD_SALT
class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao
    def get_one(self, uid):
        return self.dao.get_one(uid)
    def get_by_username(self, username):
        return self.dao.get_by_username(username)
    def get_all(self):
        return self.dao.get_all()
    def create(self, data):
        data["password"] = self.generate_password(data['password'])
        return self.dao.create(data)
    def delete(self, uid):
        return self.dao.delete(uid)
    def update(self, data):
        data["password"] = self.generate_password(data['password'])
        return self.dao.update(data)
    def generate_password(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            PWD_SALT,
            PWD_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def compare_password(self, password_hash, other_password):
        decoded_digist = base64.b64decode(password_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            "sha256",
            other_password.encode("utf-8"),
            PWD_SALT,
            PWD_ITERATIONS
        )

        return hmac.compare_digest(decoded_digist, hash_digest)