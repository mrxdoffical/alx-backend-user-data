#!/usr/bin/env python3
"""
Session Authentication Module
==========================

This module implements session-based authentication functionality.
It provides a SessionAuth class that handles:
    - Session creation and ID generation
    - Mapping between session IDs and user IDs
    - Session validation and user retrieval
    - Session destruction for logout
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    Session Authentication Class
    =========================

    This class implements session-based authentication methods.
    It stores session information in memory using a dictionary.

    Attributes:
        user_id_by_session_id (dict): Maps session IDs to user IDs
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id
        ================================

        Args:
            user_id (str): The ID of the user to create a session for

        Returns:
            str: The generated session ID
            None: If user_id is None or not a string
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID
        ====================================

        Args:
            session_id (str): The session ID to look up

        Returns:
            str: The user ID associated with the session
            None: If session_id is None or not a string
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value
        ===========================================

        Args:
            request: Flask request object containing the session cookie

        Returns:
            User: Instance of the user if found
            None: If request is None or session/user not found
        """
        if request is None:
            return None

        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes the user session / logout
        ==============================

        Args:
            request: Flask request object containing the session cookie

        Returns:
            bool: True if the session was successfully destroyed
                 False if the request is invalid or session not found
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
