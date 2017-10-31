from pygeppetto_server import PyGeppettoServer
from flask_restful import Resource, Api, abort, reqparse

from flask import Flask
from pygeppetto_blueprint import pygeppetto_core


app = Flask(__name__)
app.register_blueprint(pygeppetto_core, url_prefix='/')

api = Api(app)


class People(Resource):
    def get(self):
        print("WS: Getting People")
        return [
            {"name": "Matteo", "surname": "Cantarelli", "occupation": "Philisopher"},
            {"name": "Adrian", "surname": "Quintana", "occupation": "Guru"},
            {"name": "Giovanni", "surname": "Idilli", "occupation": "The Boss"},
        ]

    #curl -X POST http://localhost:5000/api/people
    def post(self):
        print("WS: Posting People")
        return "WS: Posting People"


api.add_resource(People, '/api/people')

if __name__ == "__main__":
    PyGeppettoServer(app).run()
