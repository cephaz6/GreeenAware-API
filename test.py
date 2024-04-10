import pytest
from your_api_module import app 
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_observations_by_city_success(client):
    # Prepare test data
    city_name = 'London'

    # Make a request to the endpoint
    response = client.get('/get-observations?city_name={}'.format(city_name))

    # Check the response status code
    assert response.status_code == 200

    # Check the response data
    data = response.json
    assert 'date' in data
    assert 'time' in data
    assert 'temperature_land_surface' in data
    assert 'temperature_sea_surface' in data
    assert 'humidity' in data
    assert 'wind_speed' in data
    assert 'wind_direction' in data
    assert 'precipitation' in data
    assert 'haze' in data
    assert 'location' in data
    assert 'city' in data['location']
    assert 'country' in data['location']
    assert 'timezone_offset' in data['location']
    assert 'longitude' in data['location']
    assert 'latitude' in data['location']
    assert 'what3words' in data['location']
    assert 'Weather Condition' in data
    assert 'main' in data['Weather Condition']
    assert 'description' in data['Weather Condition']

def test_get_observations_by_city_not_found(client):
    # Prepare test data
    city_name = 'NonexistentCity'

    # Make a request to the endpoint
    response = client.get('/get-observations?city_name={}'.format(city_name))

    # Check the response status code
    assert response.status_code == 404

    # Check the response message
    data = response.json
    assert 'message' in data
    assert data['message'] == 'Observation not found for city: {}'.format(city_name)
