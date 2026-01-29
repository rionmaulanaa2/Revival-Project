# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SeasonBuyLevelWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gutils import item_utils
from logic.gutils.mall_utils import check_yuanbao
from logic.gutils.template_utils import init_price_template
from logic.gutils.template_utils import init_setting_slider3
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gcommon.item.item_const import RARE_DEGREE_4
from logic.gcommon.common_const.battlepass_const import SEASON_CARD
from logic.gcommon.common_const.battlepass_const import ROTATE_FACTOR
from .SeasonBaseUIWidget import SeasonBaseUIWidget
from .BattlePassDisplayWidget import BattlePassDisplayWidget

class SeasonBuyLevelWidget(SeasonBaseUIWidget):

    def re_display(self):
        if not self._displaying_item_no:
            global_data.emgr.change_model_display_scene_item.emit(None)
            return
        else:
            self._display_widget.display_award(self._displaying_item_no, reset_display_type=True)
            return

    def __init__(self, parent_ui, panel, close_call_back=None):
        self.global_events = {'season_pass_update_lv': self.init_show,
           'player_money_info_update_event': self.update_price,
           'season_pass_open_type': self._init_card_buy_btn
           }
        super(SeasonBuyLevelWidget, self).__init__(parent_ui, panel)
        self.panel.setVisible(True)
        self._displaying_item_no = None
        self._close_call_back = close_call_back
        self._select_item = None
        self._display_widget = BattlePassDisplayWidget(display_cb=self._display_cb)
        self.init_show()
        return

    def init_show(self, *args):
        sp_lv, _ = global_data.player.get_battlepass_info()
        self._now_lv = sp_lv
        self._des_lv = sp_lv
        self._last_des_lv = sp_lv
        self._item_no_to_item = {}
        self._rare_to_idx = {}
        from logic.gutils.battle_pass_utils import get_now_season_pass_data
        self._sp_data = get_now_season_pass_data()
        self.panel.list_buy_award.DeleteAllSubItem()
        self._init_price()
        self._update_preview(1)
        self._init_ui_event()
        self.panel.PlayAnimation('appear')
        init_setting_slider3(self.panel.temp_slider, 1, self._sp_data.SEASON_PASS_LV_CAP - self._now_lv, 608021, self._update_preview)

    def _init_price(self):
        from logic.gcommon.const import SHOP_PAYMENT_YUANBAO
        price_info = {'original_price': self._sp_data.SEASON_PASS_LV_PRICE,
           'discount_price': None,
           'goods_payment': SHOP_PAYMENT_YUANBAO
           }
        price_node = self.panel.temp_price_special
        init_price_template(price_info, price_node, DARK_PRICE_COLOR)
        return

    def _init_ui_event(self):

        def _on_click_buy(*args):
            total_price = self._sp_data.SEASON_PASS_LV_PRICE * (self._des_lv - self._now_lv)
            if check_yuanbao(total_price, True):
                global_data.player.activate_battlepass_lv(str(self._des_lv - self._now_lv))

        self.panel.btn_buy_special.BindMethod('OnClick', _on_click_buy)

        def on_model_drag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

        self.panel.nd_special_reward.BindMethod('OnDrag', on_model_drag)
        self.panel.btn_close.BindMethod('OnClick', self.on_click_close)
        self._init_card_buy_btn()

    def _init_card_buy_btn(self, *args):
        if not global_data.player:
            return
        if global_data.player.has_buy_final_card():
            self.panel.btn_up.UnBindMethod('OnClick')
            self.panel.btn_up.setVisible(False)
        else:
            self.panel.btn_up.setVisible(True)
            self.panel.btn_up.BindMethod('OnClick', self._on_click_buy_card)

    def _on_click_buy_card(self, *args):
        from logic.gutils.battle_pass_utils import get_buy_season_card_ui_name
        if global_data.player and not global_data.player.has_buy_final_card():
            global_data.ui_mgr.show_ui(get_buy_season_card_ui_name(), 'logic.comsys.battle_pass')

    def _update_preview(self, add_lv):
        self._des_lv = add_lv + self._now_lv
        if self._des_lv > self._sp_data.SEASON_PASS_LV_CAP:
            self._des_lv = self._sp_data.SEASON_PASS_LV_CAP
        if self._des_lv < self._now_lv + 1:
            self._des_lv = self._now_lv + 1
        self.panel.lab_buy_title.SetString('{}'.format(self._des_lv))
        self.panel.lab_level_now.SetString('{}'.format(self._now_lv))
        self.update_price()
        if self._des_lv > self._last_des_lv:
            XRANGE_END = self._des_lv
            XRANGE_BEG = self._last_des_lv
            SHOW = True
        else:
            XRANGE_END = self._last_des_lv
            XRANGE_BEG = self._des_lv
            SHOW = False
        for lv in range(XRANGE_BEG + 1, XRANGE_END + 1):
            reward_list = item_utils.get_battle_pass_reward_id_list(lv, SEASON_CARD, consider_buy_card=True)
            if not reward_list:
                continue
            for item_id, num in reward_list:
                if SHOW:
                    item_info = self._item_no_to_item.setdefault(item_id, {})
                    if not item_info:
                        rare_degree = item_utils.get_item_rare_degree(item_id, num)
                        if rare_degree == RARE_DEGREE_4:
                            item = self.panel.list_buy_award.AddTemplateItem(index=0)
                        else:
                            item = self.panel.list_buy_award.AddTemplateItem()
                        self._item_no_to_item[item_id] = {'item': item,'num': num}

                        def on_click_callback(sel_item=item, reward=item_id):
                            self._displaying_item_no = reward
                            self._display_widget.display_award(reward)
                            if self._select_item and self._select_item.isValid():
                                self._select_item.btn_choose.SetSelect(False)
                            self._select_item = sel_item
                            self._select_item.btn_choose.SetSelect(True)

                        init_tempate_mall_i_item(item, item_id, num, show_rare_degree=True, callback=on_click_callback)
                    else:
                        self._item_no_to_item[item_id]['num'] += num
                        now_number = self._item_no_to_item[item_id]['num']
                        if now_number > 1:
                            lab_nd = self._item_no_to_item[item_id]['item'].lab_quantity
                            lab_nd.setVisible(True)
                            lab_nd.SetString(str(now_number))
                else:
                    if not self._item_no_to_item.get(item_id):
                        return
                    self._item_no_to_item[item_id]['num'] -= num
                    now_number = self._item_no_to_item[item_id]['num']
                    item = self._item_no_to_item[item_id]['item']
                    if now_number <= 0:
                        self._item_no_to_item.pop(item_id)
                        idx = self.panel.list_buy_award.getIndexByItem(item)
                        if idx is not None:
                            self.panel.list_buy_award.DeleteItemIndex(idx)
                    elif now_number > 1:
                        item.lab_quantity.setVisible(True)
                        item.lab_quantity.SetString(str(now_number))
                    else:
                        item.lab_quantity.setVisible(False)

        self._last_des_lv = self._des_lv
        first_item = self.panel.list_buy_award.GetItem(0)
        if first_item and not first_item == self._select_item:
            first_item.btn_choose.OnClick(None)
        if not first_item:
            self.panel.nd_empty.setVisible(True)
            self.panel.nd_display.setVisible(False)
        else:
            self.panel.nd_empty.setVisible(False)
            self.panel.nd_display.setVisible(True)
        return

    def on_click_close(self, *args):
        if self._display_widget:
            self._display_widget.clear_model_display()
        if self._close_call_back:
            self._close_call_back(False)
        self._close_call_back = None
        self.destroy()
        return

    def update_price(self):
        price_node = self.panel.temp_price_special
        total_price = self._sp_data.SEASON_PASS_LV_PRICE * (self._des_lv - self._now_lv)
        price_node.lab_price.SetString(str(total_price))
        txt_color = '#SS' if check_yuanbao(total_price, pay_tip=False) else '#SR'
        price_node.lab_price.SetColor(txt_color)

    def _display_cb(self, is_model, item_no):
        super(SeasonBuyLevelWidget, self)._display_cb(is_model, item_no)
        item_name = item_utils.get_lobby_item_name(item_no)
        item_desc = item_utils.get_lobby_item_desc(item_no)
        if is_model:
            self.panel.nd_special_reward.img_bar.lab_name.SetString(item_name)
            self.panel.nd_special_reward.lab_describe.SetString(item_desc)
            self.panel.nd_special_reward.img_bar.lab_name.setVisible(True)
        else:
            pic_path = item_utils.get_lobby_item_pic_by_item_no(item_no)
            self.panel.nd_common_reward.nd_item.nd_cut.img_item.SetDisplayFrameByPath('', pic_path)
            self.panel.nd_common_reward.lab_name.SetString(item_name)
            self.panel.nd_common_reward.lab_describe.SetString(item_desc)
        self.panel.nd_special_reward.setVisible(is_model)
        self.panel.nd_common_reward.setVisible(not is_model)

    def destroy(self):
        self._displaying_item_no = None
        self.destroy_widget('_display_widget')
        if self.panel and self.panel.isValid():
            self.panel.Destroy()
        self.panel = None
        self._sp_data = None
        super(SeasonBuyLevelWidget, self).destroy()
        return