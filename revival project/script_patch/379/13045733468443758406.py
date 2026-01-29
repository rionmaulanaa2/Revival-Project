# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SettingWidget/SoundSettingWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_utils.local_text import get_cur_voice_lang, get_cur_text_lang
from logic.gcommon.common_const.voice_lang_data import voice_lang_data
from logic.gcommon.common_const.lang_data import code_2_showname
from common.cfg import confmgr
from logic.gcommon.common_const.voice_const import CLOSE_CHANNEL, TEAM_CHANNEL, GROUP_CHANNEL
import logic.gcommon.const as const
from .SettingWidgetBase import SettingWidgetBase
import game3d

class SoundSettingWidget(SettingWidgetBase):

    def __init__(self, panel, parent):
        super(SoundSettingWidget, self).__init__(panel, parent)

    def on_init_panel(self, **kwargs):
        self.on_init_voice_mic_data()
        self.init_sound_setting(self.panel)
        self.update_player_voice_select()

    def on_init_voice_mic_data(self):
        self.all_player_voice_mic_idx = 0
        self.team_voice_mic_idx = 1
        self.player_list_nd = ['nd_player_music', 'nd_player_music_team']
        self.sub_panel_list = ['lv_player_sound', 'lv_player_mic']
        self.voice_idx = 0
        self.mic_idx = 1
        self.player_setting_datas = [[({'txt_id': 2383,'setting_key': 'ccmini_battle_speaker'}, {'txt_id': 2384,'setting_key': 'ccmini_battle_speaker'}), ({'txt_id': 2386,'setting_key': 'ccmini_battle_mic'}, {'txt_id': 2387,'setting_key': 'ccmini_battle_mic'})], [({'txt_id': 2383,'setting_key': 'ccmini_battle_group_speaker'}, {'txt_id': 2385,'setting_key': 'ccmini_battle_group_speaker'}, {'txt_id': 2384,'setting_key': 'ccmini_battle_group_speaker'}), ({'txt_id': 2386,'setting_key': 'ccmini_battle_group_mic'}, {'txt_id': 2388,'setting_key': 'ccmini_battle_group_mic'}, {'txt_id': 2387,'setting_key': 'ccmini_battle_group_mic'})]]

    def on_exit_page(self, **kwargs):
        super(SoundSettingWidget, self).on_exit_page()
        self.sync_setting_data()

    def on_recover_default(self, **kwargs):
        self.convert_sound_seting()
        self.recover_voice_and_mic_setting()
        default_voice_lang = global_data.ui_mgr.get_default_voice_lang(get_cur_text_lang())
        if default_voice_lang != get_cur_voice_lang():
            self._try_switch_to_voice_lang(default_voice_lang)

    def sync_setting_data(self):
        if global_data.player:
            global_data.player.save_settings_to_file()

    def init_sound_setting(self, page):
        sound_panel_list = ['sound_main', 'sound_3', 'sound_1', 'sound_2', 'sound_4']
        seting_keys = [uoc.SOUND_VOLUME_MAIN_KEY, uoc.SOUND_VOLUME_SFX_KEY, uoc.SOUND_VOLUME_VO_KEY, uoc.SOUND_VOLUME_MUSIC_KEY, uoc.SOUND_VOLUME_ANCHOR_VO_KEY]
        isenable_keys = [uoc.SOUND_VOLUME_MAIN_ISENABLE_KEY, uoc.SOUND_VOLUME_SFX_ISENABLE_KEY, uoc.SOUND_VOLUME_VO_ISENABLE_KEY, uoc.SOUND_VOLUME_MUSIC_ISENABLE_KEY, uoc.SOUND_VOLUME_ANCHOR_VO_ISENABLE_KEY]
        functions = [global_data.sound_mgr.set_main_volume, global_data.sound_mgr.set_sfx_volume, global_data.sound_mgr.set_vo_volume, global_data.sound_mgr.set_music_volume, global_data.sound_mgr.set_anchor_vo_volume]

        def refresh_all_btn():
            main_value_isenable = global_data.player.get_setting(uoc.SOUND_VOLUME_MAIN_ISENABLE_KEY)
            for index in range(len(sound_panel_list)):
                panel = getattr(page, sound_panel_list[index])
                is_enable = global_data.player.get_setting(isenable_keys[index])
                flag = main_value_isenable and is_enable
                panel.temp_choose.choose.setVisible(flag)

        self.soundseting_refresh_all_btn = refresh_all_btn

        def refresh_all_slider():
            for index in range(len(sound_panel_list)):
                panel = getattr(page, sound_panel_list[index])
                val = global_data.player.get_setting(seting_keys[index])
                panel.slider.setPercent(val)

        self.soundseting_refresh_all_slider = refresh_all_slider

        def init_slider(panel, seting_key, is_enabel_key, set_function):

            @panel.temp_choose.btn.callback()
            def OnClick(*args):
                if is_enabel_key != uoc.SOUND_VOLUME_MAIN_ISENABLE_KEY and not global_data.player.get_setting(uoc.SOUND_VOLUME_MAIN_ISENABLE_KEY):
                    global_data.game_mgr.show_tip(get_text_by_id(2201))
                    return
                flag = panel.temp_choose.choose.isVisible()
                flag = not flag
                global_data.player.write_setting(is_enabel_key, flag, True)
                if flag:
                    val = global_data.player.get_setting(seting_key)
                    set_function(val)
                else:
                    set_function(0)
                self.soundseting_refresh_all_btn()

            @panel.slider.unique_callback()
            def OnPercentageChanged(ctrl, slider):
                if not global_data.player.get_setting(uoc.SOUND_VOLUME_MAIN_ISENABLE_KEY) or not global_data.player.get_setting(is_enabel_key):
                    val = global_data.player.get_setting(seting_key)
                    panel.slider.setPercent(val)
                    return
                val = slider.getPercent()
                global_data.player.write_setting(seting_key, val, True)
                if global_data.player.get_setting(is_enabel_key):
                    set_function(int(val))

        for index in range(len(sound_panel_list)):
            panel = getattr(page, sound_panel_list[index])
            init_slider(panel, seting_keys[index], isenable_keys[index], functions[index])

        global_data.sound_mgr.reset_volume()
        self.soundseting_refresh_all_btn()
        self.soundseting_refresh_all_slider()
        if global_data.player and global_data.player.is_in_battle():
            self.panel.nd_voice.setVisible(False)
            self.panel.nd_lobby_music.setVisible(False)
        else:
            self._refresh_voice_lang(page)
            self._refresh_lobby_music(page)

    def convert_sound_seting(self):
        page = self.panel
        seting_keys = [
         uoc.SOUND_VOLUME_MAIN_KEY, uoc.SOUND_VOLUME_SFX_KEY, uoc.SOUND_VOLUME_VO_KEY, uoc.SOUND_VOLUME_MUSIC_KEY, uoc.SOUND_VOLUME_ANCHOR_VO_KEY]
        isenable_keys = [uoc.SOUND_VOLUME_MAIN_ISENABLE_KEY, uoc.SOUND_VOLUME_SFX_ISENABLE_KEY, uoc.SOUND_VOLUME_VO_ISENABLE_KEY, uoc.SOUND_VOLUME_MUSIC_ISENABLE_KEY, uoc.SOUND_VOLUME_ANCHOR_VO_ISENABLE_KEY]
        for index in range(len(seting_keys)):
            is_enable = global_data.player.get_default_setting(isenable_keys[index])
            global_data.player.write_setting(isenable_keys[index], is_enable, True)
            val = global_data.player.get_default_setting(seting_keys[index])
            global_data.player.write_setting(seting_keys[index], val, True)

        global_data.sound_mgr.reset_volume()
        self.soundseting_refresh_all_btn()
        self.soundseting_refresh_all_slider()

    def _refresh_voice_lang(self, page):
        voice_list = page.lv_voice_list
        voice_list.SetInitCount(len(voice_lang_data))
        allItems = voice_list.GetAllItem()
        cur_voice_lang = get_cur_voice_lang()
        for i, item in enumerate(allItems):
            item_data = voice_lang_data.get(i, {})
            voice_lan_text_id = item_data.get('cLangShow')
            item.tf_lang.SetString(get_text_by_id(voice_lan_text_id))
            if i == cur_voice_lang:
                item.btn_language.SetSelect(True)
            else:
                item.btn_language.SetSelect(False)

            @item.btn_language.callback()
            def OnClick(btn, touch, voice_code=i):
                self._try_switch_to_voice_lang(voice_code)

    def _refresh_lobby_music(self, page):
        music_list = page.lv_music_list
        music_list.SetInitCount(1)
        allItems = music_list.GetAllItem()
        for i, item in enumerate(allItems):
            item.tf_lang.SetString(610812)

            @item.btn_language.callback()
            def OnClick(btn, touch):
                self._try_switch_lobby_music()

        self.refresh_cur_bgm()

    def refresh_cur_bgm(self):
        from logic.gcommon.item.item_const import DEFAULT_LOBBY_BGM
        from logic.gutils import item_utils
        cur_bgm_item_no = global_data.player.get_lobby_bgm() or DEFAULT_LOBBY_BGM
        self.panel.nd_lobby_music.sound_title.title.SetString(''.join([get_text_by_id(12185), '\xe2\x80\x94\xe2\x80\x94', item_utils.get_lobby_item_name(cur_bgm_item_no)]))
        music_list = self.panel.lv_music_list
        item = music_list.GetItem(0)
        if item:
            from logic.gutils.red_point_utils import check_bgm_rp
            item.temp_red.setVisible(check_bgm_rp())

    def jump_to_switch_lobby_music(self, music_idx):
        if not self.parent or global_data.player and global_data.player.is_in_battle():
            return
        else:
            ui = self._try_switch_lobby_music()
            if ui:
                self.parent.panel.content_bar.page.ScrollToBottom()
                if music_idx is not None:
                    ui.panel.list_item.LocatePosByItem(music_idx)
            return

    def _try_switch_lobby_music(self):
        if global_data.player and global_data.player.is_in_battle():
            return None
        else:
            return global_data.ui_mgr.show_ui('LobbyMusicUI', 'logic.comsys.lobby')

    def _try_switch_to_voice_lang(self, voice_code):
        page = self.panel
        if global_data.player and global_data.player.is_in_battle():
            return
        global_data.emgr.should_login_channel_event.emit()
        if voice_code == get_cur_voice_lang():
            return

        def cb():
            self.switch_to_voice_lang(voice_code)
            global_data.emgr.language_select_event.emit()

        cur_text_lang = get_cur_text_lang()
        player = global_data.player
        if player and not player.in_local_battle():
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            SecondConfirmDlg2().confirm(content=get_text_by_id(3107), confirm_text=get_text_local_content(3108), confirm_callback=cb)
        else:
            cb()

    def switch_to_voice_lang(self, voice_code):
        global_data.ui_mgr.change_lang(get_cur_text_lang(), voice_code)

    def check_permision(self):
        return game3d.get_platform() == game3d.PLATFORM_WIN32 or global_data.ccmini_mgr.check_microphone_permission()

    def request_permission(self):
        global_data.ccmini_mgr.request_mic_premission()
        global_data.ccmini_mgr.stop_capture_ex(const.TEAM_SESSION_ID)
        global_data.ccmini_mgr.stop_capture_ex(const.TEAM_ALL_SESSION_ID)

    def update_player_voice_select(self):
        list_nd = self.player_list_nd
        setting_datas = self.player_setting_datas
        for index in range(len(list_nd)):
            panel_nd = getattr(self.panel, list_nd[index])
            list_data = setting_datas[index]
            for i in range(len(self.sub_panel_list)):
                list_panel = getattr(panel_nd, self.sub_panel_list[i])
                list_panel.SetInitCount(len(list_data[i]))
                data = list_data[i]
                allItems = list_panel.GetAllItem()
                for j, item in enumerate(allItems):
                    item_data = data[j]
                    voice_lan_text_id = item_data.get('txt_id')
                    select_key = item_data.get('setting_key')
                    item.tf_lang.SetString(get_text_by_id(voice_lan_text_id))
                    select_val = global_data.message_data.get_seting_inf(select_key) or CLOSE_CHANNEL
                    need_select = False
                    if index == self.all_player_voice_mic_idx:
                        if j == 1 and select_val == GROUP_CHANNEL:
                            need_select = True
                        elif j == 0 and select_val == CLOSE_CHANNEL:
                            need_select = True
                        else:
                            need_select = False
                    elif j == select_val:
                        need_select = True
                    else:
                        need_select = False
                    item.btn_language.SetSelect(need_select)

                    @item.btn_language.callback()
                    def OnClick(btn, touch, allItems=allItems, setting_type=index, sub_idx=i, select_key=select_key, select_val=j):
                        self.try_switch_player_voice_setting(allItems, setting_type, sub_idx, select_key, select_val)

    def try_switch_player_voice_setting(self, allItems, setting_type, sub_idx, select_key, select_idx):
        if select_idx != CLOSE_CHANNEL and sub_idx == self.mic_idx:
            if not self.check_permision():
                self.request_permission()
                return
        for i in range(len(allItems)):
            item = allItems[i]
            if item and select_idx == i:
                item.btn_language.SetSelect(True)
                set_val = CLOSE_CHANNEL
                if setting_type == self.all_player_voice_mic_idx:
                    if select_idx == 0:
                        set_val = CLOSE_CHANNEL
                    elif select_idx == 1:
                        set_val = GROUP_CHANNEL
                else:
                    set_val = select_idx
                global_data.message_data.set_seting_inf(select_key, set_val)
                global_data.emgr.player_voice_mic_set_change.emit(select_key, sub_idx, set_val)
                self.update_voice_mic_btn_state(setting_type, sub_idx, select_key)
            else:
                item.btn_language.SetSelect(False)

    def update_voice_mic_btn_state(self, setting_type, sub_idx, select_key):
        list_nd = self.player_list_nd
        setting_datas = self.player_setting_datas
        for index in range(len(list_nd)):
            if index == setting_type:
                panel_nd = getattr(self.panel, list_nd[index])
                list_data = setting_datas[index]
                for i in range(len(self.sub_panel_list)):
                    if i != sub_idx:
                        list_panel = getattr(panel_nd, self.sub_panel_list[i])
                        allItems = list_panel.GetAllItem()
                        val = global_data.message_data.get_seting_inf(select_key) or CLOSE_CHANNEL
                        data = list_data[i]
                        change_key = data[0].get('setting_key')
                        if sub_idx == 0:
                            mic_key = global_data.message_data.get_seting_inf(change_key) or CLOSE_CHANNEL
                            if val == CLOSE_CHANNEL:
                                self.update_voice_mic_select_btn(allItems, change_key, val, val)
                            elif val == TEAM_CHANNEL:
                                if mic_key:
                                    self.update_voice_mic_select_btn(allItems, change_key, val, val)
                            elif val == GROUP_CHANNEL:
                                if mic_key:
                                    if self.team_voice_mic_idx == setting_type:
                                        self.update_voice_mic_select_btn(allItems, change_key, val, val)
                                    else:
                                        self.update_voice_mic_select_btn(allItems, change_key, val - 1, val)
                        elif sub_idx == 1 and (val == GROUP_CHANNEL or val == TEAM_CHANNEL):
                            for j, item in enumerate(allItems):
                                set_val = j
                                if setting_type == self.team_voice_mic_idx:
                                    set_val = j
                                elif val == GROUP_CHANNEL and j == 1:
                                    set_val = GROUP_CHANNEL
                                if set_val == val:
                                    item.btn_language.SetSelect(True)
                                    global_data.message_data.set_seting_inf(change_key, set_val)
                                else:
                                    item.btn_language.SetSelect(False)

    def update_voice_mic_select_btn(self, allItems, set_key, select_id, set_val):
        for j, item in enumerate(allItems):
            if j == select_id:
                item.btn_language.SetSelect(True)
                global_data.message_data.set_seting_inf(set_key, set_val)
            else:
                item.btn_language.SetSelect(False)

    def recover_voice_and_mic_setting(self):
        list_nd = self.player_list_nd
        setting_datas = self.player_setting_datas
        for index in range(len(list_nd)):
            panel_nd = getattr(self.panel, list_nd[index])
            list_data = setting_datas[index]
            for i in range(len(self.sub_panel_list)):
                list_panel = getattr(panel_nd, self.sub_panel_list[i])
                data = list_data[i]
                allItems = list_panel.GetAllItem()
                for j, item in enumerate(allItems):
                    item_data = data[j]
                    select_key = item_data.get('setting_key')
                    if j == CLOSE_CHANNEL:
                        item.btn_language.SetSelect(True)
                        global_data.message_data.set_seting_inf(select_key, CLOSE_CHANNEL)
                        global_data.emgr.player_voice_mic_set_change.emit(select_key, i, CLOSE_CHANNEL)
                    else:
                        item.btn_language.SetSelect(False)