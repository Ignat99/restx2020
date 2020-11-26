#!/usr/bin/env python3
"""REST API for keep/shared data"""
#from __future__ import print_function
import json
from hamcrest import has_entries, has_property, equal_to, \
all_of, contains_string, assert_that, contains
#from passnfly.api.dao.todo import TodoDAO
from passnfly.api.models.todo import api
from passnfly.api.resources.todo import TodoList, DAO


#def teardown():
#def setup():
#    print(DAO.get(1))

def test_get():
#    DAO = TodoDAO()
    RS = TodoList()
    DAO.create({'name': 'passnfly'})
    print(RS.get())
    a_str = json.dumps(RS.get(), sort_keys=True)
    b_str = json.dumps(json.loads("""
[{"DST": null, "altitude": null, "city": null, "country": null, "iata": null, "icao": null, "id": 1, "latitude": null, "longitude": null, "name": "passnfly", "source": null, "timezone": null, "type": null, "tz": null}]
"""), sort_keys=True)
    assert_that(a_str, equal_to(b_str))

def test_update():
#    DAO = TodoDAO()
    api.payload = {'name': 'passnfly'}
#    DAO.update(1, {'name': 'passnfly1'})
    print(RS.post())

#    a_str = json.dumps(DAO.get(1), sort_keys=True)
#    b_str = json.dumps(json.loads("""
#{"name": "passnfly1", "id": 1}
#"""), sort_keys=True)
#    assert_that(a_str, equal_to(b_str))

#def test_delete():
#    DAO = TodoDAO()
#    DAO.create({'name': 'passnfly'})
#    DAO.delete(1)
#    a_str = json.dumps(DAO.get(1), sort_keys=True)
#    b_str = json.dumps(json.loads("""
#{"name": "passnfly", "id": 1}
#"""), sort_keys=True)
#    assert_that(a_str, equal_to(b_str))
