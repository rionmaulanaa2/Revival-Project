# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/ArenaRandomWeaponUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from mobile.common.EntityManager import EntityManager
from logic.gutils import role_head_utils
from logic.gcommon import time_utility
from logic.gutils import item_utils
from random import shuffle, sample
import math
UI_ANIM_TIME = 5

class ArenaRandomWeaponUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_arena/battle_arena_start'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.init_panel()

    def on_finalize_panel(self):
        pass

    def init_parameters(self):
        self.duel_start_time = None
        self.duel_end_time = None
        return

    def init_item_list(self):
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        if not bat:
            return
        random_weapon, self.duel_start_time, self.duel_end_time = bat.get_duel_info()
        if not random_weapon:
            return
        random_weapon = int(random_weapon)
        all_weapons = global_data.game_mode.get_cfg_data('play_data').get('weapon_list', [])
        new_weapons = [ x for x in all_weapons if x != random_weapon ]
        shuffle(new_weapons)
        new_weapons.insert(1, random_weapon)
        all_items = self.panel.list_weapon.GetAllItem()
        ui_item_num = len(all_items)
        weapon_num = len(new_weapons)
        off_num = ui_item_num - weapon_num
        if off_num > 0 and off_num <= weapon_num:
            off_list = sample(new_weapons, ui_item_num - weapon_num)
            new_weapons.extend(off_list)
        for index, item_widget in enumerate(all_items):
            item_id = new_weapons[index]
            item_widget.img_weapon.SetDisplayFrameByPath('', item_utils.get_gun_pic_by_item_id(item_id))

    def init_panel(self):
        self.init_item_list()
        start_left_time = 0
        if self.duel_start_time:
            start_left_time = int(math.ceil(self.duel_start_time - time_utility.time()))
        need_time = UI_ANIM_TIME
        if start_left_time <= need_time:
            if start_left_time > 0:
                ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')
                ui.on_delay_close(start_left_time)
            global_data.ui_mgr.show_ui('ArenaTopUI', 'logic.comsys.concert')
            self.close()
            return
        self.panel.PlayAnimation('show')
        self.panel.SetTimeOut(1, lambda : self.panel.PlayAnimation('select'))

        def _close_cb():
            if self and self.is_valid():
                self.close()
            ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')
            ui.on_delay_close(start_left_time - need_time)
            global_data.ui_mgr.show_ui('ArenaTopUI', 'logic.comsys.concert')

        self.panel.SetTimeOut(need_time, _close_cb)
        self.refresh_player_info()

    def refresh_player_info(self):
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        if not bat:
            return
        king, defier, _, _ = bat.get_battle_data()
        self.update_photo(self.panel.temp_player_1, king)
        self.update_photo(self.panel.temp_player_2, defier)

    def update_photo(self, ui_item, entity_id):
        if not entity_id:
            return
        player = EntityManager.getentity(entity_id)
        if not (player and player.logic):
            return
        char_name = player.logic.ev_g_char_name()
        head_frame = player.logic.ev_g_head_frame()
        head_photo = player.logic.ev_g_head_photo()
        role_head_utils.init_role_head(ui_item.temp_head, head_frame, head_photo)
        ui_item.lab_name.SetString(char_name)