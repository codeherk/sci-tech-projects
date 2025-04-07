deploy:
	@echo "Deploying AWS resources..."
	terraform apply -auto-approve

destroy:
	@echo "Destroying AWS resources..."
	@$(MAKE) delete-s3-bucket
	terraform destroy -auto-approve

full-start:
	@$(MAKE) deploy
	@$(MAKE) upload-sample

upload-sample:
	@echo "Uploading sample data to S3..."
	aws s3 cp data.json s3://sci-tech-scholars-bucket/input/data.json
	@echo "Sample data uploaded successfully."

delete-s3-bucket:
	@echo "Deleting S3 bucket..."
	aws s3 rb s3://sci-tech-scholars-bucket --force
	@echo "S3 bucket deleted successfully."
