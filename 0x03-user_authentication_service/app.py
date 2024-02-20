#!/usr/bin/env python3
""" Comment
"""
from flask import Flask, jsonify, request
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
            return jsonify(data)
        except ValueError:
            data = {'message': 'email already registered'}
            return jsonify(data), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
