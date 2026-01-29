# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/spectate_utils.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gcommon.common_const.spectate_const import SPECTATE_OB_PLAYER_INFO_KEYS

def parse_all_spectate_ob_player_info(raw_all_player_info):
    ret = {}
    for eid in raw_all_player_info:
        raw_player_info = raw_all_player_info[eid]
        result = parse_spectate_ob_player_info(raw_player_info)
        if not result or not result[0]:
            continue
        info = result[1]
        ret[eid] = info

    return ret


def parse_spectate_ob_player_info(raw_player_info):
    if not raw_player_info:
        return False
    else:
        try:
            info = {SPECTATE_OB_PLAYER_INFO_KEYS[i]:raw_player_info[i] for i in range(len(SPECTATE_OB_PLAYER_INFO_KEYS))}
        except Exception as e:
            log_error(e)
            import traceback
            traceback.print_stack()
            return False

        return (
         True, info)

    return False


def transform_to_group_dict(all_player_info_dict, sort=True):
    ret = {}
    for eid, info in six.iteritems(all_player_info_dict):
        group_id = info.get('group_id', None)
        if group_id is None:
            continue
        if group_id not in ret:
            ret[group_id] = []
        ret[group_id].append(eid)

    if sort:
        for group_id, pids in six.iteritems(ret):
            pids.sort()

    return ret


def has_live_competitions():
    if not global_data.player:
        return False
    from logic.gcommon.common_const import spectate_const as sp_const
    brief_list = global_data.player.get_global_specate_brief_info(sp_const.SPECTATE_LIST_COMPETITION)
    if not brief_list:
        return False
    from logic.gutils.observe_utils import decode_global_spectate_brief_info, is_global_spectate_data_time_valid
    for brief_data in brief_list:
        brief_data = decode_global_spectate_brief_info(brief_data)
        if not brief_data:
            continue
        if is_global_spectate_data_time_valid(brief_data):
            return True

    return False