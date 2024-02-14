#!/usr/bin/env python3
"""Comment
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class
    """
    def require_auth(
            self,
            path: str,
            excluded_paths: List[str]
            ) -> bool:
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
        for paths in excluded_paths:
            if paths.endswith('*') and path.startswith(
                    paths[:-1]
                    ):
                return False
            if not paths.endswith('*') and paths == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Comment
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Coment
        """
        return None
