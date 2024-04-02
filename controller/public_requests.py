#Imports from other files
from models import db, Observation
from utils.error_handler import *
from utils.api_key_checker import check_api_key


# Dependencies Imports from libraries
from flask import request, jsonify


#______________________________________________GET OBSERVATION BY CITY NAME
def get_observations_by_city():
    try:
        
        # print(api_key)
        # print(city_name)

        # Proceed with further processing for getting observations
        city_name = request.args.get('city_name')
        
        # Query the database for the observation with the specified city name
        observation = Observation.query.join(City).filter(City.city == city_name).first()

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
                    'city': observation.city.city,
                    'country': observation.city.country,
                    'timezone_offset': observation.city.timezone_offset,
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
            return jsonify({'message': 'Observation not found for city: {}'.format(city_name)}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500
