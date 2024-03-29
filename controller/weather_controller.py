import os
import jwt

#Imports from other files
from models import db, Weather, Observer
from utils.error_handler import handle_not_found_error, handle_internal_server_error
from utils.verification import verify_access_token


# Dependencies Imports from libraries
from flask import request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, jwt_required


# ____________________________________GET ALL SYSTEM WEATHER
def get_weather():
    current_user = get_jwt_identity()
    
    observers = Observer.query.all()

    if current_user not in observers:
        return jsonify({'message': 'Invalid observer'}), 401

    weather = Weather.query.all()
    return jsonify([weather.to_dict() for weather in weather])

# ____________________________________OBSERVER ADD A NEW WEATHER
def add_weather():
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
