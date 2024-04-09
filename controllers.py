"""
Name: Chris Emetoh; Iheke; Ose Cephas
Date: 28/03/2024
This is the main controller file: Others are in the 'controller directory'
"""

# Dependencies Imports from libraries
from flask import jsonify


#____________________HOME (/dir) EndPoint
def index():
    return jsonify(
        {
        'message': 'Welcome to GreenAware', 
        'status_code': 200
        }
    )