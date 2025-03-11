from azure.ai.ml import MLClient, Input, Output
from azure.ai.ml.entities import Job, Command
from azure.identity import DefaultAzureCredential
from azure.ai.ml.constants import AssetTypes
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import os

# Authenticate (use Azure CLI credentials)
credential = DefaultAzureCredential()
ml_client = MLClient(
    credential=credential,
    subscription_id="d7513e01-9e93-4556-b6d2-664349d840d8",  # Replace with your Azure subscription ID
    resource_group_name="AI-Driven-Predictive-Healthcare-Ecosystem",
    workspace_name="ExpertML"
)

# Load dataset (faster local load for small data)
dataset = ml_client.data.get(name="VitalsDataset", version="5")
data_path = dataset.path
df = pd.read_csv(data_path)

# Prepare data (drop unnecessary columns, ensure numeric types, fast processing)
X = df[['heart_rate', 'oxygen']].astype(float)  # Ensure numeric, speed up
y = df['status'].map({'High': 1, 'Normal': 0})  # Convert to binary 1/0

# Split data (70/30, fast with random_state for reproducibility)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, shuffle=True)

# Train Logistic Regression (optimized for speed, fewer iterations)
model = LogisticRegression(max_iter=50, C=1.0, solver='lbfgs')  # Fewer iterations, faster convergence
model.fit(X_train, y_train)

# Evaluate (quick check, minimal overhead)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Register model (lightweight, certification-friendly)
model_path = "./outputs/health_logistic_model.pkl"
os.makedirs("./outputs", exist_ok=True)
pd.to_pickle(model, model_path)

registered_model = Model(
    path=model_path,
    type=AssetTypes.CUSTOM_MODEL,
    name="health_logistic_model",
    description="Optimized Logistic Regression for health predictions"
)
ml_client.models.create_or_update(registered_model)

# Optional: Deploy for real-time scoring (minimal, fast setup)
from azure.ai.ml.entities import Endpoint, OnlineRequestSettings
endpoint = Endpoint(
    name="HealthEndpoint",
    description="Fast endpoint for health predictions",
    auth_mode="key"
)
ml_client.online_endpoints.begin_create_or_update(endpoint, wait=True)  # Synchronous for quick deployment

# Score a sample (fast, using simulate_vitals.py)
from simulate_vitals import preprocess_vitals
sample = preprocess_vitals()
prediction = model.predict([[sample['heart_rate'], sample['oxygen']]])
print(f"Sample Prediction: {'High' if prediction[0] == 1 else 'Normal'}")

# Clean up (stop compute manually after testing)
# Ensure mlcompute is stopped via Portal or CLI: az ml compute stop --name mlcompute --workspace-name ExpertML