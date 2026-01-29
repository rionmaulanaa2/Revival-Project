# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffectCommon.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gcommon.component.UnitCom import UnitCom
import time
import math3d
import collision
import game3d
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.common_const import water_const
from common.utils.timer import CLOCK, RELEASE
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
from logic.gcommon.common_const.battle_const import MECHA_DAMAGED_HP_RATE
from logic.gutils.mecha_skin_utils import get_accurate_mecha_skin_info_from_fasion_data, get_specific_mecha_skin_res_readonly_res_path
from logic.gutils.client_unit_tag_utils import preregistered_tags
from common.cfg import confmgr
import world
from logic.gcommon.item.item_const import FASHION_POS_SUIT
ON_GROUND_SFX = {'common': {'small': 'effect/fx/mecha/8008/8008_luodi_s.sfx',
              'middle': 'effect/fx/mecha/8008/8008_luodi_m.sfx',
              'large': 'effect/fx/mecha/8008/8008_luodi.sfx'
              },
   201801151: {'small': 'effect/fx/mecha/8011/8011_s01_jump_01_smoke.sfx',
               'middle': 'effect/fx/mecha/8011/8011_s01_jump_02_smoke.sfx',
               'large': 'effect/fx/mecha/8011/8011_s01_jump_02_smoke.sfx'
               }
   }
WATER_RIPPLE_SFX = 'effect/fx/robot/common/water_mecha_piaofu.sfx'
WATER_MOVE_SFX = 'effect/fx/robot/common/water_mecha_lianyi.sfx'
ENTER_WATER_SFX = 'effect/fx/robot/common/water_mecha_chushui01.sfx'
EXIT_WATER_SFX = 'effect/fx/robot/common/water_mecha_chushui.sfx'
FIRE_EFFECT_SMALL = {'effect/fx/mecha/8012/8012_vice_ranshao.sfx': ['fx_buff_right', 'fx_buff_left', 'fx_buff_leg']}
FIRE_EFFECT_BIG = {'effect/fx/mecha/8012/8012_vice_ranshao_01.sfx': ['part_point1']}
OIL_EFFECT = {'effect/fx/mecha/8012/8012_youwu.sfx': ['fx_buff']}
EMP_EFFECT = {'effect/fx/robot/autobot/dianliu_lift_hand.sfx': ('fx_buff_left', 'fx_buff_leg'),
   'effect/fx/robot/autobot/dianliu_right_hand.sfx': ('fx_buff_right', ),
   'effect/fx/robot/autobot/dianliu_all.sfx': ('fx_buff', )
   }
DIE_EFFECT = {'effect/fx/robot/robot_qishi/qishi_die.sfx': ('fx_die', )
   }
REAPER_CURSE_EFFECT_ID = '103'
REAPER_CURSE_END_EFFECT_ID = '104'
REAPER_CURSE_SFX_PATH_MAP = {}
REAPER_CURSE_END_SFX_PATH_MAP = {}
HIGHLIGHT_EFFECT = 'effect/fx/robot/common/shouji_fresnel.sfx'
CLEAR_HIGHLIGHT_EFFECT = 'effect/fx/robot/common/clear_fresnel.sfx'
IGNORE_HIGHLIGHT_SKIN_ID_SET = {
 201801151}
HIGHLIGHT_LENGTH = 0.2
HIGHLIGHT_COLOR = (1.0, 0.45, 0.035, 0.411)
HIGHLIGHT_POW = 6.0
HIGHLIGHT_MULTI = 10.0
RIM_MULTI_HASH = game3d.calc_string_hash('rim_multi')
RIM_COLOR_HASH = game3d.calc_string_hash('rim_color')
RIM_POWER_HASH = game3d.calc_string_hash('rim_pow')
PVE_BLESS_EFFECT = {5110406: {'effect/fx/monster/pve_shuxing/pve_bing_buff_start.sfx': ['fx_buff']}}

class ComMechaEffectCommon(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_CREATE_SCENE_EFFECT': 'on_create_scene_effect',
       'E_CREATE_MODEL_EFFECT': 'on_create_model_effects',
       'E_REMOVE_MODEL_EFFECT': 'on_remove_model_effects',
       'G_SHOW_CD_EFFECT': 'on_show_cd_effect',
       'E_SHOW_ONGROUND_SFX': 'on_show_onground_sfx',
       'E_SHOW_SKILL_HIT_SFX': 'on_show_skill_hit_sfx',
       'E_WATER_EVENT': 'on_water_event',
       'E_MECHA_ENTER_DIVING': 'on_enter_diving',
       'E_MECHA_LEAVE_DIVING': 'on_leave_diving',
       'E_FIRE_EFFECT': 'on_fire_effect',
       'E_SHOW_LIGHT': '_on_show_light_effect',
       'E_ON_SELECTION_MODEL_BINDING': '_on_selection_model_binding',
       'E_ENABLE_SFX_SYNC': 'enable_sfx_sync',
       'E_BLOCK_EFFECT_SFX': 'on_block_effect_sfx',
       'E_ON_FROZEN': 'on_frozen',
       'E_BE_EXECUTED': 'on_be_executed',
       'E_CHANGE_MECHA_FASHION': ('refresh_skin_relevant_appearance', 99),
       'E_SET_DAMAGE_EFFECT_VISIBLE': '_set_damaged_effect_visible',
       'E_HEALTH_HP_CHANGE': 'on_hp_changed',
       'E_MAX_HP_CHANGED': 'on_max_hp_changed',
       'E_CREATE_REAPER_CURSE_EFFECT': 'on_create_reaper_curse_effect',
       'E_REMOVE_REAPER_CURSE_EFFECT': 'on_remove_reaper_curse_effect',
       'E_SWITCH_STATE_SOCKET': 'switch_ball_state',
       'E_SWITCH_MODEL': 'on_switch_model',
       'E_PVE_BLESS_EFFECT': 'on_pve_bless_effect'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffectCommon, self).init_from_dict(unit_obj, bdict)
        self._last_cast_time = 0
        self._block_sfx = False
        self.hit_sfx_id = None
        self.hit_sfx_timer = 0.0
        self.is_normal_hit = False
        self._last_pos = None
        self._cur_water_height = 0
        self._last_water_height = 0
        self._enter_water_sfx = None
        self._water_ripple_sfx_id = None
        self._water_move_sfx = None
        self._stop_timer_id = None
        self._cur_water_status = water_const.WATER_NONE
        self._wave_generate_timer = None
        self._onground_sfx_info = None
        self._sync_sfx = True
        self._model_sfx_ids = {}
        self._is_frozen = False
        self.highlight_event_registered = False
        self.on_ground_sfx_path_map = None
        self.mecha_effect_event_registered = False
        self._damaged_sfx_id = None
        self.reaper_curse_sfx_id = None
        self.showing_reaper_curse_end_sfx = False
        self.reaper_curse_sfx_socket_name = 'xuetiao'
        self.reaper_curse_sfx_bias = 0
        return

    def on_init_complete(self):
        self.refresh_skin_relevant_appearance()
        if self.unit_obj.MASK & preregistered_tags.MECHA_TAG_VALUE:
            self._register_mecha_effect_event(True)

    def _register_mecha_effect_event(self, flag):
        if self.mecha_effect_event_registered ^ flag:
            func = self.regist_event if flag else self.unregist_event
            func('E_ON_DIE', self.on_die)
            func('E_SHOW_EMP_EFFECT', self._on_show_emp_effect)
            self.mecha_effect_event_registered = flag

    def destroy_event(self):
        super(ComMechaEffectCommon, self).destroy_event()
        self._register_mecha_effect_event(False)
        self._register_highlight_effect_event(False)

    def destroy(self):
        super(ComMechaEffectCommon, self).destroy()
        self._register_mecha_effect_event(False)
        self._register_highlight_effect_event(False)
        self.clear_model_sfxs()
        self.clear_water_effects()
        self.clear_waves()
        self.on_ground_sfx_path_map = None
        return

    def on_model_loaded(self, model):
        if self.ev_g_fire_debuff():
            self.on_fire_effect(True)

    def enable_sfx_sync(self, enable):
        self._sync_sfx = enable

    def on_show_cd_effect(self, cd_effect):
        cur_time = time.time()
        if cur_time - self._last_cast_time < 0.5:
            return
        model = self.ev_g_model()
        for effect in cd_effect:
            if model:
                model.set_socket_bound_obj_active(effect[0], effect[1], True)

        self._last_cast_time = cur_time
        self._sync_sfx and self.unit_obj.ev_g_call_sync_method('bcast_evt', [bcast.E_SHOW_CD_EFFECT, (cd_effect,)], True)

    def _on_pos_changed(self, pos):
        model = self.ev_g_model()
        if not model or not self._onground_sfx_info:
            if G_POS_CHANGE_MGR:
                self.unregist_pos_change(self._on_pos_changed)
            else:
                self.unregist_event('E_POSITION', self._on_pos_changed)
            return
        else:
            try:
                dest_pos, sfx_type = self._onground_sfx_info
                diff_y = abs(pos.y - dest_pos.y)
                if diff_y <= 2:
                    global_data.sfx_mgr.create_sfx_in_scene(self.on_ground_sfx_path_map[sfx_type], dest_pos, duration=1.2, int_check_type=CREATE_SRC_SIMPLE)
                    if G_POS_CHANGE_MGR:
                        self.unregist_pos_change(self._on_pos_changed)
                    else:
                        self.unregist_event('E_POSITION', self._on_pos_changed)
                    self._onground_sfx_info = None
            except:
                pass

            return

    def on_show_onground_sfx(self, sfx_type='middle', pos=None):
        if not self.on_ground_sfx_path_map:
            return
        else:
            sfx_path = self.on_ground_sfx_path_map.get(sfx_type, None)
            if not sfx_path:
                return
            if pos:
                model_pos = self.ev_g_position()
                if not model_pos:
                    return
                pos = math3d.vector(*pos)
                diff_y = abs(pos.y - model_pos.y)
                if diff_y <= 2:
                    global_data.sfx_mgr.create_sfx_in_scene(self.on_ground_sfx_path_map[sfx_type], pos, duration=1.2, int_check_type=CREATE_SRC_SIMPLE)
                else:
                    if not self._onground_sfx_info:
                        if G_POS_CHANGE_MGR:
                            self.regist_pos_change(self._on_pos_changed, 0.1)
                        else:
                            self.regist_event('E_POSITION', self._on_pos_changed)
                    self._onground_sfx_info = (
                     pos, sfx_type)
            else:
                pos = self.ev_g_position()
                if not pos:
                    return
            up = math3d.vector(0, 1, 0)
            start_pos = pos + up
            end_pos = pos - up * 2000
            from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE
            result = self.scene.scene_col.hit_by_ray(start_pos, end_pos, 0, -1, GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER)
            if result and result[0]:
                global_data.sfx_mgr.create_sfx_in_scene(self.on_ground_sfx_path_map[sfx_type], result[1], duration=1.2, int_check_type=CREATE_SRC_SIMPLE)
                self._sync_sfx and self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_ONGROUND_SFX, (sfx_type, (result[1].x, result[1].y, result[1].z))], True)
            return

    def on_show_skill_hit_sfx(self, sfx_path, pos, rot=None):
        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, math3d.vector(*pos), duration=0.5, int_check_type=CREATE_SRC_SIMPLE)
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_SKILL_HIT_SFX, (sfx_path, pos)], True)

    def create_water_ripple_effect(self):
        if self._water_ripple_sfx_id:
            return
        pos = self.ev_g_position()
        water_pos = math3d.vector(pos.x, self._cur_water_height, pos.z)
        self._water_ripple_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(WATER_RIPPLE_SFX, water_pos, duration=-1, int_check_type=CREATE_SRC_SIMPLE)

    def clear_water_ripple_effect(self):
        if self._water_ripple_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._water_ripple_sfx_id)
            self._water_ripple_sfx_id = None
        return

    def create_water_effects(self):
        self.create_water_ripple_effect()
        if self._water_move_sfx:
            return
        pos = self.ev_g_position()
        water_pos = math3d.vector(pos.x, self._cur_water_height, pos.z)

        def create_cb(sfx):
            sfx.visible = False
            self._water_move_sfx = sfx

        global_data.sfx_mgr.create_sfx_in_scene(WATER_MOVE_SFX, water_pos, duration=-1, on_create_func=create_cb)
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self.update_sfx_pos, 0.1)
        else:
            self.regist_event('E_POSITION', self.update_sfx_pos)

    def clear_water_effects(self):
        self.clear_water_ripple_effect()
        if self._water_move_sfx:
            global_data.sfx_mgr.remove_sfx(self._water_move_sfx)
            self._water_move_sfx = None
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self.update_sfx_pos)
        else:
            self.unregist_event('E_POSITION', self.update_sfx_pos)
        self._last_pos = None
        return

    def update_sfx_pos(self, pos):
        if not self._last_pos:
            self._last_pos = pos
            return
        if (pos - self._last_pos).is_zero:
            return
        forward = pos - self._last_pos
        forward.normalize()
        self._last_pos = pos
        self.clear_water_ripple_effect()
        water_pos = math3d.vector(pos.x, self._cur_water_height, pos.z)
        if self._water_move_sfx:
            self._water_move_sfx.visible = True
            self._water_move_sfx.position = water_pos
            self._water_move_sfx.rotation_matrix = math3d.matrix.make_rotation_y(forward.yaw)
        if self._stop_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._stop_timer_id)

        def switch_sfx():
            if not self.is_valid():
                return
            if self._cur_water_status == water_const.WATER_NONE or self.ev_g_is_diving():
                return
            self.create_water_ripple_effect()
            if self._water_move_sfx:
                self._water_move_sfx.visible = False

        self._stop_timer_id = global_data.game_mgr.register_logic_timer(switch_sfx, interval=0.2, times=1, mode=CLOCK)

    def on_water_event(self, water_status, water_height):
        self._last_water_height = self._cur_water_height
        self._cur_water_height = water_height or 0
        if self.ev_g_is_avatar() or self.sd.ref_is_agent:
            self.check_enter_watert_effect(water_status)
        self._cur_water_status = water_status
        if water_status == water_const.WATER_NONE:
            self.clear_water_effects()
        elif not self.ev_g_is_diving():
            self.create_water_effects()

    def clear_waves(self):
        if self._wave_generate_timer:
            global_data.game_mgr.unregister_logic_timer(self._wave_generate_timer)
            self._wave_generate_timer = None
        return

    def on_insert_waves(self, pos=None):
        if not self or not self.is_valid():
            return RELEASE
        if not pos:
            pos = self.ev_g_position()
        else:
            pos = math3d.vector(*pos)
        scale = 2

        def create_cb(sfx):
            sfx.scale = math3d.vector(scale, scale, scale)

        sfx_path = 'effect/fx/robot/common/water_mecha_qipao2.sfx'
        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, math3d.vector(pos.x, pos.y, pos.z), on_create_func=create_cb, int_check_type=CREATE_SRC_SIMPLE)
        self._sync_sfx and self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CREATE_SCENE_EFFECT, (sfx_path, (pos.x, pos.y, pos.z), 0)], True)

    def check_enter_watert_effect(self, water_status):
        if not self.ev_g_is_in_any_state([mecha_status_config.MC_MOVE, mecha_status_config.MC_RUN]):
            pos = self.ev_g_position()
            if water_status == water_const.WATER_NONE and self._cur_water_status != water_const.WATER_NONE:
                self.on_create_scene_effect(EXIT_WATER_SFX, [pos.x, self._last_water_height, pos.z], 3)
            elif water_status != water_const.WATER_NONE and self._cur_water_status == water_const.WATER_NONE:
                self.on_create_scene_effect(ENTER_WATER_SFX, [pos.x, self._cur_water_height, pos.z], 3)
                self.clear_waves()
                height = self._cur_water_height - pos.y
                lerp_times = int(height / NEOX_UNIT_SCALE)
                for i in range(lerp_times):
                    self.on_insert_waves((pos.x, pos.y + NEOX_UNIT_SCALE * (lerp_times - i), pos.z))

                self.on_insert_waves()
                self._wave_generate_timer = global_data.game_mgr.register_logic_timer(self.on_insert_waves, interval=0.03, times=4.0, mode=CLOCK)

    def _on_show_light_effect(self, show):
        water_info = self.ev_g_mecha_config('WaterEffectConfig')
        if not water_info:
            return
        if show:
            self.on_create_model_effects(**water_info['light'])
        else:
            self.on_remove_model_effects(**water_info['light'])

    def _on_selection_model_binding(self):
        if self.sd.ref_is_ball_mode:
            self._on_show_light_effect(False)

    def on_enter_diving(self):
        water_info = self.ev_g_mecha_config('WaterEffectConfig')
        if not self.sd.ref_is_ball_mode:
            self.on_create_model_effects(**water_info['light'])
        'bubble' in water_info and self.on_create_model_effects(**water_info['bubble'])
        self.clear_water_effects()

    def on_leave_diving(self):
        water_info = self.ev_g_mecha_config('WaterEffectConfig')
        self.on_remove_model_effects(**water_info['light'])
        'bubble' in water_info and self.on_remove_model_effects(**water_info['bubble'])
        if self._cur_water_status != water_const.WATER_NONE:
            self.create_water_effects()

    def on_oil_effect(self, show):
        if show:
            if self.hit_sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(self.hit_sfx_id)
            self.on_create_model_effects(**OIL_EFFECT)
        else:
            self.on_remove_model_effects(**OIL_EFFECT)

    def on_fire_effect(self, show, big_fire=False):
        if show:
            self.on_create_model_effects(**FIRE_EFFECT_BIG)
            if big_fire and self.unit_obj.MASK & preregistered_tags.MECHA_TAG_VALUE:
                self.on_create_model_effects(**FIRE_EFFECT_SMALL)
        else:
            self.on_remove_model_effects(**FIRE_EFFECT_BIG)
            self.on_remove_model_effects(**FIRE_EFFECT_SMALL)

    def _on_show_highlight(self, hit_parts, sfx_path=None, ignore_shield=False):
        if self._block_sfx:
            return
        else:
            model = self.ev_g_model()
            if not model or not model.valid:
                return
            if self._is_frozen:
                return
            if not ignore_shield:
                shield = self.ev_g_shield()
                if shield is not None and shield > 0:
                    return
            if sfx_path is not None:
                if self.hit_sfx_id:
                    global_data.sfx_mgr.remove_sfx_by_id(self.hit_sfx_id)
                    self.hit_sfx_id = None
                self.hit_sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, 'fx_buff', on_remove_func=self.clear_hit_sfx)
                self.is_normal_hit = False
                return
            if self.hit_sfx_id:
                if self.is_normal_hit:
                    sfx = global_data.sfx_mgr.get_sfx_by_id(self.hit_sfx_id)
                    if sfx and sfx.valid:
                        return
                    self.clear_hit_sfx()
                else:
                    return
            self.hit_sfx_id = global_data.sfx_mgr.create_sfx_on_model(HIGHLIGHT_EFFECT, model, 'fx_buff', on_remove_func=self.clear_hit_sfx)
            self.is_normal_hit = True
            return

    def clear_hit_sfx(self, *args):
        if self.hit_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.hit_sfx_id)
            self.hit_sfx_id = None
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        else:
            global_data.sfx_mgr.create_sfx_on_model(CLEAR_HIGHLIGHT_EFFECT, model, 'fx_buff')
            return

    def _on_show_emp_effect(self, flag):
        if flag:
            self.on_create_model_effects(**EMP_EFFECT)
        else:
            self.on_remove_model_effects(**EMP_EFFECT)

    def on_create_model_effects(self, **info):
        if self._block_sfx:
            return
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        for sfx_path, sockets in six.iteritems(info):
            for socket_name in sockets:
                sfx_id_key = sfx_path + socket_name
                if sfx_id_key in self._model_sfx_ids:
                    global_data.sfx_mgr.remove_sfx_by_id(self._model_sfx_ids[sfx_id_key])
                self._model_sfx_ids[sfx_id_key] = global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket_name)

    def on_remove_model_effects(self, **info):
        for sfx_path, sockets in six.iteritems(info):
            for socket_name in sockets:
                sfx_id_key = sfx_path + socket_name
                if sfx_id_key in self._model_sfx_ids:
                    global_data.sfx_mgr.remove_sfx_by_id(self._model_sfx_ids[sfx_id_key])
                    del self._model_sfx_ids[sfx_id_key]

    def clear_model_sfxs(self):
        for sfx_id in six.itervalues(self._model_sfx_ids):
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self._model_sfx_ids = {}
        global_data.sfx_mgr.remove_sfx_by_id(self.hit_sfx_id)

    def on_create_scene_effect(self, sfx, pos, duration):
        global_data.sfx_mgr.create_sfx_in_scene(sfx, math3d.vector(*pos), duration=duration)
        self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CREATE_SCENE_EFFECT, (sfx, pos, duration)], True)
        self._sync_sfx and self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CREATE_SCENE_EFFECT, (sfx, pos, duration)], True)

    def on_frozen(self, flag, *args, **kwargs):
        self._is_frozen = flag

    def on_be_executed(self, executer):
        self._on_show_emp_effect(False)
        self._register_mecha_effect_event(False)

    def on_die(self):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        for sfx_path, sockets in six.iteritems(DIE_EFFECT):
            for socket in sockets:
                global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket)

    def on_block_effect_sfx(self, block):
        self._block_sfx = block
        if block:
            self.clear_model_sfxs()

    def _register_highlight_effect_event(self, flag):
        if self.highlight_event_registered ^ flag:
            func = self.regist_event if flag else self.unregist_event
            func('E_SHOW_PART_HIGHLIGHT', self._on_show_highlight)
            self.highlight_event_registered = flag

    def refresh_skin_relevant_appearance(self, *args):
        skin_id = self.ev_g_mecha_fashion_id()
        self._register_highlight_effect_event(skin_id not in IGNORE_HIGHLIGHT_SKIN_ID_SET)
        self.on_ground_sfx_path_map = ON_GROUND_SFX.get(skin_id, ON_GROUND_SFX['common'])

    def _set_damaged_effect_visible(self, is_visible):
        if self._damaged_sfx_id is None:
            return
        else:
            sfx = global_data.sfx_mgr.get_sfx_by_id(self._damaged_sfx_id)
            if sfx and sfx.valid:
                sfx.visible = is_visible
            return

    def on_hp_changed(self, *args):
        self.check_in_damaged()

    def on_max_hp_changed(self, *args):
        self.check_in_damaged()

    def check_in_damaged(self):
        percent = self.ev_g_health_percent() * 100
        if percent <= MECHA_DAMAGED_HP_RATE:
            self.show_damaged_effect()
        else:
            self.delete_damaged_effect()

    def show_damaged_effect(self):
        model = self.ev_g_model()
        if self._damaged_sfx_id is None and model:
            if self._sync_sfx:
                create_cb = None
            else:

                def create_sfx_cb(sfx):
                    sfx.visible = False

                create_cb = create_sfx_cb
            self._damaged_sfx_id = global_data.sfx_mgr.create_sfx_on_model('effect/fx/robot/common/mecha_sunhuai.sfx', model, 'part_point1', type=world.BIND_TYPE_ALL, on_create_func=create_cb)
        return

    def delete_damaged_effect(self):
        if self._damaged_sfx_id is not None:
            global_data.sfx_mgr.remove_sfx_by_id(self._damaged_sfx_id)
            self._damaged_sfx_id = None
        return

    def _remove_reaper_curse_effect(self):
        if self.reaper_curse_sfx_id:
            global_data.sfx_mgr.shutdown_sfx_by_id(self.reaper_curse_sfx_id)
            self.reaper_curse_sfx_id = None
        return

    def on_create_reaper_curse_effect_callback(self, sfx):
        sfx.position = math3d.vector(0, self.reaper_curse_sfx_bias, 0)

    def on_create_reaper_curse_effect(self, creator_mecha_fashion):
        if not creator_mecha_fashion:
            return
        skin_id = creator_mecha_fashion[FASHION_POS_SUIT]
        mecha_id = int(str(skin_id)[3:7])
        skin_id, shiny_weapon_id = get_accurate_mecha_skin_info_from_fasion_data(mecha_id, creator_mecha_fashion)
        key = (skin_id, shiny_weapon_id)
        if key in REAPER_CURSE_SFX_PATH_MAP:
            sfx_path = REAPER_CURSE_SFX_PATH_MAP[key]
        else:
            sfx_path = get_specific_mecha_skin_res_readonly_res_path(8031, skin_id, shiny_weapon_id, REAPER_CURSE_EFFECT_ID)
            REAPER_CURSE_SFX_PATH_MAP[key] = sfx_path
        model = self.ev_g_model()
        if model:
            self._remove_reaper_curse_effect()
            self.reaper_curse_sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, self.reaper_curse_sfx_socket_name, type=world.BIND_TYPE_TRANSLATE, on_create_func=self.on_create_reaper_curse_effect_callback)
            self.showing_reaper_curse_end_sfx = False

    def on_remove_reaper_curse_effect(self, creator_mecha_fashion):
        if not self.showing_reaper_curse_end_sfx:
            self._remove_reaper_curse_effect()
        if creator_mecha_fashion is not None:
            skin_id, shiny_weapon_id = get_accurate_mecha_skin_info_from_fasion_data(8031, creator_mecha_fashion)
            key = (skin_id, shiny_weapon_id)
            if key in REAPER_CURSE_END_SFX_PATH_MAP:
                sfx_path = REAPER_CURSE_END_SFX_PATH_MAP[key]
            else:
                sfx_path = get_specific_mecha_skin_res_readonly_res_path(8031, skin_id, shiny_weapon_id, REAPER_CURSE_END_EFFECT_ID)
                REAPER_CURSE_END_SFX_PATH_MAP[key] = sfx_path
            model = self.ev_g_model()
            if model:
                self.reaper_curse_sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, self.reaper_curse_sfx_socket_name, type=world.BIND_TYPE_TRANSLATE, on_create_func=self.on_create_reaper_curse_effect_callback)
                self.showing_reaper_curse_end_sfx = True
        return

    def on_pve_bless_effect(self, bless_id):
        model = self.ev_g_model()
        if not model or not model.valid:
            return
        if bless_id not in PVE_BLESS_EFFECT:
            return
        sfx_info = PVE_BLESS_EFFECT[bless_id]
        for sfx_path, socket_list in six.iteritems(sfx_info):
            for socket in socket_list:
                global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket, type=world.BIND_TYPE_TRANSLATE)

    def switch_ball_state(self, socket, bias, *args):
        self.reaper_curse_sfx_socket_name = socket
        self.reaper_curse_sfx_bias = bias
        if self.reaper_curse_sfx_id:
            sfx = global_data.sfx_mgr.get_sfx_by_id(self.reaper_curse_sfx_id)
            if sfx:
                sfx.remove_from_parent()
                mecha_model = self.ev_g_model()
                if mecha_model:
                    mecha_model.bind(self.reaper_curse_sfx_socket_name, sfx, world.BIND_TYPE_TRANSLATE)
                    sfx.position = math3d.vector(0, bias, 0)
                    sfx.visible = self._sync_sfx
            else:
                self.reaper_curse_sfx_id = None
        return

    def on_switch_model(self, model):
        old_model = self.ev_g_mecha_original_model() if self.sd.ref_using_second_model else self.ev_g_mecha_second_model()
        new_key_values = {}
        for sfx_id_key, sfx_id in six.iteritems(self._model_sfx_ids):
            index = sfx_id_key.find('.sfx')
            if index == -1:
                continue
            socket_name = sfx_id_key[index + 4:]
            sfx = global_data.sfx_mgr.get_sfx_by_id(sfx_id)
            if sfx:
                sfx.remove_from_parent()
                model.bind(socket_name, sfx)
                sfx.visible = True
            else:
                global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
                new_key_values[sfx_id_key] = global_data.sfx_mgr.create_sfx_on_model(sfx_id_key[:index + 4], model, socket_name)

        new_key_values and self._model_sfx_ids.update(new_key_values)
        if self._damaged_sfx_id:
            sfx = global_data.sfx_mgr.get_sfx_by_id(self._damaged_sfx_id)
            if sfx:
                sfx.remove_from_parent()
                model.bind('part_point1', sfx, world.BIND_TYPE_ALL)
                sfx.visible = self._sync_sfx
            else:
                self.delete_damaged_effect()
                self.show_damaged_effect()
        if self.reaper_curse_sfx_id:
            sfx = global_data.sfx_mgr.get_sfx_by_id(self.reaper_curse_sfx_id)
            if sfx:
                sfx.remove_from_parent()
                model.bind(self.reaper_curse_sfx_socket_name, sfx, world.BIND_TYPE_ALL)
                sfx.visible = self._sync_sfx
            else:
                self.reaper_curse_sfx_id = None
        return