# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/rpc_code.py
from __future__ import absolute_import
from enum import IntEnum

class RPC_CODE(IntEnum):
    OK = (0, )
    UNKNOWN = (1, )
    TIMEOUT = (2, )
    CLOSE = (3, )
    CONNECT_FAIL = (4, )
    BAD_TOKEN = (10, )
    NOT_ENTITY = (11, )
    NOT_METHOD = (12, )
    NOT_INVOKE = (13, )
    NOT_RESPONSE = (14, )
    EXEC_ERROR = (15, )
    NOT_SERVICE = 100
    CAN_NOT_FIND_SERVICE_INFO = 102
    SERVICE_ALL_UNAVAILABLE = 103
    DB_COUNT_FAIL = 201
    DB_INSERT_FAIL = 202
    DB_REMOVE_FAIL = 203
    DB_UPDATE_FAIL = 204
    DB_FIND_FAIL = 205
    DB_SEQ_FAIL = 206