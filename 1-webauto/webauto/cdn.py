"""Class for cloud front distribution."""

import uuid


class DistributionManager:
    """Manage an cloud front distribution for given domain."""

    def __init__(self, session):
        """Create DistributionManager object."""
        self.session = session
        self.client = self.session.client('cloudfront')

    def find_matching_dist(self, domain_name):
        """Find an matching distribution for given domain_name."""
        paginator = self.client.get_paginator('list_distributions')
        for page in paginator.paginate():
            for dist in page['DistributionList'].get('Items', []):
                for alias in dist['Aliases']['Items']:
                    if alias == domain_name:
                        return dist
        return None

    def create_dist(self, domain_name, cert):
        """Create a distribution for given domain using certificate."""
        orgin_id = 'S3-' + domain_name

        result = self.client.create_distribution(
            DistributionConfig={
                'CallerReference': str(uuid.uuid4()),
                'Aliases': {
                    'Quantity': 1,
                    'Items': [domain_name]
                },
                'DefaultRootObject': 'index.html',
                'Comment': 'Created by Webauto',
                'Enabled': True,
                'Origins': {
                    'Quantity': 1,
                    'Items': [{
                        'Id': orgin_id,
                        'DomainName':
                        '{}.s3.amazonaws.com'.format(domain_name),
                        'S3OriginConfig': {
                            'OriginAccessIdentity': ''
                        }
                    }]
                },
                'DefaultCacheBehavior': {
                    'TargetOriginId': orgin_id,
                    'ViewerProtocolPolicy': 'redirect-to-https',
                    'TrustedSigners': {
                        'Enabled': False,
                        'Quantity': 0,
                },
                'ForwardedValues': {
                    'Cookies': {'Forward': 'all'},
                    'Headers': {'Quantity': 0},
                    'QueryString': False,
                    'QueryStringCacheKeys': {'Quantity': 0}
                },
                'DefaultTTL': 86400,
                'MinTTL': 3600
            },
            'ViewerCertificate': {
                'ACMCertificateArn': cert['CertificateArn'],
                'SSLSupportMethod': 'sni-only',
                'MinimumProtocolVersion': 'TLSv1.1_2016'
            }
        }
        )
        return result['Distribution']

    def await_deploy(self, dist):
        """Await for CDN deployment to complete after creation before use."""
        waiter = self.client.get_waiter('distribution_deployed')
        waiter.wait(Id=dist['Id'], WaiterConfig={
                        'Delay': 30,
                        'MaxAttempts': 50
                    })
