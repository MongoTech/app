import boto3


AWS_ACCESS_KEY_ID = "VG7WONEHRGNFPHIIXLSN" # noqa
AWS_SECRET_ACCESS_KEY = "6FG+T6STRNmaoQZ/zF9SX9gxsK13tBHzgfMSBKV6mUg" # noqa
AWS_BUCKET = 'cdn3d' # noqa
AWS_REGION = 'fra1' # noqa
AWS_ENDPOINT = 'https://fra1.digitaloceanspaces.com' # noqa

def is_s3_exists(file)
    s3_client = boto3.client('s3',
                             region_name=AWS_REGION,
                             endpoint_url=AWS_ENDPOINT,
                             aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)



    result = s3_client.list_objects_v2(Bucket=AWS_BUCKET, Prefix="1000444.zip")
    #
    # for res in result:
    #     print(res, result[res])