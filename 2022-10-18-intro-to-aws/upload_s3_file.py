
import os
import boto3


session = boto3.session.Session(
    aws_access_key_id=os.environ["JD_AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["JD_AWS_SECRET_ACCESS_KEY"]
)

s3 = session.client("s3")
bucket = "quincy-tech-group"


s3.upload_file(
    Filename="data.json",
    Bucket=bucket,
    Key="data.json"
)

print("File uploaded!")
