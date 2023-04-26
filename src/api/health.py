from flask import jsonify
from flask_restful import Resource

class Health(Resource):

    def __init__(self, **kwargs) -> None:
        pass

    def get(self):
        return jsonify({ 'api': 1, 'redis': 1})