# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/CreditReportResultSuccess.py
from __future__ import absolute_import
from logic.gutils.role_head_utils import init_role_head
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gutils.scene_utils import is_in_lobby

class CreditReportResultSuccess(WindowMediumBase):
    PANEL_CONFIG_NAME = 'role/report_result_success'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'lobby_scene_pause_event': '_lobby_scene_event'
       }

    def show_info(self, info):
        char_name = info.get('char_name', '')
        head_frame = info.get('head_frame', None)
        head_photo = info.get('head_photo', None)
        uid = info.get('uid', '')
        if G_IS_NA_USER:
            self.panel.nd_detail.lab_id.SetString(str(uid))
        else:
            show_id = int(uid)
            show_id -= global_data.uid_prefix
            self.panel.nd_detail.lab_id.SetString(str(show_id))
        self.panel.nd_detail.lab_name.SetString(char_name)
        init_role_head(self.panel.nd_detail.temp_role, head_frame, head_photo)
        self.panel.nd_detail.lab_point.setVisible(False)
        self.panel.nd_detail.lab_minus.setVisible(False)
        self.panel.nd_detail.lab_surplus.setVisible(False)
        return

    def on_init_panel(self):
        super(CreditReportResultSuccess, self).on_init_panel()
        cur_scene = global_data.game_mgr.scene
        if not is_in_lobby(cur_scene.scene_type):
            self.add_hide_count()

    def _lobby_scene_event(self, pause_flag):
        if not pause_flag:
            self.clear_show_count_dict()

    def on_finalize_panel(self):
        self.set_custom_close_func(None)
        return