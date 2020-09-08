from serv import db
from flask import url_for, jsonify, current_app
from datetime import datetime

class Comment(db.Model):
  __tablename__ = 'comments'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(256), unique=True)
  content = db.Column(db.String(2048))
  read = db.Column(db.Boolean, default=False)
