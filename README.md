# GreeenAware-API

This repository contains the Greenaware Weather API, which allows subscribing institutions to access climate observation data collected by a network of registered observers.

### Greenaware, is concerned with the climate changes caused by Global Warming.

##### Greenaware’s mission is to collect data to improve awareness and drive predictive modelling initiatives with the overarching goals of supporting scientific research and affecting government policy.

Greenaware’s services will allow climate-change conscious individuals and groups around the Earth to register and contribute by providing climate readings and observations related to their local regions at intervals.
What3words a ‘proprietary geocode system designed to identify any location on the surface of Earth with a resolution of about 3 meters' (What3words, n.d.), will be used to convey precise geographic coordinates.
Registered contributors, termed ‘Observers’ will first have to complete an online educational course before qualifying to contribute data. They will then be paid a monthly stipend to their accounts as a token of gratitude for their support.

### Features:

.Secure access using JSON Web Tokens (JWT).
.Standard HTTP methods (GET, POST, etc.) for interoperability.
.Observation data retrieval with filtering capabilities (date, location, etc.).
.Support for various observation parameters:.
+Date (ISO 8601 format)+
+Time (ISO 8601 format)+
+Timezone offset (ISO 8601 format)+
+Location (What3words address)+
+Temperature (land & sea surface)+
+Humidity+
+Wind speed & direction.+
+Precipitation+
+Haze+
+Notes+

### Requirements:

.Python 3.x.
.Flask.
.flask_sqlalchemy.
.flask_jwt_extended.
.python-dotenv.
.flask_migrate.
.what3words.
.marshmallow.
.flask-marshmallow.
.marshmallow-sqlalchemy.

### Installation:

.Clone this repository.
.Install required dependencies: pip install -r requirements.txt.
.Configure database connection details in the application configuration file (config.py).
.Run the API server: python api.py.

### Usage:

.Subscribe to Greenaware's data access service.
.Obtain a JWT token through the Greenaware website.
.Include the JWT token in the authorization header of API requests.
API Endpoints:
‘/observations’: Retrieves observation data based on query parameters (e.g., date range, location).
‘/observations/<<observation_id>>’: Retrieves a specific observation by its ID.

### Data Access:

The API retrieves data from the Greenaware data lake. Filtering capabilities allow institutions to reduce data payload size.

### Security:

The API utilizes JWT for secure access control. Data immutability ensures past observations cannot be modified.
