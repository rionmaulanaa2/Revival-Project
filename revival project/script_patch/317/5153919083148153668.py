# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/WeaponBarBaseUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import world
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon import const
from collections import OrderedDict
from common.const import uiconst

class WeaponBarBaseUI(BasePanel):
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    ALL_MAIN_WEAPON = const.MAIN_WEAPON_LIST

    def on_init_panel(self):
        self.weapon_pos_to_eid = {}
        self.weapon_data_dict = {}
        self.sp_items_key_dict = OrderedDict()
        from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        super(WeaponBarBaseUI, self).on_finalize_panel()
        self.player = None
        return

    def init_parameters(self):
        from logic.gcommon import const
        self.cur_weapon_pos = const.PART_WEAPON_POS_MAIN_DF
        self.is_in_pick_ani = False
        self.add_hide_count('SELF')
        self._renew_ani_sequence = {}
        self._is_in_renew_ani = {}
        for pos in self.ALL_MAIN_WEAPON:
            self._renew_ani_sequence[pos] = []
            self._is_in_renew_ani[pos] = False

        self.player = None
        return

    def on_player_setted(self):
        if global_data.cam_lplayer:
            self.player = global_data.cam_lplayer
            if self.get_show_count('SELF') < 0:
                self.add_show_count('SELF')
            self.init_weapon_info()

    def init_event(self):
        emgr = global_data.emgr
        emgr.on_item_data_changed_event += self.on_item_data_changed
        emgr.weapon_equip_attachment_event += self.on_change_weapon_attachment
        emgr.on_weapon_data_switched_event += self.on_weapon_data_switched
        emgr.on_wpbar_switch_cur_event += self.on_weapon_in_hand_changed
        emgr.on_observer_pick_up_weapon += self.on_pick_up_weapon
        emgr.scene_camera_player_setted_event += self.update_ui
        emgr.on_observer_weapon_deleted += self.on_weapon_deleted
        emgr.scene_camera_player_setted_event += self.on_player_setted
        emgr.on_observer_weapon_bullet_num_changed += self.on_weapon_bullet_num_changed
        emgr.on_weapon_mode_switched += self.on_weapon_in_hand_changed

    def on_weapon_bullet_num_changed(self, *args):
        pass

    def update_ui(self):
        pass

    def get_weapon_data(self, only_main=True):
        cam_lplayer = global_data.cam_lplayer
        if not cam_lplayer:
            return
        else:
            _weapon_data_dict = cam_lplayer.share_data.ref_wp_bar_mp_weapons
            if only_main:
                return _weapon_data_dict
            res_dict = {const.PART_WEAPON_POS_NONE: {}}
            res_dict.update(_weapon_data_dict)
            return res_dict

    def get_main_weapon_data(self):
        raise NotImplementedError('my test: not implemented!')
        main_weapon_dict = OrderedDict()
        for pos in self.ALL_MAIN_WEAPON:
            if pos in self.weapon_data_dict:
                main_weapon_dict[pos] = self.weapon_data_dict[pos]

        return main_weapon_dict

    def get_bag_bullet_num(self, bullet_type):
        if bullet_type is None:
            return 0
        else:
            item_count = global_data.cam_lplayer.ev_g_item_count(bullet_type)
            return item_count

    def get_weapon_pic_path(self, weapon_id):
        from logic.gutils.item_utils import get_item_pic_by_item_no
        return get_item_pic_by_item_no(weapon_id)

    def check_is_has_main_weapon(self):
        return any([ pos in self.weapon_data_dict for pos in self.ALL_MAIN_WEAPON ])

    def on_start_bomb_rocker(self):
        self.add_hide_count('BOMB_ROCKER')

    def on_end_bomb_rocker(self):
        self.add_show_count('BOMB_ROCKER')