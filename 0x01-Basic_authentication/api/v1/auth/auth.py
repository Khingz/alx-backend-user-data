#!/usr/bin/env python3
"""Comment
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Comment
        """
        if path is None or excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
        if path.endswith('/'):
            path = path
        else:
            path = '{}/'.format(path)
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Comment
        """
        if request is None or 'Authorization' not in request.header:
            return None
        return request.header['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Coment
        """
        return None
