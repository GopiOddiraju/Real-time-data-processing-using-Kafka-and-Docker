import os
import datetime
import random
import time
import json
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic, KafkaError

bootstrap_servers = os.environ.get('BOOTSTRAP_SERVERS', 'localhost:9092')
topic = os.environ.get('KAFKA_TOPIC', 'user-login')

# Create a Kafka producer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers,
}

# Create a Kafka producer instance
producer = Producer(producer_config)

# Function to generate a random message
def generate_random_message():
    guid=None
    if random.random() > 0.1:
        rand_num = f"{random.randrange(0, 9)}{random.randrange(0, 9)}"
        rand_letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        guid=f"0-ZZZ12345678-{rand_num}{rand_letter}"

    datestr = int(time.time())
    device_state_map = {}
    temp_base = {'WA': 48.3, 'DE': 55.3, 'DC': 58.5, 'WI': 43.1,
                 'WV': 51.8, 'HI': 70.0, 'FL': 70.7, 'WY': 42.0,
                 'NH': 43.8, 'NJ': 52.7, 'NM': 53.4, 'TX': 64.8,
                 'LA': 66.4, 'NC': 59.0, 'ND': 40.4, 'NE': 48.8,
                 'TN': 57.6, 'NY': 45.4, 'PA': 48.8, 'CA': 59.4,
                 'NV': 49.9, 'VA': 55.1, 'CO': 45.1, 'AK': 26.6,
                 'AL': 62.8, 'AR': 60.4, 'VT': 42.9, 'IL': 51.8,
                 'GA': 63.5, 'IN': 51.7, 'IA': 47.8, 'OK': 59.6,
                 'AZ': 60.3, 'ID': 44.4, 'CT': 49.0, 'ME': 41.0,
                 'MD': 54.2, 'MA': 47.9, 'OH': 50.7, 'UT': 48.6,
                 'MO': 54.5, 'MN': 41.2, 'MI': 44.4, 'RI': 50.1,
                 'KS': 54.3, 'MT': 42.7, 'MS': 63.4, 'SC': 62.4,
                 'KY': 55.6, 'OR': 48.4, 'SD': 45.2}
    
    state = random.choice(list(temp_base.keys()))
    if guid not in device_state_map:
            device_state_map[guid] = state

    temperature = random.uniform(temp_base[state] - 5, temp_base[state] + 5)
    message = {
        "guid" : guid,
        "destination" : "0-AAA12345678",
        "State" : state,
        "eventTime" : datestr,
        "payload" : {
            "format" : "urn:example:sensor:temp",
            "data" : {
                "temperature" : temperature if random.random() >= 0.1 else None
            }
        }
    }
    time.sleep(1)   #Adding delay to simulate real-time streaming
    return guid, json.dumps(message)
        
# Create an AdminClient to manage topics
admin_client = AdminClient({
    'bootstrap.servers': bootstrap_servers,
})

# Check if the 'user-login' topic exists
topic_metadata=admin_client.list_topics(timeout=10)
topic_exists = topic in topic_metadata.topics

# Create the 'user-login' topic if it doesn't exist
if not topic_exists:
   new_topic = NewTopic(topic, num_partitions=1, replication_factor=1)
   try:
       admin_client.create_topics(new_topics=[new_topic], validate_only=False)
   except KafkaError:
       pass

# Produce random messages to Kafka
try:
    while True:
        guid, message = generate_random_message()
        producer.produce(topic, key=str(guid), value=message)
        producer.flush()
        print(f"Produced message: {message}")
        time.sleep(0.5) 

except KeyboardInterrupt:
    pass

finally:
    # Close the Kafka producer
    producer.flush(30)
    producer.close()