from django import template
from django.contrib.auth.models import Group, Permission, User

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    register.filter('has_group', has_group)
    return user.groups.filter(name=group_name).exists()