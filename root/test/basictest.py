from flask_restful import Resource
from root.utils.response import PING, PONG
import jsonify


class SimpleTest(Resource):
    def get(self):
        return jsonify({"Message": PING})

    def post(self):
        return jsonify({"Message": PONG})
