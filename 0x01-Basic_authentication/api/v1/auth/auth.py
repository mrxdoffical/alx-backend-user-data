#!/usr/bin/env python3
"""auth module"""
from flask import request
from typing import List, TypeVar


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
            if ex_path.rstrip('/') == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """auth header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
