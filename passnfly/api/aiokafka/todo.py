#!/usr/bin/env python3
"""Threads for kafka journaling system communication"""
from __future__ import print_function
import sys
import json
from threading import Thread, current_thread
import hashlib
import time
from kafka import KafkaProducer, KafkaConsumer
from confluent_kafka.admin import AdminClient, NewTopic

KAFKA_SERVER = "localhost:9092"
REPEAT_DELAY_SEC=5
TOPIC_LIST = []
THREAD_LIST = []
#KAFKA_CLIENT = []
#ADMIN_CLIENT = []
#PRODUCER = []   #Kafka producer is thread-safe
loaded_post_id=[]
MY_DATE_FORMAT="%a %b %d %H:%M:%S %z %Y"
POSTS_LIMIT_FOR_HASHTAG=10
FORCE_RAISE=False

class TodoThread(Thread):
    """ Special class for stop process in thread """
    def __init__(self, topic,keywords, *args, **kwargs):
        Thread.__init__(self, target=self.body, *args, **kwargs)
        #self.target=self.body
        self.__run_backup = self.run
        self.killed = False


        self.topic=topic
        self.keywords=keywords
        self.producer= KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        try:
            self.consumer = KafkaConsumer(bootstrap_servers=['0.0.0.0:9092'],
                auto_offset_reset='earliest',
                session_timeout_ms=250000,
                request_timeout_ms=300000,
                heartbeat_interval_ms=80000,
                retry_backoff_ms=1000
                )
        except:
            print(self.consumer)
            print("Error: Kafka not running (bin/kafka-server-start.sh config/server.properties)")

        try:
            self.consumer.subscribe(['test'])
        except:
            print("Error: For Kafka need partition test (Need run ./tweeterapi.py)")

    def next_tuple(self):
        """Take next json message object"""
        for message in self.consumer:
            tweet = json.loads(message.value)
            print('Tweet : ' + tweet)

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg): #pylint: disable=unused-argument
        """ Global trase to stop thread """
        if event == 'call':
            return self.localtrace

        return None

    def localtrace(self, frame, event, arg): #pylint: disable=unused-argument
        """ Local trace to stop Thread """
        if self.killed and event == 'line':
            raise SystemExit()
        return self.localtrace

    def kill(self, del_name):
        """ Kill thread """
        print(del_name)
        self.producer.close()
        cur_name = current_thread().name
        print('Cur : ' + cur_name)
        print('Self : ' + self.name)
#        if del_name == self.name :
        self.killed = True

    def body(self):
        """Wakeup and make something every REPEAT_DELAY_SEC"""
        while True:
            print("Thread: Todo request " + self.name)
            try:
#                self.hashtags_to_sender_from_generator(self.topic,\
#                    self.keywords,POSTS_LIMIT_FOR_HASHTAG)
                pass
            except Exception as err1:
                if FORCE_RAISE:
                    raise err1
                print("Thread body Exception ")
                print(type(err1))    # the exception instance
                print(err1.args)     # arguments stored in .args
                print(err1)

            time.sleep(REPEAT_DELAY_SEC)


def topic_from_keywords(keywords):
    """Make a hash from set of keywords and data and lang etc"""
    print('Keywords :', keywords)
    keywords_encode = keywords.encode('utf-8')
    print('keywords_encode : ', keywords_encode)
    hash_keywords = hashlib.md5(keywords_encode)
    print('keyword HASH', hash_keywords)
    topic = hash_keywords.hexdigest()
    return topic


def post_data2(keywords):
    """Open new Kafka partition for new topic and start thread for write"""
    topic=topic_from_keywords(keywords)
    print('hash keywords for Topic : ', topic)
    global TOPIC_LIST
    if not NewTopic(topic, 1, 1) in TOPIC_LIST:
        TOPIC_LIST.append(NewTopic(topic, 1, 1))
        admin_client = AdminClient({"bootstrap.servers": KAFKA_SERVER})
        admin_client.create_topics(TOPIC_LIST)  #  ensure_topic_exists already created the topic

    kafka_thread = TodoThread( name=topic,topic=topic,keywords= keywords.split(','))
    THREAD_LIST.append(kafka_thread)
    kafka_thread.daemon = True
    kafka_thread.start()
    return topic
