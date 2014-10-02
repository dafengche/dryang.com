import hashlib
import json
import logging
import memcache

cache = None
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CacheControl(object):

    def __init__(self, time = 0, host = 'mw01', port = '11211'):
        '''
        time = 0 means forever
        '''
        global cache
        self.time = time
        self.host = '%s:%s' % (host, port)
        cache = memcache.Client([self.host])

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            global cache
            # Generate key - unique? package_name:class_name:function_name:args:kwargs
            m = hashlib.md5()
            margs = [x.__repr__() for x in args]
            mkwargs = [x.__repr__() for x in kwargs.values()]
            map(m.update, margs + mkwargs)
            m.update(f.__name__)
            m.update(f.__class__.__name__)
            k = m.hexdigest()
            name = f.__name__
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
