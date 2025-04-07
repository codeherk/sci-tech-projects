# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import json
import urllib.parse
import boto3
import csv
import io
from datetime import datetime

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        # Get the object from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])

        # Read the JSON content from the S3 object
        data = json.loads(response['Body'].read().decode('utf-8'))

        # Create a CSV file in memory
        csv_buffer = io.StringIO()
        csv_writer = csv.writer(csv_buffer)

        # Write the header row
        header = data[0].keys()
        csv_writer.writerow(header)

        # Write the data rows
        for record in data:
            csv_writer.writerow(record.values())

        # Generate a unique filename for the output CSV
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_filename = f"output/data_{timestamp}.csv"

        # Upload the CSV file back to S3
        s3.put_object(Bucket=bucket, Key=output_filename, Body=csv_buffer.getvalue())

        print(f"CSV file uploaded to S3 at {output_filename}")
        return output_filename
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

