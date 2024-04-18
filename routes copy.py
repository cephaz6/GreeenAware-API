from flask import Blueprint
from controllers import *

from controller.observation_controller import *
from controller.observer_controller import *
from controller.public_requests import *
from controller.weather_controller import *
from utils.w3w_generator import *

from flask_jwt_extended import jwt_required

router = Blueprint('router', __name__)

#_________________________________________________________________________
#_________THE_PUBLIC_API__ENDPOINTS_______________________PUBLIC USERS ROUTES
@router.route('/', methods=['GET'])
def homepage():
    return index()


# @router.route('/w3w', methods=['GET'])
# def homepag():
#     return get_w3w_info()

""" 
Public API USERS request - This requires a validation of the api-key of the request
Example Request (/get-observation?city_name=London&api_key=495f4901ef773c5e8433e396988ff348)
"""
@router.route('/get-observation', methods=['GET'])
def get_observation():
    # Extract API key from request
    api_key = request.args.get('api_key')
    # Check if API key is provided in the request
    if api_key is None or api_key == '':
        return jsonify({'error': 'API Key is missing'}), 400

    # Check if the provided API key is valid
    if not check_api_key(api_key):
        return jsonify({'message': 'Invalid API key'}), 401
        
    return get_observations_by_city()

#_________________________________________________________________________
#________________________________________________________ OBSERVER ROUTES
@router.route('/signup', methods=['POST'])
def observer_signup():
    return signup()

@router.route('/login', methods=['POST'])
def observer_login():
    return login()

@router.route('/get-observers', methods=['GET'])
@jwt_required()   
def get_all_observers():
    return get_observers()


#_________________________________________________________________________
#_____________________________________________________ OBSERVATION ROUTES

@router.route('/add-observation', methods=['POST'])
@jwt_required()   
def add_new_observation():
    return add_observation()

@router.route('/add-bulk-observations', methods=['POST'])
@jwt_required()   
def bulk_observation():
    return add_bulk_observations()

@router.route('/get-observations', methods=['GET'])
@jwt_required()   
def get_all_observation():
    return get_observations()
    
@router.route('/update-observations/<int:id>', methods=['PATCH'])
@jwt_required()   
def observation_update(id):
    return update_observation(id)




#_________________________________________________________________________
#_____________________________________________________  WEATHER ROUTES
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


# Error handling
# router.register_error_handler(404, handle_not_found_error)
# router.register_error_handler(500, handle_internal_server_error)