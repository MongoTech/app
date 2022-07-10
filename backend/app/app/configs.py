import os

AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "eu-west-1")
EC2_IMAGE_ID = os.getenv("EC2_IMAGE_ID", "ami-0d71ea30463e0ff8d")
EC2_MIN_COUNT = os.getenv("EC2_MIN_COUNT", 1)
EC2_MAX_COUNT = os.getenv("EC2_MAX_COUNT", 1)
EC2_INSTANCE_TYPE = os.getenv("EC2_INSTANCE_TYPE", "t2.micro")
