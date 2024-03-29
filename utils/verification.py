import jwt, os
from models import Observer  

def verify_access_token(access_token):
    try:
        # Decode the access token using the secret key
        payload = jwt.decode(payload, os.getenv('ACCESS_TOKEN_KEY'), algorithm='HS256')

        # Extract the observer username from the token's payload
        observer_username = payload.get('user')

        # Retrieve the observer from the database based on the username
        observer = Observer.query.filter_by(username=observer_username).first()

        # Return the observer if found
        return observer

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None
