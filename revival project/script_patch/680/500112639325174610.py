# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotterySpringFestival2022Widget.py
from __future__ import absolute_import
from logic.gutils.lobby_click_interval_utils import global_unique_click
from .LotteryArtCollectionWidget import LotteryArtCollectionWidget, DEFAULT_ICON_PATH, DEFAULT_TXT_COLOR, DEFAULT_OUT_LINE
from .LotterySpringFestival2022ShopWidget import LotterySpringFestival2022ShopWidget

class LotterySpringFestival2022Widget(LotteryArtCollectionWidget):

    def init_panel(self):
        super(LotteryArtCollectionWidget, self).init_panel()
        self._list_sview = None
        self.shop_widget = None
        self.panel.btn_shop.EnableCustomState(False)
        self.panel.lab_free_time.setVisible(False)
        self.panel.lab_change.SetString(81213)
        self.panel.nd_review.setVisible(False)
        self.panel.temp_red.setVisible(False)
        extra_data = self.data.get('extra_data', {})
        icon_path = extra_data.get('icon_path', DEFAULT_ICON_PATH) if extra_data else DEFAULT_ICON_PATH
        txt_color = eval(extra_data.get('text_color', DEFAULT_TXT_COLOR)) if extra_data else DEFAULT_TXT_COLOR
        out_line = eval(extra_data.get('out_line', DEFAULT_OUT_LINE)) if extra_data else DEFAULT_OUT_LINE
        act_txt_id = extra_data.get('act_text_id', None)
        shop_txt_id = extra_data.get('shop_text_id', None)
        self.panel.btn_activity.SetFrames('', [icon_path, icon_path, icon_path], False, None)
        self.panel.lab_btn_text.SetColor(txt_color)
        act_txt_id and self.panel.lab_btn_text.SetString(act_txt_id)
        shop_txt_id and self.panel.btn_shop.lab_shop_title.SetString(shop_txt_id)

        @global_unique_click(self.panel.btn_change)
        def OnClick(*args):
            self.preview_widget.show()

        @global_unique_click(self.panel.temp_btn_close.btn_back)
        def OnClick(*args):
            self.preview_widget.hide()

        @global_unique_click(self.panel.btn_question)
        def OnClick(*args):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            title, content = self.data.get('rule_desc', [608106, 608107])
            dlg.set_lottery_rule(title, content)

        @global_unique_click(self.panel.btn_shop)
        def OnClick(*args):
            if not self.shop_widget:
                return
            from logic.gutils.mall_utils import get_lottery_exchange_list
            exchange_lottery_list, lottery_exchange_goods = get_lottery_exchange_list()
            if self.lottery_id not in lottery_exchange_goods:
                global_data.game_mgr.show_tip(get_text_by_id(12128))
                return
            if self.panel.mall_box_buy.isVisible():
                self.shop_widget.parent_show()
            else:
                self.shop_widget.parent_hide()

        from common.cfg import confmgr
        ui_args = confmgr.get('lottery_page_config', str(self.lottery_id), 'advance_args', default=[])
        self.panel.btn_view.setVisible(bool(ui_args))

        @global_unique_click(self.panel.btn_view)
        def OnClick(btn, touch, ui_args=ui_args):
            if ui_args:
                global_data.ui_mgr.show_ui(*ui_args)

        @global_unique_click(self.panel.btn_history)
        def OnClick(btn, touch):
            global_data.emgr.lottery_history_open.emit()

        self._init_scroll_banner()
        self._init_buy_widget()
        self._init_preview_widget()
        self._init_shop_widget()
        self._init_rule_tag_list()
        if self.panel.lab_tips:
            self.panel.lab_tips.setVisible(True)
            txt_id = self.data.get('show_tip')
            txt = ''
            if txt_id:
                txt = get_text_by_id(txt_id)
            self.panel.lab_tips.SetString(txt)
        self.init_temporary_activity_entrance()
        self.init_extra_activity_entrance()
        self.check_show_shop()
        return

    def _init_shop_widget(self):

        def show_callback():
            if self.panel.mall_box_buy.isVisible():
                self.panel.PlayAnimation('shop_in')
            self.panel.btn_shop.SetSelect(True)
            self.panel.mall_box_buy.setVisible(False)
            global_data.emgr.refresh_switch_core_model_button_visible.emit(False)

        def hide_callback():
            if not self.panel.mall_box_buy.isVisible():
                self.panel.PlayAnimation('shop_out')
            self.panel.btn_shop.SetSelect(False)
            self.panel.mall_box_buy.setVisible(True)
            if self.panel.bar_review.isVisible():
                self.preview_widget.parent_show()
            else:
                self.refresh_show_model()
                global_data.emgr.refresh_switch_core_model_button_visible.emit(True)

        self.shop_widget = LotterySpringFestival2022ShopWidget(self.panel.nd_shop, self.panel, self.on_change_show_reward, self.lottery_id, show_callback=show_callback, hide_callback=hide_callback)

    def check_show_shop(self):
        if self.is_visible_close and self.data.get('show_shop', False):
            self.shop_widget and self.shop_widget.parent_show()
            self.panel.nd_granbelm.setVisible(False)
            return True
        return False

    def _show_shop(self):
        from common.utils.timer import CLOCK
        player = global_data.player
        extra_data = self.data.get('extra_data', {})
        tips_text_id = extra_data.get('tips_text_id', None)
        tips_item_id = extra_data.get('tips_item_id', 70400024)
        tips_goods_id = str(extra_data.get('tips_goods_id', '700400199'))
        if player and player.get_item_num_by_no(tips_item_id) >= 100 and not player.buy_num_all_dict.get(tips_goods_id, 0):
            self.panel.nd_tips.setVisible(True)
            if tips_text_id:
                self.panel.nd_tips.lab_tips_activity.SetString(tips_text_id)
            self.tips_anim_timer = global_data.game_mgr.register_logic_timer(self.tips_anim_end_callback, interval=120.0, times=1, mode=CLOCK)
        else:
            self.panel.nd_tips.setVisible(False)
        if not self.panel.mall_box_buy.isVisible():
            self.shop_widget.parent_show()
        else:
            self.preview_widget.parent_show()
        return