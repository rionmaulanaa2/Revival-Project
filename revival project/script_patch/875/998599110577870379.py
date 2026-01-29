# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillPVEStoneShooter.py
from __future__ import absolute_import
import world
import math3d
import random
import collision
from common.cfg import confmgr
from .SkillBase import SkillBase
from common.utils.timer import CLOCK
from logic.gcommon import time_utility as tutil
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.idx_const import ExploderID
from logic.gcommon.common_const.collision_const import GROUP_DYNAMIC_SHOOTUNIT
from logic.gcommon.common_const.buff_const import BUFF_GLOBAL_KEY

class SkillPVEStoneShooter(SkillBase):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillPVEStoneShooter, self).__init__(skill_id, unit_obj, data)
        ext_info = confmgr.get('skill_conf', str(self._skill_id), 'ext_info', default={})
        self.valid_target_dist = ext_info.get('valid_target_dist', 25) * NEOX_UNIT_SCALE
        self._fire_socket = ext_info.get('fire_socket', 'part_point1')
        self._need_fire_cnt = 0
        self._timer_id = None
        self._regular_fire_cd = -1
        self.acc_fire = 0
        return

    def remote_do_skill(self, skill_data):
        fire_cnt = skill_data.get('fire_cnt', None)
        if not fire_cnt:
            return
        else:
            acc_fire = skill_data.get('acc_fire', None)
            if acc_fire is not None:
                self.acc_fire += 1
                if self.acc_fire < acc_fire:
                    return
                self.acc_fire = 0
            fire_cnt += self._unit_obj.ev_g_get_buff_cnt(BUFF_GLOBAL_KEY, skill_data.get('add_fire_cnt_by_buff_layer', None))
            self.fire(fire_cnt, skill_data.get('aim_closest', False))
            return

    def fire(self, fire_cnt, aim_closest):
        model = self._unit_obj.ev_g_model()
        if not model or not model.valid:
            return
        else:
            if model.has_socket(self._fire_socket):
                position = model.get_socket_matrix(self._fire_socket, world.SPACE_TYPE_WORLD).translation
            else:
                position = model.position
            scn = global_data.game_mgr.scene
            if not scn:
                return
            check_obj = collision.col_object(collision.SPHERE, math3d.vector(self.valid_target_dist, self.valid_target_dist, self.valid_target_dist))
            check_obj.position = position
            result = scn.scene_col.static_test(check_obj, 65535, GROUP_DYNAMIC_SHOOTUNIT, collision.INCLUDE_FILTER)
            if not result:
                return
            nearby_units = []
            fire_dirs = []
            for cobj in result:
                cid = cobj.cid
                unit_obj = global_data.emgr.scene_find_unit_event.emit(cid)[0]
                if not unit_obj or unit_obj in nearby_units or not unit_obj.sd.ref_is_pve_monster or unit_obj.ev_g_death():
                    continue
                nearby_units.append(unit_obj)
                unit_model = unit_obj.ev_g_model()
                if unit_model and unit_model.valid:
                    mat = None
                    if unit_model.has_socket('fx_buff'):
                        mat = unit_model.get_socket_matrix('fx_buff', world.SPACE_TYPE_WORLD)
                    if mat:
                        unit_pos = mat.translation
                    else:
                        unit_pos = unit_obj.ev_g_model_position() + math3d.vector(0, 0.5 * NEOX_UNIT_SCALE, 0)
                    fdir = unit_pos - position
                    if fdir.length_sqr < self.valid_target_dist * self.valid_target_dist:
                        fire_dirs.append(fdir)

            if not fire_dirs:
                return

            def fire_one(fire_dir):
                if not fire_dir.is_zero:
                    fire_dir.normalize()
                throw_item = {'uniq_key': ExploderID.gen(global_data.battle_idx),
                   'position': (
                              position.x, position.y, position.z),
                   'm_position': (
                                position.x, position.y, position.z),
                   'dir': (
                         fire_dir.x, fire_dir.y, fire_dir.z),
                   'up': (0, 1, 0),
                   'use_rot_mat': 1
                   }
                self._unit_obj.send_event('E_CALL_SYNC_METHOD', 'do_skill', [self._skill_id, (throw_item, 0)], True)

            if aim_closest:
                fire_dirs.sort(key=lambda x: x.length_sqr)
                dir_cnt = min(len(fire_dirs), fire_cnt)
                for i in range(dir_cnt):
                    fire_one(fire_dirs[i])

            else:
                for i in range(fire_cnt):
                    fire_one(fire_dirs[random.randrange(len(fire_dirs))])

            return