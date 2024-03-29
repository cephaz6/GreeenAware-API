#Imports from other files
from models import db, Observer, City
from utils.error_handler import handle_not_found_error, handle_internal_server_error

# Dependencies Imports from libraries
from flask import request, jsonify


# __________________OBSERVER ADD A NEW CITY
def add_city():
    try:
        # Extract city data from request
        data = request.json

        # Create a new city object
        new_city = City(
            city=data['city'],
            country=data['country'],
            timezone_offset=data['timezone_offset']
        )

        # Add the new city to the database
        db.session.add(new_city)
        db.session.commit()

        return jsonify({'message': 'City added successfully'}), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500


# __________________ SEE LIST OF ALL CITIES
def view_city():
    cities = City.query.all()
    return jsonify([cities.to_dict() for cities in cities])