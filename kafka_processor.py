from confluent_kafka import Consumer, Producer, KafkaError
import json
from datetime import datetime
import logging
import time
from collections import defaultdict
from signal_handler import register_signal_handler

class KafkaProcessor:
    def __init__(self, consumer_conf, producer_conf, input_topic, output_topic, aggregated_topic):
        
        time.sleep(10) # Delay to ensure the consumer doesn't start before the producer creates the topics
        self.consumer_conf = consumer_conf
        self.producer_conf = producer_conf
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.aggregated_topic = aggregated_topic

        # Kafka consumer and producer instances
        self.consumer = Consumer(self.consumer_conf)
        self.producer = Producer(self.producer_conf)

        # Aggregation variables
        self.state_sensor_counts = defaultdict(set)  # Unique sensors per state
        self.state_temp_sums = defaultdict(float)  # Sum of temperatures per state
        self.state_message_counts = defaultdict(int)  # Total messages per state
        self.last_report_time = time.time()


        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    

    def process_message(self, message):
        """Process the Kafka message."""
        
        # write try and exception for this
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            self.logger.warning("Skipping message due to invalid JSON.")
            return None # Return None if the message is not valid JSON

        # Skip the messages if 'guid' or 'payload' or 'eventTime' fields are missing
        if 'guid' not in data or 'payload' not in data or 'eventTime' not in data:
            self.logger.warning("Skipping message due to missing keys.")
            return None
        
        # Skip the messages if 'guid' or 'payload' or 'eventTime' fields are None
        if data['guid'] is None or data['payload'] is None or data['eventTime'] is None:
            self.logger.warning("Skipping message due to None values.")
            return None
        
        # Extract temperature safely (handling nesting and null values)
        data['temperature'] = data.get('payload', {}).get('data', {}).get('temperature', None)
        del data['payload']

        # Convert timestamp to UTC
        data['timestamp_in_utc'] = datetime.utcfromtimestamp(int(data['eventTime'])).strftime('%Y-%m-%d %H:%M:%S')
        data['processed_time'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        return data


    def produce_message(self, data):
        """Produce the processed message to the output topic."""
        try:
            # Send the processed data to the new Kafka topic
            self.producer.produce(self.output_topic, json.dumps(data).encode('utf-8'))
            self.producer.flush()
        except KafkaError as e:
            self.logger.error(f"Failed to produce message: {e}")
        

    def consume_messages(self):

        """Consume messages from the Kafka topic and process them."""
        while True:
            # Poll for new messages
            msg = self.consumer.poll(timeout=1.0) # Set a timeout to avoid blocking indefinitely
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue # Ignore end of partition errors
                else:
                    self.logger.info(f"Error: {msg.error()}")
                    break

            # Process the message
            processed_data = self.process_message(msg.value().decode('utf-8'))

            # If data is processed, send to the new topic
            if processed_data:
                self.logger.info(f"Sending processed data: {processed_data}")
                self.aggregate_data(processed_data)
                self.produce_message(processed_data)
            else:
                self.logger.error("Message skipped due to processing error.")
            
            # Periodically report counts
            self.produce_aggregated_data()

    def aggregate_data(self, data):
        """Perform real-time aggregation."""

        state = data['State']
        guid = data['guid']
        temp = data['temperature']

        if state and guid and temp:
            self.state_sensor_counts[state].add(guid)  # Track unique sensors
            self.state_temp_sums[state] += temp  # Sum temperatures
            self.state_message_counts[state] += 1  # Count messages
        else:
        # Log a warning if data is missing important fields
            self.logger.warning("Skipping aggregation due to missing data.")


    def produce_aggregated_data(self):
        """Send aggregated data periodically."""
        
        current_time = time.time()
        if current_time - self.last_report_time >= 60:  # Every 60 seconds
            aggregation_data = {
                "total_sensors_by_state": {state: len(sensors) for state, sensors in self.state_sensor_counts.items()},
                "avg_temp_by_state": {state: (self.state_temp_sums[state] / self.state_message_counts[state]) 
                                      if self.state_message_counts[state] > 0 else 0
                                      for state in self.state_sensor_counts.keys()},
                "total_messages": sum(self.state_message_counts.values())
            }

            # Log the aggregated data before producing
            self.logger.info(f"Aggregated data: {aggregation_data}")

            self.producer.produce(self.aggregated_topic, json.dumps(aggregation_data).encode('utf-8'))
            self.producer.flush()
            self.last_report_time = current_time  # Reset timer
            return
        else:
            self.logger.debug("Aggregation report not yet due.")
                

    def start(self):
        """Start the Kafka consumer."""
        self.consumer.subscribe([self.input_topic])
        self.consume_messages()

