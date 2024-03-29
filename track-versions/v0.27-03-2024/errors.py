from flask import jsonify

def handle_not_found_error(error):
    response = jsonify({'error': 'Not Found'})
    response.status_code = 404
    return response

def handle_internal_server_error(error):
    response = jsonify({'error': 'Internal Server Error'})
    response.status_code = 500
    return response
