#!/usr/bin/python3
""" Test class """
from models import *
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
# task 13
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


# you must remove the current connection
@app.teardown_appcontext
def close_session(exception):
    storage.close()


@app.errorhandler(404)
def resource_not_found(exception):
    """ display error page not found 404 message """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
