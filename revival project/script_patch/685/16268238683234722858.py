# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/lv_template_utils.py
from __future__ import absolute_import
from six.moves import range
from data.c_lv_data_const import LV_CAP, STAR_EXP
from common.const.property_const import U_LV
MIN_LV = 1

def init_lv_node(lv_item, lv):
    if lv < MIN_LV:
        log_error('0\xe7\xba\xa7\xe4\xb8\xba\xe4\xb8\x8d\xe5\x90\x88\xe6\xb3\x95\xe7\x9a\x84\xe7\xad\x89\xe7\xba\xa7\xef\xbc\x81')
        return
    if not (lv_item and lv_item.lab_level):
        log_error('item or item.lab_level is None')
        return
    lv_item.lab_level.setVisible(True)
    lv_item.lab_level.SetString(str(lv))


def init_lv_template(panel, lv):
    if int(lv) < 100:
        panel.nd_level_normal.setVisible(True)
        panel.nd_level_special.setVisible(False)
        panel.nd_level_normal.lab_level_normal.SetString(str(lv))
    else:
        panel.nd_level_normal.setVisible(False)
        panel.nd_level_special.setVisible(True)
        panel.nd_level_special.lab_level_special.SetString(str(lv))


def get_friend_lv(uid, req_server=True):
    import time
    player_inf = global_data.message_data.get_player_simple_inf(uid)
    if not player_inf:
        if global_data.player:
            global_data.player.request_player_simple_inf(uid)
        return
    else:
        if req_server:
            if time.time() - player_inf['save_time'] < 300:
                return player_inf.get(U_LV, 1)
            if global_data.player:
                global_data.player.request_player_simple_inf(uid)
        else:
            return player_inf.get(U_LV, 1)
        return


def get_add_exp_by_lv_range(old_lv, old_exp, new_lv, new_exp):
    from common.cfg import confmgr
    if old_lv > new_lv:
        return 0
    add_exp = 0
    cur_lv = old_lv
    cur_exp = old_exp
    count = new_lv - old_lv + 1
    for i in range(count):
        if cur_lv == new_lv:
            cur_need_exp = new_exp - cur_exp
        else:
            cur_need_exp = confmgr.get('c_lv_data', str(cur_lv), 'iEXP', default=0)
        add_exp += cur_need_exp
        cur_lv += 1
        cur_exp = 0

    return add_exp


def get_lv_upgrade_need_exp(lv):
    if lv < MIN_LV:
        log_error('\xe7\xad\x89\xe7\xba\xa7\xe5\xb0\x8f\xe4\xba\x8e\xe6\x9c\x80\xe5\xb0\x8f\xe7\xad\x89\xe7\xba\xa7\xef\xbc\x81', lv)
        import traceback
        traceback.print_stack()
        return 10000 - abs(lv)
    else:
        if lv >= LV_CAP:
            return STAR_EXP
        from common.cfg import confmgr
        lv_conf = confmgr.get('c_lv_data', str(lv), default={})
        return lv_conf.get('iEXP', None)
        return


def is_full_lv(lv):
    return False


def get_cur_lv_percentage(cur_lv, cur_exp):
    lv_exp_need = get_lv_upgrade_need_exp(cur_lv)
    if not lv_exp_need:
        return 0
    else:
        exp_percent = float(cur_exp) / lv_exp_need
        return exp_percent


def get_cur_lv_reward(lv):
    from common.cfg import confmgr
    lv_conf = confmgr.get('c_lv_data', str(lv), default={})
    if not lv_conf:
        lv_conf = confmgr.get('c_lv_data', 'default', default={})
    if not lv_conf.get('Reward'):
        return (None, 0)
    else:
        reward = confmgr.get('common_reward_data', str(lv_conf['Reward']))
        if not reward:
            return (None, 0)
        reward_item = reward['reward_list'][0]
        return (
         reward_item[0], reward_item[1])