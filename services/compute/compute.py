from celery import Celery

from lib import CacheControl

# First argument is the name of the current module
# redis://:password@hostname:port/db_number, all fields after the scheme are
# optional, and will default to localhost on port 6379, using database 0
app = Celery('compute', broker = 'amqp://', backend = 'redis://')

@app.task
@CacheControl(time = 60)
def add(x, y):
    return x + y

@app.task
def sub(x, y):
    return x - y

@app.task
def mul(x, y):
    return x * y

@app.task
def div(x, y):
    return x / float(y)
