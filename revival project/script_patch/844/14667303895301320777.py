# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/InfiniteScrollWidget.py
from __future__ import absolute_import
from six.moves import range
from cocosui import cc
from cocosui import cc, ccui, ccs
import game3d

class InfiniteScrollWidget(object):
    TAG_TIMEOUT = 18060801
    TAG_TIMER = 211103

    def __init__(self, scroll_nd, timer_nd, up_limit=300, down_limit=300, get_tempate_path_func=None):
        self._sview = scroll_nd
        self._timer_nd = timer_nd
        self._up_limit = up_limit
        self._down_limit = down_limit
        self._sview_index = -1
        self._init_show_num = self.cal_init_show_count()
        self._is_check_sview = False
        self._is_in_func_check_sview = False
        self._require_data_callback = None
        self._refresh_callback = None
        self._reach_bottom_cd = None
        self._template_func = None
        self._data_list = []
        self._is_in_extra = False
        self._extra_height = 50
        self.requiring_offset = 30
        self.is_in_require = False
        self.init_touch_event()
        self.is_touch_trigger_require = False
        self._last_require_time = 0
        self._custom_add_item_func = None
        self._custom_del_item_func = None
        self._min_require_interval = 3.0
        self._check_sview_interval = 0.01
        self._is_only_add = False
        self._get_tempate_path_func = get_tempate_path_func
        self.clear()

        @self._sview.unique_callback()
        def OnScrolling(sender):
            if not self._sview:
                return
            if game3d.get_platform() != game3d.PLATFORM_WIN32 and self.is_in_touch or game3d.get_platform() == game3d.PLATFORM_WIN32:
                if self._is_check_sview == False:
                    self._is_check_sview = True
                    self._timer_nd.SetTimeOut(self._check_sview_interval, self.update_scroll_view, tag=self.TAG_TIMER)
                pos = self._sview.GetContentOffset()
                if pos.y > self.requiring_offset and self.check_can_require():
                    if self.check_require_time():
                        self.is_touch_trigger_require = True
                        self.set_in_require()
                        if self._require_data_callback:
                            self._require_data_callback()

        @self._sview.unique_callback()
        def OnScrollBounceTop(sv):
            pass

        return

    def check_refresh_callback(self):
        if self.get_view_start_index() <= 0:
            if self._refresh_callback:
                pos = self._sview.GetContentOffset()
                min_offset = self._sview.MinContainerOffset()
                _bounceTopBoundary = self._sview.GetContentSize()[1] / 3.5
                if min_offset.y - pos.y > _bounceTopBoundary:
                    if not self.is_in_require:
                        self.set_in_require()
                        self._refresh_callback()
                    else:
                        global_data.game_mgr.show_tip(get_text_local_content(15806))

    def check_can_require(self):
        if not self.is_in_require and not self.is_touch_trigger_require and self._require_data_callback:
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
            self.check_refresh_callback()
        elif event == ccui.WIDGET_TOUCHEVENTTYPE_CANCELED:
            self.is_in_touch = False
            self.check_refresh_callback()

    def destroy(self):
        self._custom_add_item_func = None
        self._custom_del_item_func = None
        self.clear()
        self._refresh_callback = None
        self._require_data_callback = None
        self._sview = None
        self._data_list = []
        self._template_func = None
        self._timer_nd = None
        return

    def set_require_data_callback(self, callback):
        self._require_data_callback = callback

    def set_refresh_callback(self, callback):
        self._refresh_callback = callback

    def set_template_init_callback(self, callback):
        self._template_func = callback

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
        if view_index is None or view_index < 0:
            return self.init_list_show(data_list)
        else:
            msg_count = len(data_list)
            if self._sview.getDirection() == ccui.SCROLLVIEW_DIRECTION_HORIZONTAL:
                new_view_index = self._sview.AutoAddAndRemoveItemHorizontal(view_index, data_list, msg_count, self.add_elem)
            else:
                new_view_index = self._sview.AutoAddAndRemoveItem(view_index, data_list, msg_count, self.add_elem, self._up_limit, self._down_limit, del_msg_func=self._custom_del_item_func, is_only_add=self._is_only_add)
            return new_view_index

    def add_elem(self, data, is_back_item=True, index=-1):
        if self._custom_add_item_func:
            panel = self._custom_add_item_func(data, is_back_item, index)
            return panel
        else:
            if self._get_tempate_path_func:
                template_path = self._get_tempate_path_func(data)
                template_conf = global_data.uisystem.load_template(template_path)
                if is_back_item:
                    panel = self._sview.AddItem(template_conf, bRefresh=True)
                else:
                    panel = self._sview.AddItem(template_conf, 0, bRefresh=True)
            elif is_back_item:
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
            return
        index = 0
        data_count = len(data_list)
        while index < self._init_show_num and index < data_count:
            data = data_list[index]
            item = self._sview.GetItem(index)
            if not item:
                self.add_elem(data, index=index)
            else:
                self.init_template_item(item, data)
            index += 1

        self._sview.RefreshItemPos()
        return index - 1

    def clear(self):
        self._sview.DeleteAllSubItem()
        self._data_list = []
        self._timer_nd.stopActionByTag(self.TAG_TIMER)
        self._timer_nd.stopActionByTag(self.TAG_TIMEOUT)
        self._is_check_sview = False
        self._sview_index = -1

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
        old_sview_index = self._sview_index
        if old_sview_index >= tail_start_index:
            for idx in range(old_sview_index, tail_start_index - 1, -1):
                if idx > len(self._data_list) - 1:
                    self._sview.DeleteItemIndex(idx, False)
                    self._sview_index = idx - 1
                else:
                    item = self.get_list_item(idx)
                    if item:
                        self.init_template_item(item, self._data_list[idx])
                    else:
                        self.add_elem(self._data_list[idx], True, idx)

        if len(self._data_list) > 0:
            if self._sview.GetItemCount() <= self._init_show_num:
                self._sview_index = self.init_list_show(self._data_list)
            else:
                self.update_scroll_view()

    def get_view_start_index(self):
        if self._sview_index is None or self._sview_index < 0:
            return -1
        else:
            s_count = self._sview.GetItemCount()
            return self._sview_index - s_count + 1

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

    def cal_init_show_count(self):
        out_size = self._sview.GetContentSize()
        item_size = self._sview.GetCtrlSize()
        height = out_size[1] - 2 * self._sview.GetVertBorder()
        item_count = int(height / (item_size.height + self._sview.GetVertIndent())) + 1
        return item_count * self._sview.GetNumPerUnit()

    def set_custom_add_item_func(self, func):
        self._custom_add_item_func = func

    def set_custom_del_item_func(self, func):
        self._custom_del_item_func = func

    def refresh_showed_item(self, has_diff_size=False, refresh_func=None):
        if self._sview_index is None:
            self.init_list_show(self._data_list)
            return
        else:
            all_item = self._sview.GetAllItem()
            end_index = self._sview_index
            count = len(all_item)
            start_index = end_index - count + 1
            view_width, view_height = self._sview.GetContentSize()
            content_size = self._sview.GetInnerContentSize()
            content_width = content_size.width
            content_height = content_size.height
            is_larger = content_width > view_width or content_height > view_height
            if len(self._data_list) > end_index and (count >= self._init_show_num or is_larger):
                for idx, ui_item in enumerate(all_item):
                    data = self._data_list[start_index + idx]
                    if refresh_func:
                        refresh_func(ui_item, data, start_index + idx)
                    else:
                        self.init_template_item(ui_item, data)

                if has_diff_size:
                    self._sview.RefreshItemPos()
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

            if has_diff_size:
                self._sview.RefreshItemPos()
            return

    def refresh_showed_item_by_data_index(self, data_start_index, data_end_index, refresh_func=None):
        data_count = len(self._data_list)
        if data_start_index >= data_count or data_end_index >= data_count:
            return
        if data_end_index < data_start_index:
            return
        all_item = self._sview.GetAllItem()
        end_index = self._sview_index
        count = len(all_item)
        start_index = end_index - count + 1
        for idx in range(data_start_index, data_end_index):
            if end_index >= idx >= start_index:
                data = self._data_list[idx]
                ui_item_index = idx - start_index
                ui_item = self._sview.GetItem(ui_item_index)
                if ui_item:
                    if refresh_func:
                        refresh_func(ui_item, data, idx)
                    else:
                        self.init_template_item(ui_item, data)

    def set_is_only_add(self, is_only_add):
        self._is_only_add = is_only_add

    def set_check_view_interval(self, interval):
        self._check_sview_interval = interval

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

    def change_num_per_unit(self):
        self._init_show_num = self.cal_init_show_count()
        self.refresh_showed_item()

    def enable_item_auto_pool(self, enable):
        self._sview.EnableItemAutoPool(True)

    def center_with_index(self, list_index, refresh_template_item_func):
        self.position_with_index(list_index, refresh_template_item_func)

    def top_with_index(self, list_index, refresh_template_item_func):
        self.position_with_index(list_index, refresh_template_item_func, pos_func=self._sview.TopWithNode)

    def position_with_index(self, list_index, refresh_template_item_func, pos_func=None):
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
        first_half = self._init_show_num // 2 + 1
        start_index = max(list_index - first_half, 0)
        end_index = min(start_index + self._init_show_num, data_count - 1)
        if not callable(refresh_template_item_func):
            self._sview.DeleteAllSubItem()
            if len(data_list) <= 0:
                return
            index = start_index
            while index <= end_index:
                data = data_list[index]
                self.add_elem(data, index=index)
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
                    self.add_elem(self._data_list[idx], index=idx)

        self._sview_index = end_index
        ui_item = self.get_list_item(list_index)
        if ui_item:
            pos_func(ui_item)