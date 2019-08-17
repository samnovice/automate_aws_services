import os

import urllib

import boto3

def start_content_detection(bucket, key):
    reko_client = boto3.client('rekognition')
    response = reko_client.start_label_detection(
                        Video={
                                'S3Object': {'Bucket': bucket, 'Name': key}
                              },
                        NotificationChannel={
                                'SNSTopicArn': os.environ['REKOGNITION_SNS_TOPIC_ARN'],
                                'RoleArn': os.environ['REKOGNITION_ROLE_ARN']
                              })

    print(response)
    return


def start_processing_video(event, context):

    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        file_name = urllib.parse.unquote_plus(record['s3']['object']['key'])
        start_content_detection(bucket_name, file_name)
    return

def handle_label_detection(event, context):

    print(event)

    return
