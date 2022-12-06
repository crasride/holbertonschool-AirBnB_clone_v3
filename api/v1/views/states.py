#!/usr/bin/python3
""" The API view for the module status object """
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models.state import State
from models import storage


# Retrieves the list of all State objects: GET /api/v1/states
@app_views.route('/states/', strict_slashes=False)
# Retrieves a State object: GET /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """ Return all states """
    if state_id is None:
        new_dict = [state.to_dict() for state in storage.all(State).values()]
        return jsonify(new_dict)
    else:
        """ Return a State object """
        new_dict = storage.get(State, state_id)
        if new_dict is None:
            abort(404)
        return jsonify(new_dict.to_dict())


# Deletes a State object:: DELETE /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deletes a state based on id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify({})), 200


# Creates a State: POST /api/v1/states
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_post_state(state_id=None):
    """ creates a new State """
    opc_request = request.get_json()
    if opc_request is None:
        return 'Not a JSON', 400
    if 'name' not in opc_request:
        return 'Missing name', 400
    n_state = State(**opc_request)
    n_state.save()
    return jsonify(n_state.to_dict()), 201


# Updates a State object: PUT /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """"updates a State object"""
    dict = storage.get(State, state_id)
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
