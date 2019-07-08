from global_logger import logger, local
from config import Config
from flask import Flask
import boto3

# Use the local dynamodb connection when running locally
if local:
    db = boto3.resource('dynamodb', region_name=Config.aws_region, aws_access_key_id=Config.aws_access_key,
                        aws_secret_access_key=Config.aws_secret_access_key, endpoint_url='http://localhost:8008')
    logger.info("Using local DynamoDB")
else:
    db = boto3.resource('dynamodb', region_name=Config.aws_region, aws_access_key_id=Config.aws_access_key,
                        aws_secret_access_key=Config.aws_secret_access_key)
    logger.info("Using cloud DynamoDB")

app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'Hello World!'


# if local:  # if __name__ == '__main__':
#     app.run(host='localhost', port=8800, debug=True)
#     logger.info("Running locally!")
