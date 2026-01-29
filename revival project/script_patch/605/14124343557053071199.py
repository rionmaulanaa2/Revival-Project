# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impPrivilege.py
from __future__ import absolute_import
import six
from logic.gcommon.cdata import privilege_data
from logic.gcommon.ctypes.Record import Record
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Dict, Int, List, Bool
from logic.gcommon.const import PRIV_SHOW_BADGE, PRIV_SHOW_PURPLE_ID, PRIV_SHOW_COLORFUL_FONT, PRIV_SETTING_KEYS, PRIVILEGE_SETTING_TO_RED_POINT, PRIV_RED_PACKET, PRIV_ENJOY_FREE_TIMES_PER_WEEK
from logic.gcommon.item.item_const import FASHION_POS_WEAPON_SFX, FASHION_POS_SUIT
from logic.gutils.item_utils import get_item_rare_degree
from logic.gcommon.item import item_const as iconst
from logic.gutils.mecha_skin_utils import get_mecha_base_skin_id
from logic.gcommon.common_utils.local_text import get_text_by_id

class impPrivilege(object):

    def _init_privilege_from_dict(self, bdict):
        self.priv_reward_record = Record(bdict.get('priv_reward_record', {}))
        self.priv_lv = bdict.get('priv_lv', 0)
        self.priv_settings = bdict.get('priv_settings', {})
        self.priv_colorful_font = bdict.get('priv_colorful_font', False)
        self.priv_purple_id = bdict.get('priv_purple_id', False)
        self.priv_share_mecha_fashion = bdict.get('priv_share_mecha_fashion', False)
        self.priv_red_packet = bdict.get('priv_red_packet', False)
        self.priv_max_lv_notified = bdict.get('priv_max_lv_notified', 0)
        self.priv_enjoy_free_cnt = bdict.get('priv_enjoy_free_cnt', PRIV_ENJOY_FREE_TIMES_PER_WEEK)
        self.chosen_pve_priv_skin = {}
        self.priv_mecha_fashion_dict = {}
        self.setting_to_value = {PRIV_SHOW_BADGE: self.priv_lv,
           PRIV_SHOW_PURPLE_ID: self.priv_purple_id,
           PRIV_SHOW_COLORFUL_FONT: self.priv_colorful_font
           }
        self._init_client_setting()

    def _init_client_setting(self):
        if self.priv_settings:
            for k, v in six.iteritems(self.priv_settings):
                if k in PRIV_SETTING_KEYS:
                    global_data.achi_mgr.set_cur_user_archive_data(k + str(self.uid), v)
                    global_data.achi_mgr.set_cur_user_archive_data(PRIVILEGE_SETTING_TO_RED_POINT[k] + str(self.uid), 1)

    @rpc_method(CLIENT_STUB, (Int('last_record_lv'), List('lv_rewards'), Int('last_reward_lv')))
    def update_priv_reward_record(self, last_record_lv, lv_rewards, last_reward_lv):
        self.priv_reward_record.update(last_record_lv, set(lv_rewards))
        global_data.emgr.receive_privilege_level_reward_succ.emit(last_reward_lv, set(lv_rewards))

    @rpc_method(CLIENT_STUB, (Dict('data'),))
    def on_privilege_upgrade(self, data):
        old_lv = data.get('old_lv', 0)
        new_lv = data.get('new_lv', 0)
        self.priv_lv = new_lv
        if new_lv < old_lv:
            return
        if old_lv == 0:
            red_point_name = PRIVILEGE_SETTING_TO_RED_POINT[PRIV_SHOW_BADGE] + str(self.uid)
            setting_point_name = PRIV_SHOW_BADGE + str(self.uid)
            global_data.achi_mgr.set_cur_user_archive_data(red_point_name, 0)
            global_data.emgr.update_setting_btn_red_point.emit()
            global_data.achi_mgr.set_cur_user_archive_data(setting_point_name, True)
            self.update_privilege_setting(PRIV_SHOW_BADGE, True)
            ui = global_data.ui_mgr.get_ui('PrivilegeSettingTips')
            if not ui:
                global_data.ui_mgr.show_ui('PrivilegeSettingTips', 'logic.comsys.privilege')

        def callback():
            global_data.ui_mgr.show_ui('PrivilegeLevelupUI', 'logic.comsys.privilege')

        if self.has_advance_callback('PrivilegeLevelupUI'):
            return
        if global_data.ui_mgr.get_ui('PrivilegeLevelupUI'):
            return
        self.add_advance_callback('PrivilegeLevelupUI', callback, hide_lobby_ui=False)
        lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
        if not lobby_ui:
            return
        if not self.is_running_show_advance():
            self.start_show_advance()
        global_data.emgr.privilege_level_upgrade.emit()

    @rpc_method(CLIENT_STUB, (Bool('priv_colorful_font'),))
    def update_priv_colorful_font(self, priv_colorful_font):
        self.priv_colorful_font = priv_colorful_font
        global_data.emgr.update_privilege_state.emit()
        global_data.emgr.unlock_privilege_settings.emit(5)

    @rpc_method(CLIENT_STUB, (Bool('priv_purple_id'),))
    def update_priv_purple_id(self, priv_purple_id):
        self.priv_purple_id = priv_purple_id
        global_data.emgr.update_privilege_state.emit()
        global_data.emgr.unlock_privilege_settings.emit(8)

    @rpc_method(CLIENT_STUB, (Bool('priv_share_mecha_fashion'),))
    def update_priv_share_mecha_fashion(self, priv_share_mecha_fashion):
        self.priv_share_mecha_fashion = priv_share_mecha_fashion
        global_data.emgr.update_privilege_state.emit()
        global_data.emgr.unlock_privilege_settings.emit(10)

    @rpc_method(CLIENT_STUB, (Bool('priv_red_packet'),))
    def update_priv_red_packet(self, priv_red_packet):
        self.priv_red_packet = priv_red_packet
        global_data.emgr.update_privilege_state.emit()
        global_data.emgr.unlock_privilege_settings.emit(12)

    @rpc_method(CLIENT_STUB, (Dict('week_reward'),))
    def on_privilege_week_reward(self, week_reward):
        self.on_privilege_week_reward_imp(week_reward)

    def on_privilege_week_reward_imp(self, week_reward):

        def callback():
            ui = global_data.ui_mgr.show_ui('PrivilegeWeekRewardUI', 'logic.comsys.privilege')
            ui and ui.init_privilege_week_reward(week_reward.get('priv_week_lv'), week_reward.get('priv_week_reward'))

        if self.has_advance_callback('PrivilegeWeekRewardUI'):
            return
        if global_data.ui_mgr.get_ui('PrivilegeWeekRewardUI'):
            return
        self.add_advance_callback('PrivilegeWeekRewardUI', callback)
        lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
        if not lobby_ui:
            return
        if not self.is_running_show_advance():
            self.start_show_advance()

    def try_notify_privilege_max_lv(self):
        self.call_server_method('try_notify_privilege_max_lv', ())

    def get_privilege_level(self):
        return self.priv_lv

    def get_privilege_reward_record(self):
        return self.priv_reward_record

    def get_privilege_setting(self):
        return self.priv_settings

    def get_purple_id_state(self):
        return self.priv_purple_id

    def get_colorful_font_state(self):
        return self.priv_colorful_font

    def get_privilege_data(self):
        priv_data = {'priv_lv': self.priv_lv,
           'priv_settings': self.priv_settings,
           'priv_colorful_font': self.priv_colorful_font,
           'priv_purple_id': self.priv_purple_id,
           'priv_share_mecha_fashion': self.priv_share_mecha_fashion,
           'priv_red_packet': self.priv_red_packet
           }
        return priv_data

    def get_setting_value(self, key):
        if key not in PRIV_SETTING_KEYS:
            return None
        else:
            return self.setting_to_value[key]

    def update_privilege_setting(self, setting_name, state):
        if setting_name in PRIV_SETTING_KEYS:
            self.priv_settings[setting_name] = state
            self.call_server_method('set_privilege_property', ({setting_name: state},))

    def try_send_priv_red_packet(self):
        if not self.priv_red_packet:
            return
        if not self.priv_settings.get(PRIV_RED_PACKET):
            return
        self.call_server_method('try_send_priv_red_packet', ())

    def get_priv_enjoy_free_cnt(self):
        return self.priv_enjoy_free_cnt

    @rpc_method(CLIENT_STUB, (Int('new_cnt'),))
    def update_priv_enjoy_free_cnt(self, new_cnt):
        self.priv_enjoy_free_cnt = new_cnt