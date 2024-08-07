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

# Public API Endpoints______________________________________________________________________
@router.route('/', methods=['GET'])
def homepage():
    return index()

@router.route('/get-observation', methods=['GET'])
def get_observation():
    return get_observations_by_city()



# Observer Routes ______________________________________________________________________
@router.route('/signup', methods=['POST'])
def observer_signup():
    return signup()

@router.route('/login', methods=['POST'])
def observer_login():
    return login()

@router.route('/update-password', methods=['POST'])
def password_update():
    return update_password()

@router.route('/get-observers', methods=['GET'])
@jwt_required()
def get_all_observers():
    return get_observers()




# Observation Routes ______________________________________________________________________
@router.route('/add-observation', methods=['POST'])
# @jwt_required()
def add_new_observation():
    return add_observation()

@router.route('/add-bulk-observations', methods=['POST'])
@jwt_required()
def bulk_observation():
    return add_bulk_observations(request.json)

@router.route('/upload-bulk', methods=['POST'])
# @jwt_required()
def upload_observation():
    return upload_bulk(request.json)


@router.route('/get-observations/<observer_id>', methods=['GET'])
# @jwt_required()
def get_all_observations(observer_id):
  return get_observations(observer_id)


@router.route('/get-observation/<int:observation_id>', methods=['GET'])
# @jwt_required()
def get_observation_id(observation_id):
    return get_observation_by_id(observation_id)


@router.route('/update-observation/<int:observation_id>')
# @jwt_required()
def observation_update(observation_id):
    return update_observation(observation_id)




# Weather Routes______________________________________________________________________
@router.route('/get-weather', methods=['GET'])
@jwt_required()
def get_all_weather():
    return get_weather()

@router.route('/add-weather', methods=['POST'])
@jwt_required()
def add_new_weather():
    return add_weather()

@router.route('/update-weather/<int:id>', methods=['PUT'])
@jwt_required()
def weather_update(id):
    return update_weather(id)

@router.route('/delete-weather/<int:id>', methods=['DELETE'])
@jwt_required()
def weather_delete(id):
    return delete_weather(id)


@router.route('/weather-notes', methods=['GET'])
def weather_notes():
    return get_weather_notes()