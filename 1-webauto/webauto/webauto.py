import boto3
import click
from botocore.exceptions import ClientError
from pathlib import Path
import mimetypes

session = boto3.Session(profile_name='samcoder')
s3 = session.resource('s3')

#@click.command('list-buckets')
@click.group()
def cli():
    "webauto deploys blogs to aws"
    pass

@cli.command('list_buckets')
def list_buckets():
    "List all s3 buckets in aws"
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('list_bucket_objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    "List all objects inside an S3 bucket"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)
    pass

@cli.command('configure_bucket')
@click.argument('bucket')
def configure_bucket(bucket):
    "Create and Configure S3 bucket for website"
    s3_bucket = None

    try:
        s3_bucket = s3.create_bucket(Bucket=bucket)

    except:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucket)
        else:
            raise e

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
    """% s3_bucket.name
    policy = policy.strip()

    bucketpolicy = s3_bucket.Policy()
    res = bucketpolicy.put(Policy=policy)

    ws = s3_bucket.Website()
    ws.put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
                             },
            'IndexDocument': {
                'Suffix': 'index.html'
                             }
                                }
           )
    return

def upload_file(s3_bucket, path, key):
    content_type = mimetypes.guess_type(key)[0] or 'text/plain'
    s3_bucket.upload_file(
                path,
                key,
                ExtraArgs={
                    'ContentType': content_type
                          })

@cli.command('sync_folder')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync_folder(pathname, bucket):
    "Sync contents from pathname or folder to S3 Bucket"
    s3_bucket = s3.Bucket(bucket)

    root = Path(pathname).expanduser().resolve()

    def handle_directory(target):
        for p in target.iterdir():
            if p.is_dir():
                handle_directory(p)
            if p.is_file():
                upload_file(s3_bucket, str(p), str(p.relative_to(root)))
                #print("Path: {}\n Key: {}".format(p, p.relative_to(root)))

    handle_directory(root)

if __name__ == '__main__':
    cli()
