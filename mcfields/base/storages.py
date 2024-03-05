from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    default_acl = "public-read"
    location = "public"
    querystring_auth = False
