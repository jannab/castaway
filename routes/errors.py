from flask import Blueprint, jsonify

from auth import AuthError

bp = Blueprint('errors', __name__)


@bp.app_errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400


@bp.app_errorhandler(401)
def unauthorized(e):
    return jsonify(error=str(e)), 401


@bp.app_errorhandler(403)
def unauthorized(e):
    return jsonify(error=str(e)), 403


@bp.app_errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@bp.app_errorhandler(405)
def not_allowed(e):
    return jsonify(error=str(e)), 405


@bp.app_errorhandler(409)
def not_allowed(e):
    return jsonify(error=str(e)), 409


@bp.app_errorhandler(422)
def unprocessable(e):
    return jsonify(error=str(e)), 422


@bp.app_errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500
