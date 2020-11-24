#!/usr/bin/env python3
""" Running point of application """
from __future__ import print_function
#import json
#from flask import Flask
#from flask_restx import Api, Resource, fields
#from flask_restx import Resource
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import func
#from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
#from passnfly.api.dao.todo import TodoDAO
#from passnfly.api.aiokafka.todo import post_data2
from passnfly.api.models.todo import app
#, api, ns, todo
from passnfly.db.schema import db, City
from passnfly.api.resources.todo import DAO

#TodoList, Todo,
#KAFKA_SERVER = "localhost:9092"
#REPEAT_DELAY_SEC=5
#MY_DATE_FORMAT="%a %b %d %H:%M:%S %z %Y"

#app = Flask(__name__)
#CORS(app)
#api = Api(app, version='1.0', title='TodoMVC API',
#    description='A simple TodoMVC API',
#)
#ns = api.namespace('api', description='TODO operations')

#db = SQLAlchemy()
#DAO = TodoDAO()

def connect_to_db(ap1):
    """Connect the database to Flask app."""

    ap1.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:Pbdivbknn123@localhost:5432/insikt'
    ap1.config['SQLALCHEMY_ECHO'] = False
    ap1.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = ap1
    db.init_app(ap1)

if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()
    print("Connected to database.")
#    for city in City.query.filter(City.name == "Thule Air Base"):
    for city in City.query.filter(City.id < 20):
        DAO.create({
            'name': city.name,
            'city': city.city,
            'country': city.country,
            'iata': city.iata,
            'icao': city.icao,
            'latitude': city.latitude,
            'longitude': city.longitude,
            'altitude': city.altitude,
            'timezone': city.timezone,
            'DST': city.dst,
            'tz': city.tz,
            'type': city.type,
            'source': city.source,
        })
    app.run(host="0.0.0.0", port=8032, debug=True)
