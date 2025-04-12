##############################
# S3
##############################

# S3 Bucket to hold the JSON and CSV files
resource "aws_s3_bucket" "sci_tech_scholars" {
  bucket = "sci-tech-scholars-bucket"
}

##############################
# IAM
##############################

# Policy to allow lambda to assume the role, granting it permissions
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda" {
  name               = "lambda_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}


# Add policy that allows lambda to write to the bucket
resource "aws_iam_policy" "lambda_s3" {
  name        = "lambda_s3_policy"
  description = "IAM policy for Lambda to access S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
        ]
        Resource = "${aws_s3_bucket.sci_tech_scholars.arn}"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
        ]
        Resource = "${aws_s3_bucket.sci_tech_scholars.arn}/*"
      }
    ]
  })
}

# Attach the s3 policy to the role
resource "aws_iam_role_policy_attachment" "lambda_s3" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_s3.arn
}

# Add policy that allows lambda to write to CloudWatch logs
resource "aws_iam_policy" "lambda_logs" {
  name        = "lambda_logs_policy"
  description = "IAM policy for Lambda to write to CloudWatch logs"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
    ]
  })
}

# Attach the cloudwatch policy to the role
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda_logs.arn
}


##############################
# Lambda
##############################
# Zips the lambda function code
data "archive_file" "lambda" {
  type        = "zip"
  source_file = "main.py"
  output_path = "localstack/json-converter.zip"
}

resource "aws_lambda_function" "json_converter" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "localstack/json-converter.zip"
  function_name = "json_converter"
  role          = aws_iam_role.lambda.arn
  # The handler is the name of the file (without the .py) and the function name
  handler       = "main.lambda_handler"

  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "python3.12"

  environment {
    variables = {
      S3_BUCKET = "${aws_s3_bucket.sci_tech_scholars.bucket}"
    }
  }
}

# S3 Bucket notification to trigger the Lambda function for files in the input/ path
resource "aws_lambda_permission" "allow_bucket" {
    statement_id  = "AllowExecutionFromS3"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.json_converter.function_name
    principal     = "s3.amazonaws.com"
    
    # The bucket ARN is used to specify the source of the event
    source_arn = "${aws_s3_bucket.sci_tech_scholars.arn}"
}

resource "aws_s3_bucket_notification" "s3_trigger" {
    bucket = aws_s3_bucket.sci_tech_scholars.id

    lambda_function {
        lambda_function_arn = aws_lambda_function.json_converter.arn
        events              = ["s3:ObjectCreated:*"]
        filter_prefix       = "input/"
        filter_suffix       = ".json"
    }

    depends_on = [aws_lambda_permission.allow_bucket]
}