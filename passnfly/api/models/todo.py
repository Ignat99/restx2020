#!/usr/bin/env python3
"""Representation of information from DB in memory"""
#from __future__ import print_function
from flask import Flask
from flask_restx import Api, fields

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='TodoMVC API',
    description='A simple TodoMVC API',
)

ns = api.namespace('api', description='TODO operations')

def add_models_to_namespace(api_namespace):
    """Make a hash of object by name"""
    api_namespace.models[todo.name] = todo

todo = api.model(
    'Todo',
    {
        'id': fields.Integer(readonly=True, description='The locate unique identifier'),
        'name': fields.String(required=True, description='The name details'),
        'city': fields.String(required=True, description='The city details'),
        'country': fields.String(required=True, description='The country details'),
        'iata': fields.String(required=True, description='The iata details'),
        'icao': fields.String(required=True, description='The icao details'),
        'latitude': fields.Float(required=True, description='The latitude details'),
        'longitude': fields.Float(required=True, description='The longitude details'),
        'altitude': fields.Integer(required=True, description='The altitude details'),
        'timezone': fields.Float(required=True, description='The timezone details'),
        'DST': fields.String(required=True, description='The DST details'),
        'tz': fields.String(required=True, description='The tz details'),
        'type': fields.String(required=True, description='The type details'),
        'source': fields.String(required=True, description='The source details')
    }
)
