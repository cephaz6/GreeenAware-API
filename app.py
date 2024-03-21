# app.py
from flask import Flask
from models import db, SECRET_KEY
from routes import api
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = SECRET_KEY
db.init_app(app)

# Register API routes
app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def home():
    return ("Welcome to the GreenAware Api")

if __name__ == '__main__':
    app.run(debug=True)
