import os
import jwt

#Imports from other files
from models import db, Observer, City, Observation, Weather
from errors import handle_not_found_error, handle_internal_server_error
from verification import verify_access_token
from utils.api_checker import *


# Dependencies Imports from libraries
from jwt import encode
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash


#____________________HOME (/dir) EndPoint
def index():
    return jsonify(
        {
        'message': 'Welcome to GreenAware', 
        'status_code': 200
        })

# __________________OBSERVER ACCOUNT CREATION
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user_role = "observer"

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    user = Observer.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = Observer(username=username, password=hashed_password, user_role=user_role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'status_code': 200})

# __________________OBSERVER LOGIN
def login():
    try:
        # Extract username and password from request data
        username = request.json.get('username')
        password = request.json.get('password')

        # Validate username and password
        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        # Retrieve observer from database
        observer = Observer.query.filter_by(username=username).first()

        # Check if observer exists and password is correct
        if not observer or not check_password_hash(observer.password, password):
            return jsonify({'message': 'Invalid username or password'}), 401

        # Generate JWT token
        payload = {
            'user': observer.username,
            'exp': datetime.utcnow() + timedelta(hours=1)  # Token expiration time
        }
        token = jwt.encode(payload, os.getenv('ACCESS_TOKEN_KEY'), algorithm='HS256')

        return jsonify({'username':username,'access_token': token}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500




# __________________ SEE LIST OF ALL OBSERVERS
def get_observers():
    observers = Observer.query.all()
    return jsonify([observer.to_dict() for observer in observers])


# __________________OBSERVER ADD A NEW CITY
def add_city():
    try:
        # Extract city data from request
        data = request.json

        # Create a new city object
        new_city = City(
            city=data['city'],
            country=data['country'],
            timezone_offset=data['timezone_offset'],
            latitude=data['latitude'],
            longitude=data['longitude']
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





#_____________________ ADD OBSERVATION CONTOLLER
def add_observation():
    try:
        # Extract observation data from request
        data = request.json

        # Check if the city name exists in the cities table
        city = City.query.filter_by(city=data['city_name']).first()
        if not city:
            return jsonify({'message': 'City not found'}), 404

        # Convert date and time strings to datetime objects
        date = datetime.strptime(data['date'], "%Y-%m-%d").date()
        time = datetime.strptime(data['time'], "%H:%M:%S").time()

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
            weather_id=data['weather_id']
        )

        # Add the new observation to the database
        db.session.add(new_observation)
        db.session.commit()

        return jsonify({'message': 'Observation added successfully'}), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500


# ____________________________________GET ALL OBSERVATIONS
def get_observations():
    observations = Observation.query.all()
    return jsonify([observations.to_dict() for observations in observations])


#______________________________________________GET OBSERVATION BY ID
def get_observations_by_city(city_name, api_key):
    try:
        
        # print(api_key)
        # print(city_name)

        if not api_key:
            return jsonify({'message': 'API key is required'}), 400

        # Check if API key is valid
        if not check_api_key(api_key):
            return jsonify({'message': 'Invalid API key'}), 401
        
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
                'city_name': {
                    'city': observation.city.city,
                    'country': observation.city.country
                },
                'weather': {
                    'main': observation.weather.main,
                    'description': observation.weather.description
                }
            }

            return jsonify(observation_data), 200
        else:
            return jsonify({'message': 'Observation not found for city: {}'.format(city_name)}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500




# ____________________________________GET ALL SYSTEM WEATHER
def get_weather():
    weather = Weather.query.all()
    return jsonify([weather.to_dict() for weather in weather])

# ____________________________________OBSERVER ADD A NEW WEATHER
def add_weather():
    weather_data = request.json
    if not weather_data:
        return jsonify({'message': 'Weather Data is required'}), 400

    # Create a new Weather object
    weather = Weather( main=weather_data.get('main'), description=weather_data.get('description'))

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
