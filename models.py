from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_role = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, user_id, email, password, user_role):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.user_role = user_role

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'email': self.email,
            'user_role': self.user_role,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }

class Observation(db.Model):
    __tablename__ = 'observations'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    temperature_land_surface = db.Column(db.Float, nullable=False)
    temperature_sea_surface = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    wind_direction = db.Column(db.Float, nullable=False)
    precipitation = db.Column(db.Float, nullable=False)
    haze = db.Column(db.Float, nullable=False)
    w3w_address = db.Column(db.String(100), nullable=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)

    observer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('users', lazy=True))

    city_name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    timezone_offset = db.Column(db.String(10), nullable=False)

    weather_id = db.Column(db.Integer, db.ForeignKey('weathers.id'), nullable=False)
    weather = db.relationship('Weather', backref=db.backref('observations', lazy=True))

    def __init__(self, date, time, temperature_land_surface,
                 temperature_sea_surface, humidity, wind_speed, 
                 wind_direction, precipitation, haze, observer_id, city_name, country,
                 timezone_offset, weather_id, longitude, latitude, w3w_address=None):
        self.date = date
        self.time = time
        self.temperature_land_surface = temperature_land_surface
        self.temperature_sea_surface = temperature_sea_surface
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.precipitation = precipitation
        self.haze = haze
        self.observer_id = observer_id
        self.city_name = city_name
        self.country = country
        self.timezone_offset = timezone_offset
        self.weather_id = weather_id
        self.longitude = longitude
        self.latitude = latitude
        self.w3w_address = w3w_address

    def to_dict(self):
        # Fetch the associated weather object
        weather = Weather.query.get(self.weather_id)

        # Initialize weather data variables
        weather_main = None
        weather_description = None

        # Check if weather object exists
        if weather:
            # Get weather data
            weather_main = weather.main
            weather_description = weather.description

        return {
            'id': self.id,
            'date': str(self.date),
            'time': str(self.time),
            'temperature_land_surface': self.temperature_land_surface,
            'temperature_sea_surface': self.temperature_sea_surface,
            'humidity': self.humidity,
            'wind_speed': self.wind_speed,
            'wind_direction': self.wind_direction,
            'precipitation': self.precipitation,
            'haze': self.haze,
            'observer_id': self.observer_id,
            'city_name': self.city_name,
            'country': self.country,
            'timezone_offset': self.timezone_offset,
            'weather_main': weather_main,  # Add weather main data
            'weather_description': weather_description,  # Add weather description data
            'longitude': self.longitude,
            'latitude': self.latitude,
            'w3w_address': self.w3w_address
        }

class Weather(db.Model):
    __tablename__ = 'weathers'

    id = db.Column(db.Integer, primary_key=True)
    main = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __init__(self, main, description):
        self.main = main
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'main': self.main,
            'description': self.description
        }