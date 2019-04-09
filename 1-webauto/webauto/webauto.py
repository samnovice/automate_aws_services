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
import click
# from botocore.exceptions import ClientError


from webauto.bucket import BucketManager
from webauto.domain import DomainManager
from webauto.certificate import CertificateManager
from webauto.cdn import DistributionManager


from webauto import util

# s3 = session.resource('s3')

session = None
bucket_manager = None
domain_manager = None
cert_manager = None
dist_manager = None


@click.group()
@click.option('--profile', default=None, help="Use an given AWS Profile")
def cli(profile):
    """Webauto deploys blogs to aws."""
    global session, bucket_manager, domain_manager, cert_manager, dist_manager
    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile
    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)
    domain_manager = DomainManager(session)
    cert_manager = CertificateManager(session)
    dist_manager = DistributionManager(session)


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
    print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))


@cli.command('setup_domain')
@click.argument('domain')
def setup_domain(domain):
    """Configure domain to point to S3 bucket."""
    bucket = bucket_manager.get_bucket(domain)
    zone = domain_manager.find_hostedzone(domain) \
        or domain_manager.create_hostedzone(domain)
    endpoint = util.get_endpoint(bucket_manager.get_region_name(bucket))
    a_record = domain_manager.create_s3_domain_record(zone, domain, endpoint)
    print("Domain configured: http://{}".format(domain))
    print(a_record)


@cli.command('find-cert')
@click.argument('domain')
def find_cert(domain):
    """Find SSL certificate for given domain."""
    print(cert_manager.find_matching_cert(domain))


@cli.command('setup-cdn')
@click.argument('domain')
@click.argument('bucket')
def setup_cdn(domain, bucket):
    """Set up an Cloud front CDN for domain."""
    dist = dist_manager.find_matching_dist(domain)

    if not dist:
        cert = cert_manager.find_matching_cert(domain)
        if not cert:
            print("No matching certificate")
            return

        dist = dist_manager.create_dist(domain, cert)
        print("Awaiting for distribution deployment")
        dist_manager.await_deploy(dist)

    zone = domain_manager.find_hostedzone(domain) \
        or domain_manager.create_hostedzone(domain)

    domain_manager.create_cf_domain_record(zone, domain, dist['DomainName'])

    print("Domain configured: https://{}".format(domain))

    return


if __name__ == '__main__':
    cli()
