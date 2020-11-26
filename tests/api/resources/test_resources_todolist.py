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
    todos1 = len(RS.get())
    todo = DAO.create({'name': 'passnfly'})
    print(RS.get())
    todos2 = len(RS.get())
    assert_that(todos2 - todos1, equal_to(1))


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
