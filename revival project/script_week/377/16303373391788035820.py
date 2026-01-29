# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryNew/LotteryNewPreviewWidgetV2.py
from __future__ import absolute_import
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_type, get_lobby_item_pic_by_item_no, get_item_rare_degree, REWARD_RARE_COLOR
from logic.comsys.lottery.LotteryPreviewWidget import LotteryPreviewWidget
from logic.comsys.lottery.LotteryNewPreviewWidget import LotteryNewPreviewWidget
from .LotteryShopWidgetNew import LotteryShopWidgetNew
from .LotteryLuckScoreWidgetNew import LotteryLuckScoreWidgetNew
from .RecordOpenBoxWidgetNew import RecordOpenBoxWidgetNew
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE_SKIN, L_ITME_TYPE_GUNSKIN, L_ITEM_YTPE_VEHICLE_SKIN, L_ITEM_TYPE_GESTURE
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from logic.client.const.mall_const import REVIEW_TAB_INDEX, SHOP_TAB_INDEX, LUCK_SCORE_TAB_INDEX
from logic.gutils.mall_utils import get_lottery_table_id_list
from logic.gutils import loop_lottery_utils
from logic.gcommon import time_utility as tutil

class LotteryNewPreviewWidgetV2(LotteryNewPreviewWidget):
    ITEM_TEMPLATE = 'mall/i_ss_lottery_review_list_group_item_new'
    TITLE_TEMPLATE = 'mall/i_lottery_review_list_group_title_new'
    ITEM_PRE_ROW = 2

    def __init__(self, panel, parent, mode, on_change_show_reward, show_callback=None, hide_callback=None, close_callback=None, data=None, default_tab_index=REVIEW_TAB_INDEX):
        super(LotteryNewPreviewWidgetV2, self).__init__(panel, parent, mode, on_change_show_reward, show_callback, hide_callback, close_callback)
        self.data = data
        self._default_tab_index = default_tab_index
        self._cur_select_tab_index = default_tab_index
        self._init_goods_id = None
        self._nd_histroy_widget = None
        self.init_tab_bar()
        return

    def init_parameters(self):
        super(LotteryNewPreviewWidgetV2, self).init_parameters()
        self._tab_info_list = [{'index': REVIEW_TAB_INDEX,'ui_node': self.panel.list_review_all,'refresh_func': self.refresh_review_widget}, {'index': SHOP_TAB_INDEX,'ui_node': self.panel.nd_exchange,'refresh_func': self.refresh_shop_widget}, {'index': LUCK_SCORE_TAB_INDEX,'ui_node': self.panel.nd_rank,'refresh_func': self.refresh_luck_score_widget}]
        self._has_init_index_list = []
        self._shop_widget = None
        self._luck_score_widget = None
        self._tab_bar_wrapper = None
        return

    def set_node_click(self, show_index=REVIEW_TAB_INDEX, init_goods_id=None):
        list_tab = self.panel.list_tab_top2
        self._init_goods_id = init_goods_id
        self._tab_bar_wrapper.set_node_click(list_tab.GetItem(show_index))

    def set_show_data(self):
        if not LotteryPreviewWidget.LOTTERY_INFO.get(self.cur_mode, None):
            global_data.player and global_data.player.request_reward_display_data(get_lottery_table_id_list())
            self.preview_list_initialized = False
            return
        else:
            self.show_callback and self.show_callback()
            if self.selected_item_id:
                self.on_change_show_reward(self.selected_item_id)
            self.is_showing = True
            return

    def show(self):
        self.set_show_data()
        self.show_panel()

    def show_panel(self):
        self.panel.setVisible(True)
        if not self.preview_list_initialized:
            if self._shop_widget:
                self._shop_widget.destroy()
                self._shop_widget = None
            if self._luck_score_widget:
                self._luck_score_widget.destroy()
                self._luck_score_widget = None
            if self._nd_histroy_widget:
                self._nd_histroy_widget.destroy()
                self._nd_histroy_widget = None
            self._has_init_index_list = []
            list_tab = self.panel.list_tab_top2
            self._tab_bar_wrapper.set_node_click(list_tab.GetItem(self._cur_select_tab_index))
        return

    def init_tab_bar(self):
        list_tab = self.panel.list_tab_top2

        def end_btn_click_cb(ui_item, data, index):
            self._cur_select_tab_index = index
            for tab_info in self._tab_info_list:
                is_visible = index == tab_info['index']
                tab_info['ui_node'].setVisible(is_visible)
                if is_visible:
                    tab_info['refresh_func']()

        def end_btn_can_click_cb(ui_item, data, index):
            if index in (SHOP_TAB_INDEX, LUCK_SCORE_TAB_INDEX):
                if loop_lottery_utils.is_loop_lottery(self.cur_mode):
                    goods_open_info, shop_open_info = loop_lottery_utils.get_loop_lottery_open_info(self.cur_mode)
                    lottery_closed = False
                    if not goods_open_info and not shop_open_info:
                        lottery_closed = True
                    else:
                        if shop_open_info:
                            shop_end_time = shop_open_info[2]
                            if shop_end_time - tutil.time() < 0.15:
                                lottery_closed = True
                        if lottery_closed:
                            global_data.game_mgr.show_tip(get_text_by_id(81354))
                            return False
            return True

        self._tab_bar_wrapper = WindowTopSingleSelectListHelper()
        self._tab_bar_wrapper.set_up_list(list_tab, self._tab_info_list, None, end_btn_click_cb, can_click_cb=end_btn_can_click_cb)
        self._tab_bar_wrapper.set_node_click(list_tab.GetItem(self._default_tab_index))
        return

    def init_one_item(self, list_nd, item, item_id, percent_up=False, force_rare_degree=None):
        name = get_lobby_item_name(item_id)
        item.lab_name.SetString(name)
        img_banner = item.img_banner
        path = get_lobby_item_pic_by_item_no(item_id)
        img_banner.SetDisplayFrameByPath('', path)
        item_type = get_lobby_item_type(item_id)
        if item_type == L_ITEM_TYPE_MECHA_SKIN or item_type == L_ITEM_TYPE_ROLE_SKIN:
            img_banner.SetPosition('50%0', '50%79')
            img_banner.setScale(0.72)
        elif item_type == L_ITME_TYPE_GUNSKIN or item_type == L_ITEM_YTPE_VEHICLE_SKIN:
            img_banner.SetPosition('50%0', '50%64')
            img_banner.setScale(0.5)
        else:
            img_banner.SetPosition('50%0', '50%46')
            img_banner.setScale(0.36)
        rare_degree = get_item_rare_degree(item_id, ignore_imporve=True)
        color = REWARD_RARE_COLOR.get(rare_degree, 'orange')
        pic = 'gui/ui_res_2/lottery/bar_lottery_preview_item_{}.png'.format(color)
        item.btn_banner.SetFrames('', [pic, pic, ''])
        lab_pr = item.lab_pr
        percent_up and lab_pr.SetColor('#SO')
        lab_pr.SetString(LotteryPreviewWidget.LOTTERY_INFO[self.cur_mode]['item_rate'][item_id])
        self._register_btn_click(item, item_id)
        if item_id == self.selected_item_id:
            item.choose.setVisible(True)
            self.selected_item = item
        else:
            item.choose.setVisible(False)

    def _register_btn_click(self, item, item_id):

        @global_unique_click(item.btn_banner)
        def OnClick(layer, touch, *args):
            item_type = get_lobby_item_type(item_id)
            if item_type == L_ITEM_TYPE_GESTURE and item_id in LotteryPreviewWidget.LOTTERY_INFO['lottery_merge_item_info'][self.cur_mode]:
                index = randint(1, LotteryPreviewWidget.LOTTERY_INFO['lottery_merge_item_info'][self.cur_mode][item_id][0])
                real_item_id = LotteryPreviewWidget.LOTTERY_INFO['lottery_merge_item_info'][self.cur_mode][item_id][index]
                self.on_change_show_reward(real_item_id, get_lobby_item_name(item_id))
            else:
                self.on_change_show_reward(item_id)
            if self.selected_item and self.selected_item.isValid():
                self.selected_item.choose.setVisible(False)
            self.selected_item = item
            self.selected_item_id = item_id
            item.choose.setVisible(True)

    def refresh_review_widget(self):
        self._nd_histroy_widget and self._nd_histroy_widget.hide()
        self.parent.btn_shop.setVisible(True)
        if REVIEW_TAB_INDEX in self._has_init_index_list:
            self.refresh_show_model()
            return
        else:
            self._has_init_index_list.append(REVIEW_TAB_INDEX)
            self.refresh_preview_list(self.cur_mode, self.data.get('limited_item_id_list', None), self.data.get('percent_up_item_id_dict', {}))
            return

    def refresh_shop_widget(self):
        self._nd_histroy_widget and self._nd_histroy_widget.hide()
        self.parent.btn_shop.setVisible(False)
        if SHOP_TAB_INDEX in self._has_init_index_list:
            self.refresh_show_model()
            self._shop_widget._init_exchange_mall_list(self._init_goods_id)
            self._init_goods_id = None
            return
        else:
            self._has_init_index_list.append(SHOP_TAB_INDEX)
            if not self._shop_widget:
                self._shop_widget = LotteryShopWidgetNew(self.parent.nd_exchange, self.parent, self.on_change_show_reward, self.cur_mode, self._init_goods_id)
            self._init_goods_id = None
            return

    def refresh_luck_score_widget(self):
        if not self._nd_histroy_widget:
            self._nd_histroy_widget = RecordOpenBoxWidgetNew(self.parent.nd_rank_history)
        self._nd_histroy_widget.hide()
        self.on_change_show_reward(None)
        self.parent.btn_shop.setVisible(True)
        if LUCK_SCORE_TAB_INDEX in self._has_init_index_list:
            self._luck_score_widget.refresh()
            return
        else:
            self._has_init_index_list.append(LUCK_SCORE_TAB_INDEX)
            if not self._luck_score_widget:
                self._luck_score_widget = LotteryLuckScoreWidgetNew(self.parent.nd_rank, self.cur_mode, self.parent.nd_rank_history)
            return

    def refresh_show_model(self):
        if self._cur_select_tab_index == REVIEW_TAB_INDEX:
            self.on_change_show_reward(self.selected_item_id)
        elif self._cur_select_tab_index == SHOP_TAB_INDEX:
            self._shop_widget.refresh_show_model()
        elif self._cur_select_tab_index == LUCK_SCORE_TAB_INDEX:
            self.on_change_show_reward(None)
        return

    def get_cur_select_tab_index(self):
        return self._cur_select_tab_index

    def destroy(self):
        super(LotteryNewPreviewWidgetV2, self).destroy()
        if self._shop_widget:
            self._shop_widget.destroy()
            self._shop_widget = None
        if self._luck_score_widget:
            self._luck_score_widget.destroy()
            self._luck_score_widget = None
        if self._nd_histroy_widget:
            self._nd_histroy_widget.destroy()
            self._nd_histroy_widget = None
        return