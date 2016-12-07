# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from dlogr.clients import DlogrClient

from django.conf import settings

from main.constants import TIMEZONE_CHOICES, REGULAR_HEROES, SUPER_HEROES


def get_dlogr_client(*args, **kwargs):
    ''' Centralized for testing/mocking purposes. '''
    return DlogrClient(settings.DLOGR_BASE_API_URL, *args, **kwargs)


def context_processor(request):
    return {
        'timezone_choices': TIMEZONE_CHOICES,
        'regular_heroes': REGULAR_HEROES,
        'super_heroes': SUPER_HEROES,
        'github': {
            'dlogr_python': {
                'main': 'http://www.github.com/filwaitman/dlogr-python',
            },
            'dlogr_web': {
                'main': 'http://www.github.com/filwaitman/dlogr-web',
            },
            'dlogr_api': {
                'main': 'http://www.github.com/filwaitman/dlogr-api',
            },
        }
    }
