#!/usr/bin/env python3
""" session Auth
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route(
        '/auth_session/login',
        methods=['POST'],
        strict_slashes=False
        )
def login():
    """Comment
    """
    email = request.form.get('email')
    if not email or email == '':
        msg = 'email missing'
        return jsonify({'error': msg}), 400
    password = request.form.get('password')
    if not password or password == '':
        msg = 'password missing'
        return jsonify({'error': msg}), 400
    try:
        found_users = User.search({'email': email})
    except Exception:
        msg = 'no user found for this email'
        return jsonify({"error": msg}), 404
    if not found_users:
        msg = 'no user found for this email'
        return jsonify({"error": msg}), 404
    for user in found_users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    user = found_users[0]
    session_id = auth.create_session(user.id)
    session_name = os.environ.get('SESSION_NAME')
    res = jsonify(user.to_json())
    res.set_cookie(session_name, session_id)
    return res


@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'],
        strict_slashes=False
        )
def logout():
    """logout user
    """
    from api.v1.app import auth
    session = auth.destroy_session(request)
    if session:
        return jsonify({}), 200
    abort(404)
