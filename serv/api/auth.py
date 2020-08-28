from serv.api import api
from serv.models import User
from serv import db
from flask import url_for, jsonify, abort, request, g
from flask_httpauth import HTTPTokenAuth
from serv.api.error import unauthorized, forbidden

auth = HTTPTokenAuth(scheme='Bearer')

# 注册
@api.route('/register', methods=['POST'])
def add_user():
    user = User.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'res': 'success',
        'user': user.to_json()
    })

# 登录
@api.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(username=request.json.get('username')).first()
    result = {}
    if user is None:
        result = {
            'res': 'failed',
            'failed_infor': '用户不存在！'
        }
    elif user.verify_password(request.json.get('password')):
        result = {
            'res': 'success',
            'token': user.generate_auth_token(expiration=3600),
            'expiration': 3600,
            'user': user.to_json()
        }
        g.current_user = user
        g.token_used = True
    else:
        result = {
            'res': 'failed',
            'failed_infor': '用户名或密码错误！'
        }
    return jsonify(result)

@api.route('/tokens/', methods=['POST'])
def get_token():
    if g.token_used:
        return False
    return jsonify({
        'token': g.current_user.generate_auth_token(expiration=3600),
        'expiration': 3600
    })
    
# @auth.verify_password
# def verify_password(username_or_token, password):
#     print('get one  password ......', password)
#     print('get one token ..........', username_or_token)
#     if username_or_token == '':
#         return False

#     if password == '':
#         g.current_user = User.verify_auth_token(username_or_token)
#         g.token_used = True
#         return g.current_user is not None

#     user = User.query.filter_by(username=username_or_token).first()
#     if not user:
#         return False
    
#     g.current_user = user
#     g.token_used = False
#     return user.verify_password(password)

@auth.verify_token
def verify_token(token):
    g.user = None
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return True

    
# @api.before_request
# def before_request():
#     if not g.token_used:
#         forbidden('Not Allowed')