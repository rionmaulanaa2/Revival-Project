# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComExerciseTargetCollision.py
from __future__ import absolute_import
from .ComCommonShootCollision import ComCommonShootCollision
import math3d
import collision
from logic.gcommon.common_const import collision_const
from logic.gcommon.time_utility import get_server_time
import time
from logic.gcommon.const import HIT_PART_BODY, HIT_PART_HEAD

class ComExerciseTargetCollision(ComCommonShootCollision):
    BIND_EVENT = ComCommonShootCollision.BIND_EVENT.copy()
    BIND_EVENT.update({'E_MACHINE_MOVING': '_set_target_final',
       'E_GM_SWITCH_MOVE': '_gm_switch_move',
       'E_ON_FROZEN': '_handle_target_frozen',
       'G_CHECK_SHOOT_INFO': '_check_shoot_info'
       })
    LERP_FIXED_LENGTH = 1
    HS_RATIO = 0.82

    def __init__(self):
        super(ComExerciseTargetCollision, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComExerciseTargetCollision, self).init_from_dict(unit_obj, bdict)
        start_pos = math3d.vector(*bdict.get('cur_start', [-217, 812, 18030]))
        final_pos = math3d.vector(*bdict['cur_dest']) if 'cur_dest' in bdict else None
        period = bdict.get('cur_period', 1.0)
        start_time = bdict.get('cur_start_time') or get_server_time()
        self._cur_pos = math3d.vector(*bdict.get('position', [-217, 812, 18030]))
        self._cur_final_pos = final_pos if final_pos else self._cur_pos
        self._cur_final_time = max(start_time + period - get_server_time(), 0) + time.time()
        self._cur_speed = (final_pos - start_pos) * (1.0 / period) if final_pos else math3d.vector(0, 0, 0)
        self.model = None
        self.tick_pos_timer_id = -1
        self.is_frozen = False
        return

    def _on_model_loaded(self, model, *args):
        self.col = collision.col_object(collision.MESH, model, 0, 0, 0, True)
        self.scene.scene_col.add_object(self.col)
        self.col.mask = collision_const.GROUP_MECHA_BALL | collision_const.GROUP_GRENADE | collision_const.GROUP_CHARACTER_INCLUDE | collision_const.GROUP_CAMERA_COLL | collision_const.GROUP_AUTO_AIM
        self.col.group = collision_const.GROUP_CHARACTER_INCLUDE | collision_const.GROUP_DYNAMIC_SHOOTUNIT
        self.col.position = model.position
        self.col.rotation_matrix = model.rotation_matrix
        global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
        global_data.emgr.scene_add_hit_mecha_event.emit(self.col.cid, self.unit_obj)
        self.model = model
        self.send_event('E_MODIFY_MODEL_SCALE', model)
        self.tick_pos_timer_id = global_data.game_mgr.get_post_logic_timer().register(func=self._tick_pos, interval=1, timedelta=True)

    def _set_target_final(self, final_pos, time_start, time_dual, move_index):
        self._cur_speed = (final_pos - self._cur_final_pos) * (1.0 / max(time_dual, 0.1))
        self._cur_final_time = time.time() + time_dual
        self._cur_final_pos = final_pos

    def _tick_pos(self, dt):
        if not self._cur_final_pos:
            return
        if self.is_frozen:
            self._cur_final_time += dt
        else:
            left_time = self._cur_final_time - time.time()
            self._cur_pos = self._cur_final_pos - self._cur_speed * max(left_time, 0)
            self.col.position = self._cur_final_pos - self._cur_speed * max(left_time - dt, 0)
            if G_POS_CHANGE_MGR:
                self.notify_pos_change(self._cur_pos)
            else:
                self.send_event('E_POSITION', self._cur_pos)

    def destroy(self):
        if self.tick_pos_timer_id:
            global_data.game_mgr.get_post_logic_timer().unregister(self.tick_pos_timer_id)
        self.tick_pos_timer_id = -1
        super(ComExerciseTargetCollision, self).destroy()

    def _destroy_shoot_collision(self):
        if self.col:
            global_data.emgr.scene_remove_hit_mecha_event.emit(self.col.cid)
        super(ComExerciseTargetCollision, self)._destroy_shoot_collision()

    def _check_shoot_info(self, begin, pdir, hit_pos=None):
        tag = self.ev_g_headshoot_tag()
        if not tag:
            return HIT_PART_BODY
        if not hit_pos:
            return HIT_PART_BODY
        hit_hight = (hit_pos - self._cur_pos).y
        total_hight = self.model.bounding_box_w.y * 2.0
        if hit_hight / total_hight >= self.HS_RATIO:
            return HIT_PART_HEAD
        return HIT_PART_BODY

    def _gm_switch_move(self, timestamp):
        if not timestamp:
            self._stop_timestamp = get_server_time()
            self._cur_start_time = None
        else:
            self._cur_start_time = timestamp + get_server_time() - self._stop_timestamp
        return

    def _handle_target_frozen(self, is_frozen):
        self.is_frozen = is_frozen