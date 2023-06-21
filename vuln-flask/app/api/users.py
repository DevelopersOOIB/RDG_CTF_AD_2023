from functools import wraps

from flask import jsonify, request, url_for, make_response, abort
from lxml import etree

from app import elasticsearch, api, db
from app.models import User
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request, not_found


@bp.route('/profile/<int:uid>', methods=['PUT'])
@token_auth.login_required
def change_profile(uid):
    if token_auth.current_user().id != uid:
        abort(403)

    current_user = User.query.get_or_404(uid)
    xml = request.get_data()
    parser = etree.XMLParser(no_network=False)
    try:
        root = etree.fromstring(xml, parser=parser)
        user = root.xpath('user')[0]
        username = user.xpath('username/text()')[0] if user.xpath('username/text()') else ''
        email = user.xpath('email/text()')[0] if user.xpath('email/text()') else ''
        bio = user.xpath('bio/text()')[0] if user.xpath('bio/text()') else ''
    except Exception as e:
        return bad_request(f"Cannot parse the xml: {e}")

    if username and username != current_user.username and User.query.filter_by(username=username).first():
        return bad_request('please use a different username')
    if email and email != current_user.email and User.query.filter_by(email=email).first():
        return bad_request('please use a different email address')
    current_user.username = username
    current_user.email = email
    current_user.bio = bio
    db.session.commit()
    response = make_response(etree.tostring(root))
    response.status_code = 201
    response.headers["Content-Type"] = "application/xml"
    return response

