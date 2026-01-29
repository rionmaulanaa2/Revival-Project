# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/TeamHall/TeamReleaseUI.py
from __future__ import absolute_import
import six
import common.utilities
from common.cfg import confmgr
from logic.gcommon.common_utils.text_utils import check_review_words
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gcommon.common_const import chat_const
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN, PLAY_TYPE_DEATH, PLAY_TYPE_PVE, DEFAULT_BATTLE_TID, DEFAULT_DEATH_TID, DEFAULT_PVE_TID
from logic.gcommon.common_const.pve_const import NORMAL_DIFFICUTY, DIFFICUTY_LIST, DIFFICULTY_TEXT_LIST
from logic.gutils import season_utils
from logic.gutils import template_utils
import logic.comsys.common_ui.InputBox as InputBox
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
import six_ex
PLAY_TYPE_2_BATTLE_TID = {PLAY_TYPE_CHICKEN: DEFAULT_BATTLE_TID,
   PLAY_TYPE_DEATH: DEFAULT_DEATH_TID,
   PLAY_TYPE_PVE: DEFAULT_PVE_TID
   }

class TeamReleaseUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'lobby/team_hall_release'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'bg'
    UI_ACTION_EVENT = {'btn_send.btn_common_big.OnClick': 'on_send',
       'btn_cancel.btn_common_big.OnClick': 'close',
       'btn_change.btn_common_big.OnClick': 'on_change'
       }

    def on_init_panel(self, *args, **kwargs):
        super(TeamReleaseUI, self).on_init_panel()
        self.init_attr(*args, **kwargs)
        self.reset()
        self.init_options()

    def init_attr(self, *args, **kwargs):
        self.message_data = global_data.message_data
        self.click_cb_dict = {}
        self.is_change = kwargs.get('is_change', False)
        self.battle_type = kwargs.get('battle_type')
        self._name_input_box = None
        self._send_callback = None
        self.setting_key = ''
        return

    def reset(self):
        self.cur_team_num = 1
        self.team_battle_tid = self.message_data.get_seting_inf('{}team_battle_tid'.format(self.setting_key))
        self.team_dan_limit = self.message_data.get_seting_inf('{}team_dan_limit'.format(self.setting_key))
        self.team_need_voice = self.message_data.get_seting_inf('{}team_need_voice'.format(self.setting_key))
        self.team_share_clan = self.message_data.get_seting_inf('team_share_clan')
        unlock_chapter_list = global_data.player.get_unlock_chapter() if global_data.player else [1]
        max_unlock_chapter = max(unlock_chapter_list)
        self.team_chapter = max_unlock_chapter
        self.team_difficulty = global_data.player.get_chapter_unlock_difficulty(self.team_chapter) if global_data.player else NORMAL_DIFFICUTY
        invite_player_msg = self.message_data.get_seting_inf('invite_player_msg')
        self.invite_player_msg = get_text_by_id(invite_player_msg) if isinstance(invite_player_msg, int) else invite_player_msg

    def on_finalize_panel(self):
        pass

    def set_send_callback(self, callback):
        self._send_callback = callback

    def save_setting_inf(self):
        filter_keys = [
         self.setting_key, self.setting_key, self.setting_key, '', '', self.setting_key, self.setting_key]
        keys = ['team_battle_tid', 'team_dan_limit', 'team_need_voice', 'team_share_clan', 'invite_player_msg', 'team_chapter', 'team_difficulty']
        for i, key in enumerate(keys):
            value = getattr(self, key)
            save_key = '{}{}'.format(filter_keys[i], key)
            if value != self.message_data.get_seting_inf(save_key):
                self.message_data.set_seting_inf(save_key, value)

    def init_options(self):
        self.init_other_widget()
        mode_options = []
        conf = confmgr.get('c_battle_mode_show_config', default={})
        for show_type, show_type_conf in six.iteritems(conf):
            is_show = show_type_conf.get('iShowInChoose', False)
            battle_type = PLAY_TYPE_2_BATTLE_TID.get(show_type_conf['iPlayType'], None)
            if is_show and battle_type:
                option = {'name': show_type_conf['cModeName'],'attr_value': battle_type}
                mode_options.append(option)

        self.init_option_list('team_battle_tid', self.panel.nd_mode, mode_options)
        mode_options = [{'name': 2150,'attr_value': 1}]
        self.init_option_list('cur_team_num', self.panel.nd_num, mode_options)
        dan_list = season_utils.get_dan_list()
        mode_options = [ {'name': season_utils.get_dan_lv_name(dan),'attr_value': dan} for dan in dan_list ]
        self.init_option_list('team_dan_limit', self.panel.nd_rank, mode_options)
        chapter_conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content')
        mode_options = [ {'name': get_text_by_id(conf.get('title_text')),'attr_value': int(chapter)} for chapter, conf in six_ex.items(chapter_conf) ]
        self.init_option_list('team_chapter', self.panel.nd_chapter, mode_options)
        mode_options = [ {'name': get_text_by_id(DIFFICULTY_TEXT_LIST[difficulty]),'attr_value': difficulty} for difficulty in DIFFICUTY_LIST ]
        self.init_option_list('team_difficulty', self.panel.nd_difficulty, mode_options)
        choose = self.panel.nd_mic
        template_utils.init_radio_group(choose)

        @choose.choose_1.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                self.team_need_voice = 1

        @choose.choose_2.unique_callback()
        def OnSelect(btn, choose, trigger_event):
            if choose and trigger_event:
                self.team_need_voice = 0

        if self.team_need_voice:
            choose.choose_1.btn.OnClick(None, False)
        else:
            choose.choose_2.btn.OnClick(None, False)
        if self.battle_type in [DEFAULT_PVE_TID, DEFAULT_BATTLE_TID, DEFAULT_DEATH_TID]:
            self.click_cb_dict['team_battle_tid'](0, self.battle_type)
        return

    def init_option_list(self, attr_name, nd, option_list):

        @nd.btn_mode.unique_callback()
        def OnClick(btn, touch):
            if not nd.mode_list.isVisible():
                nd.mode_list.setVisible(True)
                nd.btn_mode.img_icon.setRotation(180)
            else:
                nd.mode_list.setVisible(False)
                nd.btn_mode.img_icon.setRotation(0)

        def call_back(index, value=None):
            if value:
                option = None
                for _option in option_list:
                    if _option['attr_value'] == value:
                        option = _option
                        break

            else:
                option = option_list[index]
            attr_value = option['attr_value']
            if attr_name == 'team_battle_tid':
                if attr_value == DEFAULT_PVE_TID:
                    self.panel.nd_chapter.setVisible(True)
                    self.panel.nd_difficulty.setVisible(True)
                    self.panel.nd_num.setVisible(False)
                else:
                    self.panel.nd_chapter.setVisible(False)
                    self.panel.nd_difficulty.setVisible(False)
                    self.panel.nd_num.setVisible(True)
            elif attr_name == 'team_chapter':
                unlock_chapter_list = global_data.player.get_unlock_chapter() if global_data.player else [1]
                if attr_value not in unlock_chapter_list:
                    global_data.game_mgr.show_tip(get_text_by_id(541))
                    return
                unlock_difficulty = global_data.player.get_chapter_unlock_difficulty(attr_value) if global_data.player else NORMAL_DIFFICUTY
                self.team_chapter = attr_value
                if self.click_cb_dict.get('team_difficulty'):
                    self.click_cb_dict['team_difficulty'](0, unlock_difficulty)
            elif attr_name == 'team_difficulty':
                unlock_difficulty = global_data.player.get_chapter_unlock_difficulty(self.team_chapter) if global_data.player else NORMAL_DIFFICUTY
                if attr_value > unlock_difficulty:
                    global_data.game_mgr.show_tip(get_text_by_id(511))
                    return
            setattr(self, attr_name, attr_value)
            nd.btn_mode.SetText(option['name'])
            nd.mode_list.setVisible(False)
            nd.btn_mode.img_icon.setRotation(0)
            return

        template_utils.init_common_choose_list_2(nd.mode_list, nd.btn_mode.img_icon, option_list, call_back, max_height=354)
        call_back(0, value=getattr(self, attr_name))
        self.click_cb_dict[attr_name] = call_back
        return

    def init_other_widget(self):

        def callback(*args):
            self.invite_player_msg = self._name_input_box.get_text()

        self._name_input_box = InputBox.InputBox(self.panel.input_box, max_length=chat_const.CHAT_INVITE_MSG_MAX_BYTE_COUNT, placeholder=get_text_by_id(11048), need_sp_length_func=True, input_callback=callback, detach_callback=callback)
        self._name_input_box.set_rise_widget(self.panel)
        if self.invite_player_msg:
            self._name_input_box.set_text(self.invite_player_msg)
        nd = self.panel.btn_share_to_crew

        @nd.btn.callback()
        def OnClick(btn, touch):
            choose = nd.choose.isVisible()
            nd.choose.setVisible(not choose)
            self.team_share_clan = choose or 1 if 1 else 0

        nd.choose.setVisible(True if self.team_share_clan else False)
        self.panel.btn_cancel.setVisible(False)
        self.panel.btn_send.setVisible(False)
        self.panel.btn_change.setVisible(False)
        if self.is_change:
            self.panel.btn_cancel.setVisible(True)
            self.panel.btn_change.setVisible(True)
        else:
            self.panel.btn_send.setVisible(True)

    def on_send(self, *args):
        msg = self.invite_player_msg
        flag, msg = check_review_words(msg)
        if msg and not flag:
            global_data.player.notify_client_message((get_text_by_id(11032),))
            return
        if global_data.player.get_lv() < chat_const.SEND_WORLD_MSG_MIN_LV:
            global_data.player.notify_client_message((get_text_by_id(13123).format(lv=chat_const.SEND_WORLD_MSG_MIN_LV),))
            return
        self.save_setting_inf()
        public_info = {'battle_type': self.team_battle_tid,
           'limit_dan': self.team_dan_limit,
           'need_voice': bool(self.team_need_voice),
           'share_to_clan': bool(self.team_share_clan),
           'declaration': msg
           }
        if self.team_battle_tid == DEFAULT_PVE_TID:
            public_info['chapter'] = self.team_chapter
            public_info['difficulty'] = self.team_difficulty
        global_data.player.create_public_team(public_info)
        global_data.player.set_match_info(self.team_battle_tid, global_data.player.get_self_auto_match())
        if self._send_callback:
            self._send_callback()
        self.close()

    def on_change(self, *args):
        msg = self.invite_player_msg
        flag, msg = check_review_words(msg)
        if msg and not flag:
            global_data.player.notify_client_message((get_text_by_id(11032),))
            return
        self.save_setting_inf()
        new_public_info = {'battle_type': self.team_battle_tid,
           'limit_dan': self.team_dan_limit,
           'need_voice': bool(self.team_need_voice),
           'share_to_clan': bool(self.team_share_clan),
           'declaration': msg
           }
        if self.team_battle_tid == DEFAULT_PVE_TID:
            new_public_info['chapter'] = self.team_chapter
            new_public_info['difficulty'] = self.team_difficulty
        global_data.player.modify_public_team(new_public_info)
        global_data.player.set_match_info(self.team_battle_tid, global_data.player.get_self_auto_match())
        self.close()


class TeamFilterUI(TeamReleaseUI):
    PANEL_CONFIG_NAME = 'lobby/team_hall_filter'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'bg'
    UI_ACTION_EVENT = {'btn_reset.btn_common_big.OnClick': 'on_reset',
       'btn_confirm.btn_common_big.OnClick': 'on_confirm'
       }

    def init_attr(self, *args, **kwargs):
        super(TeamFilterUI, self).init_attr(*args, **kwargs)
        self.setting_key = 'filter_'

    def on_init_panel(self, *args, **kwargs):
        super(TeamFilterUI, self).on_init_panel()

    def init_other_widget(self):
        pass

    def on_reset(self, *args):
        self.reset()
        self.init_options()

    def on_confirm(self, *args):
        from logic.comsys.lobby.TeamHall.TeamHallList import REQUEST_NUM
        self.save_setting_inf()
        global_data.player.request_public_teams(self.team_battle_tid, 0, REQUEST_NUM)
        self.close()