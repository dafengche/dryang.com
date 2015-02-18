from __future__ import absolute_import

import logging

from services import celery_worker_config as cfg
from services.celery import app
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
    dataset = params['dataset']
    if dataset not in ['emep', 'gaw']:
        return {'error': 'Unsupported dataset: ' + dataset}

    if dataset == 'emep' and ('name' not in params.keys() or not params['name']):
        return {'error': 'Station name required for dataset ' + dataset}

    # Retrieve data from database
    query = None
    if dataset == 'emep': # dataset and name are available
        query = ('SELECT id, station_name, '
                'station_latitude_deg, station_longitude_deg '
                'FROM gac_%(dataset)s_stations '
                "WHERE UPPER(station_name) LIKE UPPER('%(name)s%%') "
                "OR UPPER(station_city) LIKE UPPER('%(name)s%%')"
                % params)
    else: # gaw: dataset available, name may not be available
        if 'name' not in params.keys() or not params['name']:
            query = ('SELECT id, name, lat, lon '
                'FROM gac_%(dataset)s_stations'
                % params)
        else:
            query = ('SELECT id, name, lat, lon '
                'FROM gac_%(dataset)s_stations '
                "WHERE UPPER(name) LIKE UPPER('%(name)s%%')"
                % params)
    return query_db(query, host = cfg.station['db_host'],
                port = cfg.station['db_port'],
                dbname = cfg.station['db_name'],
                user = cfg.station['db_user'],
                password = cfg.station['db_pass'])
