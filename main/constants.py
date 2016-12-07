# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from datetime import datetime

from django.contrib.staticfiles.templatetags.staticfiles import static

import pytz


def _timezone_label(timezone):
    label = pytz.timezone(timezone).localize(datetime.now()).strftime('%z')
    return '({}:{}) {}'.format(label[:-2], label[-2:], timezone)


def _timezone_offset(timezone):
    return int(pytz.timezone(timezone).localize(datetime.now()).strftime('%z'))


TIMEZONE_CHOICES_FIRST = [
    # 'America/Sao_Paulo',
    # 'UTC',
]
TIMEZONE_CHOICES = [[x, _timezone_label(x), _timezone_offset(x)] for x in pytz.common_timezones]
TIMEZONE_CHOICES = sorted(TIMEZONE_CHOICES, key=lambda x: x[2])
for x in reversed(TIMEZONE_CHOICES_FIRST):
    TIMEZONE_CHOICES.insert(0, [x, _timezone_label(x), _timezone_offset(x)])
TIMEZONE_CHOICES = [[x[0], x[1]] for x in TIMEZONE_CHOICES]


REGULAR_HEROES = sorted([
    # {'name': 'Filipe Waitman'},
], key=lambda x: x['name'])

SUPER_HEROES = sorted([
    {
        'name': 'Filipe Waitman',
        'link': 'http://filwaitman.github.io',
        'image': static('images/superheroes/filipe_waitman.jpg'),
        'description': (
            'API creator/owner, and maintainer of this project. '
            'Built both the Web client and the Python client as well.'
        )
    },
    {
        'name': 'Tomas Correa',
        'link': 'http://github.com/tomascorrea',
        'image': static('images/superheroes/tomas_correa.png'),
        'description': 'The ideator of this project. Without his concept this would not exist, for sure.'
    },
    {
        'name': 'Carol Cavalcanti',
        'link': 'http://cavalcanticarol.com.br',
        'image': static('images/superheroes/carol_cavalcanti.jpg'),
        'description': 'Web client designer and developer. If you think this interface is nice, thanks to her. =]'
    },
], key=lambda x: x['name'])
