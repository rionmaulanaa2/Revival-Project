# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_global_sync/ComPlayerGlobalReceiver.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE

class ComPlayerGlobalReceiver(UnitCom):

    def init_from_dict(self, unit_obj, bdict):
        super(ComPlayerGlobalReceiver, self).init_from_dict(unit_obj, bdict)
        self.init_global_event()

    def init_global_event(self):
        emgr = global_data.emgr
        emgr.player_try_switch_parachute_stage += self.try_switch_parachute_stage
        emgr.camera_switch_to_state_event += self.switch_camera_state
        emgr.drive_ui_ope_change_event += self.switch_vehicle_ope_type
        emgr.scene_camera_player_setted_event += self.switch_camera_player

    def try_switch_parachute_stage(self, jump_pos_info=None):
        from logic.gcommon.common_utils import parachute_utils
        cnt_stage = self.sd.ref_parachute_stage
        if self.ev_g_in_carrier_or_plane():
            mark_info = self.ev_g_warning_drawn_map_mark()
            if global_data.enable_parachute_range_circle and not (mark_info or jump_pos_info):
                return
            battle = global_data.battle
            if not battle:
                return
            plane = battle.get_entity(battle.plane_id)
            if not (plane and plane.logic):
                return
            plane = plane.logic
            start_pos = plane.ev_g_position()
            if not start_pos:
                return
            start_pos = [
             start_pos.x, start_pos.y, start_pos.z]
            if global_data.enable_parachute_range_circle:
                if jump_pos_info:
                    s_pos = jump_pos_info['start_pos']
                    s_pos[1] = start_pos[1]
                    start_pos = s_pos
                    end_pos = jump_pos_info['end_pos']
                if mark_info:
                    end_pos = mark_info['v3d_map_pos']
                    if not plane.ev_g_can_jump_to(end_pos):
                        return
                    end_pos = [
                     end_pos.x, end_pos.y, end_pos.z]
            else:
                end_pos = math3d.vector(start_pos[0], start_pos[1], start_pos[2])
                if mark_info:
                    target_pos = mark_info['v3d_map_pos']
                    target_dir = target_pos - end_pos
                    target_dir.y = 0
                    target_dir.normalize()
                    end_pos += target_dir * 10 * NEOX_UNIT_SCALE
                else:
                    plane_dir = plane.ev_g_plane_direction()
                    end_pos += plane_dir * 10 * NEOX_UNIT_SCALE
                end_pos = [
                 end_pos.x, end_pos.y, end_pos.z]
            from common.cfg import confmgr
            parachute_conf = confmgr.get('parachute_conf').get_conf()
            end_pos[1] = start_pos[1] - parachute_conf['LAUNCH_HEIGHT'] * NEOX_UNIT_SCALE
            if not global_data.enable_parachute_range_circle:
                start_pos[1] -= parachute_conf['LAUNCH_HEIGHT'] * NEOX_UNIT_SCALE * 0.66
            battle = self.unit_obj.get_battle()
            move_range = battle.get_move_range()
            if not move_range:
                from common.cfg import confmgr
                map_id = battle.map_id
                conf = confmgr.get('map_config', str(map_id), default={})
                default_ll_pos = [-350 * NEOX_UNIT_SCALE, -600 * NEOX_UNIT_SCALE]
                default_ru_pos = [480 * NEOX_UNIT_SCALE, 390 * NEOX_UNIT_SCALE]
                l_pos = conf.get('walkLowerLeftPos', default_ll_pos)
                r_pos = conf.get('walkUpRightPos', default_ru_pos)
                move_range = {'min_x': l_pos[0],
                   'max_x': r_pos[0],
                   'min_z': l_pos[1],
                   'max_z': r_pos[1]
                   }
            end_pos[0] = min(max(end_pos[0], move_range['min_x']), move_range['max_x'])
            end_pos[2] = min(max(end_pos[2], move_range['min_z']), move_range['max_z'])
            self.send_event('E_PREPARE_LAUNCH', start_pos, end_pos)
        if cnt_stage == parachute_utils.STAGE_LAUNCH_PREPARE:
            launch_pos = self.ev_g_launch_pos()
            if launch_pos:
                start_pos, end_pos = launch_pos
                start_pos = [start_pos.x, start_pos.y, start_pos.z]
                end_pos = [end_pos.x, end_pos.y, end_pos.z]
                self.send_event('E_START_PARACHUTE', start_pos, end_pos, True)
                return
        if cnt_stage == parachute_utils.STAGE_FREE_DROP:
            self.send_event('E_OPEN_PARACHUTE')
            return

    def switch_camera_state(self, *args):
        self.send_event('E_SWITCH_CAMERA_STATE', *args)

    def switch_vehicle_ope_type(self, new_ope):
        is_in_drive_vehicle = self.ev_g_is_driver()
        if is_in_drive_vehicle:
            cur_control_target = self.ev_g_control_target()
            if cur_control_target and cur_control_target.logic:
                cur_control_target.logic.send_event('E_SWITCH_VEHICLE_OPE_TYPE', new_ope)

    def switch_camera_player(self, *args):
        if global_data.cam_lplayer:
            if global_data.cam_lplayer == self.unit_obj.id:
                pass
            else:
                global_data.cam_lplayer.send_event('E_UPDATE_OCC_VIS_TYPE')