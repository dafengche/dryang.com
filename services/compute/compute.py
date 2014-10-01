from celery import Celery
from celery.utils.log import get_task_logger
from time import sleep

from cache import CacheControl

logger = get_task_logger(__name__)

# First argument is the name of the current module
# redis://:password@hostname:port/db_number, all fields after the scheme are
# optional, and will default to localhost on port 6379, using database 0
app = Celery('compute', broker = 'amqp://', backend = 'redis://')

@CacheControl(time = 600)
@app.task
def add(x, y):
    logger.debug('add() called')
    sleep(6)
    return x + y

@CacheControl(time = 600)
@app.task
def sub(x, y):
    logger.debug('sub() called')
    sleep(6)
    return x - y

@CacheControl(time = 600)
@app.task
def mul(x, y):
    logger.debug('mul() called')
    sleep(6)
    return x * y

@CacheControl(time = 600)
@app.task
def div(x, y):
    logger.debug('div() called')
    sleep(6)
    return x / float(y)
