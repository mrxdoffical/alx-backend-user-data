#!/usr/bin/env python3
""" Basic authentication module """
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ gets bas64 headers
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
        self,
            base64_authorization_header: str) -> str:
        """ Base64 decode
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                     str) -> (str, str):
        """extracting user data
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_credentials = decoded_base64_authorization_header.split(':', 1)
        return user_credentials[0], user_credentials[1]

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns user instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        if not users or len(users) == 0:
            return None
        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User
        """
        epa = self.extract_base64_authorization_header()
        auth_head = self.authorization_header(request)
        if auth_head is None:
            return None

        base64_header = self.extract_base64_authorization_header(auth_head)
        if base64_header is None:
            return None

        decoded_header = self.decode_base64_authorization_header(auth_head)
        if decoded_header is None:
            return None

        user_email, user_password = epa(decoded_header)
        if user_email is None or user_password is None:
            return None

        return self.user_object_from_credentials(user_email, user_password)
