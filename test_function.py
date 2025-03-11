import json
from simulate_vitals import preprocess_vitals
from azure.digitaltwins.core import DigitalTwinsClient
from azure.identity import DefaultAzureCredential

ADT_URL = "https://HealthTwins.api.eus.digitaltwins.azure.net"

def main(event: str) -> None:
    print(f"Event received: {event}")
    data = json.loads(event)
    credential = DefaultAzureCredential()
    client = DigitalTwinsClient(ADT_URL, credential)
    twin_id = data["patient_id"]
    twin_data = {
        "$metadata": {"$model": "dtmi:health:patient;1"},
        "heart_rate": data["heart_rate"],
        "oxygen": data["oxygen"],
        "status": data["status"]
    }
    try:
        client.upsert_digital_twin(twin_id, twin_data)
        print(f"Updated twin {twin_id}")
    except Exception as e:
        print(f"Error updating twin: {e}")

data = preprocess_vitals()
event = json.dumps(data)
print(f"Simulated event: {event}")
main(event)