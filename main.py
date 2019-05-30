from global_logger import glogger, local
import logging
from flask import Flask
app = Flask(__name__)

logger = glogger
logger.setLevel(logging.INFO)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
