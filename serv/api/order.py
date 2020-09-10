from serv.plugins.alipay import AliPlay
from serv.api import api
from flask import jsonify

def aliPay():
    obj = AliPlay(
        # 20210001166900315
        # appid = '2021001192692399',
        appid = '2021000116690035',
        app_notify_url = 'http://127.0.0.1:5000/api/v1/pay-finished',
        return_url = 'http://127.0.0.1:8080/#/mng/web-building/',
        alipay_public_key_path = 'keys/alipay_public_key',
        app_private_key_path = 'keys/app_private_key',
        debug = False
    )

    return obj
@api.route('/pay-url')
def get_pay_url():
    url = aliPay().direct_pay(
        subject = '123456',
        out_trade_no = '202009091222',
        total_amount = 1,
        return_url = 'http://127.0.0.1:8080/#/mng/web-build/'
    )

    re_url = 'https://openapi.alipaydev.com/gateway.do?{0}'.format(url)
    return jsonify({
        'url': re_url
    })
