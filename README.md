# Real-time-data-processing-using-Kafka-and-PySpark

## Abstract

Real-time temperature data processing is a crucial aspect in many applications, including weather forecasting, environmental monitoring, and industrial processes. The ability to quickly and accurately process temperature data in real-time provides valuable information for decision-making. This project is about real-time analysis of temperature data collected across the United States from IoT sensors. Each state in U.S. has many temperature sensors installed. Each sensor provides temperature data on a regular basis to a Kafka server. Every three seconds, the Kafka client retrieves the streaming data. Pyspark will be used to process and analyze them in real time.


The project's main objective is to explore Kafka and PySpark and to use the functionalities offered by them on the chosen data. Analyze the real-time data to find:

Total number of sensors by each state.

Average temperature by each state.

Total number of messages processed.

Total number of sensors.




The sensor_data.py generates simulated IoT sensor data in JSON format. It simulates temperature sensor data for a number of IoT devices, where each device is represented by a unique guid. The script takes a command-line argument to specify the number of JSON messages to generate.

The code initializes some dictionaries to store the current state and temperature of each device, as well as a dictionary with the average temperature for each US state. Then it loops num_msgs times and generates a random guid, selects a random US state, and calculates a random temperature value based on the current temperature of the device in the selected state. The temperature value is then included in a JSON message, along with the guid, a destination ID, and a timestamp.

The resulting JSON messages have the following structure:

{ "guid": "", "destination": "0-AAA12345678", "state": "", "eventTime": "", "payload": { "format": "urn:example:sensor:temp", "data": { "temperature": } } }


| Field | Description | 
| --- |--- |
| guid | A global unique identifier which is associated with a sensor | 
| destination | An identifier of the destination which sensors send data to |
| state | A randomly chosen U.S. state. |
| eventtime | A timestamp that the data is generated. |
| format | A format of data. |
| temparature | Calculated by continuously adding a random number (between -1.0 to 1.0) to each state's average annual temperature every time the data is generated. |
