from flask import Flask
from flask_restful import Api
from root.test.basictest import SimpleTest

from root.api.endpoint import EndpointExample

# Lanzado de la app #gunicorn -c gunicorn_conf.py wsgi:app -D


def create_app(name):
    app = Flask(name)
    return app


app = create_app(__name__)
api = Api(app)


# Test
api.add_resource(SimpleTest, '/test')
# API
api.add_resource(EndpointExample, '/example-endpoint')

if __name__ == "__main__":
    #logging.basicConfig(filename='centryContaline.log', level=logging.DEBUG)
    app.run(port=8080, debug=True, host="0.0.0.0")
