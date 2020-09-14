# from serv.plugins.alipay import AliPlay
from alipay import AliPay, DCAliPay, ISVAliPay
from alipay.utils import AliPayConfig
from serv.api import api
from flask import jsonify

def aliPay():
    app_private_key_string = open('keys/app_private_2048.txt').read()
    alipay_public_key_string = open('keys/alipay_public_2048.txt').read()
    obj = AliPay(
        # 20210001166900315
        # appid = '2021001192692399',
        appid = '2021000116690035',
        # app_notify_url = 'http://127.0.0.1:5000/api/v1/pay-finished',
        # return_url = 'http://127.0.0.1:8080/#/mng/web-building/',
        # alipay_public_key_path = 'keys/alipay_public_2048.txt',
        # app_private_key_path = 'keys/app_private_2048.txt',
        # debug = True
        app_notify_url = None,
        app_private_key_string = app_private_key_string,
        alipay_public_key_string = alipay_public_key_string,
        sign_type = 'RSA2',
        debug = True,
        config = AliPayConfig(timeout=15)
    )

    return obj
@api.route('/pay-url')
def get_pay_url():
    instance_aliPay = aliPay()
    # query_params = instance_aliPay.direct_pay(
    #     subject = '测试订单',
    #     out_trade_no = '202009091222',
    #     total_amount = '0.01'
    # )
    order_string = instance_aliPay.api_alipay_trade_page_pay(
        out_trade_no = '202009102728',
        total_amount = 0.01,
        subject = '测试订单',
        return_url = 'http://127.0.0.1:8080/#/mng/payload',
        notify_url = 'http://127.0.0.1:5000/api/v1/pay-finished'
    )

    pay_url = 'https://openapi.alipaydev.com/gateway.do?{0}'.format(order_string)
    return jsonify({
        'url': pay_url
    })

@api.route('/pay-finished')
def pay_finished():
    pass