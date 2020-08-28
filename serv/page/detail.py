from serv.page import page

@page.route('/detail')
def detail():
    return '<h2>Hello, Detail</h2>'