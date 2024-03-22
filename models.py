from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Observer(db.Model):
    __tablename__ = 'observers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }

class Observation(db.Model):
    __tablename__ = 'observations'

    id = db.Column(db.Integer, primary_key=True)
    observation_date = db.Column(db.Date, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)

    city = db.relationship('City', backref=db.backref('observations', lazy=True))

    def __init__(self, observation_date, temperature, humidity, city_id):
        self.observation_date = observation_date
        self.temperature = temperature
        self.humidity = humidity
        self.city_id = city_id

    def to_dict(self):
        return {
            'id': self.id,
            'observation_date': str(self.observation_date),
            'temperature': self.temperature,
            'humidity': self.humidity,
            'city_id': self.city_id
        }

class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), unique=True, nullable=False)
    country = db.Column(db.String(100), nullable=False)

    def __init__(self, city, country):
        self.city = city
        self.country = country

    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'country': self.country
        }
