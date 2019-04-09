# -*- coding : utf-8 -*-
"""
Class BucketManager to manage S3 functions.

    - Create a Bucket
    - List all Buckets
    - Configure Bucket for it to be used as website
    - Sync folder from given path to an bucket
"""

from pathlib import Path
from hashlib import md5
import mimetypes
from functools import reduce
import boto3
from botocore.exceptions import ClientError

from webauto import util



class BucketManager:
    """Manage an S3 bucket."""

    CHUNK_SIZE = 8388608

    def __init__(self, session):
        """Create and BucketManager object."""
        self.s3 = session.resource('s3')
        self.transfer_config = boto3.s3.transfer.TransferConfig(
            multipart_chunksize = self.CHUNK_SIZE,
            multipart_threshold = self.CHUNK_SIZE
        )
        self.manifest = {}

    def get_region_name(self, bucket):
        """Get the buckets region name."""
        bucket_location = self.s3.meta.client.get_bucket_location(
            Bucket=bucket.name)
        return bucket_location["LocationConstraint"] or 'us-east-1'

    def get_bucket(self, bucket_name):
        """Get bucket given the bucket name."""
        return self.s3.Bucket(bucket_name)

    def get_bucket_url(self, bucket):
        """Get the website url for this bucket."""
        return "http://{}.{}".format(
            bucket.name,
            util.get_endpoint(self.get_region_name(bucket)).host)

    def all_buckets(self):
        """Get list of all S3 buckets."""
        return self.s3.buckets.all()

    def all_objects(self, bucket_name):
        """Get all objects inside an bucket."""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        """Create an bucket or if it already exists.

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

    def load_manifest(self, bucket):
        """Load manifest for caching purpose."""
        # print("Loading manifest")
        paginator = self.s3.meta.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket.name):
            for obj in page.get('Contents', []):
                self.manifest[obj['Key']] = obj['ETag']
                # print("{} file and {}".format(obj['Key'], obj['ETag']))

    @staticmethod
    def hash_data(data):
        """Generate md5 hash for data."""
        hash = md5()
        hash.update(data)

        return hash

    def generate_etag(self, path):
        """Generate etag for given file."""
        hashes = []

        with open(path, 'rb') as f:
            while True:
                data = f.read(self.CHUNK_SIZE)

                if not data:
                    break

                hashes.append(self.hash_data(data))
        if not hashes:
            return
        elif len(hashes) == 1:
            return '"{}"'.format(hashes[0].hexdigest())
        else:
            hash = self.hash_data(reduce(lambda x, y: x + y, (h.digest() for h in hashes)))
            return '"{}-{}"'.format(hash.hexdigest(), len(hashes))

    def configurewebsite(self, bucket):
        """Set up the bucket to host static website."""
        bucket.Website().put(WebsiteConfiguration={
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'index.html'}})

    def upload_file(self, bucket, path, key):
        """Upload path to S3 bucket to key."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'

        etag = self.generate_etag(path)
        # print("Generated ETAG {} for file {} ".format(etag, key))
        if self.manifest.get(key, '') == etag:
            # print("Skipping {} etags match".format(key))
            return

        return bucket.upload_file(path, key,
                                  ExtraArgs={'ContentType': content_type},
                                  Config=self.transfer_config)

    def sync(self, pathname, bucket_name):
        """Sync files in given path to the S3 bucket."""
        bucket = self.s3.Bucket(bucket_name)
        self.load_manifest(bucket)
        root = Path(pathname).expanduser().resolve()

        def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_directory(p)
                if p.is_file():
                    self.upload_file(bucket, str(p),
                                     str(p.relative_to(root)))

        handle_directory(root)
