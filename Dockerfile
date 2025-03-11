# Use a lightweight Python 3.11 base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy your Python files and requirements into the container
COPY simulate_vitals.py vitals_generator.py requirements.txt .

# Install the required Python packages (dependencies)
RUN pip install --no-cache-dir -r requirements.txt

# Set an environment variable for the IoT Hub connection string (optional, will be passed at runtime)
ENV IOT_HUB_CONNECTION_STRING="HostName=ExpertIoTHub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=HMRQcHtex6x6sKwybuZR7nYVQrP5sHC5AAIoTKerePc="

# Specify the command to run your Python script when the container starts
CMD ["python", "simulate_vitals.py"]