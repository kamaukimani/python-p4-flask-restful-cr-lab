#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        # Return a list of all plants in the database
        plants = Plant.query.all()
        response_dict_list = [plant.to_dict() for plant in plants]
        return make_response(jsonify(response_dict_list), 200)

    def post(self):
        # Create a new plant using data from the request
        data = request.get_json()  # Get data as JSON from the body
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(jsonify(new_plant.to_dict()), 201)


class PlantByID(Resource):
    def get(self, id):
        # Get a specific plant by ID
        plant = Plant.query.get(id)
        if plant is None:
            return make_response(jsonify({'message': 'Plant not found'}), 404)

        return make_response(jsonify(plant.to_dict()), 200)


# Add resources to the API
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
