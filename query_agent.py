import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# === Configuration ===
SERVICE_ACCOUNT_FILE = "service-account.json"
AGENT_ENDPOINT = "https://asia-south1-aiplatform.googleapis.com/v1/projects/geni-project/locations/asia-south1/reasoningEngines/6280973367809933312:query"
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

# === Load service account and generate access token ===
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
credentials.refresh(Request())
access_token = credentials.token

# === Construct the payload ===
payload = {
    "text": "Hi, I want to buy a boat for $50,000.",
    "userId": "u_456",
    "sessionId": "session_001"
}

# === Send the POST request ===
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

response = requests.post(AGENT_ENDPOINT, headers=headers, json=payload)

# === Print response ===
print("Status Code:", response.status_code)
print("Response JSON:")
print(json.dumps(response.json(), indent=2))