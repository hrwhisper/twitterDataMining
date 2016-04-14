# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/4/14.
import re
from django.core.urlresolvers import reverse, NoReverseMatch
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''
