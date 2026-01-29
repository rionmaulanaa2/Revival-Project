# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/lobby_item_check_handler.py
from __future__ import absolute_import
import sys
import math
from data import lobby_item_use_conf, mecha_conf
from data.task import task_data
from data.lobby_item_data import get_item_use_type, get_item_use_parms, get_recycle_gain_item_list
from . import item_utility as iutil
from logic.gcommon import const
from logic.gcommon.cdata import bond_config as bond_conf
from logic.gcommon.cdata import bond_gift_config as bond_gift_conf
from logic.gcommon import time_utility as tutil

def do_item_check_hander(owner, item_no, cnt, params=None):
    use_type = get_item_use_type(item_no)
    if not use_type:
        log_error('do_item_check_hander, use_type not exist! item_no=%s', item_no)
        return 0
    else:
        use_conf = lobby_item_use_conf.GetUseConf().get(use_type, {})
        if not use_conf:
            log_error('do_item_check_hander, use_conf not exist! use_type=%s', use_type)
            return 0
        func_name = use_conf.get('CheckFunc', None)
        if not func_name:
            return cnt
        mod = sys.modules[__name__]
        if hasattr(mod, func_name):
            if params is None:
                params = {}
            params.update(get_item_use_parms(item_no, {}))
            ret = getattr(mod, func_name)(owner, item_no, cnt, params)
            if type(ret) != int:
                log_error('Please return int in check handler! func_name=%s', func_name)
                return 0
            return ret
        log_error('do_item_check_hander, hander not exist! hander=%s', func_name)
        return 0
        return


def check_add_proficiency(avatar, item_no, cnt, ext_info):
    mecha_type = ext_info['mecha_type']
    prof = ext_info['prof']
    lobby_mecha_id = mecha_conf.battle_mecha_2_lobby_mecha(mecha_type)
    if not avatar.has_mecha(lobby_mecha_id):
        return 0
    prof_can_add = avatar.check_proficiency_can_add(mecha_type, prof * cnt)
    can_use_cnt = prof_can_add / prof
    if prof_can_add % prof:
        can_use_cnt += 1
    return min(can_use_cnt, cnt)


def check_experience_card(avatar, item_no, cnt, ext_info):
    if ext_info.get('auto_use', 0):
        add_item_no = ext_info['add_item']
        cur_item = avatar.get_item_by_no(add_item_no)
        if cur_item and cur_item.get_expire_time() < 0:
            return 0
        return cnt
    else:
        return cnt


def check_task_card(avatar, item_no, cnt, ext_info):
    task_id = ext_info.get('task_id', None)
    if not task_id:
        return 0
    else:
        if avatar.task_has_finished(task_id):
            return 0
        cost_card_num = task_data.get_cost_task_card(task_id)
        if cost_card_num <= 0 or cost_card_num != cnt:
            return 0
        return cnt


def check_add_role_bond(avatar, item_no, cnt, ext_info):
    role_id = ext_info['role_id']
    role_id = int(role_id)
    bond = bond_conf.get_bond_gain_effect(item_no, role_id)
    if not avatar.has_role(role_id) or bond <= 0:
        return 0
    bond_can_add = avatar.check_bond_can_add(role_id, bond * cnt)
    can_use_cnt = bond_can_add / bond
    if bond_can_add % bond:
        can_use_cnt += 1
    return min(can_use_cnt, cnt)


def check_can_upgrade_bond_gift(avatar, item_no, cnt, ext_info):
    gift_id = ext_info.get('gift_id', None)
    role_id = ext_info.get('role_id', None)
    if not gift_id or not role_id or not avatar.has_role(role_id):
        return 0
    else:
        role_gifts = avatar.get_role_activated_bond_gifts(role_id)
        if not role_gifts or gift_id not in role_gifts:
            return 0
        need_item_config = bond_gift_conf.get_bond_gift_upgrade_item_config(gift_id)
        if not need_item_config:
            return 0
        need_item_no, need_item_num = need_item_config
        if not need_item_no or need_item_num <= 0:
            log_error('lobby_item_check_handler check_can_upgrade_bond_gift gift_id=%s invalid upgrade config.', gift_id)
            return 0
        if item_no != need_item_no or cnt < need_item_num:
            return 0
        return need_item_num


def check_exchange_item_open_time(avatar, item_no, cnt, ext_info):
    select = ext_info.get('select', 0)
    reward_list = ext_info.get('reward_list', ())
    len_rewardlist = len(reward_list)
    item_2_open_time = ext_info.get('item_exchange_open_time', {})
    selection = ext_info.get('selection', ())
    if not selection or len(selection) != select or not select or select > len_rewardlist:
        return 0
    now = tutil.get_time()
    for idx in selection:
        reward_id = str(reward_list[idx])
        if reward_id in item_2_open_time and item_2_open_time[reward_id] > now:
            return 0

    return cnt


def check_can_use_intimacy_item(avatar, item_no, cnt, ext_info):
    intimacy_per_gift = ext_info.get('intimacy')
    if not intimacy_per_gift:
        return 0
    frd_uid = ext_info.get('frd_uid')
    if not frd_uid:
        return 0
    if not avatar.is_friend(frd_uid):
        return 0
    intimacy_day_limit = avatar.get_intimacy_day_limit_by_uid(frd_uid, item_no)
    if cnt > intimacy_day_limit:
        return 0
    return cnt