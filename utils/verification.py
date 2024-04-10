import jwt, os
from models import Observer 
from datetime import datetime
from flask import request, jsonify, make_response
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, jwt_required 


def verify_observer():
    # Check if access token is present in cookies
    access_token = request.cookies.get('access_token')
    if not access_token:
        return jsonify({'message': 'Unauthorized'}), 403

    # Check if access token is valid
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'message': 'Unauthorized'}), 403

    # If access token is present and valid, return success
    return jsonify({'message': 'Authorized', 'username': current_user}), 200



# def verify_observer():
#     # Parse the cookie containing the access token
#     access_token_cookie = request.cookies.get('access_token')

#     # Check if the access token cookie exists
#     if not access_token_cookie:
#         return jsonify({'message': 'Access token cookie missing'}), 401

#     try:
#         # Decode and verify the access token
#         decoded_token = jwt.decode(access_token_cookie, os.getenv('ACCESS_TOKEN_KEY'), algorithms=['HS256'])
#         # Extract user identity or other information from the decoded token
#         user_id = decoded_token.get('sub')

#         # Proceed with further processing
#         return jsonify({'message': f'Protected route accessed by user {user_id}'}), 200
#     except jwt.ExpiredSignatureError:
#         return jsonify({'message': 'Expired access token'}), 401
#     except jwt.InvalidTokenError:
#         return jsonify({'message': 'Invalid access token'}), 401


#this basically gets the current year quarter
def get_current_quarter():
    now = datetime.now()
    quarter = (now.month - 1) // 3 + 1
    return now.year, quarter

#observations prior to the current quarter restricter
def check_observation_quarter(observation_year, observation_quarter):
    current_year, current_quarter = get_current_quarter()

    if (observation_year, observation_quarter) < (current_year, current_quarter):
        # Observation is before the current quarter, reject the request
        return False  