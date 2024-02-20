#!/usr/bin/env python3
""" Comment
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Comment
    """
    b_password = password.encode('utf-8')
    return bcrypt.hashpw(b_password, bcrypt.gensalt())


class Auth:
    """Class for user authentication
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Handles user registration
        """
        if email and password:
            try:
                user = self._db.find_user_by(email=email)
                raise ValueError('User {} already exists'.format(email))
            except NoResultFound:
                hashed_pwd = _hash_password(password)
                new_user = self._db.add_user(email, hashed_pwd)
                return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ checks for valid password
        """
        if email and password:
            try:
                user = self._db.find_user_by(email=email)
                user_pwd = user.__dict__.get('hashed_password')
                if bcrypt.checkpw(password.encode('utf-8'), user_pwd):
                    return True
                return False
            except Exception:
                return False

    def _generate_uuid():
        """ Generates uuid string
        """
        return uuid.uuid4()
