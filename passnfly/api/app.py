#!/usr/bin/env python3
""" Running point of application """
from __future__ import print_function
from passnfly.api.models.todo import app
from passnfly.db.sqlalchemy_extension import db
from passnfly.db.schema import City
from passnfly.api.resources.todo import DAO

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
            'geo': city.geo
        })
    app.run(host="0.0.0.0", port=8032, debug=True)
