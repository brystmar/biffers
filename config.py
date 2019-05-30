from os import path, environ
from global_logger import glogger, local
import logging

logger = glogger
logger.setLevel(logging.INFO)


class Config(object):
    """Set the config parameters for this app."""
    logger.info("Start of the Config() class.")

    if local:
        from env_tools import apply_env
        apply_env()
        logger.info("Applied .env variables using env_tools")
        logger.debug("Readme file exists? {}".format(path.isfile('README.md')))

        SECRET_KEY = environ.get('SECRET_KEY') or '1asdf'
        BUCKET_NAME = environ.get('GCP_BUCKET_NAME') or 'local_fail_bucket'
        db_user = environ.get('AWS_RDS_USER')
        db_pw = environ.get('AWS_RDS_PW')
        db_name = environ.get('AWS_RDS_DBNAME')
        db_ip = environ.get('AWS_RDS_IP')
        db_port = environ.get('AWS_RDS_PORT')
        db_instance = environ.get('AWS_RDS_REGION')
        db_url = environ.get('AWS_RDS_URL')

    else:
        from google.cloud import firestore
        # logging to stdout in the cloud is automatically routed to a useful monitoring tool
        logger.debug("JSON file exists? {}".format(path.isfile('trivialib-prod.json')))

        # supplying the private (prod) key to explicitly use creds for the default service acct
        fire = firestore.Client().from_service_account_json('trivialib-prod.json')

        # this call should work now
        fire_credentials = fire.collection('environment_vars').document('prod').get()
        # fire_credentials = fire_credentials._data
        logger.info("Fire_credentials GCP bucket: {}".format(fire_credentials._data['GCP_BUCKET_NAME']))

        SECRET_KEY = fire_credentials._data['SECRET_KEY'] or '2asdf'
        BUCKET_NAME = fire_credentials._data['GCP_BUCKET_NAME'] or 'fire_fail_bucket'
        db_user = fire_credentials._data['AWS_RDS_USER']
        db_pw = fire_credentials._data['AWS_RDS_PW']
        db_name = fire_credentials._data['AWS_RDS_DBNAME']
        db_ip = fire_credentials._data['AWS_RDS_IP']
        db_port = fire_credentials._data['AWS_RDS_PORT']
        db_instance = fire_credentials._data['AWS_RDS_REGION']
        db_url = fire_credentials._data['AWS_RDS_URL']

        logger.info("DB instance from fire_credentials: {}".format(db_instance))

    # set the database URI
    # db_url = 'postgres+psycopg2://{u}:{pw}'.format(u=db_user, pw=db_pw)
    # db_url += '@/{db}?host=/cloudsql/{i}'.format(db=db_name, i=db_instance)
    # db_url += '/.s.PGSQL.5432'

    SQLALCHEMY_DATABASE_URI = db_url

    logger.debug("SQLALCHEMY_DATABASE_URI: {}".format(db_url))

    # silence the madness
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    logger.info("End of the Config() class.")
