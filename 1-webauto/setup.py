from setuptools import setup

setup(
    name='webauto-sam',
    version='1.0',
    author='Sam',
    author_email='sam.r.raman@gmail.com',
    description='Webauto is a tool to deploy a static website in AWS S3 bucket',
    license='GPLv3+',
    packages=['webauto'],
    url='https://github.com/samnovice/automate_aws_services',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        webauto=webauto.webauto.cli
    '''

)
