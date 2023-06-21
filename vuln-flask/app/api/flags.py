from flask import jsonify, request, make_response, url_for

import app
from app import elasticsearch, api
from app.utils import insert, search
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request, not_found


@bp.route('/flags', methods=['POST'])
@token_auth.login_required
def create_flag():
    """
    This function is designed for an automated flag checking system.
    Please do not modify this code!
    """
    doc = request.get_json()
    if doc is None or doc.get('flag') is None or doc.get('created_at') is None:
        return bad_request('Flag cannot be empty')
    result = insert(doc)
    response = make_response(result)
    response.status_code = 201
    return response


@bp.route('/flags/<fid>', methods=['GET'])
@token_auth.login_required
def get_flag(fid):
    """
    This function is designed for an automated flag checking system.
    Please do not modify this code!
    """
    result = search(fid)
    response = make_response(result)
    response.status_code = 200
    return response


@bp.route('/flags/check_es', methods=['GET'])
@token_auth.login_required
def check_es():
    """
    This function is designed for an automated flag checking system.
    Please do not modify this code!
    """
    result = {'hostname': app.Config.ELASTICSEARCH_URL}
    response = make_response(result)
    response.status_code = 200
    return response
