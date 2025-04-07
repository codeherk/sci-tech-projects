# JSON to CSV Converter

This project provides an AWS Lambda function that converts JSON files uploaded to an S3 bucket into CSV format and stores the resulting CSV files back in the same bucket.

## Table of Contents

- [JSON to CSV Converter](#json-to-csv-converter)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Architecture](#architecture)
  - [Setup Instructions](#setup-instructions)
    - [Prerequisites](#prerequisites)

## Overview

The `json-converter` project automates the conversion of JSON files to CSV format using an AWS Lambda function. When a JSON file is uploaded to the `input/` folder of the S3 bucket, the Lambda function is triggered, processes the file, and uploads the resulting CSV file to the `output/` folder of the same bucket.

## Architecture

- **AWS S3**: Stores the input JSON files and the output CSV files.
- **AWS Lambda**: Processes the JSON files and converts them to CSV.
- **AWS IAM**: Manages permissions for the Lambda function to access S3 and CloudWatch logs.
- **Terraform**: Provisions the AWS resources.

## Setup Instructions

### Prerequisites

1. Install [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).
2. Install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
3. Configure your AWS CLI with appropriate credentials:
   ```bash
   aws configure
   ```
4. Ensure you have the necessary permissions to create and manage AWS resources.
5. Install [Python 3.8+](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/).
