#!/usr/bin/env python3
"""Comment
"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """Session Auth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create session method
        """
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """session id
        """
        if session_id is None or type(session_id) != str:
            return None
        session = user_id_by_session_id.get(session_id, None)
        return session