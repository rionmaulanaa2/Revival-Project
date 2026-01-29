# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/DeathReadyUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import LOADING_BG_ZORDER, LOADING_ZORDER
from logic.gcommon import time_utility
from logic.gcommon.common_utils.local_text import get_text_by_id
PLAYER_ITEM_TEMPLATE = ('battle_loading/i_battle_confirm_head', )
from common.const import uiconst

class DeathReadyUI(BasePanel):
    DLG_ZORDER = LOADING_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle_loading/open_battle_confirm'
    UI_ACTION_EVENT = {'nd_content.nd_time.temp_btn.btn.OnClick': 'on_btn_call'
       }
    CNT_DOWN_UI_MUSIC = {5: 'Play_ui_matching_cd_543',
       4: 'Play_ui_matching_cd_543',
       3: 'Play_ui_matching_cd_543',
       2: 'Play_ui_matching_cd_2',
       1: 'Play_ui_matching_cd_1'
       }
    TAG = 20230602

    def on_init_panel(self):
        global_data.sound_mgr.post_event_2d_non_opt('Play_ui_matching_begin', None)
        self.matching_loop_sound_id = global_data.sound_mgr.post_event_2d_non_opt('Play_ui_matching_loop', None)
        self.process_event(True)
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('show_bg')
        self.panel.PlayAnimation('fire_loop')
        self.panel.PlayAnimation('arrow_loop')
        global_data.ui_mgr.add_ui_show_whitelist(['DeathReadyUI', 'NormalConfirmUI2'], 'DeathReadyUI')
        self.is_confirmed = False
        self.is_all_confirmed = False
        return

    def refresh_data(self):
        self.init_parameters()
        self.init_players_widget()
        self.set_confirm_btn_enable(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'gvg_match_confirm_event': self.on_match_confirm,
           'battle_match_status_event': self.update_match_status,
           'update_allow_match_ts': self.update_match_status
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        global_data.sound_mgr.stop_playing_id(self.matching_loop_sound_id)
        self.matching_loop_sound_id = None
        if not self.is_all_confirmed:
            if self.is_confirmed:
                global_data.player and global_data.player.refresh_match_start_timestamp()
        if self.is_come_back_lobby:
            global_data.ui_mgr.remove_ui_show_whitelist('DeathReadyUI')
        self.process_event(False)
        return

    def init_parameters(self):
        self.player_list_nd = (
         self.panel.nd_content.nd_blue.list_head_blue, self.panel.nd_content.nd_red.list_head_red)
        self.target_id = global_data.player.id
        self.is_come_back_lobby = True
        player = global_data.player
        self.group_data = player.group_data
        self.init_eids()
        self.last_alarm_trigger_time = -1
        self.is_confirmed = False
        self.is_all_confirmed = False

    def init_eids(self):
        self.eid_to_group_id = {}
        self.eids = []
        for group_id, value in six.iteritems(self.group_data):
            for eid in six.iterkeys(value):
                self.eid_to_group_id[eid] = group_id
                self.eids.append(eid)

        self.init_eid_to_index()

    def init_eid_to_index(self):
        self.my_group = self.eid_to_group_id.get(self.target_id)
        self.other_group = None
        self.eid_to_index = {}
        my_group_index = 0
        other_group_index = 0
        for eid in self.eids:
            if self.my_group == self.eid_to_group_id.get(eid):
                if self.target_id != eid:
                    self.eid_to_index[eid] = my_group_index
                    my_group_index += 1
            else:
                if self.other_group is None:
                    self.other_group = self.eid_to_group_id.get(eid)
                self.eid_to_index[eid] = other_group_index
                other_group_index += 1

        self.eid_to_index[self.target_id] = my_group_index
        return

    def do_hide_panel(self):
        super(DeathReadyUI, self).do_hide_panel()

    def do_show_panel(self):
        super(DeathReadyUI, self).do_show_panel()

    def init_players_widget(self):
        for nd in self.player_list_nd:
            nd.DeleteAllSubItem()

        for eid in self.eids:
            if self.target_id == eid:
                continue
            template_index = self.get_list_template_index(eid)
            list_nd = self.player_list_nd[template_index]
            item_widget = list_nd.AddTemplateItem()
            self.set_player_item(eid, item_widget)

        item_template = global_data.uisystem.load_template(PLAYER_ITEM_TEMPLATE[-1])
        list_nd = self.player_list_nd[0]
        item_widget = global_data.uisystem.create_item(item_template)
        self.set_player_item(eid, item_widget)
        list_nd.AddControl(item_widget)
        self.check_confirmed()

    def set_player_item(self, eid, item_widget):
        group_id = self.eid_to_group_id[eid]
        has_confirmed = self.group_data[group_id][eid].get('has_confirmed', False)
        self.set_confirm(item_widget, has_confirmed)

    def on_count_down(self, confirm_end_ts):
        revive_time = confirm_end_ts - time_utility.time()

        def refresh_time(pass_time):
            left_time = int(revive_time - pass_time)
            self.panel.nd_content.nd_time.lab_time.SetString(str(left_time) + 's')
            if left_time <= 5 and left_time != self.last_alarm_trigger_time:
                if left_time in self.CNT_DOWN_UI_MUSIC:
                    global_data.sound_mgr.post_event_2d_non_opt(self.CNT_DOWN_UI_MUSIC[left_time], None)
                self.panel.nd_content.nd_time.lab_time_vx.SetString(str(left_time) + 's')
                self.panel.PlayAnimation('alarm')
                self.last_alarm_trigger_time = left_time
            return

        def refresh_time_finsh--- This code section failed: ---

 159       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'panel'
           6  LOAD_ATTR             1  'nd_content'
           9  LOAD_ATTR             2  'nd_time'
          12  LOAD_ATTR             3  'lab_time'
          15  LOAD_ATTR             4  'SetString'
          18  LOAD_CONST            1  '0s'
          21  CALL_FUNCTION_1       1 
          24  POP_TOP          

 160      25  LOAD_DEREF            0  'self'
          28  LOAD_ATTR             5  'set_confirm_btn_enable'
          31  LOAD_GLOBAL           6  'False'
          34  CALL_FUNCTION_1       1 
          37  POP_TOP          

 161      38  LOAD_GLOBAL           7  'global_data'
          41  LOAD_ATTR             8  'sound_mgr'
          44  LOAD_ATTR             9  'post_event_2d_non_opt'
          47  LOAD_CONST            2  'Play_ui_matching_fail'
          50  LOAD_CONST            0  ''
          53  CALL_FUNCTION_2       2 
          56  POP_TOP          

 162      57  LOAD_CONST               '<code_object _cb>'
          60  MAKE_FUNCTION_0       0 
          63  STORE_FAST            0  '_cb'

 164      66  LOAD_DEREF            0  'self'
          69  LOAD_ATTR             0  'panel'
          72  LOAD_ATTR            11  'SetTimeOut'
          75  LOAD_CONST            4  1.0
          78  LOAD_CONST            5  'tag'
          81  LOAD_DEREF            0  'self'
          84  LOAD_ATTR            12  'TAG'
          87  CALL_FUNCTION_258   258 
          90  POP_TOP          
          91  LOAD_CONST            0  ''
          94  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_258' instruction at offset 87

        self.stop_cancel()
        if revive_time <= 0:
            refresh_time_finsh()
            return
        refresh_time(0)
        self.panel.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh, interval=0.1)

    def get_list_node_index(self, soul_id):
        return self.eid_to_index.get(soul_id, 0)

    def get_list_template_index(self, eid):
        group_id = self.eid_to_group_id.get(eid)
        if self.my_group == group_id:
            return 0
        return 1

    def get_list_node(self, eid):
        index = self.get_list_template_index(eid)
        return self.player_list_nd[index]

    def on_btn_call(self, *args):
        self.is_confirmed = True
        global_data.sound_mgr.post_event_2d_non_opt('Play_ui_matching_confirm', None)
        player = global_data.player
        if player:
            player.confirm_join_battle()
            self.set_confirm_btn_enable(False)
        return

    def on_match_confirm(self, eid):
        index = self.get_list_node_index(eid)
        item_widget = self.get_list_node(eid).GetItem(index)
        self.set_confirm(item_widget, True)
        self.check_confirmed()

    def check_confirmed(self):
        all_confirmed = True
        confirmed_num = 0
        for e_infos in six.itervalues(self.group_data):
            for eid, e_info in six.iteritems(e_infos):
                confirmed = e_info.get('has_confirmed', False)
                if confirmed:
                    confirmed_num += 1
                    if eid != self.target_id and not all_confirmed:
                        global_data.sound_mgr.post_event_2d_non_opt('Play_ui_matching_confirm_other', None)
                if not confirmed:
                    all_confirmed = False

        self.panel.nd_content.nd_time.temp_btn.lab_tips.SetString(get_text_by_id(1054).format(confirmed_num, len(self.eids)))
        if all_confirmed:
            global_data.sound_mgr.post_event_2d_non_opt('Play_ui_matching_succeed', None)
            self.is_all_confirmed = True
            self.stop_cancel()
        return

    def set_confirm_btn_enable(self, is_enable):
        self.panel.nd_content.nd_time.temp_btn.btn.SetEnable(is_enable)
        self.panel.nd_content.nd_time.temp_btn.btn.SetText(869001 if is_enable else 19766)

    def set_confirm(self, item_widget, is_confirm):
        item_widget.bar.SetSelect(is_confirm)

    def stop_cancel(self):
        self.panel.StopTimerAction()
        self.panel.stopActionByTag(self.TAG)

    def delay_close(self):
        self.stop_cancel()

        def _cb():
            global_data.ui_mgr.close_ui('DeathReadyUI')

        self.panel.SetTimeOut(1.0, _cb)

    def update_match_status(self, *args):
        if not global_data.player.is_matching and not self.is_all_confirmed:
            global_data.game_mgr.show_tip(get_text_by_id(1058), True)
            self.close()