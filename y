version = 0.1
[default]
[default.deploy]
[default.deploy.parameters]
stack_name = "sam-app"
s3_bucket = "aws-sam-cli-managed-default-samclisourcebucket-wa67kvfzkfkr"
s3_prefix = "sam-app"
region = "us-east-1"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"
