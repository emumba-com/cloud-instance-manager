import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from settings import db, bcrypt
from config import DevelopmentConfig
import jwt
import datetime

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def get_all_users(self):
        userList = []
        all_users = db.session.query(User)
        for user in all_users:
            userDict = {
                "Id": user.id,
                "Name": user.name,
            }
            userList.append(userDict)
        return userList

    def addUser(self, username, password, admin=False):
        new_user = User(
            name =username,
            password = bcrypt.generate_password_hash(
                password, DevelopmentConfig().BCRYPT_LOG_ROUNDS
            ).decode('utf-8'),
            admin = admin
            )
        try:
            db.session.add(new_user)
            db.session.commit()

        except Exception as e:
            print(e)

    def unassign_instance_from_user(self, userId):
        db.session.query(User).filter(User.ins_id == userId).delete()
        db.session.commit()

    def deleteUser(self, userId):
        db.session.query(User).filter(User.id == userId).delete()
        db.session.commit()


    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                DevelopmentConfig().SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, DevelopmentConfig().SECRET_KEY)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def validate_token(token, uid):
        id = User.decode_auth_token(token)
        if uid == id:
            return True
        else:
            return False



class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


db.create_all()
db.session.commit()
