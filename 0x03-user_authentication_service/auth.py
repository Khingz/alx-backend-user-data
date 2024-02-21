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


def _generate_uuid() -> str:
    """ Generates uuid string
    """
    UUID = uuid.uuid4()
    return str(UUID)


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

    def create_session(self, email: str) -> str:
        """Create a session
        """
        if email:
            try:
                user = self._db.find_user_by(email=email)
            except Exception:
                return None
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Returns a user from a session
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: int):
        """ Destroy a session
        """
        if user_id:
            try:
                self._db.update_user(user_id, session_id=None)
            except Exception:
                return None

    def get_reset_password_token(self, email: str) -> str:
        """ Generate token
        """
        if email:
            try:
                user = self._db.find_user_by(email=email)
            except NoResultFound:
                raise ValueError
            reset_token = _geneate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
