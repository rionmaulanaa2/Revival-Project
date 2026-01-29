# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impReward.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from functools import cmp_to_key
from mobile.common.RpcMethodArgs import Str, Dict, Int, Bool, List
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from logic.gutils.mall_utils import get_lottery_table_to_mode_map
from logic.gutils.item_utils import get_item_rare_degree
from logic.gutils.reward_item_ui_utils import find_cur_active_probability_up_data, process_lottery_probability_up_data
from logic.gcommon.const import WEEKLY_MAX_GOLD

class impReward(object):

    def _init_reward_from_dict(self, bdict):
        self.reward_guarantee_dict = bdict.get('reward_guarantee_dict', {})
        self.category_intervene_round = bdict.get('reward_category_intervene_round', {})
        self.category_floor = bdict.get('reward_category_floor', {})
        self.reward_count = bdict.get('reward_count', {})
        self.intervene_count = bdict.get('intervene_count', {})
        self.guarantee_round_data = dict()
        self.probability_up_data = dict()
        self.reward_id_info = dict()
        self.random_reward_data = dict()
        self._intervene_up_timestamp_dict = dict()
        from logic.gutils.mall_utils import get_lottery_table_id_list
        self.request_reward_display_data(get_lottery_table_id_list())
        self.battle_reward = bdict.get('battle_reward', {})
        self._last_battle_reward = self.battle_reward
        self.reward_choose_dict = bdict.get('reward_choose_dict', {})

    def get_reward_guarantee_round_data(self, reward_id):
        data = self.guarantee_round_data.get(reward_id, [0, 100])
        return (
         self.reward_guarantee_dict.get(str(data[0]), 0), data[1])

    def get_reward_probability_up_data(self, reward_id):
        return self.probability_up_data.get(reward_id)

    def get_reward_display_data(self, reward_id):
        if reward_id in self.reward_id_info:
            return self.reward_id_info[reward_id]
        else:
            self.request_reward_display_data([reward_id])
            return None
            return None

    def get_random_reward_data(self, reward_id):
        if reward_id in self.random_reward_data:
            return self.random_reward_data[reward_id]
        else:
            self.request_random_reward_data([reward_id])
            return None
            return None

    def get_reward_category_intervene_round(self, reward_id, category):
        category_intervene_round = self.category_intervene_round.get(str(reward_id), {})
        return category_intervene_round.get(str(category), 0)

    def get_reward_category_floor(self, reward_id, category_floor_idx):
        category_floor = self.category_floor.get(str(reward_id), {})
        return category_floor.get(str(category_floor_idx), 0)

    def get_reward_count(self, reward_id):
        return self.reward_count.get(str(reward_id), 0)

    def get_reward_intervene_count(self, reward_id):
        return self.intervene_count.get(str(reward_id), {})

    @rpc_method(CLIENT_STUB, (Str('reward_name'), Int('reward_round')))
    def update_reward_guarantee_data(self, reward_name, reward_round):
        self.reward_guarantee_dict[reward_name] = reward_round

    @rpc_method(CLIENT_STUB, (Dict('intervene_round'), Dict('category_floor'), Dict('reward_count'), Dict('intervene_count')))
    def update_reward_category_data(self, intervene_round, category_floor, reward_count, intervene_count):
        if intervene_round:
            self.category_intervene_round.update(intervene_round)
        if category_floor:
            self.category_floor.update(category_floor)
        if reward_count:
            self.reward_count.update(reward_count)
        if intervene_count:
            self.intervene_count.update(intervene_count)

    def request_choose_reward(self, reward_name, choose_list):
        from common.cfg import confmgr
        optional_data = confmgr.get('preview_%s' % reward_name, 'optional_data', default=None)
        if not optional_data:
            return False
        else:
            choose_data = {}
            for item_no in choose_list:
                optional_idx, item_idx = optional_data[str(item_no)]
                choose_data[optional_idx] = item_idx

            reward_id = int(reward_name)
            self.call_server_method('request_choose_reward', (reward_id, str(reward_name), choose_data))
            return True

    @rpc_method(CLIENT_STUB, (Int('reward_id'), Str('reward_name'), List('choose_data')))
    def update_reward_choose_data(self, reward_id, reward_name, choose_data):
        if choose_data:
            reward_choose_data = self.reward_choose_dict.setdefault(reward_id, {})
            reward_choose_data[reward_name] = choose_data

    def is_reward_choose_valid(self, reward_name):
        from common.cfg import confmgr
        optional_data = confmgr.get('preview_%s' % reward_name, 'optional_data', default=None)
        if not optional_data:
            return False
        else:
            return True

    def get_reward_choose_list(self, reward_name):
        from common.cfg import confmgr
        optional_data = confmgr.get('preview_%s' % reward_name, 'optional_data', default=None)
        if not optional_data:
            return []
        else:
            reward_id = int(reward_name)
            reward_choose_data = self.reward_choose_dict.get(reward_id, {}).get(str(reward_name), [False, {}])
            return [ optional_data[str(choose_data[0])] for choose_data in six.itervalues(reward_choose_data[1]) if choose_data[0] is not None and choose_data[0] != -1 ]

    def request_random_reward_data(self, reward_id_list):
        self.call_server_method('request_random_reward_data', (reward_id_list,))

    def request_reward_display_data(self, reward_id_list):
        self.call_server_method('request_reward_display_data', (reward_id_list,))

    @rpc_method(CLIENT_STUB, (Dict('random_reward_data'),))
    def reply_random_reward_data(self, random_reward_data):
        self.random_reward_data.update(random_reward_data)
        global_data.emgr.receive_reward_info_from_server_event.emit()

    @rpc_method(CLIENT_STUB, (Dict('display_data_dict'),))
    def reply_reward_display_data(self, display_data_dict):
        has_probability_data_update = False
        self.probability_up_data = {}
        self._intervene_up_timestamp_dict = {}
        for reward_id in display_data_dict:
            items_set = set()
            reward_info = display_data_dict[reward_id]
            items_set.update(reward_info.get('fixed_reward', []))
            items_set.update(reward_info.get('cond_reward', []))
            random_reward = reward_info.get('random_reward', [])
            if random_reward:
                for category, rate_per, item_id_lst in random_reward[0][1]:
                    items_set.update(item_id_lst)

            item_id_lst = list(items_set)
            item_id_lst.sort(key=lambda x: get_item_rare_degree(x), reverse=True)
            self.reward_id_info[reward_id] = item_id_lst
            probability_data = reward_info.get('intervene_up_data', [])
            if probability_data:
                self.probability_up_data[reward_id] = find_cur_active_probability_up_data(reward_id, probability_data)
                has_probability_data_update = True
            self._intervene_up_timestamp_dict[reward_id] = reward_info.get('intervene_up_timestamp', None)

        global_data.emgr.receive_reward_info_from_server_event.emit()
        self.update_lottery_result_preview_data(display_data_dict)
        if has_probability_data_update:
            global_data.emgr.refresh_lottery_probability_up_data.emit()
        return

    def update_lottery_result_preview_data(self, data_dict):
        lottery_preview_data = dict()
        lottery_item_rate_data = dict()
        lottery_item_rate_up_data = dict()
        lottery_merge_item_info = dict()
        lottery_table_to_mode = get_lottery_table_to_mode_map(use_continual_goods_id=True)
        from common.cfg import confmgr
        item_conf = confmgr.get('lobby_item')
        for lottery_list_id, mode in six.iteritems(lottery_table_to_mode):
            if lottery_list_id not in data_dict:
                log_error('Server sent false lottery preview data!!!!')
                continue
            if not data_dict[lottery_list_id].get('random_reward', None):
                log_error('Server sent false lottery preview data!!!!')
                continue
            conf_name = 'preview_%d' % lottery_list_id
            conf = confmgr.get(conf_name, default=None)
            if conf is None:
                log_error('Table did not fill right!!!!')
                continue
            lottery_merge_item_info[mode] = dict()
            conf = conf.get_conf()
            cur_data = data_dict[lottery_list_id]['random_reward'][0][1]
            merge_item_priority = dict()
            lottery_item_rate_data[mode] = dict(data_dict[lottery_list_id]['random_reward'][0][2])

            def my_cmp(x, y):
                x_val = conf[str(x)] if str(x) in conf else (merge_item_priority[x] if x in merge_item_priority else 99)
                y_val = conf[str(y)] if str(y) in conf else (merge_item_priority[y] if y in merge_item_priority else 99)
                return six_ex.compare(x_val, y_val)

            for i in range(len(cur_data)):
                all_item = []
                for item_id in cur_data[i][2]:
                    merge_item_id = item_conf.get(str(item_id), {}).get('merge_item_id', None)
                    if merge_item_id:
                        if merge_item_id in merge_item_priority:
                            merge_item_priority[merge_item_id] = min(merge_item_priority[merge_item_id], conf[str(item_id)])
                            lottery_item_rate_data[mode][merge_item_id] += lottery_item_rate_data[mode][item_id]
                        else:
                            merge_item_priority[merge_item_id] = conf[str(item_id)]
                            all_item.append(merge_item_id)
                            lottery_item_rate_data[mode][merge_item_id] = lottery_item_rate_data[mode][item_id]
                        lottery_item_rate_data[mode].pop(item_id)
                        if merge_item_id in lottery_merge_item_info[mode]:
                            lottery_merge_item_info[mode][merge_item_id].append(item_id)
                            lottery_merge_item_info[mode][merge_item_id][0] += 1
                        else:
                            lottery_merge_item_info[mode][merge_item_id] = [
                             1, item_id]
                    else:
                        all_item.append(item_id)

                all_item.sort(key=cmp_to_key(my_cmp))
                cur_data[i][2] = all_item

            lottery_preview_data[mode] = cur_data
            if data_dict[lottery_list_id].get('guarantee_reward', None):
                self.guarantee_round_data[lottery_list_id] = data_dict[lottery_list_id]['guarantee_reward'][0]
            lottery_probability_up = self.probability_up_data.get(lottery_list_id, None)
            if lottery_probability_up:
                start_time, end_time, probability_data, banner_layout = lottery_probability_up
                _, probability_dict = process_lottery_probability_up_data(lottery_list_id, probability_data)
                lottery_item_rate_up_data[mode] = probability_dict

        from logic.comsys.lottery.LotteryPreviewWidget import LotteryPreviewWidget
        LotteryPreviewWidget.init_lottery_info(lottery_preview_data, lottery_item_rate_data, lottery_item_rate_up_data, lottery_merge_item_info)
        global_data.emgr.refresh_lottery_limited_guarantee_round.emit()
        return

    def check_is_probability_up_data_expired(self):
        for reward_id, intervene_up_timestamp in six.iteritems(self._intervene_up_timestamp_dict):
            if intervene_up_timestamp:
                need_calc = False
                from logic.gcommon import time_utility
                now = time_utility.get_server_time()
                up_item_first_timestamp, up_item_last_timestamp, up_item_end_timestamp, is_up_item = intervene_up_timestamp
                if now >= up_item_first_timestamp and not is_up_item or up_item_first_timestamp <= now < up_item_last_timestamp and now >= up_item_end_timestamp or now >= up_item_last_timestamp and is_up_item:
                    need_calc = True
                return need_calc

        return False

    def get_battle_reward(self, battle_settle=False):
        battle_reward = battle_settle and self._last_battle_reward if 1 else self.battle_reward
        battle_reward.setdefault('gold', 0)
        battle_reward.setdefault('max_gold', WEEKLY_MAX_GOLD)
        battle_reward.setdefault('last_add_gold', 0)
        return battle_reward

    @rpc_method(CLIENT_STUB, (Dict('battle_reward'), Bool('battle_settle')))
    def refresh_battle_reward(self, battle_reward, battle_settle):
        self.battle_reward = battle_reward
        if battle_settle:
            self._last_battle_reward = battle_reward