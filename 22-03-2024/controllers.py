from flask import Blueprint, request, jsonify
from models import db, Observer, City
import os

from jwt import encode
from datetime import datetime, timedelta

from errors import handle_not_found_error, handle_internal_server_error
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash


def index():
    # return("Welcome to GreenAware")
    return jsonify({'message': 'Welcome to GreenAware', 'status_code': 200})

# __________________OBSERVER ACCOUNT CREATION
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    user = Observer.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = Observer(username=username, password=hashed_password)
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
            'sub': observer.username,
            'exp': datetime.utcnow() + timedelta(hours=1)  # Token expiration time
        }
        # token = encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
        token = encode(payload, "SECRET_KEY")

        # return jsonify({'access_token': token.decode('utf-8')}), 200
        return jsonify({'access_token': token}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500


# __________________ SEE LIST OF ALL OBSERVERS
def get_observers():
    observers = Observer.query.all()
    return jsonify([observer.to_dict() for observer in observers])


# __________________OBSERVER ADD A NEW CITY
def add_city():
    # try:
    #     # Extract JWT token from request headers
    #     auth_header = request.headers.get('Authorization')
    #     token = auth_header.split(' ')[1]

    #     # Decode JWT token to extract observer's username
    #     payload = decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    #     username = payload['sub']

    #     # Retrieve observer from database
    #     observer = Observer.query.filter_by(username=username).first()

    #     # Check if observer exists
    #     if not observer:
    #         return jsonify({'message': 'Observer not found'}), 404

    #     # Ensure only observers can add cities
    #     if observer.role != 'observer':
    #         return jsonify({'message': 'Only observers can add cities'}), 403

        # Parse city data from request
    city_data = request.json
    city = city_data.get('city')
    country = city_data.get('country')

    # Validate city data
    if not city or not country:
        return jsonify({'message': 'City name and country are required'}), 400

    # Create new city
    new_city = City(city=city, country=country)

    # Add city to database
    db.session.add(new_city)
    db.session.commit()

    return jsonify({'message': 'City added successfully'}), 201

    # except exceptions.DecodeError:
    #     return jsonify({'message': 'Invalid token'}), 401

# __________________ SEE LIST OF ALL CITIES
def view_city():
    cities = City.query.all()
    return jsonify([cities.to_dict() for cities in cities])
