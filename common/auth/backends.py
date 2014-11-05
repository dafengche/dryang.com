from __future__ import absolute_import

import ldap
import logging

from django.conf import settings
from django.contrib.auth.models import User, Group

logger = logging.getLogger(__name__)

class LDAPBackend(object):
    def authenticate(self, username = None, password = None, remote_user = None):
        if username is None and remote_user is None: return None

        conn = ldap.initialize(settings.LDAP_SERVER_URI)
        try:
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

            user = None
            try:
                user = User.objects.get(username = username)
                logger.debug('Found ' + username + " in Django's user database")
                logger.debug('%s, %s %s, %s, %s' % (user.username, user.first_name, user.last_name, user.email, user.groups.all()))
            except User.DoesNotExist:
                logger.debug(username + " not found in Django's user database, trying LDAP...")
                try:
                    r = conn.search_s(settings.LDAP_DIR_USER,
                            ldap.SCOPE_SUBTREE,
                            filterstr = '(uid=%s)' % username,
                            attrlist = ['givenName', 'sn', 'mail', 'group'])
                    if not r:
                        logger.warn('User %s not found in LDAP' % username)
                        return None

                    r = [attrs for (dn, attrs) in r if dn is not None]
                    if len(r) > 1:
                        logger.warn('Multiple LDAP entries for %s: %s' % (username, r))
                    r = r[0]

                    # Each result tuple is of the form (dn, attrs), where dn is
                    # a string containing the DN of the entry, and attrs is a
                    # dictionary containing the attributes associated with the
                    # entry. The keys of attrs are strings, and the associated
                    # values are lists of string
                    first_name = r.get('givenName', [None])[0]
                    last_name = r.get('sn', [None])[0]
                    mail = r.get('mail', [None])[0]
                    groups = r.get('group', ['public'])
                    logger.debug('%s: %s %s, %s, %s' % (username, first_name, last_name, mail, groups))
                    user = User(username = username, first_name = first_name, last_name = last_name, email = mail)
                    user.set_unusable_password()
                    user.is_active = True
                    user.is_staff = False
                    user.is_superuser = False
                    if 'admin' in groups:
                        user.is_staff = True
                        user.is_superuser = True
                    user.save()

                    # Set groups
                    user.groups = [Group.objects.get_or_create(name = g)[0] for g in groups]
                    user.save()
#                    for g in groups:
#                        group = Group.objects.get_or_create(name = g)[0]
#                        group.user_set.add(user)
#                        group.save()
                    logger.debug('Group(s) has been set for %s' % username)
                except ldap.LDAPError, e:
                    logger.debug('LDAP query failed - %s' % e)
                    return None

            return user
        except Exception, e:
            logger.debug('Unexpected error - %s' % e)
            return None
        finally:
            conn.unbind()

    def get_user(self, user_id):
        logger.debug('get_user(): ' + str(user_id))
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
            return None
