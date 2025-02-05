from confluent_kafka import Consumer, Producer

def create_consumer(consumer_conf):
    #Create and return a Kafka consumer.
    consumer=Consumer(consumer_conf)
    return consumer

def create_producer(producer_conf):
    #Create and return a Kafka producer
    producer=Producer(producer_conf)
    return producer