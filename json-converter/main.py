# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import json
import urllib.parse
import boto3

import csv
import io
from datetime import datetime
import os
import logging

logger = logging.getLogger()

if os.environ.get('DEBUG') == '1':
    logger.setLevel("DEBUG")
else:
    logger.setLevel("INFO")

logger.info('Loading function')
s3=boto3.client('s3')

# check that client is working
if os.environ.get('ENVIRONMENT') == 'local':
    logger.debug("Running in localstack")
    # s3 = boto3.client('s3', endpoint_url='http://localhost:4566', region_name='us-east-1')
    try:
        # get endpoint URL
        endpoint_url = s3.meta.endpoint_url
        logger.debug(f"Endpoint URL: {endpoint_url}")
        s3.list_buckets()
        logger.debug("S3 client is working")
    except Exception as e:
        logger.debug(f"S3 client is not working. Error: {e}")


def lambda_handler(event, context):
    # TODO: get remote debugpy to work with localstack
    # if os.environ.get('DEBUG') == '1':
    #     import sys, glob
    #     sys.path.append(glob.glob("venv/lib/python*/site-packages")[0])
    #     import debugpy
    #     debugpy.listen(19891)
    #     debugpy.wait_for_client()  # blocks execution until client is attached

    logger.info("Processing received event...")
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        logger.info(f"Getting object from S3: bucket={bucket}, key={key}")
        response = s3.get_object(Bucket=bucket, Key=key)
        logger.info(f"Object {key} retrieved from S3 bucket {bucket}")
        logger.debug("CONTENT TYPE: " + response['ContentType'])

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

        logger.info(f"CSV file uploaded to S3 at {output_filename}")
        return output_filename
    except Exception as e:
        logger.debug(e)
        logger.info('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e