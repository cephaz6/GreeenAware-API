import os
import jwt

#Imports from other files
from models import db, Weather
from utils.error_handler import handle_not_found_error, handle_internal_server_error
from utils.verification import *


# Dependencies Imports from libraries
from flask import request, jsonify


# ____________________________________GET ALL SYSTEM WEATHER
def get_weather():
    verify_observer()

    # Query all weather objects
    weather_objects = Weather.query.all()
    weather_dicts = [weather.to_dict() for weather in weather_objects]

    # Return JSON response with list of dictionaries
    return jsonify(weather_dicts), 200

# ____________________________________OBSERVER ADD A NEW WEATHER
def add_weather():
    #check if authenticated
    verify_observer()

    data = request.json
    if not data:
        return jsonify({'message': 'Weather Data is required'}), 400

    # Create a new Weather object
    weather = Weather( main=data.get('main'), description=data.get('description'))

    # Add city to the database
    db.session.add(weather)
    db.session.commit()

    return jsonify(
        {
            'message': 'Weather added successfully', 
            'id': weather.id, 
            'name': weather.main, 
            'desc': weather.description
        }), 201

#_______________________________________ OBSERVER OR ADMIN UPDATE WEATHER STRAIN
def update_weather(id):
    try:
        verify_observer()

        # Get the updated data for the weather from the request
        updated_data = request.json

        # Query the weather by its ID
        weather = Weather.query.get(id)

        # Check if the weather exists
        if weather:
            # Update the weather attributes with the new data
            weather.main = updated_data.get('main', weather.main)
            weather.description = updated_data.get('description', weather.description)

            # Commit changes to the database
            db.session.commit()

            return jsonify({'message': 'Weather updated successfully'}), 200
        else:
            return jsonify({'message': 'Weather Info not found'}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500


#________________________________________OBSERVER OR ADMIN DELETE WEATHER STRAIN
def delete_weather(id):
    try:
        #check if authenticated
        verify_observer()

        # Query the weather by its ID
        weather = Weather.query.get(id)

        # Check if the weather exists
        if weather:
            db.session.delete(weather)
            db.session.commit()

            return jsonify({'message': 'Weather deleted successfully'}), 200
        else:
            return jsonify({'message': 'Weather not found'}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500


def get_weather_notes():
    weather_objects = Weather.query.all()
    sorted_weather_objects = sorted(weather_objects, key=lambda x: x.main)
    
    # Convert sorted weather objects to dictionaries
    weather_dicts = [weather.to_dict() for weather in sorted_weather_objects]
    return jsonify(weather_dicts), 200
