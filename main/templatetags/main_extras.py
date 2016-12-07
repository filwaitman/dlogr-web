# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import arrow

from django import template

register = template.Library()


@register.filter(name='arrow')
def arrow_filter(date):
    if not date:
        return
    return arrow.get(date)


@register.filter(name='utc_to_local')
def utc_to_local_filter(date, timezone):
    if not date or not timezone:
        return
    return arrow_filter(date).to(timezone)


@register.filter(name='date_formatted')
def date_formatted_filter(local_date):
    if not local_date:
        return ''
    return local_date.strftime('%Y-%d-%m %H:%M:%S %Z')


@register.filter(name='attr')
def attr_filter(whatever, attribute):
    if not whatever or not attribute:
        return
    return getattr(whatever, attribute)


@register.filter(name='humanize_date')
def humanize_date_filter(date):
    if not date:
        return ''
    return arrow_filter(date).humanize()
