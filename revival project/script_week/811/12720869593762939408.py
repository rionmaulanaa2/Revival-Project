# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/battle_pass_utils.py
from __future__ import absolute_import
from six.moves import range
import logic.gcommon.common_const.battlepass_const as bp_const
import six
from data.season_update_config import TOKEN_DICT, MONEY_DICT, NOW_SEASON
from logic.gcommon.item.item_const import ITEM_UNRECEIVED

def get_now_season():
    if not global_data.player:
        return NOW_SEASON
    return int(global_data.player.get_battle_season())


def get_retrospect_season_unlock_item():
    from common.cfg import confmgr
    return confmgr.get('season_retrospect_info', 'act_item', default=None)


def get_retrospect_task_unlock_item(season):
    path = 'season_retrospect_{}'.format(season)
    return confmgr.get(path, 'task_unlock_coin', default=None)


def get_season_token(season):
    return TOKEN_DICT.get(season, None)


def get_season_money(season):
    return MONEY_DICT.get(season, None)


def get_now_season_money():
    now_season = get_now_season()
    return get_season_money(now_season)


def get_exchange_goods_lst(season):
    m_path = 'data.season_pass_data_%s' % season
    data = __import__(m_path, globals(), locals(), ['season_pass_data_%s' % season])
    return data.EXCHANGE_MALL_ITEM


def get_permium_exchange_goods_lst(season):
    m_path = 'data.season_pass_data_%s' % season
    data = __import__(m_path, globals(), locals(), ['season_pass_data_%s' % season])
    return data.PERMIUM_EXCHANGE_MALL_ITEM


def get_season_pass_data(season):
    m_path = 'data.season_pass_data_%s' % season
    data = __import__(m_path, globals(), locals(), ['season_pass_data_%s' % season])
    return data


def get_now_season_pass_data():
    now_season = get_now_season()
    return get_season_pass_data(now_season)


def refresh_battlepass_lv_item(nd_bp_item, lv, point):
    sp_lv_data = get_now_season_pass_data().season_pass_lv_data
    nd_bp_item.nd_level.lab_level.SetString('LV.%d' % lv)
    next_lv_point = sp_lv_data[lv][0]
    now_lv_point = 0 if lv <= 1 else sp_lv_data[lv - 1][0]
    need_point = next_lv_point - now_lv_point
    next_lv_point = sp_lv_data[lv][0]
    if next_lv_point:
        nd_bp_item.nd_exp.exp_layout.progress_exp.SetPercent((point - now_lv_point) * 100.0 / need_point)
        nd_bp_item.nd_exp_num.lab_num_exp.SetString(str(point - now_lv_point))
        nd_bp_item.nd_exp_num.lab_num_exp_need.SetString('/%s' % str(need_point))


def need_sp_red():
    if not global_data.player:
        return False
    else:
        from logic.gutils import system_unlock_utils
        has_unlock = system_unlock_utils.is_sys_unlocked(system_unlock_utils.SYSTEM_BATTLE_PASS)
        if not has_unlock:
            return False
        from logic.gcommon.common_const.battlepass_const import SEASON_CARD_TYPE, SEASON_PASS_L2, SEASON_PASS_L3, SEASON_PASS_L1
        if not global_data.player:
            has_buy_card = False if 1 else global_data.player.has_buy_one_kind_season_card()
            season_pass_lv, _ = global_data.player.get_battlepass_info()
            card_list = (
             SEASON_PASS_L1, SEASON_PASS_L2, SEASON_PASS_L3)
            care_reward_type_list = (SEASON_PASS_L2,)
            sp_data = get_now_season_pass_data()
            reward_type_limit_dict = {SEASON_PASS_L2: 0}
            for card in card_list:
                if global_data.player.has_activate_battlepass_type(card):
                    for reward_type in care_reward_type_list:
                        limit_lv = sp_data.season_pass_type_data.get(card).get('battlepass_reward_limit_lv', {}).get(reward_type, sp_data.SEASON_PASS_LV_CAP)
                        if limit_lv > reward_type_limit_dict.get(reward_type, 0):
                            reward_type_limit_dict[reward_type] = limit_lv

            return global_data.player.has_get_season_pass_daily_award() or True
        from common.cfg import confmgr
        sp_data = get_now_season_pass_data()
        for sp_type in SEASON_CARD_TYPE:
            if sp_type == SEASON_PASS_L2 and not has_buy_card:
                continue
            max_check_lv = sp_data.SEASON_PASS_LV_CAP
            if sp_type in reward_type_limit_dict:
                max_check_lv = reward_type_limit_dict[sp_type]
            reward_record = global_data.player.get_battlepass_reward_record().get(str(sp_type), None)
            for lv in range(min(season_pass_lv, max_check_lv)):
                sp_lv = lv + 1
                if reward_record is None:
                    is_received = False if 1 else reward_record.is_record(sp_lv)
                    reward_lv_id = is_received or sp_data.get_lv_reward(str(sp_type), sp_lv)
                    if reward_lv_id:
                        reward_conf = confmgr.get('common_reward_data', str(reward_lv_id))
                        reward_list = reward_conf.get('reward_list', [])
                        if len(reward_list) > 0:
                            return True

        from logic.gutils import mall_utils
        now_season = get_now_season()
        need_show_entry_rp = mall_utils.check_can_show_sp_exchange_entry_rp(now_season)
        if need_show_entry_rp and mall_utils.check_item_money(get_season_token(now_season), 1, pay_tip=False):
            for goods_id in get_exchange_goods_lst(now_season):
                valid, need_rp = mall_utils.check_sp_exchange_goods(goods_id, now_season)
                if valid and need_rp:
                    return True

        open_season = confmgr.get('season_retrospect_info').get('open_season')
        for season in open_season:
            if global_data.player and global_data.player.get_unreceived_task_cnt(season) > 0:
                return True

        task_list = global_data.player.get_active_gift_tasks()
        for task_id in task_list:
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNRECEIVED:
                return True

        return False


def get_buy_season_card_ui_name():
    return 'BuySeasonCardUI'


def get_season_card_consumed(season_pass_data, card_type):
    season_pass_type_data = season_pass_data.season_pass_type_data
    pre_yuan_bao_consumed = season_pass_type_data[card_type]['yuanbao_consumed']
    if callable(pre_yuan_bao_consumed):
        real_yuan_bao_consumed = global_data.player or 99999 if 1 else pre_yuan_bao_consumed(global_data.player)
    else:
        real_yuan_bao_consumed = pre_yuan_bao_consumed
    return real_yuan_bao_consumed


def get_season_card_price_info(season_pass_data, card_type):
    from logic.gcommon.common_const.battlepass_const import SEASON_PASS_L1, SEASON_PASS_L2, SEASON_PASS_L3
    import math
    season_pass_type_data = season_pass_data.season_pass_type_data
    up_types = season_pass_type_data[card_type].get('upgrade_to_battlepass_types', [])
    high_types = set(up_types)
    for up_card_type in up_types:
        tmp_high_types = set(season_pass_type_data[up_card_type].get('upgrade_to_battlepass_types', []))
        high_types |= tmp_high_types

    now_bp_types = global_data.player or set() if 1 else global_data.player.get_battlepass_types()
    if card_type in now_bp_types or now_bp_types & high_types:
        text_id = 12014 if card_type in now_bp_types else 12121
        price_info = None
        real_price = None
    else:
        consume_yuan_bao = get_season_card_consumed(season_pass_data, card_type)
        original_yuan_bao = season_pass_type_data.get(str(card_type)).get('orginal_yuanbao')
        low_type_lst = bp_const.LOW_CARD_TYPE_INFO[card_type]
        for low_type in low_type_lst:
            if low_type in now_bp_types:
                consume_yuan_bao -= get_season_card_consumed(season_pass_data, low_type)
                break

        battle_pass_gift = global_data.player.get_battle_pass_chance_gift()
        if battle_pass_gift:
            discount = battle_pass_gift.get('discount', 0)
            if discount > 0:
                if card_type == SEASON_PASS_L2:
                    original_yuan_bao = consume_yuan_bao
                consume_yuan_bao = int(math.floor(consume_yuan_bao * discount))
        discount_price = None if consume_yuan_bao == original_yuan_bao else consume_yuan_bao
        from logic.gcommon.const import SHOP_PAYMENT_YUANBAO
        price_info = {'original_price': original_yuan_bao,
           'discount_price': discount_price,
           'goods_payment': SHOP_PAYMENT_YUANBAO
           }
        text_id = ''
        real_price = consume_yuan_bao
    return (
     price_info, real_price, text_id)


def check_trial_version_sp(lv, sp_data=None):
    if global_data.player and global_data.player.active_battlepass_type == bp_const.SEASON_PASS_L3:
        if sp_data is None:
            sp_data = get_now_season_pass_data()
        sp_info_l3 = sp_data.season_pass_type_data.get(bp_const.SEASON_PASS_L3, None)
        if sp_info_l3:
            limit_lv = sp_info_l3['battlepass_reward_limit_lv'][bp_const.SEASON_PASS_L2]
            return lv <= limit_lv
    return True


def get_receive_num(now_sp_level, sp_data=None, only_check=False):
    from common.cfg import confmgr
    can_receive_num = 0
    if sp_data is None:
        sp_data = get_now_season_pass_data()
    lv_unfinished = global_data.player.get_unfinished_lv()
    for sp_type in bp_const.SEASON_CARD_TYPE:
        if sp_type == bp_const.SEASON_PASS_L2 and not global_data.player.has_buy_one_kind_season_card():
            continue
        reward_record = global_data.player.get_battlepass_reward_record().get(str(sp_type), None)
        for lv in range(now_sp_level + lv_unfinished):
            sp_lv = lv + 1
            if sp_type == bp_const.SEASON_PASS_L2 and not check_trial_version_sp(sp_lv, sp_data):
                break
            if reward_record is None:
                is_received = False if 1 else reward_record.is_record(sp_lv)
                reward_lv_id = is_received or sp_data.get_lv_reward(str(sp_type), sp_lv)
                if reward_lv_id:
                    reward_conf = confmgr.get('common_reward_data', str(reward_lv_id))
                    reward_list = reward_conf.get('reward_list', [])
                    can_receive_num += len(reward_list)
                    if only_check and can_receive_num > 0:
                        return can_receive_num

    return can_receive_num


def is_sp_level_has_reward(sp_level, sp_data=None):
    from common.cfg import confmgr
    can_receive_num = 0
    if sp_data is None:
        sp_data = get_now_season_pass_data()
    for sp_type in bp_const.SEASON_CARD_TYPE:
        if sp_type == bp_const.SEASON_PASS_L2 and not global_data.player.has_buy_one_kind_season_card():
            continue
        if sp_type == bp_const.SEASON_PASS_L2 and not check_trial_version_sp(sp_level, sp_data):
            continue
        reward_record = global_data.player.get_battlepass_reward_record().get(str(sp_type), None)
        if reward_record is None:
            is_received = False if 1 else reward_record.is_record(sp_level)
            reward_lv_id = is_received or sp_data.get_lv_reward(str(sp_type), sp_level)
            if reward_lv_id:
                reward_conf = confmgr.get('common_reward_data', str(reward_lv_id))
                reward_list = reward_conf.get('reward_list', [])
                can_receive_num += len(reward_list)
                if can_receive_num > 0:
                    return can_receive_num

    return can_receive_num


def get_season_pass_coin_path(season):
    return 'gui/ui_res_2/icon/icon_s{}.png'.format(season)


def on_avatar_active_battlepass():
    if not global_data.player:
        return
    from logic.gcommon import time_utility
    from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_belong_no
    active_battlepass_type = global_data.player.active_battlepass_type
    now_season_data = get_now_season_pass_data()
    core_reward = tuple(now_season_data.two_core_reward)
    cur_season = global_data.player.get_battle_season()
    if active_battlepass_type:
        if active_battlepass_type in ('1', '2'):
            reward_dic = [{str(get_lobby_item_belong_no(core_reward[0])): time_utility.get_server_time()}, {str(get_lobby_item_belong_no(core_reward[1])): time_utility.get_server_time()}]
            update_dict = {str(cur_season): reward_dic}
            global_data.player.update_bp_exp_item_dict(update_dict)


def avatar_get_battlepass_free_ids_dict():
    if not global_data.player:
        return {}
    from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_belong_no
    cur_season = global_data.player.get_battle_season()
    now_season_data = get_now_season_pass_data()
    core_reward = tuple(now_season_data.two_core_reward)
    active_battlepass_type = global_data.player.active_battlepass_type
    free_ids_dict = {}
    bp_exp_item_dict = dict(global_data.player.get_bp_exp_item_dict())
    sorted_keys = sorted(bp_exp_item_dict.keys(), key=lambda x: int(x))
    for season in sorted_keys:
        season_exp_item_list = bp_exp_item_dict[season]
        for season_exp_item_dict in season_exp_item_list:
            for item_no, item_time in six.iteritems(season_exp_item_dict):
                free_ids_dict[item_no] = [
                 item_time, season]

    for item_no in list(free_ids_dict.keys()):
        item = global_data.player.get_item_by_no(int(item_no))
        if not (item and not item.is_permanent_item()):
            del free_ids_dict[item_no]

    return free_ids_dict


def update_battlepass_free_trial_template(temp_bp_free, target_id):
    import logic.gcommon.time_utility as time_utils
    bp_free_dicts = avatar_get_battlepass_free_ids_dict()
    if not target_id:
        temp_bp_free.setVisible(False)
        temp_bp_free.stopAllActions()
        return
    buy_timestamp, season = bp_free_dicts.get(str(target_id), [-1, -1])
    temp_bp_free.stopAllActions()
    temp_bp_free.setVisible(buy_timestamp >= 0)
    if buy_timestamp >= 0:
        end_timestamp = buy_timestamp + bp_const.BATTLE_PASS_MECHA_TRIAL_TIME
        season_money = get_season_money(int(season))
        from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
        pic = get_lobby_item_pic_by_item_no(season_money)

        def update_func():
            cur_time = time_utils.get_server_time()
            left_time = end_timestamp - cur_time
            left_time = max(0, left_time)
            temp_bp_free.lab_countdown.SetString(get_text_by_id(633922, [time_utils.get_simply_time(left_time)]))
            if left_time == 0:
                temp_bp_free.setVisible(False)
                return 0
            return 5

        temp_bp_free.DelayCallWithTag(5, update_func, tag=230921)
        update_func()


def get_is_battlepass_free_trial(target_id):
    import logic.gcommon.time_utility as time_utils
    bp_free_dicts = avatar_get_battlepass_free_ids_dict()
    buy_timestamp, _ = bp_free_dicts.get(str(target_id), [-1, -1])
    end_timestamp = buy_timestamp + bp_const.BATTLE_PASS_MECHA_TRIAL_TIME
    return end_timestamp > time_utils.get_server_time()