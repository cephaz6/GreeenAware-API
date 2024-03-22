from flask import jsonify
from models import Observer


def index():
    # return("Welcome to GreenAware")
    return jsonify({'message': 'Welcome to GreenAware', 'status_code': 200})

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

def get_observers():
    observers = Observer.query.all()
    return jsonify([observer.to_dict() for observer in observers])