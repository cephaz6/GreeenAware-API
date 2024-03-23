import os
import jwt

#Imports from other files
from models import db, Observer, City, Observation, Weather
from errors import handle_not_found_error, handle_internal_server_error
from verification import verify_access_token


# Dependencies Imports from libraries
from jwt import encode
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash


#____________________HOME (/dir) EndPoint
def index():
    return jsonify({'message': 'Welcome to GreenAware', 'status_code': 200})

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
    # try:
        # Extract observer username and access token from request headers

        # observer_username = request.headers.get('user')
        # access_token = request.headers.get('access_token')

        # Verify access token and get observer

        # observer = verify_access_token(access_token)
        # if not observer:
        #     return jsonify({'message': 'Invalid access token'}), 401

        # Check if observer has permission to add city
        
        # if observer.username != observer_username:
        #     return jsonify({'message': 'Unauthorized'}), 403

        # Extract city data from request body
    city_data = request.json
    if not city_data:
        return jsonify({'message': 'City data is required'}), 400

    # Create a new city object
    city = City(city=city_data.get('city'), country=city_data.get('country'))

    # Add city to the database
    db.session.add(city)
    db.session.commit()

    return jsonify({'message': 'City added successfully', 'city_id': city.id}), 201

    # except Exception as e:
    #     return jsonify({'message': str(e)}), 500


# __________________ SEE LIST OF ALL CITIES
def view_city():
    cities = City.query.all()
    return jsonify([cities.to_dict() for cities in cities])



#_____________________ ADD OBSERVATION CONTOLLER
def add_observation():
    try:
        # Extract observation data from request body
        observation_data = request.json
        if not observation_data:
            return jsonify({'message': 'Observation data is required'}), 400
        
        date_str = observation_data.get('date')
        date_str = datetime.strptime(date_str, "%Y-%m-%d").date()

        time_str = observation_data.get('time')
        time_str = datetime.strptime(time_str, "%H:%M:%S").time()

        # Create a new observation object
        observation = Observation(
            date = date_str,
            time = time_str,
            timezone_offset=observation_data.get('timezone_offset'),
            latitude=observation_data.get('latitude'),
            longitude=observation_data.get('longitude'),
            temperature_land_surface=observation_data.get('temperature_land_surface'),
            temperature_sea_surface=observation_data.get('temperature_sea_surface'),
            humidity=observation_data.get('humidity'),
            wind_speed=observation_data.get('wind_speed'),
            wind_direction=observation_data.get('wind_direction'),
            precipitation=observation_data.get('precipitation'),
            haze=observation_data.get('haze'),
            city_id=observation_data.get('city_id'),
            weather_id=observation_data.get('weather_id')
        )

        # Add observation to the database
        db.session.add(observation)
        db.session.commit()

        return jsonify({'message': 'Observation added successfully', 'observation_id': observation.id}), 201

    except Exception as e:
        return jsonify({'message': str(e)}), 500

# ____________________________________GET ALL OBSERVATIONS
def get_observations():
    observations = Observation.query.all()
    return jsonify([observations.to_dict() for observations in observations])

#______________________________________________GET OBSERVATION BY ID
def get_observations_by_ids(weather_id, city_id):
    try:
        # Query observations with matching weather_id and city_id
        observations = Observation.query.filter_by(weather_id=weather_id, city_id=city_id).all()

        # Check if any observations were found
        if not observations:
            return jsonify({'message': 'No observations found for the specified IDs'}), 404

        # Serialize observations data to JSON
        observations_data = []
        for observation in observations:
            observation_data = {
                'id': observation.id,
                'date': str(observation.date),
                'time': str(observation.time),
                'timezone_offset': observation.timezone_offset,
                'latitude': observation.latitude,
                'longitude': observation.longitude,
                'temperature_land_surface': observation.temperature_land_surface,
                'temperature_sea_surface': observation.temperature_sea_surface,
                'humidity': observation.humidity,
                'wind_speed': observation.wind_speed,
                'wind_direction': observation.wind_direction,
                'precipitation': observation.precipitation,
                'haze': observation.haze,
                'city': {
                    'id': observation.city.id,
                    'city': observation.city.city,
                    'country': observation.city.country
                },
                'weather': {
                    'id': observation.weather.id,
                    'main': observation.weather.main,
                    'description': observation.weather.description
                }
            }
            observations_data.append(observation_data)

        return jsonify({'observations': observations_data}), 200

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
