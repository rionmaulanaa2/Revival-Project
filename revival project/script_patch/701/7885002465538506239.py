# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/King/KothCampShopPlayerWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gutils import item_utils
from logic.gcommon import const
from logic.gutils import koth_shop_utils
import time
from logic.gcommon import time_utility
import cc

class PlayerInfoWidgetBase(object):

    def __init__(self, panel, parent):
        self.panel = panel
        self._cur_sel_item = None
        self._is_binded = False
        self._goods_id_to_ui_item_dict = {}
        self._goods_id_to_item_info_dict = {}
        return

    def get_global_data_event_confs(self):
        return {}

    def process_event(self, is_bind):
        if is_bind == self._is_binded:
            return
        emgr = global_data.emgr
        econf = self.get_global_data_event_confs()
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)
        self._is_binded = is_bind

    def show(self):
        self.panel.setVisible(True)
        self.init_widget()
        self.process_event(True)

    def hide(self):
        self.panel.setVisible(False)
        if self._cur_sel_item:
            self.common_select_item(None, None)
        self._goods_id_to_ui_item_dict = {}
        self._goods_id_to_item_info_dict = {}
        self.process_event(False)
        return

    def destroy(self):
        self.process_event(False)
        self.panel = None
        self._goods_id_to_ui_item_dict = {}
        self._goods_id_to_item_info_dict = {}
        return

    def init_widget(self):
        pass

    def set_show_tips(self, text_id):
        self.panel.lab_tips.SetString(text_id)

    def common_select_item(self, ui_item, item_no, weapon_pos=0):
        self.set_list_item_selected(ui_item)
        ui_inst = global_data.ui_mgr.get_ui('KothCampShopUI')
        if ui_inst:
            ui_inst.on_player_choose_own_item(item_no, weapon_pos)

    def set_list_item_selected(self, ui_item):
        if self._cur_sel_item is not None and self._cur_sel_item.isValid():
            self._cur_sel_item.img_select.setVisible(False)
        self._cur_sel_item = ui_item
        if self._cur_sel_item:
            self._cur_sel_item.img_select.setVisible(True)
        return

    def on_player_choose_own_item(self, goods_id):
        if goods_id in self._goods_id_to_ui_item_dict:
            ui_item = self._goods_id_to_ui_item_dict.get(goods_id)
            if ui_item and ui_item.isValid():
                self.set_list_item_selected(ui_item)
        else:
            self.set_list_item_selected(None)
        return

    def set_item_no_widget(self, item_no, widget):
        if not item_no:
            return
        goods_id = koth_shop_utils.get_goods_id_by_item_id(item_no)
        if goods_id:
            self._goods_id_to_ui_item_dict[goods_id] = widget

    def get_goods_id_to_owned_item_no(self, goods_id):
        if goods_id in self._goods_id_to_item_info_dict:
            item_info = self._goods_id_to_item_info_dict.get(goods_id, {})
            return item_info
        return {}

    def set_item_no_info(self, item_no, item_data):
        goods_id = koth_shop_utils.get_goods_id_by_item_id(item_no)
        if goods_id:
            item_info = {'item_no': item_no}
            item_info.update(item_data)
            self._goods_id_to_item_info_dict[goods_id] = item_info


class PlayerWeaponInfoWidget(PlayerInfoWidgetBase):

    def get_global_data_event_confs(self):
        return {'on_weapon_data_switched_event': self._on_weapon_data_switched,'on_wpbar_switch_cur_event': self._on_weapon_data_changed,
           'on_observer_pick_up_weapon': self._on_weapon_data_changed,
           'on_observer_weapon_deleted': self._on_weapon_data_changed
           }

    def init_widget(self):
        weapon_list = [
         const.PART_WEAPON_POS_MAIN1, const.PART_WEAPON_POS_MAIN2, const.PART_WEAPON_POS_MAIN3]
        self.panel.list_equip.SetInitCount(len(weapon_list))
        self.init_weapon_widget(weapon_list)

    def _on_weapon_data_changed(self, *args):
        if not self.panel:
            return
        self.init_weapon_widget([const.PART_WEAPON_POS_MAIN1, const.PART_WEAPON_POS_MAIN2,
         const.PART_WEAPON_POS_MAIN3])

    def _on_weapon_data_switched(self, pos1, pos2):
        self.init_weapon_widget([pos1, pos2])

    def init_weapon_widget(self, pos_list):
        if global_data.player:
            player = global_data.player.logic if 1 else None
            return player or None
        else:
            from logic.gutils import template_utils
            hand_pos = player.share_data.ref_wp_bar_cur_pos
            self._goods_id_to_ui_item_dict = {}
            self._goods_id_to_item_info_dict = {}
            for pos in pos_list:
                weapon_obj = player.share_data.ref_wp_bar_mp_weapons.get(pos)
                weapon_data = None if weapon_obj is None else weapon_obj.get_data()
                if weapon_obj is None:
                    item_no = None if 1 else weapon_obj.get_id()
                    if weapon_data:
                        weapon_data['iBulletCap'] = weapon_obj.get_bullet_cap()
                    show_pos = self.get_pos_show_idx(pos)
                    if show_pos is None:
                        continue
                    item_widget = self.panel.list_equip.GetItem(show_pos)
                    if not item_widget:
                        continue
                    koth_shop_utils.init_mall_item_temp(item_widget, {'item_no': item_no})
                    self.set_item_no_widget(item_no, item_widget)
                    self.set_item_no_info(item_no, {'position': pos})

                    @item_widget.btn_item.callback()
                    def OnClick(btn, touch, item_widget=item_widget, item_no=item_no, pos=pos):
                        self.common_select_item(item_widget, item_no, pos)

            return

    def get_pos_show_idx(self, weapon_pos):
        dic = {const.PART_WEAPON_POS_MAIN1: 0,
           const.PART_WEAPON_POS_MAIN2: 1,
           const.PART_WEAPON_POS_MAIN3: 2
           }
        return dic.get(weapon_pos, None)

    def show(self):
        super(PlayerWeaponInfoWidget, self).show()

    def hide(self):
        super(PlayerWeaponInfoWidget, self).hide()

    def destroy(self):
        super(PlayerWeaponInfoWidget, self).destroy()


class PlayerArmorInfoWidget(PlayerInfoWidgetBase):

    def init_widget(self):
        from logic.gcommon.item import item_const as iconst
        self.show_list = [
         iconst.DRESS_POS_HEAD, iconst.DRESS_POS_ARMOR, iconst.DRESS_POS_LEG]
        self.panel.list_equip.SetInitCount(len(self.show_list))
        self.init_bone_equip_widget()

    def get_global_data_event_confs(self):
        return {'on_clothes_data_changed_event': self._on_clothes_data_changed
           }

    def _on_clothes_data_changed(self, dress_pos):
        self.init_bone_equip_widget()

    def init_bone_equip_widget(self):
        from logic.gcommon.item import item_const as iconst
        if global_data.player:
            player = global_data.player.logic if 1 else None
            return player or None
        else:
            from logic.gutils import template_utils
            default_icon = {iconst.DRESS_POS_HEAD: 'icon_helmet',
               iconst.DRESS_POS_ARMOR: 'icon_armor',
               iconst.DRESS_POS_LEG: 'icon_shose'
               }
            self._goods_id_to_ui_item_dict = {}
            self._goods_id_to_item_info_dict = {}
            clothes = player.ev_g_clothing()
            for idx, pos in enumerate(self.show_list):
                clothes_widget = self.panel.list_equip.GetItem(idx)
                clothes_data = clothes.get(pos, None)
                if clothes_data:
                    item_no = clothes_data['item_id'] if 1 else None
                    koth_shop_utils.init_mall_item_temp(clothes_widget, {'item_no': item_no})

                    @clothes_widget.btn_item.callback()
                    def OnClick(btn, touch, clothes_widget=clothes_widget, item_no=item_no):
                        self.common_select_item(clothes_widget, item_no)

                    self.set_item_no_widget(item_no, clothes_widget)
                    self.set_item_no_info(item_no, {})

            return


class PlayerModuleInfoWidget(PlayerInfoWidgetBase):

    def get_global_data_event_confs(self):
        return {'observer_module_changed_event': self.refresh_modules
           }

    def init_widget(self):
        from logic.gcommon.common_const import mecha_const
        self.panel.list_equip.SetTemplate('battle_koth/i_mall_item_module')
        self.panel.list_equip.SetInitCount(0)
        self.panel.list_equip.SetInitCount(mecha_const.MODULE_MAX_SLOT_COUNT)
        self.refresh_modules()

    def refresh_modules(self):
        from logic.gcommon.common_const import mecha_const
        if global_data.player:
            player = global_data.player.logic if 1 else None
            return player or None
        else:
            self._goods_id_to_ui_item_dict = {}
            self._goods_id_to_item_info_dict = {}
            if player:
                cur_module_config = player.ev_g_mecha_all_installed_module() or {}
                for show_slot in range(1, mecha_const.MODULE_MAX_SLOT_COUNT + 1):
                    ui_item = self.panel.list_equip.GetItem(show_slot - 1)
                    if not ui_item:
                        continue
                    if show_slot in cur_module_config:
                        card_id, item_id = cur_module_config[show_slot]
                        _, card_lv = player.ev_g_module_item_slot_lv(item_id)
                        self.init_module_item(ui_item, item_id, card_id, show_slot, card_lv)
                        self.set_item_no_widget(item_id, ui_item)
                        self.set_item_no_info(item_id, {})
                    else:
                        self.init_module_item(ui_item, None, None, show_slot, None)

            return

    def init_module_item(self, ui_item, module_id, conf, slot, card_lv):
        from logic.gutils import template_utils
        template_utils.init_module_temp_item(ui_item.temp_module, slot, conf, card_lv)

        @ui_item.btn_item.callback()
        def OnClick(btn, touch):
            self.common_select_item(ui_item, module_id)

    def hide(self):
        super(PlayerModuleInfoWidget, self).hide()
        self.panel.list_equip.SetTemplate('battle_koth/i_mall_item')
        self.panel.list_equip.SetInitCount(0)


class PlayerItemInfoWidget(PlayerInfoWidgetBase):

    def __init__(self, panel, parent):
        super(PlayerItemInfoWidget, self).__init__(panel, parent)
        self.only_check_list = set()

    def get_global_data_event_confs(self):
        return {'on_item_data_changed_event': self.on_item_data_change
           }

    def set_only_check_list(self, item_id_list):
        self.only_check_list = set(item_id_list)
        self.init_item_widget()

    def on_item_data_change(self, item_data):
        self.init_item_widget()

    def init_widget(self):
        pass

    def init_item_widget(self):
        from logic.gcommon.common_const import mecha_const
        if global_data.player:
            player = global_data.player.logic if 1 else None
            return player or None
        else:
            items = self.get_bag_item_list()
            total_count = max(len(items), 4)
            self.panel.list_equip.SetInitCount(total_count)
            all_items = self.panel.list_equip.GetAllItem()
            idx = 0
            for item_info in sorted(items, key=--- This code section failed: ---

 366       0  LOAD_GLOBAL           0  'item_utils'
           3  LOAD_ATTR             1  'item_sort_key'
           6  LOAD_ATTR             1  'item_sort_key'
           9  BINARY_SUBSCR    
          10  CALL_FUNCTION_1       1 
          13  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `BINARY_SUBSCR' instruction at offset 9
, reverse=True):
                entity_id, item_data = item_info
                item_widget = all_items[idx]
                idx += 1
                self.init_package_item_widget(item_widget, entity_id, item_data)
                if item_data is not None:
                    item_id = item_data['item_id'] if 1 else None
                    self.set_item_no_widget(item_id, item_widget)
                    self.set_item_no_info(item_id, {})

            for i in range(idx, total_count):
                item_widget = all_items[i]
                self.init_package_item_widget(item_widget, i, None)

            return

    def get_bag_item_list(self):
        if global_data.player:
            player = global_data.player.logic if 1 else None
            return player or []
        else:
            items_map = player.ev_g_others()
            if not items_map:
                items_map = {}
            items = []
            for entity_id, item_data in six.iteritems(items_map):
                item_id = item_data['item_id']
                if item_id in self.only_check_list:
                    items.append((entity_id, item_data))

            return items

    def init_package_item_widget(self, item_widget, entity_id, item_data):
        if item_data:
            item_id = item_data['item_id']
            count = item_data.get('count', 1)
            show_text = str(count)
        else:
            item_id = None
            show_text = None
        koth_shop_utils.init_mall_item_temp(item_widget, {'item_no': item_id,'show_text': show_text})

        @item_widget.btn_item.callback()
        def OnClick(btn, touch):
            self.common_select_item(item_widget, item_id)

        return