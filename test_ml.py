import json
import requests
import time
from vitals_generator import preprocess_vitals  # Changed import
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Replace these with your actual endpoint details from Azure ML > Endpoints > HealthEndpoint
SCORING_URI = "https://health-endpoint.eastus2.inference.ml.azure.com/score"  # Update with your Scoring URI
API_KEY = "1Byce5acHIWOHutRcueVrjTQUNrsS1Bgiwet0iFh4hbLOSAPGomJJQQJ99BCAAAAAAAAAAAAINFRAZML1jkq"  # Update with your Key from HealthEndpoint

def setup_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def test_prediction():
    session = setup_session()
    try:
        for _ in range(5):  # Test 5 predictions to stay within free tier limits
            vitals = preprocess_vitals()
            payload = json.dumps({
                "input_data": {
                    "data": [vitals]  # Nested structure for Azure ML endpoints
                }
            })
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            }
            response = session.post(
                SCORING_URI,
                data=payload,
                headers=headers,
                timeout=30  # 30-second timeout
            )
            response.raise_for_status()  # Raise exception for bad responses
            prediction = response.json()
            pred_value = prediction[0] if isinstance(prediction, list) and prediction else None
            if not pred_value:
                raise ValueError(f"Unexpected response format: {prediction}")
            print(f"Vitals: {vitals}, Prediction: {pred_value}")
    except requests.exceptions.Timeout:
        print("Error: Connection timed out. Check your internet or endpoint status.")
    except requests.exceptions.ConnectionError:
        print("Error: Connection failed. Verify endpoint URI and network settings.")
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error occurred - {e.response.text}")
    except ValueError as e:
        print(f"Error: Invalid response format - {e}")
    except Exception as e:
        print(f"Error: Unexpected error - {e}")
    finally:
        print("Testing complete. Stop the endpoint in Azure ML to avoid charges.")
        session.close()  # Close session to free resources

if __name__ == "__main__":
    test_prediction()