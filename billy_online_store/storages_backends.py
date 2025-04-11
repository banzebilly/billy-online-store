from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = "static"  # change this to "static" instead of "staticfiles"
    default_acl = None


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
    default_acl = None
