import random
import time
import json
import os
from azure.iot.device import IoTHubDeviceClient, Message
from vitals_generator import preprocess_vitals  # Import from separate file (create if not done)

# Use environment variable for CONNECTION_STRING, with fallback for testing
CONNECTION_STRING = os.getenv("IOT_HUB_CONNECTION_STRING", "HostName=ExpertIoTHub.azure-devices.net;DeviceId=SimDevice1;SharedAccessKey=yfDXQ98eD5hqHxBuYE5XaWuPQfwnKE95QhidAers08g=")

def main():
    # Connect to IoT Hub
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    try:
        for _ in range(10):  # Small batch for free tier
            data = preprocess_vitals()
            message = Message(json.dumps(data))
            client.send_message(message)
            print(f"Sent from container: {data}")
            time.sleep(2)  # Mimic real-time
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.shutdown()

if __name__ == "__main__":
    main()