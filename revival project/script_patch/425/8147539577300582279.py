# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/guide_ui/NewMechaNewbieGuideUI.py
from __future__ import absolute_import
from logic.comsys.activity.SimpleAdvance import SimpleAdvance
from logic.gutils.jump_to_ui_utils import jump_to_mode_choose
import common.const.uiconst as ui_const
import cc
from logic.gutils.fly_out_animation import FlyOutMotion

class NewMechaNewbieGuideUI(SimpleAdvance):
    PANEL_CONFIG_NAME = 'guide/guide_new_give_away'
    LASTING_TIME = 0.5
    UI_VKB_TYPE = ui_const.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME

    def on_init_panel(self, *args):
        super(NewMechaNewbieGuideUI, self).on_init_panel(*args)
        action = self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show_title')),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]))

        @self.panel.temp_go.btn_common.callback()
        def OnClick(*args):
            self.close()
            global_data.ui_mgr.show_ui('MechaDisplay', 'logic.comsys.mecha_display')

    def get_close_node(self):
        return (
         self.panel.nd_touch, self.panel.btn_close)

    def on_click_close_btn(self):
        self.close()