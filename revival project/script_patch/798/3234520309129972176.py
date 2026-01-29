# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/SeasonPassActiveGiftUI.py
import common.const.uiconst as ui_const
from common.uisys.basepanel import BasePanel
from logic.gutils.template_utils import init_price_template
from logic.gutils.template_utils import init_setting_slider3
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.gutils.mall_utils import check_yuanbao
from logic.gutils import item_utils, task_utils
from logic.gcommon.common_const.battlepass_const import SEASON_CARD
from logic.gcommon.item.item_const import RARE_DEGREE_4
from common.cfg import confmgr
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
TASK_LIST = [
 1451318, 1451319, 1451320, 1451321, 1451322, 1451323, 1451324, 1451325,
 1451326, 1451327, 1451328, 1451329, 1451330, 1451331, 1451332, 1451333,
 1451334, 1451335, 1451336]

class SeasonPassActiveGiftUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/active_gift/i_battle_pass_active_gift_reward'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = ui_const.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_back.OnClick': 'on_close'
       }
    GLOBAL_EVENT = {'buy_good_success': 'update_panel',
       'receive_task_reward_succ_event': 'update_panel',
       'receive_task_prog_reward_succ_event': 'update_panel',
       'task_prog_changed': 'update_panel',
       'season_pass_buy_active_gift': 'update_panel'
       }

    def on_init_panel(self, close_callback, *args):
        self.close_cb = close_callback
        self.init_parameters()
        self.init_panel()
        self.init_btn()
        self.panel.PlayAnimation('appear')
        self.panel.PlayAnimation('loop')
        self.update_panel()

    def init_panel(self, *args):
        from logic.gcommon.cdata import season_data
        from logic.gcommon import time_utility
        self.panel.list_item.SetInitCount(len(TASK_LIST))
        total_rewatd_num = 0
        for i, item in enumerate(self.panel.list_item.GetAllItem()):
            if i + 1 > len(TASK_LIST):
                return
            task_id = TASK_LIST[i]
            status = global_data.player.get_task_reward_status(task_id)
            reward_id = task_utils.get_task_reward(task_id)
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            reward_list = reward_conf.get('reward_list', [])
            if len(reward_list) < 1:
                return
            item_id, item_num = reward_list[0]
            init_tempate_mall_i_item(item.temp_item, item_id, item_num, isget=status == ITEM_RECEIVED, show_rare_degree=True, show_tips=True)
            total_rewatd_num += item_num

        cur_season = global_data.player.get_battle_season()
        start_time = time_utility.get_date_str('%Y.%m.%d', season_data.get_start_timestamp(cur_season))
        end_time = time_utility.get_date_str('%Y.%m.%d', season_data.get_end_timestamp(cur_season))
        self.panel.lab_tips_time.SetString(get_text_by_id(604006).format(start_time, end_time))
        self.panel.lab_total.SetString(get_text_by_id(635163).format(total_rewatd_num))

    def init_parameters(self, *args):
        from logic.gutils.battle_pass_utils import get_now_season_pass_data
        self._sp_data = get_now_season_pass_data()
        self.per_gift_prog = task_utils.get_total_prog(TASK_LIST[0]) if len(TASK_LIST) > 0 else 10

    def init_btn(self, *args):
        from logic.gutils import template_utils

        @self.panel.temp_btn_buy.btn_major.unique_callback()
        def OnClick(btn, touch, *args):
            ui = SeasonPassActiveBuyLevelUI(None)
            return

        @self.panel.temp_btn_go.btn_major.unique_callback()
        def OnClick(btn, touch, *args):
            from logic.gutils.jump_to_ui_utils import jump_to_task_ui
            from logic.gcommon.common_const.task_const import TASK_TYPE_SEASON
            jump_to_task_ui(TASK_TYPE_SEASON)

        @self.panel.btn_describe.unique_callback()
        def OnClick(*args):
            from cocosui import cc
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(635186), get_text_by_id(635185))
            x, y = self.panel.btn_describe.GetPosition()
            wpos = self.panel.btn_describe.GetParent().ConvertToWorldSpace(x, y)
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
            template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

    def update_panel(self, *args):
        if not global_data.player:
            return
        active_gift_tasks = global_data.player.get_active_gift_tasks()
        can_receive_tasks = []
        sp_lv, _ = global_data.player.get_battlepass_info()
        sp_lv += global_data.player.get_unfinished_lv()
        lv_buy_max = min(len(TASK_LIST) * self.per_gift_prog, int((self._sp_data.SEASON_PASS_LV_CAP - sp_lv) / self.per_gift_prog) * self.per_gift_prog)
        reward_got = 0
        for i, item in enumerate(self.panel.list_item.GetAllItem()):
            if i + 1 > len(TASK_LIST):
                return
            task_id = TASK_LIST[i]
            if task_id not in active_gift_tasks:
                item.bar_prog.prog_0.setVisible(False)
                item.bar_prog.prog_1.setVisible(False)
            else:
                prog = global_data.player.get_task_prog(task_id)
                item.prog_0.setVisible(True)
                item.prog_1.setVisible(True)
                item.prog_1.SetPercentage(float(max(0, prog - i * self.per_gift_prog)) * 100 / self.per_gift_prog)
                item.prog_0.SetPercentage(100)
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNRECEIVED:
                can_receive_tasks.append(str(task_id))
            elif status == ITEM_RECEIVED:
                reward_id = task_utils.get_task_reward(task_id)
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                reward_list = reward_conf.get('reward_list', [])
                if len(reward_list) < 1:
                    return
                item_id, item_num = reward_list[0]
                reward_got += item_num
            item.temp_item.nd_get.setVisible(status == ITEM_RECEIVED)
            item.temp_item.nd_lock.setVisible(task_id not in global_data.player.get_active_gift_tasks())
            item.temp_item.nd_get_tips.setVisible(status == ITEM_UNRECEIVED)
            item.bar_level.SetEnable(status == ITEM_UNGAIN)
            item.bar_level.SetText(get_text_by_id(83532).format((i + 1) * self.per_gift_prog))

            @item.temp_item.btn_choose.unique_callback()
            def OnClick(btn, touch, task_id=task_id, *args):
                if not global_data.player:
                    return
                global_data.player.receive_task_reward(task_id)

        can_buy_gift = lv_buy_max > 0
        upgrade_lv = global_data.player.get_active_gift_lv_upgrade()
        buy_lv = global_data.player.get_active_gift_lv_buy()
        self.panel.lab_tips_got.SetString(get_text_by_id(635159).format(reward_got))
        self.panel.temp_btn_get.setVisible(len(can_receive_tasks) > 0)
        self.panel.temp_btn_buy.setVisible(len(can_receive_tasks) <= 0)
        self.panel.temp_btn_go.setVisible(upgrade_lv < buy_lv)
        self.panel.temp_btn_buy.btn_major.SetEnable(can_buy_gift)
        self.panel.nd_not_purchased.setVisible(buy_lv <= 0)
        self.panel.nd_purchased.setVisible(buy_lv > 0)
        self.panel.lab_level.SetString(str(sp_lv))
        self.panel.lab_level_now.SetString(str(upgrade_lv))
        self.panel.lab_level_target.SetString(str(buy_lv))

        @self.panel.temp_btn_get.btn_major.unique_callback()
        def OnClick(btn, touch, can_receive_tasks=can_receive_tasks, *args):
            global_data.player.receive_tasks_reward(can_receive_tasks)

    def on_close(self, *args):
        if self.close_cb:
            self.close_cb()
        self.close()

    def on_finalize_panel(self):
        pass


class SeasonPassActiveBuyLevelUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/active_gift/open_bp_active_gift_quantity'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = ui_const.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'temp_bg.btn_close.OnClick': 'on_close'
       }
    GLOBAL_EVENT = {}

    def on_init_panel(self, *args):
        sp_lv, _ = global_data.player.get_battlepass_info()
        sp_lv += global_data.player.get_unfinished_lv()
        self._now_lv = sp_lv
        self._des_lv = sp_lv
        self._last_des_lv = sp_lv
        self.per_gift_prog = task_utils.get_total_prog(TASK_LIST[0]) if len(TASK_LIST) > 0 else 10
        from logic.gutils.battle_pass_utils import get_now_season_pass_data
        self._sp_data = get_now_season_pass_data()
        self.lv_buy_max = min(len(TASK_LIST) * self.per_gift_prog, int((self._sp_data.SEASON_PASS_LV_CAP - sp_lv) / self.per_gift_prog) * self.per_gift_prog)
        self._item_no_to_item = {}
        self._rare_to_idx = {}
        self.panel.list_reward.DeleteAllSubItem()
        self._init_price()
        self._update_preview(self.per_gift_prog)
        self.init_btn()

    def init_btn(self, *args):

        @self.panel.temp_btn_buy.btn_common_big.unique_callback()
        def OnClick(btn, touch, *args):
            total_price = self._sp_data.SEASON_PASS_LV_PRICE * (self._des_lv - self._now_lv)
            if check_yuanbao(total_price, True):
                global_data.player.buy_battlepass_active_gift(self._des_lv - self._now_lv)
                self.close()

        @self.panel.temp_quantity.btn_increase_max.unique_callback()
        def OnClick(btn, touch, *args):
            self._update_preview(len(TASK_LIST) * self.per_gift_prog - self._des_lv + self._now_lv)

        @self.panel.temp_quantity.btn_minus.unique_callback()
        def OnClick(btn, touch, *args):
            self._update_preview(-self.per_gift_prog)

        @self.panel.temp_quantity.btn_plus.unique_callback()
        def OnClick(btn, touch, *args):
            self._update_preview(self.per_gift_prog)

    def update_panel(self, *args):
        pass

    def on_close(self, *args):
        self.close()

    def _init_price(self):
        price_info = {'original_price': self._sp_data.SEASON_PASS_LV_PRICE * self.per_gift_prog,
           'discount_price': None,
           'goods_payment': SHOP_PAYMENT_YUANBAO
           }
        price_node = self.panel.temp_price
        price_node.setVisible(True)
        init_price_template(price_info, price_node, DARK_PRICE_COLOR)
        return

    def _update_preview(self, add_lv):
        self._des_lv = add_lv + self._des_lv
        if self._des_lv > self._now_lv + self.lv_buy_max:
            self._des_lv = self._now_lv + self.lv_buy_max
        if self._des_lv < self._now_lv + self.per_gift_prog:
            self._des_lv = self._now_lv + self.per_gift_prog
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
                            item = self.panel.list_reward.AddTemplateItem(index=0)
                        else:
                            item = self.panel.list_reward.AddTemplateItem()
                        self._item_no_to_item[item_id] = {'item': item,'num': num}
                        init_tempate_mall_i_item(item, item_id, num, show_rare_degree=True, show_tips=True, show_jump=False)
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
                        idx = self.panel.list_reward.getIndexByItem(item)
                        if idx is not None:
                            self.panel.list_reward.DeleteItemIndex(idx)
                    elif now_number > 1:
                        item.lab_quantity.setVisible(True)
                        item.lab_quantity.SetString(str(now_number))
                    else:
                        item.lab_quantity.setVisible(False)

        self._last_des_lv = self._des_lv
        self.temp_quantity.lab_num.SetString(str(self._des_lv - self._now_lv))
        self.lab_tips.SetString(get_text_by_id(860275, args={'num': (self._des_lv - self._now_lv) * self._sp_data.SEASON_PASS_LV_PRICE,'level': self._des_lv - self._now_lv}))
        return

    def on_click_close(self, *args):
        self.close()

    def update_price(self):
        price_node = self.panel.temp_price
        total_price = self._sp_data.SEASON_PASS_LV_PRICE * (self._des_lv - self._now_lv)
        price_node.lab_price.SetString(str(total_price))
        txt_color = '#SS' if check_yuanbao(total_price, pay_tip=False) else '#SR'
        price_node.lab_price.SetColor(txt_color)