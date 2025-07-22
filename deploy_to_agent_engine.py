import os
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv
from agent import root_agent
from google.oauth2 import service_account

load_dotenv()

credentials = service_account.Credentials.from_service_account_file(
    "service-account.json"
)

vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    staging_bucket="gs://geni-project_cloudbuild",
    credentials=credentials,
)

remote_app = agent_engines.create(
    display_name=os.getenv("APP_NAME", "Agent App"),
    agent_engine=root_agent,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
        "cloudpickle==3.1.1"
    ]
)
