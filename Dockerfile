# Use a Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy local files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script
COPY start.sh /app/start.sh

# Give execution permission
RUN chmod +x /app/start.sh

# Set the default command to run the script
CMD ["/app/start.sh"]
