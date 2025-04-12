#!/bin/bash

echo "Creating localstack S3 bucket..."
awslocal --endpoint-url=http://localhost:4566 s3 mb s3://sci-tech-scholars-bucket

echo "Creating localstack lambda..."
echo "VARS: ${DEBUG} ${AWS_ACCESS_KEY_ID} ${AWS_SECRET_ACCESS_KEY} ${PYDEVD_DISABLE_FILE_VALIDATION}"
# Create a lambda with mounted zip file
awslocal --endpoint-url=http://localhost:4566 lambda create-function \
--function-name json-converter \
--zip-file fileb:///var/lib/localstack/lambda/json-converter.zip \
--environment "Variables={ENVIRONMENT=${ENVIRONMENT}, DEBUG=${DEBUG}, LAMBDA_DEBUG_MODE=${LAMBDA_DEBUG_MODE}, \
    AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}, AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}, \
    PYDEVD_DISABLE_FILE_VALIDATION=${PYDEVD_DISABLE_FILE_VALIDATION}}" \
--handler main.lambda_handler --runtime python3.12 \
--role arn:aws:iam::000000000000:role/lambda-role 

echo "Waiting until lambda transitions from Pending to Active..."
# https://docs.localstack.cloud/user-guide/aws/lambda/#function-in-pending-state
awslocal lambda wait function-active-v2 --function-name json-converter && \
echo "Creating localstack S3 bucket notification ..."

# Create S3 bucket notification configuration
awslocal --endpoint-url=http://localhost:4566 \
s3api put-bucket-notification-configuration --bucket sci-tech-scholars-bucket \
--notification-configuration file:///var/lib/localstack/s3-notif-config.json