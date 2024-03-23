from flask import Blueprint, request, jsonify
from models import db, Observer
from controllers import *

from errors import handle_not_found_error, handle_internal_server_error
from flask_jwt_extended import jwt_required, create_access_token

router = Blueprint('router', __name__)

@router.route('/', methods=['GET'])
def homepage():
    return index()

#_____________________________________________________ OBSERVER ROUTES
@router.route('/observer_signup', methods=['POST'])
def observer_signup():
    return signup()

@router.route('/observer_login', methods=['POST'])
def observer_login():
    return login()

@router.route('/get_observers', methods=['GET'])
# @jwt_required()   
def get_all_observers():
    return get_observers()


#_____________________________________________________  CITIES ROUTES
@router.route('/cities', methods=['POST'])
def add_city_route():
    return add_city()

@router.route('/cities', methods=['GET'])
def view_cities():
    return view_city()



#_____________________________________________________ OBSERVATION ROUTES
@router.route('/add-observation', methods=['POST'])
# @jwt_required()   
def add_new_observation():
    return add_observation()

@router.route('/get-observations', methods=['GET'])
# @jwt_required()   
def get_all_observation():
    return get_observations()

@router.route('/observations/weather_id=<int:weather_id>&city_id=<int:city_id>', methods=['GET'])
def get_observations(weather_id, city_id):
    return get_observations_by_ids(weather_id, city_id)

#_____________________________________________________  WEATHER ROUTES
@router.route('/get-weather', methods=['GET'])
# @jwt_required()   
def get_all_weather():
    return get_weather()

@router.route('/add-weather', methods=['POST'])
# @jwt_required()   
def add_new_weather():
    return add_weather()


# Error handling
router.register_error_handler(404, handle_not_found_error)
router.register_error_handler(500, handle_internal_server_error)