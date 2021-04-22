from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    # default_acl = 'private'  # for private access
    file_overwrite = True
