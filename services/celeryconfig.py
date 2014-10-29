BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'redis://'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
#
CELERY_INCLUDE = [
    'services.compute.compute',
    'services.plot.plot',
    'services.station.station',
]
'''
# Routing config
from kombu import Exchange, Queue
# Rename the default queue from 'celery' to 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key = 'default'),
    Queue('plot', Exchange('plot'), routing_key = 'plot'),
)
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_ROUTING_KEY = 'default'
# Route tasks to queues
CELERY_ROUTES = {
    'plot.plot.make_plot_mpl': {
        'queue': 'plot',
        'routing_key': 'plot'
    },
}
'''
