#!/bin/bash

# Start producer in the background
python producer.py &

# Start consumer in the foreground
python main.py
