#!/usr/bin/env python3
"""Comment
"""
from flask import request
from typing import List, TypeVar
from .auth import Auth


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
