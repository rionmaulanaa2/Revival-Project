# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/WeixinBindingCodeUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
import logic.comsys.common_ui.InputBox as InputBox
from logic.gutils import role_head_utils
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.activity.TeachingStepsUI import TeachingStepsUI
from logic.gcommon.const import WECHAT_BIND_ROLE_BIND_CODE_VALID_MAX_TIME
import common.utils.timer as timer
from common.cfg import confmgr
WEIXIN_BINDING_TASK_ID = '1301302'

class WeixinBindingCodeUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'activity/activity_community/i_activity_weixin_2'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'temp_bg.btn_copy.btn_major.OnClick': 'on_click_btn_copy',
       'temp_bg.lab_title.nd_auto_fit.btn_tips.OnClick': 'on_click_btn_tips'
       }
    GLOBAL_EVENT = {'receive_wechat_bind_code_event': 'on_receive_bind_code'
       }

    def on_init_panel(self, *args, **kwargs):
        super(WeixinBindingCodeUI, self).on_init_panel(*args, **kwargs)
        self.binding_code_inputbox = InputBox.InputBox(self.panel.temp_input)
        self.binding_code_inputbox.enable_input(False)
        self.set_player_head()
        self.set_player_uid()
        self.set_binding_status()
        self.set_binding_code()
        self.refresh_bind_code_timer = global_data.game_mgr.register_logic_timer(self.refresh_bind_code, interval=WECHAT_BIND_ROLE_BIND_CODE_VALID_MAX_TIME, times=-1, mode=timer.CLOCK)

    def on_finalize_panel(self):
        if self.refresh_bind_code_timer:
            global_data.game_mgr.unregister_logic_timer(self.refresh_bind_code_timer)
            self.refresh_bind_code_timer = None
        return

    def refresh_bind_code(self, *args):
        if global_data.player:
            global_data.player.call_server_method('req_wechat_bind_code', ())

    def set_player_uid(self, player_uid=None):
        if player_uid is not None:
            self.panel.lab_id_2.SetString(str(player_uid))
        else:
            self.panel.lab_id_2.SetString(str(global_data.player.uid))
        return

    def set_binding_code(self, binding_code_str=None):
        if binding_code_str is not None:
            self.binding_code_inputbox.set_text(binding_code_str)
        return

    def set_binding_status(self, status=None):
        if status is not None:
            self.panel.lab_status_2.SetString(status)
        else:
            is_binded = global_data.player.is_task_finished(WEIXIN_BINDING_TASK_ID)
            if is_binded:
                self.panel.lab_status_2.SetString(get_text_by_id(606301))
            else:
                self.panel.lab_status_2.SetString(get_text_by_id(606273))
        return

    def set_player_head(self):
        player = global_data.player
        role_head_utils.init_role_head(self.panel.temp_head, player.get_head_frame(), player.get_head_photo())

    def on_click_btn_copy(self, *args):
        import game3d
        text = self.binding_code_inputbox.get_text()
        game3d.set_clipboard_text(text)
        global_data.game_mgr.show_tip(get_text_by_id(606294))

    def on_click_btn_tips(self, *args):
        from logic.gcommon.common_const.activity_const import ACTIVITY_WEIXN_BINDING
        ui_data = confmgr.get('c_activity_config', ACTIVITY_WEIXN_BINDING, 'cUiData', default={})
        TeachingStepsUI(content_dict=ui_data)

    def on_receive_bind_code(self, bind_code):
        self.set_binding_code(str(bind_code))