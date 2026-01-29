# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyVoiceWidget.py
from __future__ import absolute_import
RES_HEAR_PHONIC = 'gui/ui_res_2/common/icon/on_hear.png'
RES_HEAR_MUTE = 'gui/ui_res_2/common/icon/no_hear.png'
RES_SPEAK_PHONIC = 'gui/ui_res_2/common/icon/speak.png'
RES_SPEAK_MUTE = 'gui/ui_res_2/common/icon/no_speak.png'
import game3d
import logic.gcommon.const as gconst
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gcommon.common_const.voice_const import CLOSE_CHANNEL, TEAM_CHANNEL, GROUP_CHANNEL, TYPE_VOICE_IDX, TYPE_MIC_IDX
from common.audio.ccmini_mgr import LOBBY_TEAM_SPEAKER, LOBBY_TEAM_MIC

class LobbyVoiceWidget(BaseUIWidget):
    ACT_TAG = 190917

    def __init__(self, parent_ui, panel):
        self.global_events = {'player_join_team_event': self.on_join_team,
           'player_leave_team_event': self.on_leave_team,
           'player_voice_mic_set_change': self.update_voice_mic_status,
           'refresh_mic_info': self.update_widget
           }
        super(LobbyVoiceWidget, self).__init__(parent_ui, panel)
        self.team_laba_key = LOBBY_TEAM_SPEAKER
        self.team_mic_key = LOBBY_TEAM_MIC
        self.init_widget()
        self.init_ui_event()

    def on_click_btn_laba(self, *args):
        self.panel.list_speak.setVisible(False)
        list_sound = self.panel.list_sound
        is_show = list_sound.isVisible()
        list_sound.setVisible(not is_show)
        for index, item in enumerate(reversed(list_sound.GetAllItem())):

            @item.btn_sound.callback()
            def OnClick(btn, touch, index=index):
                self.refresh_laba_info(index)
                self.panel.list_sound.setVisible(False)
                self.panel.list_speak.setVisible(False)

    def refresh_laba_info(self, index, need_check_mic=True, only_show=False):
        team_laba = index
        global_data.ccmini_mgr.reset_engine()
        global_data.ccmini_mgr.mute_playback(gconst.TEAM_SESSION_ID, 1 if team_laba == CLOSE_CHANNEL else 0)
        self.update_laba_ui(team_laba)
        global_data.message_data.set_seting_inf(self.team_laba_key, team_laba)
        if need_check_mic:
            old_mic = global_data.message_data.get_seting_inf(self.team_mic_key)
            if index == CLOSE_CHANNEL:
                global_data.message_data.set_seting_inf(self.team_mic_key, team_laba)
            elif old_mic != CLOSE_CHANNEL and old_mic != index:
                global_data.message_data.set_seting_inf(self.team_mic_key, team_laba)
            new_val = global_data.message_data.get_seting_inf(self.team_mic_key)
            self.refresh_mic_info(new_val, need_check_laba=False)

    def destroy(self):
        self.btn_voice = None
        self.btn_speak = None
        self.speak_tips = None
        super(LobbyVoiceWidget, self).destroy()
        return

    def init_ui_event(self):
        self.btn_voice.BindMethod('OnClick', self.on_click_btn_laba)
        self.btn_speak.BindMethod('OnClick', self.on_click_btn_mic)
        self.btn_speak.set_sound_enable(False)

    def init_event(self):
        super(LobbyVoiceWidget, self).init_event()

    def on_join_team(self, *args):
        global_data.ccmini_mgr.set_team_keys(self.team_laba_key, self.team_mic_key)
        global_data.player.req_team_login_session_data()
        self.panel.nd_voice.setVisible(True)
        self.refresh_team_mic_tips_show()
        team_laba = global_data.message_data.get_seting_inf(self.team_laba_key)
        team_mic = global_data.message_data.get_seting_inf(self.team_mic_key)
        if not self.check_permision():
            team_mic = 0
        self.update_laba_ui(team_laba)
        self.update_mic_ui(team_mic)

    def on_leave_team(self, *args):
        self.panel.nd_voice.setVisible(False)

    def init_widget(self):
        global_data.ccmini_mgr.set_team_keys(self.team_laba_key, self.team_mic_key)
        global_data.player and global_data.player.req_team_login_session_data()
        self.btn_voice = self.panel.btn_voice
        self.btn_speak = self.panel.btn_speak
        self.speak_tips = self.panel.nd_tips
        team_info = global_data.player and global_data.player.get_team_info()
        self.parent.nd_voice.setVisible(bool(team_info))
        self.update_widget()
        self.speak_tips.lab_tips.SetString(get_text_by_id(11015))

    def update_widget(self):
        team_laba = global_data.message_data.get_seting_inf(self.team_laba_key)
        team_mic = global_data.message_data.get_seting_inf(self.team_mic_key)
        if not global_data.player:
            return
        if global_data.player.is_in_team() and not self.check_permision():
            team_mic = 0
        self.update_laba_ui(team_laba)
        self.update_mic_ui(team_mic)

    def refresh_team_mic_tips_show(self):
        team_mic = global_data.message_data.get_seting_inf(self.team_mic_key)
        if global_data.player.is_in_team() and not self.check_permision():
            team_mic = 0
        self.speak_tips.setVisible(not team_mic)
        if not team_mic:
            self.speak_tips.SetTimeOut(3, lambda : self.speak_tips.setVisible(False), tag=self.ACT_TAG)
        else:
            self.speak_tips.stopActionByTag(self.ACT_TAG)

    def update_laba_ui(self, team_mic):
        res_path = RES_HEAR_PHONIC if team_mic else RES_HEAR_MUTE
        self.btn_voice.img_voice.SetDisplayFrameByPath('', res_path)
        txt_id = ''
        if team_mic == TEAM_CHANNEL:
            txt_id = 80127
        elif team_mic == GROUP_CHANNEL:
            txt_id = 19612
        self.panel.lab_voice.SetString(txt_id)

    def update_mic_ui(self, team_mic):
        res_path = RES_SPEAK_PHONIC if team_mic else RES_SPEAK_MUTE
        self.btn_speak.img_speak.SetDisplayFrameByPath('', res_path)
        if team_mic:
            self.speak_tips.setVisible(False)
            self.speak_tips.stopActionByTag(self.ACT_TAG)
        txt_id = ''
        if team_mic == TEAM_CHANNEL:
            txt_id = 80127
        elif team_mic == GROUP_CHANNEL:
            txt_id = 19612
        self.panel.lab_speak.SetString(txt_id)

    def check_permision(self):
        return game3d.get_platform() == game3d.PLATFORM_WIN32 or global_data.ccmini_mgr.check_microphone_permission()

    def on_click_btn_mic(self, *args):
        self.panel.list_sound.setVisible(False)
        self.panel.StopTimerAction()
        speak_list = self.panel.list_speak
        is_show = speak_list.isVisible()
        speak_list.setVisible(not is_show)
        for index, item in enumerate(reversed(speak_list.GetAllItem())):

            @item.btn_speak.callback()
            def OnClick(btn, touch, index=index):
                self.refresh_mic_info(index)
                self.panel.list_sound.setVisible(False)
                self.panel.list_speak.setVisible(False)

    def refresh_mic_info(self, index, need_check_laba=True):
        self.panel.StopTimerAction()
        team_mic = index
        if team_mic:
            if not self.check_permision():
                self.request_permission()
            else:
                global_data.game_mgr.show_tip(get_text_by_id(11016))
                global_data.ccmini_mgr.start_capture(gconst.TEAM_SESSION_ID)
        else:
            global_data.ccmini_mgr.stop_capture(gconst.TEAM_SESSION_ID)
        self.update_mic_ui(team_mic)
        global_data.message_data.set_seting_inf(self.team_mic_key, team_mic)
        if need_check_laba:
            old_mic = global_data.message_data.get_seting_inf(self.team_laba_key)
            if index != CLOSE_CHANNEL:
                global_data.message_data.set_seting_inf(self.team_laba_key, team_mic)
            elif old_mic != CLOSE_CHANNEL and team_mic != CLOSE_CHANNEL and old_mic != index:
                global_data.message_data.set_seting_inf(self.team_laba_key, team_mic)
            new_val = global_data.message_data.get_seting_inf(self.team_laba_key)
            self.refresh_laba_info(new_val, need_check_mic=False)
        global_data.emgr.refresh_mic_info.emit()

    def request_permission(self):
        global_data.ccmini_mgr.request_mic_premission()
        global_data.ccmini_mgr.stop_capture(gconst.TEAM_SESSION_ID)

        def tick_callback(*args):
            if self.check_permision():
                global_data.ccmini_mgr.start_capture(gconst.TEAM_SESSION_ID)
                self.update_mic_ui(1)
                global_data.message_data.set_seting_inf(self.team_mic_key, 1)
                self.panel.StopTimerAction()

        self.panel.TimerAction(tick_callback, 6.0, interval=0.3)

    def update_voice_mic_status(self, select_key, type_id, index):
        if type_id == TYPE_VOICE_IDX and select_key == self.team_laba_key:
            self.refresh_laba_info(index)
        elif type_id == TYPE_MIC_IDX and select_key == self.team_mic_key:
            self.refresh_mic_info(index)