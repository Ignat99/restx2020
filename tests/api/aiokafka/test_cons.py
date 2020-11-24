#!/usr/bin/env python
from confluent_kafka import Consumer, KafkaError

c = Consumer({'bootstrap.servers': '192.168.99.100:9092', 'group.id': 'mygroup', 'default.topic.config': {'auto.offset.reset': 'smallest'}})
c.subscribe(['8e45c76c6d04666f047a204cb9566c4b'])

running = True
while running:
    msg = c.poll()
    if not msg.error():
        print('Received message: %s' % msg.value().decode('utf-8'))
    elif msg.error().code() != KafkaError._PARTITION_EOF:
        print(msg.error())
        running = False
        c.close()