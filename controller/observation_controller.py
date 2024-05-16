#Imports from other files
from models import db, Observation, User
from utils.w3w_generator import *
from utils.verification import *
from utils.error_handler import *


# Dependencies Imports from libraries
from flask import request, jsonify
from datetime import datetime
from flask_jwt_extended import get_jwt_identity


#_____________________ ADD OBSERVATION CONTROLLER
def add_observation():
    try:
        # Check if authenticated
        # verify_observer()
        # current_user = get_jwt_identity()

        # user = User.query.filter_by(email=current_user).first()

        data = request.json
        print(data)

        # Convert date and time strings to datetime objects
        date = datetime.strptime(data['date'], "%Y-%m-%d").date()
        time = datetime.strptime(data['time'], "%H:%M:%S").time()

        # Generate what3words address based on latitude and longitude
        if not data.get('w3w_address'):
            return jsonify({'message': 'Please provide a W3W address'}), 400
        
        w3w_info = get_w3w_info(data['w3w_address'])

        coordinates = w3w_info["coordinates"]

        # Create a new observation object
        new_observation = Observation(
            date=date,
            time=time,
            observer_id = data['user_id'],
            temperature_land_surface=data['temperature_land_surface'],
            temperature_sea_surface=data['temperature_sea_surface'],
            timezone_offset=data['timezone_offset'],
            humidity=data['humidity'],
            wind_speed=data['wind_speed'],
            wind_direction=data['wind_direction'],
            precipitation=data['precipitation'],
            haze=data['haze'],
            weather_id=data['weather_id'],
            country =  w3w_info["country"],
            w3w_address=data['w3w_address'],
            city_name= w3w_info["nearest_place"],
            longitude=coordinates["lng"],
            latitude=coordinates['lat']
        )

        # Add the new observation to the database
        db.session.add(new_observation)
        db.session.commit()

        return jsonify({'message': 'Observation added successfully', 'status_code': 201}), 201

    except Exception as e:
        print(e)
        return jsonify({'message': str(e), 'status_code': 500}), 500


#_____________________ ADD BULK OBSERVATION CONTROLLER
def add_bulk_observations():
    try:
        # Check if authenticated
        verify_observer()

        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        data = request.json
        
        print(data)
        # Check if observations key exists in the JSON data
        if 'observations' not in data:
            return jsonify({'message': 'No observations found in the request data'}), 400
        
        # Extract observations from the JSON data
        observations = data['observations']
        
        # Check if observations is a list
        if not isinstance(observations, list):
            return jsonify({'message': 'Observations must be provided as a list'}), 400
        
        # Iterate over each observation in the list
        for obs_data in observations:
            # Convert date and time strings to datetime objects
            date = datetime.strptime(obs_data['date'], "%Y-%m-%d").date()
            time = datetime.strptime(obs_data['time'], "%H:%M:%S").time()

            # Generate what3words address based on latitude and longitude
            if not obs_data.get('w3w_address'):
                return jsonify({'message': 'Please provide a W3W address'}), 400
            
            w3w_info = get_w3w_info(obs_data['w3w_address'])

            coordinates = w3w_info["coordinates"]

            # Create a new observation object
            new_observation = Observation(
                date=date,
                time=time,
                observer_id=user.user_id,
                temperature_land_surface=obs_data['temperature_land_surface'],
                temperature_sea_surface=obs_data['temperature_sea_surface'],
                timezone_offset=obs_data['timezone_offset'],
                humidity=obs_data['humidity'],
                wind_speed=obs_data['wind_speed'],
                wind_direction=obs_data['wind_direction'],
                precipitation=obs_data['precipitation'],
                haze=obs_data['haze'],
                weather_id=obs_data['weather_id'],
                country=w3w_info["country"],
                w3w_address=obs_data['w3w_address'],
                city_name=w3w_info["nearest_place"],
                longitude=coordinates["lng"],
                latitude=coordinates['lat']
            )

            # Add the new observation to the database
            db.session.add(new_observation)
        
        # Commit all observations to the database
        db.session.commit()

        return jsonify({'message': 'Bulk observations added successfully', 'status_code': 201}), 201

    except Exception as e:
        return jsonify({'message': str(e), 'status_code': 500}), 500


def upload_bulk():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        try:
            json_data = json.load(file)
            print(json_data)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON format'}), 400

        # Process the JSON data and save to the database
        try:
            observations = []
            for item in json_data:

                # Convert date and time strings to datetime objects
                date = datetime.strptime(item['date'], "%Y-%m-%d").date()
                time = datetime.strptime(item['time'], "%H:%M:%S").time()

                # Generate what3words address based on latitude and longitude
                if not item['w3w_address']:
                    return jsonify({'message': 'Please provide a W3W address'}), 400
                
                w3w_info = get_w3w_info(item['w3w_address'])

                coordinates = w3w_info["coordinates"]

                observation = Observation(
                    date=date,
                    time=time,
                    observer_id=user.user_id,
                    temperature_land_surface=item['temperature_land_surface'],
                    temperature_sea_surface=item['temperature_sea_surface'],
                    timezone_offset=item['timezone_offset'],
                    humidity=item['humidity'],
                    wind_speed=item['wind_speed'],
                    wind_direction=item['wind_direction'],
                    precipitation=item['precipitation'],
                    haze=item['haze'],
                    weather_id=item['weather_id'],
                    country=w3w_info["country"],
                    w3w_address=item['w3w_address'],
                    city_name=w3w_info["nearest_place"],
                    longitude=coordinates["lng"],
                    latitude=coordinates['lat']
                )
                observations.append(observation)
            
            db.session.bulk_save_objects(observations)
            db.session.commit()
            return jsonify({'message': 'File processed successfully'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error saving to database: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500



# ____________________________________GET ALL OBSERVATIONS
def get_observations(observer_id):
    # Query observations created by the particular observer
    observations = Observation.query.filter_by(observer_id=observer_id).all()

    # Convert observations to dictionary format
    observation_list = [observation.to_dict() for observation in observations]

    return jsonify(observation_list)



def get_observation_by_id(observation_id):
    # Query observations created by the particular observer
    observations = Observation.query.filter_by(id=observation_id).all()

    # Convert observations to dictionary format
    observation_list = [observation.to_dict() for observation in observations]

    return jsonify(observation_list)


#_______________________________________                                                UPDATE OBSERVATION
def update_observation(observation_id):

    # verify_observer()

    # current_user = get_jwt_identity()
    # user = User.query.filter_by(email=current_user).first()

    observation = Observation.query.get_or_404(observation_id)
    
    # if user.user_id is not observation.observer_id:
    #     return {'error': 'Unauthorized, Not Your Observation'}, 403  

    observation_year = observation.date.year
    observation_quarter = observation.date.month

    #restrict any attempted amendments to observations prior to the current quarter.
    if check_observation_quarter(observation_year, observation_quarter) == False:
        return {'error': 'Amendment to observations prior to the current quarter is restricted'}, 403  

    data = request.json
    for field in ['temperature_land_surface', 'temperature_sea_surface', 'humidity', 'wind_speed', 'wind_direction', 'precipitation', 'haze']:
        if field in data:
            setattr(observation, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Observation updated successfully'}), 200