#!/usr/bin/python3
""" Module APi Users """
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models import storage
from models.user import User


# Retrieves the list of all User objects: GET /api/v1/users
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ List all Users"""
    list_users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(list_users)


# Retrieves a User object: GET /api/v1/users/<user_id>
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def ret_user_id(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


# Deletes a User object:: DELETE /api/v1/users/<user_id>
@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    n_dict = storage.get(User, user_id)
    if n_dict is None:
        abort(404)
    storage.delete(n_dict)
    storage.save()
    return jsonify({}), 200


# Creates a User: POST /api/v1/users
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_new_user():
    """Creates users"""
    opc_request = request.get_json()
    if opc_request is None:
        return 'Not a JSON', 400
    if 'email' not in opc_request:
        return 'Missing email', 400
    if 'password' not in opc_request:
        return 'Missing password', 400
    n_user = User(**opc_request)
    n_user.save()
    return jsonify(n_user.to_dict()), 201


# Updates a User object: PUT /api/v1/users/<user_id>
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    """ Update User"""
    n_dict = storage.get(User, user_id)
    if n_dict is None:
        abort(404)
    opc_request = request.get_json()
    if opc_request is None:
        return 'Not a JSON', 400
    for key in ('id', 'email', 'created_at', 'updated_at'):
        opc_request.pop(key, None)
    for key, value in opc_request.items():
        setattr(n_dict, key, value)
    storage.save()
    return jsonify(n_dict.to_dict()), 200
