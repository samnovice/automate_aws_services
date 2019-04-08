# -*- coding : utf-8 -*-
"""Class for ACM Az Certificate Manager."""


class CertificateManager:
    """Manager Certificates in Az for website registered."""

    def __init__(self, session):
        """Create CertificateManager object."""
        self.session = session
        self.client = self.session.client('acm')

    def cert_matches(self, cert_arn, domain_name):
        """Check if the given certificate mathces for given domain."""
        cert_details = self.client.describe_certificate(CertificateArn=cert_arn)
        alt_names = cert_details['Certificate']['SubjectAlternativeNames']
        for name in alt_names:
            if name == domain_name:
                return True
            if name[0] == '*' and domain_name.endswith(name[1:]):
                return True

        return False

    def find_matching_cert(self, domain_name):
        """Find a certificate for given domain or sub domain."""
        paginator = self.client.get_paginator('list_certificates')
        for page in paginator.paginate(CertificateStatuses=['ISSUED']):
            for cert in page['CertificateSummaryList']:
                if self.cert_matches(cert['CertificateArn'], domain_name):
                    return cert

        return None
