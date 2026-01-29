# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMonsterAppearance.py
from __future__ import absolute_import
from .ComAnimatorAppearance import ComAnimatorAppearance
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
import math3d
import game3d
from logic.gutils import delay
from logic.vscene.parts.gamemode.CGameModeManager import CGameModeManager
from common.cfg import confmgr
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const.game_mode_const import GAME_MODE_PVES
from logic.gutils.effect_utils import check_need_ignore_effect_behind_camera
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE, GROUP_DEFAULT_VISIBLE
import collision
_HASH_RIM_COLOR = game3d.calc_string_hash('rim_color')
_HASH_RIM_MULTI = game3d.calc_string_hash('rim_multi')
ray_offset = math3d.vector(0, 5 * NEOX_UNIT_SCALE, 0)

class ComMonsterAppearance(ComAnimatorAppearance):
    BIND_EVENT = ComAnimatorAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'G_COLLISION_INFO': 'get_collision_info',
       'G_POSITION': 'get_monster_pos',
       'G_TRAJECTORY_START_POINT': 'get_trajectory_point',
       'G_WEAPON_TYPE': 'get_weapon_type',
       'G_CONFIG_DATA': 'get_config_data',
       'E_ENABLE_BEHAVIOR': 'on_enable_behavior',
       'E_UPDATE_MONSTER_FIGHT': 'update_fight',
       'E_GM_RESCALE_TARGET': 'gm_rescale_mecha_model',
       'E_HIT_BLOOD_SFX': '_on_be_hited',
       'E_HEALTH_HP_EMPTY': 'on_hp_empty'
       })
    BIND_LOAD_FINISH_EVENT = ComAnimatorAppearance.BIND_LOAD_FINISH_EVENT.copy()
    BIND_LOAD_FINISH_EVENT.update({'G_AIM_POSITION': 'get_aim_position',
       'G_CHARACTER_SIZE': 'get_character_size'
       })
    UP = math3d.vector(0, 1, 0)

    def __init__(self):
        super(ComMonsterAppearance, self).__init__()
        self._monster_id = None
        self._trajectory_index = 0
        self._cfg_data = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        self._monster_id = bdict.get('npc_id', None)
        self._pos = math3d.vector(*bdict.get('position', (0, 0, 0)))
        self._cfg_data = confmgr.get('monster_data', 'Monster', 'Content', str(self._monster_id))
        self._level_conf = {}
        self._level = bdict.get('pve_monster_level', None)
        if self._level:
            self._level_conf = confmgr.get('monster_level_data', str(self._monster_id), 'Content', str(self._level))
        self._res_path = self.get_level_config_value('ResPath')
        self._model_scale = self.get_level_config_value('ModelScale')
        self._character_size = self.get_level_config_value('CharacterSize')
        self._y_offset = self.get_level_config_value('Yoffset')
        self._bounding_y = self.get_level_config_value('BoundingBoxY')
        self._is_fight = bdict.get('is_fight', False)
        self._night_sfx = bdict.get('night_sfx', False)
        super(ComMonsterAppearance, self).init_from_dict(unit_obj, bdict)
        self.update_fight(self._is_fight)
        self.sd.ref_sub_model_map = {}
        self.handle_sunshine()
        return

    def handle_sunshine(self):
        self.C_SIZE = [
         0, 0]
        self.Y_OFF = 0
        self.M_SCALE = 0
        self.B_Y = 0
        if not global_data.use_sunshine:
            return
        p = global_data.sunshine_monster_col_dict
        if not p:
            return
        m_id = p.get('monster_id', 0)
        if m_id == self._monster_id:
            self.C_SIZE = p.get('c_size', [0, 0])
            self.Y_OFF = p.get('y_offset', 0)
            self.M_SCALE = p.get('scale', 0)
            self.B_Y = p.get('bounding_y', 0)

    def get_config_data(self):
        return self._cfg_data or {}

    def get_character_size(self):
        return self._character_size

    def get_level_config_value(self, key):
        if self._level_conf:
            ret = self._level_conf.get(key, None)
            if ret:
                return ret
        return self._cfg_data.get(key, None)

    def get_model_info(self, unit_obj, bdict):
        if self._monster_id == 9003:
            env = CGameModeManager().get_enviroment()
            if env == 'snow_night':
                return (confmgr.get('script_gim_ref')['8903_snow_night'], None, None)
        model_path = self._res_path
        dir = bdict.get('monster_dir', None)
        forward = None
        if dir:
            forward = math3d.vector(*dir)
            forward.normalize()
        data = {'forward': forward}
        return (model_path, None, data)

    def on_load_model_complete(self, model, userdata):
        if not model:
            return
        else:
            if self.sd.ref_is_pve_monster:
                model.visible = False
            model.position = self._pos
            from common.animate import animator
            xml_path = self._cfg_data.get('xml_path', None)
            if not xml_path:
                pass
            self._animator = animator.Animator(model, xml_path, self.unit_obj)
            self._animator.Load(False, self.on_load_animator_complete, userdata)
            self.send_event('E_HUMAN_MODEL_LOADED', model, userdata)
            if userdata:
                forward = userdata.get('forward', None)
                if forward:
                    mat = math3d.matrix.make_orient(forward, self.UP)
                    model.rotation_matrix = mat
            model_scale = self.M_SCALE if self.M_SCALE else self._model_scale
            model.scale = math3d.vector(model_scale, model_scale, model_scale)
            self.update_fight(self._is_fight)
            char_size = self.C_SIZE if self.C_SIZE[0] else self._character_size
            y_offset = self.Y_OFF * NEOX_UNIT_SCALE if self.Y_OFF else self._y_offset * NEOX_UNIT_SCALE
            bounding_box_y = self.B_Y if self.B_Y else self._bounding_y
            if bounding_box_y:
                bounding_box_y *= 0.5
            else:
                bounding_box_y = model.bounding_box.y
            self.send_event('E_RESET_CHAR_SIZE', char_size[0] * NEOX_UNIT_SCALE / 2, char_size[1] * NEOX_UNIT_SCALE, bounding_box_y * model_scale + y_offset)
            if self._night_sfx:
                global_data.sfx_mgr.create_sfx_in_scene('effect/fx/monster/yemu_monster/ym_down_guangzhu.sfx', model.position)
            sub_model_socket = self._cfg_data.get('SubModelSocket', None)
            if sub_model_socket:
                sub_model = model.get_socket_obj(sub_model_socket)
                if sub_model:
                    self.sd.ref_sub_model_map[sub_model_socket] = [
                     sub_model]
            global_data.emgr.pve_monster_init.emit(self.unit_obj)
            return

    def on_hp_empty(self, *args):
        global_data.emgr.pve_monster_die.emit(self.unit_obj)
        self.send_event('E_DISABLE_DRIVER')

    def on_model_destroy(self):
        global_data.emgr.pve_monster_destroy.emit(self.unit_obj)

    def on_enable_behavior(self, *args):
        if self.model and self.model.valid:
            model_scale = self._model_scale
            char_size = self.C_SIZE if self.C_SIZE[0] else self._character_size
            y_offset = self.Y_OFF * NEOX_UNIT_SCALE if self.Y_OFF else self._y_offset * NEOX_UNIT_SCALE
            bounding_box_y = self.B_Y if self.B_Y else self._bounding_y
            if bounding_box_y:
                bounding_box_y *= 0.5
            else:
                bounding_box_y = self.model.bounding_box.y
            self.send_event('E_RESET_CHAR_SIZE', char_size[0] * NEOX_UNIT_SCALE / 2, char_size[1] * NEOX_UNIT_SCALE, bounding_box_y * model_scale + y_offset)

    def on_touch_ground(self, *args):
        if self.sd.ref_is_pve_monster:
            pos = self.ev_g_position()
            start_pos = pos + ray_offset
            end_pos = pos - ray_offset
            group = GROUP_CHARACTER_INCLUDE & ~GROUP_DEFAULT_VISIBLE
            mask = group
            scene = global_data.game_mgr.scene
            result = scene.scene_col.hit_by_ray(start_pos, end_pos, 0, group, mask, collision.INCLUDE_FILTER, False)
            if result and result[0]:
                ret_pos = result[1]
                if abs(ret_pos.y - pos.y) > 1.0:
                    self.send_event('E_POSITION', ret_pos)

    def get_monster_pos(self):
        if self.model and self.model.valid:
            return self.model.position
        else:
            return self._pos

    def get_weapon_type(self):
        return self._cfg_data.get('WeaponId', 1001)

    def get_trajectory_point(self):
        if self.model and self.model.valid:
            mat = self.model.get_socket_matrix('fx_spark_kaihuo_0%d' % (self._trajectory_index + 1), world.SPACE_TYPE_WORLD)
            self._trajectory_index = 1 - self._trajectory_index
            if mat:
                return mat.translation
            return self.model.center_w
        else:
            return None

    def get_collision_info(self):
        if self.model:
            return {'bind_bone': 'biped'
               }
        else:
            return {}

    def get_aim_position(self):
        socket = self._model.get_socket_matrix('part_point1', world.SPACE_TYPE_WORLD)
        if socket:
            return socket.translation
        else:
            return None

    @execute_by_mode(False, GAME_MODE_PVES)
    def update_fight(self, is_fight):
        self._is_fight = is_fight
        fight_param = (1.0, 0.0, 0.0, 0.0) if is_fight else (0.0, 1.0, 0.0, 0.0)
        rim_multi = 10.0
        if self.model and self.model.valid:
            sub_material = self.model.get_sub_material(1)
            if sub_material:
                sub_material.set_var(_HASH_RIM_COLOR, 'rim_color', fight_param)
                sub_material.set_var(_HASH_RIM_MULTI, 'rim_multi', rim_multi)

    def _on_be_hited(self, begin_pos, end_pos, shot_type, **kwargs):
        global_data.sound_mgr.play_sound_optimize('Play_bullet_hit', self.unit_obj, end_pos, ('bullet_hit_material',
                                                                                              'metal'))
        if check_need_ignore_effect_behind_camera(shot_type, end_pos):
            return
        else:
            if shot_type:
                res_conf = confmgr.get('firearm_res_config', str(shot_type), default={})
                sfx_path = res_conf.get('cSfxHit')
                sfx_scale = res_conf.get('cSfxHitScale', None)
                if sfx_path:
                    if not sfx_scale:
                        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, end_pos, duration=0.5, int_check_type=CREATE_SRC_SIMPLE)
                        return
                    else:
                        scale = math3d.vector(sfx_scale, sfx_scale, sfx_scale)

                        def cb(sfx):
                            sfx.scale = scale

                        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, end_pos, duration=0.5, on_create_func=cb, int_check_type=CREATE_SRC_SIMPLE)
                        return

            return

    def gm_rescale_mecha_model(self, scl_xyz):
        model = self.ev_g_model()
        if not model:
            return
        f_scl_xyz = float(scl_xyz)
        model_scale = self._model_scale
        model.scale = math3d.vector(model_scale * f_scl_xyz, model_scale * f_scl_xyz, model_scale * f_scl_xyz)
        char_size = self.C_SIZE if self.C_SIZE[0] else self._character_size
        y_offset = self.Y_OFF * NEOX_UNIT_SCALE if self.Y_OFF else self._y_offset * NEOX_UNIT_SCALE
        bounding_box_y = self.B_Y if self.B_Y else self._bounding_y
        if bounding_box_y:
            bounding_box_y *= 0.5
        else:
            bounding_box_y = model.bounding_box.y
        delay.call(1, lambda : self.send_event('E_RESET_CHAR_SIZE', char_size[0] * NEOX_UNIT_SCALE / 2 * f_scl_xyz, char_size[1] * NEOX_UNIT_SCALE * f_scl_xyz, bounding_box_y * model_scale * f_scl_xyz + y_offset * f_scl_xyz))