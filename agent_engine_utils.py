import os
import fire
from dotenv import load_dotenv
import vertexai
from vertexai import agent_engines

load_dotenv()
vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    staging_bucket=os.getenv("STAGING_BUCKET")
)

def list():
    for agent in agent_engines.list():
        print(agent.display_name)
        print(agent.resource_name + "\n")

def delete(resource_name):
    agent_engines.delete(resource_name, force=True)

if __name__ == "__main__":
    fire.Fire()