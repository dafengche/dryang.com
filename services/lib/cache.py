import hashlib
import json
import logging
import memcache

cache = None
logger = logging.getLogger(__name__)

class CacheControl(object):

    def __init__(self, time = 0, host = 'mw01', port = '11211'):
        '''
        time = 0 means forever
        '''
        self.time = time
        self.host = '%s:%s' % (host, port)
        cache = memcache.Client([self.host])

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            name = f.func_name
            req = (name, args, kwargs.items())
            req_enc = json.dumps(req, sort_keys = True)
            k = hashlib.md5(req_enc).hexdigest()
            logger.debug('Cache control (%s) for %s ', k, name)
            v = cache.get(k)
            if v:
                logger.debug('Cache control (%s) hit for %s', k, name)
            else:
                logger.debug('Cache control (%s) calling function for %s', k, name)
                v = f(*args, **kwargs)
                cache.set(k, v, self.time)
            return v
        return wrapped_f
