#!/usr/bin/python3
""" Blueprint for the api"""
from flask import Blueprint

# Create a variable app_views which is an instance of Blueprint  (url /api/v1)
app_views = Blueprint('app_view', __name__, url_prefix='/api/v1')

# wildcard import of everything in the package
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
