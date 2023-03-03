from settings import Config
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError


async def upload_file(filename, filetype="files"):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=Config.aws_access_key_id,
        aws_secret_access_key=Config.aws_secret_access_key,
    )

    # TODO: This does not handle unique types properly
    # filetype will be something like image/png or video/mp4 or audio/mpeg
    bucket = Config.s3_image_bucket
    if filetype == "image":
        bucket = Config.s3_image_bucket
    if filetype == "video":
        bucket = Config.s3_video_bucket

    bucket_file = f"{datetime.now().timestamp()}-{filename}"

    try:
        s3.upload_file(filename, bucket, bucket_file)
        print(f"successfully uploaded {bucket}/{bucket_file}")
        return bucket_file
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
