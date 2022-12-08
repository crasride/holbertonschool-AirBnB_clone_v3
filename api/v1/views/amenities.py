#!/usr/bin/python3
"""
Create a new view for Amenity objects
that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models.amenity import Amenity
from models import storage


# Retrieves the list of all Amenity objects: GET /api/v1/amenities
@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ List All Amenities """
    a_dict = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(a_dict)


# Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>
@app_views.route('/amenities/<amenity_id>/',
                 methods=['GET'], strict_slashes=False)
def ret_amenity_id(amenity_id=None):
    """ Retrieves Amenity object """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        return abort(404)
    return jsonify(amenity_obj.to_dict())


# Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>
@app_views.route('/amenity/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_id(amenity_id):
    """Deletes Amenity id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


# Creates a Amenity: POST /api/v1/amenities
@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def create_post_amenity(amenity_id):
    """ Creates New Amenity """
    opc_reqst = request.get_json()
    if opc_reqst is None:
        return 'Not a JSON', 400
    if 'name' not in opc_reqst:
        return 'Missing name', 400
    n_amenity = Amenity(**opc_reqst)
    n_amenity.save()
    return jsonify(n_amenity.to_dict()), 201


# Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>
@app_views.route('/amenities/<amenity_id>/', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """"updates Amenity object"""
    n_dict = storage.get(Amenity, amenity_id)
    if n_dict is None:
        return abort(404)
    opc_reqst = request.get_json()
    if opc_reqst is None:
        return 'Not a JSON', 400
    for key in ('id', 'created_at', 'updated_at'):
        opc_reqst.pop(key, None)
    for key, value in opc_reqst.items():
        setattr(n_dict, key, value)
    n_dict.save()
    return jsonify(n_dict.to_dict()), 200
