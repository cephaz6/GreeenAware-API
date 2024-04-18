"""
Name: Chris Emetoh
Name: Iheke
Name: Ose Cephas
Date: 23/03/2024
Objective: Building GreenAware Api Using Flask
"""

# App Dependencies
from flask import Flask
from models import db
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
import os
from flasgger import Swagger

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

# JWT configurations
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)

# Register API routes
from routes import router as router
app.register_blueprint(router)

Swagger(app)

# Swagger UI configurations
SWAGGER_URL = '/swagger/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/swagger/swagger.json'  # URL for the Swagger JSON file
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "GreenAware API"  # Swagger UI config
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


with app.app_context():
   db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
