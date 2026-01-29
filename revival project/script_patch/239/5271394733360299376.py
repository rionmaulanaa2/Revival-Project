# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8016.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
from common.utils import timer
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
import logic.gcommon.common_utils.bcast_utils as bcast
import collision
from mobile.common.EntityManager import EntityManager
from logic.gcommon.cdata.mecha_status_config import *
VICE_MODEL_EFFECT = ('99', '91')
VICE_GUIDE_EFFECT = ('98', '92')
VICE_END_EFFECT = ('97', '90')
VICE_WAVE_EFFECT = '96'
VICE_HIT_BLOCK_EFFECT = ('95', '89')
VICE_HIT_TARGET_EFFECT = '94'
MAIN_IDLE_EFFECT = '93'
SMOG_EFFECT = ('effect/fx/mecha/8016/8016_jump_yan.sfx', 'effect/fx/mecha/8016/8016_kaihuo_qikuosan.sfx')
NEED_WING_UPDATE = ('201801661', '201801662', '201801663')
NEED_WING_SFX_STATE = (MC_RUN, MC_SECOND_WEAPON_ATTACK, MC_JUMP_1, MC_JUMP_2, MC_JUMP_3, MC_FLIGHT_BOOST, MC_SUPER_JUMP)

class ComMechaEffect8016(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_MODEL_LOADED': 'on_model_loaded',
       'E_CREATE_VICE_EFFECT': 'on_create_sfxs',
       'E_CLEAR_VICE_EFFECT': 'on_clear_sfx',
       'G_UPDATE_VICE_EFFECT': 'on_update_sfxs',
       'E_CREATE_VICE_END_EFFECT': 'on_create_end_sfx',
       'E_SYNC_CREATE_VICE_EFFECT': 'on_sync_create_sfxs',
       'E_SYNC_UPDATE_VICE_EFFECT': 'on_sync_update_sfxs',
       'E_SYNC_UPDATE_VICE_HIT': 'on_sync_update_hit',
       'E_CREATE_SMOG_EFFECT': 'on_create_smog_effect',
       'E_SHOW_MAIN_ACC_IDLE_EFFECT': 'on_show_main_acc_idle_effect',
       'E_MECHA_LOD_LOADED_FIRST': ('on_load_lod_complete', 10),
       'E_HEALTH_HP_EMPTY': 'on_clear_sfx',
       'E_DEATH': 'on_clear_sfx',
       'E_ENTER_STATE': 'update_wing_sfx',
       'E_LEAVE_STATE': 'update_wing_sfx',
       'E_8016_UPDATE_WING_SFX': '_update_wing_sfx'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8016, self).init_from_dict(unit_obj, bdict)
        self.fire_sfx = None
        self.fire_mod = None
        self.fire_wave = None
        self.fire_sfx_scale = 0
        self.fire_sfx_pos = None
        self.fire_sfx_end = None
        self.fire_sfx_rot = None
        self.main_idle_effect = None
        self.fire_sfx_arrived = False
        self.cur_fire_sfx_scale = 0
        self.target_start_pos = None
        self.target_end_pos = None
        self.update_timer_id = None
        self.atk_radius = 1.0
        self._need_update_wing_sfx = self._shiny_weapon_id in NEED_WING_UPDATE
        if not self._need_update_wing_sfx:
            self._enable_bind_event(False, ['E_ENTER_STATE', 'E_LEAVE_STATE'])
        return

    def destroy(self):
        super(ComMechaEffect8016, self).destroy()
        self.on_clear_sfx()
        if self.main_idle_effect:
            global_data.sfx_mgr.remove_sfx_by_id(self.main_idle_effect)
        self.main_idle_effect = None
        return

    def is_teammate(self):
        return self.ev_g_is_campmate(global_data.player.logic.ev_g_camp_id()) or global_data.cam_lctarget == self.unit_obj

    def on_model_loaded(self, model):
        super(ComMechaEffect8016, self).on_model_loaded(model)

    def on_load_lod_complete(self):
        model = self.ev_g_model()

        def on_create_func(sfx):
            sfx.remove_from_parent()
            model.bind('fx_vice_huandan', sfx)
            sfx.visible = self.ev_g_is_main_acc_mode()

        self.main_idle_effect = self.trigger_hold_effect(MAIN_IDLE_EFFECT, on_create_func)

    def on_sync_create_sfxs(self, atk_radius):
        self.on_create_sfxs(atk_radius)
        global_data.game_mgr.delay_exec(4, self.on_clear_sfx)

    def on_create_sfxs(self, atk_radius, sync=False):
        self.atk_radius = atk_radius
        self.fire_sfx_arrived = False
        self.cur_fire_sfx_scale = 0
        self.fire_sfx = self.trigger_hold_effect(VICE_GUIDE_EFFECT)
        self.fire_mod = self.trigger_hold_effect(VICE_MODEL_EFFECT)
        self.fire_wave = self.trigger_hold_effect(VICE_WAVE_EFFECT)
        if sync:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SYNC_CREATE_VICE_EFFECT, (atk_radius,)], True)

    def on_sync_update_hit(self, hit_target_list, sync=True):
        if self.fire_sfx_pos is None:
            return
        else:
            for eid, _ in hit_target_list:
                target = EntityManager.getentity(eid)
                if target and target.logic:
                    model = target.logic.ev_g_model()
                    if model:
                        bounding = model.bounding_box * model.scale
                        r = bounding.x if bounding.x < 3 * NEOX_UNIT_SCALE else 3 * NEOX_UNIT_SCALE
                        size = math3d.vector(r, r, r)
                        magic_code = 22601
                        col_test = collision.col_object(collision.SPHERE, size, magic_code, magic_code)
                        global_data.game_mgr.scene.scene_col.add_object(col_test)
                        col_test.position = target.logic.ev_g_position() + math3d.vector(0, size.y, 0)
                        ret = global_data.game_mgr.scene.scene_col.hit_by_ray(self.fire_sfx_pos, self.fire_sfx_end, 0, magic_code, magic_code, collision.EQUAL_FILTER)
                        if ret and ret[0]:
                            offset = ret[1] - col_test.position
                            sfx_pos = col_test.position + offset * 0.5
                            global_data.sfx_mgr.create_sfx_in_scene('effect/fx/mecha/8016/8016_vice_hit.sfx', pos=sfx_pos, duration=0.1)
                        global_data.game_mgr.scene.scene_col.remove_object(col_test)
                        col_test = None

            if sync:
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SYNC_UPDATE_VICE_HIT, (hit_target_list,)], True)
            return

    def on_sync_update_sfxs(self, start_pos, end_pos):
        if not self.fire_sfx:
            self.on_create_sfxs(self.atk_radius)
            return
        else:
            SYNC_INTERVAL = self.sd.ref_vice_sync_interval
            start_pos = math3d.vector(*start_pos)
            end_pos = math3d.vector(*end_pos)
            if self.target_end_pos is None or self.target_start_pos is None:
                self.on_update_sfxs(0, start_pos, end_pos)
            else:

                def update_sfxs(dt):
                    self.sync_cnt += dt
                    start = math3d.vector(0, 0, 0)
                    end = math3d.vector(0, 0, 0)
                    coe = self.sync_cnt / SYNC_INTERVAL
                    start.intrp(self.fire_sfx_pos, self.target_start_pos, coe)
                    end.intrp(self.fire_sfx_end, self.target_end_pos, coe)
                    self.on_update_sfxs(dt, start_pos, end_pos)
                    if coe >= 1:
                        return timer.RELEASE

                if self.update_timer_id:
                    global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
                self.update_timer_id = global_data.game_mgr.register_logic_timer(update_sfxs, 1, timedelta=True)
            self.sync_cnt = 0
            self.target_start_pos = start_pos
            self.target_end_pos = end_pos
            return

    def on_update_sfxs(self, dt, start_pos, end_pos, sync=False):
        forward = end_pos - start_pos
        dist = forward.length
        forward.normalize()
        self.cur_fire_sfx_scale += self.sd.ref_vice_fire_scale_speed * dt
        if self.cur_fire_sfx_scale >= dist:
            self.cur_fire_sfx_scale = dist
            self.switch_sfx()
        end_pos = start_pos + forward * self.cur_fire_sfx_scale
        sfx = global_data.sfx_mgr.get_sfx_by_id(self.fire_sfx)
        if sfx:
            sfx.position = start_pos
            sfx.end_pos = end_pos
        right = math3d.vector(0, 1, 0).cross(forward)
        up = forward.cross(right)
        rotation_matrix = math3d.matrix.make_orient(forward, up)
        self.fire_sfx_pos = start_pos
        self.fire_sfx_end = end_pos
        self.fire_sfx_rot = rotation_matrix
        mod = global_data.sfx_mgr.get_sfx_by_id(self.fire_mod)
        if mod:
            mod.position = start_pos
            mod.rotation_matrix = rotation_matrix
            self.fire_sfx_scale = (end_pos - start_pos).length / (10 * NEOX_UNIT_SCALE)
            mod.scale = math3d.vector(self.fire_sfx_scale, self.atk_radius, self.atk_radius)
        wave = global_data.sfx_mgr.get_sfx_by_id(self.fire_wave)
        if wave:
            wave.position = end_pos
            wave.rotation_matrix = rotation_matrix
        if sync:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SYNC_UPDATE_VICE_EFFECT,
             (
              (
               start_pos.x, start_pos.y, start_pos.z),
              (
               end_pos.x, end_pos.y, end_pos.z))], True)
        return end_pos

    def on_create_end_sfx(self, sync=False, force=False):
        if not self.fire_sfx and not force:
            return
        self.on_clear_sfx()
        if not self.fire_sfx_pos:
            return

        def on_create_func(sfx):
            sfx.position = self.fire_sfx_pos
            sfx.rotation_matrix = self.fire_sfx_rot
            sfx.scale = math3d.vector(self.fire_sfx_scale, self.atk_radius, self.atk_radius)

        self.trigger_hold_effect(VICE_END_EFFECT, on_create_func, duration=0.8)
        if sync:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CREATE_VICE_END_EFFECT, ()], True)

    def switch_sfx(self):
        if self.fire_sfx_arrived:
            return
        if self.fire_wave:
            global_data.sfx_mgr.remove_sfx_by_id(self.fire_wave)
        self.fire_wave = self.trigger_hold_effect(VICE_HIT_BLOCK_EFFECT)
        self.fire_sfx_arrived = True

    def on_clear_sfx(self):
        if self.fire_sfx:
            global_data.sfx_mgr.remove_sfx_by_id(self.fire_sfx)
        self.fire_sfx = None
        if self.fire_mod:
            global_data.sfx_mgr.remove_sfx_by_id(self.fire_mod)
        self.fire_mod = None
        if self.fire_wave:
            global_data.sfx_mgr.remove_sfx_by_id(self.fire_wave)
        self.fire_wave = None
        if self.update_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
            self.update_timer_id = None
        return

    def on_create_smog_effect(self, idx, sync=False):
        model = self.ev_g_model()
        if model:
            global_data.sfx_mgr.create_sfx_on_model(SMOG_EFFECT[idx], model, 'fx_root', duration=1.5)
        if sync:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_CREATE_SMOG_EFFECT, (idx,)], True)

    def on_show_main_acc_idle_effect(self, show, sync=False):
        sfx = global_data.sfx_mgr.get_sfx_by_id(self.main_idle_effect)
        if sfx:
            sfx.visible = show
        if sync:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_MAIN_ACC_IDLE_EFFECT, (show,)], True)

    def trigger_hold_effect(self, effect_id, *args, **kwargs):
        if type(effect_id) in (list, tuple):
            my_effect, enemy_effect = effect_id
            effect_id = my_effect if self.is_teammate() else enemy_effect
        ret = self.on_trigger_hold_effect(effect_id, *args, **kwargs)
        if ret:
            return ret[0]

    def update_wing_sfx(self, *args):
        if not self._need_update_wing_sfx:
            return
        cur_state = self.ev_g_get_all_state()
        show_wing_sfx = False
        for state in cur_state:
            if state in NEED_WING_SFX_STATE:
                show_wing_sfx = True
                break

        self._update_wing_sfx(show_wing_sfx)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_8016_UPDATE_WING_SFX, (show_wing_sfx,)], True)

    def _update_wing_sfx(self, show_wing_sfx):
        self.sd.ref_socket_res_agent.set_sfx_res_visible(not show_wing_sfx, 's_wings')
        self.sd.ref_socket_res_agent.set_sfx_res_visible(show_wing_sfx, 'wings')