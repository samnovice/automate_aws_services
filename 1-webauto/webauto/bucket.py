# -*- coding : utf-8 -*-
"""
Class BucketManager to manage S3 functions
    - Create a Bucket
    - List all Buckets
    - Configure Bucket for it to be used as website
    - Sync folder from given path to an bucket
"""

from pathlib import Path
import mimetypes
from botocore.exceptions import ClientError


class BucketManager:
    """Manage an S3 bucket."""

    def __init__(self, session):
        """Create and BucketManager object."""
        self.s3 = session.resource('s3')

    def all_buckets(self):
        """Get list of all S3 buckets."""
        return self.s3.buckets.all()

    def all_objects(self, bucket_name):
        """Get all objects inside an bucket."""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        """

        Create an bucket or if it already exists.
        initializing that bucket.
        """
        s3_bucket = None

        try:
            s3_bucket = self.s3.create_bucket(Bucket=bucket_name)
        except ClientError as error:
            if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3_bucket = self.s3.Bucket(bucket_name)
            else:
                raise error

        return s3_bucket

    def setpolicy(self, bucket):
        """Set up policy for S3 bucket for it to be public."""
        policy = """
        {
          "Version":"2012-10-17",
          "Statement":[{
          "Sid":"PublicReadGetObject",
                "Effect":"Allow",
                "Principal": "*",
                "Action":["s3:GetObject"],
                "Resource":["arn:aws:s3:::%s/*"
              ]
            }
          ]
        }
        """ % bucket.name
        policy = policy.strip()

        bucketpolicy = bucket.Policy()
        bucketpolicy.put(Policy=policy)

    def configurewebsite(self, bucket):
        """Set up the bucket to host static website."""
        bucket.Website().put(WebsiteConfiguration={
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'index.html'}})

    def upload_file(self, bucket, path, key):
        """Upload path to S3 bucket to key."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'
        return bucket.upload_file(path, key,
                                  ExtraArgs={'ContentType': content_type})

    def sync(self, pathname, bucket_name):
        """Sync files in given path to the S3 bucket."""
        bucket = self.s3.Bucket(bucket_name)
        root = Path(pathname).expanduser().resolve()

        def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_directory(p)
                if p.is_file():
                    self.upload_file(bucket, str(p),
                                     str(p.relative_to(root)))

        handle_directory(root)
