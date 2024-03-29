#!/usr/bin/env python3
""" Comment
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello():
    """Hello route
    """
    data = {'message': 'Bienvenue'}
    return jsonify(data)


@app.route('/users', methods=['POST'])
def users():
    """register a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        try:
            user = AUTH.register_user(email, password)
            data = {'email': email, 'message': 'user created'}
            return jsonify(data), 200
        except ValueError:
            data = {'message': 'email already registered'}
            return jsonify(data), 400


@app.route('/sessions', methods=['POST'])
def login():
    """ Handles login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        valid = AUTH.valid_login(email, password)
        if valid:
            session_id = AUTH.create_session(email)
            data = jsonify({'email': email, 'message': 'logged in'})
            data.set_cookie('session_id', session_id)
            return data
        abort(401)
    abort(400)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """ Handle logout functionality
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('hello'))


@app.route('/profile', methods=['GET'])
def profile():
    """ Comment
    """
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    msg = {"email": user.email}
    return jsonify(msg), 200


@app.route('/reset_password', methods=['POST'])
def reset_password():
    """ reset password token
    """
    email = request.form.get('email')
    if email:
        try:
            reset_token = AUTH.get_reset_password_token(email)
        except ValueError:
            abort(403)
        msg = {"email": email, "reset_token": reset_token}
        return jsonify(msg), 200
    abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """ Updates user pasword using token
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    if email and reset_token and new_password:
        try:
            AUTH.update_password(reset_token, new_password)
        except ValueError:
            abort(403)
        msg = {"email": email, "message": "Password updated"}
        return jsonify(msg), 200
    abort(400)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
