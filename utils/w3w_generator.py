import requests, os

def get_w3w_address(latitude, longitude):
    try:
        # API endpoint for What3words API
        endpoint = "https://api.what3words.com/v3/convert-to-3wa"

        # API key for What3words
        api_key = os.getenv('W3W_API_KEY')

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