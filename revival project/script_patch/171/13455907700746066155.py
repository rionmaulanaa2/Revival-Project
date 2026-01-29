# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEDebrisReceiveUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_CUSTOM
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import FrameLoaderTemplate
from logic.gutils.pve_lobby_utils import init_story_debris_item
from logic.gcommon.common_const.pve_const import PVE_STORY_DEBRIS_CACHE

class PVEDebrisReceiveUI(BasePanel):
    DELAY_CLOSE_TAG = 20231113
    PANEL_CONFIG_NAME = 'pve/fragments/bg_pve_fragments_confirm'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CUSTOM

    def on_init_panel(self, item_list, *args, **kwargs):
        super(PVEDebrisReceiveUI, self).on_init_panel()
        self.init_params(item_list)
        self.init_panel()
        self.init_ui_events()

    def init_params(self, item_list):
        self._disappearing = None
        self._item_list = item_list
        return

    def init_panel(self):
        self.panel.PlayAnimation('appear')
        self._init_list_item()

    def init_ui_events(self):

        @self.panel.callback()
        def OnClick(btn, touch):
            self.play_disappear_anim()

    def _init_list_item(self):
        self._frame_loader_template = FrameLoaderTemplate(self.panel.list_item, len(self._item_list), self.init_debris_item)

    def init_debris_item(self, debris_item, cur_index):
        item_no = self._item_list[cur_index]
        item_num = 1
        btn_item = debris_item.btn_item
        btn_item.EnableCustomState(True)
        init_story_debris_item(debris_item, item_no, item_num)

    def play_disappear_anim(self):
        if self._disappearing:
            return
        self._disappearing = True
        anim_time = self.panel.GetAnimationMaxRunTime('disappear')

        def delay_call(*args):
            self._disappearing = False
            self.close()

        self.panel.StopAnimation('disappear')
        self.panel.DelayCallWithTag(anim_time, delay_call, self.DELAY_CLOSE_TAG)
        self.panel.PlayAnimation('disappear')

    def on_finalize_panel(self):
        self._disappearing = None
        self._item_list = None
        if self._frame_loader_template:
            self._frame_loader_template.destroy()
            self._frame_loader_template = None
        super(PVEDebrisReceiveUI, self).on_finalize_panel()
        return