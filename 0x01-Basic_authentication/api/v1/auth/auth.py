#!/usr/bin/env python3
"""auth module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """auth requird"""
        return False

    def authorization_header(self, request=None) -> str:
        """auth header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
