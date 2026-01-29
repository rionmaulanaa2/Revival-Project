# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SeasonBaseUIWidget.py
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gutils.item_utils import get_lobby_item_type
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.mecha_skin_utils import is_mecha_skin_customable

class SeasonBaseUIWidget(BaseUIWidget):

    def get_display_model_item_no(self):
        if not self._display_widget:
            return None
        else:
            return self._display_widget.get_display_model_item_no()

    def _display_cb(self, is_model, item_no):
        if self.parent and self.parent.panel and self.parent.panel.btn_splus_ex:
            item_type = get_lobby_item_type(item_no)
            is_showing_upgradeable_mecha_skin = item_type == L_ITEM_TYPE_MECHA_SKIN and is_mecha_skin_customable(item_no)
            self.parent.panel.btn_splus_ex and self.parent.panel.btn_splus_ex.setVisible(is_showing_upgradeable_mecha_skin)