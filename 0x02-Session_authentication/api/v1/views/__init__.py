#!/usr/bin/env python3
"""
Views module initialization
=========================

This module initializes the views Blueprint and imports all view modules.
The Blueprint handles all routes for the Session Authentication API.

Imported views:
    - index: Basic API status endpoints
    - users: User management endpoints
    - session_auth: Session authentication endpoints
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

User.load_from_file()
