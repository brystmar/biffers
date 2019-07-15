from global_logger import logger, local
from os import path, environ
import pytz


class Config(object):
    """Define the config parameters for this app."""
    logger.info("Start of the Config() class.")

    if local:
        from env_tools import apply_env
        apply_env()
        logger.info("Applied .env variables using env_tools")

        # AWS Credentials
        aws_account_id = environ.get('AWS_ACCOUNT_ID')
        aws_access_key = environ.get('AWS_ACCESS_KEY')
        aws_secret_access_key = environ.get('AWS_SECRET_ACCESS_KEY')
        aws_region = environ.get('AWS_REGION')

        # TalkBeer
        tb_username = environ.get('TB_USER')
        tb_password = environ.get('TB_PW')

        # App-related
        SECRET_KEY = environ.get('SECRET_KEY') or '1ASDFKwekeapoij4o844ORKW#k2-093iedd'

    else:
        from google.cloud import firestore
        # logging to stdout in the cloud is automatically routed to a useful monitoring tool
        logger.debug(f"JSON file exists? {path.isfile('biffers-prod.json')}")

        # supply the private key to explicitly use creds for the default service acct
        fire = firestore.Client().from_service_account_json('biffers-prod.json')
        fire_credentials = fire.collection('environment_vars').document('prod').get()

        # AWS Credentials
        aws_account_id = fire_credentials._data['AWS_ACCOUNT_ID']
        aws_access_key = fire_credentials._data['AWS_ACCESS_KEY']
        aws_secret_access_key = fire_credentials._data['AWS_SECRET_ACCESS_KEY']
        aws_region = fire_credentials._data['AWS_REGION']

        # TalkBeer
        tb_username = fire_credentials._data['TB_USER']
        tb_password = fire_credentials._data['TB_PW']

        # App-related
        SECRET_KEY = fire_credentials._data['SECRET_KEY'] or '2ASDFKwekeapoij4o844ORKW#k2-093iedd'

    tb_url_post = 'https://www.talkbeer.com/community/goto/post?id='
    tb_url_likes = 'https://www.talkbeer.com/community/posts/post_id/likes'
    tb_url_login = 'https://www.talkbeer.com/community/login/login'
    tb_url_user_page = 'https://www.talkbeer.com/community/members/'

    logger.info("End of the Config() class.")


# TODO: Add support for moment.js
PST = pytz.timezone('US/Pacific')
