# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/SearchTeammateInviteUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst
from common.const.property_const import *
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import const
import logic.comsys.common_ui.InputBox as InputBox
from logic.gutils import role_head_utils
from common.const import uiconst

class SearchTeammateInviteUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/match_teamate_invite'
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'img_search.OnClick': 'search',
       'temp_pnl.btn_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self, *args, **kargs):
        self.panel.lab_myid.setString('%s%d' % (get_text_by_id(10025), global_data.player.uid))
        self.init_event()
        self.hide_main_ui()
        global_data.emgr.show_screen_effect.emit('GaussanBlurEffect', {})
        input_box = self.panel.inputbox
        self._input_box = InputBox.InputBox(input_box, placeholder=get_text_by_id(10042))
        self._input_box.set_rise_widget(self.panel)
        self.refresh_search_friends()

    def init_event(self):
        global_data.emgr.message_refresh_friend_search += self.refresh_search_friends

    def set_info(self, battle_type, auto_flag):
        self.battle_type = battle_type
        self.auto_flag = auto_flag

    def refresh_search_friends(self):
        friends = global_data.message_data.get_search_friends()
        if friends:
            self.panel.nd_add.nd_title.setVisible(True)
            self.panel.nd_add.lab_none.setVisible(False)
        else:
            self.panel.nd_add.nd_title.setVisible(False)
            self.panel.nd_add.lab_none.setVisible(True)
        lv_friend = self.panel.lv_friend
        lv_friend.DeleteAllSubItem()
        for friend in friends:
            uid = friend.get(U_ID, 0)
            if uid == global_data.player.uid:
                continue
            head_frame = friend.get(HEAD_FRAME)
            head_photo = friend.get(HEAD_PHOTO)
            panel = lv_friend.AddTemplateItem()
            panel.lab_name.setString(friend.get(C_NAME, ''))
            role_head_utils.init_role_head(panel.temp_head, head_frame, head_photo)

            @panel.btn_add.callback()
            def OnClick(*args):
                from logic.gcommon.common_const.log_const import TEAM_MODE_FRIEND
                global_data.player.invite_frd(uid, self.battle_type, self.auto_flag, TEAM_MODE_FRIEND)

    def search(self, *args):
        text = self._input_box.get_text()
        self._input_box.set_text('')
        if self.check_is_int(text):
            frd_uid = int(text)
            frd_name = ''
        else:
            frd_uid = 0
            frd_name = str(text)
        if not global_data.player.search_friend(frd_uid, frd_name):
            global_data.game_mgr.show_tip(get_text_by_id(10041))

    def close_invite(self, *args):
        self.close()

    def check_is_int(self, text):
        try:
            int(text)
            return True
        except:
            return False

    def on_click_close_btn(self, *args):
        self.close()

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        self.show_main_ui()
        global_data.emgr.hide_screen_effect.emit('GaussanBlurEffect')
        return