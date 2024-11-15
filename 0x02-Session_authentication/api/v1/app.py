#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = getenv("AUTH_TYPE")

# Initialize auth variable to None
if auth_type == "auth":
    auth = Auth()
elif auth_type == "basic_auth":
    # if auth type is basic auth use basic auth class
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authirized(error) -> str:
    """not authorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """authorized but shouldn't be here function
    """
    return jsonify({"error": "Forbidden"}), 403


@app.route('/unauthorized')
def unauthorized_route():
    """triggers abort 401
    """
    abort(401)


@app.route('/forbidden')
def forbidden_function():
    """forbidden url
    """
    abort(403)


@app.before_request
def before_request_func():
    """Filtering each request
    """
    if auth is None:
        return
    excluded_path = ['/api/v1/status/',
                     '/api/v1/unauthorized/',
                     '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_path):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
