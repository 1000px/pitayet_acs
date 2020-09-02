from serv import db
from flask import url_for, jsonify, current_app
from datetime import datetime

class Site(db.Model):
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    sitename = db.Column(db.String(128), unique=True)
    desc = db.Column(db.String(512))
    status = db.Column(db.Integer) # 1 运行中 2 暂停（待续费） 3 已清除
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)

    sections = db.relationship('Section', backref='site')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_json(self):
        return {
            'id': self.id,
            'sitename': self.sitename,
            'desc': self.desc,
            'status': self.status,
            'create_time': self.create_time,
            'sections': [section.to_json() for section in self.sections],
            'user_id': self.user_id
        }
