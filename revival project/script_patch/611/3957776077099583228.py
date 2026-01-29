# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/status_utils.py
from __future__ import absolute_import
import six
from logic.gcommon.cdata import mecha_status_config

def get_behavior_config(npc_id):
    if npc_id.find('_') > 0:
        npc_id, _ = npc_id.split('_')
    mpath = 'logic.gcommon.cdata.%s' % npc_id
    data = __import__(mpath, globals(), locals(), [npc_id])
    return data


def convert_status(st_set):
    ret = set([])
    for st in st_set:
        if isinstance(st, str):
            st = mecha_status_config.desc_2_num[st]
        ret.add(st)

    return ret


def get_behavior_status_param(npc_id, status, key=None, default=None):
    s_npc_id = str(npc_id)
    data = get_behavior_config(s_npc_id).get_behavior(s_npc_id)
    if data:
        custom_param = data.get(status, {}).get('custom_param', {})
        if key:
            return custom_param.get(key, default)
        return custom_param
    return default


def get_forbid_copy(npc_id):
    default = get_behavior_config(npc_id).get_forbid(npc_id)
    forbid_data = {k:set(v) for k, v in six.iteritems(default)}
    return forbid_data


def get_cover_copy(npc_id):
    default = get_behavior_config(npc_id).get_cover(npc_id)
    cover_data = {k:set(v) for k, v in six.iteritems(default)}
    return cover_data