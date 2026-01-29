# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/capsule_proto.py
from __future__ import absolute_import
import six_ex

def on_coin_change(synchronizer, coin_cnt, reason):
    synchronizer.send_event('E_AGENT_COIN_CHANGED', coin_cnt, reason)


def on_scenebox_st_change(synchronizer, status):
    synchronizer.send_event('E_SCENE_BOX_STAT_CHANGE', status)


def set_capsule_list(synchronizer, cap_list):
    synchronizer.send_event('E_CAPSULE_PREVIEW', cap_list)


def on_capsule_change(synchronizer, capsule_id):
    synchronizer.send_event('E_GET_CAPSULE', capsule_id)


def capsule_show_msg(synchronizer, capsule_id, text):
    global_data.emgr.capsule_show_msg.emit(capsule_id, unpack_text(text))


def capsule_show_item_msg(synchronizer, items):
    from logic.gutils import item_utils
    item_list, text = [], []
    for item_id, count in six_ex.items(items):
        text.append(item_utils.get_item_name(item_id) + '*{0}'.format(count))
        item_list.append(item_id)


def show_effect(synchronizer, e_type, e_id):
    synchronizer.send_event('E_SHOW_EFFECT', e_type, e_id)


def set_attr(synchronizer, attr_name, attr, source_info=None):
    synchronizer.send_event('S_ATTR_SET', attr_name, attr, source_info)


def clear_attr(synchronizer):
    synchronizer.send_event('E_CLEAR_ATTR')


def mod_add_attr(synchronizer, attr_name, mod, item_id, source_info):
    synchronizer.send_event('E_MOD_ADD_ATTR', attr_name, mod, item_id, source_info)


def clear_add_factor(synchronizer):
    synchronizer.send_event('E_CLEAR_ADD_FACTOR')


def clear_bond_gifts(synchronizer):
    synchronizer.send_event('E_CLEAR_BOND_GIFTS')


def on_scenebox_holder_change(synchronizer, holder_soul_id):
    synchronizer.send_event('E_SCENE_BOX_HOLDER_CHANGE', holder_soul_id)