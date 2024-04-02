#Imports from other files
from models import db, City
from utils.verification import *
from utils.error_handler import handle_not_found_error, handle_internal_server_error

# Dependencies Imports from libraries
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import IntegrityError


# __________________OBSERVER ADD A NEW CITY
def add_city():
    try:
        verify_observer()

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

    # If city name already exists in the database
    except IntegrityError:
        return jsonify({'message': 'City name already exists'}), 400

    except Exception as e:
        return jsonify({'message': str(e)}), 500


# __________________ SEE LIST OF ALL CITIES
def view_cities():
    verify_observer()
    cities = City.query.all()
    return jsonify([cities.to_dict() for cities in cities])


# __________________ SEE UPDATE CITY BY ID
def update_city(id):
    try:
        verify_observer()

        # Get the updated data for the city from the request
        updated_data = request.json

        # Query the city by its ID
        city = City.query.get(id)

        # Check if the city exists
        if city:
            # Update the city attributes with the new data
            city.city = updated_data.get('city', city.city)
            city.country = updated_data.get('country', city.country)
            # Add more fields to update as needed

            # Commit changes to the database
            db.session.commit()

            return jsonify({'message': 'City updated successfully'}), 200
        else:
            return jsonify({'message': 'City not found'}), 404

    # If city the new city name exists in the database
    except IntegrityError:
        return jsonify({'message': 'City name already exists'}), 400

    except Exception as e:
        return jsonify({'message': str(e)}), 500


# __________________ DELETE A CITY BY ID
def delete_city(id):
    try:
        verify_observer()

        # Query the city by its ID
        city = City.query.get(id)

        # Check if the city exists
        if city:
            # Delete the city from the database
            db.session.delete(city)
            db.session.commit()

            return jsonify({'message': 'City deleted successfully'}), 200
        else:
            return jsonify({'message': 'City not found'}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500