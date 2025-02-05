# Real time data processing using Kafka

## Abstract

Real-time temperature data processing plays a crucial role in applications like weather forecasting, environmental monitoring, and industrial automation. The ability to process temperature data in real-time provides valuable insights for decision-making. This project focuses on real-time analysis of temperature data collected across the United States from IoT sensors. Each state in the U.S. has multiple temperature sensors installed, continuously sending data to a Kafka server. Every three seconds, a Kafka client retrieves this streaming data, which is then processed and analyzed.


## Data Simulation and Processing

To simulate IoT devices, the producer.py file generates random, continuous messages representing temperature sensor readings. These messages are published on a Kafka topic.

I decided to host Kafka and Kafka UI on Docker to simplify deployment and monitoring. Additionally, I built Docker images for the producer and consumer, ensuring a modular and scalable architecture.

## Data Cleaning and Transformation

The Kafka consumer processes the incoming data by:
- Removing messages with null values in specific fields.
- Flattening the temperature payload
- Adding a field "processing timestamp"
- Converting event timestamps into UTC.


## Aggregation and Derived Data

To derive insights, the consumer publishes processed data to a separate Kafka topic, computing:
- Total number of sensors per state.
- Average temperature per state.
- Total number of messages consumed so far.


## Example Data Format

The generated JSON messages follow this structure:
```
{
  "guid": "0-ZZZ12345678-53X",
  "destination": "0-AAA12345678",
  "state": "WV",
  "eventTime": "1738738714",
  "payload": {
    "format": "urn:example:sensor:temp",
    "data": {
      "temperature": "51.83263738093986"
    }
  }
}
```

| Field | Description | 
| --- |--- |
| guid | A global unique identifier which is associated with a sensor | 
| destination | An identifier of the destination which sensors send data to |
| state | A randomly chosen U.S. state. |
| eventtime | A timestamp that the data is generated. |
| temparature | Calculated by continuously adding a random number (between -5.0 to 5.0) to each state's average annual temperature every time the data is generated. |


### Processed Message Format

After cleaning and transformation, the processed messages are structured as follows:

```
{
  "guid": "0-ZZZ12345678-53X",
  "destination": "0-AAA12345678",
  "State": "WV",
  "eventTime": 1738738714,
  "temperature": 51.83263738093986,
  "timestamp_in_utc": "2025-02-05 06:58:34",
  "processed_time": "2025-02-05 06:58:41"
}
```


### Aggregated Message Format

The aggregated data computed over time is structured as follows:

```
{
	"total_sensors_by_state": {
		"WV": 8,
		"RI": 9,
		"CA": 10,
		"OK": 8,
		"MS": 6,
		"NY": 6,
		...
	},
	"avg_temp_by_state": {
		"WV": 49.75194185247884,
		"RI": 51.16258590969683,
		"CA": 59.46853763827388,
		"OK": 60.68093387728677,
		"MS": 64.06487954758667,
		"NY": 46.81063762044777,
                ...
	},
	"total_messages": 332
}
```

### **How to run the application**

- Install Docker Desktop    
    - Docker Desktop is required to build and run the containerized environment.
      
- Clone the Repository
    - Clone the project repository to your local machine using the command  `git clone https://github.com/GopiOddiraju/Real-time-data-processing-using-Kafka-and-Docker`

- Navigate to the project directory and start the application using the command  `docker-compose up`

    This command builds and runs all the services defined in the docker-compose .yaml file

- When we execute docker-compose up, the following services are started in sequence based on the dependencies defined in docker-compose.yaml file

    - Zookeeper: Initializes zookeeper, which acts as the coordination service for managing Kafka brokers.
    - Kafka Broker: A Kafka instance that processes and manages message streams. 
    - Kafka UI: Provides a user-friendly web interface for monitoring and managing Kafka clusters.
    - Producer Service: Sends simulated user login data to the Kafka topic 'IoT-data'.
    - Consumer Service: Reads and processes data from the Kafka topic 'IoT-data'.



## **Detailed Implementation Walkthrough**

- **docker-compose.yaml**

    I created a docker-compose.yml file to host multiple services essential for a Kafka-based streaming setup:
    - Zookeeper & Kafka: The setup includes Zookeeper (for managing Kafka brokers) and a Kafka broker, configured with advertised listeners for both internal and external access.
    - Kafka UI: A web-based interface is included to monitor Kafka topics, consumers, and producers.
    - Python Producer & Consumer: Custom-built Python services act as a Kafka producer and consumer, to send and receive messages.
    - Networking & Dependencies: All services are connected via a dedicated kafka-network, ensuring seamless communication between them. Dependencies are set to ensure services start in the correct order.

- **Adding requirements.txt**
    
    To manage dependencies, I created a requirements.txt file:
    - Set up a virtual environment using `python -m venv venv` and activated it with `.\venv\Scripts\Activate.ps1` (On Windows).
    - Installed the required dependency (confluent_kafka) using `pip install confluent_kafka`.
    - `Ran pip freeze > requirements.txt` to generate a list of installed packages along with the versions, ensuring consistent environment setup.


- **Creating the Dockerfile**

    - It defines how to build a container for the application.
    - Automatically installs the dependencies listed in requirements.txt
    - Copies the project files into the container's /app directory, making the code available during runtime.
    - Specifies start.sh as the script to execute when the container starts, ensuring the consumer processes messages without manual intervention.


- **Key Points**

    - **Handling Topic Creation Timing with `time.sleep(10)`**.
        - Added a delay because, in this current setup, the source topic is not readily available, which throws an error with the consumer.
          

    - **Designing for two topics: Processed data and Aggregated data**

        - **processed-data**:
            - Contains messages that have undergone validations and transformations, including:
                - Adding a processed_time field for tracking when the message was processed.
                - Converting the original timestamp into UTC format.
                - Filtering out invalid messages(e.g., missing fields, messages with null values in specific fields).
        
        - **Aggregated-data**:
            - Captures real-time counts of sensors by each state, average temperature by each state, and total number of messages consumed so far.
            - Messages are produced on this topic every 60 seconds, providing a snapshot of temperature trends.
            - This separation allows the analytics team to monitor device-specific trends in real-time without interfering with the raw message data processing.






