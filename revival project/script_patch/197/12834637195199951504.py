# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTVMissileDriver.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.character_ctrl_utils import AirWalkDirectionSetter
from logic.gutils.screen_effect_utils import create_screen_effect_with_auto_refresh, remove_screen_effect_with_auto_refresh
from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_INCLUDE
from logic.gutils.collision_test_utils import CollisionTester
from logic.vscene.parts import PartCtrl
from common.cfg import confmgr
import collision
import math3d
import math
CONTROL_EXPLODE_SCREEN_EFFECT_PATH = 'effect/fx/weapon/boomer/boomer_pm.sfx'
FLY_SOUND_NAME = 'Play_tvmissile_fly_3p'

class ComTVMissileDriver(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_JUMP': 'jump',
       'E_EXPLODE_IN_ADVANCE': 'explode',
       'E_TV_MISSILE_EXPLODE_FROM_SERVER': 'do_explode_appearance',
       'G_HUMAN_COL_ID': 'get_col_id'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComTVMissileDriver, self).init_from_dict(unit_obj, bdict)
        self.owner_eid = bdict['owner_id']
        self.is_avatar = self.owner_eid == global_data.player.id
        self.weapon_id = bdict['npc_id']
        self.initial_position = math3d.vector(*bdict['position'])
        self.init_parameters()
        self.air_walk_direction_setter = AirWalkDirectionSetter(self)
        self.cur_position = self.initial_position
        self.explosion_appearance_done = False
        self.cur_yaw_enabled = True
        self.start_control_notified = False
        self.stop_control_notified = False
        self.scene_tester = None
        self.enemy_tester = None
        self.game_obj_id = global_data.sound_mgr.register_game_obj('tv_missile')
        self.sound_id = None
        global_data.emgr.scene_camera_player_setted_event += self.on_cam_lplayer_changed
        return

    def on_init_complete(self):
        if self.is_avatar:
            com_name = 'ComMoveSyncSender2'
            self.send_event('E_RECREATE_CHARACTER', 1, 3.5, 0.6)
        else:
            com_name = 'ComMoveSyncReceiver2'
        if not self.unit_obj.get_com(com_name):
            com = self.unit_obj.add_com(com_name, 'client')
            com.init_from_dict(self.unit_obj, {})
            com.on_init_complete()
            com.on_post_init_complete({})

    def init_parameters(self):
        conf = confmgr.get('grenade_config', str(self.weapon_id), default={})
        self.max_fly_radius = conf.get('fMaxDistance', 10000)
        self.fly_duration = conf.get('fTimeFly', 10)
        self.sd.ref_left_duration_percent = 1.0
        self.max_fly_duration = self.fly_duration
        self.fly_speed = conf.get('fSpeed', 1000)
        custom_param = conf.get('cCustomParam', {})
        self.delay_start_duration = custom_param.get('delay_start_duration', 1.0)
        self.check_scene_radius = custom_param.get('check_scene_radius', 0.5) * NEOX_UNIT_SCALE
        self.check_enemy_radius = custom_param.get('check_enemy_radius', 2) * NEOX_UNIT_SCALE
        self.delay_end_duration = custom_param.get('delay_end_duration', 1)
        self.camera_sense = custom_param.get('camera_sense', 4)

    def _notify_stop_control(self):
        if self.start_control_notified and not self.stop_control_notified:
            entity = global_data.battle.get_entity(self.owner_eid)
            if entity and entity.logic:
                entity.logic.send_event('E_STOP_CONTROL_TV_MISSILE')
                self.stop_control_notified = True
            if self.is_avatar:
                PartCtrl.enable_clamp_cam_rotation(False)

    def destroy(self):
        if self.sound_id:
            global_data.sound_mgr.stop_playing_id(self.sound_id)
            self.sound_id = None
        global_data.sound_mgr.unregister_game_obj(self.game_obj_id)
        self.game_obj_id = None
        if self.air_walk_direction_setter:
            self.air_walk_direction_setter.destroy()
            self.air_walk_direction_setter = None
        self._notify_stop_control()
        self._set_enable_yaw(True)
        global_data.emgr.scene_camera_player_setted_event -= self.on_cam_lplayer_changed
        if self.scene_tester:
            self.scene_tester.destroy()
            self.scene_tester = None
        if self.enemy_tester:
            self.enemy_tester.destroy()
            self.enemy_tester = None
        super(ComTVMissileDriver, self).destroy()
        remove_screen_effect_with_auto_refresh(self.owner_eid, CONTROL_EXPLODE_SCREEN_EFFECT_PATH)
        return

    def on_pos_changed(self, pos, *args):
        if math.isinf(pos.x) or math.isinf(pos.y) or math.isinf(pos.y) or math.isnan(pos.x) or math.isnan(pos.y) or math.isnan(pos.y):
            return
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(pos)
        else:
            self.send_event('E_POSITION', pos)
        self.cur_position = pos

    def _set_enable_yaw(self, enable):
        if not self.is_avatar:
            return
        if self.cur_yaw_enabled ^ enable:
            global_data.emgr.enable_camera_yaw.emit(enable)
            self.cur_yaw_enabled = enable

    def on_model_loaded(self, model):
        self.need_update = True
        self.sound_id = global_data.sound_mgr.post_event(FLY_SOUND_NAME, self.game_obj_id, self.cur_position)
        entity = global_data.battle.get_entity(self.owner_eid)
        if entity and entity.logic:
            entity.logic.send_event('E_TV_MISSILE_FIRED', self.unit_obj.get_owner())
        if not self.is_avatar:
            return
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        char_ctrl.setPositionChangedCallback(self.on_pos_changed)
        self.send_event('E_TRY_ACTIVE_CHARACTER')
        self.send_event('E_FOOT_POSITION', self.initial_position)
        self.send_event('E_GRAVITY', 0)
        self._set_enable_yaw(False)
        radius = self.check_scene_radius
        col = collision.col_object(collision.SPHERE, math3d.vector(radius, radius, radius), 0, 0, 1)
        self.scene_tester = CollisionTester(col, self.owner_eid, GROUP_CHARACTER_INCLUDE, GROUP_CHARACTER_INCLUDE)
        radius = self.check_enemy_radius
        col = collision.col_object(collision.SPHERE, math3d.vector(radius, radius, radius), 0, 0, 1)
        self.enemy_tester = CollisionTester(col, self.owner_eid, ignore_groupmates=True)
        self.air_walk_direction_setter.reset()

    def explode(self, with_delay_appearance=True):
        if self.is_avatar:
            self.do_explode_appearance()
            self.send_event('E_ENABLE_SYNC', True)
            self.send_event('E_PHY_DIRECTION', math3d.vector(0, 0, 0))
            self.send_event('E_VERTICAL_SPEED', 0)
            self.need_update = False
            position = self.cur_position
            self.send_event('E_CALL_SYNC_METHOD', 'trigger_tvmissile_explode', (
             (
              position.x, position.y, position.z), self.delay_end_duration if with_delay_appearance else 0), True)
            if not with_delay_appearance:
                self._notify_stop_control()

    def start_control_missile(self):
        if self.start_control_notified:
            return
        entity = global_data.battle.get_entity(self.owner_eid)
        if entity and entity.logic:
            entity.logic.send_event('E_START_CONTROL_TV_MISSILE', self.unit_obj.get_owner())
        self.start_control_notified = True
        self.on_cam_lplayer_changed()
        self._set_enable_yaw(True)
        if self.is_avatar:
            PartCtrl.enable_clamp_cam_rotation(True, 0.01 * self.camera_sense)

    def tick(self, dt):
        global_data.sound_mgr.set_position(self.game_obj_id, self.ev_g_position())
        if self.is_avatar:
            self.fly_duration -= dt
            if self.fly_duration <= 0:
                self.sd.ref_left_duration_percent = 0
                self.explode()
                return
            self.sd.ref_left_duration_percent = self.fly_duration / self.max_fly_duration
            if (self.cur_position - self.initial_position).length > self.max_fly_radius:
                self.explode()
                return
            if self.enemy_tester.get_hit_obj_eid_list_by_static_test(self.cur_position) or self.scene_tester.check_hit_scene_by_static_test(self.cur_position):
                self.explode()
                return
            cam = self.scene.active_camera
            forward = cam.rotation_matrix.forward
            self.air_walk_direction_setter.execute(forward * self.fly_speed, horizontal_walk_event_name='E_PHY_DIRECTION')
        self.delay_start_duration -= dt
        if -dt < self.delay_start_duration <= 0:
            self.start_control_missile()

    def jump(self, jump_speed=None):
        jump_speed *= self.jump_factor
        char_ctrl = self.sd.ref_character
        if not char_ctrl:
            return
        else:
            if jump_speed is not None:
                char_ctrl.setJumpSpeed(jump_speed)
            char_ctrl.jump()
            return

    def do_explode_appearance(self):
        if self.explosion_appearance_done:
            return
        else:
            if self.start_control_notified:
                self.is_avatar and global_data.emgr.camera_play_added_trk_event.emit('1054_FIRE', None, None)
                create_screen_effect_with_auto_refresh(self.owner_eid, CONTROL_EXPLODE_SCREEN_EFFECT_PATH)
            model = self.ev_g_model()
            if model:
                model.visible = False
            entity = global_data.battle.get_entity(self.owner_eid)
            if entity and entity.logic:
                entity.logic.send_event('E_TV_MISSILE_EXPLODED')
            self.explosion_appearance_done = True
            self._set_enable_yaw(False)
            global_data.sound_mgr.stop_playing_id(self.sound_id)
            self.sound_id = None
            return

    def on_cam_lplayer_changed(self):
        cam_lplayer = global_data.cam_lplayer
        if cam_lplayer and cam_lplayer.id == self.owner_eid:
            visible = not self.start_control_notified
        else:
            visible = True
        model = self.ev_g_model()
        if model:
            model.visible = visible

    def get_col_id(self):
        return []