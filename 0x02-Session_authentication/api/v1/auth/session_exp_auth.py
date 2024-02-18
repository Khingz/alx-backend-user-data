#!/usr/bin/env python3
"""Comment
"""
import os
from .session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Seesion Expiration Auth Class
    """
    def __init__(self):
        """init method
        """
        try:
            duration = os.environ.get('SESSION_DURATION')
            self.session_duration = int(duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """creates a session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
            }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Comment
        """
        if session_id is None:
            return None
        sess_dict = self.user_id_by_session_id.get(session_id, None)
        if sess_dict is None:
            return None
        if self.session_duration < 1:
            return session_dictionary.get('user_id')
        created_at = sess_dict.get('created_at')
        if created_at is None:
            return None
        exp = created_at + timedelta(seconds=self.session_duration)
        if exp < datetime.now():
            return None
        return sess_dict.get('user_id')
