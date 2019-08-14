# coding: utf-8
import boto3
session = boto3.Session(profile_name='samcoder')
s3 = session.resource('s3')
bucket = s3.create_bucket(Bucket='samvideoanalyzervideos')
from pathlib import Path
get_ipython().run_line_magic('ls', '-l /home/sampath/Downloads/*.mp4')
pathname = '~/Downloads/Couple Walking on a Beach Filmed with a Drone.mp4'
pathname
path = Path(pathname).expanduser().resolve()
print(path)
path.name
bucket.upload_file(str(path), str(path.name))
reko_client = session.client('rekognition')
response = reko_client.start_label_detection(Video={'S3Object': {'Bucket': bucket.name, 'Name': path.name}})
response
job_id = respoonse['JobId']
job_id = response['JobId']
result = reko_client.get_label_detection(JobId=job_id)
result
result.keys()
result['JobStatus']
result['Labels']
len(result['Labels'])
