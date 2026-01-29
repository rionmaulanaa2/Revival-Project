# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfo/CommunicateWidget.py
from __future__ import absolute_import
import game3d
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.gcommon.const as const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.entities.Battle import Battle
from logic.gcommon.common_const.voice_const import CLOSE_CHANNEL, TEAM_CHANNEL, GROUP_CHANNEL, NEARBY_FACTION_CHANNEL, TYPE_VOICE_IDX, TYPE_MIC_IDX
RES_HEAR_PHONIC = 'gui/ui_res_2/battle/icon/icon_sound_open.png'
RES_HEAR_MUTE = 'gui/ui_res_2/battle/icon/icon_sound_close.png'
RES_SPEAK_PHONIC = 'gui/ui_res_2/battle/icon/icon_speak_open.png'
RES_SPEAK_MUTE = 'gui/ui_res_2/battle/icon/icon_speak_close.png'

class CommunicateBaseWidget(object):
    TIPS_CD = 5

    def __init__(self, nd):
        self.tips_time = -1
        self.panel = nd
        self.is_group = False
        self.setting_key_speaker = 'ccmini_battle_speaker'
        self.setting_key_mic = 'ccmini_battle_mic'
        self.last_speaker_indx = -1
        self.last_mic_indx = -1
        self.is_faction_room = bool(global_data.player and global_data.player.is_custom_faction_room())
        self.init_click_event()
        self.init_team_ccmini()
        self.process_event(True)

    def process_event(self, is_bind):
        pass

    def destroy(self):
        self.process_event(False)
        self.panel = None
        return

    def init_click_event(self):
        pass

    def init_team_ccmini(self):
        if self.is_faction_room:
            self.set_ccmini_status_faction_room()
            self.init_sound_and_speak_list_faction_room()
        else:
            self.set_ccmini_status()

        @self.panel.btn_sound.callback()
        def OnClick(btn, touch):
            self.panel.list_speak.setVisible(False)
            list_sound = self.panel.list_sound
            is_show = list_sound.isVisible()
            list_sound.setVisible(not is_show)
            px, py = self.panel.nd_custom.GetPosition()
            pw, ph = self.panel.nd_custom.GetContentSize()
            w, h = list_sound.GetContentSize()
            if py < ph + h:
                list_sound.SetPosition('50%0', '100%165')
            else:
                list_sound.SetPosition('50%0', -9)
            if global_data.mouse_mgr:
                global_data.mouse_mgr.add_cursor_hide_count('CommunicateBaseWidget.list_speak')
                if is_show:
                    global_data.mouse_mgr.add_cursor_hide_count('CommunicateBaseWidget.list_sound')
                else:
                    global_data.mouse_mgr.add_cursor_show_count('CommunicateBaseWidget.list_speak')
            for index, item in enumerate(reversed(list_sound.GetAllItem())):

                @item.btn_sound.callback()
                def OnClick(btn, touch, index=index):
                    if self.is_faction_room:
                        self.refresh_voice_info_faction_room(index)
                    else:
                        self.refresh_voice_info(index)
                    self.close_all_list()

            return True

        @self.panel.btn_speak.callback()
        def OnClick(btn, touch):
            self.panel.list_sound.setVisible(False)
            self.panel.StopTimerAction()
            speak_list = self.panel.list_speak
            is_show = speak_list.isVisible()
            speak_list.setVisible(not is_show)
            px, py = self.panel.nd_custom.GetPosition()
            pw, ph = self.panel.nd_custom.GetContentSize()
            w, h = speak_list.GetContentSize()
            if py < ph + h:
                speak_list.SetPosition('50%0', '100%165')
            else:
                speak_list.SetPosition('50%0', -9)
            if global_data.mouse_mgr:
                global_data.mouse_mgr.add_cursor_hide_count('CommunicateBaseWidget.list_sound')
                if is_show:
                    global_data.mouse_mgr.add_cursor_hide_count('CommunicateBaseWidget.list_speak')
                else:
                    global_data.mouse_mgr.add_cursor_show_count('CommunicateBaseWidget.list_speak')
            for index, item in enumerate(reversed(speak_list.GetAllItem())):

                @item.btn_speak.callback()
                def OnClick(btn, touch, index=index):
                    if self.is_faction_room:
                        self.refresh_speak_info_faction_room(index)
                    else:
                        self.refresh_speak_info(index)
                    self.close_all_list()

            return True

        self.panel.btn_speak.set_sound_enable(False)

    def close_all_list(self):
        self.panel.list_sound.setVisible(False)
        self.panel.list_speak.setVisible(False)
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_hide_count('CommunicateBaseWidget.list_sound')
            global_data.mouse_mgr.add_cursor_hide_count('CommunicateBaseWidget.list_speak')

    def refresh_speak_info(self, index, is_force=False):
        if not global_data.player:
            return
        if index == self.last_mic_indx and not is_force:
            return
        if index == CLOSE_CHANNEL:
            global_data.ccmini_mgr.stop_capture_ex(const.TEAM_SESSION_ID)
            global_data.ccmini_mgr.stop_capture_ex(const.TEAM_ALL_SESSION_ID)
        elif index >= TEAM_CHANNEL:
            global_data.ccmini_mgr.set_team_keys(self.setting_key_speaker, self.setting_key_mic)
            global_data.player.req_team_login_session_data()
            if index >= GROUP_CHANNEL:
                global_data.player.req_group_login_session_data()
            self.try_open_speak(index)
            self.refresh_setting(self.setting_key_speaker, index)
            if not self.check_permision():
                index = CLOSE_CHANNEL
                global_data.ccmini_mgr.stop_capture_ex(const.TEAM_SESSION_ID)
                global_data.ccmini_mgr.stop_capture_ex(const.TEAM_ALL_SESSION_ID)
        self.refresh_setting(self.setting_key_mic, index)

    def refresh_speak_info_faction_room(self, index, is_force=False):
        if not global_data.player:
            return
        if index == self.last_mic_indx and not is_force:
            return
        if index == CLOSE_CHANNEL:
            global_data.ccmini_mgr.stop_capture_ex(const.TEAM_SESSION_ID)
            global_data.ccmini_mgr.stop_capture_ex(const.TEAM_ALL_SESSION_ID)
            global_data.ccmini_mgr.stop_capture_ex(const.NEAR_SESSION_ID)
        elif index == NEARBY_FACTION_CHANNEL:
            if not self.check_permision():
                self.request_permission(index)
            else:
                global_data.ccmini_mgr.start_capture(const.NEAR_SESSION_ID)
        self.update_speak_ui_faction_room(index)
        self.last_mic_indx = index

    def refresh_setting(self, key, value):
        if key == self.setting_key_mic:
            self.update_speak_ui(value)
            self.last_mic_indx = value
        elif key == self.setting_key_speaker:
            self.update_voice_ui(value)
            self.last_speaker_indx = value
        global_data.message_data.set_seting_inf(key, value)

    def refresh_voice_info(self, index, is_force=False):
        if not global_data.player:
            return
        if index == self.last_speaker_indx and not is_force:
            return
        team_mic = self.get_team_mic()
        if index == CLOSE_CHANNEL:
            global_data.ccmini_mgr.mute_playback(const.TEAM_SESSION_ID, 1)
            global_data.ccmini_mgr.stop_capture_ex(const.TEAM_SESSION_ID)
            global_data.ccmini_mgr.mute_playback(const.TEAM_ALL_SESSION_ID, 1)
            global_data.ccmini_mgr.stop_capture_ex(const.TEAM_ALL_SESSION_ID)
            self.refresh_setting(self.setting_key_mic, index)
        elif index in [TEAM_CHANNEL, GROUP_CHANNEL]:
            global_data.ccmini_mgr.set_team_keys(self.setting_key_speaker, self.setting_key_mic)
            global_data.player.req_team_login_session_data()
            if index == GROUP_CHANNEL:
                global_data.player.req_group_login_session_data()
            else:
                global_data.ccmini_mgr.mute_playback(const.TEAM_ALL_SESSION_ID, 1)
                global_data.ccmini_mgr.stop_capture_ex(const.TEAM_ALL_SESSION_ID)
            if team_mic:
                self.try_open_speak(index)
                mic_index = index
                if not self.check_permision():
                    mic_index = CLOSE_CHANNEL
                    global_data.ccmini_mgr.stop_capture_ex(const.TEAM_SESSION_ID)
                    global_data.ccmini_mgr.stop_capture_ex(const.TEAM_ALL_SESSION_ID)
                self.refresh_setting(self.setting_key_mic, mic_index)
        self.refresh_setting(self.setting_key_speaker, index)

    def refresh_voice_info_faction_room(self, index, is_force=False):
        if not global_data.player:
            return
        if index == self.last_speaker_indx and not is_force:
            return
        global_data.ccmini_mgr.mute_playback(const.TEAM_SESSION_ID, 1)
        global_data.ccmini_mgr.stop_capture_ex(const.TEAM_SESSION_ID)
        global_data.ccmini_mgr.mute_playback(const.TEAM_ALL_SESSION_ID, 1)
        global_data.ccmini_mgr.stop_capture_ex(const.TEAM_ALL_SESSION_ID)
        if index == CLOSE_CHANNEL:
            global_data.ccmini_mgr.mute_playback(const.NEAR_SESSION_ID, 1)
        elif index == NEARBY_FACTION_CHANNEL:
            global_data.ccmini_mgr.mute_playback(const.NEAR_SESSION_ID, 0)
        self.update_voice_ui_faction_room(index)
        self.last_speaker_indx = index

    def update_voice_ui(self, index):
        if self.is_faction_room:
            self.update_voice_ui_faction_room(index)
            return
        res_path = RES_HEAR_PHONIC if index else RES_HEAR_MUTE
        self.panel.btn_sound.img.SetDisplayFrameByPath('', res_path)
        txt_id = ''
        if index == TEAM_CHANNEL:
            txt_id = 80127
        elif index == GROUP_CHANNEL:
            txt_id = 19612
        self.panel.lab_sound.SetString(txt_id)

    def update_speak_ui(self, index):
        if self.is_faction_room:
            self.update_speak_ui_faction_room(index)
            return
        res_path = RES_SPEAK_PHONIC if index else RES_SPEAK_MUTE
        self.panel.btn_speak.img.SetDisplayFrameByPath('', res_path)
        txt_id = ''
        if index == TEAM_CHANNEL:
            txt_id = 80127
        elif index == GROUP_CHANNEL:
            txt_id = 19612
        self.panel.lab_speak.SetString(txt_id)

    def update_voice_ui_faction_room(self, index):
        res_path = RES_HEAR_PHONIC if index else RES_HEAR_MUTE
        self.panel.btn_sound.img.SetDisplayFrameByPath('', res_path)
        txt_id = ''
        if index == NEARBY_FACTION_CHANNEL:
            txt_id = 18023
        self.panel.lab_sound.SetString(txt_id)

    def update_speak_ui_faction_room(self, index):
        res_path = RES_SPEAK_PHONIC if index else RES_SPEAK_MUTE
        self.panel.btn_speak.img.SetDisplayFrameByPath('', res_path)
        txt_id = ''
        if index == NEARBY_FACTION_CHANNEL:
            txt_id = 18023
        self.panel.lab_speak.SetString(txt_id)

    def on_battle_status_changed(self, status):
        if status in [Battle.BATTLE_STATUS_FIGHT, Battle.BATTLE_STATUS_PARACHUTE]:
            if self.is_faction_room:
                self.set_ccmini_status_faction_room()
            else:
                self.set_ccmini_status()

    def on_team_change(self, *args):
        self.set_ccmini_status(True)

    def scene_on_teammate_change(self, unit_id):
        if global_data.cam_lplayer and global_data.cam_lplayer.id == unit_id:
            self.set_ccmini_status(True)

    def set_ccmini_status(self, is_force=False):
        if not (self.panel and self.panel.isValid()):
            return
        self.is_group = False
        if global_data.player:
            self.is_group = global_data.player.get_team_size() > 0
        if self.is_group:
            self.setting_key_speaker = 'ccmini_battle_group_speaker'
            self.setting_key_mic = 'ccmini_battle_group_mic'
        else:
            self.setting_key_speaker = 'ccmini_battle_speaker'
            self.setting_key_mic = 'ccmini_battle_mic'
        global_data.ccmini_mgr.set_team_keys(self.setting_key_speaker, self.setting_key_mic)
        team_nd = self.panel.list_sound.GetItem(1)
        team_nd and team_nd.btn_sound.SetEnable(self.is_group)
        team_nd and team_nd.btn_lock.setVisible(not self.is_group)
        team_nd = self.panel.list_speak.GetItem(1)
        team_nd and team_nd.btn_speak.SetEnable(self.is_group)
        team_nd and team_nd.btn_lock.setVisible(not self.is_group)
        team_speaker = global_data.message_data.get_seting_inf(self.setting_key_speaker) or CLOSE_CHANNEL
        team_mic = self.get_team_mic()
        self.refresh_voice_info(team_speaker, is_force)
        self.refresh_speak_info(team_mic, is_force)

    def set_ccmini_status_faction_room(self, is_force=False):
        voice_index = CLOSE_CHANNEL
        self.refresh_voice_info_faction_room(voice_index, is_force)
        speak_index = CLOSE_CHANNEL
        self.refresh_speak_info_faction_room(speak_index, is_force)

    def init_sound_and_speak_list_faction_room(self):
        if not (self.panel and self.panel.isValid()):
            return
        self.panel.list_sound.DeleteAllSubItem()
        self.panel.list_sound.SetInitCount(2)
        near_item = self.panel.list_sound.GetItem(0)
        close_item = self.panel.list_sound.GetItem(1)
        close_item.btn_sound.img.SetDisplayFrameByPath('', RES_HEAR_MUTE)
        near_item.btn_sound.img.SetDisplayFrameByPath('', RES_HEAR_PHONIC)
        if global_data.is_pc_mode:
            close_item.btn_sound.lab_name.SetString('')
            near_item.btn_sound.lab_name.SetString(18023)
        else:
            close_item.btn_sound.lab_sound.SetString('')
            near_item.btn_sound.lab_sound.SetString(18023)
        self.panel.list_speak.DeleteAllSubItem()
        self.panel.list_speak.SetInitCount(2)
        near_item = self.panel.list_speak.GetItem(0)
        close_item = self.panel.list_speak.GetItem(1)
        close_item.btn_speak.img.SetDisplayFrameByPath('', RES_SPEAK_MUTE)
        near_item.btn_speak.img.SetDisplayFrameByPath('', RES_SPEAK_PHONIC)
        if global_data.is_pc_mode:
            close_item.btn_speak.lab_name.SetString('')
            near_item.btn_speak.lab_name.SetString(18023)
        else:
            close_item.btn_speak.lab_speak.SetString('')
            near_item.btn_speak.lab_speak.SetString(18023)

    def check_permision(self):
        return game3d.get_platform() == game3d.PLATFORM_WIN32 or global_data.ccmini_mgr.check_microphone_permission()

    def first_check_mic(self):
        if game3d.get_platform() != game3d.PLATFORM_WIN32:
            if not global_data.ccmini_mgr.check_microphone_permission():
                global_data.ccmini_mgr.stop_capture_ex(const.TEAM_SESSION_ID)
                global_data.ccmini_mgr.stop_capture_ex(const.TEAM_ALL_SESSION_ID)
                self.update_speak_ui(CLOSE_CHANNEL)
            else:
                global_data.ccmini_mgr.start_capture(const.TEAM_SESSION_ID)
                global_data.ccmini_mgr.start_capture(const.TEAM_ALL_SESSION_ID)
                self.update_speak_ui(TEAM_CHANNEL)

    def try_open_speak(self, index):
        if not self.check_permision():
            self.request_permission(index)
        else:
            import time
            cur_time = time.time()
            if cur_time - self.tips_time > self.TIPS_CD:
                global_data.game_mgr.show_tip(get_text_by_id(11016))
                self.tips_time = cur_time

    def request_permission(self, index):
        global_data.ccmini_mgr.request_mic_premission()
        global_data.ccmini_mgr.stop_capture_ex(const.TEAM_SESSION_ID)
        global_data.ccmini_mgr.stop_capture_ex(const.TEAM_ALL_SESSION_ID)
        global_data.ccmini_mgr.stop_capture_ex(const.NEAR_SESSION_ID)

        def tick_callback(pass_time, index=index):
            if self.check_permision():
                global_data.ccmini_mgr.start_capture(const.TEAM_SESSION_ID)
                global_data.ccmini_mgr.start_capture(const.TEAM_ALL_SESSION_ID)
                global_data.ccmini_mgr.start_capture(const.NEAR_SESSION_ID)
                self.refresh_setting(self.setting_key_mic, index)
                self.refresh_setting(self.setting_key_speaker, index)
                self.panel.StopTimerAction()

        self.panel.TimerAction(tick_callback, 6.0, interval=0.3)

    def get_team_mic(self):
        team_mic = global_data.message_data.get_seting_inf(self.setting_key_mic) or CLOSE_CHANNEL
        if team_mic and game3d.get_platform() != game3d.PLATFORM_WIN32 and not global_data.ccmini_mgr.check_microphone_permission():
            team_mic = CLOSE_CHANNEL
        return team_mic

    def show_cd_progress(self, from_percent, to_percent, time):
        self.panel.progress_cd.setVisible(True)
        self.panel.progress_cd.SetPercentage(from_percent)
        self.panel.progress_cd.SetPercentageWithAni(to_percent, time, end_cb=self.end_send_cd)

    def end_send_cd(self):
        self.panel.progress_cd.setVisible(False)

    def on_enter_observe(self, target):
        pass

    def trigger_btn_speaker(self):
        self.panel.btn_speak.OnClick(None)
        return

    def trigger_btn_sound(self):
        self.panel.btn_sound.OnClick(None)
        return


class CommunicateWidget(CommunicateBaseWidget):

    def init_click_event(self):

        @self.panel.callback()
        def OnClick(btn, touch):
            self.close_all_list()

        self.panel.set_sound_enable(False)

    def process_event(self, is_bind):
        event_infos = {'show_fight_chat_send_cd_progress_event': self.show_cd_progress,
           'scene_observed_player_setted_event': self.on_enter_observe,
           'on_battle_status_changed': self.on_battle_status_changed,
           'player_join_team_event': self.on_team_change,
           'player_leave_team_event': self.on_team_change,
           'scene_on_teammate_change': self.scene_on_teammate_change,
           'player_voice_mic_set_change': self.update_voice_mic_status
           }
        if is_bind:
            global_data.emgr.bind_events(event_infos)
        else:
            global_data.emgr.unbind_events(event_infos)

    def update_voice_mic_status(self, select_key, type_id, index):
        if type_id == TYPE_VOICE_IDX and select_key == self.setting_key_speaker:
            self.refresh_voice_info(index)
        elif type_id == TYPE_MIC_IDX and select_key == self.setting_key_mic:
            self.refresh_speak_info(index)

    def on_enter_observe(self, target):
        if global_data.player and global_data.player.logic:
            from logic.gutils import judge_utils
            is_judge = judge_utils.is_ob()
            is_in_global_spectate = global_data.player and global_data.player.is_in_global_spectate()
            from logic.gutils.team_utils import is_all_death
            teammate = global_data.player.logic.ev_g_groupmate()
            all_death = is_all_death(teammate)
            if is_judge or all_death or is_in_global_spectate:
                self.panel.btn_speak.setVisible(False)
                self.panel.btn_sound.setVisible(False)
                global_data.ccmini_mgr.stop_capture(const.TEAM_SESSION_ID)
                global_data.ccmini_mgr.stop_capture(const.TEAM_ALL_SESSION_ID)


class CommunicateWidgetPC(CommunicateBaseWidget):

    def init_click_event(self):
        pass

    def process_event(self, is_bind):
        event_infos = {'scene_observed_player_setted_event': self.on_enter_observe,
           'on_battle_status_changed': self.on_battle_status_changed,
           'player_join_team_event': self.on_team_change,
           'player_leave_team_event': self.on_team_change,
           'scene_on_teammate_change': self.scene_on_teammate_change,
           'player_voice_mic_set_change': self.update_voice_mic_status
           }
        if is_bind:
            global_data.emgr.bind_events(event_infos)
        else:
            global_data.emgr.unbind_events(event_infos)

    def update_voice_mic_status(self, select_key, type_id, index):
        if type_id == TYPE_VOICE_IDX and select_key == self.setting_key_speaker:
            self.refresh_voice_info(index)
        elif type_id == TYPE_MIC_IDX and select_key == self.setting_key_mic:
            self.refresh_speak_info(index)

    def on_enter_observe(self, target):
        if global_data.player and global_data.player.logic:
            from logic.gutils import judge_utils
            is_judge = judge_utils.is_ob()
            is_in_global_spectate = global_data.player and global_data.player.is_in_global_spectate()
            from logic.gutils.team_utils import is_all_death
            teammate = global_data.player.logic.ev_g_groupmate()
            all_death = is_all_death(teammate)
            if is_judge or all_death or is_in_global_spectate:
                self.panel.btn_speak.setVisible(False)
                self.panel.btn_sound.setVisible(False)
                global_data.ccmini_mgr.stop_capture(const.TEAM_SESSION_ID)
                global_data.ccmini_mgr.stop_capture(const.TEAM_ALL_SESSION_ID)