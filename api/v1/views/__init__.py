#!/usr/bin/python3
""" Blueprint for the api"""
from flask import Blueprint

# Create a variable app_views which is an instance of Blueprint  (url /api/v1)
app_views = Blueprint('app_view', __name__, url_prefix='/api/v1')

# wildcard import of everything in the package
from api.v1.views.index import *
