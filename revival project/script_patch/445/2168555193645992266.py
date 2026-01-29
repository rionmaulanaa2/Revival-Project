# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Magic/MagicSurvivalBattleMgr.py
from __future__ import absolute_import
import six
import six_ex
from common.framework import Singleton
import math3d
import collision
import world
from logic.gutils import magic_mode_utils
from common.utils import timer

class MagicCircleRegionChecker(object):

    def __init__(self):
        self._timer_id = 0
        self._region_id = None
        return

    def destroy(self):
        self.clear_timer()

    def clear_timer(self):
        if self._timer_id:
            global_data.game_mgr.get_logic_timer().unregister(self._timer_id)
            self._timer_id = None
        return

    def init_timer(self):
        if self._timer_id:
            global_data.game_mgr.get_logic_timer().unregister(self._timer_id)
        self._timer_id = global_data.game_mgr.get_logic_timer().register(func=self.check_in_magic_region, mode=timer.CLOCK, interval=1)

    def check_in_magic_region(self):
        player_pos = self.get_player_pos()
        if player_pos:
            region_id = global_data.magic_sur_battle_mgr.get_region_by_pos(player_pos)
            self._region_id = region_id
            global_data.emgr.notify_inside_magic_region_id.emit(region_id)

    def get_player_region(self):
        return self._region_id

    def get_player_pos(self):
        cam_lplayer = global_data.cam_lplayer
        if cam_lplayer:
            control_target = cam_lplayer.ev_g_control_target()
            if control_target and control_target.logic:
                pos = control_target.logic.ev_g_model_position()
            else:
                pos = cam_lplayer.ev_g_model_position()
            if pos:
                return pos
        elif global_data.is_in_judge_camera:
            if global_data.game_mgr.scene:
                return global_data.game_mgr.scene.active_camera.world_position
        return global_data.sound_mgr.get_listener_pos()


class MagicSurvivalBattleMgr(Singleton):
    ALIAS_NAME = 'magic_sur_battle_mgr'

    def init(self):
        self.init_parameters()
        self.magic_checker = MagicCircleRegionChecker()

    def init_parameters(self):
        self.magic_region_model_id_dict = {}
        self.magic_region_info_dict = {}
        self.applied_magic_rune_id = None
        return

    def on_finalize(self):
        for region_id in list(six_ex.keys(self.magic_region_info_dict)):
            self.set_region_param(region_id, None, None, None)

        if self.magic_checker:
            self.magic_checker.destroy()
            self.magic_checker = None
        self.remove_region_model()
        self.init_parameters()
        return

    def get_region_by_pos(self, t_pos):
        for region_id in six.iterkeys(self.magic_region_info_dict):
            pos, radius, data = self.magic_region_info_dict[region_id]
            if (t_pos.x - pos[0]) * (t_pos.x - pos[0]) + (t_pos.z - pos[2]) * (t_pos.z - pos[2]) <= radius * radius:
                return region_id

        return None

    def get_player_region(self):
        return self.magic_checker.get_player_region()

    def get_all_region_ids(self):
        return six_ex.keys(self.magic_region_info_dict)

    def update_magic_regions(self, region_all_dict):
        region_dict = region_all_dict.get('magic_region', {})
        region_level = region_all_dict.get('region_level')
        to_be_remove_region_id = []
        for cur_region_id in six.iterkeys(self.magic_region_info_dict):
            if cur_region_id not in region_dict:
                to_be_remove_region_id.append(cur_region_id)

        for rid in to_be_remove_region_id:
            self.set_region_param(rid, None, None, None)

        for region_id, region_info in six.iteritems(region_dict):
            if region_id not in self.magic_region_info_dict:
                region_pos = region_info[0]
                region_r = region_info[1]
                self.set_region_param(region_id, region_pos, region_r, {})

        if self.magic_checker:
            if self.magic_region_info_dict:
                self.magic_checker.init_timer()
            else:
                self.magic_checker.clear_timer()
                self.magic_checker.check_in_magic_region()
        return

    def set_region_param(self, region_id, pos, radius, data):
        if pos and radius:
            self.magic_region_info_dict[region_id] = (
             pos, radius, data)
            self.create_region_model(region_id)
            global_data.emgr.init_magic_region.emit(region_id)
        else:
            if region_id in self.magic_region_info_dict:
                del self.magic_region_info_dict[region_id]
            self.remove_region_model(region_id)
            global_data.emgr.remove_magic_region.emit(region_id)

    def get_region_param(self, region_id):
        return self.magic_region_info_dict.get(region_id, [None, None, None])

    def create_region_model(self, region_id):
        if region_id in self.magic_region_model_id_dict:
            return
        region_pos, region_r, region_data = self.get_region_param(region_id)
        path = 'effect/fx/niudan/s10_quyu.sfx'
        if not path:
            return
        pos = math3d.vector(region_pos[0], region_pos[1], region_pos[2])

        def create_sfx_cb(sfx):
            sfx.scale = math3d.vector(region_r / 42.0, 10, region_r / 42.0)

        self.remove_region_model(region_id)
        region_model_id = global_data.sfx_mgr.create_sfx_in_scene(path, pos, on_create_func=create_sfx_cb)
        self.magic_region_model_id_dict[region_id] = region_model_id

    def remove_region_model(self, region_id=None):
        if region_id is not None:
            if region_id in self.magic_region_model_id_dict:
                global_data.sfx_mgr.remove_sfx_by_id(self.magic_region_model_id_dict[region_id])
                del self.magic_region_model_id_dict[region_id]
        return

    def set_magic_rune_id(self, rune_id):
        self.applied_magic_rune_id = rune_id
        if rune_id:
            ui = global_data.ui_mgr.show_ui('MagicRuneDisplayUI', 'logic.comsys.battle.Magic')
            ui and ui.update_rune_id(rune_id)
        else:
            global_data.ui_mgr.close_ui('MagicRuneDisplayUI')