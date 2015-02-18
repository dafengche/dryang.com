from __future__ import absolute_import

import logging

from time import sleep

from services.celery import app
from services import celery_worker_config as cfg
from services.servicelib.cache import CacheControl

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.task
def add(x, y):
    logger.debug('add() called')
    return compute(x, y, 'add')

@app.task
def sub(x, y):
    logger.debug('sub() called')
    return compute(x, y, 'sub')

@app.task
def mul(x, y):
    logger.debug('mul() called')
    return compute(x, y, 'mul')

@app.task
def div(x, y):
    logger.debug('div() called')
    return compute(x, y, 'div')

@CacheControl(host = cfg.cache['host'], port = cfg.cache['port'], time = cfg.cache['time'])
def compute(x, y, o):
    logger.debug('compute() called')
    logger.debug('Cache: %s:%s, valid for %ds' % (cfg.cache['host'], cfg.cache['port'], cfg.cache['time']))
    r = None
    if 'add' == o: r = x + y
    elif 'sub' == o: r = x - y
    elif 'mul' == o: r = x * y
    elif 'div' == o: r = x / float(y)
    sleep(4)
    return r
