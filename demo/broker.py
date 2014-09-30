from __future__ import absolute_import

from celery import Celery
import logging
import time

logger = logging.getLogger(__name__)

class Broker(object):
    def __init__(self):
#        self.broker = Celery('demo',
#                            broker = 'amqp://mw01/',
#                            backend = 'redis://mw01/')
        self.broker = Celery('demo')
        self.broker.config_from_object('django.conf:settings')

    def execute(self, task_name, *args, **kwargs):
        logger.debug('Calling task ' + task_name + '...')
        result = self.broker.send_task(task_name, args = args, kwargs = {})
        counter = 0
        while counter < 3:
            if result.ready():
                logger.debug('Got result!')
                return {'result': result.result}
            else:
                logger.debug('Waiting for 3 seconds...')
                time.sleep(3)
                counter += 1
        if counter >= 3:
            return {'error': "I'm not that patient, haven't got the result"}

    def process_request(self, request):
        request.broker = Broker()
