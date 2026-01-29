# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/skill/client/SkillPVEStoneIce.py
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
from mobile.common.EntityManager import EntityManager

class SkillPVEStoneIce(SkillBase):

    def __init__(self, skill_id, unit_obj, data):
        super(SkillPVEStoneIce, self).__init__(skill_id, unit_obj, data)
        ext_info = confmgr.get('skill_conf', str(self._skill_id), 'ext_info', default={})
        self.valid_target_dist = ext_info.get('valid_target_dist', 25) * NEOX_UNIT_SCALE

    def remote_do_skill(self, skill_data):
        self.fire(skill_data)

    def fire(self, skill_data):
        fire_cnt = skill_data.get('fire_cnt', None)
        if not fire_cnt:
            return
        else:
            from_entity_id = skill_data.get('from_entity')
            from_entity = EntityManager.getentity(from_entity_id)
            if not from_entity or not from_entity.logic:
                return
            model = from_entity.logic.ev_g_model()
            if not model:
                return
            mat = model.get_socket_matrix('fx_buff', world.SPACE_TYPE_WORLD)
            if mat:
                fire_pos = mat.translation
            else:
                fire_pos = model.position
            scn = global_data.game_mgr.scene
            if not scn:
                return
            if skill_data.get('valid_target_dist'):
                valid_target_dist = skill_data.get('valid_target_dist') * NEOX_UNIT_SCALE
            else:
                valid_target_dist = self.valid_target_dist
            check_obj = collision.col_object(collision.SPHERE, math3d.vector(valid_target_dist, valid_target_dist, valid_target_dist))
            check_obj.position = fire_pos
            result = scn.scene_col.static_test(check_obj, 65535, GROUP_DYNAMIC_SHOOTUNIT, collision.INCLUDE_FILTER)
            if not result:
                return
            ignore_cids = []
            ignore_unit_ids = []
            nearby_units = []
            fire_dirs = []
            for cobj in result:
                cid = cobj.cid
                unit_obj = global_data.emgr.scene_find_unit_event.emit(cid)[0]
                if not unit_obj or unit_obj in nearby_units or not unit_obj.sd.ref_is_pve_monster or unit_obj.ev_g_death():
                    continue
                if from_entity and from_entity.id == unit_obj.id:
                    ignore_cids.append(cid)
                    ignore_unit_ids.append(from_entity.id)
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
                    fdir = unit_pos - fire_pos
                    if fdir.length_sqr < valid_target_dist * valid_target_dist:
                        fire_dirs.append(fdir)

            if not fire_dirs:
                return

            def fire_one(fire_dir):
                if not fire_dir.is_zero:
                    fire_dir.normalize()
                throw_item = {'uniq_key': ExploderID.gen(global_data.battle_idx),
                   'position': (
                              fire_pos.x, fire_pos.y, fire_pos.z),
                   'm_position': (
                                fire_pos.x, fire_pos.y, fire_pos.z),
                   'dir': (
                         fire_dir.x, fire_dir.y, fire_dir.z),
                   'up': (0, 1, 0),
                   'use_rot_mat': 1,
                   'client_extra': {'ignore_cobj_ids': ignore_cids,'ignore_unit_ids': ignore_unit_ids}}
                self._unit_obj.send_event('E_CALL_SYNC_METHOD', 'do_skill', [self._skill_id, (throw_item, 0)], True)

            fire_dirs.sort(key=lambda x: x.length_sqr)
            dir_cnt = min(len(fire_dirs), fire_cnt)
            for i in range(dir_cnt):
                fire_one(fire_dirs[i])

            return