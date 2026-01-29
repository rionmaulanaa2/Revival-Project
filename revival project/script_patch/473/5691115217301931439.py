# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEShopUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_VKB_CLOSE
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from mobile.common.EntityManager import EntityManager
from logic.gutils.pve_utils import init_common_display_item, init_break_display_item, init_bless_display_item, get_bless_elem_res, check_elems_out_cnt, stop_movement
from logic.comsys.battle.pve.PVEBreakUpgradeWidget import PVEBreakUpgradeWidget
from logic.comsys.battle.pve.PVEBlessUpgradeWidget import PVEBlessUpgradeWidget
from logic.gcommon.common_utils.text_utils import get_color_str
from logic.gcommon.time_utility import get_server_time
from .PVESellUI import PVESellUI
NORMAL_COLOR = '0xFEFFFFFF'
CANT_BUY_COLOR = '0xF42551FF'

class PVEShopUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/shop/pve_shop_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_close',
       'btn_show.OnClick': 'on_show_info',
       'btn_refresh.OnClick': 'on_click_refresh',
       'btn_buy.OnClick': 'on_click_buy',
       'btn_sell.OnClick': 'on_click_sell'
       }
    T_ITEM = 1
    T_BREAK = 2
    T_BLESS = 3
    T_STORY = 4
    T_RANDOM_UP_BLESS = 5
    REFRESH_DUR = 0.5

    def on_init_panel(self, *args):
        super(PVEShopUI, self).on_init_panel(*args)
        self.init_params()
        self.init_widget()
        self.process_events(True)
        self.handle_cursor(True)
        self.panel.PlayAnimation('appear')
        stop_movement()

    def init_params(self):
        self.shop_eid = None
        self.crystal_num = global_data.player.logic.ev_g_crystal_stone()
        self.crystal_debt_limit = global_data.player.logic.ev_g_crystal_stone_debt_limit()
        self.mecha_id = 8001
        if global_data.player and global_data.player.logic:
            self.mecha_id = global_data.player.logic.ev_g_get_bind_mecha_type()
        self.break_conf = confmgr.get('mecha_breakthrough_data', str(self.mecha_id), default=None)
        self.bless_conf = confmgr.get('bless_data', default=None)
        self.item_conf = confmgr.get('pve_shop_data', default=None)
        self.select_idx = -1
        self.select_slot = -1
        self.break_upgrade_widget = None
        self.bless_upgrade_widget = None
        self.refresh_ts = 0
        return

    def init_widget(self):
        if not global_data.player or not global_data.player.logic:
            return
        self.panel.lab_money.SetString(str(self.crystal_num))
        self.init_break_upgrade_widget()
        self.init_bless_upgrade_widget()
        self.update_sell_btn_state()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'pve_update_crystal_num': self.update_crystal,
           'pve_cost_crystal_stone': self.update_crystal,
           'on_pve_boss_cleared_event': self.update_sell_btn_state,
           'on_pve_notify_reset_mecha': self.on_pve_notify_reset_mecha
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_events(False)
        self.handle_cursor(False)
        self.break_upgrade_widget and self.break_upgrade_widget.clear()
        self.bless_upgrade_widget and self.bless_upgrade_widget.clear()
        self.destroy_widget('break_upgrade_widget')
        self.destroy_widget('bless_upgrade_widget')
        super(PVEShopUI, self).on_finalize_panel()

    def init_goods(self, shop_eid, goods_data, refresh_price):
        print (
         'shop_eid', shop_eid)
        print ('goods_data', goods_data)
        print ('refresh_price', refresh_price)
        self.shop_eid = shop_eid
        shop = EntityManager.getentity(shop_eid)
        if not shop:
            return
        else:
            self.goods_data = goods_data
            self.refresh_price = refresh_price
            self.update_crystal()
            slot_list = list(goods_data.keys())
            slot_list.sort()
            self.panel.list_item.DeleteAllSubItem()
            self.panel.list_item.SetInitCount(len(slot_list))
            for idx, ui_item in enumerate(self.panel.list_item.GetAllItem()):
                slot = slot_list[idx]
                item_id, item_price, item_num, item_type = goods_data[slot]
                print (
                 'init_goods', item_id, item_price, item_num, item_type)
                tag_visible = False
                img_path = ''
                name_text = 0
                enable = True
                if item_type in (self.T_ITEM, self.T_STORY, self.T_RANDOM_UP_BLESS):
                    conf = self.item_conf.get(str(item_id), {})
                    name_text = conf['name_id']
                    img_path = conf['icon']
                elif item_type == self.T_BREAK:
                    break_data = global_data.player.logic.ev_g_mecha_breakthrough_data()
                    level = break_data.get(str(item_id), 0)
                    next_level = level + 1
                    conf = self.break_conf[str(item_id)].get(str(next_level), {})
                    if not conf:
                        enable = False
                        conf = self.break_conf[str(item_id)].get(str(level), {})
                    img_path = conf['icon']
                    name_text = conf['name_id']
                elif item_type == self.T_BLESS:
                    conf = self.bless_conf[str(item_id)]
                    img_path = conf['icon']
                    name_text = conf['name_id']
                    elem_id = conf.get('elem_id', None)
                    if elem_id:
                        tag_visible = True
                        tag_pnl, tag_icon = get_bless_elem_res(elem_id, ['tag', 'small_icon'])
                        ui_item.img_tag.SetDisplayFrameByPath('', tag_pnl)
                        ui_item.icon.SetDisplayFrameByPath('', tag_icon)
                    else:
                        tag_visible = False
                ui_item.img_tag.setVisible(tag_visible)
                ui_item.img_item.SetDisplayFrameByPath('', img_path)
                ui_item.lab_name.SetString(get_text_by_id(name_text))
                ui_item.lab_price.SetString(str(item_price))
                nd_got_visible = False
                if not enable or item_num == 0:
                    nd_got_visible = True
                ui_item.nd_got.setVisible(nd_got_visible)
                if item_num == -1:
                    ui_item.nd_got.setVisible(True)
                    ui_item.icon_tick.setVisible(False)
                ui_item.btn_describe.setVisible(False)

                @ui_item.btn_choose.unique_callback()
                def OnClick(_layer, _touch, _idx=idx, _slot=slot, _item_id=item_id, _item_price=item_price, _item_num=item_num, _item_type=item_type):
                    if not global_data.player or not global_data.player.logic:
                        return
                    self.switch_select_item(_idx, _slot)
                    self.init_display_item(_item_id, _item_type, _item_price)
                    self.update_buy_status(_slot, _item_price, _item_num)
                    if _item_num == -1:
                        if _item_type == self.T_BREAK:
                            global_data.emgr.battle_show_message_event.emit(get_text_by_id(443))
                        elif _item_type == self.T_BLESS:
                            if check_elems_out_cnt(_item_id):
                                global_data.emgr.battle_show_message_event.emit(get_text_by_id(538))
                            else:
                                global_data.emgr.battle_show_message_event.emit(get_text_by_id(442))

            self.update_refresh_status()
            default_item = self.panel.list_item.GetItem(0 if self.select_idx == -1 else self.select_idx)
            if not default_item:
                default_item = self.panel.list_item.GetItem(0)
            default_item.btn_choose.OnClick(None)
            shop = EntityManager.getentity(self.shop_eid)
            if not shop or not shop.logic:
                return
            global_data.emgr.pve_shop_closed_event.emit(shop.logic)
            return

    def switch_select_item(self, idx, slot):
        if idx != self.select_idx:
            ui_item = self.panel.list_item.GetItem(self.select_idx)
            ui_item and ui_item.btn_choose.SetSelect(False)
        ui_item = self.panel.list_item.GetItem(idx)
        ui_item.btn_choose.SetSelect(True)
        self.select_idx = idx
        self.select_slot = slot

    def init_display_item(self, item_id, item_type, item_price):
        self.panel.pnl_empty.setVisible(False)
        self.update_lab_price_buy(item_price)
        if item_type in (self.T_ITEM, self.T_STORY, self.T_RANDOM_UP_BLESS):
            self.panel.temp_item.setVisible(True)
            self.panel.temp_breakthrough.setVisible(False)
            self.panel.temp_energy.setVisible(False)
            init_common_display_item(self.panel.temp_item, item_id)
        elif item_type == self.T_BREAK:
            self.panel.temp_item.setVisible(False)
            self.panel.temp_breakthrough.setVisible(True)
            self.panel.temp_energy.setVisible(False)
            break_data = global_data.player.logic.ev_g_mecha_breakthrough_data()
            init_break_display_item(self.panel.temp_breakthrough, break_data, self.break_conf, item_id)
        elif item_type == self.T_BLESS:
            self.panel.temp_item.setVisible(False)
            self.panel.temp_breakthrough.setVisible(False)
            self.panel.temp_energy.setVisible(True)
            bless_id = str(item_id)
            cur_level = global_data.cam_lplayer.ev_g_bless_level(item_id)
            init_bless_display_item(self.panel.temp_energy, bless_id, cur_level)

    def update_lab_price_buy(self, item_price):
        color = NORMAL_COLOR if self.crystal_num + self.crystal_debt_limit >= item_price else CANT_BUY_COLOR
        color_str = get_color_str(color, item_price)
        self.panel.lab_price_buy.SetString(color_str)

    def update_crystal(self, *args):
        self.crystal_num = global_data.player.logic.ev_g_crystal_stone()
        self.panel.lab_money.SetString(str(self.crystal_num))
        if self.select_slot != -1 and self.select_slot in self.goods_data:
            _, price, num, _ = self.goods_data[self.select_slot]
            self.update_buy_status(self.select_slot, price, num)
            self.update_lab_price_buy(price)
        self.update_refresh_status()

    def update_buy_status(self, slot, item_price, item_num):
        self.panel.btn_buy.SetEnable(self.crystal_num + self.crystal_debt_limit >= item_price and item_num > 0)

    def update_refresh_status(self):
        self.panel.lab_refresh.setVisible(False)
        self.panel.lab_price_refresh.SetString(str(self.refresh_price))
        self.panel.btn_refresh.SetEnable(self.crystal_num + self.crystal_debt_limit >= self.refresh_price)

    def update_sell_btn_state(self):
        battle = global_data.player.get_battle()
        if not battle:
            self.panel.btn_sell.setVisible(False)
        pve_boss_cleared = battle.get_pve_boss_cleared()
        self.panel.btn_sell.setVisible(not pve_boss_cleared)

    def on_click_refresh(self, *args):
        shop = EntityManager.getentity(self.shop_eid)
        if not shop:
            return
        else:
            ts = get_server_time()
            if ts - self.refresh_ts > self.REFRESH_DUR:
                self.refresh_ts = ts
            else:
                global_data.game_mgr.show_tip(get_text_by_id(503))
                return
            shop.logic.send_event('E_CALL_SYNC_METHOD', 'refresh_pve_shop', (global_data.player.logic.id,), True, True)
            global_data.sound_mgr.post_event_2d_non_opt('Play_ui_pve_shop_refresh', None)
            return

    def on_click_buy(self, *args):
        shop = EntityManager.getentity(self.shop_eid)
        if not shop:
            return
        else:
            item_id, _, _, _ = self.goods_data[self.select_slot]
            cnt = global_data.cam_lplayer.ev_g_item_count(item_id)
            max_amount = confmgr.get('item', str(item_id), 'max_amount', default=0)
            if max_amount and cnt >= max_amount:
                global_data.game_mgr.show_tip(get_text_by_id(532))
                return
            shop.logic.send_event('E_CALL_SYNC_METHOD', 'pve_shop_buy_good', (global_data.player.logic.id, self.select_slot), True, True)
            global_data.sound_mgr.post_event_2d_non_opt('Play_ui_pve_shop_buy', None)
            return

    def on_click_sell(self, *args):
        PVESellUI(shop_eid=self.shop_eid)

    def on_close(self, *args):
        self.panel.PlayAnimation('disappear')
        delay = self.panel.GetAnimationMaxRunTime('disappear')
        self.panel.SetTimeOut(delay, lambda : self.close())

    def on_show_info(self, *args):
        ui = global_data.ui_mgr.get_ui('PVEInfoUI')
        ui and ui.close()
        global_data.ui_mgr.show_ui('PVEInfoUI', 'logic.comsys.control_ui')

    def handle_cursor(self, ret):
        if global_data.mouse_mgr:
            if ret:
                global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)
            else:
                global_data.mouse_mgr.add_cursor_hide_count(self.__class__.__name__)

    def on_pve_notify_reset_mecha(self, mecha_id):
        self.mecha_id = mecha_id
        self.break_conf = confmgr.get('mecha_breakthrough_data', str(self.mecha_id), default=None)
        self.init_goods(self.shop_eid, self.goods_data, self.refresh_price)
        return

    def init_break_upgrade_widget(self):
        self.break_upgrade_widget = PVEBreakUpgradeWidget(self.panel)

    def init_bless_upgrade_widget(self):
        self.bless_upgrade_widget = PVEBlessUpgradeWidget(self.panel)