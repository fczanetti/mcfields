from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    bucket_name = 'mcfields-media'
    location = 'photos_from_texts'
    querystring_auth = False
    file_overwrite = False
