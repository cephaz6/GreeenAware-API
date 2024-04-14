import requests, os
from flask import request, jsonify

# API key for What3word
api_key = os.getenv('W3W_API_KEY')


def get_w3w_info(w3w_address):
    try:
        # Define the What3Words API endpoint
        endpoint = "https://api.what3words.com/v3/convert-to-coordinates"

        # Parameters for the API request
        params = {
            "words": w3w_address,
            "key": api_key
        }

        # Make a GET request to the What3words API
        response = requests.get(endpoint, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            w3w_data = response.json()

            # Extract relevant information from the response
            coordinates = w3w_data['coordinates']
            country = w3w_data['country']
            nearest_place = w3w_data['nearestPlace']
            words = w3w_data['words']

            # Create a dictionary to store the information
            w3w_info = {
                'coordinates': coordinates,
                'country': country,
                'nearest_place': nearest_place,
                'words': words
            }

            # Return the information as a dictionary
            return w3w_info
        else:
            # If the request was not successful, return None
            return None
    except Exception as e:
        # If an exception occurs, return None
        return None

def get_w3w_address(latitude, longitude):
    try:
        # API endpoint for What3words API
        endpoint = "https://api.what3words.com/v3/convert-to-3wa"

        # Parameters for the API request
        params = {
            "coordinates": f"{latitude},{longitude}",
            "key": api_key
        }

        # Make a GET request to the What3words API
        response = requests.get(endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Extract the What3words address from the response
            if 'words' in data:
                w3w_address = data['words']
                return w3w_address
            else:
                return "What3words address not found"
        else:
            return "Error fetching What3words address"

    except Exception as e:
        return str(e)


def get_coordinates(w3w_address):
    try:
        # API endpoint for What3words API
        endpoint = "https://api.what3words.com/v3/convert-to-coordinates"


        # Parameters for the API request
        params = {
            "words": w3w_address,
            "key": api_key
        }

        # Make a GET request to the What3words API
        response = requests.get(endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Extract the coordinates from the response
            if 'coordinates' in data:
                coordinates = data['coordinates']
                return coordinates
            else:
                return "Coordinates not found"
        else:
            return "Error fetching coordinates"

    except Exception as e:
        return str(e)

