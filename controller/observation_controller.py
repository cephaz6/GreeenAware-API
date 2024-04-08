#Imports from other files
from models import db, City, Observation
from utils.w3w_generator import get_w3w_address
from utils.verification import *
from utils.error_handler import handle_not_found_error, handle_internal_server_error


# Dependencies Imports from libraries
from flask import request, jsonify
from datetime import datetime
from flask_jwt_extended import get_jwt_identity


#_____________________ ADD OBSERVATION CONTOLLER
def add_observation():
    try:
        #check if authenticated
        verify_observer()

        data = request.json

        # Check if the city name exists in the cities table
        city = City.query.filter_by(city=data['city_name']).first()
        if not city:
            return jsonify({'message': 'City not found'}), 404

        # Convert date and time strings to datetime objects
        date = datetime.strptime(data['date'], "%Y-%m-%d").date()
        time = datetime.strptime(data['time'], "%H:%M:%S").time()

        w3w_address = get_w3w_address(data['latitude'], data['longitude'])

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


#_____________________ ADD BULK OBSERVATION CONTOLLER
def add_bulk_observation():
    try:
        #check if authenticated
        verify_observer()

        # Get the list of observations from the request body
        observations = request.json.get('observations')
        
        if not observations:
            return jsonify({'message': 'No observations provided in the request'}), 400

         # Iterate over each observation and add it to the database
        for data in observations:

            city = City.query.filter_by(city=data.get('city_name')).first()

            if not city:
                # Return a JSON response indicating that the city was not found
                return jsonify({'message': 'City not found for observation: {}'.format(observation_data['city_name'])}), 404

            w3w_address = get_w3w_address(data.get('latitude'), data.get('longitude'))

            # Convert date and time strings to datetime objects
            date = datetime.strptime(data.get('date'), "%Y-%m-%d").date()
            time = datetime.strptime(data.get('time'), "%H:%M:%S").time()

            # Create a new Observation object
            observation = Observation(
                date=date,
                temperature=time,
                temperature_land_surface=data.get('temperature_land_surface'),
                temperature_sea_surface=data.get('temperature_sea_surface'),
                humidity=data.get('humidity'),
                wind_speed=data.get('wind_speed'),
                wind_direction=data.get('wind_direction'),
                precipitation=data.get('precipitation'),
                haze=data.get('haze'),
                city_name=data.get('city_name'),
                weather_id=data.get('weather_id'),
                w3w_address = w3w_address,
                longitude=data.get('longitude'),
                latitude=data.get('latitude')
            )
            
            # Add the observation to the database session
            db.session.add(observation)

        #Commit all the changes to the database
        db.session.commit()

        return jsonify({'message': 'Bulk Observations added successfully'}), 201

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


#_______________________________________                                                UPDATE OBSERVATION
def update_observation(id):

    verify_observer()

    observation = Observation.query.get_or_404(id)
    
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