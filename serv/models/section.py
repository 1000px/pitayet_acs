from serv import db
from flask import url_for, jsonify, current_app

from datetime import datetime

# 正在运行的网站，一旦续费，在当前时间的基础上顺延
# 当网站停止运行，续费之后，原时间区间不再作用，重新开始一条记录
# 一个网站只有一个时间区间是有效的

class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    from_time = db.Column(db.DateTime())
    to_time = db.Column(db.DateTime())

    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))

    def to_json(self):
        return {
            'id': self.id,
            'from_time': self.from_time,
            'to_time': self.to_time,
            'site_id': self.site_id
        }
