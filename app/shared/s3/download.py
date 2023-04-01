"""
@author: Kuro
"""
from settings import Config
import boto3
from botocore.exceptions import NoCredentialsError


def get_file_from_bucket(filename, file_type="files"):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=Config.aws_access_key_id,
        aws_secret_access_key=Config.aws_secret_access_key,
    )

    bucket = Config.s3_image_bucket
    if file_type == "image":
        bucket = Config.s3_image_bucket
    elif file_type == "video":
        bucket = Config.s3_video_bucket

    try:
        file = s3.get_object(Bucket=bucket, Key=filename)
        return file["Body"].iter_chunks()
    except FileNotFoundError:
        print("The file was not found")
        return {"success": False, "error": "File not found"}
    except NoCredentialsError:
        print("Credentials not available")
        return {"success": False, "error": "Credentials not available"}
    except Exception as e:
        print(type(e), e)
        return {"success": False, "error": "File not found in bucket"}
