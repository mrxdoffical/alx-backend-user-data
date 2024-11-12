#!/usr/bin/env python3
""" Basic authentication module """
from api.v1.auth.auth import Auth
import base64


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
