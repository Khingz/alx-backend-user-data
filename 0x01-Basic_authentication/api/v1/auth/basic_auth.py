#!/usr/bin/env python3
"""Comment
"""
from flask import request
from typing import List, TypeVar
from .auth import Auth


class BasicAuth(Auth):
    """BasicAuth class
    """
