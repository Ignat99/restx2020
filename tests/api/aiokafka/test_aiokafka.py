#!/usr/bin/python
# coding: utf-8

"""
Test twitterapi.py
"""

from __future__ import print_function
import os
import socket as s
import json as j
from io import BytesIO
import hashlib
from collections import namedtuple
import pycurl
#import requests
import pytest
import allure
from hamcrest import assert_that, has_property, equal_to, \
all_of, contains_string
#is_not, raises, calling
#, contains, has_entries, has_entry
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from kafka import KafkaConsumer
#from postgres import update_server
from twitterapi import init_twitterapi
from insikt import L1NAME

SOCKET_ERROR = s.error
ERROR_CONDITION = None

#HOSTS = [H2, H3, H4, H5]
HOSTS = [L1NAME]

Prc = namedtuple('prc', 'proc pos cont')
Srv = namedtuple('Server', 'host port link')
Case = namedtuple('Case', 'token data')

try:
    APIUSERTEST = os.environ["APIUSERTEST"]
except KeyError:
    print("Please set the environment variable APIUSERTEST")
    APIUSERTEST = ""

class BaseModifyMatcher(BaseMatcher):
    """A matcher that modify check value and pass it following the specified matcher."""
    def __init__(self, item_matcher):
        self.item_matcher = item_matcher
        self.new_item = ''
        self.modify = item_matcher
        self.description = ''
        self.instance = ''

    def _matches(self, item):
        """ _Matches """
        if isinstance(item, self.instance) and item:
            self.new_item = self.modify(item)
            return self.item_matcher.matches(self.new_item)
        return False

    def describe_mismatch(self, item, mismatch_description):
        """ Mismatch """
        if isinstance(item, self.instance) and item:
            self.item_matcher.describe_mismatch(self.new_item, mismatch_description)
        else:
            mismatch_description.append_text('not %s, was: ' % self.instance) \
.append_text(repr(item))

    def describe_to(self, description):
        """ Describe_to """
        description.append_text(self.description) \
.append_text(' ') \
.append_description_of(self.item_matcher)

@pytest.yield_fixture
def socket():
    """Open internet socket for test listen server."""
    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    yield _socket
    _socket.close()

# scope='module'
@pytest.fixture()
def api_server(request):
    """ Maked link to http server. """
    class Dummy(object): # pylint: disable=too-few-public-methods
        """Just any port for test"""
        def __init__(self, srv):
            self.srv = srv
            self.sock = None

        @property
        def uri(self):
            """ Just any host:port/link for test from parameters"""
            return 'https://{host}:{port}/{link}'.format(**self.srv._asdict())

        @property
        def uri_es(self):
            """ Just any host:port/link for test from parameters"""
            return [{'host': self.srv.host, 'port': self.srv.port}]


        def connect(self):
            """Connection for test from parameters"""
            self.sock = s.create_connection((self.srv.host, self.srv.port))
            self.sock.sendall('HEAD /404 HTTP/1.0\r\n\r\n') # pylint: disable=no-member
            self.sock.recv(1024) # pylint: disable=no-member

        def connect_es(self):
            """Connection for ES"""
            self.sock = s.create_connection((self.srv.host, self.srv.port))
#            self.sock.sendall('') # pylint: disable=no-member
#            self.sock.recv(1024) # pylint: disable=no-member


        def close(self):
            """ Close connection after responce """
            if self.sock:
                self.sock.close()

    res = Dummy(request.param)
    yield res
    res.close()

def has_content(item):
    """In that lib payload content in param text, when we get it, we start parsing."""
    return has_property('text', item if isinstance(item, BaseMatcher) else contains_string(item))

def has_status(status):
    """Check status code."""
    return has_property('status_code', equal_to(status))

def has_status201():
    """Check status code."""
    return 201

def is_json(item_match):
    """
    Example:
        >>> from hamcrest import *
        >>> is_json(has_entries('foo', contains('bar'))).matches('{"foo": ["bar"]}')
        True
    """
    class AsJson(BaseModifyMatcher): # pylint: disable=too-few-public-methods
        """Add our matcher for JSON data"""
        description = 'json with'
        modify = lambda _, item: j.loads(item)
        instance = basestring

    return AsJson(wrap_matcher(item_match))

def idparametrize(name, values, fixture=False):
    """
    Auxiliary decorator idparametrize, in which we use the additional parameter ids=
    of decorator pytest.mark.parametrize.
    """
    return pytest.mark.parametrize(name, values, ids=list(map(repr, values)), indirect=fixture)

#{'content-type': 'application/x-www-urlencoded; charset=utf-8'}, \


class DefaultCase(object): # pylint: disable=too-few-public-methods
    """Default class for response analysis."""
    def __init__(self, text):
        self.text = text
        self.req = dict(
            headers={}, data={}, params={})
#            has_content('success'),
        self.match_string = all_of(has_status(200))

    def __repr__(self):
        return 'text="{text}", {cls}, {req}'.format(cls=self.__class__.__name__, \
            text=self.text, req=self.req)
#        return 'text="{text}", {cls}'.format(cls=self.__class__.__name__, text=self.text)

class JSONCase(DefaultCase): # pylint: disable=too-few-public-methods
    """Class for JSON analysis."""
    def __init__(self, text):
        DefaultCase.__init__(self, text)
        self.req['headers'].update({'Content-Type': 'application/json'})
#        self.req['headers'].update({'Accept': 'application/json'})
        self.req['data'].update({'keywords': 'trump bomb', 'users': 'ak47', \
'locations': 'Madrid', 'langs': ["en"]})

        self.match_string = all_of(
            has_content('result'),
            has_status(201),
        )

        self.match_200 = all_of(
            has_status(200),
        )

        self.match_201 = all_of(
            has_status201(),
        )


KEYWORDS = "trump bomb"
HASH_KEYWORDS = hashlib.md5(KEYWORDS.encode())
KAFKA_TOPIC = HASH_KEYWORDS.hexdigest()
LANGS = ["en"]

(KAFKA_CLIENT, ADMIN_CLIENT, PRODUCER) = ([], [], [])

(KAFKA_CLIENT, ADMIN_CLIENT, PRODUCER) = init_twitterapi(KAFKA_CLIENT, ADMIN_CLIENT, PRODUCER)
#ADMIN_CLIENT.delete_topics([KAFKA_TOPIC])

KAFKA_CONSUMER = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=['0.0.0.0:9092'], \
consumer_timeout_ms=1500, auto_offset_reset='earliest')
#, value_deserializer=bytes.decode)


# Storm # Srv(H1, 8090, 'index.html'), # Srv(H3, 8090, 'index.html'),
# Srv(H5, 8090, 'index.html'),
# Kibana # Srv(H1L, 56013, 'app/kibana'), # Srv(H2L, 56013, 'app/kibana'),
# Srv(H3L, 5601, 'app/kibana'), # Srv(H4L, 5601, 'app/kibana'), # Srv(H5L, 5601, 'app/kibana'),
#    Srv(H2, 8090, 'index.html'),

SERVER_CASES = [
    Srv(L1NAME, 8032, 'keywords')
]

#@pytest.mark.skip(reason="Temporal running without call api")
@idparametrize('api_server', SERVER_CASES, fixture=True)
@idparametrize('case', [testclazz(login)
                        for login in [APIUSERTEST]
                        for testclazz in [JSONCase]])
def test_twitterapi_port(case, api_server): # pylint: disable=redefined-outer-name
    """
    Open ports on twitter api
    Test ports

    Step 1:
        Try connect to host, port,
        and check for not raises SOCKET_ERROR.

    Step 2:
        Test of call to Twitter API
        Check for server responce 'data' message
        Responce status should be equal to 200.

    Step 3:
        Full test of API by Kafka
    """
#    update_server(api_server.srv.host, api_server.srv.port, api_server.srv.link, 0)


#    with allure.step('Try connect'):
#        assert_that(calling(api_server.connect), is_not(raises(SOCKET_ERROR)))
#        update_server(api_server.srv.host, api_server.srv.port, api_server.srv.link, 1)

    with allure.step('Check response'):
#        response = requests.post(api_server.uri, data=j.dumps({'keywords': KEYWORDS, \
#'users': 'ak47', 'locations': 'Madrid', 'langs': ["en"]}), \
#headers={'Content-Type': 'application/json'}, verify=False)
        header = ['Content-Type: application/json']
        data = '{"keywords": "'+ KEYWORDS + \
'", "users": "ak47", "locations": "Madrid", "langs": "en"}'
        curl = pycurl.Curl()  # pylint: disable=c-extension-no-member
        buffer1 = BytesIO()
        curl.setopt(curl.URL, api_server.uri)
        print(api_server.uri)
        curl.setopt(curl.WRITEFUNCTION, buffer1.write)
        curl.setopt(curl.POST, True)
        curl.setopt(curl.POSTFIELDS, data)
        curl.setopt(curl.HTTPHEADER, header)
        curl.setopt(curl.CAINFO, '/home/code/s.crt')
        curl.setopt(curl.VERBOSE, False)
        curl.perform()
        body = buffer1.getvalue().decode('UTF-8')
        print(body)
        response_code = curl.getinfo(pycurl.HTTP_CODE) # pylint: disable=c-extension-no-member

#        allure.attach('response_body', response.text)
        allure.attach('response_body', body)
#        allure.attach('response_headers', j.dumps(dict(response.headers), indent=4))
#        allure.attach('response_url', response.url)
#        allure.attach('response_status', str(response.status_code))
        allure.attach('response_status', str(response_code))
        assert_that(response_code, case.match_201)
#        assert response_code == 201

#        update_server(api_server.srv.host, api_server.srv.port, api_server.srv.link, 2)

    with allure.step('Test API by Kafka'):
        check_kafka_sender()


#def test_email():
#    """ Send email with report """
#    pass


#curl -k -i -H "Content-Type: application/json" -X POST -d \
#'{"keywords": "trump bomb", "users": "ak47", "locations": "Madrid"}' \
#https://172.31.27.112:8033/delete

def execute_before_any_test():
    """ Fixture for start stream before tests """
    pass

def check_kafka_sender():
    """ Test of Kafka Producer """
    topic = KAFKA_TOPIC
    keywords = KEYWORDS
    allure.attach('Topic', topic)
    allure.attach('Keywords', keywords)
    for message in KAFKA_CONSUMER:
        tweet = j.loads(message.value)
#        print(tweet)
        try:
            text = tweet["text"]
            print('Text-----------------------------')
            print(text.encode('utf-8'))
            allure.attach('Text', text)
        except: # pylint: disable=bare-except
            pass

        try:
            lang = tweet["lang"]
            print(lang)
            allure.attach('Lang', lang)
            assert_that(lang, equal_to("en"))
        except: # pylint: disable=bare-except
            pass

#        assert_that("en", equal_to("en"))

#        break
