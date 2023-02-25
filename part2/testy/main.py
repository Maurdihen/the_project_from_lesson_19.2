from flask import Flask
from flask_restx import Api
from views.user import user_ns
from views.auth import auth_ns
from setup_db import db
from app.dao.model.user import User
from config import Config


def create_app(config: Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    app.app_context().push()

    configure_app(app)
    return app

def configure_app(app: Flask):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    load_data(app)

def load_data(app):

    with app.app_context():
        user = User(user_name="root", password="random_password", role="admin")
        db.create_all()

        with db.session.begin():
            db.session.add(user)

if __name__ == "__main__":
    app = create_app(Config)
    app.run(port=5001)