#!/usr/bin/env python3
"""REST API for keep/shared data"""
#from __future__ import print_function
import json
from hamcrest import has_entries, has_property, equal_to, \
all_of, contains_string, assert_that, contains
from passnfly.api.dao.todo import TodoDAO

def test_create():
    DAO = TodoDAO()
    DAO.create({'name': 'passnfly'})
    print(DAO.get(1))

    a_str = json.dumps(DAO.get(1), sort_keys=True)
    b_str = json.dumps(json.loads("""
{"name": "passnfly", "id": 1}
"""), sort_keys=True)
    assert_that(a_str, b_str)
