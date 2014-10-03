from __future__ import absolute_import

import sys
print(sys.path)
#sys.path.append('/home/celery/git/dev/dryang.com/services')
#print(sys.path)

import celery
print(celery.__file__)

from celery import Celery

#app = Celery('ss',
#             broker='amqp://',
#             backend='redis://',
#             include=['services.compute.compute', 'services.plot.plot'])
app = Celery('services')
# Load config file, it should be in your Python path or in the directory you
# start Celery the worker server
app.config_from_object('celeryconfig')

# Optional configuration, see the application user guide
#app.conf.update(
#    CELERY_TASK_RESULT_EXPIRES=3600,
#)

if __name__ == '__main__':
    app.start()
