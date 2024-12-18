#!/usr/bin/env python3
"""auth module"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """auth requird"""
        if path is None:
            return True
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        path = path.rstrip('/')

        for ex_path in excluded_paths:
            if ex_path.endswith('*'):
                if path.startswith(ex_path.rstrip('*')):
                    return False
            if ex_path.rstrip('/') == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """auth header"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None

        session_name = getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
