# Name of the virtual environment directory
VENV_DIR = venv
LANG = es

# Python executable
PYTHON = python3.12

#############################
#### Virtual Environment ####
#############################
# Create the virtual environment
create-venv:
	$(PYTHON) -m venv $(VENV_DIR)

# Install dependencies
venv-install:
	$(VENV_DIR)/bin/pip install -r requirements.txt

# Export dependencies to requirements.txt
venv-freeze:
	$(VENV_DIR)/bin/pip freeze > requirements.txt

#############################
#### Local Infrastructure ###
#############################

# https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-dependencies
local-provision: # Provision local resources via docker-compose
	@echo "Packaging Lambda function..."
	zip -rq ./localstack/lambda/lambda_function_payload.zip ./venv/lib/python3.12/site-packages/ main.py
	@echo "Provisioning local resources..."
	docker-compose up -d --build
	@echo "Local resources provisioned successfully."

local-destroy: # Destroy local resources via docker-compose
	@echo "Destroying local resources..."
	docker-compose down
	@echo "Local resources destroyed successfully."

local-upload-sample: # Upload sample data to local S3 bucket
	@echo "Uploading sample data to local S3..."
	aws --endpoint-url=http://localhost:4566 s3api put-object --bucket sci-tech-scholars-bucket \
		--key /input/data.json --body=data.json
	@echo "Sample data uploaded successfully."

local-follow-lambda:
	aws --endpoint-url=http://localhost:4566 logs tail '/aws/lambda/json-converter' --follow


#############################
###### Infrastructure #######
#############################
provision: # Provision AWS resources via terraform
	@echo "Provisioning AWS resources..."
	terraform apply -auto-approve

destroy: # Destroy AWS resources via terraform
	@echo "Destroying AWS resources..."
	@$(MAKE) delete-s3-bucket
	terraform destroy -auto-approve

full-start: # Provision AWS resources and upload sample data to S3, triggering the Lambda function
	@$(MAKE) provision
	@$(MAKE) upload-sample

upload-sample: # Upload sample data to S3 bucket
	@echo "Uploading sample data to S3..."
	aws s3 cp data.json s3://sci-tech-scholars-bucket/input/data.json
	@echo "Sample data uploaded successfully."

delete-s3-bucket: # Delete S3 bucket, including all objects (if any)
	@echo "Deleting S3 bucket..."
	aws s3 rb s3://sci-tech-scholars-bucket --force
	@echo "S3 bucket deleted successfully."
