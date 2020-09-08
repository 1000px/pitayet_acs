from flask import Blueprint, make_response,request
from serv.plugins import create_verify_code, token_ctrl
from io import BytesIO

file_api = Blueprint('file_api', __name__)

@file_api.route('/img_code')
def get_img_code():
    img, code = create_verify_code.create_verify_code()
    # 如果当前请求包含token，将该token失效，再生成新的token
    # token = request.headers['authorization']
    # if token is not None and token != '':
    #     token = token.split(' ')[1]
        
    buf = BytesIO()
    img.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Access-Control-Expose-Headers'] = 'authorization'
    response.headers['Content-Type'] = 'image/gif'
    response.headers['authorization'] = 'bearerToken ' + token_ctrl.gen_token(code, 300)
    return response

# @file_api.route('/verify_img_code', methods=['POST'])
# def verify_img_code():
#     code = request.json.get('code') 
#     token = request.headers['Authorization'].split(' ')[1]
#     if token is not None and token_ctrl.verify_token(token, code):
#         return jsonify({
#             'res': 'success'
#         })
#     return jsonify({
#         'res': 'failed',
#         'failed_infor': '图片验证码错误'
#     })