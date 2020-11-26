#!/usr/bin/env python3
"""REST API for keep/shared data"""
from __future__ import print_function
from hamcrest import has_entries, has_property, equal_to, \
all_of, contains_string, assert_that, contains
from passnfly.api.models.todo import api
from passnfly.api.resources.todo import TodoList, DAO
from passnfly.api.models.todo import app
from flask import json

def test_get():
    RS = TodoList()
    DAO.create({'name': 'passnfly'})
    print(RS.get())
    a_str = json.dumps(RS.get(), sort_keys=True)
    b_str = json.dumps(json.loads("""
[{"DST": null, "altitude": null, "city": null, "country": null, "iata": null, "icao": null, "id": 1, "latitude": null, "longitude": null, "name": "passnfly", "source": null, "timezone": null, "type": null, "tz": null}]
"""), sort_keys=True)
    assert_that(a_str, equal_to(b_str))


def test_post():
    response = app.test_client().post(
        '/api/',
        data=json.dumps({'name': 'passnfly'}),
        content_type='application/json',
    )

    print(response.get_data(as_text=True))
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 201
    assert data['name'] == 'passnfly'
