from serv.api import api
from serv.models import User
from serv import db
from flask import url_for, jsonify, abort, request, g, make_response
from flask_httpauth import HTTPTokenAuth
from serv.api.error import unauthorized, forbidden
from serv.plugins import create_verify_code, token_ctrl
from io import BytesIO
import re

auth = HTTPTokenAuth(scheme='Bearer')

# 注册
@api.route('/register', methods=['POST'])
def add_user():
    # 参数验证逻辑
    # 用户名5-18位数字、字母和下划线
    username = request.json.get('username')
    pat_username = r'^[0-9a-zA-Z_]{5,18}$'
    if re.match(pat_username, username) is None:
        return jsonify({
            'res': 'failed',
            'failed_infor': '用户名为5-18位数字、字母和下划线！'
        })
    # email格式验证
    email = request.json.get('email')
    pat_email = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
    if re.match(pat_email, email) is None:
        return jsonify({
            'res': 'failed',
            'failed_infor': '邮箱地址格式错误！'
        })

    # 密码为8-20位数字、字母和下划线
    password = request.json.get('password')
    pat_password = r'^[0-9a-zA-Z_]{8,20}$'
    if re.match(pat_password, password) is None:
        return jsonify({
            'res': 'failed',
            'failed_infor': '密码为8-20位数字、字母和下划线！'
        })

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
    if user is not None and user.verify_password(request.json.get('password')):
        result = {
            'res': 'success',
            'token': user.generate_auth_token(expiration=3600),
            'expiration': 3600,
            'user': user.to_json()
        }
        g.current_user = user
        g.token_used = True
        return result

    result = {
        'res': 'failed',
        'failed_infor': '用户名或密码错误！'
    }
    response = jsonify(result)
    response.status_code = 400
    return response

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

@api.route('/modify-password', methods=['POST'])
@auth.login_required
def modify_password():
    user = g.current_user
    result = {}
    old_password = request.json.get('oldPassword')
    if old_password is None or old_password == '':
        return {
            'res': 'failed',
            'failed_infor': '旧密码不能为空！'
        }
    if not user.verify_password(old_password):
        return {
            'res': 'failed',
            'failed_infor': '旧密码错误！'
        }
    new_password = request.json.get('newPassword')
    if new_password is None or new_password == '':
        return {
            'res': 'failed',
            'failed_infor': '新密码不符合要求！'
        }
    user.password = new_password
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'res': 'success'
    })

# @api.route('/img_code')
# def get_img_code():
#     img, code = create_verify_code.create_verify_code()
#     buf = BytesIO()
#     img.save(buf, 'jpeg')
#     buf_str = buf.getvalue()
#     response = make_response(buf_str)
#     response.headers['Content-Type'] = 'image/gif'
#     response.headers['Authorization'] = 'bearerToken ' + token_ctrl.gen_token(code, 300)
#     return response

@api.route('/verify_img_code', methods=['POST'])
def verify_img_code():
    code = request.json.get('code') 
    token = request.headers['authorization']
    print(token)
    if token is not None and token != '' and token != '' and token_ctrl.verify_token(token.split(' ')[1], code):
        return jsonify({
            'res': 'success'
        })
    return jsonify({
        'res': 'failed',
        'failed_infor': '图片验证码错误'
    })
