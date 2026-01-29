# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/rank_title_utils.py
from __future__ import absolute_import
import six
import six_ex
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import rank_pve_const, rank_const
from logic.gutils.item_utils import get_mecha_name_by_id
from logic.gcommon import time_utility as tutil

def get_pve_rank_title_text(rank_data):
    from logic.comsys.battle.pve.rank.PVERankDataObj import PVERankDataObj
    if not rank_data:
        return ''
    data_type_obj, rank, rank_expire = rank_data
    if isinstance(data_type_obj, str):
        data_obj = PVERankDataObj(data_type_obj) if 1 else data_type_obj
        server_rank_type = data_obj.to_server()
        min_rank = rank_pve_const.data.get(server_rank_type, {}).get('min_title_rank')
        if rank > min_rank:
            return ''
        split_ret = server_rank_type.split('_')
        if len(split_ret) == 4:
            chapter, difficulty, refresh_type, mecha_id = split_ret
        else:
            if len(split_ret) == 5:
                return ''
            return ''
        title_text_data = rank_pve_const.data.get(server_rank_type, {}).get('title_text')
        return title_text_data or ''
    for _rank, text_id in title_text_data:
        if rank <= _rank:
            if int(mecha_id) > 0:
                return get_text_by_id(text_id).format(n=chapter, mecha_name=get_mecha_name_by_id(mecha_id))
            else:
                return get_text_by_id(text_id)

    return ''


def get_pve_rank_title_icon(rank_data):
    from logic.comsys.battle.pve.rank.PVERankDataObj import PVERankDataObj
    default_path = 'gui/ui_res_2/rank/badge/badge_31000004.png'
    if not rank_data:
        return default_path
    data_type_obj, rank, rank_expire = rank_data
    if isinstance(data_type_obj, str):
        data_obj = PVERankDataObj(data_type_obj) if 1 else data_type_obj
        server_rank_type = data_obj.to_server()
        min_rank = rank_pve_const.data.get(server_rank_type, {}).get('min_title_rank')
        if rank > min_rank:
            return default_path
        title_icon_data = rank_pve_const.data.get(server_rank_type, {}).get('title_icon')
        return title_icon_data or default_path
    for _rank, icon in title_icon_data:
        if rank <= _rank:
            return icon

    return default_path


def get_pve_rank_title_bar(rank_data):
    from logic.comsys.battle.pve.rank.PVERankDataObj import PVERankDataObj
    default_path = 'gui/ui_res_2/rank/title/pnl_1.png'
    if not rank_data:
        return default_path
    data_type_obj, rank, rank_expire = rank_data
    if isinstance(data_type_obj, str):
        data_obj = PVERankDataObj(data_type_obj) if 1 else data_type_obj
        server_rank_type = data_obj.to_server()
        min_rank = rank_pve_const.data.get(server_rank_type, {}).get('min_title_rank')
        if rank > min_rank:
            return default_path
        title_bar_data = rank_pve_const.data.get(server_rank_type, {}).get('title_bar')
        return title_bar_data or default_path
    for _rank, bar in title_bar_data:
        if rank <= _rank:
            return bar

    return default_path


def get_pve_rank_title_list(title_type, custom_title_dict):
    from logic.comsys.battle.pve.rank.PVERankDataObj import PVERankDataObj
    rank_list = []
    for pve_rank_type, info in six.iteritems(custom_title_dict):
        rank = info[0]
        rank_expire = info[1]
        data_obj = PVERankDataObj(pve_rank_type)
        if data_obj.get_list_type() == rank_const.SEASON_REFRESH:
            from logic.gcommon.cdata import season_data
            is_expire = season_data.get_cur_battle_season() > rank_expire
        else:
            is_expire = tutil.time() > rank_expire
        if not is_expire:
            data = [
             title_type, pve_rank_type, rank, rank_expire]
            rank_list.append(data)

    return rank_list