import boto3
import pytest
import os
import time

# Configuration
LOCALSTACK_ENDPOINT = "http://localhost:4566"
BUCKET_NAME = "sci-tech-scholars-bucket"
DATA_JSON = "tests/data.json"
DATA_KEY = "input/data.json"
GENERATED_CSV = "output.csv"


def clean_s3_bucket(s3_client):
    """Fixture to remove all objects from S3 bucket."""
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    if "Contents" in response:
        for obj in response["Contents"]:
            s3_client.delete_object(Bucket=BUCKET_NAME, Key=obj["Key"])

@pytest.fixture(scope="module")
def s3_client():
    """Fixture to create an S3 client."""
    client = boto3.client(
        "s3",
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )
    clean_s3_bucket(client)
    return client

def test_notification_processing(s3_client):
    """Test uploading a JSON file and checking for a generated CSV file."""
    # Upload the JSON file to the S3 bucket
    with open(DATA_JSON, "rb") as f:
        s3_client.upload_fileobj(f, BUCKET_NAME, DATA_KEY)

    # Simulate processing time (replace this with actual processing logic if needed)
    time.sleep(5)

    # Check if the generated CSV file exists in the bucket
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    assert "Contents" in response, "No files found in the bucket."
    files = [obj["Key"] for obj in response["Contents"]]
    assert any(file.startswith("output/data_") and file.endswith(".csv") for file in files), \
        "No CSV file with the expected format found in the bucket after uploading JSON file."