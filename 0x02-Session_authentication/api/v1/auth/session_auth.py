#!/usr/bin/env python3
"""Comment
"""
from .auth import Auth
import uuid
from models.user import User


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
        """returns user_id from session id
        """
        if session_id is None or type(session_id) != str:
            return None
        session = self.user_id_by_session_id.get(session_id, None)
        return session

    def current_user(self, request=None):
        """returns instance of current user
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        user = User.get(user_id)
        return user
