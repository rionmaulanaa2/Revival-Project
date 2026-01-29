# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SimpleAdvance.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
import cc

class SimpleAdvance(BasePanel):
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_1
    APPEAR_ANIM = 'appear'
    LOOP_ANIM = ''
    LASTING_TIME = 0.1
    NEED_GAUSSIAN_BLUR = True
    UI_VKB_TYPE = ui_const.UI_VKB_CLOSE

    def on_init_panel(self, *args):
        self.regist_main_ui()
        self.hide_main_ui()
        self._close_btn_cb = None
        act = []
        if self.APPEAR_ANIM:
            act.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation(self.APPEAR_ANIM)))
        if self.LASTING_TIME:
            act.append(cc.DelayTime.create(self.LASTING_TIME))
        act.append(cc.CallFunc.create(self.on_anim_finish))
        self.panel.runAction(cc.Sequence.create(act))
        self.set_content()
        return

    def get_close_node(self):
        return (
         self.panel,)

    def set_content(self):
        pass

    def _set_close_btn_cb(self, cb):
        self._close_btn_cb = cb

    def on_anim_finish(self):
        close_node = self.get_close_node()
        for nd in close_node:

            @nd.callback()
            def OnClick(*args):
                if callable(self._close_btn_cb):
                    self._close_btn_cb()
                else:
                    self.close()

        if self.LOOP_ANIM:
            self.panel.PlayAnimation(self.LOOP_ANIM)

    def on_finalize_panel(self):
        self.unregist_main_ui()
        self._close_btn_cb = None
        if self.NEED_GAUSSIAN_BLUR:
            import render
            global_data.display_agent.set_post_effect_active('gaussian_blur', False)
        self.show_main_ui()
        return

    def do_hide_panel(self):
        super(SimpleAdvance, self).do_hide_panel()
        if self.NEED_GAUSSIAN_BLUR:
            import render
            global_data.display_agent.set_post_effect_active('gaussian_blur', False)

    def do_show_panel(self):
        super(SimpleAdvance, self).do_show_panel()
        if self.NEED_GAUSSIAN_BLUR:
            import render
            global_data.display_agent.set_post_effect_active('gaussian_blur', True)