# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryNew/LotteryLuckScoreWidgetNew.py
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from logic.comsys.lottery.LuckScore.LuckScoreTotalRankWidget import LuckScoreTotalRankWidget
from logic.comsys.lottery.LuckScore.LuckScoreWeekRankWidget import LuckScoreWeekRankWidget
from logic.gutils.mall_utils import check_lucky_score_rank_week_likes_red_point, check_lucky_score_rank_total_likes_red_point, get_goods_item_open_date, check_limit_time_lottery_open_info
from logic.gcommon.common_const.luck_score_const import LUCK_SCORE_TOTAL_TYPE, LUCK_SCORE_WEEK_TYPE
from common.cfg import confmgr
from common.const import uiconst
from logic.gcommon.common_const.rank_const import RANK_TYPE_LUCK_WEEK, RANK_TYPE_LUCK_TOTAL
from logic.gutils import loop_lottery_utils
from logic.gcommon import time_utility as tutil
import six_ex

class LotteryLuckScoreWidgetNew(object):

    def __init__(self, panel, lottery_id, nd_rank_history):
        self.panel = panel
        self.lottery_id = lottery_id
        self.nd_rank_history = nd_rank_history
        self.on_init_panel()

    def on_init_panel(self):
        self.init_parameters()
        self.init_rank_bar()
        self.refresh_red_point()
        self.process_event(True)

    def destroy(self):
        self.process_event(False)
        for widget in six_ex.values(self.tab_widgets):
            widget.destroy()
            widget = None

        return

    def init_parameters(self):
        self.tab_widgets = {}
        self.tab_list = [{'index': 0,'text': 634629,'widget_func': self.init_week_template,'rank_type': RANK_TYPE_LUCK_WEEK,'check_click_func': self.check_week_click_func}, {'index': 1,'text': 634630,'widget_func': self.init_total_template,'rank_type': RANK_TYPE_LUCK_TOTAL}]
        continual_goods_id = confmgr.get('lottery_page_config', str(self.lottery_id), 'continual_goods_id')
        self._lottery_item_no = confmgr.get('mall_config', str(continual_goods_id), 'item_no')
        if loop_lottery_utils.is_loop_collection_lottery(self.lottery_id):
            goods_open_info, shop_open_info = loop_lottery_utils.get_loop_lottery_open_info(self.lottery_id)
            opening = True if goods_open_info else False
            if opening:
                left_time = goods_open_info[2] - tutil.time()
            else:
                left_time = -1
        else:
            single_goods_id = confmgr.get('lottery_page_config', self.lottery_id, 'single_goods_id')
            open_date_range = get_goods_item_open_date(single_goods_id)
            opening, left_time = check_limit_time_lottery_open_info(open_date_range)
        if not opening or left_time <= 0:
            self._is_lottery_close = True
            self._cur_select_index = 1
        else:
            self._is_lottery_close = False
            self._cur_select_index = 0

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'message_on_luck_rank_like_data': self.refresh_red_point
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_rank_bar(self):
        list_tab = self.panel.list_tab

        def init_rank_btn(node, data):
            node.btn_tab.SetText(get_text_by_id(data.get('text', '')))

        def rank_btn_click_cb(ui_item, data, idx):
            check_click_func = data.get('check_click_func')
            if check_click_func and callable(check_click_func):
                if check_click_func():
                    cur_item = list_tab.GetItem(self._cur_select_index)
                    self._rank_bar_wrapper.set_node_select(cur_item)
                    return
            global_data.emgr.on_show_record_open_box_widget_event.emit()
            self._set_lab_tips(data)
            index = data.get('index', 0)
            self._cur_select_index = index
            if index in self.tab_widgets:
                self.tab_widgets[index].show_default_info()
                for ind in self.tab_widgets:
                    cur_widget = self.tab_widgets[ind]
                    cur_widget.setVisible(index == ind)

            else:
                widget_func = data.get('widget_func')
                if widget_func:
                    _nd = global_data.uisystem.load_template_create('mall/i_lottery_rank_list', self.panel.temp_list)
                    _nd.SetPosition('50%', '50%')
                    widget_wrapper = widget_func(_nd)
                    self.tab_widgets[index] = widget_wrapper
                    self.tab_widgets[index].show_default_info()
                    for ind in self.tab_widgets:
                        cur_widget = self.tab_widgets[ind]
                        cur_widget.setVisible(index == ind)

        self._rank_bar_wrapper = WindowTopSingleSelectListHelper()
        self._rank_bar_wrapper.set_up_list(list_tab, self.tab_list, init_rank_btn, rank_btn_click_cb)
        self._rank_bar_wrapper.set_node_click(list_tab.GetItem(self._cur_select_index))

    def refresh(self):
        list_tab = self.panel.list_tab
        self._rank_bar_wrapper.set_node_click(list_tab.GetItem(0))

    def _set_lab_tips(self, data):
        rank_type = data.get('rank_type').format(self._lottery_item_no)
        luck_rank_data = confmgr.get('luck_rank_data').get(rank_type)
        if not luck_rank_data:
            self.panel.lab_tips_rank.setString('')
            return
        self.panel.lab_tips_rank.setString(get_text_by_id(634767).format(luck_rank_data.get('min_score', 0)))

    def init_total_template(self, nd):
        return LuckScoreTotalRankWidget(nd, self.lottery_id, self.panel.temp_rank_self, self._is_lottery_close)

    def init_week_template(self, nd):
        return LuckScoreWeekRankWidget(nd, self.lottery_id, self.panel.temp_rank_self, self._is_lottery_close)

    def check_week_click_func(self):
        if self._is_lottery_close:
            global_data.game_mgr.show_tip(get_text_by_id(635079))
        return self._is_lottery_close

    def refresh_red_point(self, luck_type=None):
        has_total_red_point = check_lucky_score_rank_total_likes_red_point(self.lottery_id)
        has_week_red_point = check_lucky_score_rank_week_likes_red_point(self.lottery_id)
        list_tab = self.panel.list_tab
        if luck_type == LUCK_SCORE_WEEK_TYPE:
            list_tab.GetItem(0).red_point.setVisible(has_week_red_point)
        elif luck_type == LUCK_SCORE_TOTAL_TYPE:
            list_tab.GetItem(1).red_point.setVisible(has_total_red_point)
        else:
            list_tab.GetItem(0).red_point.setVisible(has_week_red_point)
            list_tab.GetItem(1).red_point.setVisible(has_total_red_point)