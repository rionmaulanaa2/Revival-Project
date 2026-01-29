# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/ThrowRockerUIPC.py
from __future__ import absolute_import
from .ThrowRockerUI import ThrowRockerBaseUI
from data import hot_key_def
from data.item_use_var import THROW_ID_LIST
from logic.gcommon.item.backpack_item_type import B_ITEM_ICEWALL_ID

class ThrowRockerUIPC(ThrowRockerBaseUI):
    PANEL_CONFIG_NAME = 'battle/fight_throw_pc'
    HOT_KEY_FUNC_MAP = {hot_key_def.USE_CUR_THROW_ITEM: '_keyboard_use_cur_item',
       hot_key_def.OPEN_THROW_PANEL: '_keyboard_open_throw_panel',
       hot_key_def.THROW_ITEM_SCROLL_UP: '_keyboard_item_scroll_up',
       hot_key_def.THROW_ITEM_SCROLL_DOWN: '_keyboard_item_scroll_down'
       }
    HOT_KEY_FUNC_MAP_SHOW = {hot_key_def.USE_CUR_THROW_ITEM: {'node': 'nd_change_throw.temp_pc'},hot_key_def.OPEN_THROW_PANEL: {'node': 'nd_change_throw.change_throw.temp_pc'}}

    def _init_throw_btn(self):
        self.discard_widget.init_btn(self.panel.change_throw, is_scrollable=False)

        @self.panel.change_throw.unique_callback()
        def OnBegin(btn, touch):
            return self._throw_btn_on_begin(touch)

        @self.panel.change_throw.unique_callback()
        def OnEnd(btn, touch):
            if not self._player:
                return
            else:
                if not self.panel.drag_item.isVisible():
                    self._throw_btn_on_end(btn, touch)
                if not self._can_interact():
                    return
                if self._cur_item_data:
                    self.discard_widget.OnEnd(self.panel.change_throw, touch, self._cur_item_data.get('item_id', 0), self._cur_item_data.get('num', 0), [
                     self.panel.change_throw], is_scrollable=False)
                else:
                    self.discard_widget.OnEnd(self.panel.change_throw, touch, None, 0, [
                     self.panel.change_throw], is_scrollable=False)
                return

        self.panel.change_throw.SetPressEnable(True)

        @self.panel.change_throw.unique_callback()
        def OnPressed(btn):
            if not self._player:
                return
            self._throw_btn_on_pressed()

        @self.panel.change_throw.unique_callback()
        def OnDrag(btn, touch):
            if not self._player:
                return
            self._throw_btn_on_drag(touch)
            if not self._can_interact():
                return
            if self._cur_item_data:
                self.discard_widget.OnDrag(btn, touch, self._cur_item_data.get('item_id'), non_discard_list=[
                 self.panel.change_throw], is_scrollable=False)

        @self.panel.btn_close.unique_callback()
        def OnClick(btn, touch):
            self._hide_scroll_panel()