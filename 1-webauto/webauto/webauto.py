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

import boto3
#from botocore.exceptions import ClientError
import click

from bucket import BucketManager

session = boto3.Session(profile_name='samcoder')
bucket_manager = BucketManager(session)
# s3 = session.resource('s3')

# @click.command('list-buckets')
@click.group()
def cli():
    """Webauto deploys blogs to aws."""


@cli.command('list_buckets')
def list_buckets():
    """List all s3 buckets in aws."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list_bucket_objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List all objects inside an S3 bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('configure_bucket')
@click.argument('bucket')
def configure_bucket(bucket):
    """Create and Configure S3 bucket for website."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.setpolicy(s3_bucket)
    bucket_manager.configurewebsite(s3_bucket)


@cli.command('sync_folder')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync_folder(pathname, bucket):
    """Sync contents from pathname or folder to S3 Bucket."""
    bucket_manager.sync(pathname, bucket)


if __name__ == '__main__':
    cli()
