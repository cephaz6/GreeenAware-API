import os
import jwt

#Imports from other files
from models import db, User
from utils.error_handler import *
from utils.verification import *


# Dependencies Imports from libraries
from jwt import encode
from email_validator import validate_email, EmailNotValidError
from flask import request, jsonify, make_response
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


# __________________OBSERVER ACCOUNT CREATION
def signup():
    data = request.json

    email = data.get('email_address')
    password = data.get('password')

    user_id = data.get('user_id') or generate_unique_user_id()
    user_role = "admin" if not data.get('user_role') else "observer"

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400
        
    try:
        # Validate email format
        validate_email(email)
    except EmailNotValidError:
        return jsonify({'message': 'Invalid email address'}), 400

    if not is_strong_password(password):
        return jsonify(
            {'message': 'Choose A Stronger Password'}), 400

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({'message': 'Email address already exists'}), 400

    hashed_password = generate_password_hash(password)
    
    new_user = User (
        email=email,
        user_id = user_id,
        password = hashed_password,
        user_role=user_role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'status_code': 200})

# __________________OBSERVER LOGIN
def login():
    try:
        # Extract email and password from request data
        email = request.json.get('email')
        password = request.json.get('password')

        # Validate email and password
        if not email or not password:
            return jsonify({'message': 'Email and password are required', 'status_code': 204})

        # Retrieve observer from database
        user = User.query.filter_by(email=email).first()

        # Check if observer exists and password is correct
        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid email or password', 'status_code': 401})

        # Generate JWT token
        access_token = create_access_token(identity=email)

        # Create a response with the access token as a cookie
        response = make_response(jsonify({
            'message': f'Hi {user.email}, Welcome Back!',
            'status_code': 200
        }))
        response.headers['Authorization'] = 'Bearer ' + access_token  # Add access token to Authorization header
        response.set_cookie('access_token', access_token, httponly=True, max_age=1800)  # Set cookie with a timeout of 30 minutes

        return response

    except Exception as e:
        return jsonify({'message': str(e), 'status_code': 500}), 500



# __________________ SEE LIST OF ALL OBSERVERS
def get_observers():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    
    # Check if the user has admin privileges
    if user.user_role != 'admin':
        return jsonify({'message': 'Unauthorized access: You are not admin'}), 403
    
    # Fetch all users
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append(user.to_dict())
    
    return jsonify({'users': user_list}), 200
