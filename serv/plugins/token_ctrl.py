from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

def gen_token(code, expiration):
  s = Serializer(current_app.config['SECRET_KEY'], expiration)
  return s.dumps({'token': code}).decode('utf-8')

def verify_token(token, code):
  s = Serializer(current_app.config['SECRET_KEY'])
  print('verify token:', token)
  try:
    data = s.loads(token)
  except:
    return None
  
  return data['token'].lower() == code.lower()
