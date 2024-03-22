"""
Name: Chris Emetor
Name: Iheke
Name: Ose Cephas
Date: 23/03/2024
Objective: Building GreenAware Api Using Flask
"""

# App Dependencies
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from dotenv import load_dotenv
# from flask_migrate import Migrate
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db.init_app(app)


# Register API routes
from routes import router as router
app.register_blueprint(router)

with app.app_context():
   db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
