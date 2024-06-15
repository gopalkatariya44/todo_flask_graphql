from main import db
from main.features.auth.auth_models import User


class AuthServices:
    @staticmethod
    def create_user(user_vo):
        db.session.add(user_vo)
        db.session.commit()

    @staticmethod
    def update_pro(user_id):
        user = User.query.get(user_id)
        user.is_pro = True
        db.session.commit()

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        return user
