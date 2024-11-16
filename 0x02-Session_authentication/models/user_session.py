#!/usr/bin/env python3
"""
User Session Model Module
======================

This module defines the UserSession model for storing session information
in a database. It inherits from the Base model and adds fields for
tracking user sessions.
"""
from models.base import Base


class UserSession(Base):
    """
    User Session Model
    ================

    Stores information about user sessions in the database.

    Attributes:
        user_id (str): ID of the user who owns this session
        session_id (str): Unique identifier for this session
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a UserSession instance
        =============================

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        The following keys are expected in kwargs:
            - user_id: ID of the user who owns this session
            - session_id: Unique identifier for this session
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
