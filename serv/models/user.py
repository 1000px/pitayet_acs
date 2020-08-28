from serv import db
from flask import url_for, jsonify, current_app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, index=True)
    email = db.Column(db.String(256), unique=True, index=True)

    disabled = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)
    last_login = db.Column(db.DateTime(), default=datetime.utcnow)

    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password是非可读属性')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'disabled': self.disabled,
            'create_time': self.create_time,
            'last_login': self.last_login
        }

    @staticmethod
    def from_json(json_user):
        username = json_user.get('username')
        if username is None:
            # 返回非空提示
            pass
        email = json_user.get('email')
        if email is None:
            # 返回非空提示
            pass
        # 判断邮箱格式，并返回错误提示

        # 密码验证逻辑
        password = json_user.get('password')

        return User(
            username        = username,
            email           = email,
            password        = password
        )

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])