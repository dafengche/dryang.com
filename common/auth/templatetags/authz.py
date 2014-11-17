from django import template

from common.auth import utils

register = template.Library()

@register.filter
def is_user_in_group(user, group_name):
    return utils.is_user_in_group(user, group_name)
