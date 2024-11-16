#!/usr/bin/env python3
"""Initialize views module
"""
from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
"""
Initialize views module
======================

This module initializes the views module which contains the routes of
the API
"""


User.load_from_file()
