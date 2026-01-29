# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/live/LiveGuessUI.py
from __future__ import absolute_import
import six_ex
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_CLOSE
from common.live.live_agent_mgr import LiveAgentMgr
from logic.gcommon.common_utils.local_text import get_text_by_id
import time
import game3d
import render
from cocosui import cc
from logic.gcommon.common_utils.text_utils import check_review_words
from common.cfg import confmgr
from logic.gcommon.cdata.round_competition import gen_bet_item, gen_bet_item_list
from logic.gutils import item_utils
from logic.gutils import mall_utils
from logic.gutils import observe_utils

class LiveGuessUI(BasePanel):
    PANEL_CONFIG_NAME = 'live/open_live_guess'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn',
       'temp_btn_support.btn_common.OnClick': 'on_click_support'
       }
    GLOBAL_EVENT = {'player_money_info_update_event': '_on_player_info_update'
       }

    def on_init_panel(self, *args, **kwargs):
        self.panel.temp_btn_support.btn_common.EnableCustomState(True)
        self._last_click_time = 0
        self._click_cd = 2
        self.on_init_data()

    def on_init_data(self):
        self.cur_tab_btn = None
        self.cur_select_index = None
        self.own_currency = 0
        self.price_data = []
        self.battle_id = None
        self.uid = None
        self.comp_id = None
        self.comp_round = None
        self.rate = 1.0
        return

    def init_play_data(self, data=None):
        self.data = data
        head = self.data.get('head_photo', 0)
        name_lab = self.data.get('char_name', '')
        win = self.data.get('win_cnt', 0)
        rate = self.data.get('bet_ratio', 1.0)
        self.rate = rate
        if rate is None:
            self.rate = 1.0
        head_path = 'gui/ui_res_2/item/role_head/%s.png' % str(head)
        comp_id = self.data.get('comp_id', 'SUMMER23_CN')
        cur_round = self.data.get('round', 1)
        self.uid = self.data.get('uid', None)
        self.battle_id = self.data.get('battle_id', None)
        self.comp_id = comp_id
        self.comp_round = cur_round
        bet_dic = gen_bet_item(comp_id, cur_round, 1)
        key_list = list(six_ex.keys(bet_dic))
        currency_id = int(key_list[0])
        own_currency = self.get_money_num(currency_id)
        self.currency_id = currency_id
        self.own_currency = own_currency or 0
        self.panel.img_head.SetDisplayFrameByPath('', head_path)
        self.panel.lab_name.SetString(name_lab)
        self.panel.lab_win.SetString(get_text_by_id(930011).format(win))
        self.panel.lab_value_rate.SetString(str(self.rate))
        icon_png = item_utils.get_money_icon(currency_id)
        self.panel.lab_currency.SetString(get_text_by_id(931022).format('#SW<img="%s", scale=0>#n' % icon_png))
        self.panel.lab_got.SetString(get_text_by_id(930024).format(own_currency))
        price_data = gen_bet_item_list(comp_id, cur_round)
        self.price_data = price_data
        list_btn = self.panel.list_btn
        list_btn.SetInitCount(len(price_data))
        all_items = list_btn.GetAllItem()
        for i, widget in enumerate(all_items):
            info = price_data[i]
            widget.temp_money.lab_price.SetString(str(info.get('price', 0)))
            widget.temp_money.lab_price.img_price.SetDisplayFrameByPath('', info.get('icon'))
            widget.temp_money.lab_price.img_price.setScale(0.2, 0.2)
            widget.temp_money.lab_price.lab_price_before.setVisible(False)

            @widget.btn.callback()
            def OnClick(btn, touch, item=widget, index=i):
                if self.cur_tab_btn:
                    self.cur_tab_btn.SetSelect(False)
                self.cur_tab_btn = btn
                self.cur_select_index = index
                self.cur_tab_btn.SetSelect(True)
                self.update_price_state(index)
                self.panel.temp_btn_support.btn_common.SetSelect(True)

        self.update_price_state()
        has_guessed = observe_utils.check_has_battle_observe_bet()
        if has_guessed:
            self.panel.lab_reward.setScale(0)
            self.panel.lab_value_rate.setScale(0)
            self.panel.lab_rate.setScale(0)
            self.panel.temp_btn_support.btn_common.SetText(930028)
            self.panel.temp_btn_support.btn_common.SetEnable(False)
            bet_info = observe_utils.get_battle_observe_bet_item_on_player(self.uid)
            if bet_info.get(str(self.currency_id), 0) > 0:
                for i, widget in enumerate(all_items):
                    info = price_data[i]
                    if info.get('price', 0) == bet_info.get(str(self.currency_id), 0):
                        self.cur_tab_btn = widget.btn
                        self.cur_select_index = i
                        self.cur_tab_btn.SetSelect(True)
                        self.update_price_state(i)

                    @widget.btn.callback()
                    def OnClick(btn, touch, item=widget, index=i):
                        pass

        else:
            self.panel.temp_btn_support.btn_common.setVisible(True)
        return

    def update_price_state(self, index=None):
        list_btn = self.panel.list_btn
        all_items = list_btn.GetAllItem()
        for i, widget in enumerate(all_items):
            info = self.price_data[i]
            price = info.get('price', 0)
            if self.own_currency < price:
                widget.temp_money.lab_price.SetColor(15340307)
            elif index == i:
                widget.temp_money.lab_price.SetColor('#SW')
            else:
                widget.temp_money.lab_price.SetColor(8755896)

        if self.cur_tab_btn is not None and self.cur_select_index is not None:
            self.panel.lab_reward.setVisible(True)
            price_info = self.price_data[self.cur_select_index]
            price = price_info.get('price', 0)
            price = int(self.rate * price)
            currency_id = self.currency_id
            icon_png = item_utils.get_money_icon(currency_id)
            self.panel.lab_reward.SetString(get_text_by_id(931024, ['#SW<img="%s", scale=0>#n*%s' % (icon_png, price)]))
        else:
            self.panel.lab_reward.setVisible(False)
        return

    def on_finalize_panel(self):
        pass

    def on_click_close_btn(self, btn, touch):
        self.close()

    def on_click_support(self, btn, touch):
        if not global_data.player:
            return
        else:
            currency_id = self.currency_id
            icon_png = item_utils.get_money_icon(currency_id)
            if self.cur_tab_btn is None or self.cur_select_index is None:
                tips_txt = get_text_by_id(931026, ['#SW<img="%s", scale=0>#n' % icon_png])
                global_data.game_mgr.show_tip(tips_txt)
                return
            if not self.comp_id or not self.comp_round or not self.battle_id or not self.uid:
                return
            cur_time = time.time()
            if cur_time - self._last_click_time < self._click_cd:
                return
            self._last_click_time = cur_time
            info = self.price_data[self.cur_select_index]
            price = info.get('price', 0)
            if self.own_currency < price:
                global_data.game_mgr.show_tip(get_text_by_id(931032, ['#SW<img="%s", scale=0>#n' % icon_png]))
            else:
                global_data.player.bet_battle_top_player(self.battle_id, self.uid, self.comp_id, self.comp_round, self.cur_select_index + 1)
            return

    def _on_player_info_update(self, *args):
        if self.currency_id:
            own_currency = self.get_money_num(self.currency_id)
            self.own_currency = own_currency or 0
            self.panel.lab_got.SetString(get_text_by_id(930024).format(own_currency))
        self.update_price_state(self.cur_select_index)

    def get_money_num(self, currency_id):
        import logic.gcommon.item.item_const as iconst
        OWN_HANDLER = {iconst.ITEM_NO_GOLD: lambda player: player.get_gold(),
           iconst.ITEM_NO_DIAMOND: lambda player: player.get_diamond(),
           iconst.ITEM_NO_YUANBAO: lambda player: player.get_yuanbao()
           }
        if currency_id in OWN_HANDLER:
            return OWN_HANDLER[currency_id](global_data.player)
        else:
            return global_data.player.get_item_num_by_no(currency_id)