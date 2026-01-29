# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/homeland/ImgShareConfirmUI.py
from __future__ import absolute_import
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER, UI_TYPE_CONFIRM
from common.const.property_const import *
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import role_head_utils
from logic.gcommon import const
from common.const import uiconst

class ImgShareConfirmUI(BasePanel):
    PANEL_CONFIG_NAME = 'home_system/share_invite'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_CONFIRM
    UI_ACTION_EVENT = {'btn_refuse.btn_common.OnClick': 'cancel',
       'btn_agree.btn_common.OnClick': 'confirm',
       'btn_close.OnClick': 'close_share'
       }
    GLOBAL_EVENT = {'update_lobby_puppet_count': '_on_lobby_puppet_count'
       }

    def on_init_panel(self):
        self._cb = None
        self.count_down_timer = None
        self._start_count_time = 0
        self._limit_count_down_time = 10
        self.panel.PlayAnimation('invite_show')
        self._init_refuse_text = self.panel.btn_refuse.btn_common.GetText()
        self.panel.lab_title.SetString(611617)
        self.panel.lab_recruit.SetString(611618)
        return

    def on_finalize_panel(self):
        self.destrot_count_down_timer()

    def destrot_count_down_timer(self):
        if self.count_down_timer:
            global_data.game_mgr.unregister_logic_timer(self.count_down_timer)
        self.count_down_timer = None
        return

    def init_count_down_timer(self):
        from common.utils.timer import CLOCK
        self._start_count_time = time.time()
        self.destrot_count_down_timer()
        self.count_down_timer = global_data.game_mgr.register_logic_timer(self.update_count_down, interval=1, times=self._limit_count_down_time, mode=CLOCK)
        self.update_count_down()

    def update_count_down(self):
        left_time = int(self._limit_count_down_time - (time.time() - self._start_count_time))
        if left_time <= 0:
            self.panel.btn_refuse.btn_common.SetText(self._init_refuse_text)
            self.cancel()
        else:
            self.panel.btn_refuse.btn_common.SetText(self._init_refuse_text + '(%ds)' % left_time)

    def set_share_info(self, extra_info, cb):
        self._cb = cb
        char_name = extra_info.get('char_name', '')
        head_frame = extra_info.get('head_frame')
        head_photo = extra_info.get('head_photo')
        uid = extra_info.get('uid')
        self.name.setString(unpack_text(char_name))
        role_head_utils.init_role_head(self.panel.head, head_frame, head_photo)
        nd = self.panel.head

        @nd.callback()
        def OnClick(*args):
            if not uid:
                return
            ui = global_data.ui_mgr.get_ui('PlayerInfoUI')
            if ui:
                ui.clear_show_count_dict()
                ui.hide_main_ui()
            else:
                ui = global_data.ui_mgr.show_ui('PlayerInfoUI', 'logic.comsys.role')
            ui.refresh_by_uid(uid)

        role_head_utils.set_role_dan(self.panel.temp_tier, extra_info.get('dan_info'))
        self.init_count_down_timer()

    def cancel(self, *args):
        self._cb and self._cb(False)
        self.close()

    def confirm(self, *args):
        self._cb and self._cb(True)
        self.close()

    def close_share(self, *args):
        self._cb and self._cb(False)
        self.close()

    def _on_lobby_puppet_count(self, count):
        if not global_data.player:
            return
        if not global_data.player.is_sharer_in_lobby():
            self.close()