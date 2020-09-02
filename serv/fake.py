from random import randint
from sqlalchemy.exc import IntegrityError
from serv import db
from serv.models import User, Section, Site
from faker import Faker

# 用户
def users(count=100):
    fake = Faker(locale='zh_CN')
    i = 0
    print('add users into user table')
    while i < count:
        u = User(
            username            = fake.user_name(),
            email               = fake.email(),
            password            = '123456'
        )
        db.session.add(u)
        i += 1
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

# 网站
def sites(count=100):
    fake = Faker(locale='zh_CN')
    count = User.query.count()
    i = 0
    while i < count:
        s = Site(
            sitename = fake.word(),
            desc = fake.sentence(),
            status = 1, 
            create_time = fake.date_time_between(start_date='-3y', end_date='-2y'),
            user = User.query.offset(randint(0, count - 1)).first()
        )
        db.session.add(s)
        i += 1
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    

# 时间区间
def sections(count=5):
    fake = Faker(locale='zh_CN')
    count = Site.query.count()
    i = 0
    while i < count:
        s = Section(
            from_time = fake.date_time_between(start_date='-2y', end_date='now'),
            to_time = fake.date_time_between(start_date='now'),
            site = Site.query.offset(randint(0, count - 1)).first()
        )
        db.session.add(s)
        i += 1
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()