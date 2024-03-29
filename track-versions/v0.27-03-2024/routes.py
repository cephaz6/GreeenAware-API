from flask import Blueprint
from controllers import *

from errors import handle_not_found_error, handle_internal_server_error
from flask_jwt_extended import jwt_required

router = Blueprint('router', __name__)

@router.route('/', methods=['GET'])
def homepage():
    return index()

# @router.route('/api_key/api_key=<api_key>', methods=['GET'])
# def check_api(api_key):   
#     return check_api_key(api_key)

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

@router.route('/observation/city_name=<city_name>&api_key=<api_key>', methods=['GET'])
def get_observation(city_name, api_key):
    return get_observations_by_city(city_name, api_key)



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