#!/usr/bin/env python3
""" Comment
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    """Hello route
    """
    data = {'message': 'Bienvenue'}
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
