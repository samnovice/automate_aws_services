import json

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

def get_video_labels(job_id):
    reko_client = boto3.client('rekognition')
    response = reko_client.get_label_detection(JobId=job_id)

        # get label detection returns only 1000 labels at a single call
        # use next token to retrive next set of results

        # refer doc
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Client.get_label_detection

    next_token = response.get('NextToken', None)

    while next_token:
        next_page = rekognition_client.get_label_detection(
            JobId=job_id,
            NextToken=next_token
        )

        next_token = next_page.get('NextToken', None)

        # Use extend function instead of append function here
        response['Labels'].extend(next_page['Labels'])

    return response

def make_item(data):

    if isinstance(data, dict):
        return { k: make_item(v) for k, v in data.items() }

    if isinstance(data, list):
        return [ make_item(v) for v in data ]

    if isinstance(data, float):
        return str(data)

    return data

def put_labels_in_db(data, video_name, video_bucket):
    del data['ResponseMetadata']
    del data['JobStatus']

    data['videoName'] = video_name
    data['videoBucket'] = video_bucket

    dynamodb = boto3.resource('dynamodb')

    table_name = os.environ['DYNAMODB_TABLE_NAME']
    videos_table = dynamodb.Table(table_name)

    data = make_item(data)

    videos_table.put_item(Item=data)

    return

#Handler Functions

def start_processing_video(event, context):

    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        file_name = urllib.parse.unquote_plus(record['s3']['object']['key'])
        start_content_detection(bucket_name, file_name)
    return

def handle_label_detection(event, context):

    print(event)
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        job_id = message['JobId']
        s3_object = message['Video']['S3ObjectName']
        s3_bucket = message['Video']['S3Bucket']

        response = get_video_labels(job_id)
        print(response)
        put_labels_in_db(response, s3_object, s3_bucket)

    return
