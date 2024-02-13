#!/usr/bin/env python3
"""Comment
"""
from flask import request
from typing import List, TypeVar
from .auth import Auth
import base64


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
