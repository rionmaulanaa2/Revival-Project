# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/BagBaseUI.py
from __future__ import absolute_import
from six.moves import range
import cc
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_TYPE_MESSAGE
from common.uisys.basepanel import BasePanel
from logic.gcommon import const
from logic.gcommon.cdata.status_config import ST_SWIM, ST_PARACHUTE, ST_USE_ITEM, ST_SKATE_MOVE, ST_MECHA_DRIVER, ST_MECHA_PASSENGER, ST_SKATE
from logic.gcommon.cdata import status_config
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import item_utils
from logic.gutils import template_utils
from logic.gcommon.common_const import mecha_const
from common.utils.ui_utils import get_scale
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
from common.const.cocos_constant import ONE_MINUS_SRC_ALPHA, ONE
from logic.gutils.mecha_module_utils import get_module_card_name_and_desc, get_module_type_name_by_slot
from .BagHumanWeaponWidget import BagHumanWeaponWidget
from .BagHumanItemWidget import BagHumanItemWidget
from .BagMechaModuleWidget import BagMechaModuleWidget
from .BagMechaItemWidget import BagMechaItemWidget
from common.utils.cocos_utils import neox_pos_to_cocos
from common.cfg import confmgr
from logic.gutils.ui_salog_utils import add_uiclick_add_up_salog
from logic.comsys.battle import BattleUtils
DRAG_X = 80
DRAG_BACKWARD_X = 60
DRAG_DELTA = 0.05
DRAG_TAN = 1.303
PACKAGE_MOVE_OFFSET = 136
PANEL_HUMAN = 1
PANEL_MECHA = 2
NOT_THROW_ITEM_STATE = [
 ST_SWIM, ST_PARACHUTE]
from common.const import uiconst
MIN_MOVE_DIST = get_scale('10w')
BAG_UI_TYPE_OTHERS = -1
BAG_UI_TYPE_GUN = 0
BAG_UI_TYPE_ITEM = 1
BAG_UI_TYPE_CLOTHING = 2
BAG_UI_TYPE_MODULE = 3
HUMAN_ITEM_HEIGHT = 78
WEAPON_POS_TO_UI_IDX = {const.PART_WEAPON_POS_MAIN1: 1,
   const.PART_WEAPON_POS_MAIN2: 2,
   const.PART_WEAPON_POS_MAIN3: 3,
   const.PART_WEAPON_POS_MAIN_DF: 4
   }

class BagBaseUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    EXCEPT_HIDE_UI_LIST = ['FightLeftShotUI', 'MoveRockerUI', 'MoveRockerTouchUI', 'FightReadyTipsUI', 'BagUI']
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self, player=None):
        self.init_parameters()
        self.init_widgets()
        self.on_player_setted(player)
        self.process_events(True)

    def on_finalize_panel(self):
        self.unregister_event()
        self.process_events(False)
        self.destroy_widget('human_weapon_widget')
        self.destroy_widget('mecha_module_widget')
        self.destroy_widget('human_item_widget')
        self.destroy_widget('mecha_item_widget')

    def init_parameters(self):
        self.lplayer = None
        self._appearing = False
        self._other_ui_visible = True
        self.gun_ui_list = [
         self.panel.nd_human.gun_1, self.panel.nd_human.gun_2, self.panel.nd_human.gun_3, self.panel.nd_human.gun_4]
        self.clothing_ui_list = [self.panel.bone_equip.temp_helmet, self.panel.bone_equip.temp_cloth, self.panel.bone_equip.temp_leg]
        self.module_ui_list = [self.panel.mech_module.module_1, self.panel.mech_module.module_2, self.panel.mech_module.module_3, self.panel.mech_module.module_4]
        self.tips_ui_list = [self.panel.item_tips, self.panel.item_tips_2]
        self._tip_ui_height = 0
        self.rogue_gifts_ui_list = [
         self.panel.btn_firm1, self.panel.btn_firm2, self.panel.btn_firm3]
        self.cur_ui = None
        self.cur_ui_type = None
        self.cur_ui_sub_type = None
        self.cur_ui_item_data = None
        return

    def init_widgets(self):
        self.panel.drag_item.setVisible(False)

    def register_event(self):
        if not self.lplayer:
            return
        register_event = self.lplayer.regist_event
        register_event('E_WEAPON_DATA_SWITCHED', self._on_weapon_data_switched)
        register_event('E_CLOTHING_CHANGED', self._on_clothing_changed)
        register_event('E_ARMOR_DO_DAMAGE', self._on_armor_do_damage)
        register_event('E_WPBAR_SWITCH_CUR', self._on_wpbar_switch_cur)
        register_event('E_ITEM_DATA_CHANGED', self._on_item_data_changed)
        register_event('E_WEAPON_DATA_DELETED_SUCCESS', self._on_weapon_data_deleted_success)
        register_event('E_CUR_BULLET_NUM_CHG', self._on_weapon_bullet_changed)
        register_event('E_MEOW_COIN_CHANGE', self._on_meow_coin_change)

    def unregister_event(self):
        if not self.lplayer:
            return
        unregister_event = self.lplayer.unregist_event
        unregister_event('E_WEAPON_DATA_SWITCHED', self._on_weapon_data_switched)
        unregister_event('E_CLOTHING_CHANGED', self._on_clothing_changed)
        unregister_event('E_ARMOR_DO_DAMAGE', self._on_armor_do_damage)
        unregister_event('E_WPBAR_SWITCH_CUR', self._on_wpbar_switch_cur)
        unregister_event('E_ITEM_DATA_CHANGED', self._on_item_data_changed)
        unregister_event('E_WEAPON_DATA_DELETED_SUCCESS', self._on_weapon_data_deleted_success)
        unregister_event('E_CUR_BULLET_NUM_CHG', self._on_weapon_bullet_changed)
        unregister_event('E_MEOW_COIN_CHANGE', self._on_meow_coin_change)

    def process_events(self, is_bind):
        econf = {'scene_player_setted_event': self.on_player_setted,
           'net_reconnect_before_destroy_event': self.on_reconnect,
           'net_login_reconnect_before_destroy_event': self.on_reconnect,
           'global_rogue_gifts_updated': self._on_global_rogue_gifts_updated
           }
        if is_bind:
            global_data.emgr.bind_events(econf)
        else:
            global_data.emgr.unbind_events(econf)

    def on_player_setted(self, lplayer):
        if lplayer is None:
            if self._appearing:
                self.unregister_event()
            return
        else:
            self.lplayer = lplayer
            self.human_weapon_widget.init_widget()
            self.human_item_widget.init_widget()
            self.mecha_module_widget.init_widget()
            self.mecha_item_widget.init_widget()
            self._refresh_rogue_gift_list(lplayer)
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
        self.human_weapon_widget.init_widget()
        self.human_item_widget.init_widget()
        self.mecha_module_widget.init_widget()
        self.mecha_item_widget.init_widget()
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
        self.unregister_event()
        if self.panel.IsPlayingAnimation('bag_show'):
            self.panel.StopAnimation('bag_show')
        self.panel.PlayAnimation('bag_disappear')
        self.panel.setVisible(False)
        for tip_ui in self.tips_ui_list:
            tip_ui.setVisible(False)

    def isPanelVisible(self):
        return self._appearing and super(BagBaseUI, self).isPanelVisible()

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

    def on_gun_click(self, layer, touch, item_data, item_widget):
        if not item_data:
            return
        else:
            cur_gun_ui = layer.GetParent()
            cur_gun_ui.choose.setVisible(True)
            self.cur_ui = cur_gun_ui
            self.cur_ui_type = BAG_UI_TYPE_GUN
            self.cur_ui_sub_type = BAG_UI_TYPE_GUN
            self.cur_ui_item_data = None
            self.show_item_tips(self.tips_ui_list[0], item_data)
            return

    def on_gun_drag(self, layer, touch, item_data, item_widget, pos):
        if not item_data:
            return
        else:
            if pos == const.PART_WEAPON_POS_MAIN_DF:
                return
            from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_SKIN_SHOW_KEY
            wpos = touch.getLocation()
            lpos = self.panel.drag_item.getParent().convertToNodeSpace(wpos)
            item_id = item_data.get('item_id')
            from logic.gcommon.item.item_const import FASHION_POS_SUIT
            from logic.gutils.dress_utils import get_weapon_default_fashion
            if global_data.player and global_data.player.get_setting_2(WEAPON_BAR_SKIN_SHOW_KEY):
                item_fashion = item_data.get('fashion', {}).get(FASHION_POS_SUIT, None) or get_weapon_default_fashion(item_id)
            else:
                item_fashion = get_weapon_default_fashion(item_id)
            self.show_drag_item(lpos, item_data.get('item_id'), item_fashion)
            self.show_delete_widget_gun(wpos)
            return

    def on_gun_end(self, layer, touch, item_data, pos):
        if not item_data:
            return
        else:
            self.panel.drag_item.setVisible(False)
            self.hide_delete_widget()
            wpos = touch.getLocation()
            end_gun_pos = self.cal_end_gun_pos(wpos)
            if end_gun_pos is None:

                def callback(num, pos=pos, item_data=item_data):
                    item_utils.throw_item(self.lplayer, const.BACKPACK_PART_WEAPON, item_data['entity_id'], pos)

                item_id = item_data.get('item_id', -1)
                item_name = item_utils.get_item_name(item_id)
                self.discard_item(callback, item_name, item_data.get('count', 1))
            else:
                if end_gun_pos == pos:
                    return
                if end_gun_pos == const.PART_WEAPON_POS_MAIN_DF or pos == const.PART_WEAPON_POS_MAIN_DF:
                    return
                self.lplayer.send_event('E_CALL_SYNC_METHOD', 'try_switch_weapon', (pos, end_gun_pos), False, True)
            return

    def on_clothes_click(self, layer, touch, item_data):
        if not item_data:
            return
        else:
            cur_clothing_ui = layer.GetParent()
            cur_clothing_ui.img_select.setVisible(True)
            self.cur_ui = cur_clothing_ui
            self.cur_ui_type = BAG_UI_TYPE_CLOTHING
            self.cur_ui_sub_type = BAG_UI_TYPE_CLOTHING
            self.cur_ui_item_data = None
            self.show_item_tips(self.tips_ui_list[0], item_data)
            return

    def on_clothes_drag(self, layer, touch, item_data):
        if not item_data:
            return
        wpos = touch.getLocation()
        lpos = self.panel.drag_item.getParent().convertToNodeSpace(wpos)
        self.show_drag_item(lpos, item_data.get('item_id'))
        self.show_delete_widget_clothes(wpos)

    def on_clothes_end(self, layer, touch, item_data):
        if not item_data:
            return
        wpos = touch.getLocation()
        self.panel.drag_item.setVisible(False)
        self.hide_delete_widget()
        if self.panel.nd_human.IsPointIn(wpos):
            return

        def callback(num, item_data=item_data):
            if not BattleUtils.can_throw_clothes():
                return
            else:
                item_utils.throw_item(self.lplayer, const.BACKPACK_PART_CLOTHING, item_data['entity_id'], 1, None)
                return

        item_id = item_data.get('item_id', -1)
        item_name = item_utils.get_item_name(item_id)
        self.discard_item(callback, item_name, item_data.get('count', 1))

    def on_module_click(self, layer, touch, module_id, card_id, card_lv, slot_no):
        self.cur_ui = layer
        self.cur_ui_type = BAG_UI_TYPE_MODULE
        self.cur_ui_sub_type = BAG_UI_TYPE_MODULE
        self.cur_ui_item_data = None
        if not self.lplayer:
            return
        else:
            layer.module_bar.SetBlendFunc((ONE, ONE))
            layer.icon_skill.SetBlendFunc((ONE, ONE))
            if self.lplayer.ev_g_get_bind_mecha():
                all_module_config = self.lplayer.ev_g_replicate_module_plans()
                mecha_id = self.lplayer.ev_g_get_bind_mecha_type()
                module_config = all_module_config.get(mecha_id, {})
                card_ids = module_config.get(slot_no, [])
                for idx, cur_card_id in enumerate(card_ids):
                    name_desc, card_effect_desc = get_module_card_name_and_desc(cur_card_id, card_lv)
                    item_data = {'is_module': True,
                       'item_id': module_id,
                       'card_lv': card_lv if cur_card_id == card_id else None,
                       'card_id': cur_card_id,
                       'card_plan': card_ids,
                       'slot_no': slot_no,
                       'module_prefix': '',
                       'name_text': name_desc,
                       'desc_text': card_effect_desc
                       }
                    self.show_item_tips(self.tips_ui_list[idx], item_data, idx)

            else:
                name_desc = get_module_type_name_by_slot(slot_no)
                card_effect_desc = get_text_by_id(80437)
                item_data = {'is_module': True,
                   'item_id': module_id,
                   'card_lv': card_lv,
                   'card_id': card_id,
                   'slot_no': slot_no,
                   'module_prefix': '',
                   'name_text': name_desc,
                   'desc_text': card_effect_desc
                   }
                self.show_item_tips(self.item_tips, item_data)
            return

    def on_module_drag(self, layer, touch, module_id, slot_no):
        if not module_id or module_id == mecha_const.SP_MODULE_CHOOSE_ITEM_ID:
            return
        wpos = touch.getLocation()
        lpos = self.panel.drag_item.getParent().convertToNodeSpace(wpos)
        self.show_drag_item(lpos, module_id)
        self.show_delete_widget_module(wpos)

    def on_module_end(self, layer, touch, module_id, slot_no):
        if not module_id:
            return
        self.panel.drag_item.setVisible(False)
        self.hide_delete_widget()
        wpos = touch.getLocation()
        if not self.is_in_empty_area(wpos):
            return
        if self.lplayer and slot_no:
            self.lplayer.send_event('E_MECHA_UNINSTALL_MODULE', slot_no)

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
        self.panel.item_tips_2.SetTouchEnabledRecursion(False)

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
            item_utils.throw_item(self.lplayer, const.BACKPACK_PART_OTHERS, item_data['entity_id'], num, None)
            return

        item_id = item_data.get('item_id', -1)
        item_name = item_utils.get_item_name(item_id)
        self.discard_item(callback, item_name, item_data.get('count', 1), wpos)

    def on_item_end_mecha(self, layer, touch, item_data):
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
            item_utils.throw_item(self.lplayer, const.BACKPACK_PART_OTHERS, item_data['entity_id'], num, None)
            return

        item_id = item_data.get('item_id', -1)
        item_name = item_utils.get_item_name(item_id)
        self.discard_item(callback, item_name, item_data.get('count', 1), wpos)

    def _on_weapon_data_switched(self, pos1, pos2):
        self.human_weapon_widget.init_weapon([pos1, pos2])

    def _on_clothing_changed(self, *args):
        self.human_weapon_widget.init_bone_equip()

    def _on_armor_do_damage(self, *args):
        self.human_weapon_widget.init_bone_equip()

    def _on_wpbar_switch_cur(self, *args):
        self.human_weapon_widget.init_weapon([const.PART_WEAPON_POS_MAIN1, const.PART_WEAPON_POS_MAIN2, const.PART_WEAPON_POS_MAIN3, const.PART_WEAPON_POS_MAIN_DF])

    def _on_item_data_changed(self, item_data):
        self.human_item_widget.init_widget()
        self.mecha_item_widget.init_widget()
        self.resize_bag_height()

    def _on_weapon_data_deleted_success(self, pos):
        self.human_weapon_widget.init_weapon([pos])

    def _on_weapon_bullet_changed(self, pos_or_pos_list):
        if not self.lplayer:
            return
        else:
            weapon_pos_list = [pos_or_pos_list] if isinstance(pos_or_pos_list, int) else pos_or_pos_list
            for pos in weapon_pos_list:
                weapon_obj = self.lplayer.share_data.ref_wp_bar_mp_weapons.get(pos)
                if weapon_obj is None:
                    weapon_data = None if 1 else weapon_obj.get_data()
                    if weapon_data:
                        weapon_data['iBulletCap'] = weapon_obj.get_bullet_cap()
                        weapon_data['iCarryBulletNum'] = weapon_obj.get_carry_bullet_num()
                    ui_idx = WEAPON_POS_TO_UI_IDX.get(pos, -1)
                    item_widget = getattr(self.panel, 'gun_{}'.format(ui_idx))
                    if not item_widget:
                        continue
                    template_utils.refresh_gun_bullet_show(item_widget, weapon_data, None, self.lplayer)

            return

    def on_click_close_btn(self, *args):
        self.disappear()

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

    def cal_end_gun_pos(self, wpos):
        gun_pos = None
        for idx, gun_ui in enumerate(self.gun_ui_list):
            if gun_ui.IsPointIn(wpos):
                gun_ui.choose.setVisible(False)
                if idx == 3:
                    return const.PART_WEAPON_POS_MAIN_DF
                return idx + 1

        return gun_pos

    def discard_item(self, callback, item_name, max_count, wpos=None):
        if not self.lplayer:
            return
        else:
            if not self.lplayer.ev_g_can_throw_item():
                return
            self.cur_ui = None
            if max_count <= 1:
                callback(max_count)
                return
            if wpos:
                width, height = self.panel.discard.GetContentSize()
                discard_scale = self.panel.discard.getScaleX()
                offset_x, offset_y = template_utils.get_panel_show_all_offset(self.panel.discard, self.panel, wpos, 1, width * discard_scale, height * discard_scale)
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
        delta_h = self.mecha_item_widget.resize_height_by_item_cnt()
        self.human_item_widget.resize_height_by_item_cnt(delta_h)

    def show_item_tips(self, tip_ui, item_data, tip_no=0):
        self.tips_ui_list[1].setVisible(False)
        tip_ui.setVisible(False)
        tip_ui_height = template_utils.init_item_tips_new(tip_ui, item_data) * tip_ui.getScaleY()
        tip_ui_width = tip_ui.GetContentSize()[0] * tip_ui.getScaleX()
        if tip_no == 1:
            tip_show_pos = cc.Vec2(self.cur_mouse_pos.x, self.cur_mouse_pos.y - self._tip_ui_height)
        else:
            tip_show_pos = cc.Vec2(self.cur_mouse_pos.x, self.cur_mouse_pos.y)
            self._tip_ui_height = tip_ui_height
        offset_x, offset_y = template_utils.get_panel_show_all_offset(tip_ui, self.panel, tip_show_pos, 1, tip_ui_width, tip_ui_height)
        if offset_x < 0:
            tip_show_pos.x = tip_show_pos.x - tip_ui_width
        if offset_y > 0:
            tip_show_pos.y = tip_show_pos.y + tip_ui_height
        tip_ui.setPosition(tip_show_pos.x, tip_show_pos.y)
        tip_ui.setVisible(True)

    def remove_cur_select_state(self):
        if self.cur_ui is None:
            return
        else:
            if self.cur_ui_type == BAG_UI_TYPE_GUN:
                choose = getattr(self.cur_ui, 'choose')
                if choose and choose.isValid():
                    choose.setVisible(False)
            elif self.cur_ui_type == BAG_UI_TYPE_ITEM:
                item_sel = getattr(self.cur_ui, 'item_sel')
                if item_sel and item_sel.isValid():
                    item_sel.setVisible(False)
                else:
                    return
                item_id = self.cur_ui_item_data.get('item_id')
                path = 'box_res' if item_utils.is_package_item(item_id) else 'item'
                item_conf = confmgr.get(path, str(item_id))
                pnl_right = getattr(self.cur_ui, 'pnl_right')
                if pnl_right and pnl_right.isValid():
                    pnl_right.SetDisplayFrameByPath('', template_utils.get_quality_pic_l(item_conf.get('iQuality')))
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
            elif self.cur_ui_type == BAG_UI_TYPE_CLOTHING:
                img_select = getattr(self.cur_ui, 'img_select')
                if img_select and img_select.isValid():
                    img_select.setVisible(False)
            elif self.cur_ui_type == BAG_UI_TYPE_MODULE:
                module_bar = getattr(self.cur_ui, 'module_bar')
                icon_skill = getattr(self.cur_ui, 'icon_skill')
                if module_bar and module_bar.isValid() and icon_skill and icon_skill.isValid():
                    module_bar.SetBlendFunc((ONE, ONE_MINUS_SRC_ALPHA))
                    icon_skill.SetBlendFunc((ONE, ONE_MINUS_SRC_ALPHA))
            return

    def use_bag_item(self, item_data):
        from logic.gutils import item_utils
        from logic.gcommon.item.item_utility import is_mecha_battery, is_neutral_shop_candy
        if not self.lplayer:
            return
        item_id = item_data['item_id']
        if item_utils.is_gun(item_id):
            return
        if item_utils.is_health_item(item_id) or item_utils.is_food_item(item_id) or is_mecha_battery(item_id) or is_neutral_shop_candy(item_id):
            self.use_medicine_item(item_id)
            return
        if item_utils.is_summon_item(item_id):
            self.use_summon_item(item_id)
            return
        if item_utils.is_charger_item(item_id):
            self.use_charger_item(item_id)
            return
        if item_utils.is_bullet(item_id):
            if self.lplayer.ev_g_is_in_any_state((ST_MECHA_DRIVER, ST_MECHA_PASSENGER, status_config.ST_VEHICLE_GUNNER, status_config.ST_VEHICLE_PASSENGER)):
                if not self.lplayer or not self.lplayer.ev_g_status_check_pass(ST_USE_ITEM):
                    if self.lplayer.ev_g_get_state(ST_SKATE_MOVE):
                        self.lplayer.send_event('E_TRY_STOP_SKATE')
                    return
                self.lplayer.send_event('E_CTRL_USE_DRUG', item_id)
                self.lplayer.send_event('E_ITEMUSE_TRY', item_id)
            else:
                global_data.emgr.battle_show_message_event.emit(get_text_local_content(18128))
            return
        if item_utils.is_consumable_item(item_id):
            self.use_throwable_item(item_id)
            return

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

    def _refresh_rogue_gift_list(self, lplayer):
        if lplayer:
            from logic.gutils import rogue_utils as r_u
            gift_ids = r_u.get_lplayer_gifts(lplayer)
        else:
            gift_ids = []
        self._refresh_rogue_list(gift_ids)

    def _on_global_rogue_gifts_updated(self, unit_id, gift_ids):
        if not self.lplayer or self.lplayer.id != unit_id:
            return
        self._refresh_rogue_list(gift_ids)

    def _get_rogue_list_item(self, idx):
        cnt = self._get_rogue_list_cnt()
        if idx >= 0 and idx < cnt:
            return self.rogue_gifts_ui_list[idx]
        else:
            return None
            return None

    def _get_rogue_list_cnt(self):
        return len(self.rogue_gifts_ui_list)

    def _refresh_rogue_list(self, gift_ids):
        from logic.gutils import rogue_utils as r_u
        cnt = self._get_rogue_list_cnt()
        data_cnt = len(gift_ids) if gift_ids else 0
        for i in range(cnt):
            if i < data_cnt:
                gift_id = gift_ids[i]
            else:
                gift_id = -1
            item = self._get_rogue_list_item(i)
            if gift_id == -1:
                item.SetEnable(False)
                continue
            item.SetEnable(True)
            icon_path = r_u.get_gift_icon(gift_id)
            item.SetFrames('', [icon_path, icon_path, r_u.get_gift_gray_icon()])

            @item.unique_callback()
            def OnClick(btn, touch, gift_id=gift_id):
                self._on_rogue_gift_click(gift_id)

    def _on_rogue_gift_click(self, gift_id):
        from logic.gutils import rogue_utils as r_u
        item_data = {'gift_id': gift_id,
           'item_id': 0,
           'is_rogue_gift': True,
           'name_text': r_u.get_gift_name_text(gift_id),
           'desc_text': r_u.get_gift_desc_text(gift_id),
           'item_pic': r_u.get_gift_icon(gift_id)
           }
        self.show_item_tips(self.panel.item_tips, item_data)

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