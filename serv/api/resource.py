from serv.api import api
from serv.api.auth import auth
from flask import jsonify, request, url_for, abort, current_app, g, Response
from serv import db
from config import config
import os
from datetime import datetime
from werkzeug.utils import secure_filename

@api.route('/upload_avatar', methods=['POST'])
@auth.login_required
def upload():
  file_obj = request.files.get('file')
  if file_obj is None:
    return jsonify({
      'res': 'failed',
      'failed_infor': '没有上传文件'
    })
  
  filename = secure_filename(file_obj.filename)
  filetype = filename.split('.')[-1]
  savename = str(datetime.now().timestamp()) + str(hash(filename)) + '.' + filetype
  file_obj.save(os.path.join(current_app.config['RESOURCE_IMG'], savename))
  # 当有图片上传后 更新当前用户的avatar图片信息到数据库
  user = g.current_user
  if user is not None:
    if user.avatar_name != '':
      os.remove(os.path.join(current_app.config['RESOURCE_IMG'], user.avatar_name))
    user.avatar_name = savename
    db.session.add(user)
    db.session.commit()
  return jsonify({
    'res': 'success',
    'user': user.to_json()
  })

@api.route('/get_avatar/<avatar_name>')
def get_avatar(avatar_name):
  response = Response(open(os.path.join(current_app.config['RESOURCE_IMG'], avatar_name), 'rb'),
    mimetype='image/' + avatar_name.split('.')[-1])
  return response