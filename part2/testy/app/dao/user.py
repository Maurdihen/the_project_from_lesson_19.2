from app.dao.model.user import User

class UserDAO:
    def __init__(self, sessiion):
        self.session = sessiion

    def get_one(self, uid):
        return self.session.query(User).get(uid)
    def get_by_username(self, username):
        return self.session.query(User).filter(User.user_name == username).first()
    def get_all(self):
        return self.session.query(User).all()
    def create(self, data):
        user = User(**data)
        print(user, data)
        self.session.add(user)
        self.session.commit()
    def delete(self, uid):
        user = self.session.query(User).get(uid)
        print(user)

        self.session.delete(user)
        self.session.commit()
    def update(self, data):
        uid = data.get("id")

        user = self.get_one(uid)

        user.user_name = data.get("user_name")
        user.role = data.get("role")
        user.password = data.get("password")

        self.session.add(user)
        self.session.commit()
