#!/usr/bin/env python3
""" Comment
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Comment
    """
    b_password = password.encode('utf-8')
    return bcrypt.hashpw(b_password, bcrypt.gensalt())
