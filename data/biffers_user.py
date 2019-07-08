"""For each user record, add info about the BIFs they've participated in.

NOTE:
This script doesn't create the proper records when someone sends to (or receives from) a team.  I updated the
necessary records manually in the biffers.json file after running this script.
"""

import boto3
import sqlite3
import time
from os import environ

# set the config variables
from boto3.dynamodb.conditions import Key
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

# define tables
#table = db.Table('biffers_user')
table = db_cloud.Table('biffers_user')

# read all users into memory
db_data = table.scan()['Items']
# db_data = table.query(KeyConditionExpression=Key('user_id').eq(456))

# load the biffers table into memory
tbdb.execute('''SELECT DISTINCT b.thread_name, b.username, b.user_id, b.haul_id, b.target, b.target_id,
                    b.sender, b.sender_id, b.partner, b.partner_id, b2.haul_id as 'box_sent', b.list_order,
                    b.my_sender, t.id
                FROM biffer b
                join biffer b2 on b.thread_name = b2.thread_name
                    AND (b.user_id = b2.sender_id OR b.partner_id = b2.sender_id)
                join thread t on b.thread_name = t.name AND b2.thread_name = t.name
                ORDER BY b.thread_name DESC, b.list_order''')
biffers_data = tbdb.fetchall()

i = 0
completed = 0
failed = 0
skipped = 0

for d in db_data:
    for bd in biffers_data:
        # verify we are looking at the same record
        if d['user_id'] == int(bd[2]):
            item = {
                "thread_name": bd[0],
                "thread_id":   int(bd[13]),
                "username":    bd[1],
                "user_id":     bd[2],
                "hauls":       [bd[3]],
                "boxes_sent":  [bd[10]],
                "list_order":  bd[11],
                "targets":     [
                    {
                        "target_username": bd[4],
                        "target_id":   bd[5]
                    }
                ],
                "senders":     [
                    {
                        "sender_username": bd[6],
                        "sender_id":   bd[7]
                    }
                ]
            }

            if bd[9]:
                # they had partner(s) that round
                item["partners"] = [
                    {
                        "partner_username": bd[8],
                        "partner_id":  bd[9]
                    }
                ]

            if bd[12]:
                # ruled out my sender
                item["my_sender"] = int(bd[12])

            d['bifs'].append(item)

            response = table.update_item(Key={"user_id": bd[2]},
                                         UpdateExpression="SET bifs = :newbif",
                                         ExpressionAttributeValues={":newbif": d['bifs']})

            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                print(f"Error with {d['user_id'], d['username']}:")
                print(response, '\n')
                failed += 1
            else:
                print(f"{i}.  Added {d['user_id'], d['username']} successfully")
                completed += 1

            i += 1

print(f"Completed {completed}, Failed {failed}, Skipped {skipped}")
print(f"Total: {i}")
conn_tbdb.close()
