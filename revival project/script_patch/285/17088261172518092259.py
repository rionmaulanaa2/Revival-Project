# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/observe_ui/JudgeLoadingUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_VKB_CUSTOM, LOADING_ZORDER_ABOVE

class JudgeLoadingUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/common_bg_unadjust'
    DLG_ZORDER = LOADING_ZORDER_ABOVE
    UI_VKB_TYPE = UI_VKB_CUSTOM

    def on_init_panel(self, *args, **kwargs):
        super(JudgeLoadingUI, self).on_init_panel(*args, **kwargs)
        self.process_event(True)
        self.panel.img_bg.SetDisplayFrameByPath('', 'gui/ui_res_2/common/bg/bg_flying.png')
        self._tips_node = global_data.uisystem.load_template_create('observe/fight_loading_for_judge', self.panel)

    def on_finalize_panel(self, *args, **kwargs):
        self.process_event(False)
        super(JudgeLoadingUI, self).on_finalize_panel(*args, **kwargs)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_observed_player_setted_event': self._on_observe_target_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_observe_target_setted(self, ltarget):
        if ltarget is not None:

            def cb():
                self.close()

            time = self._tips_node.GetAnimationMaxRunTime('go')
            self._tips_node.PlayAnimation('go')
            self.DelayCall(time, cb)
        return

    def ui_vkb_custom_func(self):
        return True