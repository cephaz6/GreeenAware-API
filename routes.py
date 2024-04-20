from flask import Blueprint, jsonify, request

from controllers import *
from controller.observation_controller import *
from controller.observer_controller import *
from controller.public_requests import *
from controller.weather_controller import *

from utils.api_key_checker import *
from utils.w3w_generator import *
from flask_jwt_extended import jwt_required
from flasgger import swag_from

router = Blueprint('router', __name__)

# Public API Endpoints
@router.route('/', methods=['GET'])
@swag_from('swagger/homepage.yml')
def homepage():
    """
    API Endpoint for the homepage.
    ---
    responses:
      200:
        description: A welcome message.
    """
    return index()

@router.route('/get-observation', methods=['GET'])
@swag_from('swagger/get_observation.yml')
def get_observation():
    """
    API Endpoint to get observation data.
    ---
    parameters:
      - name: api_key
        in: query
        type: string
        required: true
        description: API Key for authentication.
    responses:
      200:
        description: Observation data.
      400:
        description: Error message if API Key is missing.
      401:
        description: Error message if API Key is invalid.
    """
    api_key = request.args.get('api_key')
    if not api_key:
        return jsonify({'error': 'API Key is missing'}), 400
    if not check_api_key(api_key):
        return jsonify({'message': 'Invalid API key'}), 401
    return get_observations_by_city()

# Observer Routes
@router.route('/signup', methods=['POST'])
@swag_from('swagger/observer_signup.yml')
def observer_signup():
    """
    API Endpoint for observer signup.
    ---
    parameters:
      - name: email
        in: formData
        type: string
        required: true
        description: Email address of the observer.
      - name: password
        in: formData
        type: string
        required: true
        description: Password of the observer.
    responses:
      200:
        description: Success message.
    """
    return signup()

@router.route('/login', methods=['POST'])
@swag_from('swagger/observer_login.yml')
def observer_login():
    """
    API Endpoint for observer login.
    ---
    parameters:
      - name: email
        in: formData
        type: string
        required: true
        description: Email address of the observer.
      - name: password
        in: formData
        type: string
        required: true
        description: Password of the observer.
    responses:
      200:
        description: Success message.
    """
    return login()

@router.route('/get-observers', methods=['GET'])
@jwt_required()
@swag_from('swagger/get_all_observers.yml')
def get_all_observers():
    """
    API Endpoint to get all observers.
    ---
    responses:
      200:
        description: List of observers.
    """
    return get_observers()

# Observation Routes
@router.route('/add-observation', methods=['POST'])
@jwt_required()
@swag_from('swagger/add_new_observation.yml')
def add_new_observation():
    """
    API Endpoint to add a new observation.
    ---
    parameters:
      - name: date
        in: formData
        type: string
        required: true
        description: Date of the observation.
      - name: time
        in: formData
        type: string
        required: true
        description: Time of the observation.
      # Add more parameters as needed
    responses:
      200:
        description: Success message.
    """
    return add_observation()

@router.route('/add-bulk-observations', methods=['POST'])
@jwt_required()
@swag_from('swagger/bulk_observation.yml')
def bulk_observation():
    """
    API Endpoint to add bulk observations.
    ---
    parameters:
      - name: observations
        in: body
        required: true
        description: List of observations.
        schema:
          type: array
          items:
            type: object
            properties:
              date:
                type: string
                description: Date of the observation.
              time:
                type: string
                description: Time of the observation.
              # Add more properties as needed
    responses:
      200:
        description: Success message.
    """
    return add_bulk_observations(request.json)

@router.route('/get-observations', methods=['GET'])
@jwt_required()
@swag_from('swagger/get_all_observations.yml')
def get_all_observations():
    """
    API Endpoint to get all observations.
    ---
    responses:
      200:
        description: List of observations.
    """
    return get_observations()

@router.route('/update-observations/<int:id>', methods=['PATCH'])
@jwt_required()
@swag_from('swagger/observation_update.yml')
def observation_update(id):
    """
    API Endpoint to update an observation.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the observation to update.
      # Add more parameters as needed
    responses:
      200:
        description: Success message.
    """
    return update_observation(id)

# Weather Routes
@router.route('/get-weather', methods=['GET'])
@jwt_required()
@swag_from('swagger/get_all_weather.yml')
def get_all_weather():
    """
    API Endpoint to get all weather data.
    ---
    responses:
      200:
        description: List of weather data.
    """
    return get_weather()

@router.route('/add-weather', methods=['POST'])
@jwt_required()
@swag_from('swagger/add_new_weather.yml')
def add_new_weather():
    """
    API Endpoint to add new weather data.
    ---
    parameters:
      - name: data
        in: body
        required: true
        description: Weather data.
        schema:
          type: object
          properties:
            # Add properties as needed
    responses:
      200:
        description: Success message.
    """
    return add_weather()

@router.route('/update-weather/<int:id>', methods=['PUT'])
@jwt_required()
@swag_from('swagger/weather_update.yml')
def weather_update(id):
    """
    API Endpoint to update weather data.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the weather data to update.
      # Add more parameters as needed
    responses:
      200:
        description: Success message.
    """
    return update_weather(id)

@router.route('/delete-weather/<int:id>', methods=['DELETE'])
@jwt_required()
@swag_from('swagger/weather_delete.yml')
def weather_delete(id):
    """
    API Endpoint to delete weather data.
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the weather data to delete.
    responses:
      200:
        description: Success message.
    """
    return delete_weather(id)


@router.route('/weather-notes', methods=['GET'])
def weather_notes():
    return get_weather_notes()