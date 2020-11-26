#!/usr/bin/env python3
"""REST API for keep/shared data"""
from __future__ import print_function
from hamcrest import has_entries, has_property, equal_to, \
all_of, contains_string, assert_that, contains
from passnfly.api.models.todo import api
from passnfly.api.resources.todo import Todo, DAO
from passnfly.api.models.todo import app
from flask import json

def test_get():
    RS = Todo()
    DAO.create({'name': 'passnfly'})
    print(RS.get(1))
    a_str = json.dumps(RS.get(1), sort_keys=True)
    b_str = json.dumps(json.loads("""
{"DST": null, "altitude": null, "city": null, "country": null, "iata": null, "icao": null, "id": 1, "latitude": null, "longitude": null, "name": "passnfly", "source": null, "timezone": null, "type": null, "tz": null}
"""), sort_keys=True)
    assert_that(a_str, equal_to(b_str))

def test_resources_delete():
    RS = Todo()
    DAO.create({'name': 'passnfly'})
    print(RS.get(1))
    (a_str, my_status) = RS.delete(1)
#    print(RS.get(1))
    assert my_status == 204


def test_delete():
    RS = Todo()
    DAO.create({'name': 'passnfly'})
#    print(RS.get(1))
    response = app.test_client().delete(
        '/api/2',
        data=json.dumps({'id': 2}),
        content_type='application/json',
    )
    assert response.status_code == 204

def test_update():
    RS = Todo()
    DAO.create({'name': 'passnfly'})
#    print(RS.get(2))
    response = app.test_client().put(
        '/api/3',
        data=json.dumps({'name': 'passnfly1'}),
        content_type='application/json',
    )
    print(response.get_data(as_text=True))
    data = json.loads(response.get_data(as_text=True))
    assert data['name'] == 'passnfly1'
