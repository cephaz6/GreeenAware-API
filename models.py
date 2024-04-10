from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy()

class Observer(db.Model):
    __tablename__ = 'observers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_role = db.Column(db.String(100), default=False)

    def __init__(self, username, password, user_role):
        self.username = username
        self.password = password
        self.user_role = user_role

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'user_role': self.user_role
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

    city_name = db.Column(db.Integer, db.ForeignKey('cities.city'), nullable=False)
    city = db.relationship('City', backref=db.backref('observations', lazy=True))

    weather_id = db.Column(db.Integer, db.ForeignKey('weathers.id'), nullable=False)
    weather = db.relationship('Weather', backref=db.backref('observations', lazy=True))

    def __init__(self, date, time, temperature_land_surface,
                 temperature_sea_surface, humidity, wind_speed, 
                 wind_direction, precipitation, haze, city_name, weather_id,
                 longitude, latitude, w3w_address=None):
        self.date = date
        self.time = time
        self.temperature_land_surface = temperature_land_surface
        self.temperature_sea_surface = temperature_sea_surface
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.precipitation = precipitation
        self.haze = haze
        self.city_name = city_name
        self.weather_id = weather_id
        self.longitude = longitude
        self.latitude = latitude
        self.w3w_address = w3w_address

    def to_dict(self):
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
            'city_id': self.city_id,
            'weather_id': self.weather_id,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'w3w_address': self.w3w_address
        }

class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), unique=True, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    timezone_offset = db.Column(db.String(10), nullable=False)

    def __init__(self, city, country, timezone_offset):
        self.city = city
        self.country = country
        self.timezone_offset = timezone_offset

    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'country': self.country,
            'timezone_offset': self.timezone_offset
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


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_key = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email_address = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.String(100), unique=True, nullable=False)
    subscription_type = db.Column(db.String(100), nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, username, first_name, last_name, email_address, password, api_key, subscription_type=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.set_password(password)
        self.api_key = api_key
        self.subscription_type = subscription_type

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email_address': self.email_address,
            'api_key': self.api_key,
            'subscription_type': self.subscription_type,
            'date_created': str(self.date_created),
            'date_modified': str(self.date_modified)
        }