# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/Sys3DPlayerInfoMgr.py
from __future__ import absolute_import
import six
from logic.vscene.part_sys.ScenePartSysBase import ScenePartSysBase
import world
import math3d
import logic.gutils.map_3d_utils as mutil
from logic.gutils.map_utils import get_world_pos_from_map
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon.common_const.battle_const import MAP_COL_BLUE, MAP_COL_GREEN, MAP_COL_RED, MAP_COL_YELLOW
from mobile.common.EntityManager import EntityManager
from common.utils.cocos_utils import ccp
BLUE_RES = 'effect/fx/scenes/common/biaozhi/3dmap_locate_blue_i.sfx'
GREEN_RES = 'effect/fx/scenes/common/biaozhi/3dmap_locate_green_i.sfx'
RED_RES = 'effect/fx/scenes/common/biaozhi/3dmap_locate_red_i.sfx'
YELLOW_RES = 'effect/fx/scenes/common/biaozhi/3dmap_locate_yellow_i.sfx'
BLUE_MARK_RES = 'effect/fx/scenes/common/map/map_biaoji_blue.sfx'
GREEN_MARK_RES = 'effect/fx/scenes/common/map/map_biaoji_green.sfx'
RED_MARK_RES = 'effect/fx/scenes/common/map/map_biaoji_red.sfx'
YELLOW_MARK_RES = 'effect/fx/scenes/common/map/map_biaoji_yellow.sfx'
PLAYER_RES_MAP = {MAP_COL_BLUE: BLUE_RES,
   MAP_COL_GREEN: GREEN_RES,
   MAP_COL_RED: RED_RES,
   MAP_COL_YELLOW: YELLOW_RES
   }
MARK_RES_MAP = {MAP_COL_BLUE: BLUE_MARK_RES,
   MAP_COL_GREEN: GREEN_MARK_RES,
   MAP_COL_RED: RED_MARK_RES,
   MAP_COL_YELLOW: YELLOW_MARK_RES
   }

class Sys3DPlayerInfoMgr(ScenePartSysBase):

    def __init__(self):
        super(Sys3DPlayerInfoMgr, self).__init__()
        self.gui_map_model_ref = None
        self.player_ids = []
        self.player_targets = {}
        self.local_widgets = {}
        self.local_marks = {}
        self.local_marks2 = {}
        self.local_marks_pos = {}
        self.init_events()
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 1)
        return

    def init_events(self):
        global_data.emgr.on_player_parachute_stage_changed += self.on_player_parachute_stage_changed
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        global_data.emgr.net_reconnect_event += self.on_login_reconnect
        global_data.emgr.map_3d_model_loaded_event += self.map_model_loaded

    def map_model_loaded(self, model):
        import weakref
        self.gui_map_model_ref = weakref.ref(model)

    def on_login_reconnect(self):
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.player_targets.clear()
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.on_update, 1)

    def on_update(self):
        if not global_data.player or not global_data.player.logic:
            return
        player = global_data.player.logic
        if player.share_data.ref_parachute_stage == parachute_utils.STAGE_NONE:
            return
        new_player_ids = player.ev_g_groupmate()
        self.update_new_player_ids(new_player_ids)

    def update_new_player_ids(self, new_player_ids):
        old_ids = self.player_ids
        cnt_ids = []
        for _old_id in old_ids:
            if _old_id not in new_player_ids:
                self.del_item(_old_id)
            else:
                cnt_ids.append(_old_id)

        for _new_id in new_player_ids:
            if self.add_item(_new_id):
                cnt_ids.append(_new_id)

        self.player_ids = cnt_ids
        for player_id in self.player_ids:
            self.update_player_info(player_id)
            self.check_player_mark(player_id)

    def add_item(self, player_id):
        if player_id in self.local_widgets:
            return
        else:
            map_rt = global_data.emgr.get_3d_map_rt_event.emit()[0]
            if not map_rt:
                return False
            if not global_data.player or not global_data.player.logic:
                return False
            player = global_data.player.logic
            final_mat = mutil.FINAL_WORLD_MAT
            map_model = self.gui_map_model_ref() if self.gui_map_model_ref else None
            if map_model and map_model.valid:
                final_mat = map_model.world_transformation
            teammate_infos = player.ev_g_teammate_infos()
            player_info = teammate_infos.get(player_id, {})
            color = player.ev_g_group_color(player_id)
            res_path = PLAYER_RES_MAP.get(color, BLUE_RES)
            sfx = world.sfx(res_path)
            pos = player_info.get('pos', (0, 0, 0))
            map_pos = mutil.trans_world_pos_to_3dmap_pos(math3d.vector(*pos)) * final_mat
            map_rt.add_sfx(sfx, pos=map_pos, rotation_matrix=mutil.END_ROT_MAT, scale=math3d.vector(10, 10, 10))
            self.local_widgets[player_id] = sfx
            return True

    def add_player_mark(self, player_id):
        if player_id in self.local_marks:
            return False
        map_rt = global_data.emgr.get_3d_map_rt_event.emit()[0]
        if not map_rt:
            return False
        if not global_data.player or not global_data.player.logic:
            return
        player = global_data.player.logic
        color = player.ev_g_group_color(player_id)
        res_path = MARK_RES_MAP.get(color, BLUE_MARK_RES)
        mark_sfx = world.sfx(res_path)
        map_rt.add_sfx(mark_sfx, pos=math3d.vector(0, 0, 0), rotation_matrix=mutil.END_ROT_MAT, scale=math3d.vector(3, 3, 3))
        self.local_marks[player_id] = mark_sfx
        self.check_player_mark(player_id)
        return mark_sfx

    def del_player_mark(self, player_id):
        if player_id in self.local_marks:
            sfx = self.local_marks[player_id]
            if sfx and sfx.valid:
                sfx.destroy()
            del self.local_marks[player_id]

    def del_item(self, player_id):
        if player_id in self.local_widgets:
            sfx = self.local_widgets[player_id]
            if sfx and sfx.valid:
                sfx.destroy()
            del self.local_widgets[player_id]

    def clear(self):
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
            self.update_timer_id = None
        for sfx in six.itervalues(self.local_widgets):
            if sfx and sfx.valid:
                sfx.destroy()

        for sfx in six.itervalues(self.local_marks):
            if sfx and sfx.valid:
                sfx.destroy()

        self.local_widgets.clear()
        self.local_marks.clear()
        self.player_ids = []
        self.player_targets = {}
        return

    def update_player_info(self, player_id):
        if player_id not in self.local_widgets:
            return
        else:
            player_pos_sfx = self.local_widgets[player_id]
            if not player_pos_sfx or not player_pos_sfx.valid:
                del self.local_widgets[player_id]
                return
            target = self.get_target_by_id(player_id)
            if target and target.logic:
                player = target.logic
                pos = player.ev_g_position()
                if not pos:
                    pos = player.ev_g_model_position()
                return pos or None
            final_mat = mutil.FINAL_WORLD_MAT
            if self.gui_map_model_ref:
                map_model = self.gui_map_model_ref() if 1 else None
                if map_model and map_model.valid:
                    final_mat = map_model.world_transformation
                map_pos = mutil.trans_world_pos_to_3dmap_pos(pos) * final_mat
                player_pos_sfx.position = map_pos
                player_pos_sfx.world_rotation_matrix = final_mat
            return

    def get_target_by_id(self, player_id):
        if player_id in self.player_targets:
            target = self.player_targets[player_id]
            if target and target.logic and target.logic.is_valid():
                return target
        else:
            target = EntityManager.getentity(player_id)
            if target and target.logic and target.logic.is_valid():
                self.player_targets[player_id] = target
                return target
        return None

    def check_player_mark(self, player_id):
        target = self.get_target_by_id(player_id)
        if target and target.logic:
            player = target.logic
            cnt_mark_info = player.ev_g_warning_drawn_map_mark() or None
            cnt_mark_info or self.del_player_mark(player_id)
            return
        else:
            player_mark = None
            if player_id not in self.local_marks:
                player_mark = self.add_player_mark(player_id)
            else:
                player_mark = self.local_marks[player_id]
            if not player_mark or not player_mark.valid:
                return
            final_mat = mutil.FINAL_WORLD_MAT
            if self.gui_map_model_ref:
                gui_model = self.gui_map_model_ref() if 1 else None
                if gui_model and gui_model.valid:
                    final_mat = gui_model.world_transformation
                pos = cnt_mark_info['v3d_map_pos']
                last_pos = self.local_marks_pos.get(player_id, None)
                if not last_pos or (last_pos - pos).length > 0:
                    player_mark.restart()
                self.local_marks_pos[player_id] = pos
                map_pos = mutil.trans_world_pos_to_3dmap_pos(pos) * final_mat
                player_mark.position = map_pos
                player_mark.rotation_matrix = final_mat
            return

    def on_player_parachute_stage_changed(self, *args):
        if not global_data.player or not global_data.player.logic:
            return
        stage = global_data.player.logic.share_data.ref_parachute_stage
        if stage not in (parachute_utils.STAGE_PLANE, parachute_utils.STAGE_MECHA_READY, parachute_utils.STAGE_NONE):
            self.clear()

    def destroy(self):
        self.clear()