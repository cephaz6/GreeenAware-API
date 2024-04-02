import os
import jwt

#Imports from other files
from models import db, Observer
from utils.error_handler import handle_not_found_error, handle_internal_server_error
from utils.verification import verify_access_token


# Dependencies Imports from libraries
from jwt import encode
from flask import request, jsonify
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


# __________________OBSERVER ACCOUNT CREATION
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user_role = "observer"

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    user = Observer.query.filter_by(username=username).first()
    if user:
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = Observer(
        username=username,
        password=hashed_password,
        user_role=user_role
        )
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
        access_token = create_access_token(identity=username)
        return jsonify({
            'Message': f'Hi {username}, Welcome Back!!', 
            'access_token': access_token,
            'status_code': 200}
            ), 200

        response.set_cookie('access_token', access_token)

    except Exception as e:
        return jsonify({'message': str(e)}), 500



# __________________ SEE LIST OF ALL OBSERVERS
def get_observers():
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 403

    observer = Observer.query.filter_by(username=current_user).first()
    if observer.user_role is not 'admin':
        return jsonify({'message': 'You are not an admin'}), 403

    observers = Observer.query.all()
    return jsonify([observer.to_dict() for observer in observers])
