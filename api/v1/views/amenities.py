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
@app_views.route('/amenities/', strict_slashes=False)
# Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>
# If the amenity_id is not linked to any Amenity object, raise a 404 error
@app_views.route('/states/<state_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenities(amenities_id=None):
    """ Return all amenities """
    if amenities_id is None:
        new_dict = [amenity.to_dict() for amenity in
                    storage.all(Amenity).values()]
        return jsonify(new_dict)
    else:
        """ Return a Amenity object """
        new_dict = storage.get(Amenity, amenities_id)
        if new_dict is None:
            abort(404)
        return jsonify(new_dict.to_dict())


# Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>
@app_views.route('/amenity/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes amenity based on id"""
    n_dict = storage.get(Amenity, amenity_id)
    # state = storage.get((state), amenity_id)
    if n_dict is None:
        abort(404)
    storage.delete(n_dict)
    storage.save()
    return (jsonify({})), 200


# Creates a Amenity: POST /api/v1/amenities
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_post_amenity(amenity_id=None):
    """ creates a new Amenity """
    opc_request = request.get_json()
    if opc_request is None:
        return 'Not a JSON', 400
    if 'name' not in opc_request:
        return 'Missing name', 400
    n_amenity = Amenity(**opc_request)
    n_amenity.save()
    return jsonify(n_amenity.to_dict()), 201


# Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>
@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """"updates Amenity object"""
    dict = storage.get(Amenity, amenity_id)
    if dict is None:
        abort(404)
    opc_request = request.get_json()
    if opc_request is None:
        return 'Not a JSON', 400
    for key in ('id', 'created_at', 'updated_at'):
        opc_request.pop(key, None)
    for key, value in opc_request.items():
        setattr(dict, key, value)
    dict.save()
    return jsonify(dict.to_dict()), 200
