#Imports from other files
from models import db, Observation
from utils.error_handler import *
from sqlalchemy import func
from utils.api_key_checker import *


# Dependencies Imports from libraries
from flask import request, jsonify


#______________________________________________GET OBSERVATION BY CITY NAME
def get_observations_by_city():
    api_key = request.args.get('api_key')
    if not api_key:
        return jsonify({'error': 'API Key is missing'}), 400
    
    response = check_api_key(api_key)
    if not response[0]:
        return jsonify({'message': 'Invalid API key'}), 401
    else:
        key_data = response[1]
        user_id = key_data['user_id']
        api_key = key_data['api_key']

    if key_data['calls'] >= key_data['quota_allotted']:
        return jsonify({'message': 'You Have Used Up Your Allotted Quota, Please Upgrade Your Plan'}), 401
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
            register_call(user_id, api_key)
            return jsonify(observation_data), 200

        else:
            return jsonify({'message': f'Observation not found for city: {city_name}', 'status_code': 404}), 404

    except Exception as e:
        return jsonify({'message': str(e), 'status_code': 500}), 500