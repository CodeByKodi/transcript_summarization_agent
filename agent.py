import os
from google.adk import Agent

root_agent = Agent(
    name="transcript_summarization_agent",
    description="Summarizes chat transcripts.",
    model="gemini-1.5-pro",
    instruction="Summarize the provided chat transcript."
)

# transcript_summarization_agent/deploy_to_agent_engine.py
import os
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv
from agent import root_agent

load_dotenv()

vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    staging_bucket="gs://geni-project_cloudbuild",
)

remote_app = agent_engines.create(
    display_name=os.getenv("APP_NAME", "Agent App"),
    agent_engine=root_agent,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
        "cloudpickle==3.1.1"
    ]
)
