import os
import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv
from agent import root_agent
from google.oauth2 import service_account

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

credentials = service_account.Credentials.from_service_account_file(
    "service-account.json"
)

vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    staging_bucket="gs://geni-project_cloudbuild",
    credentials=credentials,
)

print(f"Using service account: {credentials.service_account_email}")

from google.cloud import storage
from google.cloud.exceptions import Forbidden

# ✅ Optional: test GCS access before deploying agent
def validate_gcs_access():
    client = storage.Client(credentials=credentials)
    bucket_name = "geni-project_cloudbuild"
    test_blob_name = "adk-upload-test.txt"

    try:
        bucket = client.bucket(bucket_name)

        # Check IAM permission for write access
        permissions = bucket.test_iam_permissions(["storage.objects.create"])
        if "storage.objects.create" not in permissions:
            raise PermissionError(f"❌ Service account does not have 'storage.objects.create' permission on bucket {bucket_name}")

        # Proceed with test upload
        blob = bucket.blob(test_blob_name)
        with blob.open("w") as f:
            f.write("This is a test file to verify GCS permissions.")
        print(f"✅ Successfully uploaded test file to {bucket_name}")
        blob.delete()
        print(f"🧹 Test file cleaned up")
    except Exception as e:
        print(f"❌ Failed GCS access check: {e}")
        exit(1)

validate_gcs_access()

try:
    # Confirm bucket exists
    gcs_client = storage.Client(credentials=credentials)
    bucket_name = "geni-project_cloudbuild"
    if not gcs_client.lookup_bucket(bucket_name):
        raise Exception(f"❌ Bucket '{bucket_name}' not found or not accessible by the service account.")

    # Proceed with deployment
    remote_app = agent_engines.create(
        display_name=os.getenv("APP_NAME", "Agent App"),
        agent_engine=root_agent,
        requirements=[
            "google-cloud-aiplatform[adk,agent_engines]",
            "cloudpickle==3.1.1"
        ]
    )
except Forbidden as e:
    print(f"❌ GCS write permission denied: {e}")
    exit(1)
except Exception as e:
    print(f"❌ Failed to deploy agent engine: {e}")
    exit(1)
