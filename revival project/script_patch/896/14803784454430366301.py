# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallPageTabWidget.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import mall_utils
from common.cfg import confmgr
from logic.client.const import mall_const
from logic.gutils import template_utils
from logic.comsys.charge_ui.LeftTimeCountDownWidget import LeftTimeCountDownWidget
from logic.gcommon import time_utility as tutil

class MallPageTabWidget(object):

    def __init__(self, parent):
        self.parent = parent
        self.panel = parent.panel
        self.init_parameters()
        self.init_event()

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'mall_red_point_update': self._update_rp_or_new_or_dc_bubble,
           'mall_new_recommendation_update': self._update_rp_or_new_or_dc_bubble,
           'mall_goods_discount_rp_update': self._update_rp_or_new_or_dc_bubble,
           'mall_dec_set_rp_update': self._update_rp_or_new_or_dc_bubble,
           'mall_new_arrivals_update': self._update_rp_or_new_or_dc_bubble
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)
        for page_index, sub_page_2_widget in six.iteritems(self._left_time_widgets):
            for sub_page, widget in six.iteritems(sub_page_2_widget):
                if widget:
                    widget.destroy()

        self._left_time_widgets = None
        return

    def init_parameters(self):
        self._cur_page_widget = None
        self._cur_sub_page_widget = None
        self._cur_widget_index = 0
        self._sub_page_list_widget = None
        self._is_recycle_sub_page_list = False
        self._sub_page_list_conf = global_data.uisystem.load_template('common/i_left_second_tab_dark_list')
        self._page_type_to_widget = {}
        self._sub_page_type_to_widget = {}
        self._left_time_widgets = {}
        return

    def on_red_point_update(self):
        self._update_rp_or_new_or_dc_bubble()

    def get_cur_page_widget(self):
        return self._cur_page_widget

    def _update_rp_or_new_or_dc_bubble(self, *args):
        for page, widget in six.iteritems(self._page_type_to_widget):
            widget = self._page_type_to_widget[page]
            if widget:
                self._refresh_rp_or_new_or_dc_bubble(page, None, widget.img_red, widget.mall_new, widget.mall_dc)

        if self._sub_page_list_widget:
            page_num = mall_utils.get_sub_page_num(self._sub_page_list_widget._page_index)
            for sub_index in range(page_num):
                sub_widget = self._sub_page_list_widget.GetItem(sub_index)
                if not (sub_widget and sub_widget.isValid()):
                    continue
                self._refresh_rp_or_new_or_dc_bubble(self._sub_page_list_widget._page_index, sub_widget._sub_page_idx, sub_widget.img_red, sub_widget.mall_new, sub_widget.mall_dc)

        global_data.emgr.lobby_mall_red_point_update.emit()
        return

    def init_page_tab(self):
        tab_conf = global_data.lobby_mall_data.get_mall_tag_conf()
        self._page_type_to_widget = {}
        self._sub_page_type_to_widget = {}
        tab_info_list = []
        sorted_list = sorted(six_ex.keys(tab_conf), key=lambda x: tab_conf.get(str(x), {}).get('sort_val', 100))
        for page_index in sorted_list:
            name_id = tab_conf[page_index]['name_id']
            tab_info_list.append([page_index, get_text_by_id(name_id)])

        tablist = self.panel.temp_left_tab.tab_list
        tablist.SetInitCount(len(tab_info_list))
        all_items = tablist.GetAllItem()
        for index, item_widget in enumerate(all_items):
            page_index, name = tab_info_list[index]
            item_widget.btn.SetText(name)
            if mall_utils.get_sub_page_num(page_index) > 0:
                item_widget.btn_arrow.setVisible(True)
                item_widget.btn_arrow.setRotation(0)
            else:
                item_widget.btn_arrow.setVisible(False)
            if not getattr(item_widget, 'mall_new', None):
                item_widget.mall_new = template_utils.create_and_init_mall_new_icon(item_widget.img_red, 'mall_new')
            if not getattr(item_widget, 'mall_dc', None):
                item_widget.mall_dc = template_utils.create_and_init_mall_discount_icon(item_widget.img_red, 'mall_dc')
            self._page_type_to_widget[page_index] = item_widget
            self._refresh_rp_or_new_or_dc_bubble(page_index, None, item_widget.img_red, item_widget.mall_new, item_widget.mall_dc)
            item_widget.btn.EnableCustomState(True)

            @item_widget.btn.unique_callback()
            def OnClick(btn, touch, index=index, item_widget=item_widget, page_index=page_index, tab_conf=tab_conf, def_sub_page=None):
                if page_index == mall_const.CHARGE_ID:
                    from logic.comsys.charge_ui.ChargeUINew import ChargeUINew
                    ChargeUINew()
                    return
                self.set_selected_widget(index, item_widget, page_index, tab_conf, def_sub_page)

        return

    def set_selected_widget(self, index, item_widget, page_index, tab_conf, def_sub_page):
        if self._cur_page_widget and self._cur_page_widget.isValid():
            self._cur_page_widget.btn.SetSelect(False)
            del_count = mall_utils.get_sub_page_num(self.parent.get_cur_page_index())
            if del_count > 0 and self._cur_sub_page_widget and self._sub_page_list_widget:
                self.panel.temp_left_tab.tab_list.StopTimerAction()
                self._is_recycle_sub_page_list = True
                self._sub_page_list_widget.retain()
                self._sub_page_list_widget.removeFromParent()
                del self.panel.temp_left_tab.tab_list._container._child_item[self._cur_widget_index + 1]
                self.panel.temp_left_tab.tab_list._container._refreshItemPos()
                self.panel.temp_left_tab.tab_list._refreshItemPos()
                self.panel.temp_left_tab.tab_list.GetItem(self._cur_widget_index).btn_arrow.setRotation(0)
                self._cur_sub_page_widget = None
                if self._cur_widget_index == index:
                    self._cur_page_widget.btn.SetSelect(True)
                    return
            self._cur_page_widget.StopAnimation('continue')
            self._cur_page_widget.RecoverAnimationNodeState('continue')
        sub_page_index = None
        if mall_utils.get_sub_page_num(page_index) > 0:
            item_widget.btn_arrow.setRotation(180)
            sub_page_index = self.init_sub_page_list(index, page_index, tab_conf[page_index], def_sub_page)
        self._cur_page_widget = item_widget
        self._cur_widget_index = index
        self._cur_page_widget.btn.SetSelect(True)
        self._cur_page_widget.PlayAnimation('click')
        self._cur_page_widget.RecordAnimationNodeState('continue')
        self._cur_page_widget.PlayAnimation('continue')
        self.parent.set_selected_page(page_index, sub_page_index)
        if page_index == mall_const.MECHA_FRAGMENT_ID:
            self._update_rp_or_new_or_dc_bubble()
        if sub_page_index == None:
            mall_utils.read_new_arrivals_by_page(page_index)
        return

    def init_sub_page_list(self, index, page_index, tab_dict, def_sub_page):
        if not self._sub_page_list_widget:
            self._sub_page_list_widget = global_data.uisystem.create_item(self._sub_page_list_conf)
        self._sub_page_list_widget._page_index = page_index
        page_num = mall_utils.get_sub_page_num(page_index)
        self._sub_page_list_widget.SetInitCount(page_num)
        sub_index = 0
        first_sub_page_index = None
        max_time = 0
        ani_name = 'show'
        def_sub_index = 0
        for _sub_page_index in sorted(six_ex.keys(tab_dict)):
            if not _sub_page_index.isdigit():
                continue
            if mall_utils.is_mall_page_expired(page_index, _sub_page_index):
                continue
            if not first_sub_page_index:
                first_sub_page_index = _sub_page_index
            if def_sub_page == _sub_page_index:
                def_sub_index = sub_index
                first_sub_page_index = _sub_page_index
            name_id = tab_dict[_sub_page_index]
            sub_item_widget = self._sub_page_list_widget.GetItem(sub_index)
            sub_item_widget._sub_page_idx = _sub_page_index
            sub_item_widget.button.SetSelect(False)
            sub_item_widget.button.SetText(get_text_by_id(name_id))
            if not getattr(sub_item_widget, 'mall_new', None):
                sub_item_widget.mall_new = template_utils.create_and_init_mall_new_icon(sub_item_widget.img_red, 'mall_new')
            if not getattr(sub_item_widget, 'mall_dc', None):
                sub_item_widget.mall_dc = template_utils.create_and_init_mall_discount_icon(sub_item_widget.img_red, 'mall_dc')
            if page_index not in self._sub_page_type_to_widget:
                self._sub_page_type_to_widget[page_index] = {}
            self._sub_page_type_to_widget[page_index][_sub_page_index] = sub_item_widget
            self._try_show_left_time_of_tab(sub_item_widget, page_index, _sub_page_index)
            self._refresh_rp_or_new_or_dc_bubble(page_index, _sub_page_index, sub_item_widget.img_red, sub_item_widget.mall_new, sub_item_widget.mall_dc)
            sub_item_widget.PlayAnimation(ani_name)
            time = sub_item_widget.GetAnimationMaxRunTime(ani_name)
            max_time = max(time, max_time)
            sub_item_widget.PlayAnimation('click')
            sub_item_widget.StopAnimation('click', finish_ani=True)
            sub_item_widget.button.EnableCustomState(True)

            @sub_item_widget.button.unique_callback()
            def OnClick(btn, touch, item_widget=sub_item_widget, page_index=page_index, sub_page_index=_sub_page_index):
                if self._cur_sub_page_widget:
                    self._cur_sub_page_widget.button.SetSelect(False)
                self._cur_sub_page_widget = item_widget
                self._cur_sub_page_widget.button.SetSelect(True)
                self._cur_sub_page_widget.PlayAnimation('click')
                self.parent.set_selected_page(page_index, sub_page_index)
                if getattr(sub_item_widget, 'mall_dc', None) and item_widget.mall_dc.isVisible():
                    if page_index == mall_const.RECOMMEND_ID and sub_page_index == mall_const.RECOMMEND_DISCOUNT_ID:
                        mall_utils.read_discount_hint(mall_const.DISCOUNT_TYPE_NEWYEAR, page_index, sub_page_index)
                mall_utils.read_new_arrivals_by_page(page_index, sub_page_index)
                return

            sub_index += 1

        self.panel.temp_left_tab.tab_list.AddControl(self._sub_page_list_widget, index=index + 1)
        if self._is_recycle_sub_page_list:
            self._sub_page_list_widget.release()
            self._is_recycle_sub_page_list = False
        self._sub_page_list_widget.img_bar.ResizeAndPosition()
        first_sub_item_widget = self._sub_page_list_widget.GetItem(def_sub_index)
        self._cur_sub_page_widget = first_sub_item_widget
        self._cur_sub_page_widget.button.SetSelect(True)
        return first_sub_page_index

    def select_tab_page(self, goods_id, iTypeIdx=None):
        if iTypeIdx is None:
            i_type, i_stype = mall_utils.get_mall_type_stype(goods_id, prior=True)
        else:
            i_type, i_stype = mall_utils.get_mall_type_stype(goods_id, index=iTypeIdx, prior=False)
        self.select_tab_page_by_type(i_type, i_stype)
        return

    def select_tab_page_by_type(self, i_type, i_stype):
        cur_page_index = self.parent.get_cur_page_index()
        cur_sub_page_index = self.parent.get_cur_sub_page_index()
        if cur_page_index is not None and cur_page_index == i_type and cur_sub_page_index == i_stype:
            return
        else:
            if cur_page_index == i_type:
                if cur_page_index in self._sub_page_type_to_widget:
                    sub_item_widget = self._sub_page_type_to_widget[cur_page_index].get(i_stype)
                    sub_item_widget and sub_item_widget.button.OnClick(None)
                    return
            if i_type in self._page_type_to_widget:
                widget = self._page_type_to_widget[i_type]
                widget and widget.btn.OnClick(None, def_sub_page=i_stype)
            else:
                widget = self.panel.temp_left_tab.tab_list.GetItem(0)
                widget and widget.btn.OnClick(None)
            return

    def _refresh_rp_or_new_or_dc_bubble(self, page, sub_page, rp_node, new_node, dc_node):
        has_dc_bubble = False
        if page == mall_const.RECOMMEND_ID and sub_page == mall_const.RECOMMEND_DISCOUNT_ID:
            has_dc_bubble, _ = mall_utils.need_discount_hint(page, sub_page)
        dc_node.setVisible(has_dc_bubble)
        if has_dc_bubble:
            dc_node.PlayAnimation('show')
        else:
            dc_node.StopAnimation('show')
        has_new = False
        if not has_dc_bubble:
            has_new = mall_utils.has_new_recommendations_by_page(page, sub_page)
        new_node.setVisible(has_new)
        if has_new:
            new_node.PlayAnimation('show')
        else:
            new_node.StopAnimation('show')
        show_rp = False
        if not has_dc_bubble and not has_new:
            show_rp = bool(mall_utils.get_mall_red_point(page, sub_page))
        rp_node.setVisible(show_rp)

    def _try_show_left_time_of_tab(self, sub_item_widget, page_index, sub_page_index):
        tab_conf = global_data.lobby_mall_data.get_mall_tag_conf().get(page_index)
        if not tab_conf:
            return
        else:
            expire_time = tab_conf.get('end_time_val', {}).get(sub_page_index, 0)
            if expire_time > tutil.get_server_time():
                sub_item_widget.lab_count.setVisible(True)
                if page_index not in self._left_time_widgets:
                    self._left_time_widgets[page_index] = {}
                existing_widget = self._left_time_widgets[page_index].get(sub_page_index)
                if existing_widget:
                    existing_widget.destroy()
                    self._left_time_widgets[page_index][sub_page_index] = None
                left_time_widget = LeftTimeCountDownWidget(self.panel, sub_item_widget.lab_count, lambda timestamp: tutil.get_readable_time_2(timestamp))
                left_time_widget.begin_count_down_time(expire_time, lambda p_index=page_index, s_index=sub_page_index: self._on_sub_page_time_up(p_index, s_index))
                self._left_time_widgets[page_index][sub_page_index] = left_time_widget
            else:
                sub_item_widget.lab_count.setVisible(False)
            return

    def _on_sub_page_time_up(self, page_index, sub_page_index):
        if page_index not in self._sub_page_type_to_widget:
            return
        sub_item_widget = self._sub_page_type_to_widget[page_index].get(sub_page_index)
        if sub_item_widget:
            sub_item_widget.lab_count.SetString(get_text_by_id(81154))