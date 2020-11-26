#!/usr/bin/env python3
"""REST API for keep/shared data"""
from __future__ import print_function
import json
from hamcrest import has_entries, has_property, equal_to, \
all_of, contains_string, assert_that, contains
from passnfly.api.aiokafka.todo import topic_from_keywords

def test_hash():
    my_hash = topic_from_keywords('list_todos')
    assert_that(my_hash, equal_to('c3d465c2efa3c3ef6af2f49f695be1c6'))
