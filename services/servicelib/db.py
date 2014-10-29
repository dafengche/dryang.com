from __future__ import absolute_import

import logging
import psycopg2

from services.servicelib.cache import CacheControl

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

HOST = 'db01'
DB = 'verif'
USER = 'verif'
PASS = 'verif'

@CacheControl(time = 3600)
def query_db(query):
    logger.debug(query)
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect('host=%s dbname=%s user=%s password=%s' %
            (HOST, DB, USER, PASS))
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
