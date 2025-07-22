import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from sseclient import SSEClient

# === Config ===
SERVICE_ACCOUNT_FILE = "service-account.json"
REGION = "asia-south1"
PROJECT_ID = "geni-project"
ENGINE_ID = "6280973367809933312"
ENDPOINT = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/reasoningEngines/{ENGINE_ID}:streamQuery?alt=sse"

# === Auth ===
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
credentials.refresh(Request())
access_token = credentials.token

# === Payload ===
data = {
    "text": "Hi, I want to buy a boat for $50,000.",
    "userId": "u_456",
    "sessionId": "session_001"
}

# === Headers ===
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# === Stream response ===
response = requests.post(ENDPOINT, headers=headers, data=json.dumps(data), stream=True)
if response.status_code != 200:
    print("❌ Request failed:")
    print("Status:", response.status_code)
    print(response.text)
    exit(1)
client = SSEClient(response)

print("🧠 Streaming Response:")
for event in client.events():
    print("→", event.data)