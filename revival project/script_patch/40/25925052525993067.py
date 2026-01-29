# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/sync_key_mapping_utils.py
from __future__ import absolute_import
from . import sync_key_mapping_config as config
SAVE_MODE = 'map_cnt'
is_enable_saving_keys = False
if G_IS_SERVER:
    import msgpack
    from mobile.common.proto_python import common_pb2
    from mobile.distserver.game import GameServerRepo
    if GameServerRepo.game_server_type == common_pb2.ServerInfo.DIRECT_BATTLE:
        try:
            if config.data:
                msgpack.update_msgpack_key_mapping(config.data)
        except Exception as e:
            log_error('[sync_key_mapping_utils] server - update_msgpack_key_mapping failed. msg=%s, \ndata=%s', e, config.data)

        if GameServerRepo.is_inner_server():
            try:
                file_path = './'
                msgpack.set_enable_unused_mapping_collecting(SAVE_MODE)
                is_enable_saving_keys = True
            except Exception as e:
                log_error('[sync_key_mapping_utils] server - set_enable_unused_mapping_collecting failed. msg=%s, \ndata=%s', e, config.data)
                is_enable_saving_keys = False

else:
    import msgpack
    try:
        if config.data:
            msgpack.update_msgpack_key_mapping(config.data)
    except Exception as e:
        log_error('[sync_key_mapping_utils] client - update_msgpack_key_mapping faileg failed. msg=%s, \ndata=%s', e, config.data)

config.data = None

def do_saving_keys():
    if not is_enable_saving_keys or not G_IS_SERVER:
        return
    from mobile.distserver.game import GameServerRepo
    if not GameServerRepo.is_inner_server():
        return
    import logic.server_const as server_const
    save_path = '%s/data/key_mapping_raw/' % server_const.SERVER_PATH
    import msgpack
    try:
        if SAVE_MODE == 'map_cnt':
            msgpack.save_unused_map(save_path)
        elif SAVE_MODE == 'set':
            msgpack.save_unused_set(save_path)
        else:
            log_error('[sync_key_mapping_utils] server - do_saving_keys error. unkown_mode = %s', SAVE_MODE)
    except Exception as e:
        log_error('[sync_key_mapping_utils] server - update_msgpack_key_mapping failed. msg=%s.', e)