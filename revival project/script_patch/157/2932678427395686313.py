# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryNewPreviewWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gcommon.item.item_const import SORTED_RARE_DEGREE_LIST, RARE_DEGREE_0, RARE_DEGREE_1, RARE_DEGREE_2, RARE_DEGREE_3, RARE_DEGREE_4, RARE_DEGREE_5, RARE_DEGREE_6, RARE_DEGREE_7
from logic.gutils.mall_utils import get_lottery_id_list, get_lottery_table_id_list, get_lottery_category_floor_data
from logic.gutils.item_utils import get_skin_rare_path_by_rare, get_lobby_item_type, get_lobby_item_name, get_item_rare_degree
from logic.gutils.lobby_click_interval_utils import global_unique_click
from .LotteryPreviewWidget import LotteryPreviewWidget, CATEGORY_FLOOR_TEXT_MAP
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_GESTURE
from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
from logic.gcommon.common_utils.local_text import get_text_by_id
from random import randint
LOAD_SMALL_ITEM_ACTION_TAG = 10000
LOAD_BIG_BAR_ACTION_TAG = 10001

class LotteryNewPreviewWidget(object):
    ITEM_TEMPLATE = 'mall/i_ss_lottery_review_list_group_item'
    TITLE_TEMPLATE = 'mall/i_ss_lottery_review_list_group_title'
    ITEM_PRE_ROW = 4
    CACHE_ACTION = 20190910

    def __init__(self, panel, parent, mode, on_change_show_reward, show_callback=None, hide_callback=None, close_callback=None):
        self.panel = panel
        self.parent = parent
        self.cur_mode = mode
        self.show_callback = show_callback
        self.hide_callback = hide_callback
        self.close_callback = close_callback
        self.on_change_show_reward = on_change_show_reward
        self._is_init_award_list = False
        self.is_showing = False
        self.on_init_panel()

    def on_init_panel(self):
        if not LotteryPreviewWidget.LOTTERY_INFO:
            global_data.player.request_reward_display_data(get_lottery_table_id_list())
        self.init_parameters()

    def update_award_scroll_list(self, rate_list):
        if self._is_init_award_list:
            return
        self._is_init_award_list = True
        if self._list_sview:
            self._list_sview.clear()
        if rate_list:
            self.prepare_data(rate_list)
            self.init_review_list(self._prepared_data_list)

    def init_parameters(self):
        self.percent_up_item_dict = set()
        self.preview_list_initialized = False
        self.selected_item = None
        self.selected_item_id = None
        self.random_index = None
        self._prepared_data_list = []
        self._list_sview = None
        self.category_floor = {}
        self.item_cache = global_data.item_cache_without_check
        self.init_item_cache()
        from common.utils.ui_utils import get_scale
        import cc
        win_size = cc.Director.getInstance().getWinSize()
        win_w = win_size.width
        self._cancel_dist = get_scale('1w') * win_w / 50
        return

    def item_func_helper(self, ui_item):
        ui_item.list_all_item.SetInitCount(self.ITEM_PRE_ROW)

    def init_item_cache(self, template_conf=None):

        def check_item_cache():
            temp_conf = template_conf
            if not temp_conf:
                temp_conf = {self.ITEM_TEMPLATE: (10, self.item_func_helper),self.TITLE_TEMPLATE: (2, None)
                   }
            for template, conf in six.iteritems(temp_conf):
                num, func = conf
                cur_size = self.item_cache.get_template_cache_size(template)
                if cur_size >= num:
                    continue
                for i in range(cur_size, num):
                    item_widget = global_data.uisystem.load_template_create(template)
                    if func:
                        func(item_widget)
                    self.item_cache.put_back_item_to_cache(item_widget, template)
                    return 0.03

            return None

        self.panel.DelayCallWithTag(0.03, check_item_cache, self.CACHE_ACTION)

    def parent_show(self):
        if self.is_showing:
            self.show()

    def show(self):
        if not LotteryPreviewWidget.LOTTERY_INFO.get(self.cur_mode, None):
            global_data.player.request_reward_display_data(get_lottery_table_id_list())
            self.preview_list_initialized = False
            return
        else:
            self.panel.setVisible(True)
            self.show_callback and self.show_callback()
            if self.selected_item_id:
                self.on_change_show_reward(self.selected_item_id)
            self.is_showing = True
            return

    def parent_hide(self):
        if self.is_showing:
            self.hide(is_passive=True)

    def hide(self, is_passive=False):
        if not self.panel.isVisible():
            return
        self.panel.setVisible(False)
        self.hide_callback and self.hide_callback()
        if is_passive:
            return
        self.close_callback and self.close_callback()
        self.is_showing = False

    def destroy(self):
        self.panel.stopActionByTag(self.CACHE_ACTION)
        self.callback = None
        if self.item_cache:
            self.item_cache = None
        self.on_change_show_reward = None
        self.percent_up_item_dict = None
        self.selected_item = None
        if self._list_sview:
            self._list_sview.destroy()
            self._list_sview = None
        self._prepared_data_list = []
        self.category_floor = {}
        return

    def refresh_preview_list(self, mode, limited_reward_data, percent_up_reward_data, is_force=False):
        if self.preview_list_initialized and not is_force:
            return
        else:
            if not LotteryPreviewWidget.LOTTERY_INFO:
                return
            self.preview_list_initialized = True
            self.cur_mode = mode
            self.category_floor = get_lottery_category_floor_data(self.cur_mode)
            self.percent_up_item_dict = percent_up_reward_data
            mode_data = LotteryPreviewWidget.LOTTERY_INFO[self.cur_mode]
            rate_list = []
            max_rare_degree = -1
            for rare_degree in SORTED_RARE_DEGREE_LIST:
                if rare_degree in mode_data:
                    rate_list.append(rare_degree)
                    if max_rare_degree == -1:
                        max_rare_degree = rare_degree

            if self.random_index is None:
                self.random_index = 0
                items = mode_data.get(max_rare_degree, {}).get('items', None)
                if items:
                    self.selected_item_id = items[0]
            self.update_award_scroll_list(rate_list)
            if self.panel.isVisible():
                self.on_change_show_reward(self.selected_item_id)
            return

    def _register_btn_click(self, item, item_id):

        @global_unique_click(item.btn_choose)
        def OnClick(layer, touch, *args):
            item_type = get_lobby_item_type(item_id)
            if item_type == L_ITEM_TYPE_GESTURE and item_id in LotteryPreviewWidget.LOTTERY_INFO['lottery_merge_item_info'][self.cur_mode]:
                index = randint(1, LotteryPreviewWidget.LOTTERY_INFO['lottery_merge_item_info'][self.cur_mode][item_id][0])
                real_item_id = LotteryPreviewWidget.LOTTERY_INFO['lottery_merge_item_info'][self.cur_mode][item_id][index]
                self.on_change_show_reward(real_item_id, get_lobby_item_name(item_id))
            else:
                self.on_change_show_reward(item_id)
            if self.selected_item and self.selected_item.isValid():
                self.selected_item.btn_choose.SetSelect(False)
            self.selected_item = item
            self.selected_item_id = item_id
            layer.SetSelect(True)

    def init_one_item(self, list_nd, item, item_id, percent_up=False, force_rare_degree=None):
        from logic.gutils import template_utils
        template_utils.init_tempate_mall_i_item(item, item_id, isget=global_data.player.get_item_num_by_no(item_id) > 0, show_icon_up=percent_up, templatePath=list_nd._templatePath, force_rare_degree=force_rare_degree)
        percent_up and item.lab_rate.SetColor('#SO')
        item.lab_rate.SetString(LotteryPreviewWidget.LOTTERY_INFO[self.cur_mode]['item_rate'][item_id])
        self._register_btn_click(item, item_id)
        item.btn_choose.SetNoEventAfterMoveRecursion(True, self._cancel_dist)
        item.btn_choose.SetClipObject(self.panel.list_review_all)
        if item_id == self.selected_item_id:
            item.btn_choose.SetSelect(True)
            self.selected_item = item
        else:
            item.btn_choose.SetSelect(False)

    def init_review_list(self, data_list):
        if not self._list_sview:
            self._list_sview = InfiniteScrollWidget(self.panel.list_review_all, self.panel, up_limit=300, down_limit=300)
        self._list_sview.update_data_list(data_list)
        self._list_sview.set_custom_add_item_func(self.add_scroll_elem)
        self._list_sview.set_check_view_interval(0.01)
        self.panel.stopActionByTag(self.CACHE_ACTION)
        self._list_sview.set_is_only_add(True)
        self._list_sview.update_scroll_view()

    def add_scroll_elem(self, data, is_back_item=True, index=-1):
        is_title = data.get('is_title')
        if is_title:
            temp_path = self.TITLE_TEMPLATE
        else:
            temp_path = self.ITEM_TEMPLATE

        def add_func--- This code section failed: ---

 219       0  LOAD_FAST             0  'ui_item'
           3  POP_JUMP_IF_FALSE    77  'to 77'

 220       6  LOAD_DEREF            0  'is_back_item'
           9  POP_JUMP_IF_FALSE    43  'to 43'

 221      12  LOAD_DEREF            1  'self'
          15  LOAD_ATTR             0  'panel'
          18  LOAD_ATTR             1  'list_review_all'
          21  LOAD_ATTR             2  'AddControl'
          24  LOAD_ATTR             1  'list_review_all'
          27  LOAD_GLOBAL           3  'True'
          30  LOAD_CONST            2  'bSetupCtrl'
          33  LOAD_GLOBAL           4  'False'
          36  CALL_FUNCTION_513   513 
          39  POP_TOP          
          40  JUMP_ABSOLUTE        77  'to 77'

 223      43  LOAD_DEREF            1  'self'
          46  LOAD_ATTR             0  'panel'
          49  LOAD_ATTR             1  'list_review_all'
          52  LOAD_ATTR             2  'AddControl'
          55  LOAD_ATTR             3  'True'
          58  LOAD_CONST            1  'bRefresh'
          61  LOAD_GLOBAL           3  'True'
          64  LOAD_CONST            2  'bSetupCtrl'
          67  LOAD_GLOBAL           4  'False'
          70  CALL_FUNCTION_514   514 
          73  POP_TOP          
          74  JUMP_FORWARD          0  'to 77'
        77_0  COME_FROM                '74'

Parse error at or near `CALL_FUNCTION_513' instruction at offset 36

        use_cache = True
        if use_cache:
            cache_ret = self.item_cache.pop_item_by_json(temp_path, add_func)
        else:
            cache_ret = None
        if cache_ret:
            item_widget = cache_ret
        else:
            item_widget = global_data.uisystem.load_template_create(temp_path)
            add_func(item_widget)
        if temp_path == self.ITEM_TEMPLATE:
            self.init_item_cache({temp_path: (2, self.item_func_helper)})
        if is_title:
            ui_item = self.init_title_widget(item_widget, data)
        else:
            ui_item = self.init_item_widget(item_widget, data)
        return ui_item

    def init_title_widget(self, item_widget, data):
        if not G_IS_NA_PROJECT:
            rare_degree = data.get('rare_degree', RARE_DEGREE_0)
            if str(rare_degree) in self.category_floor:
                num = self.category_floor[str(rare_degree)][0]
                if self.cur_mode == '55' and rare_degree == RARE_DEGREE_5:
                    text_id = 611459
                else:
                    text_id = CATEGORY_FLOOR_TEXT_MAP[rare_degree]
                item_widget.lab_num_times.SetString(get_text_by_id(text_id, {'num': str(num)}))
            else:
                item_widget.lab_num_times.setVisible(False)
        else:
            item_widget.lab_num_times.setVisible(False)
        rare_degree = data.get('rare_degree', RARE_DEGREE_0)
        if self.cur_mode == '55' and rare_degree == RARE_DEGREE_5:
            rare_path = 'gui/ui_res_2/lottery/img_quality_splus_ss_small.png'
        else:
            rare_path = get_skin_rare_path_by_rare(rare_degree)
        item_widget.img_quatity.SetDisplayFrameByPath('', rare_path)
        mode_data = LotteryPreviewWidget.LOTTERY_INFO[self.cur_mode]
        rate_desc = str(mode_data[rare_degree]['rate'])
        item_widget.lab_rate.SetString(rate_desc)
        return item_widget

    def init_item_widget(self, item_widget, data):
        item_data = data.get('item_data', [])
        item_widget.list_all_item.SetInitCount(self.ITEM_PRE_ROW)
        rare_degree = data.get('rare_degree', None)
        need_reget_rare_degree = self.cur_mode == '55' and rare_degree == RARE_DEGREE_5
        for idx in range(0, len(item_data)):
            ele_data = item_data[idx]
            item_id = ele_data
            one_item = item_widget.list_all_item.GetItem(idx)
            one_item.setVisible(True)
            if need_reget_rare_degree:
                self.init_one_item(item_widget.list_all_item, one_item, item_id, percent_up=item_id in self.percent_up_item_dict, force_rare_degree=get_item_rare_degree(item_id))
            else:
                self.init_one_item(item_widget.list_all_item, one_item, item_id, percent_up=item_id in self.percent_up_item_dict, force_rare_degree=rare_degree)

        for idx in range(len(item_data), self.ITEM_PRE_ROW):
            one_item = item_widget.list_all_item.GetItem(idx)
            if one_item:
                one_item.setVisible(False)

        return item_widget

    def prepare_data(self, rare_list):
        data_list = []
        for rare_degree in rare_list:
            mode_data = LotteryPreviewWidget.LOTTERY_INFO[self.cur_mode]
            items = mode_data.get(rare_degree, {}).get('items', None)
            data_list.append({'is_title': True,'rare_degree': rare_degree})
            num = self.ITEM_PRE_ROW
            item_count = len(items)
            for idx in range(0, item_count, num):
                start = idx
                end = idx + num
                if end > item_count:
                    end = item_count
                data_list.append({'is_title': False,'rare_degree': rare_degree,'item_data': items[start:end]
                   })

        self._prepared_data_list = data_list
        return

    def on_remove_scroll_item(self, ui_item, index):
        if ui_item and ui_item.isValid():
            if ui_item.list_all_item:
                if self.item_cache.check_can_put_back(ui_item, self.ITEM_TEMPLATE):
                    self.item_cache.put_back_item_to_cache(ui_item, self.ITEM_TEMPLATE)
            elif self.item_cache.check_can_put_back(ui_item, self.TITLE_TEMPLATE):
                self.item_cache.put_back_item_to_cache(ui_item, self.TITLE_TEMPLATE)

    def jump_to_preview_item_no(self, item_no):
        if self._list_sview:
            data_list = self._prepared_data_list
            jump_to_index = 0
            for index, data_dict in enumerate(data_list):
                if not data_dict.get('is_title', False):
                    if item_no in data_dict.get('item_data', []):
                        jump_to_index = index
                        break

            self._list_sview.top_with_index(jump_to_index, None)
            ui_item = self._list_sview.get_list_item(jump_to_index)
            if ui_item:
                if hasattr(ui_item, 'list_all_item'):
                    first_item = ui_item.list_all_item.GetItem(0)
                    if first_item:
                        first_item.btn_choose.OnClick(None)
        return

    def jump_to_preview_rare_degree(self, rare_degree):
        if self._list_sview:
            data_list = self._prepared_data_list
            jump_to_index = 0
            for index, data_dict in enumerate(data_list):
                if not data_dict.get('is_title', False):
                    if rare_degree == data_dict.get('rare_degree', []):
                        jump_to_index = index
                        break

            self._list_sview.top_with_index(jump_to_index, None)
            ui_item = self._list_sview.get_list_item(jump_to_index)
            if ui_item:
                if hasattr(ui_item, 'list_all_item'):
                    first_item = ui_item.list_all_item.GetItem(0)
                    if first_item:
                        first_item.btn_choose.OnClick(None)
            self._list_sview.top_with_index(max(jump_to_index - 1, 0), None)
        return