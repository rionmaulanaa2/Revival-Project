# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/InfiniteScrollHelper.py
from __future__ import absolute_import
from six.moves import range
from cocosui import cc
import game3d

class InfiniteScrollHelper(object):
    TAG_TIMEOUT = 18060801

    def __init__(self, scroll_nd, timer_nd, up_limit=2000, down_limit=2000):
        self._sview = scroll_nd
        self._timer_nd = timer_nd
        self._up_limit = up_limit
        self._down_limit = down_limit
        self._sview_index = -1
        self.cur_max_page = 0
        self._init_show_num = self.cal_init_show_count()
        self._is_check_sview = False
        self._is_in_func_check_sview = False
        self._require_data_callback = None
        self._refresh_callback = None
        self._on_scroll_callback = None
        self._reach_bottom_cd = None
        self._template_func = None
        self._data_list = []
        self._is_in_extra = False
        self._extra_height = 0
        self.requiring_offset = 50
        self.is_in_require = False
        self.init_touch_event()
        self.is_touch_trigger_require = False
        self._last_require_time = 0
        self._min_require_interval = 3.0
        self._custom_scroll_item_func = None

        @self._sview.unique_callback()
        def OnScrolling(sender):
            if not self._sview:
                return
            if game3d.get_platform() != game3d.PLATFORM_WIN32 and self.is_in_touch or game3d.get_platform() == game3d.PLATFORM_WIN32:
                if self._is_check_sview == False:
                    self._is_check_sview = True
                    self._timer_nd.SetTimeOut(0.1, self.update_scroll_view)
                pos = self._sview.GetContentOffset()
                if pos.y > self.requiring_offset and self.check_can_require():
                    if self.check_require_time():
                        self.is_touch_trigger_require = True
                        self.set_in_require()
                        if self.get_data_list_len() > 0:
                            self.show_requiring_tips()
                        if self._require_data_callback:
                            self._require_data_callback()
                    else:
                        global_data.game_mgr.show_tip(get_text_local_content(15806))
            if self._on_scroll_callback:
                self._on_scroll_callback()

        @self._sview.unique_callback()
        def OnScrollBounceTop(sv):
            if self.is_in_touch and self.check_can_require():
                if self.check_can_require():
                    if self._refresh_callback:
                        self.set_in_require()
                        self._refresh_callback()
                else:
                    global_data.game_mgr.show_tip(get_text_local_content(15806))

        return

    def check_can_require(self):
        if not self.is_in_require and not self.is_touch_trigger_require:
            return True
        else:
            return False

    def check_require_time(self):
        import time
        return time.time() - self._last_require_time > self._min_require_interval

    def init_touch_event(self):
        self.is_in_touch = False
        self._sview.addTouchEventListener(self._on_normal_touch)

    def _on_normal_touch(self, widget, event):
        import ccui
        if event == ccui.WIDGET_TOUCHEVENTTYPE_BEGAN:
            self.is_in_touch = True
            self.is_touch_trigger_require = False
        elif event == ccui.WIDGET_TOUCHEVENTTYPE_ENDED:
            self.is_in_touch = False

    def destroy(self):
        self.clear()
        self._refresh_callback = None
        self._require_data_callback = None
        self._sview = None
        self._data_list = []
        self._template_func = None
        self._timer_nd = None
        self._custom_scroll_item_func = None
        return

    def set_require_data_callback(self, callback):
        self._require_data_callback = callback

    def set_refresh_callback(self, callback):
        self._refresh_callback = callback

    def set_template_init_callback(self, callback):
        self._template_func = callback

    def set_scroll_callback(self, callback):
        self._on_scroll_callback = callback

    def update_data_list(self, data_list):
        self._data_list = data_list

    def update_scroll_view(self):
        self._is_in_func_check_sview = True
        self._sview_index = self.check_sview(self._data_list, self._sview_index)
        self._is_in_func_check_sview = False
        self._is_check_sview = False

    def get_scroll_data(self):
        pass

    def check_sview(self, data_list, view_index):
        if view_index < 0:
            return self.init_list_show(data_list)
        msg_count = len(data_list)
        new_view_index = self._sview.AutoAddAndRemoveItem_chat(view_index, data_list, msg_count, self.add_scroll_elem, self._up_limit, self._down_limit)
        return new_view_index

    def add_scroll_elem(self, data, is_back_item=True, index=-1):
        if self._custom_scroll_item_func:
            panel = self._custom_scroll_item_func(data, is_back_item, index)
            return panel
        else:
            if is_back_item:
                panel = self._sview.AddTemplateItem(bRefresh=True)
            else:
                panel = self._sview.AddTemplateItem(0, bRefresh=True)
            self.init_template_item(panel, data)
            return panel

    def init_template_item(self, nd, data):
        if self._template_func:
            self._template_func(nd, data)

    def init_list_show(self, data_list):
        if len(data_list) <= 0:
            return -1
        index = 0
        data_count = len(data_list)
        while index < self._init_show_num and index < data_count:
            data = data_list[index]
            self.add_scroll_elem(data, index=index)
            index += 1

        return index - 1

    def clear(self):
        self._sview.DeleteAllSubItem()
        self._data_list = []
        self._timer_nd.stopAllActions()
        self._is_check_sview = False
        self._sview_index = -1

    def show_requiring_tips(self):
        if hasattr(self._sview, 'nd_loading') and self._sview.nd_loading:
            self._sview.nd_loading.setVisible(True)
            self._sview.nd_loading.PlayAnimation('loading')
        self.set_extra_height()

    def hide_requiring_tips(self):
        if hasattr(self._sview, 'nd_loading') and self._sview.nd_loading:
            self._sview.nd_loading.setVisible(False)
            self._sview.nd_loading.StopAnimation('loading')
        self.clear_extra_height()

    def set_require_timeout_callback(self):

        def timeout():
            self.set_out_require()

        self._timer_nd.SetTimeOut(5.0, timeout, tag=self.TAG_TIMEOUT)

    def set_in_require(self):
        self.is_in_require = True
        self.set_require_timeout_callback()

    def set_out_require(self):
        self._timer_nd.stopActionByTag(self.TAG_TIMEOUT)
        self.is_in_require = False
        self.hide_requiring_tips()

    def set_extra_height(self):
        if self._is_in_extra:
            return
        self._is_in_extra = True
        self._sview.SetExtraBottomMargin(self._extra_height)

    def clear_extra_height(self):
        if not self._is_in_extra:
            return
        self._is_in_extra = False
        self._sview.SetExtraBottomMargin(0)

    def on_receive_data(self, extra_data_list):
        self.set_out_require()
        self._data_list.extend(extra_data_list)
        self.update_scroll_view()
        if not extra_data_list and not self.is_in_touch:
            self._sview.ScrollToBottom(0.2)

    def on_receive_update_tail_data(self, tail_start_index, update_list):
        self.set_out_require()
        self._data_list = self._data_list[:tail_start_index]
        self._data_list.extend(update_list)
        s_count = self._sview.GetItemCount()
        if self._sview_index >= tail_start_index:
            for idx in range(tail_start_index, self._sview_index + 1):
                s_idx = s_count - 1 - (self._sview_index - tail_start_index)
                item = self._sview.GetItem(s_idx)
                if item:
                    self.init_template_item(item, self._data_list[idx])

        self.update_scroll_view()
        if len(update_list) <= self._sview_index - tail_start_index:
            self._sview.ScrollToBottom(0.2)

    def get_data_list_len(self):
        return len(self._data_list)

    def get_view_list(self):
        view_list = []
        s_count = self._sview.GetItemCount()
        for i in range(s_count):
            item_widget = self._sview.GetItem(i)
            data = self._data_list[self._sview_index - s_count + 1 + i]
            view_list.append((item_widget, data))

        return view_list

    def refresh_showed_item(self, refresh_func=None):
        if self._sview_index < 0:
            self.init_list_show(self._data_list)
            return
        all_item = self._sview.GetAllItem()
        end_index = self._sview_index
        count = len(all_item)
        start_index = end_index - count + 1
        if len(self._data_list) >= end_index and count >= self._init_show_num:
            for idx, ui_item in enumerate(all_item):
                data = self._data_list[start_index + idx]
                if refresh_func:
                    refresh_func(ui_item, data, start_index + idx)
                else:
                    self.init_template_item(ui_item, data)

        else:
            self._sview.ScrollToTop()
            start_index = 0
            max_len = min(self._init_show_num, len(self._data_list))
            end_index = max_len - 1
            self._sview.SetInitCount(max_len)
            self._sview_index = end_index
            all_item = self._sview.GetAllItem()
            for idx, ui_item in enumerate(all_item):
                data = self._data_list[start_index + idx]
                if refresh_func:
                    refresh_func(ui_item, data, start_index + idx)
                else:
                    self.init_template_item(ui_item, data)

    def get_slider_info(self):
        import common.utilities
        info = {}
        in_height = self._sview.getInnerContainerSize().height
        out_height = self._sview.getContentSize().height
        pos_y = self._sview.getInnerContainer().getPositionY()
        scale = float(out_height) / in_height
        info['scale'] = scale
        if out_height - in_height == 0.0:
            info['percent'] = 50.0
        else:
            info['percent'] = common.utilities.smoothstep(out_height - in_height, 0.0, pos_y) * 100.0
        return info

    def cal_init_show_count(self):
        out_size = self._sview.GetContentSize()
        item_size = self._sview.GetCtrlSize()
        item_count = int(out_size[1] / item_size.height) + 1
        return item_count * self._sview.GetNumPerUnit()

    def set_custom_scroll_item_func(self, func):
        self._custom_scroll_item_func = func

    def get_list_item(self, list_index):
        if self._is_in_func_check_sview:
            log_error('sview index is not correct when in check_sview')
            return None
        else:
            count = self._sview.GetItemCount()
            if count == 0:
                return None
            valid_end_index = self._sview_index
            valid_start_index = self._sview_index + 1 - count
            if valid_start_index <= list_index < valid_end_index + 1:
                return self._sview.GetItem(list_index - valid_start_index)
            return None
            return None

    def center_with_index(self, list_index, refresh_template_item_func, pos_func=None):
        if not pos_func:
            pos_func = self._sview.CenterWithNode
        ui_item = self.get_list_item(list_index)
        if ui_item:
            pos_func(ui_item)
        elif list_index >= len(self._data_list) or list_index < 0:
            log_error('try to jump to an invalid index: ', list_index)
            return
        data_list = self._data_list
        data_count = len(data_list)
        first_half = self._init_show_num / 2 + 1
        start_index = max(list_index - first_half, 0)
        end_index = min(start_index + self._init_show_num, data_count - 1)
        if not callable(refresh_template_item_func):
            self._sview.DeleteAllSubItem()
            if len(data_list) <= 0:
                return
            index = start_index
            while index <= end_index:
                data = data_list[index]
                self.add_scroll_elem(data, index=index)
                index += 1

            self._sview_index = end_index
            ui_item = self.get_list_item(list_index)
            if ui_item:
                pos_func(ui_item)
        else:
            count = self._sview.GetItemCount()
            exceed_count = count - (end_index + 1 - start_index)
            if exceed_count > 0:
                end_index = min(end_index + exceed_count, data_count - 1)
            exceed_count = count - (end_index + 1 - start_index)
            if exceed_count > 0:
                start_index = max(start_index - exceed_count, 0)
            exceed_count = count - (end_index + 1 - start_index)
            if exceed_count > 0:
                self._sview.SetInitCount(end_index + 1 - start_index)
            for idx in range(start_index, end_index + 1):
                ui_item = self._sview.GetItem(idx - start_index)
                if ui_item:
                    refresh_template_item_func(ui_item, self._data_list[idx])
                else:
                    self.add_scroll_elem(self._data_list[idx], index=idx)

        self._sview_index = end_index
        ui_item = self.get_list_item(list_index)
        if ui_item:
            pos_func(ui_item)