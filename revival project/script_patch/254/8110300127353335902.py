# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/season_shop/NeutralShopUI.py
from __future__ import absolute_import
import six_ex
import math
from cocosui import cc
from common import utilities
from logic.gcommon.cdata import dan_data
from logic.gcommon.cdata import season_data
from logic.gutils import template_utils
from logic.gutils import season_utils
from logic.gutils import task_utils
from logic.gutils import item_utils
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from mobile.common.EntityManager import EntityManager
from logic.gutils import item_utils
from logic.gcommon.time_utility import get_server_time

class NeutralShopUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_s4_shop/battle_shop_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_close',
       'btn_tips.OnClick': 'on_rule_btn'
       }
    MOUSE_CURSOR_TRIGGER_SHOW = True
    GLOBAL_EVENT = {'update_shop_buy_history_event': 'on_update_shop_buy_history_event',
       'update_shop_entity_ace_coins_event': 'on_update_shop_entity_ace_coins',
       'scene_player_setted_event': 'on_scene_player_setted',
       'update_shop_refresh_time_event': 'update_refresh_time',
       'on_item_data_changed_event': 'on_item_data_change',
       'update_neutral_shop_goods_change_event': 'on_shop_goods_changed',
       'observer_module_changed_event': 'refresh_modules',
       'on_clothes_data_changed_event': '_on_clothes_data_changed'
       }
    HOT_KEY_FUNC_MAP = {'scene_interaction': 'keyboard_interaction'
       }

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.hide_main_ui(['SceneInteractionUI'])
        self.update_ace_coin()
        self.hide()

    def init_parameters(self):
        self._shop_entity_id = None
        self._player_entity_id = None
        if global_data.player:
            self._player_entity_id = global_data.player.id
        self._goods_data = {}
        self._refresh_id = None
        self._ace_coin = 0
        return

    def set_shop_entity_id(self, entity_id):
        self._shop_entity_id = entity_id
        neutral_shop_ent = EntityManager.getentity(entity_id)
        if not (neutral_shop_ent and neutral_shop_ent.logic):
            return
        info = neutral_shop_ent.logic.ev_g_shop_sell_goods_info()
        if not info:
            return
        goods_data, refresh_id = info
        next_refresh_server_time = global_data.neutral_shop_battle_data.get_shop_refresh_time()
        self.set_goods_data(goods_data, refresh_id)
        self.show()
        self.panel.stopAllActions()
        self.start_check_pos_player()
        self.update_next_refresh_time(next_refresh_server_time)

    def start_check_pos_player(self):
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.check_pos),
         cc.DelayTime.create(1)])))

    def check_pos(self):
        if self._shop_entity_id:
            neutral_shop_ent = EntityManager.getentity(self._shop_entity_id)
            if neutral_shop_ent and neutral_shop_ent.logic and global_data.player and global_data.player.logic:
                pos = global_data.player.logic.ev_g_position()
                if pos:
                    is_enter, _ = neutral_shop_ent.logic.ev_g_check_enter_consoloe_zone(pos)
                    if is_enter:
                        return
        self.close()

    def set_goods_data(self, goods_data, refresh_id):
        self._goods_data = goods_data
        self._refresh_id = refresh_id
        self.refresh_goods_show(goods_data)
        self.refresh_item_show(self._goods_data)

    def refresh_goods_show(self, goods_data):
        self.panel.list_item.SetInitCount(len(goods_data))
        all_item = self.panel.list_item.GetAllItem()
        pos_list = sorted(six_ex.keys(goods_data))
        for idx, pos in enumerate(pos_list):
            ui_item = self.panel.list_item.GetItem(idx)
            goods_id = goods_data[pos]
            self.init_goods_item(ui_item, pos, goods_id)

        self.refresh_limit_status()

    def init_goods_item(self, ui_item, pos, goods_id):
        good_conf = confmgr.get('neutral_shop_config', 'goods_data', str(pos), str(goods_id), default={})
        item_id = good_conf.get('item_no')
        from logic.gutils.item_utils import get_item_pic_by_item_no
        ui_item.img_item.SetDisplayFrameByPath('', get_item_pic_by_item_no(item_id))
        txt_sort = confmgr.get('neutral_shop_type_conf', str(good_conf.get('goods_type')), 'iItemTypeDesc', default='')
        ui_item.lab_sort.SetString(txt_sort)
        ui_item.img_bar.SetDisplayFrameByPath('', item_utils.get_battle_item_rare_degree_pic_by_item_no(item_id, 1))
        price = good_conf.get('sell_price', '1000')
        ui_item.lab_price.SetString(str(price))
        ui_item.lab_name.SetString(item_utils.get_item_name(item_id))
        special_effect_text_id = good_conf.get('special_effect_text_id', '')
        if special_effect_text_id:
            ui_item.lab_special.SetString(special_effect_text_id)
        else:
            ui_item.lab_special.SetString('')
        ui_item.temp_btn_buy.btn_common.SetText(get_text_by_id(80166))

        @ui_item.temp_btn_buy.btn_common.callback()
        def OnClick(btn, touch):
            if self._ace_coin >= price and global_data.player and global_data.neutral_shop_battle_data:
                goods_buy_history, shop_history = global_data.neutral_shop_battle_data.get_shop_buy_history(self._shop_entity_id, self._refresh_id, self._player_entity_id)
                meet_buy_limit, msg_id = self.can_meet_buy_num_limit(pos, goods_id, goods_buy_history, shop_history)
                if not meet_buy_limit:
                    global_data.game_mgr.show_tip(get_text_by_id(msg_id))
                    return
                neutral_shop_ent = EntityManager.getentity(self._shop_entity_id)
                if not (neutral_shop_ent and neutral_shop_ent.logic):
                    return
                neutral_shop_ent.logic.send_event('E_BUY_GOODS', global_data.player.id, [(str(goods_id), 1)])
            elif self._ace_coin < price:
                global_data.game_mgr.show_tip(get_text_by_id(81438))

    def refresh_limit_status(self):
        if not global_data.neutral_shop_battle_data:
            return
        goods_buy_history, shop_history = global_data.neutral_shop_battle_data.get_shop_buy_history(self._shop_entity_id, self._refresh_id, self._player_entity_id)
        pos_list = sorted(six_ex.keys(self._goods_data))
        for idx, pos in enumerate(pos_list):
            goods_id = self._goods_data[pos]
            ui_item = self.panel.list_item.GetItem(idx)
            if not ui_item:
                continue
            shop_max_num = self.get_buy_limit_per_shop(pos, goods_id)
            bought_num = shop_history.get(str(goods_id), 0)
            if shop_max_num - bought_num <= 0:
                color = '#SR'
            else:
                color = '#SW'
            b_str = color + str(shop_max_num - bought_num) + '#n'
            ui_item.lab_num_limit.SetString(get_text_by_id(81439, {'bought': b_str,'all': shop_max_num}))
            limit_num_all = self.get_buy_limit_all_shop(pos, goods_id)
            limit_num_all_left = limit_num_all - goods_buy_history.get(str(goods_id), 0)
            ui_item.lab_quantity.SetString(str(limit_num_all_left))
            ui_item.nd_sold_out.setVisible(limit_num_all_left <= 0)
            good_conf = confmgr.get('neutral_shop_config', 'goods_data', str(pos), str(goods_id), default={})
            sell_price = good_conf.get('sell_price', 0)
            meet_buy_limit, _ = self.can_meet_buy_num_limit(pos, goods_id, goods_buy_history, shop_history)
            if self._ace_coin >= sell_price and meet_buy_limit:
                ui_item.temp_btn_buy.btn_common.SetShowEnable(True)
            else:
                ui_item.temp_btn_buy.btn_common.SetShowEnable(False)

    def on_finalize_panel(self):
        self.show_main_ui()
        global_data.ui_mgr.close_ui('GameRuleDescUI')

    def update_ace_coin(self):
        self._ace_coin = 0
        if self._player_entity_id:
            self._ace_coin = global_data.neutral_shop_battle_data.get_entity_ace_coins(self._player_entity_id)
        self.panel.lab_price.SetString(str(self._ace_coin))
        self.refresh_limit_status()

    def on_close(self, btn, touch):
        self.close()

    def on_update_shop_entity_ace_coins(self, entity_id, money):
        if entity_id == self._player_entity_id:
            self.update_ace_coin()

    def on_scene_player_setted(self, player):
        if player:
            self._player_entity_id = player.id
            self.update_ace_coin()
        else:
            self._player_entity_id = None
        return

    def on_update_shop_buy_history_event(self, *args):
        self.refresh_limit_status()

    def can_meet_buy_num_limit(self, good_pos, goods_id, goods_buy_history, shop_bought_history):
        limit_num = self.get_buy_limit_per_shop(good_pos, goods_id)
        if limit_num > 0 and shop_bought_history.get(str(goods_id), 0) >= limit_num:
            return (False, 81436)
        limit_num_all = self.get_buy_limit_all_shop(good_pos, goods_id)
        if limit_num_all > 0 and goods_buy_history.get(str(goods_id), 0) >= limit_num_all:
            return (False, 81437)
        return (True, '')

    def get_buy_limit_per_shop(self, good_pos, goods_id):
        good_config = confmgr.get('neutral_shop_config', 'goods_data', str(good_pos), str(goods_id), default={})
        if not good_config:
            return 0
        return good_config.get('limit_num', 0)

    def get_buy_limit_all_shop(self, good_pos, goods_id):
        good_config = confmgr.get('neutral_shop_config', 'goods_data', str(good_pos), str(goods_id), default={})
        if not good_config:
            return 0
        return good_config.get('limit_num_all', 0)

    def on_rule_btn(self, btn, click):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(19522, 19523)

    def update_next_refresh_time(self, next_refresh_time_stamp):

        def timer_func(pass_time):
            remain_time = int(math.ceil(next_refresh_time_stamp - get_server_time()))
            if remain_time <= 0:
                remain_time = 0
            self.panel.lab_time.SetString(get_text_by_id(19524, {'n': remain_time}))

        cur_time = get_server_time()
        if cur_time >= next_refresh_time_stamp:
            timer_func(0)
            return
        timer_func(0)
        self.panel.lab_time.StopTimerAction()
        self.panel.lab_time.TimerAction(timer_func, int(next_refresh_time_stamp - cur_time) + 2, interval=0.2)

    def keyboard_interaction(self, msg, keycode):
        self.close()

    def update_refresh_time(self, next_refresh_server_time):
        self.update_next_refresh_time(next_refresh_server_time)

    def on_item_data_change(self, item_data):
        self.refresh_item_show(self._goods_data)

    def refresh_modules(self):
        self.refresh_item_show(self._goods_data)

    def _on_clothes_data_changed(self, dress_pos):
        self.refresh_item_show(self._goods_data)

    def refresh_item_show(self, goods_data):
        if not global_data.cam_lplayer:
            return
        else:
            pos_list = sorted(six_ex.keys(goods_data))
            for idx, pos in enumerate(pos_list):
                goods_id = self._goods_data[pos]
                good_conf = confmgr.get('neutral_shop_config', 'goods_data', str(pos), str(goods_id), default={})
                item_id = good_conf.get('item_no')
                ui_item = self.panel.list_item.GetItem(idx)
                if not ui_item:
                    continue
                state = self.get_statue_of_buying_module_or_exoskeleton_item(global_data.cam_lplayer, item_id)
                if state is None:
                    ui_item.nd_have.setVisible(False)
                else:
                    ui_item.nd_have.setVisible(not state)

            return

    def get_statue_of_buying_module_or_exoskeleton_item(self, lplayer, item_id):
        from logic.gcommon.item import item_utility as iutil
        from logic.gutils.item_utils import is_exoskeleton_equip
        if is_exoskeleton_equip(item_id):
            return lplayer.ev_g_compare_armor_level(item_id)
        else:
            if iutil.is_mecha_module_item(item_id):
                return lplayer.ev_g_mecha_can_install_module(item_id)
            return None

    def on_shop_goods_changed(self, shop_entity_id, refresh_id, goods_data):
        if str(shop_entity_id) == str(self._shop_entity_id):
            self.set_goods_data(goods_data, refresh_id)