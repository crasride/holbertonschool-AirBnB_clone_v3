#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


# create routes for objects taht return json status
@app_views.route('/status', strict_slashes=False)
def status():
    """ status code """
    return jsonify({'status': 'OK'})


# create routes for objects
list_classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
    }


# Create an endpoint that retrieves the number of each objects by type
@app_views.route('/stats', strict_slashes=False)
def objects():
    """ objects endpoint """
    count_dict = {}
    for name, cls in list_classes.items():
        count = storage.count(cls)
        count_dict[name] = count
    return jsonify(count_dict)
