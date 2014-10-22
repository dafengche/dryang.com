from __future__ import absolute_import

import logging

from django.conf import settings

logger = logging.getLogger(__name__)

class LDAPBackend(object):
    def authenticate(self, username = None, password = None):
        if username is None: return None
        logger.debug('authenticate: ' + username)
        # TODO: LDAP authN
        logger.debug(settings.LDAP_SERVER_URI)
        logger.debug(settings.LDAP_BASE_DN)
        return None

    def get_user(self, user_id):
        logger.debug('get_user: ' + user_id)
        return None
