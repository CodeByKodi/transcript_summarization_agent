import os
import logging
from dotenv import load_dotenv
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler
import vertexai
from vertexai import agent_engines

load_dotenv()
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")
app_name = os.getenv("APP_NAME", "Transcript Summarizer")
bucket_name = f"gs://geni-project_cloudbuild"

cloud_logging_client = google.cloud.logging.Client(project=project_id)
handler = CloudLoggingHandler(cloud_logging_client, name="transcript-summarizer")
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(handler)

vertexai.init(project=project_id, location=location, staging_bucket=bucket_name)
ae_apps = agent_engines.list(filter=f'display_name="{app_name}"')
ae_apps_list = list(ae_apps)
print("Available apps:", ae_apps_list)

if not ae_apps_list:
    print("❌ No agent found with name:", app_name)
    exit(1)

remote_app = ae_apps_list[0]
remote_session = remote_app.create_session(user_id="u_456")
print("Session created:", remote_session)

transcript = """
    Virtual Agent: Hi, I am a vehicle sales agent. How can I help you?
    User: I'd like to buy a boat.
    Virtual Agent: A big boat, or a small boat?
    User: How much boat will $50,000 get me?
    Virtual Agent: That will get you a very nice boat.
    User: Let's do it!
"""

for event in remote_app.stream_query(user_id="u_456", session_id=remote_session["id"], message=transcript):
    print("Received event:", event)
    for part in event["content"]["parts"]:
        if "text" in part:
            print("[DEBUG] Agent responded with:", part["text"])
            print("[remote response]", part["text"])
            logging.info("[remote response] " + part["text"])

cloud_logging_client.flush_handlers()