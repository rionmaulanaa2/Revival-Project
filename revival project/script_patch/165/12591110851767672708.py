# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/EndSceneUIBase.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.comsys.video.VideoRecord import VideoRecord
from logic.comsys.video.video_record_utils import V_STATE_PROCESSING, V_STATE_READY, is_high_light_support

class EndSceneUIBase(BasePanel):
    GLOBAL_EVENT = {'on_video_stop_event': '_on_video_stop_event'
       }

    def on_init_panel(self, *args, **kwargs):
        super(EndSceneUIBase, self).on_init_panel(*args, **kwargs)
        self._node_high = None
        self._init_high_light()
        return

    def on_finalize_panel(self):
        super(EndSceneUIBase, self).on_finalize_panel()

    def _on_video_stop_event(self, success):
        if not success:
            if self._node_high:
                self._node_high.setVisible(False)
        else:
            self._init_high_light()

    def _init_high_light(self):
        if is_high_light_support():
            if not self._node_high:
                self._node_high = global_data.uisystem.load_template_create(self._get_high_light_btn(), self.panel.nd_high_light)
                self._node_high.btn_high_light.btn.BindMethod('OnClick', self._on_click_high_light_btn)
                self._node_high.setVisible(True)
            state = VideoRecord().get_video_state()
            if state in (V_STATE_PROCESSING, V_STATE_READY):
                self._node_high.PlayAnimation('loop_highlight')
        elif self._node_high:
            self._node_high.setVisible(False)

    def _get_high_light_btn(self):
        return 'end/i_end_highlight_btn'

    def _on_click_high_light_btn(self, *args):
        from logic.gcommon.common_const.ui_operation_const import HIGH_LIGHT_KEY
        high_light_enable = global_data.player or False if 1 else global_data.player.get_setting_2(HIGH_LIGHT_KEY)
        if not high_light_enable:
            from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
            NormalConfirmUI2(content=get_text_by_id(243))
        else:
            state = VideoRecord().get_video_state()
            if state in (V_STATE_PROCESSING, V_STATE_READY):
                global_data.ui_mgr.show_ui('EndHighlightUI', 'logic.comsys.video')
            else:
                global_data.game_mgr.show_tip(get_text_by_id(3143))
                return

    def on_begin_share(self):
        self.panel.nd_high_light.setVisible(False)

    def on_end_share(self):
        self.panel.nd_high_light.setVisible(True)

    def get_battle_type(self):
        from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN, PLAY_TYPE_GVG
        return PLAY_TYPE_CHICKEN