#!/usr/bin/env python3
"""Comment
"""
from flask import request
from typing import List, TypeVar, Tuple
from .auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """Comment
        """
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        auth_head = authorization_header.split()
        if auth_head[1] and len(auth_head[1]) > 0:
            return auth_head[1]
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str,
            ) -> str:
        """Commnt
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            b = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
            return b.decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str,
            ) -> Tuple[str, str]:
        """Commnt
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(':', 1)
        return (credentials[0], credentials[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Comment
        """
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        try:
            found_users = User.search({'email': user_email})
        except Exception:
            return None
        for user in found_users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and retrieves the User instance for a request """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        encoded = self.extract_base64_authorization_header(auth_header)
        if not encoded:
            return None
        decoded = self.decode_base64_authorization_header(encoded)
        if not decoded:
            return None
        email, pwd = self.extract_user_credentials(decoded)
        if not email or not pwd:
            return None
        user = self.user_object_from_credentials(email, pwd)
        return user
