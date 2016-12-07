# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import copy


LIST_NO_OBJECTS = {
    'count': 0,
    'next': None,
    'previous': None,
    'results': []
}

NO_CONTENT = {}

CUSTOMER_OBJECT = {
    'id': 'df19508a-9196-4cb5-97e7-0a6926b8ff3a',
    'created': '2016-11-14T21:56:44.226486Z',
    'modified': '2016-11-14T21:56:44.226526Z',
    'email': 'filwaitman@gmail.com',
    'name': 'Waitcorp',
    'timezone': 'UTC'
}

CUSTOMER_OBJECT_WITH_AUTH_KEY = copy.deepcopy(CUSTOMER_OBJECT)
CUSTOMER_OBJECT_WITH_AUTH_KEY['auth_token'] = '34a180bd1a1ccd3b90ab94f1633c64bdde21adb7'

EVENT_OBJECT1 = {
    'id': '1ee6e41e-5b87-4c72-9b1d-ff1266eee5ee',
    'created': '2016-11-02T00:57:47.654255Z',
    'modified': '2016-11-02T00:57:47.654293Z',
    'object_id': '85bfedcc-7d77-4838-a243-21f6f84959cb',
    'object_type': 'users.models.User',
    'human_identifier': 'Filipe Waitman',
    'timestamp': '2016-10-02T00:57:38.124166Z',
    'message': 'User logged in',
    'metadata': None
}

EVENT_OBJECT2 = {
    'id': '3c0160b8-3db0-44e0-809f-faaf871686ac',
    'created': '2016-11-02T00:57:47.654255Z',
    'modified': '2016-11-02T00:57:47.654293Z',
    'object_id': '85bfedcc-7d77-4838-a243-21f6f84959cb',
    'object_type': 'users.models.User',
    'human_identifier': 'Filipe Waitman',
    'timestamp': '2016-10-03T00:57:38.124166Z',
    'message': 'User logged out',
    'metadata': None
}

EVENT_OBJECT3 = {
    'id': '19611c9c-6071-4b29-8c56-dbd58bd9e2ad',
    'created': '2016-11-02T00:57:47.654255Z',
    'modified': '2016-11-02T00:57:47.654293Z',
    'object_id': '85bfedcc-7d77-4838-a243-21f6f84959cb',
    'object_type': 'users.models.User',
    'human_identifier': 'Filipe Waitman',
    'timestamp': '2016-10-04T00:57:38.124166Z',
    'message': 'User deleted account',
    'metadata': None
}

EVENT_LIST = {
    'count': 3,
    'next': None,
    'previous': None,
    'results': [
        EVENT_OBJECT3,
        EVENT_OBJECT2,
        EVENT_OBJECT1,
    ]
}
