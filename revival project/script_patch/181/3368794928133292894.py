# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityKizunaAIInviteLink.py
from __future__ import absolute_import
import game3d
from logic.gcommon import const
from logic.gutils import template_utils
from logic.gutils import role_head_utils
from logic.gutils import online_state_utils
from logic.gutils.share_utils import generate_spec_enlist_code, spec_enlist_code_2_uid
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase

class ActivityKizunaAIInviteLink(WindowSmallBase):
    PANEL_CONFIG_NAME = 'activity/activity_202109/kizuna/new_player/i_activity_recruit_kizuna_tips'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    TEMPLATE_NODE_NAME = 'temp_window'
    TITLE_TEXT_ID = 607803
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'message_on_players_detail_inf': 'on_players_detail_inf',
       'message_on_spec_enlist_verify': 'on_enlist_verify'
       }
    OPEN_SOUND_NAME = 'menu_shop'
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_finalize_panel(self):
        pass

    def on_init_panel(self, *args, **kwargs):
        super(ActivityKizunaAIInviteLink, self).on_init_panel()
        from data import c_recruit_data
        import logic.comsys.common_ui.InputBox as InputBox
        self._cur_show_uid = 0
        invite_code = kwargs.get('invite_code', '')
        enlist_from_uid = global_data.player.get_spec_enlist_from_uid()
        if enlist_from_uid:
            invite_code = generate_spec_enlist_code(enlist_from_uid)
        self.set_invite_code(invite_code)
        self._input_box = None
        self.panel.lab_player_me.SetString(19151)
        role_head_utils.init_role_head(self.panel.temp_head_me, global_data.player.get_head_frame(), global_data.player.get_head_photo())
        from logic.gcommon.common_const.activity_const import ACTIVITY_KIZUNA_AI_RECRUIT
        from common.cfg import confmgr
        conf = confmgr.get('c_activity_config', ACTIVITY_KIZUNA_AI_RECRUIT, 'cUiData')
        newbee_gift = conf.get('enlist_verify_gift', 0)
        template_utils.init_common_reward_list(self.panel.list_items, newbee_gift)
        self.panel.lab_player.SetString('')
        if global_data.player.has_spec_enlist_verify_gift():
            self.panel.nd_middle_01.setVisible(False)
            self.panel.nd_middle_02.setVisible(True)
            if self.invite_code:
                message_data = global_data.message_data
                uid = spec_enlist_code_2_uid(self.invite_code)
                if not G_IS_NA_USER:
                    if uid < global_data.uid_prefix:
                        uid += global_data.uid_prefix
                if not message_data.is_friend(uid):
                    global_data.player.req_add_friend(uid)
        else:
            self.panel.nd_middle_01.setVisible(True)
            self.panel.nd_middle_02.setVisible(False)

        @self.panel.btn_confirm.btn_common.unique_callback()
        def OnClick(btn, touch):
            if not self._cur_show_uid:
                return
            global_data.player.try_spec_enlist_from_code(self.invite_code)

        def input_callback(*args, **kwargs):
            text = self._input_box.get_text()
            if not text:
                return
            self.request_players_info(text)

        self._input_box = InputBox.InputBox(self.panel.temp_input, placeholder='', input_callback=input_callback)
        self._input_box.set_rise_widget(self.panel)

        @self.panel.btn_paste.btn_common.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils import deeplink_utils
            text = ''
            if G_IS_NA_USER:
                player_id = deeplink_utils.get_deep_link_param(deeplink_utils.DEEP_LINK_ADD_FRIEND)
                if player_id:
                    try:
                        group = player_id.split('_')
                        text = group[0]
                    except:
                        pass

            else:
                text = game3d.get_clipboard_text()
                text = text if text else deeplink_utils.TEMP_CLIPBOARD_TEXT
            if not text:
                return
            self._input_box.set_text(text)
            self.request_players_info(text)

        @self.panel.btn_get.btn_common.unique_callback()
        def OnClick(btn, touch):
            if not self._cur_show_uid:
                return
            self.close()
            global_data.player.receive_spec_enlist_verify_gift()

        self.refresh_btn()
        if invite_code:
            self.request_players_info(invite_code)
        return

    def set_invite_code(self, invite_code):
        try:
            uid = int(invite_code, 16)
        except:
            uid = -1

        if uid < 0:
            self.invite_code = ''
            return
        self.invite_code = invite_code

    def refresh_btn(self):
        enable = True if self._cur_show_uid else False
        self.panel.btn_confirm.btn_common.SetEnable(enable)

    def on_enlist_verify(self):
        message_data = global_data.message_data
        self.on_players_detail_inf()
        if self._cur_show_uid and not message_data.is_friend(self._cur_show_uid):
            global_data.player.req_add_friend(self._cur_show_uid)
        global_data.player.receive_spec_enlist_verify_gift()
        self.close()

    def request_players_info(self, invite_code):
        self.set_invite_code(invite_code)
        if not self.invite_code:
            return
        uid = spec_enlist_code_2_uid(invite_code)
        if not G_IS_NA_USER:
            if uid < global_data.uid_prefix:
                uid += global_data.uid_prefix
        message_data = global_data.message_data
        if not message_data.has_player_inf(uid):
            global_data.player.request_players_detail_inf([uid])
        else:
            self.on_players_detail_inf()

    def on_players_detail_inf(self, *argv):
        from logic.gutils.role_head_utils import set_gray
        from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
        if not self.invite_code:
            return
        else:
            uid = spec_enlist_code_2_uid(self.invite_code)
            if uid < 0:
                return
            if not G_IS_NA_USER:
                if uid < global_data.uid_prefix:
                    uid += global_data.uid_prefix
            message_data = global_data.message_data
            player_info = message_data.get_player_inf(const.PLAYER_INFO_DETAIL, uid)
            if not player_info:
                return
            self._cur_show_uid = uid
            self.refresh_btn()
            friend_online_state = message_data.get_player_online_state()
            state = int(friend_online_state.get(int(uid), const.STATE_OFFLINE))
            text_id, color = ui_utils.get_online_inf(state)
            other_name = player_info.get('char_name', '')
            self.panel.lab_player.SetString(other_name)
            self.panel.lab_player.SetColor(color)
            role_head_utils.init_role_head(self.panel.temp_head, player_info.get('head_frame', None), player_info.get('head_photo', None))
            online = not online_state_utils.is_not_online(state)
            role_head_utils.set_gray(self.panel.temp_head, not online)
            self.panel.nd_middle_01.setVisible(False)
            self.panel.nd_middle_02.setVisible(False)
            if global_data.player.has_spec_enlist_verify_gift():
                self.panel.nd_middle_02.setVisible(True)
                self.panel.lab_tips.SetString(get_text_by_id(10016, {'playername': other_name}))
                lv = global_data.player.get_lv()
                self.panel.btn_get.btn_common.SetEnable(lv >= 5)
            else:
                self.panel.nd_middle_01.setVisible(True)
            return