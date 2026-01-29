# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/exercise_ui/ExerciseCommandUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, BASE_LAYER_ZORDER
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from common.const import uiconst

class ExerciseCommandUI(MechaDistortHelper, BasePanel):
    PANEL_CONFIG_NAME = 'battle_train/fight_controller'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_distance.OnClick': '_on_click_dist'
       }
    HOT_KEY_FUNC_MAP = {'switch_command_distance': '_on_click_dist_PC'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'switch_command_distance': {'node': 'nd_controller.temp_pc'}}

    def on_init_panel(self, *args, **kwargs):
        super(ExerciseCommandUI, self).on_init_panel()
        self.init_ui()
        self.process_event(True)

    def init_ui(self):
        self.panel.btn_distance.SetSelect(True)
        self.panel.btn_distance.img_choose.setVisible(True)
        if global_data.is_pc_mode:
            self.panel.nd_controller.SetPosition('0%9', '100%-37')
        else:
            self.panel.nd_controller.SetPosition('0%9', '100%-6')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_camera_player_setted_event': self.on_cam_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_cam_player_setted(self):
        self.on_ctrl_target_changed()

    def _on_click_dist(self, *args, **kwargs):
        is_select = self.panel.btn_distance.GetSelect()
        self.panel.btn_distance.SetSelect(not is_select)
        self.panel.btn_distance.img_choose.setVisible(not is_select)
        self._switch_distance(not is_select)

    def _on_click_dist_PC(self, *args, **kwargs):
        from logic.vscene.parts.ctrl.InputMockHelper import trigger_ui_btn_event
        trigger_ui_btn_event('ExerciseCommandUI', 'btn_distance')

    def _switch_distance(self, is_show_dist):
        ui = global_data.ui_mgr.get_ui('ExerciseDistanceUI')
        if not ui:
            return
        ui.is_show_dist = is_show_dist
        for _, target_info in six.iteritems(ui.target_dict):
            nd = target_info[0]
            if nd:
                nd.nd_distance.setVisible(is_show_dist)

    def on_finalize_panel(self):
        self.process_event(False)
        super(ExerciseCommandUI, self).on_finalize_panel()