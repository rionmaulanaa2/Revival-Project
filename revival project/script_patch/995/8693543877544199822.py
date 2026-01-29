# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallBannerWidget.py
from __future__ import absolute_import
import math
import ccui
import cc
from common.cfg import confmgr
from common.utils.timer import CLOCK
from common.utils.cocos_utils import ccp
from logic.gutils import mall_utils
from logic.gutils import template_utils
LEFT = 0
RIGHT = 1
REFRESH_INTERVAL = 10.0

class MallBannerWidget(object):

    def __init__(self, panel):
        super(MallBannerWidget, self).__init__()
        self.sub_panel = panel
        self._last_offset = 0
        self._scroll_direction = RIGHT
        self._cur_idx = 0
        self._is_focus = False
        self._timer = None
        self._time_count = REFRESH_INTERVAL
        self._switch_callback = None
        self._banner_goods_list = []
        self.init_panel()
        self.init_ui_event()
        self.process_event(True)
        return

    def set_focus(self, flag):
        self._is_focus = flag
        self._time_count = REFRESH_INTERVAL

    def reset_time_count(self):
        self._time_count = REFRESH_INTERVAL

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'rotate_model_display': self.on_rotate_model
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_panel(self):
        mall_recommend_conf = confmgr.get('mall_recommend_conf')
        self._banner_goods_list = mall_utils.get_recommend_banner_list()
        self.sub_panel.list_num.DeleteAllSubItem()
        self.sub_panel.list_item.DeleteAllSubItem()
        for goods_id in self._banner_goods_list:
            self.sub_panel.list_num.AddTemplateItem()
            item = self.sub_panel.list_item.AddTemplateItem()

            @item.bar.unique_callback()
            def OnClick(btn, touch):
                self.on_switch_banner(is_click=True)

        self.update_list()
        if self.sub_panel.list_item.GetItemCount() > 0:
            self._timer = global_data.game_mgr.register_logic_timer(self.tick, interval=1.0, times=-1, mode=CLOCK)
        else:
            self.sub_panel.setVisible(False)

    def update_list(self):
        for i, goods_id in enumerate(self._banner_goods_list):
            item = self.sub_panel.list_item.GetItem(i)
            template_utils.init_mall_recommend_item1(item, goods_id)

    def set_switch_callback(self, callback):
        self._switch_callback = callback

    def select_good(self, index):
        if index > len(self._banner_goods_list) - 1:
            return
        self.sub_panel.list_num.GetItem(self._cur_idx).btn_icon_choose.SetSelect(False)
        self.sub_panel.list_num.GetItem(index).btn_icon_choose.SetSelect(True)
        self._cur_idx = index
        self.sub_panel.list_item.LocatePosByItem(index)
        self.on_switch_banner(is_click=True)

    def init_ui_event(self):
        self.sub_panel.list_item.BindMethod('OnScrolling', self._on_scrolling)
        self.sub_panel.list_item.addTouchEventListener(self._on_normal_touch)
        self.sub_panel.list_item.setInertiaScrollEnabled(False)

    def on_switch_banner(self, is_click=False):
        if self._switch_callback:
            self._switch_callback(self.sub_panel.list_item.GetItem(self._cur_idx), self._banner_goods_list[self._cur_idx], is_click=is_click)

    def _on_normal_touch(self, widget, event):
        if event in (ccui.WIDGET_TOUCHEVENTTYPE_ENDED, ccui.WIDGET_TOUCHEVENTTYPE_CANCELED):
            idx_item = self.update_now_idx()
            self.sub_panel.list_num.GetItem(self._cur_idx).btn_icon_choose.SetSelect(False)
            self.sub_panel.list_num.GetItem(idx_item).btn_icon_choose.SetSelect(True)
            self._cur_idx = idx_item
            self.sub_panel.list_item.LocatePosByItem(idx_item)
            self.on_switch_banner(is_click=True)
            if not self._timer:
                self._timer = global_data.game_mgr.register_logic_timer(self.tick, interval=1.0, times=-1, mode=CLOCK)

    def _on_scrolling(self, *args):
        num = self.sub_panel.list_item.GetItemCount()
        if num <= 1:
            return
        else:
            if self._timer:
                global_data.game_mgr.unregister_logic_timer(self._timer)
                self._timer = None
            off_set_now = self.sub_panel.list_item.GetContentOffset()
            self._scroll_direction = RIGHT if off_set_now.x - self._last_offset <= 0 else LEFT
            self._last_offset = off_set_now.x
            now_idx = self.update_now_idx()
            if now_idx != self._cur_idx:
                self.sub_panel.list_num.GetItem(self._cur_idx).btn_icon_choose.SetSelect(False)
                self.sub_panel.list_num.GetItem(now_idx).btn_icon_choose.SetSelect(True)
                self._cur_idx = now_idx
                self.on_switch_banner()
            return

    def update_now_idx(self):
        ctrl_size = self.sub_panel.list_item.GetCtrlSize()
        off_set_now = self.sub_panel.list_item.GetContentOffset()
        off_num = abs(off_set_now.x / ctrl_size.width)
        if self._scroll_direction == RIGHT:
            idx_item = int(math.ceil(off_num))
        else:
            idx_item = int(math.floor(off_num))
        item_count = self.sub_panel.list_num.GetItemCount()
        if idx_item >= item_count:
            return item_count - 1
        return idx_item

    def on_rotate_model(self, rotate_times):
        self._time_count = REFRESH_INTERVAL

    def tick(self):
        if not self._is_focus:
            return
        self._time_count -= 1
        if self._time_count > 0:
            return
        num = self.sub_panel.list_item.GetItemCount() if self.sub_panel.list_item else 0
        if num <= 1:
            return
        next_idx = 0 if self._cur_idx + 1 >= num else self._cur_idx + 1
        container = self.sub_panel.list_item.GetInnerContainer()
        container.stopAllActions()

        def scroll_end():
            self.sub_panel.list_num.GetItem(self._cur_idx).btn_icon_choose.SetSelect(False)
            self.sub_panel.list_num.GetItem(next_idx).btn_icon_choose.SetSelect(True)
            self.sub_panel.list_item.LocatePosByItem(next_idx)
            self._cur_idx = next_idx
            self.on_switch_banner()

        ctrl_size = self.sub_panel.list_item.GetCtrlSize()
        container.runAction(cc.Sequence.create([
         cc.MoveTo.create(0.3, ccp(ctrl_size.width * next_idx * -1, container.getPosition().y)),
         cc.CallFunc.create(scroll_end)]))
        self._time_count = REFRESH_INTERVAL

    def destroy(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
            self._timer = None
        self.process_event(False)
        return