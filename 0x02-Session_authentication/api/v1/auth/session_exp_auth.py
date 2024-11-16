#!/usr/bin/env python3
"""
Session Expiration Module
=======================

This module extends the SessionAuth class to add session expiration
functionality. It uses an environment variable SESSION_DURATION to
determine how long a session should remain valid.

If SESSION_DURATION is 0 or negative, the session never expires.
Otherwise, the session expires after SESSION_DURATION seconds from creation.
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Session Expiration Authentication Class
    ===================================

    This class extends SessionAuth to add session expiration.
    Each session stores its creation time and checks against
    SESSION_DURATION to determine if it's still valid.

    Attributes:
        session_duration (int): Number of seconds a session remains valid
        user_id_by_session_id (dict): Inherited from SessionAuth, stores
            session data including creation time
    """

    def __init__(self):
        """
        Initialize SessionExpAuth
        ======================

        Sets up session_duration from environment variable.
        If SESSION_DURATION is not set or invalid, defaults to 0
        (sessions never expire).
        """
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a new session with expiration
        ================================

        Creates a new session ID and stores both the user ID and
        creation timestamp.

        Args:
            user_id (str): The ID of the user to create a session for

        Returns:
            str: The new session ID if successful
            None: If session creation fails
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Get user ID if session is still valid
        =================================

        Checks if a session is still valid based on its creation time
        and session_duration.

        Args:
            session_id (str): The session ID to check

        Returns:
            str: The user ID if session is valid
            None: If session is invalid or expired
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        exp_time = created_at + timedelta(seconds=self.session_duration)
        if exp_time < datetime.now():
            return None

        return session_dict.get('user_id')
