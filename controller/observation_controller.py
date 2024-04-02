#Imports from other files
from models import db, Observer, City, Observation
from utils.w3w_generator import get_w3w_address
from utils.error_handler import handle_not_found_error, handle_internal_server_error


# Dependencies Imports from libraries
from flask import request, jsonify
from datetime import datetime
from flask_jwt_extended import get_jwt_identity


#_____________________ ADD OBSERVATION CONTOLLER
def add_observation():
    try:
        #check if authenticated
        current_user = get_jwt_identity()

        if not current_user:
            return jsonify({'message': 'Unauthorized'}), 403

        data = request.json

        # Check if the city name exists in the cities table
        city = City.query.filter_by(city=data['city_name']).first()
        if not city:
            return jsonify({'message': 'City not found'}), 404

        # Convert date and time strings to datetime objects
        date = datetime.strptime(data['date'], "%Y-%m-%d").date()
        time = datetime.strptime(data['time'], "%H:%M:%S").time()

        w3w_address = get_w3w_address(data['longitude'], data['latitude'])

        # Create a new observation object
        new_observation = Observation(
            date=date,
            time=time,
            temperature_land_surface=data['temperature_land_surface'],
            temperature_sea_surface=data['temperature_sea_surface'],
            humidity=data['humidity'],
            wind_speed=data['wind_speed'],
            wind_direction=data['wind_direction'],
            precipitation=data['precipitation'],
            haze=data['haze'],
            city_name=data['city_name'],
            weather_id=data['weather_id'],
            w3w_address = w3w_address,
            longitude=data['longitude'],
            latitude=data['latitude']
        )

        # Add the new observation to the database
        db.session.add(new_observation)
        db.session.commit()

        return jsonify({'message': 'Observation added successfully'}), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500



# ____________________________________GET ALL OBSERVATIONS
def get_observations():
    #check if authenticated
    current_user = get_jwt_identity()

    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 403
        
    observations = Observation.query.all()
    return jsonify([observations.to_dict() for observations in observations])
