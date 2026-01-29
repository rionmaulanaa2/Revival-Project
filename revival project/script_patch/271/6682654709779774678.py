# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/weapon_trans_type_config.py
_reload_all = True
data = {800102: {'iItemID': 800102,
            'cCondEvent': 'G_COND_RAGE_KEY',
            'mpMapping': {'default': 800102,'low': 800102,'full': 800103}}
   }
import six_ex
KEY_COND_FROM_ARGS = 'ARGS'

def get_trans_type_event_mapping(item_id):
    if item_id not in data:
        return (None, None)
    else:
        info = data[item_id]
        return (
         info['cCondEvent'], info['mpMapping'])


def get_trans_type_by_cond_key(item_id, cond_key):
    if item_id not in data or not cond_key:
        return item_id
    info = data[item_id]
    if info['cCondEvent'] is not KEY_COND_FROM_ARGS:
        return item_id
    return info['mpMapping'].get(cond_key, info['mpMapping']['default'])


def get_weapon_before_trans(item_id):
    if not item_id:
        return
    else:
        if item_id in data:
            return item_id
        item_id_str = str(item_id)
        if len(item_id_str) < 4:
            return
        shorter_item_id = int(item_id_str[:4])
        trans_item = data.get(shorter_item_id, None)
        if not trans_item:
            return
        for k, v in six_ex.items(trans_item['mpMapping']):
            if v == item_id:
                return shorter_item_id

        return