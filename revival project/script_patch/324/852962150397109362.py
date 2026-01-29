# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/WeaponBarSelectUIPC.py
from __future__ import absolute_import
import six
from .WeaponBarSelectUI import WeaponBarSelectBaseUI
from logic.gcommon import const
from logic.gutils import item_utils
from common.cfg import confmgr
from logic.gcommon.common_const import weapon_const
from logic.gutils.template_utils import get_item_quality
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gutils.dress_utils import get_weapon_default_fashion
from logic.client.const import game_mode_const

class WeaponBarSelectUIPC(WeaponBarSelectBaseUI):
    PANEL_CONFIG_NAME = 'battle/change_weapon_pc'
    HOT_KEY_FUNC_MAP_SHOW = {'switch_to_gun_1': {'node': ['nd_weapon_1.ccb_weapon_1.temp_pc', 'nd_weapon_1.ccb_weapon_1_sel.temp_pc']},'switch_to_gun_2': {'node': ['nd_weapon_2.ccb_weapon_2.temp_pc', 'nd_weapon_2.ccb_weapon_2_sel.temp_pc']},'switch_to_gun_3': {'node': ['nd_weapon_3.ccb_weapon_3.temp_pc', 'nd_weapon_3.ccb_weapon_3_sel.temp_pc']},'switch_to_uzi': {'node': ['nd_weapon_4.ccb_weapon_4.temp_pc', 'nd_weapon_4.ccb_weapon_4_sel.temp_pc']}}

    def init_widget(self):
        self.switch_scale_ani = None
        self.weapon_pos_to_eid = {}
        self._renew_ani_sequence = {}
        self.weapon_widget_dict = {const.PART_WEAPON_POS_MAIN1: (
                                       self.panel.ccb_weapon_1, self.panel.ccb_weapon_1_sel),
           const.PART_WEAPON_POS_MAIN2: (
                                       self.panel.ccb_weapon_2, self.panel.ccb_weapon_2_sel),
           const.PART_WEAPON_POS_MAIN3: (
                                       self.panel.ccb_weapon_3, self.panel.ccb_weapon_3_sel),
           const.PART_WEAPON_POS_MAIN_DF: (
                                         self.panel.ccb_weapon_4, self.panel.ccb_weapon_4_sel)
           }
        self.weapon_root_nd_dict = {const.PART_WEAPON_POS_MAIN1: self.panel.nd_weapon_1,
           const.PART_WEAPON_POS_MAIN2: self.panel.nd_weapon_2,
           const.PART_WEAPON_POS_MAIN3: self.panel.nd_weapon_3,
           const.PART_WEAPON_POS_MAIN_DF: self.panel.nd_weapon_4
           }
        self._init_improvise_highlight()
        self.weapon_pos_to_key_num = {const.PART_WEAPON_POS_MAIN1: 1,
           const.PART_WEAPON_POS_MAIN2: 2,
           const.PART_WEAPON_POS_MAIN3: 3,
           const.PART_WEAPON_POS_MAIN_DF: 4
           }
        self.init_weapon_ui_pos()
        for k, v in six.iteritems(self.weapon_widget_dict):
            for ccb_btn in v:
                ccb_btn.btn_weapon.disabled = False
                ccb_btn.btn_weapon.EnableCustomState(True)
                ccb_btn.btn_weapon.SetNoEventAfterMove(True, '10w')
                ccb_btn.anim_timer = None

            self._renew_ani_sequence[k] = []

        self.init_ui_event()
        return

    def init_weapon_ui_pos(self):
        self.weapon_ui_init_pos = [
         self.panel.nd_weapon_4.GetPosition(), self.panel.nd_weapon_3.GetPosition(),
         self.panel.nd_weapon_2.GetPosition(), self.panel.nd_weapon_1.GetPosition()]
        self.weapon_ui_offset = {3: (0, 0, 0, 20),
           2: (0, 0, 20, 40),
           1: (0, 20, 40, 40),
           0: (20, 40, 40, 40)
           }

    def update_weapon_ui(self, is_init=False):
        if not global_data.cam_lplayer:
            return
        if self.is_in_pick_ani:
            return
        self.update_weapon_item_visible()
        self.update_weapon_item_position()
        self.update_all_main_weapon_widgets()

    def update_all_main_weapon_widgets(self, need_refresh=False):
        main_weapon_pos_list = self.ALL_MAIN_WEAPON
        main_weapon_data = self.get_weapon_data(True) or {}
        weapon_pos_main3_data = None
        for weapon_pos in main_weapon_pos_list:
            weapon_ui_tuple = self.get_weapon_ui_by_pos(weapon_pos)
            weapon_object = main_weapon_data.get(weapon_pos, None)
            if hasattr(weapon_ui_tuple[0], 'img_weapon_num') and weapon_ui_tuple[0].img_weapon_num:
                weapon_ui_tuple[0].img_weapon_num.setVisible(not bool(weapon_object))
            for idx, weapon_ui in enumerate(weapon_ui_tuple):
                self.update_main_weapon_info(weapon_ui, weapon_pos, weapon_object, idx=idx)

        self.tick_armor_hp()
        return

    def update_weapon_item_position(self):
        cur_weapon_pos = global_data.cam_lplayer.share_data.ref_wp_bar_cur_pos
        if cur_weapon_pos not in self.ALL_MAIN_WEAPON:
            return
        else:
            main_weapon_data = self.get_weapon_data(True) or {}
            main_weapon_pos_list = self.ALL_MAIN_WEAPON[::-1]
            pos_index = 1
            selected_pos_index = 0
            exist_weapon_root_nd_list = [self.weapon_root_nd_dict.get(const.PART_WEAPON_POS_MAIN_DF)]
            exist_weapon_root_nd_list[0].SetPosition(self.weapon_ui_init_pos[0][0], self.weapon_ui_init_pos[0][1])
            for weapon_pos in main_weapon_pos_list:
                if weapon_pos == const.PART_WEAPON_POS_MAIN_DF:
                    continue
                weapon_object = main_weapon_data.get(weapon_pos, None)
                if weapon_object:
                    if cur_weapon_pos == weapon_pos:
                        selected_pos_index = pos_index
                    weapon_root_nd = self.weapon_root_nd_dict.get(weapon_pos)
                    exist_weapon_root_nd_list.append(weapon_root_nd)
                    weapon_root_nd.SetPosition(self.weapon_ui_init_pos[pos_index][0], self.weapon_ui_init_pos[pos_index][1])
                    pos_index += 1
                else:
                    continue

            cur_offset_tuple = self.weapon_ui_offset.get(selected_pos_index)
            for idx, weapon_root_nd in enumerate(exist_weapon_root_nd_list):
                cur_weapon_root_nd_pos = weapon_root_nd.GetPosition()
                y_offset = cur_offset_tuple[idx]
                weapon_root_nd.SetPosition(cur_weapon_root_nd_pos[0], cur_weapon_root_nd_pos[1] + y_offset)

            return

    def update_bullet_info(self, weapon_ui_item, wp, weapon_pos=None):
        cur_weapon_pos = global_data.cam_lplayer.share_data.ref_wp_bar_cur_pos
        if not wp or weapon_pos is None or cur_weapon_pos != weapon_pos:
            return
        else:
            if getattr(weapon_ui_item, 'nd_bullet') is None:
                return
            max_bullet = wp.get_bullet_cap()
            show_ratio = wp.get_show_ratio()
            weapon_data = wp.get_data()
            cur_bullet_num = weapon_data.get('iBulletNum', 0)
            iReloadRatio = wp.get_reload_ratio()
            bullet_type = wp.get_bullet_type()
            if bullet_type == weapon_const.ITEM_ID_INFINITE_BULLET:
                show_bullet_num = max_bullet
            elif bullet_type == weapon_const.ITEM_ID_LIMITED_BULLET:
                show_bullet_num = wp.get_carry_bullet_num()
            else:
                show_bullet_num = self.get_bag_bullet_num(bullet_type) * iReloadRatio
            weapon_ui_item.nd_bullet.lab_bullet_num.SetString(str(int(cur_bullet_num * show_ratio)))
            weapon_ui_item.nd_bullet.lab_bullet_full.SetString(''.join(['/', str(int(show_bullet_num * show_ratio))]))
            weapon_ui_item.PlayAnimation('bullet_low')
            return

    def update_gun_widget(self, weapon_ui_item, weapon, idx=0):
        weapon_data = weapon.get_data()
        item_no = weapon_data['item_id']
        if self._show_weapon_skin:
            lobby_item_fashion = weapon_data.get('fashion', {}).get(FASHION_POS_SUIT, None) or get_weapon_default_fashion(item_no)
        else:
            lobby_item_fashion = get_weapon_default_fashion(item_no)
        if lobby_item_fashion:
            pic_path = item_utils.get_lobby_item_pic_by_item_no(lobby_item_fashion)
        else:
            pic_path = item_utils.get_gun_pic_by_item_id(item_no, is_shadow=False)
        weapon_ui_item.sp_weapon.SetDisplayFrameByPath('', pic_path)
        from logic.gutils.weapon_skin_utils import set_weapon_skin_pic_pos_and_scale
        set_weapon_skin_pic_pos_and_scale(weapon_ui_item.sp_weapon, lobby_item_fashion, item_no)
        from logic.gutils.weapon_skin_utils import set_weapon_skin_pic_pos_and_scale
        set_weapon_skin_pic_pos_and_scale(weapon_ui_item.sp_weapon, lobby_item_fashion, item_no)
        if hasattr(weapon_ui_item, 'icon_type') and weapon_ui_item.icon_type:
            weapon_ui_item.icon_type.setVisible(False)
            if weapon and weapon.is_multi_wp():
                wp_id = weapon.get_item_id()
                mode_pic = confmgr.get('firearm_res_config', str(wp_id), 'cModeBarPic')
                if mode_pic:
                    weapon_ui_item.icon_type.setVisible(True)
                    weapon_ui_item.icon_type.SetDisplayFrameByPath('', mode_pic)
        level = get_item_quality(item_no)
        gun_name = item_utils.get_gun_name_by_item_id(item_no)
        if weapon_ui_item.lab_name:
            weapon_ui_item.lab_name.SetString(gun_name)
        tail = 'btn_change_l_choose' if idx == 1 else 'btn_change_l_nml'
        path = 'gui/ui_res_2_pc/battle/button/' + tail + '_%s_pc.png' % str(level)
        path_list = [path, path, path]
        if weapon_ui_item.btn_weapon:
            weapon_ui_item.btn_weapon.SetFrames('', path_list, False, None)
        return

    def update_weapon_key_num(self, weapon_ui_item, weapon_pos):
        if weapon_ui_item.lab_num:
            key_num = self.weapon_pos_to_key_num.get(weapon_pos)
            if key_num is None:
                key_num = ''
            weapon_ui_item.lab_num.SetString(str(key_num))
        return

    def update_widgets_visible(self, weapon_ui_item, is_vis, weapon_pos=None):
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CONCERT):
            if weapon_pos in (const.PART_WEAPON_POS_MAIN2, const.PART_WEAPON_POS_MAIN3, const.PART_WEAPON_POS_MAIN_DF):
                is_vis = False
        weapon_root_nd = self.weapon_root_nd_dict.get(weapon_pos)
        if weapon_root_nd:
            weapon_root_nd.setVisible(is_vis)

    def update_main_weapon_info(self, weapon_ui_item, weapon_pos, weapon, play_ani=False, idx=0):
        self.update_widgets_visible(weapon_ui_item, bool(weapon), weapon_pos)
        if not weapon:
            return
        self.update_gun_widget(weapon_ui_item, weapon, idx=idx)
        self.update_bullet_info(weapon_ui_item, weapon, weapon_pos)
        self.update_weapon_key_num(weapon_ui_item, weapon_pos)

    def on_weapon_bullet_num_changed(self, pos_or_pos_list):
        weapon_pos_list = [pos_or_pos_list] if isinstance(pos_or_pos_list, int) else pos_or_pos_list
        main_weapon_data = self.get_weapon_data(True)
        for weapon_pos in weapon_pos_list:
            weapon_ui_tuple = self.get_weapon_ui_by_pos(weapon_pos)
            weapon_object = main_weapon_data.get(weapon_pos, None)
            for idx, weapon_ui in enumerate(weapon_ui_tuple):
                if weapon_object:
                    self.update_bullet_info(weapon_ui, weapon_object, weapon_pos)

        return

    def on_hot_key_opened_state(self):
        if self.player and global_data.player and global_data.player.logic:
            if self.player.id != global_data.player.logic.id:
                return
        super(WeaponBarSelectUIPC, self).on_hot_key_opened_state()

    def on_player_setted(self):
        super(WeaponBarSelectUIPC, self).on_player_setted()
        if self.player and global_data.player and global_data.player.logic:
            if self.player.id != global_data.player.logic.id:
                self.on_switch_off_hot_key()