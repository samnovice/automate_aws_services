import boto3
import click

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

if __name__ == '__main__':
    cli()
