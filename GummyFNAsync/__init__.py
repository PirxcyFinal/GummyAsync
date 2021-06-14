"""
“Commons Clause” License Condition v1.0
Copyright Oli 2020

The Software is provided to you by the Licensor under the
License, as defined below, subject to the following condition.
Without limiting other conditions in the License, the grant
of rights under the License will not include, and the License
does not grant to you, the right to Sell the Software.
For purposes of the foregoing, “Sell” means practicing any or
all of the rights granted to you under the License to provide
to third parties, for a fee or other consideration (including
without limitation fees for hosting or consulting/ support
services related to the Software), a product or service whose
value derives, entirely or substantially, from the functionality
of the Software. Any license notice or attribution required by
the License must also include this Commons Clause License
Condition notice.

Software: BenBotAsync
License: Apache 2.0
"""

"""
Credit Oli, Terbau and Pirxcy
"""

from typing import Tuple, Union, Any
from enum import Enum

import aiohttp
import base64
import codecs
import traceback
import functools
import asyncio
import json

__name__ = 'GummyFNAsync'
__version__ = '0.0.1'
__author__ = 'Pirxcy'

GUMMYFN_BASE = 'https://api.gummyfn.com'

#Overall Credits To Oli For Original Code For BenbotAsync
#Original Link: https://github.com/xMistt/BenBotAsync


class GummyFNAsyncException(Exception):
    pass


class InvalidParameters(GummyFNAsyncException):
    pass


class NotFound(GummyFNAsyncException):
    pass

class cosmetic_result:
    def __init__(self, data: dict) -> None:
        self.data = data
        self.id = data['info']['id']
        self.images = data['images']
        self.name = data['info']['name']
        self.description = data['info']['description']

class cc_result:
    def __init__(self, data: dict) -> None:
        self.data = data
        self.code = data['code']['code']
        self.account = data['account']
        self.account.name = data['account']['name']
        self.account.id = data['account']['id']
        self.name = data['code']['code']
        self.status = data['info']['status']
        self.info = data['info']
            
class stat_result:
    def __init__(self, data: dict) -> None:
        self.data = data
        self.id = data['account']['id']
        self.images = data['image']
        self.name = data['account']['name']
        self.overallstats = data['overallstats']
        
            
            
async def get_cosmetic(**params: Any):
    async with aiohttp.ClientSession() as session:
        async with session.request(method='GET', url=f'{GUMMYFN_BASE}/cosmetic', params=params) as r:
            data = await r.json()

            if 'missing name and id parameter' in str(data):
                raise InvalidParameters('Please Use Valid Parameters')

            if 'Could not find any cosmetic matching parameters' in str(data):
                raise NotFound('Could not find any cosmetic matching parameters.')

            return cosmetic_result(data)

async def get_creator_code(**params: Any):
    async with aiohttp.ClientSession() as session:
        async with session.request(method='GET', url=f'{GUMMYFN_BASE}/creatorcode', params=params) as r:
            data = await r.json()

            if 'parameter' in str(data):
                raise InvalidParameters('Please Use Valid Parameters')

            if 'unable to find' in str(data):
                raise NotFound('Could not find any cosmetic matching parameters.')

            return cc_result(data)         
        
async def get_stats(**params: Any):
    async with aiohttp.ClientSession() as session:
        async with session.request(method='GET', url=f'{GUMMYFN_BASE}/stats', params=params) as r:
            data = await r.json()

            if 'parameter' in str(data):
                raise InvalidParameters('Please Use Valid Parameters')

            if 'the requested account does not exist' in str(data):
                raise NotFound('The Requested Account Does not Exist')

            return cc_result(data)        
