#!/usr/bin/env python3
"""
Session Authentication Views Module
================================

This module contains the views/routes for the session authentication system:
    - /auth_session/login: Handles user login and session creation
    - /auth_session/logout: Handles user logout and session destruction

Each route is properly documented with its purpose, parameters,
and possible return values and status codes.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    POST /api/v1/auth_session/login
    ==============================
    Handles user login and creates a new session.

    Form Parameters:
        - email: User's email address
        - password: User's password

    Returns:
        - 400: If email or password is missing
            {"error": "email missing"}
            {"error": "password missing"}
        - 404: If no user is found for the email
            {"error": "no user found for this email"}
        - 401: If the password is incorrect
            {"error": "wrong password"}
        - 200: If login is successful
            {User object JSON} + Set-Cookie header
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """
    DELETE /api/v1/auth_session/logout
    ================================
    Handles user logout by destroying the session.

    Returns:
        - 404: If the session could not be destroyed
            {"error": "Not found"}
        - 200: If logout is successful
            {}
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
