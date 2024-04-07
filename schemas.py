from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow()

class ObserverSchema(ma.Schema):
    class Meta:
        fields = ('username', 'user_role')

class ObservationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'time', 'temperature_land_surface',
                  'temperature_sea_surface', 'humidity', 'wind_speed',
                  'wind_direction', 'precipitation', 'haze', 'city_name',
                  'weather_id', 'longitude', 'latitude', 'w3w_address')

class CitySchema(ma.Schema):
    class Meta:
        fields = ('id', 'city', 'country', 'timezone_offset')

class WeatherSchema(ma.Schema):
    class Meta:
        fields = ('id', 'main', 'description')

# Initialize schemas
observer_schema = ObserverSchema()
observation_schema = ObservationSchema()
city_schema = CitySchema()
weather_schema = WeatherSchema()
