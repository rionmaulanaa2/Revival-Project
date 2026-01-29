# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/BagHumanWeaponWidget.py
from __future__ import absolute_import
from logic.gcommon import const
from logic.gcommon.item import item_const as iconst
from logic.gutils import template_utils

class BagHumanWeaponWidget(object):
    WEAPON_POS_TO_UI_INDEX_DICT = {const.PART_WEAPON_POS_MAIN1: 1,
       const.PART_WEAPON_POS_MAIN2: 2,
       const.PART_WEAPON_POS_MAIN3: 3,
       const.PART_WEAPON_POS_MAIN_DF: 4
       }
    DEFAULT_DRESS_ICON_DICT = {iconst.DRESS_POS_HEAD: 'icon_helmet',
       iconst.DRESS_POS_ARMOR: 'icon_armor',
       iconst.DRESS_POS_LEG: 'icon_shose'
       }
    DRESS_POS_LIST = [
     iconst.DRESS_POS_HEAD, iconst.DRESS_POS_ARMOR, iconst.DRESS_POS_LEG]

    def __init__(self, nd_weapon, clothes_ui_list, click_method, drag_method, end_method, click_clothes, drag_clothes, end_clothes):
        self._nd_weapon = nd_weapon
        self._clothes_ui_list = clothes_ui_list
        self._on_gun_click = click_method
        self._on_gun_drag = drag_method
        self._on_gun_end = end_method
        self._on_clothes_click = click_clothes
        self._on_clothes_drag = drag_clothes
        self._on_clothes_end = end_clothes
        self.init_widget()

    def init_widget(self):
        self.init_weapon([const.PART_WEAPON_POS_MAIN1, const.PART_WEAPON_POS_MAIN2, const.PART_WEAPON_POS_MAIN3, const.PART_WEAPON_POS_MAIN_DF])
        self.init_bone_equip()

    def init_weapon(self, pos_list):
        if not global_data.player or not global_data.player.logic:
            return
        else:
            hand_pos = global_data.player.logic.share_data.ref_wp_bar_cur_pos
            from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_SKIN_SHOW_KEY
            show_skin = global_data.player.get_setting_2(WEAPON_BAR_SKIN_SHOW_KEY)
            for pos in pos_list:
                weapon_obj = global_data.player.logic.share_data.ref_wp_bar_mp_weapons.get(pos)
                if weapon_obj is None:
                    weapon_data = None if 1 else weapon_obj.get_data()
                    if weapon_data:
                        weapon_data['iBulletCap'] = weapon_obj.get_bullet_cap()
                    gun_ui_index = self.WEAPON_POS_TO_UI_INDEX_DICT.get(pos)
                    gun_item = getattr(self._nd_weapon, 'gun_{}'.format(gun_ui_index))
                    gun_lab_num = getattr(gun_item, 'lab_{}'.format(gun_ui_index))
                    gun_lab_num.SetString(str(gun_ui_index))
                    if not gun_item:
                        continue
                    weapon_conf = template_utils.init_gun_equipment_new(gun_item, weapon_data, lplayer=global_data.player.logic, show_skin=show_skin)
                    gun_item.img_using.setVisible(hand_pos == pos)
                    gun_item.bg_bullet.setVisible(hand_pos == pos)
                    if hand_pos == pos:
                        gun_item.bullet_quantity.SetColor(3678582)
                    else:
                        gun_item.bullet_quantity.SetColor('#SW')

                    @gun_item.btn.unique_callback()
                    def OnClick(layer, touch, item_data=weapon_data, item_widget=gun_item):
                        if not self._on_gun_click:
                            return
                        self._on_gun_click(layer, touch, item_data, item_widget)

                    @gun_item.btn.unique_callback()
                    def OnDrag(layer, touch, item_data=weapon_data, item_widget=gun_item, pos=pos):
                        if not self._on_gun_drag:
                            return
                        self._on_gun_drag(layer, touch, item_data, item_widget, pos)

                    @gun_item.btn.unique_callback()
                    def OnEnd(layer, touch, item_data=weapon_data, pos=pos):
                        if not self._on_gun_end:
                            return
                        self._on_gun_end(layer, touch, item_data, pos)

                    if not weapon_conf:
                        pass
                    continue

            return

    def init_bone_equip(self):
        if not global_data.player or not global_data.player.logic:
            return
        else:
            clothes = global_data.player.logic.ev_g_clothing()
            for idx, clothing_ui in enumerate(self._clothes_ui_list):
                clothing_pos = self.DRESS_POS_LIST[idx]
                clothing_data = clothes.get(clothing_pos, None)
                clothing_conf = template_utils.init_bone_equip_item_new(clothing_ui, clothing_data)
                if not clothing_conf:
                    clothing_ui.img_empty.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/icon/{}.png'.format(self.DEFAULT_DRESS_ICON_DICT[clothing_pos]))
                    clothing_ui.img_equipment.setVisible(False)
                    clothing_ui.img_empty.setVisible(True)
                else:
                    clothing_ui.img_equipment.setVisible(True)
                    clothing_ui.img_empty.setVisible(False)

                @clothing_ui.btn.unique_callback()
                def OnClick(btn, touch, item_ui=clothing_ui, item_data=clothing_data):
                    self._on_clothes_click(btn, touch, item_data)

                @clothing_ui.btn.unique_callback()
                def OnDrag(btn, touch, item_ui=clothing_ui, item_data=clothing_data):
                    self._on_clothes_drag(btn, touch, item_data)

                @clothing_ui.btn.unique_callback()
                def OnEnd(btn, touch, item_ui=clothing_ui, item_data=clothing_data):
                    self._on_clothes_end(btn, touch, item_data)

            return

    def destroy(self):
        self._nd_weapon = None
        return


class BagHumanWeaponMobileWidget(BagHumanWeaponWidget):

    def init_weapon(self, pos_list):
        if not global_data.player or not global_data.player.logic:
            return
        else:
            from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_SKIN_SHOW_KEY
            show_skin = global_data.player.get_setting_2(WEAPON_BAR_SKIN_SHOW_KEY)
            hand_pos = global_data.player.logic.share_data.ref_wp_bar_cur_pos
            for pos in pos_list:
                weapon_obj = global_data.player.logic.share_data.ref_wp_bar_mp_weapons.get(pos)
                if weapon_obj is None:
                    weapon_data = None if 1 else weapon_obj.get_data()
                    if weapon_data:
                        weapon_data['iBulletCap'] = weapon_obj.get_bullet_cap()
                    gun_ui_index = self.WEAPON_POS_TO_UI_INDEX_DICT.get(pos)
                    gun_item = getattr(self._nd_weapon, 'gun_{}'.format(gun_ui_index))
                    if not gun_item:
                        continue
                    weapon_conf = template_utils.init_gun_equipment(gun_item, weapon_data, player=global_data.player.logic, show_skin=show_skin)
                    gun_item.img_using.setVisible(hand_pos == pos)
                    gun_item.bullet_bg.setVisible(hand_pos == pos)
                    if hand_pos == pos:
                        gun_item.bullet_quantity.SetColor(3678582)
                    else:
                        gun_item.bullet_quantity.SetColor('#SW')

                    @gun_item.btn.unique_callback()
                    def OnClick(layer, touch, item_data=weapon_data, item_widget=gun_item):
                        if not self._on_gun_click:
                            return
                        self._on_gun_click(layer, touch, item_data, item_widget)

                    @gun_item.btn.unique_callback()
                    def OnDrag(layer, touch, item_data=weapon_data, item_widget=gun_item, pos=pos):
                        if not self._on_gun_drag:
                            return
                        self._on_gun_drag(layer, touch, item_data, item_widget, pos)

                    @gun_item.btn.unique_callback()
                    def OnEnd(layer, touch, item_data=weapon_data, pos=pos):
                        if not self._on_gun_end:
                            return
                        self._on_gun_end(layer, touch, item_data, pos)

                    if not weapon_conf:
                        pass
                    continue

            return

    def init_bone_equip(self):
        if not global_data.player or not global_data.player.logic:
            return
        else:
            clothes = global_data.player.logic.ev_g_clothing()
            for idx, clothing_ui in enumerate(self._clothes_ui_list):
                clothing_pos = self.DRESS_POS_LIST[idx]
                clothing_data = clothes.get(clothing_pos, None)
                clothing_conf = template_utils.init_bone_equip_item(clothing_ui, clothing_data)
                if not clothing_conf:
                    clothing_ui.img_equipment.setVisible(False)
                else:
                    clothing_ui.img_equipment.setVisible(True)

                @clothing_ui.btn.unique_callback()
                def OnClick(btn, touch, item_ui=clothing_ui, item_data=clothing_data):
                    self._on_clothes_click(btn, touch, item_data)

                @clothing_ui.btn.unique_callback()
                def OnDrag(btn, touch, item_ui=clothing_ui, item_data=clothing_data):
                    self._on_clothes_drag(btn, touch, item_data)

                @clothing_ui.btn.unique_callback()
                def OnEnd(btn, touch, item_ui=clothing_ui, item_data=clothing_data):
                    self._on_clothes_end(btn, touch, item_data)

            return