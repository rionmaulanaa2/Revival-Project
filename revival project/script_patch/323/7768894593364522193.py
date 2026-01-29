# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/PVEBagBaseUI.py
from __future__ import absolute_import
import cc
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from logic.gutils.ui_salog_utils import add_uiclick_add_up_salog
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME, UI_TYPE_MESSAGE
from logic.gutils.item_utils import throw_item, get_item_name, is_package_item, is_health_item, is_food_item, is_summon_item, is_charger_item, is_consumable_item
from logic.gcommon.item.item_utility import is_mecha_battery, is_neutral_shop_candy
from logic.gutils.template_utils import init_item_tips_new, get_panel_show_all_offset, get_quality_pic_l
from logic.gcommon.const import BACKPACK_PART_OTHERS
from logic.gcommon.cdata.status_config import ST_USE_ITEM, ST_SKATE_MOVE, ST_SKATE
DRAG_X = 80
DRAG_BACKWARD_X = 60
DRAG_DELTA = 0.05
DRAG_TAN = 1.303
BAG_UI_TYPE_ITEM = 1
BAG_UI_TYPE_BLESS = 2

class PVEBagBaseUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    EXCEPT_HIDE_UI_LIST = ['FightLeftShotUI', 'MoveRockerUI', 'MoveRockerTouchUI', 'FightReadyTipsUI', 'PVEBagUI', 'PVEBlessConfUI']
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self, player=None):
        self.init_parameters()
        self.init_widgets()
        self.on_player_setted(player)
        self.process_events(True)

    def on_finalize_panel(self):
        self.register_event(False)
        self.process_events(False)
        self.destroy_widget('human_item_widget')
        self.destroy_widget('pve_bless_widget')

    def init_parameters(self):
        self.lplayer = None
        self._appearing = False
        self._other_ui_visible = True
        self.tips_ui_list = [
         self.panel.item_tips]
        self._tip_ui_height = 0
        self.cur_ui = None
        self.cur_ui_type = None
        self.cur_ui_sub_type = None
        self.cur_ui_item_data = None
        return

    def init_widgets(self):
        self.panel.drag_item.setVisible(False)

    def register_event(self, regist=True):
        if not self.lplayer:
            return
        func = self.lplayer.regist_event if regist else self.lplayer.unregist_event
        func('E_ITEM_DATA_CHANGED', self._on_item_data_changed)
        func('E_MEOW_COIN_CHANGE', self._on_meow_coin_change)

    def process_events(self, is_bind):
        econf = {'scene_player_setted_event': self.on_player_setted,
           'net_reconnect_before_destroy_event': self.on_reconnect,
           'net_login_reconnect_before_destroy_event': self.on_reconnect
           }
        if is_bind:
            global_data.emgr.bind_events(econf)
        else:
            global_data.emgr.unbind_events(econf)

    def on_player_setted(self, lplayer):
        if lplayer is None:
            if self._appearing:
                self.register_event(False)
            return
        else:
            self.lplayer = lplayer
            self.human_item_widget.init_widget()
            self.pve_bless_widget.init_widget()
            self.resize_bag_height()
            if self._appearing:
                self.register_event()
            self._on_meow_coin_change()
            return

    def on_reconnect(self, *args):
        self.disappear()

    def on_resolution_changed(self):
        self.appear()
        self.disappear()
        global_data.emgr.reconf_all_ui_end += self.on_reconf_all_ui_end

    def on_reconf_all_ui_end(self):
        self.appear()
        self.disappear()

    def appear(self):
        if self._appearing:
            return
        self._appearing = True
        self.clear_show_count_dict()
        self.set_other_ui_visible(False)
        self.panel.setVisible(True)
        self.register_event()
        self.human_item_widget.init_widget()
        self.pve_bless_widget.init_widget()
        self.resize_bag_height()
        if self.panel.IsPlayingAnimation('bag_disappear'):
            self.panel.StopAnimation('bag_disappear')
        self.panel.PlayAnimation('bag_show')
        add_uiclick_add_up_salog('open_bag_cnt', '')
        self._on_meow_coin_change()

    def disappear(self):
        if not self._appearing:
            return
        self._appearing = False
        self.set_other_ui_visible(True)
        self.register_event(False)
        if self.panel.IsPlayingAnimation('bag_show'):
            self.panel.StopAnimation('bag_show')
        self.panel.PlayAnimation('bag_disappear')
        self.panel.setVisible(False)
        for tip_ui in self.tips_ui_list:
            tip_ui.setVisible(False)

    def on_click_close_btn(self, *args):
        self.disappear()

    def isPanelVisible(self):
        return self._appearing and super(PVEBagBaseUI, self).isPanelVisible()

    def is_appeared(self):
        return self._appearing

    def get_block_ui_list(self):
        import copy
        from common.uisys import basepanel
        block_ui_list = copy.deepcopy(basepanel.MECHA_AIM_UI_LSIT)
        block_ui_list.append('StateChangeUI')
        return block_ui_list

    def set_other_ui_visible(self, visible):
        if self._other_ui_visible == visible:
            return
        self._other_ui_visible = visible
        if not visible:
            self.add_blocking_ui_list(self.get_block_ui_list())
            self.hide_main_ui(exceptions=self.EXCEPT_HIDE_UI_LIST, exception_types=(UI_TYPE_MESSAGE,))
        else:
            self.remove_blocking_ui_list()
            self.show_main_ui()
        ui = global_data.ui_mgr.get_ui('FightLeftShotUI')
        if ui:
            if not visible:
                ui.hide_aim_one_shot_button()
            else:
                ui.check_left_fire_ope()

    def on_bless_click(self, layer, touch, item_data):
        if not item_data:
            return
        cur_item_ui = layer.GetParent()
        self.cur_ui = cur_item_ui
        self.cur_ui_type = BAG_UI_TYPE_BLESS
        self.cur_ui_sub_type = BAG_UI_TYPE_BLESS
        self.cur_ui_item_data = item_data
        self.show_item_tips(self.tips_ui_list[0], item_data)
        self.panel.item_tips.SetTouchEnabledRecursion(False)

    def on_item_click(self, layer, touch, item_data):
        if not item_data:
            return
        cur_item_ui = layer.GetParent()
        cur_item_ui.item_sel.setVisible(True)
        cur_item_ui.pnl_right.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/panel/pnl_item_choose.png')
        cur_item_ui.name.SetColor('#SK')
        cur_item_ui.details.SetColor('#SK')
        cur_item_ui.img_line.SetColor('#SK')
        self.cur_ui = cur_item_ui
        self.cur_ui_type = BAG_UI_TYPE_ITEM
        self.cur_ui_sub_type = BAG_UI_TYPE_ITEM
        self.cur_ui_item_data = item_data
        self.show_item_tips(self.tips_ui_list[0], item_data)
        self.panel.item_tips.SetTouchEnabledRecursion(False)

    def on_item_drag(self, layer, touch, item_data):
        if not item_data:
            return
        start_wpos = touch.getStartLocation()
        wpos = touch.getLocation()
        dx = wpos.x - start_wpos.x
        dy = wpos.y - start_wpos.y
        if abs(dx) + abs(dy) < DRAG_DELTA and not self.panel.drag_item.isVisible():
            layer.SetSwallowTouch(False)
            return
        if abs(dx) * DRAG_TAN < abs(dy) and not self.panel.drag_item.isVisible():
            layer.SetSelect(False)
            layer.SetEnableTouch(True)
            layer.SetSwallowTouch(False)
            return
        lpos = self.panel.drag_item.getParent().convertToNodeSpace(wpos)
        self.show_drag_item(lpos, item_data.get('item_id'))
        self.show_delete_widget_item(wpos)
        layer.SetSwallowTouch(True)

    def on_item_end(self, layer, touch, item_data):
        if not item_data:
            return
        if not self.panel.drag_item.isVisible():
            return
        layer.SetSwallowTouch(False)
        self.panel.drag_item.setVisible(False)
        self.hide_delete_widget()
        wpos = touch.getLocation()
        if not self.is_in_empty_area(wpos):
            return

        def callback(num, item_data=item_data):
            throw_item(self.lplayer, BACKPACK_PART_OTHERS, item_data['entity_id'], num, None)
            return

        item_id = item_data.get('item_id', -1)
        item_name = get_item_name(item_id)
        self.discard_item(callback, item_name, item_data.get('count', 1), wpos)

    def show_drag_item(self, lpos, item_id, item_fashion=None):
        from logic.gutils import item_utils
        self.panel.drag_item.setPosition(lpos)
        self.panel.drag_item.setVisible(True)
        item_icon = self.panel.drag_item_icon
        if item_utils.is_gun(item_id):
            if item_fashion:
                item_icon.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(item_fashion))
            else:
                pic_path = item_utils.get_gun_pic_by_item_id(item_id, is_shadow=False)
                item_icon.SetDisplayFrameByPath('', pic_path)
        else:
            item_icon.SetDisplayFrameByPath('', item_utils.get_item_pic_by_item_no(item_id))

    def discard_item(self, callback, item_name, max_count, wpos=None):
        if not self.lplayer:
            return
        else:
            self.cur_ui = None
            if max_count <= 1:
                callback(max_count)
                return
            if wpos:
                width, height = self.panel.discard.GetContentSize()
                discard_scale = self.panel.discard.getScaleX()
                offset_x, offset_y = get_panel_show_all_offset(self.panel.discard, self.panel, wpos, 1, width * discard_scale, height * discard_scale)
                self.panel.discard.setPosition(wpos.x + offset_x, wpos.y + offset_y)
            from logic.gutils.template_utils import init_common_discard_pc
            init_common_discard_pc(self.panel.discard, item_name, max_count, callback)
            return

    def is_in_empty_area(self, wpos):
        return False

    def is_in_item_area(self, wpos):
        return False

    def show_delete_widget_item(self, wpos):
        pass

    def show_delete_widget_gun(self, wpos):
        pass

    def show_delete_widget_module(self, wpos):
        pass

    def show_delete_widget_clothes(self, wpos):
        pass

    def hide_delete_widget(self):
        pass

    def resize_bag_height(self):
        pass

    def show_item_tips(self, tip_ui, item_data, tip_no=0):
        tip_ui.setVisible(False)
        tip_ui.lab_item_name.SetString(item_data.get('name_text', ''))
        tip_ui.lab_item_describe.SetString(item_data.get('desc_text', ''))
        tip_ui.temp_item.GetItem(0).item.SetDisplayFrameByPath('', item_data.get('icon', ''))
        tip_ui.lab_paid_num.setVisible(False)
        tip_ui.setVisible(True)

    def remove_cur_select_state(self):
        if self.cur_ui is None:
            return
        else:
            if self.cur_ui_type == BAG_UI_TYPE_ITEM:
                item_sel = getattr(self.cur_ui, 'item_sel')
                if item_sel and item_sel.isValid():
                    item_sel.setVisible(False)
                else:
                    return
                item_id = self.cur_ui_item_data.get('item_id')
                path = 'box_res' if is_package_item(item_id) else 'item'
                item_conf = confmgr.get(path, str(item_id))
                pnl_right = getattr(self.cur_ui, 'pnl_right')
                if pnl_right and pnl_right.isValid():
                    pnl_right.SetDisplayFrameByPath('', get_quality_pic_l(item_conf.get('iQuality')))
                else:
                    return
                name = getattr(self.cur_ui, 'name')
                if name and name.isValid():
                    self.cur_ui.name.SetColor('#SW')
                else:
                    return
                details = getattr(self.cur_ui, 'details')
                if details and details.isValid():
                    self.cur_ui.details.SetColor('#SW')
                else:
                    return
                img_line = getattr(self.cur_ui, 'img_line')
                if img_line and img_line.isValid():
                    self.cur_ui.img_line.SetColor('#SW')
            return

    def use_bag_item(self, item_data):
        if not self.lplayer:
            return
        item_id = item_data['item_id']
        if is_health_item(item_id) or is_food_item(item_id) or is_mecha_battery(item_id) or is_neutral_shop_candy(item_id):
            self.use_medicine_item(item_id)
        elif is_summon_item(item_id):
            self.use_summon_item(item_id)
        elif is_charger_item(item_id):
            self.use_charger_item(item_id)
        elif is_consumable_item(item_id):
            self.use_throwable_item(item_id)

    def use_medicine_item(self, item_id):
        if not self.lplayer:
            return
        if not self.lplayer or not self.lplayer.ev_g_status_check_pass(ST_USE_ITEM):
            return
        self.lplayer.send_event('E_CTRL_USE_DRUG', item_id)
        self.lplayer.send_event('E_ITEMUSE_TRY', item_id)

    def use_summon_item(self, item_id):
        if not self.lplayer:
            return
        if not self.lplayer or not self.lplayer.ev_g_status_check_pass(ST_USE_ITEM):
            return
        if not self.lplayer.ev_g_control_human() or self.lplayer.ev_g_get_state(ST_SKATE):
            self.lplayer.send_event('E_SHOW_MESSAGE', get_text_by_id(19055))
            return
        self.lplayer.send_event('E_ITEMUSE_TRY', item_id)

    def use_charger_item(self, item_id):
        if not self.lplayer:
            return
        if not self.lplayer or not self.lplayer.ev_g_status_check_pass(ST_USE_ITEM):
            return
        if not self.lplayer.ev_g_control_human():
            self.lplayer.send_event('E_SHOW_MESSAGE', get_text_by_id(19055))
            return
        self.lplayer.send_event('E_ITEMUSE_TRY', item_id)

    def use_throwable_item(self, item_id):
        if not self.lplayer or not item_id:
            return
        if not self.lplayer.ev_g_status_check_pass(ST_USE_ITEM):
            return
        if self.lplayer.ev_g_get_state(ST_SKATE_MOVE):
            self.lplayer.send_event('E_SHOW_MESSAGE', get_text_by_id(19055))
            return
        self.lplayer.send_event('E_ITEMUSE_TRY', item_id)

    def get_lplayer(self):
        if not global_data.player or not global_data.player.logic:
            return None
        else:
            return global_data.player.logic

    def _on_meow_coin_change(self):
        if not self.lplayer or not self.lplayer.is_valid():
            return
        bag_num, bag_size = self.lplayer.ev_g_meow_bag_info() or (0, 0)
        safe_box_num, safe_box_size = self.lplayer.ev_g_meow_safe_box_info() or (0,
                                                                                 0)
        self.panel.nd_all.lab_all_num.SetString('%d/%d' % (bag_num, bag_size))
        self.panel.nd_all.lab_all_num.nd_auto_fit.img_full.setVisible(bag_num == bag_size)
        self.panel.nd_box.lab_box_num.SetString('%d/%d' % (safe_box_num, safe_box_size))
        self.panel.nd_box.lab_box_num.nd_auto_fit.img_full.setVisible(safe_box_num == safe_box_size)