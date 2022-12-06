#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import jsonify

# create routes for objects taht return json status
@app_views.route('/status', strict_slashes=False)
def status():
    """ status code """
    return jsonify({'status': 'OK'})

