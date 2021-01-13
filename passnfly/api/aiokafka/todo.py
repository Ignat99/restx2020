#!/usr/bin/env python3
"""Threads for kafka journaling system communication"""
from __future__ import print_function
import sys
import json
from threading import Thread, current_thread
import hashlib
import time
#from kafka import KafkaProducer, KafkaConsumer
from confluent_kafka import Producer, Consumer, KafkaError, TopicPartition
from confluent_kafka.admin import AdminClient, NewTopic

KAFKA_SERVER = "localhost:9092"
REPEAT_DELAY_SEC=30
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
        self.transactional_id='todo.py'

        try:
            self.consumer = Consumer({'bootstrap.servers': '0.0.0.0:9092',
                'auto.offset.reset': 'earliest',
                'group.id': 'ping-pong',
                'client.id': 'client-1',
                'enable.auto.commit': False,
                'enable.partition.eof': True
            })



#            self.consumer = KafkaConsumer(bootstrap_servers=['0.0.0.0:9092'],
#                auto_offset_reset='latest',
#                group_id='ping-pong',
#                client_id='client-1',

#                isolation_level='read_committed'
#                auto_offset_reset='earliest',
#                session_timeout_ms=250000,
#                request_timeout_ms=300000,
#                heartbeat_interval_ms=80000,
#                retry_backoff_ms=1000
#                )
        except:
            print(self.consumer)
            print("Error: Kafka not running (bin/kafka-server-start.sh config/server.properties)")

        try:
            self.consumer.subscribe(['df911f0151f9ef021d410b4be5060972'])
            # Prior to KIP-447 being supported each input partition requires
            # its own transactional producer, so in this example we use
            # assign() to a single partition rather than subscribe().
            # A more complex alternative is to dynamically create a producer per
            # partition in subscribe's rebalance callback.
#            self.consumer.assign([TopicPartition('df911f0151f9ef021d410b4be5060972', self.input_partition)])
        except:
            print("Error: For Kafka need partition test (Need run ./tweeterapi.py)")




        self.producer=Producer({'bootstrap.servers': KAFKA_SERVER,
            'acks': 'all',
            'retries': 5,
            'transactional.id': self.transactional_id
        })

#        self.producer= KafkaProducer(bootstrap_servers=KAFKA_SERVER,
#            acks='all',
#            retries=5,
#            )

#            enable_idempotence=True,
#            max_in_flight_requests_per_connection=1

        # Initialize producer transaction.
#        self.producer.init_transactions()
        # Start producer transaction.
#        self.producer.begin_transaction()

        self.eof = {}
        self.msg_cnt = 0
        self.input_partition = 0




    def next_tuple(self):
        """Take next json message object"""
        for message in self.consumer:
            ping_dict = json.loads(message.value)
            print('Ping : ' , ping_dict['payload']['force_error'])
#            print('Ping : ' , message.value)

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

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), str(msg.partition()), err))


    def ping_send(self,topic, hashtags,max_items=0):
        item = { 'transaction-id': self.transactional_id,
            'payload': {
                'message': 'ping',
                'force_error': 'false'
            }
        }
        post_json=json.dumps(item)
        print("send to kafka topic="+topic)
        print(post_json)
#        future=self.producer.send(topic,post_json.encode("utf-8"))
        self.producer.poll(0)
        self.producer.produce(topic, post_json.encode("utf-8"), callback=self.delivery_report)
        self.producer.flush()
        print("async ping data transfer started...")

    def pong_send(self,topic, hashtags,max_items=0):
        item = { 'transaction-id': self.transactional_id,
            'payload': {
                'message': 'pong',
                'force_error': 'false'
            }
        }
        post_json=json.dumps(item)
        print("send to kafka topic="+topic)
        print(post_json)
#        future=self.producer.send(topic,post_json.encode("utf-8"))
        self.producer.poll(0)
        self.producer.produce(topic, post_json.encode("utf-8"), callback=self.delivery_report)
        self.producer.flush()
        print("async pong data transfer started...")

    def body(self):
        """Wakeup and make something every REPEAT_DELAY_SEC"""
        print("=== Starting Consume-Transform-Process loop ===")
        while True:
            print("Thread: Todo request {} -  {} ".format(self.name, str(self.msg_cnt)))
            # serve delivery reports from previous produce()s
            self.producer.poll(0)
                    #self.next_tuple()
#                    message=next(self.consumer)

            # read message from input_topic
            message = self.consumer.poll(timeout=1.0)
            if message is None:
                continue

            msg_topic, msg_partition = message.topic(), message.partition()
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    self.eof[(msg_topic, msg_partition)] = True
                    print("=== Reached the end of {} [{}] at {}====".format(
                        msg_topic, msg_partition, message.offset()))

                    if len(eof) == len(self.consumer.assignment()):
                        print("=== Reached end of input ===")
                        break
                continue
            # clear EOF if a new message has been received
            self.eof.pop((msg_topic, msg_partition), None)
            self.msg_cnt += 1

            # process message
            try:
                if (self.name == 'df911f0151f9ef021d410b4be5060972'):
                    self.ping_send(self.topic, self.keywords, POSTS_LIMIT_FOR_HASHTAG)

                else:
                    ping_dict = json.loads(message.value().decode('utf-8'))
                    print('Ping : ' , ping_dict['payload']['force_error'])

                    # produce transformed message to output topic TODO: dead_letter topic
                    if ping_dict['payload']['force_error'] == 'false':
                        self.pong_send(self.topic, self.keywords, POSTS_LIMIT_FOR_HASHTAG)

                    if self.msg_cnt % 100 == 0:
                        print("=== Committing transaction with {} messages at input offset {} ===".format(
                            self.msg_cnt, message.offset()))
                        # Send the consumer's position to transaction to commit
                        # them along with the transaction, committing both
                        # input and outputs in the same transaction is what provides EOS.
#                        self.producer.send_offsets_to_transaction(
#                            self.consumer.position(self.consumer.assignment()),
#                            self.consumer_group_metadata())

                        # Commit the transaction
#                        self.producer.commit_transaction()

                        # Begin new transaction
#                        self.producer.begin_transaction()
                        self.msg_cnt = 0

            except Exception as err1:
                if FORCE_RAISE:
                    raise err1
                print("Thread body Exception ")
                print(type(err1))    # the exception instance
                print(err1.args)     # arguments stored in .args
                print(err1)

            time.sleep(REPEAT_DELAY_SEC)


        print("=== Committing final transaction with {} messages ===".format(self.msg_cnt))
        # commit processed message offsets to the transaction
#        self.producer.send_offsets_to_transaction(
#            self.consumer.position(self.consumer.assignment()),
#            self.consumer_group_metadata())

        # commit transaction
#        self.producer.commit_transaction()

        self.consumer.close()

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
