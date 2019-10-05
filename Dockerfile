FROM python:3.7-slim

RUN apt-get update && apt-get install -y net-tools
# Set the working directory to /app
WORKDIR /app/

# Copy the current directory contents into the container at /app
COPY . /app/

ENV PYTHONPATH /app
# Run app.py when the container launches
CMD ["python", "discovery_service/listener.py"]
