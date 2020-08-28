from random import randint
from sqlalchemy.exc import IntegrityError
from serv import db
from serv.models import User
from faker import Faker

def users(count=100):
    fake = Faker(locale='zh_CN')
    i = 0
    while i < count:
        u = User(
            username            = fake.user_name(),
            email               = fake.email(),
            password            = '123456'
        )
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()
