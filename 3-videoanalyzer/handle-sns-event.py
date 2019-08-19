# coding: utf-8
event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:us-east-1:997257716700:handleLabelDetectionTopic:8c3072c3-b1ae-4de0-b6b6-f7de919ba42d', 'Sns': {'Type': 'Notification', 'MessageId': 'cb5a8f1f-d393-57bb-bf52-dace23c7c97b', 'TopicArn': 'arn:aws:sns:us-east-1:997257716700:handleLabelDetectionTopic', 'Subject': None, 'Message': '{"JobId":"8d14a293147b67b19ec00e05c8e1903db86d8533c2cd6228e4bbd3fae6392ac7","Status":"SUCCEEDED","API":"StartLabelDetection","Timestamp":1566043668809,"Video":{"S3ObjectName":"Memory of a Woman.mp4","S3Bucket":"samvideoanalyzer1"}}', 'Timestamp': '2019-08-17T12:07:48.892Z', 'SignatureVersion': '1', 'Signature': 'aZ31mwH4Brq7pPVdeWd+lDxGlJcriwYddBOV3H7NsdcTJXbbkwPb9qhB7R9kbaY6L45ikeocYHXZ5QBi5DZTFIansinIsOlGz4u2AYbJBPSNVf+g8dxc8zQWy4coaEe6K8yEdy36R4HhTromTYXCh0NOoL5okAHxq0Ck2EztfWmHo1Bnm3Bca+6egdJAJBir7d83/nc5UIDwU/IyCZYN0PEsTRzSDF99+QmRtZTN/oCoitOsBgHb6JnEjbl3/pr/zqotZBPjE3e5YtvhXiyNFbwDGgOEPuYZzM6sWZ7lkxGuYTxMGDN6pEFInvjN010N2TzZh3BLJ1uIdbdouQ2bpA==', 'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-6aad65c2f9911b05cd53efda11f913f9.pem', 'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:997257716700:handleLabelDetectionTopic:8c3072c3-b1ae-4de0-b6b6-f7de919ba42d', 'MessageAttributes': {}}}]}
event
event.keys()
event['Records'][0].keys()
event['Records'][0]['EventSource']
event['Records'][0]['EventVersion']
event['Records'][0]['EventSubscriptionArn']
event['Records'][0]['Sns']
event['Records'][0]['Sns'].keys()
event['Records'][0]['Sns']['Message']
import json
json.loads(event['Records'][0]['Sns']['Message'])
