# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMonsterCollision.py
from __future__ import absolute_import
from six.moves import range
import weakref
import collision
import math3d
import random
from ..UnitCom import UnitCom
from common.cfg import confmgr
import logic.gcommon.common_const.collision_const as collision_const
from logic.gutils.scene_utils import apply_ragdoll_explosion, apply_ragdoll_custom_gravity
from logic.gutils.model_collision_utils import ModelCollisionAgent
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.const import COLOR_MASK, COLOR_PART_MAP, LEG_COLOR

class ComMonsterCollision(UnitCom):
    BIND_EVENT = {'E_HUMAN_MODEL_LOADED': 'on_humman_model_load',
       'E_DEATH': 'die',
       'E_HEALTH_HP_EMPTY': 'die',
       'G_HUMAN_COL_ID': 'get_human_col_id',
       'G_HUMAN_COL': 'get_human_col',
       'G_HUMAN_BASE_COL_ID': 'get_human_base_col_id',
       'G_HUMAN_COL_INFO': 'get_human_col_info',
       'G_MODEL_HIT_RAY': 'get_hit_by_ray_color',
       'G_SHOOT_PART': 'be_shoot_check',
       'G_HIT_MODEL': 'get_hit_model',
       'E_GM_RESCALE_TARGET': 'gm_rescale_mecha_model',
       'E_RECORD_ON_HIT_INFO': 'record_on_hit_info',
       'E_ADD_HANDY_SHIELD_COL': 'add_handy_shield_col',
       'E_REMOVE_HANDY_SHIELD_COL': 'remove_handy_shield_col'
       }

    def __init__(self):
        super(ComMonsterCollision, self).__init__()
        self.col = None
        self.handy_shield_col = None
        self._hit_ref = None
        self._load_mesh_task = None
        self.last_behit_info = None
        self.need_update = True
        self.sd.ref_mecha_relative_cols = set()
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComMonsterCollision, self).init_from_dict(unit_obj, bdict)
        self._monster_id = bdict.get('npc_id', '9001')
        self._dead = bdict.get('hp', 0) == 0
        self._cfg_data = confmgr.get('monster_data', 'Monster', 'Content', str(self._monster_id))
        self._level_conf = {}
        self._level = bdict.get('pve_monster_level', None)
        if self._level:
            self._level_conf = confmgr.get('monster_level_data', str(self._monster_id), 'Content', str(self._level))
        self._model_scale = self.get_level_config_value('ModelScale')
        self._collision_size = self.get_level_config_value('CollisonSize')
        self._hit_path = self.get_level_config_value('hit_path')
        self.model_col_agent = ModelCollisionAgent(self)
        self.handle_sunshine()
        return

    def tick(self, dt):
        model = self.ev_g_model()
        apply_ragdoll_custom_gravity(model)

    def handle_sunshine(self):
        self.SIZE = [
         0, 0, 0]
        self.BONE = 0
        if not global_data.use_sunshine:
            return
        p = global_data.sunshine_monster_col_dict
        if not p:
            return
        m_id = p.get('monster_id', 0)
        if m_id == self._monster_id:
            self.SIZE = p.get('s_size', [0, 0, 0])
            self.BONE = p.get('s_bone', 0)

    def get_level_config_value(self, key):
        if self._level_conf:
            ret = self._level_conf.get(key, None)
            if ret:
                return ret
        return self._cfg_data.get(key, None)

    def record_on_hit_info(self, attacker_id, bomb_id, hit_pos):
        self.last_behit_info = (
         attacker_id, bomb_id, hit_pos)

    def die(self, *args):
        if self.col:
            if self.col.cid in global_data.war_mecha_aim_objs:
                global_data.war_mecha_aim_objs.pop(self.col.cid)
            model = self.ev_g_model()
            if model:
                model.unbind_col_obj(self.col)
            global_data.emgr.scene_remove_shoot_mecha_event.emit(self.col.cid)
            self.scene.scene_col.remove_object(self.col)
            self.col = None
        model = self.ev_g_model()
        apply_ragdoll_explosion(model, self.last_behit_info)
        self.last_behit_info = None
        return

    def get_hit_model(self):
        return self._hit_ref()

    def _create_collision(self, model, scl_xyz=1):
        if self._dead:
            return
        if not self.scene:
            return
        self._remove_col()
        scale = self._model_scale
        size = self.SIZE if self.SIZE[0] else self._collision_size
        model_box = math3d.vector(*size) * NEOX_UNIT_SCALE
        self.col = collision.col_object(collision.BOX, model_box * scale * 1.1 * scl_xyz, 0, 0, 0)
        self.col.car_undrivable = True
        self.scene.scene_col.add_object(self.col)
        if self.ev_g_health_percent() > 0:
            global_data.war_mecha_aim_objs[self.col.cid] = self.unit_obj
        self.col.mask = collision_const.GROUP_GRENADE | collision_const.GROUP_DYNAMIC_SHOOTUNIT | collision_const.GROUP_AUTO_AIM
        self.col.group = collision_const.GROUP_DYNAMIC_SHOOTUNIT | collision_const.GROUP_AUTO_AIM
        self.col.kinematic = True
        self.col.is_unragdoll = True
        bone = self.BONE if self.BONE else self._cfg_data['BindBone']
        model.bind_col_obj(self.col, bone)
        self._hit_ref = weakref.ref(model)
        global_data.emgr.scene_add_shoot_mecha_event.emit(self.col.cid, self.unit_obj)
        global_data.emgr.scene_add_hit_mecha_event.emit(self.col.cid, self.unit_obj)

    def on_humman_model_load(self, model, *arg):
        import world
        import game3d
        self._create_collision(model)
        submesh_cnt = model.get_submesh_count()
        for i in range(submesh_cnt):
            if model.get_submesh_name(i) != 'hit':
                model.set_submesh_hitmask(i, world.HIT_SKIP)

        if self.col:
            self.model_col_agent.set_mask_and_group(self.col.mask, self.col.group)
            self.model_col_agent.load(model, self._hit_path)
            self.model_col_agent.set_cur_model(model)

    def _remove_col(self):
        if self.col:
            if self.col.cid in global_data.war_mecha_aim_objs:
                global_data.war_mecha_aim_objs.pop(self.col.cid)
            model = self.ev_g_model()
            if model:
                model.unbind_col_obj(self.col)
            global_data.emgr.scene_remove_shoot_mecha_event.emit(self.col.cid)
            global_data.emgr.scene_remove_hit_mecha_event.emit(self.col.cid)
            self.scene.scene_col.remove_object(self.col)
            self.col = None
        return

    def get_hit_by_ray_color(self, begin, pdir):
        if not self._hit_ref:
            return None
        else:
            return self.model_col_agent.check_shoot_part(begin, pdir)

    def be_shoot_check(self, color):
        color = color & COLOR_MASK
        color = color if color in COLOR_PART_MAP else LEG_COLOR
        return COLOR_PART_MAP[color]

    def get_human_col_info(self):
        return (
         self.col.group, self.col.mask)

    def get_human_base_col_id(self):
        if self.col:
            return self.col.cid
        else:
            return None

    def get_human_col_id(self):
        ret = []
        for col in [self.col, self.handy_shield_col]:
            if col:
                ret.append(col.cid)

        return ret

    def get_human_col(self):
        ret = []
        for col in [self.col, self.handy_shield_col]:
            if col:
                ret.append(col)

        return ret

    def destroy(self):
        self._remove_col()
        if self.model_col_agent:
            self.model_col_agent.destroy()
            self.model_col_agent = None
        super(ComMonsterCollision, self).destroy()
        return

    def add_handy_shield_col(self, col):
        self.handy_shield_col = col

    def remove_handy_shield_col(self):
        self.handy_shield_col = None
        return

    def gm_rescale_mecha_model(self, scl_xyz):
        f_scl_xyz = float(scl_xyz)
        model = self.ev_g_model()
        if not model:
            return
        self._remove_col()
        self._create_collision(model, f_scl_xyz)