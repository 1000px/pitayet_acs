from serv.api import api
from flask import jsonify, request, url_for, abort, g
from serv.models import User
from serv import db
from serv.api.auth import auth
import re

# 根据分页信息获取相应users列表
@api.route('/users/')
@auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = User.query.paginate(
        page,
        per_page=per_page,
        error_out=False
    )
    users = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_users', page=page-1, per_page=per_page)
    next = None
    if pagination.has_next:
        next = url_for('api.get_users', page=page+1, per_page=per_page)

    return jsonify({
        'users': [user.to_json() for user in users],
        'prev_url': prev,
        'next_url': next,
        'total': pagination.total
    })

# 根据id获取用户信息
@api.route('/users/<int:id>')
@auth.login_required
def get_user(id):
    user = User.query.filter_by(id=id).first()
    result = {}
    if user is None:
        result = {
            'res': 'failed',
            'failed_infor': '用户不存在！'
        }
    else:
        result = {
            'res': 'success',
            'url': url_for('api.get_user', id=id),
            'user': user.to_json()
        }
    return jsonify(result)

# 用户启用或禁用
@api.route('/users/<int:id>/toggle_disabled', methods=['PUT'])
@auth.login_required
def disabled_user(id):
    user = User.query.filter_by(id=id).first()
    result = {}
    if user is None:
        result = {
            'res': 'failed',
            'failed_infor': '用户不存在'
        }
    else:
        user.disabled = not user.disabled
        db.session.add(user)
        db.session.commit()
        result = {
            'res': 'success',
            'url': url_for('api.get_user', id=id),
            'user': user.to_json()
        }
    return jsonify(result)

@api.route('/user', methods=['PUT'])
@auth.login_required
def update_user():
    # 目前允许更新的，只有用户名！
    username = request.json.get('username')
    # 用户名格式验证
    pat_username = r'^[0-9a-zA-Z_]{5,18}$'
    if re.match(pat_username, username) is None:
        return jsonify({
            'res': 'failed',
            'failed_infor': '用户名格式错误'
        })
    user = g.current_user
    user.username = username
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'res': 'success',
        'user': user.to_json()
    })
