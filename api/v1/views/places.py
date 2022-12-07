#!/usr/bin/python3
""" Module APi Place """
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models import storage
from models.place import Place
from models.city import City
from models.state import State


# Retrieves the list of all Place objects of a City
@app_views.route('/cities/<city_id>/places/', methods=['GET'],
                 strict_slashes=False)
def get_all_place(city_id):
    """ list of all Objects in a City """
    list_city = storage.get(City, city_id)
    if list_city is None:
        abort(404)
    places_dict = [place.to_dict() for place in list_city.places]
    return jsonify(places_dict)


# Retrieves a Place object. : GET /api/v1/places/<place_id>
@app_views.route('/places/<place_id>/', methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


# Deletes a Place object: DELETE /api/v1/places/<place_id>
@app_views.route('/places/<place_id>/', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Delete Place for Id """
    n_dict = storage.get(Place, place_id)
    if n_dict is None:
        abort(404)
    storage.delete(n_dict)
    storage.save()
    return jsonify({}), 200


# Creates a Place: POST /api/v1/cities/<city_id>/places
@app_views.route('/cities/<city_id>/places/', methods=['POST'],
                 strict_slashes=False)
def create_place_city_id(city_id):
    """ Creates Place """
    if request.method == 'POST':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        opc_reqst = request.get_json()
        if opc_reqst is None:
            return 'Not a JSON', 400
        if 'user_id' not in opc_reqst:
            return 'Missing user_id', 400
        user = storage.get("User", opc_reqst.get("user_id"))
        if user is None:
            abort(404)
        if 'name' not in opc_reqst:
            return 'Missing name', 400
        opc_reqst['city_id'] = city_id
        n_place = Place(**opc_reqst)
        n_place.save()
        return jsonify(n_place.to_dict()), 201


# Updates a Place object: PUT /api/v1/places/<place_id>
@app_views.route('/places/<place_id>/', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Update Place Object """
    n_dict = storage.get(Place, place_id)
    if n_dict is None:
        abort(404)
    opc_reqst = request.get_json()
    if opc_reqst is None:
        return 'Not a JSON', 400
    for key in ('id', 'user_id', 'city_id', 'created_at', 'updated_at'):
        opc_reqst.pop(key, None)
    for key, value in opc_reqst.items():
        setattr(n_dict, key, value)
    n_dict.save()
    return jsonify(n_dict.to_dict()), 200
