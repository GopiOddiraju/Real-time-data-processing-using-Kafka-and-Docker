import time
from kafka_processor import KafkaProcessor
from kafka_client import create_consumer, create_producer
from signal_handler import register_signal_handler

if __name__ == "__main__":

    # Kafka consumer configuration
    consumer_conf = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'my-consumer-group',
        'auto.offset.reset': 'earliest'
    }

    # Kafka producer configuration
    producer_conf = {
        'bootstrap.servers': 'kafka:9092'
    }

    INPUT_TOPIC = 'IoT-data'
    OUTPUT_TOPIC = 'processed-data'
    AGGREGATED_TOPIC = 'aggregated-data'

    # Kafka consumer and producer instances
    consumer = create_consumer(consumer_conf)
    producer = create_producer(producer_conf)

    # Register signal handler
    register_signal_handler(consumer, producer)
    
    # Create KafkaProcessor instance and start consuming messages
    kafka_processor = KafkaProcessor(consumer_conf, producer_conf, INPUT_TOPIC, OUTPUT_TOPIC, AGGREGATED_TOPIC)
    kafka_processor.start()

    