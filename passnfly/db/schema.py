#!/usr/bin/env python3

#from __future__ import print_function
#import sys
#import json
#from threading import Thread, current_thread
#import hashlib
#from flask import Flask
#from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
#from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
#from kafka import KafkaProducer, KafkaConsumer
#import time
#from confluent_kafka.admin import AdminClient, NewTopic


db = SQLAlchemy()

class City(db.Model):
    """A city, including its geospatial data."""

    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    iata = db.Column(db.String(10))
    icao = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    altitude = db.Column(db.Integer)
    timezone = db.Column(db.Float)
    dst = db.Column(db.String(50))
    tz = db.Column(db.String(50))
    type = db.Column(db.String(50))
    source = db.Column(db.String(50))
#    geo = db.Column(Geometry(geometry_type="POINT"))

    def __repr__(self):
        return "<City {name} ({lat}, {lon})>".format(
            name=self.name, lat=self.latitude, lon=self.longitude)

#    def get_cities_within_radius(self, radius):
#        """Return all cities within a given radius (in meters) of this city."""

#        return City.query.filter(func.ST_Distance_Sphere(City.geo, self.geo) < radius).all()

    @classmethod
    def add_city(cls, name, longitude, latitude):
        """Put a new city in the database."""

#        geo = 'POINT({} {})'.format(longitude, latitude)
        city = City(name=name,
                           longitude=longitude,
                           latitude=latitude)

#                          geo=geo)

        db.session.add(city)
        db.session.commit()

    @classmethod
    def update_geometries(cls):
        """Using each city's longitude and latitude, add geometry data to db."""

        cities = City.query.all()

        for city in cities:
            point = 'POINT({} {})'.format(city.longitude, city.latitude)
#            city.geo = point

        db.session.commit()


#def connect_to_db(app):
#    """Connect the database to Flask app."""

#    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:Pbdivbknn123@localhost:5432/insikt'
#    app.config['SQLALCHEMY_ECHO'] = False
#    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#    db.app = app
#    db.init_app(app)
