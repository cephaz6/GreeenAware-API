import json

def check_api_key(api_key):
    try:
        # Read the JSON data from the file
        with open('data/api_keys.json', 'r') as file:
            api_keys = json.load(file)

        # Check if the API key exists in the JSON data
        for key in api_keys:
            if key['api_key'] == api_key:
                return True

        return False
    except Exception as e:
        print(f"Error checking API key: {e}")
        return False