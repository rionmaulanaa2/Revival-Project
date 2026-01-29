# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_building/ComDeathDoor.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
import logic.gcommon.common_const.ai_const as ai_const
import math3d
import math
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
from logic.gutils.effect_utils import check_need_ignore_effect_behind_camera
DESTROY = 0
DAMAGED = 1

class ComDeathDoor(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_HEALTH_HP_CHANGE': 'on_change_hp',
       'E_HIT_BLOOD_SFX': 'on_be_hited_by_ray',
       'E_HIT_SHIELD_SFX': 'on_be_hited_by_bomb',
       'G_AI_CAN_ATK_TYPE': '_get_ai_can_atk_type',
       'G_IS_DOOR_DESTROYED': '_is_door_destroyed',
       'G_IS_SHIELD': 'on_get_shield'
       }

    def __init__(self):
        super(ComDeathDoor, self).__init__()
        self.state_effects = {}
        self.destroyed = False
        self.last_hp = 0
        self._max_hp = 0
        self._hp = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComDeathDoor, self).init_from_dict(unit_obj, bdict)
        self._max_hp = int(bdict.get('max_hp', 100))
        self._hp = int(bdict.get('hp', self._max_hp))
        self.npc_id = bdict.get('npc_id')
        door_cfg_data = global_data.game_mode.get_cfg_data('door_data')
        self.door_info = door_cfg_data.get(str(self.npc_id), {})
        self.door_break_sfxs = self.door_info.get('break_sfx_path', [])
        self.door_break_scale = self.door_info.get('break_sfx_scale', [1.0, 1.0, 1.0])
        if global_data.death_battle_door_col:
            col = global_data.death_battle_door_col.get_door_col(self.npc_id)
            col and col.set_trigger(self._hp <= 0)
        pos = self.door_info.get('pos')
        rot = self.door_info.get('rot')
        self.door_pos = math3d.vector(*pos)
        self.door_rot_mat = math3d.euler_to_matrix(math3d.vector(math.pi * rot[0] / 180, math.pi * rot[1] / 180, math.pi * rot[2] / 180))

    def cache(self):
        self._clear_light_shield()
        super(ComDeathDoor, self).cache()

    def _is_door_destroyed(self):
        return self.destroyed

    def on_model_loaded(self, model):
        self.on_change_hp(self._hp)

    def on_change_hp(self, hp, *args):
        is_destroyed = False
        cur_hp = hp * 1.0 / self._max_hp
        if cur_hp >= 0.6:
            self.del_state_effect(DAMAGED)
        elif cur_hp < 0.6 <= self.last_hp:
            self.del_state_effect(DAMAGED)
            self.show_state_effect(DAMAGED, sfx_posix='01')
        elif cur_hp < 0.4 <= self.last_hp:
            self.del_state_effect(DAMAGED)
            self.show_state_effect(DAMAGED, sfx_posix='02')
        elif cur_hp < 0.2 <= self.last_hp:
            self.del_state_effect(DAMAGED)
            self.show_state_effect(DAMAGED, sfx_posix='03')
        self.last_hp = cur_hp
        if hp <= 0:
            self.del_state_effect(DAMAGED)
            self.show_state_effect(DESTROY, 2.0)
            global_data.sound_mgr.play_sound('Play_props', self.door_pos, ('props_action',
                                                                           'sidou_shield_break'))
            is_destroyed = True
        if is_destroyed != self.destroyed:
            col = global_data.death_battle_door_col.get_door_col(self.npc_id)
            col and col.set_trigger(is_destroyed)
            self.send_event('E_DOOR_STATE_CHANGE', is_destroyed)
            self.check_door_notice_ui()
        self.destroyed = is_destroyed

    def _clear_light_shield(self):
        for sfx_id in six.itervalues(self.state_effects):
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

    def destroy(self):
        self._clear_light_shield()
        super(ComDeathDoor, self).destroy()

    def show_state_effect(self, state, duration=-1, sfx_posix=''):
        model = self.ev_g_model()
        if not model:
            return

        def create_cb(sfx):
            sfx.rotation_matrix = self.door_rot_mat
            sfx.scale = math3d.vector(*self.door_break_scale)

        color_txt = '_blue' if self.ev_g_is_teammate_door() else '_red'
        sfx_path = ''.join([self.door_break_sfxs[state], color_txt, sfx_posix, '.sfx'])
        self.state_effects[state] = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, model.center_w, duration=duration, on_create_func=create_cb)

    def del_state_effect(self, state):
        if state in self.state_effects:
            global_data.sfx_mgr.remove_sfx_by_id(self.state_effects[state])

    def _get_ai_can_atk_type(self):
        return ai_const.AI_CAN_ATK_TYPE_BUILDING

    def on_be_hited_by_ray(self, begin_pos, end_pos, shot_type, **kwargs):
        self.show_hit_effect(begin_pos, end_pos, shot_type)

    def on_be_hited_by_bomb(self, begin=None, end=None, itype=None):
        pass

    def show_hit_effect(self, begin_pos, end_pos, shot_type):
        if end_pos is None:
            return
        else:
            model = self.ev_g_model()
            if not (model and model.valid):
                return
            if check_need_ignore_effect_behind_camera(shot_type, end_pos):
                return
            hit_vect = end_pos - begin_pos
            if hit_vect.is_zero:
                hit_vect = math3d.vector(0, 0, 1)
            else:
                hit_vect.normalize()
            check_pos = end_pos - hit_vect * 10
            check_dir = hit_vect * 30
            result = model.hit_by_ray(check_pos, check_dir)
            if result[0]:
                normal = model.get_triangle_normal(result[2], result[3])
                normal = normal if hit_vect.dot(normal) > 0 else -normal
                hit_sfx = 'effect/fx/scenes/common/sidou/sd_men_blue_hit.sfx' if self.ev_g_is_teammate_door() else 'effect/fx/scenes/common/sidou/sd_men_red_hit.sfx'

                def create_cb(sfx):
                    global_data.sfx_mgr.set_rotation_by_world_normal(sfx, normal * -1)

                global_data.sfx_mgr.create_sfx_in_scene(hit_sfx, end_pos, on_create_func=create_cb, int_check_type=CREATE_SRC_SIMPLE)
            return

    def check_door_notice_ui(self):
        from logic.gcommon.common_const import battle_const
        msg = None
        if self.last_hp <= 0:
            if self.ev_g_is_teammate_door():
                msg = {'i_type': battle_const.TDM_BLUE_DOOR_DESTROYED}
            else:
                msg = {'i_type': battle_const.TDM_RED_DOOR_DESTROYED}
        elif self.last_hp >= 1.0:
            if self.ev_g_is_teammate_door():
                msg = {'i_type': battle_const.TDM_BLUE_DOOR_RECOVER}
            else:
                msg = {'i_type': battle_const.TDM_RED_DOOR_RECOVER}
        if msg:
            global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)
        return

    def on_get_shield(self):
        return True