# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_global_sync/ComPlayerGlobalSender.py
from __future__ import absolute_import
from .ComObserverGlobalSender import ComObserverGlobalSender
from logic.gcommon import const

class ComPlayerGlobalSender(ComObserverGlobalSender):
    BIND_EVENT = dict(ComObserverGlobalSender.BIND_EVENT)
    BIND_EVENT.update({'E_ON_GROUND_FINISH': 'player_on_ground',
       'E_ON_ACTION_LEAVE_VEHICLE': 'player_on_leave_vehicle',
       'E_LEAVE_SKATE': 'on_player_leave_skate',
       'S_ROLL_STAMINA': 'on_player_roll_stamina_changed',
       'S_AIR_JUMP_STAMINA': 'on_player_air_jump_stamina_changed',
       'E_AGONY': 'on_player_agony',
       'E_ON_SAVED': 'on_player_being_stop_rescue',
       'E_CANCEL_THROW_BOMB': 'on_player_cancel_throw_bomb',
       'E_UNEQUIP_RUSH_BONE': ('on_unequip_rush_bone', 10),
       'E_EQUIP_RUSH_BONE': ('on_equip_rush_bone', 10),
       'E_UNEQUIP_DOUBLE_JUMP_BONE': ('on_unequip_double_jump_bone', 10),
       'E_EQUIP_DOUBLE_JUMP_BONE': ('on_equip_double_jump_bone', 10),
       'E_ADD_JUMP_MAX_STAGE': ('on_add_jump_max_stage', 10),
       'E_ON_CURE_EXPIRED_CHANGE': 'on_cur_expired_changed',
       'E_DISABLE_MOVE': 'on_disable_rocker_move',
       'E_SUCCESS_INTERACTION': 'on_success_interaction',
       'E_SUCCESS_CELEBRATE': 'on_success_celebrate',
       'E_QUIT_CELEBRATE': 'on_quit_celebrate',
       'E_ON_CONTROL_TARGET_CHANGE': '_on_control_target_change'
       })
    DIRECT_FORWARDING_EVENT = dict(ComObserverGlobalSender.DIRECT_FORWARDING_EVENT)
    DIRECT_FORWARDING_EVENT.update({'E_PICK_UP_OTHERS': ('on_observer_pick_up_others_event', 10),
       'E_RECHOOSE_MECHA': ('on_player_rechoose_mecha_event', 10),
       'E_CHECK_ROTATION_INIT_EVENT': ('on_player_check_rotate_init_event', 10),
       'E_ON_LEAVE_MECHA': ('on_player_global_leave_mecha', 99),
       'E_DO_RB_POS': ('server_roll_back_pos', 99),
       'E_DEATH_DOOR_WEAK_POWER': 'death_door_weak_power_event',
       'E_SHOW_EFFECT_ENTRY': 'battle_add_pve_buff',
       'E_CLEAR_EFFECT_ENTRY': 'battle_remove_pve_buff'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComPlayerGlobalSender, self).init_from_dict(unit_obj, bdict)

    def get_in_plane(self, *args):
        super(ComPlayerGlobalSender, self).get_in_plane(*args)
        global_data.emgr.on_player_plane_stage_start.emit()

    def on_disable_rocker_move(self, enable):
        global_data.emgr.on_player_disable_rocker_move.emit(enable)
        if enable:
            self.send_event('E_MOVE_STOP')
        else:
            move_rocker = global_data.ui_mgr.get_ui('MoveRockerUI')
            if move_rocker:
                last_move_dir = move_rocker.last_move_dir
                if last_move_dir:
                    self.send_event('E_MOVE', last_move_dir)

    def parachute_status_changed(self, stage):
        super(ComPlayerGlobalSender, self).parachute_status_changed(stage)
        global_data.emgr.on_player_parachute_stage_changed.emit(stage)

    def player_on_ground(self, *args):
        global_data.emgr.on_player_jump_on_ground.emit()

    def player_on_leave_vehicle(self):
        global_data.emgr.player_on_leave_vehicle_event.emit()

    def on_player_leave_skate(self):
        global_data.emgr.on_player_leave_skate.emit()

    def _on_control_target_change(self, *args, **kw):
        global_data.emgr.on_player_control_target_change.emit(*args, **kw)

    def on_player_roll_stamina_changed(self, stamina):
        global_data.emgr.on_player_roll_stamina_changed.emit(stamina)

    def on_player_air_jump_stamina_changed(self, stamina):
        global_data.emgr.on_player_air_jump_stamina_changed.emit(stamina)

    def on_player_agony(self):
        global_data.emgr.on_player_agony_event.emit()

    def on_player_being_stop_rescue(self):
        global_data.emgr.on_player_rescue_back_event.emit()

    def on_player_cancel_throw_bomb(self):
        global_data.emgr.on_player_cancel_throw_bomb_event.emit()

    def on_unequip_rush_bone(self):
        global_data.emgr.on_player_unequip_rush_bone_event.emit()

    def on_equip_rush_bone(self):
        global_data.emgr.on_player_equip_rush_bone_event.emit()

    def on_unequip_double_jump_bone(self):
        global_data.emgr.on_player_unequip_double_jump_bone_event.emit()

    def on_equip_double_jump_bone(self):
        global_data.emgr.on_player_equip_double_jump_bone_event.emit()

    def on_add_jump_max_stage(self, *args):
        global_data.emgr.on_player_add_jump_max_stage_event.emit()

    def on_cur_expired_changed(self, expired_time):
        global_data.emgr.on_cure_expired_changed_event.emit(expired_time)

    def on_success_interaction(self):
        global_data.emgr.on_success_interaction_event.emit()

    def on_success_celebrate(self):
        global_data.player.logic.send_event('E_FREE_CAMERA_STATE', True)

    def on_quit_celebrate(self):
        global_data.player.logic.send_event('E_FREE_CAMERA_STATE', False)