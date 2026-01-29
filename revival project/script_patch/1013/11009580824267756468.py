# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8005.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
import logic.gcommon.const as g_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.timer import LOGIC, CLOCK
import world
import math3d
import game3d
import render
from logic.gutils.mecha_skin_utils import is_ss_level_skin
_HASH_Rim_intensity = game3d.calc_string_hash('Rim_intensity')
_HASH_AlphaFix = game3d.calc_string_hash('AlphaFix')
TRACK_END_MODEL_EFFECT_ID = '16'
FEET_SFX_KEY = 'feet'

class ComMechaEffect8005(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_MODEL_LOADED': 'on_model_loaded',
       'E_SHOW_WP_TRACK': 'show_weapon_track',
       'E_STOP_WP_TRACK': 'stop_weapon_track',
       'E_SET_TRACK_DATA': 'set_show_track_data',
       'E_DEATH': '_on_died',
       'E_MOD_RADIUS_FACTOR': 'mod_radius_factor',
       'E_RELOADING': 'on_reloading_bullet',
       'E_SHAPESHIFT': 'on_change_shape',
       'E_ON_SKIN_SUB_MODEL_LOADED': 'on_skin_sub_model_loaded'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8005, self).init_from_dict(unit_obj, bdict)
        self.track_enable = False
        self.track_target_model = None
        self.track_positions = []
        self.outline_enable = False
        self.outline_targets = set()
        self.outline_timer = None
        self.show_track_data = {}
        self.radius = 1
        self.radius_factor = 1
        self.temp_stop = False
        self.cur_mode = bdict.get('shoot_mode', 0)
        self.weapon_pos = g_const.PART_WEAPON_POS_MAIN1
        self.sync_yaw_timer = None
        self._hide_track_timer_id = None
        self.mecha_death = False
        self.sub_model_visible_timer = None
        return

    def destroy(self):
        self.stop_weapon_track()
        if self.sub_model_visible_timer:
            global_data.game_mgr.unregister_logic_timer(self.sub_model_visible_timer)
            self.sub_model_visible_timer = None
        super(ComMechaEffect8005, self).destroy()
        return

    def on_model_loaded(self, model):
        super(ComMechaEffect8005, self).on_model_loaded(model)
        if self.track_enable:
            self.show_weapon_track()

    def get_track_start_pos(self):
        partcamera = self.scene.get_com('PartCamera')
        if partcamera and partcamera.cam:
            return partcamera.cam.world_position
        else:
            return None

    def start_sync_yaw(self):
        if self.sync_yaw_timer is None:
            self.sync_yaw_timer = global_data.game_mgr.register_logic_timer(self.sync_yaw_tick, interval=1)
        return

    def sync_yaw_tick(self):
        position = self.get_track_start_pos()
        if position and self.track_enable:
            self.send_event('E_UPDATE_PARABOLA_TRACK', position)

    def stop_sync_yaw(self):
        if self.sync_yaw_timer:
            global_data.game_mgr.unregister_logic_timer(self.sync_yaw_timer)
            self.sync_yaw_timer = None
        return

    def track_callback(self, visible, start_pos, end_pos):
        if self.track_target_model:
            self.set_traget_model_var(start_pos, end_pos, visible)
        else:
            self.send_event('E_HIDE_PARABOLA_TRACK', True)
        self.track_positions = [
         start_pos, end_pos, visible]

    def set_traget_model_var(self, start_pos, end_pos, visible):
        distance = (end_pos - start_pos).length
        if distance > 50 * NEOX_UNIT_SCALE:
            rate = 1.0
        else:
            rate = distance / (50 * NEOX_UNIT_SCALE)
        Rim_intensity = rate * 5.0
        AlphaFix = rate * 2.0
        self.track_target_model.all_materials.set_var(_HASH_Rim_intensity, 'Rim_intensity', Rim_intensity)
        self.track_target_model.all_materials.set_var(_HASH_AlphaFix, 'AlphaFix', AlphaFix)
        self.track_target_model.position = end_pos
        show_radius = self.radius - 2.0 * NEOX_UNIT_SCALE
        if show_radius <= 1e-06:
            show_radius = 1e-06
        scale = show_radius / self.track_target_model.bounding_box.x
        self.track_target_model.scale = math3d.vector(scale, scale, scale)
        self.track_target_model.visible = visible

    def end_model_callback(self, model, *args):
        if not model or not model.valid:
            return
        if not self.track_enable:
            model.destroy()
            return
        world.get_active_scene().add_object(model)
        if global_data.game_mgr.gds.get_actual_quality() < 1:
            model.all_materials.set_macro('DEPTH_OUTLINE', 'FALSE')
            model.all_materials.rebuild_tech()
        else:
            model.set_rendergroup_and_priority(world.RENDER_GROUP_DECAL, 0)
        if self.track_target_model:
            self.track_target_model.destroy()
        self.track_target_model = model
        if self.track_positions:
            self.set_traget_model_var(self.track_positions[0], self.track_positions[1], self.track_positions[2])
        self.start_sync_yaw()

    def show_track(self):
        weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
        if not weapon:
            return
        else:
            from common.cfg import confmgr
            conf = confmgr.get('grenade_config', str(weapon.iType))
            speed = conf['fSpeed']
            g = -confmgr.get('grenade_config', str(weapon.iType), 'fGravity', default=98)
            up_angle = confmgr.get('grenade_config', str(weapon.iType), 'fUpAngle', default=0)
            mass = conf.get('fMass', 1.0)
            linear_damp = conf.get('fLinearDamp', 0.0)
            position = self.get_track_start_pos()
            end_sfx = None
            if position:
                is_line_visible = self.show_track_data.get('show_weapon_id', 0) == weapon.iType
                self.send_event('E_SHOW_PARABOLA_TRACK', end_sfx, position, speed, g, up_angle, callback=self.track_callback, para_line_visible=is_line_visible, mass=mass, linear_damping=linear_damp)
            self.track_enable = True
            if self.track_target_model:
                self.track_target_model.destroy()
                self.track_target_model = None
            self.on_trigger_hold_effect(TRACK_END_MODEL_EFFECT_ID, create_cb=self.end_model_callback)
            return

    def del_track(self):
        if self.track_enable:
            self.send_event('E_HIDE_PARABOLA_TRACK')
            self.track_enable = False
            self.track_positions = None
            if self.track_target_model:
                self.track_target_model.destroy()
                self.track_target_model = None
            self.stop_sync_yaw()
        return

    def start_outline(self):
        self.outline_enable = True
        self.outline_timer = global_data.game_mgr.register_logic_timer(self.outline_tick, interval=1, times=-1, mode=LOGIC)

    def stop_outline(self):
        self.refresh_outline_unit([])
        self.outline_enable = False
        self.outline_targets = set()
        if self.outline_timer:
            global_data.game_mgr.unregister_logic_timer(self.outline_timer)
            self.outline_timer = False

    def refresh_outline_unit(self, units):
        destroys = set()
        for unit in self.outline_targets:
            if unit not in units:
                destroys.add(unit)

        for unit in destroys:
            self.outline_targets.remove(unit)
            model = unit.ev_g_model()
            if model:
                model.show_ext_technique(render.EXT_TECH_SMOOTH_OUTLINE, False)
                self.scene.enable_smooth_outline(False, unit.id)

        for unit in units:
            if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate(unit.ev_g_camp_id()):
                continue
            if unit not in self.outline_targets:
                model = unit.ev_g_model()
                if model:
                    self.outline_targets.add(unit)
                    model.show_ext_technique(render.EXT_TECH_SMOOTH_OUTLINE, True)
                    self.scene.enable_smooth_outline(True, unit.id)

    def outline_tick(self):
        if self.track_positions:
            if (self.track_positions[0] - self.track_positions[1]).length < 15 * NEOX_UNIT_SCALE:
                units = []
            else:
                ret = global_data.emgr.scene_get_area_unit_event.emit(self.track_positions[1], self.radius)
                units = ret[0] if ret else []
            self.refresh_outline_unit(units)

    def show_weapon_track(self):
        if global_data.cam_lplayer and self.sd.ref_driver_id != global_data.cam_lplayer.id:
            return
        if self.mecha_death:
            return
        if self.show_track_data:
            self.show_track()
        if self.show_track_data.get('enable_area_outline', False):
            self.start_outline()

    def stop_weapon_track(self):
        if self.track_enable:
            self.send_event('E_HIDE_PARABOLA_TRACK')
            self.track_enable = False
            self.track_positions = None
            if self.track_target_model:
                self.track_target_model.visible = False
                self.track_target_model.destroy()
                self.track_target_model = None
            self.stop_sync_yaw()
        if self.outline_enable:
            self.stop_outline()
        return

    def set_show_track_data(self, show_track_data, weapon_pos):
        self.show_track_data = show_track_data
        self.weapon_pos = weapon_pos
        weapon = self.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
        if self.show_track_data:
            self.radius = self.show_track_data['radius'].get(str(weapon.iType)) * self.radius_factor

    def _on_died(self):
        self.stop_weapon_track()
        self.mecha_death = True

    def mod_radius_factor(self, mod_value):
        self.radius_factor += mod_value
        if not self.show_track_data:
            return
        weapon = self.sd.ref_wp_bar_mp_weapons.get(self.weapon_pos)
        if weapon:
            self.radius = self.show_track_data['radius'].get(str(weapon.iType)) * self.radius_factor

    def keep_track_hide(self, duration):
        if self._hide_track_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._hide_track_timer_id)
            self._hide_track_timer_id = None
        self._hide_track_timer_id = global_data.game_mgr.register_logic_timer(self.delay_show_line, duration, times=1, mode=CLOCK)
        return

    def delay_show_line(self):
        self.send_event('E_SET_PARA_LINE_VISIBLE', self.track_enable and True or False)

    def on_reloading_bullet(self, time, *args):
        is_track_line_visible = self.ev_g_track_line_visible()
        if not is_track_line_visible:
            return
        self.send_event('E_SET_PARA_LINE_VISIBLE', False)
        self.keep_track_hide(time)

    def _change_sub_model_visible(self, visible):
        if not self.sd.ref_socket_res_agent:
            return
        else:
            self.sd.ref_socket_res_agent.set_model_res_visible(visible)
            self.sub_model_visible_timer = None
            self.sd.ref_socket_res_agent.set_sfx_res_visible(visible, FEET_SFX_KEY)
            if self.ev_g_is_avatar():
                self.send_event('E_USE_MECHA_SPECIAL_FORM_SENSITIVITY', not visible)
            return

    def on_change_shape(self, shape_type):
        visible = shape_type == ''
        interval = 0.1 if visible else 1.0
        if self.sub_model_visible_timer:
            global_data.game_mgr.unregister_logic_timer(self.sub_model_visible_timer)
        self.sub_model_visible_timer = global_data.game_mgr.register_logic_timer(self._change_sub_model_visible, interval=interval, args=(visible,), times=1, mode=CLOCK)

    def on_skin_sub_model_loaded(self):
        if self.ev_g_shape_shift():
            self._change_sub_model_visible(False)