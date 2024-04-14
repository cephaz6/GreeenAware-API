#Imports from other files
from models import db, Observation
from utils.error_handler import *


# Dependencies Imports from libraries
from flask import request, jsonify


#______________________________________________GET OBSERVATION BY CITY NAME
def get_observations_by_city():
    try:
        # Extract city name from request query parameters
        city_name = request.args.get('city_name')

        # Query the database for the observation with the specified city name
        observation = Observation.query.filter_by(city_name=city_name).first()

        # Check if the observation exists
        if observation:
            # Serialize the observation data
            observation_data = {
                'date': str(observation.date),
                'time': str(observation.time),
                'temperature_land_surface': observation.temperature_land_surface,
                'temperature_sea_surface': observation.temperature_sea_surface,
                'humidity': observation.humidity,
                'wind_speed': observation.wind_speed,
                'wind_direction': observation.wind_direction,
                'precipitation': observation.precipitation,
                'haze': observation.haze,
                'location': {
                    'city': observation.city_name,
                    'country': observation.country,
                    'timezone_offset': observation.timezone_offset,
                    'longitude': observation.longitude,
                    'latitude': observation.latitude,
                    'what3words': observation.w3w_address,
                },
                'Weather Condition': {
                    'main': observation.weather.main,
                    'description': observation.weather.description
                }
            }
            return jsonify(observation_data), 200
        else:
            return jsonify({'message': f'Observation not found for city: {city_name}', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'message': str(e), 'status_code': 500}), 500