"""Migrate data from the local sqlite db to DynamoDB."""
import boto3
import sqlite3
import time
from os import environ

# set the config variables
from env_tools import apply_env
apply_env()

# AWS Credentials
aws_account_id = environ.get('AWS_ACCOUNT_ID')
aws_access_key = environ.get('AWS_ACCESS_KEY')
aws_secret_access_key = environ.get('AWS_SECRET_ACCESS_KEY')
aws_user = environ.get('AWS_USER')
aws_region = environ.get('AWS_REGION')
aws_arn = environ.get('AWS_ARN')

# initialize the dynamodb connections
db = boto3.resource('dynamodb', region_name=aws_region, aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_access_key, endpoint_url='http://localhost:8008')

db_cloud = boto3.resource('dynamodb', region_name=aws_region, aws_access_key_id=aws_access_key,
                          aws_secret_access_key=aws_secret_access_key)

# initialize the sqlite db connection
conn_tbdb = sqlite3.connect('/Users/tberg/Documents/Dev/PyCharm/talkbeer/talkbeer.sqlite')
tbdb = conn_tbdb.cursor()

tbdb.execute('''SELECT name, number, url, html FROM thread_page 
                    WHERE (name = 'SSF16' AND number >= 27)
                ORDER BY name, number''')
data = tbdb.fetchall()
conn_tbdb.close()

i = 0
completed = 0
failed = 0
for d in data:
    item = {
        "thread_name":  d[0],
        "page":     int(d[1]),
        "url":  d[2] or "--",
        "html": d[3]
    }

    response = db_cloud.Table('biffers_thread_page_raw').put_item(Item=item)

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(f"Error with {item['thread_name'], item['page']}:")
        print(response, '\n')
        failed += 1
    else:
        print(f"Added {item['thread_name'], item['page']} successfully")
        completed += 1

    i += 1

print(f"Completed {completed}, Failed {failed}")
print(f"Total: {i}")
