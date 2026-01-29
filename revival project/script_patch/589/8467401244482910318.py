# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LuckScore/LuckScoreRankListUI.py
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from logic.comsys.lottery.LuckScore.LuckScoreTotalRankWidget import LuckScoreTotalRankWidget
from logic.comsys.lottery.LuckScore.LuckScoreWeekRankWidget import LuckScoreWeekRankWidget
from logic.gutils.mall_utils import check_lucky_score_rank_week_likes_red_point, check_lucky_score_rank_total_likes_red_point
from logic.gcommon.common_const.luck_score_const import LUCK_SCORE_TOTAL_TYPE, LUCK_SCORE_WEEK_TYPE
from common.cfg import confmgr
from common.const import uiconst
from logic.gcommon.common_const.rank_const import RANK_TYPE_LUCK_WEEK, RANK_TYPE_LUCK_TOTAL

class LuckScoreRankListUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'mall/luck/open_mall_luck_rank'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    TEMPLATE_NODE_NAME = 'pnl'
    UI_ACTION_EVENT = {'panel.pnl.btn_close.OnClick': 'on_close'
       }

    def on_close(self, *args):
        self.close()

    def on_init_panel(self, lottery_id=None):
        self.init_parameters(lottery_id)
        self.process_event(True)
        self.init_event()
        self.init_rank_bar()
        self.refresh_red_point()

    def on_finalize_panel(self):
        self.process_event(False)
        super(LuckScoreRankListUI, self).on_finalize_panel()
        for widget in self.tab_widgets.values():
            widget.destroy()

    def init_parameters(self, lottery_id):
        self.lottery_id = lottery_id
        continual_goods_id = confmgr.get('lottery_page_config', str(lottery_id), 'continual_goods_id')
        self.item_no = confmgr.get('mall_config', str(continual_goods_id), 'item_no')
        self.tab_widgets = {}
        self.tab_list = [{'index': 0,'text': 634629,'widget_func': self.init_week_template,'tips': 634634,'rank_type': RANK_TYPE_LUCK_WEEK}, {'index': 1,'text': 634630,'widget_func': self.init_total_template,'tips': 634635,'rank_type': RANK_TYPE_LUCK_TOTAL}]

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'message_on_luck_rank_like_data': self.refresh_red_point
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_event(self):

        @self.panel.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(634644, 634871)

    def init_rank_bar(self):
        pnl = self.panel.pnl

        def init_rank_btn(node, data):
            node.btn_tab.SetText(get_text_by_id(data.get('text', '')))

        def rank_btn_click_cb(ui_item, data, idx):
            self._set_lab_tips(data)
            index = data.get('index', 0)
            if index in self.tab_widgets:
                for ind in self.tab_widgets:
                    widget = self.tab_widgets[ind]
                    widget.setVisible(index == ind)

            else:
                widget_func = data.get('widget_func')
                if widget_func:
                    _nd = global_data.uisystem.load_template_create('mall/luck/i_mall_luck_rank_list', self.pnl.nd_list)
                    _nd.SetPosition('50%', '50%')
                    widget_wrapper = widget_func(_nd)
                    self.tab_widgets[index] = widget_wrapper
                    for ind in self.tab_widgets:
                        cur_widget = self.tab_widgets[ind]
                        cur_widget.setVisible(index == ind)

        self._rank_bar_wrapper = WindowTopSingleSelectListHelper()
        self._rank_bar_wrapper.set_up_list(pnl.list_tab, self.tab_list, init_rank_btn, rank_btn_click_cb)
        self._rank_bar_wrapper.set_node_click(pnl.list_tab.GetItem(0))

    def _set_lab_tips(self, data):
        self.panel.lab_tips.setString(get_text_by_id(data.get('tips')))
        rank_type = data.get('rank_type').format(self.item_no)
        luck_rank_data = confmgr.get('luck_rank_data').get(rank_type)
        if not luck_rank_data:
            return
        min_score = luck_rank_data.get('min_score')
        self.panel.lab_tips2.setString(get_text_by_id(634767).format(min_score))

    def init_total_template(self, nd):
        return LuckScoreTotalRankWidget(nd)

    def init_week_template(self, nd):
        return LuckScoreWeekRankWidget(nd)

    def refresh_red_point(self, luck_type=None):
        has_total_red_point = check_lucky_score_rank_total_likes_red_point(self.lottery_id)
        has_week_red_point = check_lucky_score_rank_week_likes_red_point(self.lottery_id)
        list_tab = self.panel.pnl.list_tab
        if luck_type == LUCK_SCORE_WEEK_TYPE:
            list_tab.GetItem(0).red_point.setVisible(has_week_red_point)
        elif luck_type == LUCK_SCORE_TOTAL_TYPE:
            list_tab.GetItem(1).red_point.setVisible(has_total_red_point)
        else:
            list_tab.GetItem(0).red_point.setVisible(has_week_red_point)
            list_tab.GetItem(1).red_point.setVisible(has_total_red_point)