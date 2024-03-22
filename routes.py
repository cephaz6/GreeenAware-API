from flask import Blueprint, request, jsonify
from models import db, Observer
from controllers import *

from errors import handle_not_found_error, handle_internal_server_error
from flask_jwt_extended import jwt_required, create_access_token

router = Blueprint('router', __name__)

@router.route('/', methods=['GET'])
def homepage():
    return index()

@router.route('/signup', methods=['POST'])
def observer_signup():
    return signup()

@router.route('/login', methods=['POST'])
def observer_login():
    return login()

@router.route('/observers', methods=['GET'])
# @jwt_required()   
def get_all_observers():
    return get_observers()


@router.route('/cities', methods=['POST'])
def add_city_route():
    return add_city()

@router.route('/cities', methods=['GET'])
def view_cities():
    return view_city()

# Error handling
router.register_error_handler(404, handle_not_found_error)
router.register_error_handler(500, handle_internal_server_error)
