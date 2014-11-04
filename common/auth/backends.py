from __future__ import absolute_import

import ldap
import logging

from django.conf import settings
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

class LDAPBackend(object):
    def authenticate(self, username = None, password = None, remote_user = None):
        if username is None and remote_user is None: return None

        conn = ldap.initialize(settings.LDAP_SERVER_URI)

        # remote_user has priority
        if remote_user is not None:
            username = remote_user
            logger.debug('User ' + username + ' has already been authenticated by the web server')
        else:
            try:
                logger.debug('Authenticating ' + username + ' against ' + settings.LDAP_SERVER_URI + '...')
                conn.simple_bind_s('cn=' + username + ',' + settings.LDAP_DIR_USER, password)
                logger.debug('LDAP authentication for ' + username + ' was successful')
            except ldap.LDAPError, e:
                logger.debug('LDAP authentication failed!')
                logger.debug(e)
                return None
            except Exception, e:
                logger.debug('LDAP authentication failed!')
                logger.debug(e)
                return None

        user = None
        try:
            user = User.objects.get(username = username)
            logger.debug('Found ' + username + " in Django's user database")
        except User.DoesNotExist:
            logger.debug(username + " not found in Django's user database")
            try:
                result = conn.search_s(settings.LDAP_DIR_USER, ldap.SCOPE_SUBTREE, 'cn=%s' % username, ['uid', 'givenName', 'sn', 'mail'])
                uid = result[0][-1].get('uid')
                first_name = result[0][-1].get('givenName')
                last_name = result[0][-1].get('sn')
                mail = result[0][-1].get('mail')
                logger.debug('%s: %s %s, %s ' % (uid, first_name, last_name, mail))
                user = User(username = username, password = '!', first_name = first_name, last_name = last_name, email = mail)
                user.is_active = True
                user.is_staff = False
                user.is_superuser = False
                user.save()
            except Exception, e:
                logger.debug('LDAP query failed!')
                logger.debug(e)
                return None
        return user

    def get_user(self, user_id):
        logger.debug('get_user(): ' + str(user_id))
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
            return None
