from serv.page import page
from flask import redirect
from alipay import AliPay
from alipay.utils import AliPayConfig


def aliPay():
    app_private_key_string = open('keys/app_private_2048.txt').read()
    alipay_public_key_string = open('keys/alipay_public_2048.txt').read()
    obj = AliPay(
        appid = '2021000116690035',
        app_notify_url = None,
        app_private_key_string = app_private_key_string,
        alipay_public_key_string = alipay_public_key_string,
        sign_type = 'RSA2',
        debug = True,
        config = AliPayConfig(timeout=15)
    )

    return obj

@page.route('/detail')
def detail():
    alipay = aliPay()
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no = '202009102728',
        total_amount = 0.01,
        subject = '测试订单',
        return_url = 'http://127.0.0.1:8080/#/mng/web-building',
        notify_url = 'http://127.0.0.1:5000/api/v1/pay-finished'
    )

    pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string

    return redirect(pay_url)