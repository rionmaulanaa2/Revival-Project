# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSphereShield.py
import world
import math3d
import collision
import render
import game3d
from common.cfg import confmgr
from .ComBaseModelAppearance import ComBaseModelAppearance
from logic.gcommon.common_const import scene_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
from logic.gcommon.common_const.collision_const import BUILDING_GROUP, GROUP_GRENADE, GROUP_SHOOTUNIT, GROUP_SHIELD, GROUP_AUTO_AIM
from logic.gutils.effect_utils import check_need_ignore_effect_behind_camera
from logic.gutils.client_unit_tag_utils import register_unit_tag
SHILED_ADD_BUFF = register_unit_tag(('LAvatar', 'LPuppet', 'LMecha'))

class ComSphereShield(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_SHILED_CHANGE_HP': '_on_hp_change',
       'E_HIT_BLOOD_SFX': '_on_be_hited',
       'G_CHECK_SHOOT_INFO': 'check_shoot_info',
       'G_IS_TEAMMATE': '_on_get_is_teammate',
       'G_IS_CAMPMATE': '_on_get_is_teammate',
       'G_CAN_THROUGH': '_on_can_through',
       'G_IS_SHIELD': 'is_shield'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComSphereShield, self).init_from_dict(unit_obj, bdict)
        self._timer = None
        self.col = None
        self.shield_no = str(bdict.get('item_type', '803202'))
        self.shield_res = confmgr.get('grenade_res_config', str(self.shield_no))
        self.shield_custom_param = self.shield_res.get('cCustomParam', {})
        self.shield_crack_sfx_list = self.shield_custom_param.get('shield_crack_sfx_list', [])
        self.change_sfx_hp_range = self.shield_custom_param.get('change_sfx_hp_range', [])
        self.sphere_radius = bdict.get('radius', 20) * self.shield_custom_param.get('extra_collison_scale', 2.6)
        self.hitted_sound = self.shield_custom_param.get('be_hitted_sound', 'm_8032_shield_hited')
        self.loop_sound = self.shield_custom_param.get('loop_sound', 'm_8032_shield_sfx')
        self.disappear_sound = self.shield_custom_param.get('disappear_sound', 'm_8032_shield_disappear')
        self._max_hp = bdict.get('max_hp', 100)
        self._hp = bdict.get('hp', 100)
        self._faction_id = bdict.get('faction_id', None)
        self._loop_sfx = None
        self._crack_sfx = None
        self._crack_level = -1
        self._loop_sound_id = None
        self._sound_id = None
        return

    def get_model_info(self, unit_obj, bdict):
        model_path = self.shield_custom_param.get('shield_collision', 'effect/mesh/common/8032/8032_hudun_collision.gim')
        if model_path.endswith('.sfx'):
            self.load_model = self.load_sfx
        return (model_path, None, None)

    def cache(self):
        super(ComSphereShield, self).cache()

    def check_shoot_info(self, *args):
        return 0

    def update_crack_sfx(self, hp):
        crack_level = -1
        for i in range(len(self.change_sfx_hp_range)):
            if hp < self.change_sfx_hp_range[i]:
                break
            crack_level = i

        if self._crack_level != crack_level:
            global_data.sfx_mgr.remove_sfx_by_id(self._crack_sfx)
            self._crack_sfx = global_data.sfx_mgr.create_sfx_in_scene(self.shield_crack_sfx_list[self._crack_level], math3d.vector(self._position.x, self._position.y, self._position.z))
            self._crack_level = crack_level

    def _init_voice(self):
        self._sound_id = global_data.sound_mgr.register_game_obj('m_8032_shield_sfx_' + str(self.unit_obj.id))
        global_data.sound_mgr.set_position(self._sound_id, self.model.position)
        if self._loop_sound_id:
            global_data.sound_mgr.stop_playing_id(self._loop_sound_id)
        self._loop_sound = global_data.sound_mgr.post_event('m_8032_shield_sfx_3p', self._sound_id)

    def _on_hp_change(self, hp):
        self.update_crack_sfx(float(hp) / float(self._max_hp))
        self.send_event('E_HEALTH_HP_CHANGE', hp)

    def _on_be_hited(self, begin_pos, end_pos, shot_type, **kwargs):
        if check_need_ignore_effect_behind_camera(shot_type, end_pos):
            return
        else:
            if shot_type:
                sfx_path = confmgr.get('firearm_res_config', str(shot_type), 'cSfxHit')
                if sfx_path:
                    global_data.sfx_mgr.create_sfx_in_scene(sfx_path, end_pos, duration=0.5, int_check_type=CREATE_SRC_SIMPLE)
                    return
            col_type = kwargs.get('col_type', None)
            hit_sfx_path = ('effect/fx/weapon/bullet/jinshu.sfx', 'effect/fx/weapon/bullet/jinshu_dankong.sfx')
            if col_type:
                hit_sfx_path = scene_const.collision_sfx_map.get(col_type, hit_sfx_path)
            global_data.sfx_mgr.create_sfx_in_scene(hit_sfx_path[0], end_pos, int_check_type=CREATE_SRC_SIMPLE)
            if self.model:
                global_data.sound_mgr.play_event(self.hitted_sound, self.model.position)
            return

    def on_load_model_complete(self, model, user_data):
        model.visible = False
        self.update_crack_sfx(float(self._hp) / float(self._max_hp))
        mask = GROUP_GRENADE | GROUP_SHOOTUNIT | GROUP_AUTO_AIM
        group = BUILDING_GROUP | GROUP_SHOOTUNIT | GROUP_SHIELD | GROUP_AUTO_AIM
        model.scale = math3d.vector(self.sphere_radius, self.sphere_radius, self.sphere_radius)
        col_obj = collision.col_object(collision.MESH, model, mask, group, 0, True)
        global_data.game_mgr.scene.scene_col.add_object(col_obj)
        col_obj.position = self._position
        self.col = col_obj
        global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
        self._model.world_position = self._position
        if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate(self._faction_id):
            shield_loop = self.shield_custom_param.get('shield_begin_sfx', 'effect/fx/mecha/8032/8032_vice_dome_start.sfx')
        else:
            shield_loop = self.shield_custom_param.get('shield_begin_sfx_enemy', 'effect/fx/mecha/8032/8032_vice_dome_start_red.sfx')
        self._loop_sfx = global_data.sfx_mgr.create_sfx_in_scene(shield_loop, math3d.vector(self._position.x, self._position.y, self._position.z))
        self._init_voice()
        self.send_event('E_MODEL_LOADED', self._model, self._model.bounding_box)

    def _destroy_shoot_collision(self):
        if self.col:
            global_data.emgr.scene_remove_common_shoot_obj.emit(self.col.cid)
            self.scene.scene_col.remove_object(self.col)
            self.col = None
        return

    def _on_get_is_teammate(self, camp_id):
        return False

    def _on_can_through(self, camp_id):
        return camp_id == self._faction_id

    def is_shield(self):
        return True

    def destroy(self):
        self._destroy_shoot_collision()
        if self.model:
            global_data.sound_mgr.play_event(self.disappear_sound, self.model.position)
        if self._sound_id:
            global_data.sound_mgr.unregister_game_obj(self._sound_id)
        if self._loop_sound_id:
            global_data.sound_mgr.stop_playing_id(self._loop_sound_id)
        if self._loop_sfx:
            global_data.sfx_mgr.remove_sfx_by_id(self._loop_sfx)
            self._loop_sfx = None
        if self._crack_sfx:
            global_data.sfx_mgr.remove_sfx_by_id(self._crack_sfx)
            self._crack_sfx = None
        if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate(self._faction_id):
            shield_destroy = self.shield_custom_param.get('shield_destroy_sfx', 'effect/fx/mecha/8032/8032_vice_dome_end.sfx')
        else:
            shield_destroy = self.shield_custom_param.get('shield_destroy_enemy_sfx', 'effect/fx/mecha/8032/8032_vice_dome_end.sfx')
        global_data.sfx_mgr.create_sfx_in_scene(shield_destroy, math3d.vector(self._position.x, self._position.y, self._position.z), duration=2.0)
        super(ComSphereShield, self).destroy()
        return