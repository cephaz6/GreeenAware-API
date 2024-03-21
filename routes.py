from flask import Blueprint, request, jsonify
from models import db, Observer
from errors import handle_not_found_error, handle_internal_server_error
from flask_jwt_extended import jwt_required, create_access_token

api = Blueprint('api', __name__)

@api.route('/signup', methods=['POST'])
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

    return jsonify({'message': 'User created successfully'}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    user = Observer.authenticate(username, password)
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = user.generate_token()
    return jsonify({'access_token': access_token}), 200

@api.route('/observers', methods=['GET'])
@jwt_required()
def get_observers():
    observers = Observer.query.all()
    return jsonify([observer.to_dict() for observer in observers])

# Add other CRUD operations for observers as needed

# Error handling
api.register_error_handler(404, handle_not_found_error)
api.register_error_handler(500, handle_internal_server_error)
