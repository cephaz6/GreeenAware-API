import json, requests

def check_api_key(api_key):
    try:
        # Make an HTTP request to the Django endpoint to fetch all active API keys
        response = requests.get('http://127.0.0.1:8000/fetch-api-keys')
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the list of API keys from the JSON response
            api_keys_data = response.json().get('api_keys', [])
            
            # Check if the provided API key exists in the list of API keys
            for key_data in api_keys_data:
                if key_data.get('api_key') == api_key:
                    return True
        return False
    
    except Exception as e:
        print(f"Error checking API key: {e}")
        return False


# def check_api_key(api_key):
#     try:
#         # Read the JSON data from the file
#         with open('data/api_keys.json', 'r') as file:
#             api_keys = json.load(file)

#         # Check if the API key exists in the JSON data
#         for key in api_keys:
#             if key['api_key'] == api_key:
#                 return True

#         return False
#     except Exception as e:
#         print(f"Error checking API key: {e}")
#         return False