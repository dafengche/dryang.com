from __future__ import absolute_import

import logging
import psycopg2

import services.celery_worker_config as cfg
from services.servicelib.cache import CacheControl

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@CacheControl(host = cfg.cache['host'], port = cfg.cache['port'], time = cfg.cache['time'])
def query_db(query, *args, **kwargs):
    logger.debug(query)
    logger.debug(str(args))
    logger.debug(str(kwargs))
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect('host=%s port=%s dbname=%s user=%s password=%s' %
            (kwargs['host'], kwargs['port'], kwargs['dbname'], kwargs['user'], kwargs['password']))
        cursor = conn.cursor()
        cursor.execute(query)
        result = {'number_of_results': cursor.rowcount, 'data': cursor.fetchall()}
        logger.debug(result)
        return result
    except psycopg2.DatabaseError, e:
        logger.warning('Database query failed - ' + query)
        logger.warning(str(e))
        return {'error': 'Database query failed'}
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
