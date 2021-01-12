import os


# KAFKA BROKER
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')


# TOPIC
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
PING_TOPIC = os.environ.get('PING_TOPIC')
PONG_TOPIC = os.environ.get('PONG_TOPIC')
DEAD_LETTER_TOPIC = os.environ.get('DEAD_LETTER_TOPIC')
