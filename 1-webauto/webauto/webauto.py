# !/usr/bin/python
# -*- coding : utf-8 -*-
"""
Webauto: Deploy websites with aws.

Webauto automates the process of deploying static web sites to aws.
- Configure AWS S3 list_buckets
    - Create them
    - Set them up for static website hosting
    - Deploy local files to them
- Configure DNS using AWS Route 53.
- Configure Cloudfront CDN and SSL with aws.
"""
from pathlib import Path
import mimetypes
import boto3
from botocore.exceptions import ClientError
import click

session = boto3.Session(profile_name='samcoder')
s3 = session.resource('s3')

# @click.command('list-buckets')
@click.group()
def cli():
    """Webauto deploys blogs to aws."""



@cli.command('list_buckets')
def list_buckets():
    """List all s3 buckets in aws."""
    for bucket in s3.buckets.all():
        print(bucket)


@cli.command('list_bucket_objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List all objects inside an S3 bucket."""
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)


@cli.command('configure_bucket')
@click.argument('bucket')
def configure_bucket(bucket):
    """Create and Configure S3 bucket for website."""
    s3_bucket = None

    try:
        s3_bucket = s3.create_bucket(Bucket=bucket)
    except ClientError as error:
        if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucket)
        else:
            raise error

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
    """ % s3_bucket.name
    policy = policy.strip()

    bucketpolicy = s3_bucket.Policy()
    bucketpolicy.put(Policy=policy)

    s3_bucket.Website().put(WebsiteConfiguration={
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'}})
    return


def upload_file(s3_bucket, path, key):
    """Upload path to S3 bucket to key."""
    content_type = mimetypes.guess_type(key)[0] or 'text/plain'
    s3_bucket.upload_file(
                path,
                key,
                ExtraArgs={'ContentType': content_type})


@cli.command('sync_folder')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync_folder(pathname, bucket):
    """Sync contents from pathname or folder to S3 Bucket."""
    s3_bucket = s3.Bucket(bucket)

    root = Path(pathname).expanduser().resolve()

    def handle_directory(target):
        for p in target.iterdir():
            if p.is_dir():
                handle_directory(p)
            if p.is_file():
                upload_file(s3_bucket, str(p), str(p.relative_to(root)))
                # print("Path: {}\n Key: {}".format(p, p.relative_to(root)))

    handle_directory(root)


if __name__ == '__main__':
    cli()
