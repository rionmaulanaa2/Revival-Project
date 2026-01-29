# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/SunshineRpc/Decorator.py
UNKNOWN = 0
CLIENT = 1
SERVER = 2
GAME_CLIENT = 4
GAME_SERVER = 8
SERVER_GAME_SERVER = SERVER | GAME_SERVER
REMOTE_NAMES = {UNKNOWN: 'Unknown',
   CLIENT: 'Game Client',
   SERVER: 'Sunshine',
   GAME_SERVER: 'Game Server',
   GAME_CLIENT: 'Game Client'
   }
RPC_SOLO = 0
RPC_MULTI = 16

def rpcmethod(rpcType=UNKNOWN | RPC_SOLO):

    def _rpcmethod(func):
        func.__rpc_flags__ = rpcType
        return func

    return _rpcmethod