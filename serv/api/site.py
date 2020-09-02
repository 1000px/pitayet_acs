from serv.api import api
from flask import jsonify, request, url_for, abort
from serv.models import Site
from serv import db

@api.route('/sites/')
def get_sites():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 9, type=int)
    user_id = request.args.get('user_id', None, type=int)
    query = Site.query
    if user_id is None:
        query.filter_by(user_id=user_id)
    pagination = query.paginate(
        page,
        per_page=per_page,
        error_out=False
    )
    sites = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_sites', page=page-1, per_page=per_page)
    next = None
    if pagination.has_next:
        next = url_for('api.get_sites', page=page+1, per_page=per_page)

    return jsonify({
        'sites': [site.to_json() for site in sites],
        'prev_url': prev,
        'next_url': next,
        'total': pagination.total
    })