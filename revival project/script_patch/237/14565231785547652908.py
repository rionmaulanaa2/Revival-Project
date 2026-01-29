# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/CreditReportResultFail.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils.role_head_utils import init_role_head
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gutils.scene_utils import is_in_lobby

class CreditReportResultFail(WindowMediumBase):
    PANEL_CONFIG_NAME = 'role/report_result_fail'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'btn_sure.btn_common.OnClick': 'close',
       'btn_report.btn_common.OnClick': '_go_to_feedback'
       }
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
        return

    def on_init_panel(self):
        super(CreditReportResultFail, self).on_init_panel()
        cur_scene = global_data.game_mgr.scene
        if not is_in_lobby(cur_scene.scene_type):
            self.add_hide_count()

    def _go_to_feedback(self, *args):
        import game3d
        if game3d.get_app_name() == 'com.netease.g93natw':
            from logic.comsys.feedback import echoes
            echoes.show_feedback_view(echoes.LOBBY)
            return
        if hasattr(game3d, 'open_gm_web_view'):
            global_data.player.get_custom_service_token()
            game3d.open_gm_web_view('')
        else:
            data = {'methodId': 'ntOpenGMPage',
               'refer': ''
               }
            global_data.channel.extend_func_by_dict(data)

    def _lobby_scene_event(self, pause_flag):
        if not pause_flag:
            self.clear_show_count_dict()

    def on_finalize_panel(self):
        self.set_custom_close_func(None)
        return