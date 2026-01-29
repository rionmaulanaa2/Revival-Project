# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/simplerpc/simplerpc_common.py
from __future__ import absolute_import
from ..mobilelog.LogManager import LogManager
from . import check_in_service_env
if check_in_service_env():
    from ..IO import Timer
else:
    try:
        from ..common import Timer
    except:
        from ..IO import Timer

MAIN_RPC_PROCESSOR = None
SERVICE_CENTER_STUB = None
RPC_REQUEST = 1
RPC_RESPONSE = 2
RPC_SYNC = 3
RPC_SYNC_MISTY = 4
RPC_HEARTBEAT = -1
RPC_PROCESSOR_CONNECTION_CLEAR_INTERVAL = 300
HEART_INTERVAL = 20
HEART_TIMEOUT = 40
TCP = 1
ENET = 2
KCP = 3
CON_TYPE = {'TCP': TCP,
   'ENET': ENET,
   'KCP': KCP
   }
SERVICE_CENTER_ID = '_sc'
SERVICE_CENTER_STUB_ID = '_scs'

def addTimer(delay, func, *args, **kwargs):
    return Timer.addTimer(delay, func, *args, **kwargs)


def addRepeatTimer(delay, func, *args, **kwargs):
    return Timer.addRepeatTimer(delay, func, *args, **kwargs)


from . import SimpleServiceManager

def register_service(service_obj, to_global=False):
    SimpleServiceManager.SimpleServiceManager.add_service(service_obj.id, service_obj)
    if to_global:
        SERVICE_CENTER_STUB.register_service_to_center(service_obj.id, tag_name=service_obj.tag_name)


def unregister_service(service_obj, to_global=False):
    SimpleServiceManager.SimpleServiceManager.remove_service(service_obj.id)
    if to_global:
        SERVICE_CENTER_STUB.un_register_service_to_center(service_obj.id)


def get_service_info_byid(service_id):
    return SERVICE_CENTER_STUB.get_service_by_id(service_id)


def request_rpc(*args, **kwargs):
    return MAIN_RPC_PROCESSOR.request_rpc(*args, **kwargs)