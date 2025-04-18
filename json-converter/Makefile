# Name of the virtual environment directory
VENV_DIR = venv

VENV_PIP = $(VENV_DIR)/bin/pip
VENV_SITE_PACKAGES = $(VENV_DIR)/lib/python3.12/site-packages/

# If you are using Windows, uncomment the following lines below and comment the above lines
# VENV_PIP = $(VENV_DIR)/Scripts/pip
# VENV_SITE_PACKAGES = $(VENV_DIR)/Lib/site-packages/

# Python executable
PYTHON = python3.12

#############################
#### Virtual Environment ####
#############################

venv-create: # Create python virtual environment
	$(PYTHON) -m venv $(VENV_DIR)

venv-install: # Install dependencies in the virtual environment
	$(VENV_PIP) install -r requirements.txt

venv-freeze: # Export dependencies to requirements.txt
	$(VENV_PIP) freeze > requirements.txt

#############################
#### Local Infrastructure ###
#############################

# https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-dependencies
local-provision: # Provision local resources via docker-compose
	@echo "Packaging Lambda function..."
	zip ./localstack/json-converter.zip ./$(VENV_SITE_PACKAGES) ./src/
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
		--key input/data.json --body=tests/data.json
	@echo "Sample data uploaded successfully."

local-show-s3: # Show objects in local S3 bucket
	@echo "Showing objects in local S3..."
	aws --endpoint-url=http://localhost:4566 s3api list-objects-v2 --bucket sci-tech-scholars-bucket

local-follow-lambda: # Tail logs of localstack Lambda function
	aws --endpoint-url=http://localhost:4566 logs tail '/aws/lambda/json-converter' --follow

run-unit-tests: # Run unit tests
	pytest tests/unit/ --disable-pytest-warnings -p no:cacheprovider

run-it-tests: # Run integration tests
	pytest tests/integration/ --disable-pytest-warnings -p no:cacheprovider


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

upload-sample: # Upload sample data to S3 bucket
	@echo "Uploading sample data to S3..."
	aws s3 cp tests/data.json s3://sci-tech-scholars-bucket/input/data.json
	@echo "Sample data uploaded successfully."

# Provision AWS resources and upload sample data to S3, triggering the Lambda function
full-start: provision upload-sample

delete-s3-bucket: # Delete S3 bucket, including all objects (if any)
	@echo "Deleting S3 bucket..."
	aws s3 rb s3://sci-tech-scholars-bucket --force
	@echo "S3 bucket deleted successfully."
