# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/SkinCustomJumpEntryWidget.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gutils.item_utils import get_lobby_item_type
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN
from logic.gutils import mecha_skin_utils
from logic.gutils.item_utils import check_is_improvable_skin
from logic.gutils.lobby_click_interval_utils import global_unique_click

class SkinCustomJumpEntryWidget(BaseUIWidget):

    def __init__(self, parent_ui, panel):
        super(SkinCustomJumpEntryWidget, self).__init__(parent_ui, panel)
        self._item_no = None
        self._init_panel()
        self._init_ui_event()
        return

    def switch_panel(self, panel):
        if panel == self.panel:
            return
        self.panel = panel
        self._init_panel()
        self._init_ui_event()

    def destroy(self):
        super(SkinCustomJumpEntryWidget, self).destroy()

    def _init_panel(self):
        pass

    def _init_ui_event(self):

        @global_unique_click(self.panel)
        def OnClick(*args):
            self._jump()

    def set_item(self, item_no):
        self._item_no = item_no
        self._refresh_panel()

    def _refresh_panel(self):
        is_show = self._refresh_panel_vis()
        if not is_show:
            return
        pic_path = 'gui/ui_res_2/lottery/icon_promotion.png'
        self.panel.SetFrames('', [pic_path, pic_path, ''])
        self.panel.lab_promotion.SetString(81769)

    def _refresh_panel_vis(self):
        show = False
        if self._item_no is not None:
            item_type = get_lobby_item_type(self._item_no) if 1 else None
            if item_type == L_ITEM_TYPE_MECHA_SKIN and mecha_skin_utils.is_mecha_skin_customable(self._item_no) and mecha_skin_utils.is_ss_level_skin(self._item_no):
                show = True
        self.panel.setVisible(show)
        return show

    def _jump(self):
        if self._item_no is None:
            return
        else:
            item_type = get_lobby_item_type(self._item_no)
            if item_type == L_ITEM_TYPE_MECHA_SKIN:
                if mecha_skin_utils.is_mecha_skin_customable(self._item_no) and mecha_skin_utils.is_ss_level_skin(self._item_no):
                    from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
                    jump_to_display_detail_by_item_no(self._item_no)
            return