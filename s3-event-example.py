# coding: utf-8
events = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2019-08-17T07:01:48.819Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDAIE4BL77AEAQCSCARK'}, 'requestParameters': {'sourceIPAddress': '182.65.50.215'}, 'responseElements': {'x-amz-request-id': '74FD286D1BB7E1D5', 'x-amz-id-2': 'I+n65jbdgA3uAYYWBWaJ4NpInkh+MLDABwdNvFPHuuzJmAiZZc88pZM6yVxUMw22edPgzCf5fTc='}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'ea0760bf-534c-4332-a797-ac8b45d7df2a', 'bucket': {'name': 'samvideoanalyzer1', 'ownerIdentity': {'principalId': 'A2MVRG6R673R28'}, 'arn': 'arn:aws:s3:::samvideoanalyzer1'}, 'object': {'key': 'Memory+of+a+Woman.mp4', 'size': 3861431, 'eTag': '929374ffb3524bc2e4137b39f5645baf', 'sequencer': '005D57A659EA67372A'}}}]}
events
events['Records'][0]
events['Records'][0]['s3']['bucket']
events['Records'][0]['s3']['bucket']['name']
events['Records'][0]['s3']['object']['key']
import urllib
urllib.parse.unquote_plus(events['Records'][0]['s3']['object']['key'])
