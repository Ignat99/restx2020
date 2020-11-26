#!/usr/bin/env python3
from confluent_kafka import Consumer, KafkaError

c = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'mygroup', 'default.topic.config': {'auto.offset.reset': 'smallest'}})
c.subscribe(['test'])

#running = True
counter = 2
#while running:
while counter:
    counter = counter - 1
    msg = c.poll()
    if not msg.error():
        print('Received message: %s' % msg.value().decode('utf-8'))
    elif msg.error().code() != KafkaError._PARTITION_EOF:
        print(msg.error())
#        running = False
        c.close()