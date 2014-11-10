from __future__ import absolute_import

import logging

logger = logging.getLogger(__name__)

def is_user_in_group(user, group_name):
    if user:
        return user.groups.filter(name = group_name).count() == 1
    return False
