from __future__ import absolute_import

import logging

from services.celery import app
from services.servicelib.cache import CacheControl
from services.servicelib.db import query_db

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.task
def get_stations(params):
    logger.debug('get_stations() called')
    logger.debug(params)

    if 'dataset' not in params.keys() or not params['dataset']:
        return {'error': 'Dataset not provided'}
    if 'name' not in params.keys() or not params['name']:
        return {'error': 'Station name not provided'}

    dataset = params['dataset']
    if dataset not in ['emep']:
        return {'error': 'Unsupported dataset: ' + dataset}
    name = params['name']

    # Retrieve data from database
    query = None
    if dataset == 'emep':
        query = ('SELECT id, station_name, station_city, '
                'station_latitude_deg, station_longitude_deg '
                'FROM gac_emep_stations '
                "WHERE UPPER(station_name) LIKE UPPER('%(name)s%%') "
                "OR UPPER(station_city) LIKE UPPER('%(name)s%%')"
                % params)
    else:
        pass
    return query_db(query)
