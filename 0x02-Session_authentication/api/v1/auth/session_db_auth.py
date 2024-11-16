#!/usr/bin/env python3
"""
Session Database Authentication Module
=================================

This module implements session authentication with database storage.
It extends the SessionExpAuth class to store sessions in a database
instead of memory, providing persistence across application restarts.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    Session Database Authentication Class
    =================================

    This class extends SessionExpAuth to store session information
    in a database using the UserSession model.

    The sessions are still subject to expiration as defined in
    SessionExpAuth, but they persist across application restarts.
    """

    def create_session(self, user_id=None) -> str:
        """
        Create a new session and store it in the database
        ============================================

        Args:
            user_id (str): The ID of the user to create a session for

        Returns:
            str: The new session ID if successful
            None: If session creation fails
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        kwargs = {
            'user_id': user_id,
            'session_id': session_id,
        }
        user_session = UserSession(**kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        Get user ID from database session if still valid
        ==========================================

        Args:
            session_id (str): The session ID to look up

        Returns:
            str: The user ID if session is valid
            None: If session is invalid or expired
        """
        if session_id is None:
            return None

        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None

        if not sessions:
            return None

        user_session = sessions[0]

        if self.session_duration <= 0:
            return user_session.user_id

        created_at = user_session.created_at
        if created_at is None:
            return None

        exp_time = created_at + timedelta(seconds=self.session_duration)
        if exp_time < datetime.now():
            return None

        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """
        Destroy session from database
        =========================

        Args:
            request: Flask request object containing the session cookie

        Returns:
            bool: True if session was destroyed
                 False if session couldn't be found or destroyed
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False

        if not sessions:
            return False

        sessions[0].remove()
        return True
