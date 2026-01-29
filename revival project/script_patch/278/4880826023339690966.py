# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileHttpClientWorker.py
from ..Utils.NileHttpClient import NileHttpClient

class NileHttpClientWorker(object):
    MAX_CONCURRENT = 4
    __instance = None

    def __init__(self):
        pass

    @staticmethod
    def GetInstance():
        if not NileHttpClientWorker.__instance:
            NileHttpClientWorker.__instance = NileHttpClient(NileHttpClientWorker.MAX_CONCURRENT)
        return NileHttpClientWorker.__instance