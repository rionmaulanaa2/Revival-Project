# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impBattlePass.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from logic.comsys.battle_pass.UnlockRetrospectUI import UnlockRetrospectUI
from logic.gutils import item_utils, mall_utils, task_utils
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Str, Dict, Bool, List
from logic.gcommon.ctypes.Record import Record
from logic.gcommon.ctypes.RewardRecord import RewardRecord
from logic.gcommon.common_const import battlepass_const
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_CURRENCY
from common.platform import appsflyer_const as af_const
from common.platform.appsflyer import Appsflyer
from common.cfg import confmgr

class impBattlePass(object):

    def _init_battlepass_from_dict(self, bdict):
        self.battlepass_lv = bdict.get('battlepass_lv', 1)
        self.battlepass_point = bdict.get('battlepass_point', 0)
        self.battlepass_types = set((str(ele) for ele in bdict.get('battlepass_types', ())))
        self.battlepass_daily = bdict.get('battlepass_daily')
        self.active_battlepass_type = bdict.get('active_battlepass_type', None)
        self.active_retrospect_season = bdict.get('active_retrospect_season', [])
        self.first_enter_retrospect_system = bdict.get('first_enter_retrospect_system', True)
        if self.active_battlepass_type is not None:
            self.active_battlepass_type = str(self.active_battlepass_type)
        self.battlepass_reward_record = RewardRecord()
        self.battlepass_reward_record.init_from_dict(bdict.get('battlepass_reward_record', {}))
        self.active_gift_lv_upgrade = bdict.get('active_gift_lv_upgrade', 0)
        self.active_gift_lv_buy = bdict.get('active_gift_lv_buy', 0)
        self.active_gift_tasks = bdict.get('active_gift_tasks', [])

        def init_bp_exp_item_dict(exp_get_time):
            for season, item_info in six.iteritems(exp_get_time):
                if not self.bp_exp_item_dict.get(season):
                    self.bp_exp_item_dict[season] = []
                self.bp_exp_item_dict[season].append(item_info)

        self.bp_exp_item_dict = {}
        self.exp_mecha_get_time = bdict.get('exp_mecha_get_time', {}) or {}
        self.exp_role_get_time = bdict.get('exp_role_get_time', {}) or {}
        init_bp_exp_item_dict(self.exp_mecha_get_time)
        init_bp_exp_item_dict(self.exp_role_get_time)
        return

    @rpc_method(CLIENT_STUB, ())
    def reset_battlepass(self):
        self.battlepass_lv = 1
        self.battlepass_point = 0
        self.battlepass_types = set()
        self.battlepass_reward_record.clear()
        self.active_gift_lv_buy = 0
        self.active_gift_lv_upgrade = 0
        self.active_gift_tasks = []

    def activate_battlepass_type(self, battlepass_type):
        if battlepass_type in self.battlepass_types:
            return
        self.call_server_method('activate_battlepass_type', (battlepass_type,))

    @rpc_method(CLIENT_STUB, (List('battlepass_types'), Str('battlepass_reward_type'), Str('battlepass_type')))
    def open_battlepass_type(self, battlepass_types, battlepass_reward_type, battlepass_type):
        from logic.gutils.battle_pass_utils import get_buy_season_card_ui_name
        global_data.ui_mgr.close_ui('CardBuyCheck')
        global_data.ui_mgr.close_ui('BuyCardConfirmUI')
        global_data.ui_mgr.close_ui(get_buy_season_card_ui_name())
        if self.is_running_show_advance():

            def callback():
                global_data.ui_mgr.show_ui('BuyCardSuccess', 'logic.comsys.battle_pass')

            self.add_advance_callback('BuyCardSuccess', callback, advance_first=True)
            global_data.ui_mgr.close_ui('NewSeasonReward')
        else:
            global_data.ui_mgr.close_ui('NewSeasonReward')
            global_data.ui_mgr.show_ui('BuyCardSuccess', 'logic.comsys.battle_pass')
        self.battlepass_types = set(battlepass_types)
        self.battlepass_reward_record.setdefault(battlepass_reward_type, Record())
        self.active_battlepass_type = battlepass_type
        self.check_active_battlepass_card_on_free_trial()
        global_data.emgr.season_pass_open_type.emit(battlepass_types)
        if battlepass_const.SEASON_PASS_L2 == battlepass_type:
            Appsflyer().advert_track_event(event_name=af_const.AF_SEASON_BATTLEPASS_H)
        elif battlepass_const.SEASON_PASS_L1 == battlepass_type:
            Appsflyer().advert_track_event(event_name=af_const.AF_SEASON_BATTLEPASS_L)

    def accept_to_add_bp(self):
        self.call_server_method('accept_to_add_bp', ())

    def activate_battlepass_lv(self, battlepass_lv):
        self.call_server_method('activate_battlepass_lv', (battlepass_lv,))

    @rpc_method(CLIENT_STUB, (Int('battlepass_lv'), Int('battlepass_point'), Bool('show_ad')))
    def update_battlepass_lv(self, battlepass_lv, battlepass_point, show_ad):
        if self.battlepass_lv < battlepass_lv:
            self.active_gift_lv_upgrade = int(min(self.active_gift_lv_buy, self.active_gift_lv_upgrade + battlepass_lv - self.battlepass_lv))
        if self.battlepass_lv != battlepass_lv:
            if show_ad:
                ui = global_data.ui_mgr.show_ui('BpAdvisementUI', 'logic.comsys.battle_pass')
                if ui:
                    ui.set_level(battlepass_const.SEASON_CARD, self.battlepass_lv, battlepass_lv)
            else:
                ui = global_data.ui_mgr.show_ui('SeasonPassLevelUp', 'logic.comsys.battle_pass')
                if ui:
                    ui.set_level(battlepass_const.SEASON_CARD, self.battlepass_lv, battlepass_lv)
        self.battlepass_lv = battlepass_lv
        self.battlepass_point = battlepass_point
        global_data.emgr.season_pass_update_lv.emit(self.battlepass_lv, self.battlepass_point)
        for check_lv in af_const.af_battlepass_lvs:
            if self.battlepass_lv >= check_lv:
                Appsflyer().advert_track_event(event_name=af_const.AF_BATTLEPASS_LV, suffix=str(check_lv))
                break

    def receive_battlepass_reward(self, battlepass_reward_type, battlepass_lv):
        self.call_server_method('receive_battlepass_reward', (battlepass_reward_type, battlepass_lv))

    def receive_all_battlepass_reward(self):
        self.call_server_method('receive_all_battlepass_reward', ())

    @rpc_method(CLIENT_STUB, (Dict('battlepass_reward_records'),))
    def update_battlepass_rewards(self, battlepass_reward_records):
        dif_reward_dict = {}
        for battlepass_reward_type, record_data in six.iteritems(battlepass_reward_records):
            reward_record = self.battlepass_reward_record.setdefault(battlepass_reward_type, Record())
            old_reward_set = reward_record.get_reward_set()
            reward_record.update(record_data[0], set(record_data[1]))
            now_award_set = reward_record.get_reward_set()
            minus_award_set = now_award_set - old_reward_set
            dif_reward_dict[battlepass_reward_type] = minus_award_set

        global_data.emgr.season_pass_update_award.emit(dif_reward_dict)

    def get_battlepass_info(self):
        return (
         self.battlepass_lv, self.battlepass_point)

    def get_battlepass_types(self):
        return self.battlepass_types

    def get_battlepass_reward_record(self):
        return self.battlepass_reward_record

    def has_activate_battlepass_type(self, battlepass_type=None):
        if battlepass_type is None:
            return len(self.battlepass_types) > 0
        else:
            return battlepass_type in self.battlepass_types
            return

    def has_buy_season_card_type(self):
        return len(self.battlepass_types) > 0

    def has_buy_one_kind_season_card(self):
        return len(self.battlepass_types) > 0

    def has_buy_final_card(self):
        for sp_type in battlepass_const.SEASON_CARD_FINAL_TYPE:
            if str(sp_type) in self.battlepass_types:
                return True

        return False

    def has_buy_test_version_card(self):
        return battlepass_const.SEASON_PASS_L3 in self.battlepass_types

    @rpc_method(CLIENT_STUB, (Bool('battlepass_daily'),))
    def on_battlepass_daily_state(self, battlepass_daily):
        self.battlepass_daily = battlepass_daily
        global_data.emgr.season_pass_update_daily_award.emit()

    def try_get_battlepass_daily_reward(self):
        self.call_server_method('get_battlepass_daily_reward', ())

    def has_get_season_pass_daily_award(self):
        return self.battlepass_daily

    def unlock_retrospect_season(self, season):
        conf = confmgr.get('season_retrospect_info')
        act_item = conf.get('act_item', None)
        act_num = conf.get('act_num', 2)
        money_type = mall_utils.get_item_money_type(int(act_item))
        coin_num = mall_utils.get_my_money(money_type)
        if coin_num < act_num:
            return
        else:
            self.call_server_method('request_unlock_retrosepct_season', (season,))
            return

    def unlock_retrospect_task(self, task_id, season):
        task_list = []
        season_path = 'season_retrospect_{}'.format(season)
        retrospect_conf = confmgr.get(season_path)
        if not retrospect_conf:
            return
        base_tasks = retrospect_conf.get('base_task', [])
        advanced_tasks = retrospect_conf.get('advanced_task', [])
        ultimate_tasks = retrospect_conf.get('ultimate_task', [])
        task_list = base_tasks + advanced_tasks + ultimate_tasks
        if task_id not in task_list:
            return
        idx = task_list.index(task_id)
        for i in range(idx):
            t_id = task_list[i]

        task_conf = task_utils.get_task_conf_by_id(task_id)
        unlock_item = task_conf.get('retrospect_arg', {}).get('unlock_item', {})
        for k, v in six.iteritems(unlock_item):
            money_type = mall_utils.get_item_money_type(int(k))
            coin_num = mall_utils.get_my_money(money_type)
            if coin_num < v:
                return

        self.call_server_method('request_unlock_task', (task_id, season))

    def is_season_retrospect_unlocked(self, season):
        return season in self.active_retrospect_season

    @rpc_method(CLIENT_STUB, (Int('season'),))
    def unlock_retrospect_season_succeed(self, season):
        if season not in self.active_retrospect_season:
            self.active_retrospect_season.append(season)
        if self.is_running_show_advance():

            def callback():
                UnlockRetrospectUI(None, season)
                return

            self.add_advance_callback('UnlockRetrospectUI', callback, advance_first=True)
        else:
            UnlockRetrospectUI(None, season)
        global_data.emgr.retrospect_season_unlocked.emit()
        return

    def get_unreceived_task_cnt(self, season):
        path = 'season_retrospect_{}'.format(season)
        conf = confmgr.get(path)
        cnt = 0
        if not conf:
            return cnt
        task_list = conf.get('base_task', []) + conf.get('advanced_task', []) + conf.get('ultimate_task', [])
        for task_id in task_list:
            task_status = self.get_task_reward_status(task_id)
            if task_status == ITEM_UNRECEIVED:
                cnt += 1

        return cnt

    def get_retrospect_prog(self, season):
        path = 'season_retrospect_{}'.format(season)
        conf = confmgr.get(path)
        prog = 0
        if not conf:
            return (0, 0)
        task_list = conf.get('base_task', []) + conf.get('advanced_task', []) + conf.get('ultimate_task', [])
        for task_id in task_list:
            if self.is_retrospect_task_finished(task_id):
                prog += 1

        return (
         prog, len(task_list))

    def is_retrospect_season_finished(self, season):
        path = 'season_retrospect_{}'.format(season)
        conf = confmgr.get(path)
        if not conf:
            return False
        base_task = conf.get('base_task')
        if not self.is_retrospect_tasks_finished(base_task):
            return False
        advanced_task = conf.get('advanced_task')
        if not self.is_retrospect_tasks_finished(advanced_task):
            return False
        ultimate_task = conf.get('ultimate_task')
        if not self.is_retrospect_tasks_finished(ultimate_task):
            return False
        return True

    def is_retrospect_tasks_finished(self, task_list):
        for task_id in task_list:
            if not self.is_retrospect_task_finished(task_id):
                return False

        return True

    def is_retrospect_task_finished(self, task_id):
        if self.get_task_reward_status(task_id) == ITEM_RECEIVED:
            return True
        reward_id = task_utils.get_task_reward(task_id)
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        reward_list = reward_conf.get('reward_list', [])
        for reward in reward_list:
            item, num = reward
            if item_utils.get_lobby_item_type(item) == L_ITEM_TYPE_CURRENCY or self.has_item_by_no(item):
                continue
            else:
                return False

        return True

    def on_enter_retrospect_system(self):
        if self.first_enter_retrospect_system:
            self.call_server_method('first_enter_retrospect', ())

    @rpc_method(CLIENT_STUB, ())
    def first_enter_retrospect_succeed(self):
        self.first_enter_retrospect_system = False

    def buy_battlepass_active_gift(self, lv):
        print('buy_battle_gift', lv)
        self.call_server_method('buy_battlepass_active_gift', (lv,))

    @rpc_method(CLIENT_STUB, (Int('active_gift_lv_upgrade'), Int('active_gift_lv_buy'), List('active_gift_tasks')))
    def buy_battlepass_active_gift_succeed(self, active_gift_lv_upgrade, active_gift_lv_buy, active_gift_tasks):
        self.active_gift_lv_upgrade = active_gift_lv_upgrade
        self.active_gift_lv_buy = active_gift_lv_buy
        self.active_gift_tasks = active_gift_tasks
        global_data.emgr.season_pass_buy_active_gift.emit()
        self.receive_all_battlepass_reward()

    def get_active_gift_tasks(self):
        return self.active_gift_tasks

    def get_active_gift_lv_buy(self):
        return self.active_gift_lv_buy

    def get_active_gift_lv_upgrade(self):
        return self.active_gift_lv_upgrade

    def get_unfinished_lv(self):
        return int(self.active_gift_lv_buy - self.active_gift_lv_upgrade)

    def update_bp_exp_item_dict(self, _time_dict):
        self.bp_exp_item_dict.update(_time_dict)

    def get_bp_exp_item_dict(self):
        return self.bp_exp_item_dict or {}

    def check_active_battlepass_card_on_free_trial(self):
        from logic.gutils.battle_pass_utils import on_avatar_active_battlepass
        on_avatar_active_battlepass()