# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/SkinDefineGuideDecalListUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import GUIDE_LAYER_ZORDER, UI_VKB_CUSTOM
from logic.gcommon.common_utils.local_text import get_text_by_id

class SkinDefineGuideDecalListUI(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/i_skin_define_guide_decal_list'
    DLG_ZORDER = GUIDE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'canvas1.OnBegin': '_on_click',
       'canvas2.OnBegin': '_on_click'
       }
    GLOBAL_EVENT = {}
    GUIDE_NUM = 2
    GUIDE_TEXT = [0, 5149, 5150]

    def on_init_panel(self, *args, **kwargs):
        super(SkinDefineGuideDecalListUI, self).on_init_panel()
        self.step = 1
        ui = global_data.ui_mgr.get_ui('SkinDefineUI')
        if not ui:
            self.close()
            return
        self.widget = ui.decal_widget
        if not self.widget:
            self.close()
            return
        self.show_guide()

    def show_guide(self):
        self.item = getattr(self.widget.panel, 'temp_guide_%d' % (self.step + 6))
        self.item.nd_step.lab_tips.SetString(get_text_by_id(self.GUIDE_TEXT[self.step]))
        self.item.setVisible(True)
        self.item.PlayAnimation('show')

    def _on_click(self, *args):
        if self.item:
            self.item.setVisible(False)
        self.step += 1
        if self.step > self.GUIDE_NUM:
            self.close()
            return
        self.show_guide()

    def on_finalize_panel(self):
        if self.step > self.GUIDE_NUM:
            global_data.achi_mgr.set_cur_user_archive_data('skin_define_decal_list', True)
        super(SkinDefineGuideDecalListUI, self).on_finalize_panel()

    def ui_vkb_custom_func(self):
        self._on_click()