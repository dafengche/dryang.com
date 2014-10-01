from celery import Celery
from time import sleep

from cache import CacheControl

# First argument is the name of the current module
# redis://:password@hostname:port/db_number, all fields after the scheme are
# optional, and will default to localhost on port 6379, using database 0
app = Celery('compute', broker = 'amqp://', backend = 'redis://')

@CacheControl(time = 600)
@app.task
def add(x, y):
    sleep(6)
    return x + y

@CacheControl(time = 600)
@app.task
def sub(x, y):
    sleep(6)
    return x - y

@CacheControl(time = 600)
@app.task
def mul(x, y):
    sleep(6)
    return x * y

@CacheControl(time = 600)
@app.task
def div(x, y):
    sleep(6)
    return x / float(y)
