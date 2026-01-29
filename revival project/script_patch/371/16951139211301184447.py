# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComCtrlMecha.py
from __future__ import absolute_import
from __future__ import print_function
import six
from ..UnitCom import UnitCom
from mobile.common.EntityManager import EntityManager
from logic.gutils import get_on_mecha_utils
from logic.gutils import mecha_utils as mutils
from logic.gcommon.common_const import mecha_const as mconst
from logic.gcommon.const import NEOX_UNIT_SCALE
from ...cdata import status_config
from common.cfg import confmgr
from logic.gcommon import time_utility
from logic.gcommon.common_const import water_const
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT, GROUP_GRENADE, GROUP_STATIC_SHOOTUNIT
from logic.gutils.client_unit_tag_utils import preregistered_tags
from logic.client.const import game_mode_const
import world
import math3d
import time
import game3d
import copy
from logic.gutils import character_ctrl_utils
from data.vibrate_key_def import DESTROYED_VIBRATE_LV
from logic.gutils.CameraHelper import get_mecha_camera_type
from logic.gcommon.common_const import battle_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
import logic.gcommon.common_const.vehicle_const as vehicle_const
MODEL_SHADER_CTRL_SET_ENABLE = hasattr(world.model, 'set_inherit_parent_shaderctrl')

class ComCtrlMecha(UnitCom):
    BIND_EVENT = {'E_RECALL_SUCESS': '_on_recall_result',
       'E_TRY_LEAVE_MECHA': '_try_leave_mecha',
       'E_ON_JOIN_MECHA_START': '_on_join_mecha_start',
       'E_ON_JOIN_MECHA': '_on_join_mecha',
       'E_ON_LEAVE_MECHA_START': '_on_leave_mecha_start',
       'E_ON_LEAVE_MECHA': '_on_leave_mecha',
       'E_SWITCH_TO_MECHA_STATE': '_on_switch_to_mecha_state',
       'E_PARACHUTE_STATUS_CHANGED': '_on_parachute_state_changed',
       'G_GET_BIND_MECHA': '_get_bind_mecha',
       'G_GET_FIXED_MECHA': '_get_fixed_mecha',
       'G_BIND_MECHA_ENTITY': '_get_bind_mecha_entity',
       'E_SET_BIND_MECHA_TYPE': '_set_bind_mecha_type',
       'G_GET_BIND_MECHA_TYPE': '_get_bind_mecha_type',
       'G_NEED_PLAY_JOIN_ANIM': '_get_need_play_join_anim',
       'G_GET_CHANGE_STATE': '_get_change_state',
       'G_MECHA_HP_INIT': '_get_hp_init',
       'G_MECHA_RECALL_TIMES': '_get_recall_times',
       'G_TRY_JOIN_MECHA': '_try_join_mecha',
       'G_TRY_JOIN_MECHA_SHARE': '_try_join_mecha_share',
       'G_CTRL_MECHA': '_get_ctrl_mecha_id',
       'G_CTRL_MECHA_OBJ': '_get_ctrl_mecha_obj',
       'G_MECHA_EXP_INIT': '_get_mecha_exp',
       'E_STATE_CHANGE_CD': 'on_update_change_cd',
       'S_MECHA_RECALL_CD_TYPE': 'set_recall_cd_type',
       'E_SET_RECHOOSE_MECHA': 'set_rechoose_mecha',
       'G_IS_CTRL_SHARE_MECHA': 'on_is_ctrl_share_mecha',
       'E_SELECT_RANDOM_MECHA': '_select_random_mecha',
       'G_SELECTED_RANDOM_MECHA': '_get_selected_random_mecha',
       'G_IS_PURE_MECHA': '_get_is_pure_mecha',
       'G_IS_HUNTER_MECHA': '_get_is_hunter_mecha',
       'G_MECHA_GROUPMATE_MUTEX': '_get_groupmate_mutex',
       'G_CHECK_GROUPMATE_MECHA_NUM': '_check_groupmate_mecha_num',
       'G_JOIN_VEHICLE_MECHA_TIMES': '_get_join_vehicle_mecha_times',
       'G_IS_FIRST_CALLING': '_get_is_first_calling',
       'E_SET_IS_FIRST_CALLING': '_set_is_first_calling',
       'G_IS_FIRST_JOINING_VEH_MECHA': '_get_is_first_joining_vehicle_mecha',
       'E_SET_IS_FIRST_JOINING_VEH_MECHA': '_set_is_first_joining_vehicle_mecha',
       'E_TRANS_CREATE_MECHA_TO_SHARE': '_trans_create_mecha_to_share',
       'E_REVIVE': '_on_revive',
       'E_CHANGE_SEAT': '_try_change_seat',
       'G_ENABLE_MECHA_REDRESS': '_get_enable_mecha_redress'
       }
    SHARE_MECHA_ZONE_DIST = 50
    PURE_MECHA_HIDE_UI = ('StateChangeUI', 'StateChangeUIPC', 'MechaUI', 'WeaponBarSelectUI',
                          'PostureControlUI', 'FireRockerUI', 'FightLeftShotUI',
                          'BulletReloadUI', 'HpInfoUI')

    def __init__(self):
        super(ComCtrlMecha, self).__init__()
        self.mecha_ui_list = []
        self.mecha_ui_load_list = []
        self._high_eject = False
        self._is_share_mecha = False
        self._joining_share_mecha_entity_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComCtrlMecha, self).init_from_dict(unit_obj, bdict)
        self._bind_mecha_id = bdict.get('created_mecha_id', None)
        self._fixed_mecha_id = self._bind_mecha_id
        self._bind_mecha_type = bdict.get('created_mecha_type', None)
        self._fixed_mecha_type = self._bind_mecha_type
        self._ctrl_mecha_id = bdict.get('ctrl_mecha_id', None)
        self._recall_cd = bdict.get('recall_cd', mconst.RECALL_MAXCD_TYPE_GETMECHA)
        self._recall_left_time = bdict.get('recall_left_time', mconst.RECALL_MAXCD_TYPE_GETMECHA)
        self._recall_cd_type = bdict.get('recall_cd_type', None)
        self._recall_cd_end_timestamp = self._recall_left_time + time_utility.get_server_time()
        self._init_hp = bdict.get('created_mecha_hp', [0, 0, 0, 0])
        self._mecha_exp = bdict.get('mecha_exp', 0) or 0
        self._recall_times = bdict.get('recall_times', 0)
        self._recall_cd_rate = bdict.get('recall_cd_rate', 1)
        self._mecha_ui = False
        self._need_play_join_anim = False
        self._is_pure_mecha = bdict.get('is_pure_mecha', False)
        self._is_hunter_mecha = False
        self._battle_type = global_data.game_mode.get_mode_type()
        self._can_change_mecha = bdict.get('change_mecha', False)
        self._enable_mecha_redress = bdict.get('enable_mecha_redress', False)
        if global_data.game_mode.get_mode_type() == game_mode_const.GAME_MODE_HUNTING:
            self._is_hunter_mecha = global_data.battle.is_mecha_group(self.ev_g_group_id())
            self._is_pure_mecha = self._is_hunter_mecha
            global_data.ui_mgr.remove_blocking_ui_list(self.PURE_MECHA_HIDE_UI, 'pure_mecha')
        elif self._is_pure_mecha:
            global_data.ui_mgr.add_blocking_ui_list(self.PURE_MECHA_HIDE_UI, 'pure_mecha')
        else:
            global_data.ui_mgr.remove_blocking_ui_list(self.PURE_MECHA_HIDE_UI, 'pure_mecha')
        self._entering_share_mecha = False
        self.switch_to_state_change_ui()
        self._selected_random_mecha_no = bdict.get('selected_random_mecha', 0)
        self._mecha_groupmate_mutex = bdict.get('groupmate_mecha_mutex', 0)
        self._groupmate_mecha_num = bdict.get('groupmate_mecha_num', 0)
        self._is_first_calling = False
        self._is_first_joining_vehicle_mecha = False
        self._join_vehicle_mecha_times = bdict.get('join_vehicle_mecha_times', 0)
        self._has_trans_created_to_share = False
        self._enable_early_create_mecha = bdict.get('enable_early_create_mecha', 0)
        self._lobby_mecha_info = bdict.get('lobby_mecha_info', None)
        return

    def set_rechoose_mecha(self, is_revive):
        self._can_change_mecha = True
        if is_revive:
            self.rechoose_mecha()

    def rechoose_mecha(self):
        if not self._can_change_mecha:
            return
        else:
            self._bind_mecha_id = None
            self._bind_mecha_type = None
            self._ctrl_mecha_id = None
            self._init_hp = [0, 0, 0, 0]
            if self.is_unit_obj_type('LAvatar') or self.ev_g_is_cam_target():
                global_data.ui_mgr.close_ui('StateChangeUI')
                self._refresh_stage()
                global_data.emgr.reset_join_mecha_bgm.emit()
            self._can_change_mecha = False
            return

    def _on_switch_to_mecha_state(self, mecha_id=None):
        self.switch_to_state_change_ui()
        if self.sd.ref_is_avatar:
            ui = global_data.ui_mgr.get_ui('StateChangeUI')
            if ui:
                ui.on_cancel_enter_mecha()

    def switch_to_state_change_ui(self, mecha_state=False):
        if self.sd.ref_is_avatar:
            if not global_data.ui_mgr.get_ui('StateChangeUI'):
                if global_data.ex_scene_mgr_agent.check_settle_scene_active():
                    return
                ui = global_data.ui_mgr.show_ui('StateChangeUI', 'logic.comsys.battle')
                if mecha_state:
                    ui.on_change_state(mecha_state)

    def on_init_complete(self):
        self._refresh_stage()

    def on_post_init_complete(self, bdict):
        if self._is_pure_mecha:
            self.send_event('E_HIDE_MODEL')
            self.send_event('E_FORCE_DEACTIVE')
        if not self.sd.ref_is_avatar:
            return

    def _on_parachute_state_changed(self, stage):
        self._refresh_stage()

    def _refresh_stage(self):
        _id = None
        from logic.gutils import judge_utils
        if judge_utils.is_ob():
            ob_unit = judge_utils.get_ob_target_unit()
            if ob_unit:
                _id = ob_unit.id
        else:
            _id = global_data.player.id
        if _id == self.unit_obj.id and not self._bind_mecha_id and not self.ev_g_death() and not global_data.player.is_in_global_spectate():
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_IMPROVISE):
                if global_data.improvise_battle_data.get_cur_round_mecha_type_id() <= 0:
                    global_data.ui_mgr.close_ui('StateChangeUI')
            else:
                global_data.ui_mgr.close_ui('StateChangeUI')
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_HUMAN_SURVIVAL):
                global_data.ui_mgr.close_ui('MechaUI')
            else:
                bat = self.unit_obj.get_battle()

                def do_later(bat=bat):
                    if not global_data.ex_scene_mgr_agent.check_settle_scene_active() and not (bat and bat.is_in_settle_celebrate_stage() and (self._has_trans_created_to_share or self._fixed_mecha_id)):
                        ui = global_data.ui_mgr.show_ui('MechaUI', 'logic.comsys.battle')
                        if ui:
                            p_stage = self.sd.ref_parachute_stage
                            from logic.gcommon.common_utils.parachute_utils import STAGE_LAND, STAGE_ISLAND
                            if p_stage >= STAGE_LAND and p_stage != STAGE_ISLAND:
                                ui.add_show_count('ComCtrlMecha')
                            else:
                                ui.add_hide_count('ComCtrlMecha')
                            ui.refresh_random_mecha_icon()
                        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_TRAIN):
                            from logic.comsys.battle.BattleUtils import get_prepare_left_time
                            if get_prepare_left_time() > 0:
                                global_data.ui_mgr.close_ui('MechaUI')

                global_data.game_mgr.next_exec(do_later)
        return

    def _refresh_share_ui(self, show_other):
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_HUMAN_SURVIVAL):
            global_data.ui_mgr.close_ui('MechaUI')
            return
        if show_other:
            bat = self.unit_obj.get_battle()
            if not (bat and bat.is_in_settle_celebrate_stage() and (self._has_trans_created_to_share or self._fixed_mecha_id)):
                if not self._bind_mecha_id and not global_data.ex_scene_mgr_agent.check_settle_scene_active():
                    global_data.ui_mgr.show_ui('MechaUI', 'logic.comsys.battle')
        else:
            global_data.ui_mgr.close_ui('MechaUI')

    def destroy(self):
        owner = self.unit_obj.get_owner()
        if owner and owner.__class__.__name__ == 'Avatar':
            self._switch_to_mecha_ui(False)
            from data import camera_state_const
            global_data.emgr.switch_to_mecha_camera.emit(camera_state_const.THIRD_PERSON_MODEL)
        if self.ev_g_is_cam_target():
            global_data.emgr.scene_show_small_map_event.emit(False)
        if self._entering_share_mecha:
            self.cancel_join_share_mecha()
        super(ComCtrlMecha, self).destroy()

    def _get_hp_init(self):
        return self._init_hp

    def _get_change_state(self):
        return (
         self._recall_cd_type, self._recall_cd, self._recall_cd_end_timestamp - time_utility.get_server_time())

    def _get_bind_mecha(self):
        return self._bind_mecha_id

    def _get_fixed_mecha(self):
        return self._fixed_mecha_id

    def _get_bind_mecha_entity(self):
        return EntityManager.getentity(self._bind_mecha_id)

    def _get_bind_mecha_type(self):
        return self._bind_mecha_type

    def _set_bind_mecha_type(self, mecha_type_id, is_share):
        self._bind_mecha_type = mecha_type_id
        if not is_share:
            self._fixed_mecha_type = mecha_type_id

    def _get_need_play_join_anim(self):
        return self._need_play_join_anim and not self._is_pure_mecha and not self._is_hunter_mecha

    def _get_is_pure_mecha(self):
        return self._is_pure_mecha

    def _get_is_hunter_mecha(self):
        return self._is_hunter_mecha

    def _get_groupmate_mutex(self):
        return self._mecha_groupmate_mutex

    def _get_mecha_exp(self):
        return self._mecha_exp

    def _on_recall_result(self, ret, err_code=None):
        if not ret:
            self.ev_g_cancel_state(status_config.ST_MECHA_BOARDING)
            global_data.emgr.enable_camera_yaw.emit(True)
        else:
            global_data.emgr.close_mecha_summon_ui_event.emit()
            self._recall_times += 1
            self._is_first_calling = self._recall_times == 1
            if self.unit_obj.__class__.__name__ == 'LAvatar':
                global_data.ui_mgr.close_ui('MechaUI')

    def record_used_mecha(self):
        if not global_data.player:
            return
        used_mecha = global_data.player.get_setting('used_mecha', [])
        mecha_entity = self._get_bind_mecha_entity()
        if mecha_entity and mecha_entity.logic:
            mecha_id = mecha_entity.logic.share_data.ref_mecha_id
            if mecha_id in used_mecha:
                return
            used_mecha.append(mecha_id)
            global_data.player.write_setting('used_mecha', used_mecha)
            global_data.player.save_settings_to_file()

    def _check_groupmate_mecha_num(self, show_tips=True):
        if self._groupmate_mecha_num <= 0:
            return True
        now_mecha_num = mutils.get_groupmate_inmecha_num(global_data.player.logic)
        if now_mecha_num < self._groupmate_mecha_num:
            return True
        if show_tips:
            global_data.emgr.battle_show_message_event.emit(','.join([get_text_by_id(860092), get_text_by_id(860093)]))
        return False

    def _try_join_mecha(self, mecha_id, seat_type=vehicle_const.SEAT_TYPE_DRIVER):
        self._request_join_mecha('try_join_mecha', mecha_id, seat_type)

    def _try_join_mecha_share(self, mecha_id):
        if not self._check_groupmate_mecha_num():
            return
        else:
            self._joining_share_mecha_entity_id = mecha_id

            def finish_join_share_mecha(*args):
                if not self or not self.is_valid():
                    return
                if not self._check_groupmate_mecha_num():
                    return
                if self._entering_share_mecha:
                    self.cancel_join_share_mecha()
                    self._request_join_mecha('try_join_mecha_share', mecha_id, vehicle_const.SEAT_TYPE_DRIVER)

            self.send_event('E_SHOW_PROGRESS', 3, None, get_text_by_id(19112), callback=finish_join_share_mecha, cancel_callback=self.cancel_join_share_mecha, icon_path='gui/ui_res_2/battle/read_bar/icon_get_on_mecha.png')
            regist_event = self.regist_event
            if G_POS_CHANGE_MGR:
                self.regist_pos_change(self.check_share_mecha_zone, 0.2)
            else:
                regist_event('E_POSITION', self.check_share_mecha_zone, -999)
            regist_event('E_ON_HIT', self.cancel_join_share_mecha, -999)
            regist_event('E_ENTER_STATE', self._enter_states, -999)
            self._entering_share_mecha = True
            return

    def check_share_mecha_zone(self, *args):
        if self._joining_share_mecha_entity_id:
            mecha_entity = EntityManager.getentity(self._joining_share_mecha_entity_id)
            if mecha_entity and mecha_entity.logic:
                is_enter, dist = mecha_entity.logic.ev_g_check_enter_consoloe_zone(self.ev_g_position())
                if dist and dist < self.SHARE_MECHA_ZONE_DIST:
                    return
        self.cancel_join_share_mecha()

    def cancel_join_share_mecha(self, *args):
        if self._entering_share_mecha:
            self._entering_share_mecha = False
            self.send_event('E_CLOSE_PROGRESS')
            unregist_event = self.unregist_event
            if G_POS_CHANGE_MGR:
                self.unregist_pos_change(self.check_share_mecha_zone)
            else:
                unregist_event('E_POSITION', self.check_share_mecha_zone)
            unregist_event('E_ON_HIT', self.cancel_join_share_mecha)
            unregist_event('E_ENTER_STATE', self._enter_states)
            self._joining_share_mecha_entity_id = None
        return

    def _try_change_seat(self):
        control_target = self.ev_g_control_target()
        if not control_target or not control_target.logic or control_target.logic.__class__.__name__ != 'LMotorcycle':
            return
        if control_target.logic.ev_g_is_full_seat():
            return
        cur_seat_index = control_target.logic.ev_g_passenger_seat_index(self.unit_obj.id)
        if cur_seat_index < 0:
            log_error('test--_try_change_seat--step2--cur_seat_index =', cur_seat_index, '--control_target =', control_target, '--unit_obj =', self.unit_obj)
            import traceback
            traceback.print_stack()
            return
        all_empty_seat = control_target.logic.ev_g_all_empty_seat()
        new_seat_index = -1
        if all_empty_seat[-1] <= cur_seat_index:
            new_seat_index = all_empty_seat[0]
        else:
            for one_seat_index in all_empty_seat:
                if one_seat_index > cur_seat_index:
                    new_seat_index = one_seat_index
                    break

        seat_name = control_target.logic.ev_g_seat_name_by_index(new_seat_index)
        self.send_event('E_CALL_SYNC_METHOD', 'try_change_seat', (seat_name,), True)

    def _request_join_mecha(self, proto, mecha_id, seat_type):
        mecha_entity = EntityManager.getentity(mecha_id)
        if mecha_entity and mecha_entity.logic:
            sname, flag = mecha_entity.logic.ev_g_empty_seat(seat_type)
            if flag:
                self.send_event('E_CALL_SYNC_METHOD', proto, (mecha_id, sname, False), True)

    def _on_join_mecha_start(self, mecha_entity_id, mecha_type, timestamp, share_mecha, fashion, seat_name):
        is_avatar = self.sd.ref_is_avatar
        if is_avatar:
            print('[Mecha] _on_join_mecha_start ', mecha_entity_id, mecha_type, timestamp, share_mecha, fashion, seat_name)
        self._is_share_mecha = share_mecha
        if mecha_type == mconst.MECHA_TYPE_NORMAL:
            if not self._is_share_mecha:
                self._fixed_mecha_id = mecha_entity_id
                self._bind_mecha_id = mecha_entity_id
            delta_time = time_utility.time() - timestamp
            if delta_time < 2:
                self._need_play_join_anim = True
            if self.sd.ref_is_avatar:
                global_data.emgr.enable_camera_yaw.emit(False)
            mecha_entity = EntityManager.getentity(mecha_entity_id)
            if mecha_entity and mecha_entity.logic:
                if mecha_entity.is_share():
                    if fashion:
                        mecha_entity.logic.send_event('E_CHANGE_MECHA_FASHION', fashion)
                    mecha_entity.logic.send_event('E_NOTIFY_BOARD', self.unit_obj)
                    if self.ev_g_is_groupmate(global_data.player.id):
                        now_mecha_num = mutils.get_groupmate_inmecha_num(global_data.player.logic)
                        if self._groupmate_mecha_num > 0 and self._groupmate_mecha_num == now_mecha_num + 1:
                            message = {'i_type': battle_const.ONLY_JOIN_ONE_SHARE_MECHA_TIPS,'interval_time': 3}
                            global_data.emgr.show_battle_main_message.emit(message, battle_const.MAIN_NODE_COMMON_INFO)
            return
        owner = self.unit_obj.get_owner()
        mecha_entity = EntityManager.getentity(mecha_entity_id)
        if mecha_entity and mecha_entity.logic:
            mecha_id = mecha_entity.logic.share_data.ref_mecha_id
            mecha_type = mutils.get_mecha_type(mecha_id)
            mecha_entity.logic.send_event('E_ENABLE_SYNC', is_avatar or mecha_entity.logic.share_data.ref_is_agent)
            if mecha_type == mconst.MECHA_TYPE_VEHICLE:
                self._on_join_mecha_vehicle(mecha_entity_id, seat_name=seat_name)
        is_show_gun = self.ev_g_is_show_gun()
        if not is_show_gun:
            self.send_event('E_SET_EMPTY_HAND', False)

    def _on_join_mecha_vehicle(self, mecha_id, driver=None, passenger=None, seat_name=None):
        if self.ev_g_is_cam_target():
            global_data.game_mgr.scene.disable_vegetation()
        from logic.gcommon.common_const import vehicle_const
        self._join_vehicle_mecha_times += 1
        self._is_first_joining_vehicle_mecha = self._join_vehicle_mecha_times == 1
        if passenger is None:
            passenger = {}
        mecha_entity = EntityManager.getentity(mecha_id)
        if mecha_entity and mecha_entity.logic:
            if driver is None:
                driver = mecha_entity.logic.sd.ref_driver_id
            pattern = mecha_entity.logic.ev_g_pattern()
            eid = self.unit_obj.id
            if self.sd.ref_is_avatar:
                mecha_entity.logic.send_event('E_UPDATE_LOD', 0)
            is_vehicle = pattern == mconst.MECHA_TYPE_VEHICLE
            if eid == driver:
                self.ev_g_status_try_trans(status_config.ST_MECHA_DRIVER)
                is_driver = True
            else:
                vehicle_state = self.ev_g_vehicle_state(mecha_entity, status_config.ST_MECHA_PASSENGER)
                if vehicle_state is not None:
                    self.ev_g_status_try_trans(vehicle_state)
                is_driver = False
            self.send_event('E_ON_ACTION_ON_VEHICLE', mecha_entity)
            self.send_event('E_ON_STATUS_CHANGED')
            self.send_event('E_CLEAR_ACC_INFO')
            if driver:
                passenger['driver_info'] = {'new_driver': driver}
            data = {'data': passenger,'change_type': vehicle_const.CH_SEAT_INFO
               }
            mecha_entity.logic.send_event('E_ON_JOIN_MECHA')
            mecha_entity.logic.send_event('E_VEHICLE_DATA_CHANGE', data)
            mecha_entity.logic.send_event('E_PATTERN_HANDLE', pattern, force_update=True)
            mecha_entity.logic.send_event('E_ENABLE_BEHAVIOR', True)
            mecha_entity.logic.send_event('E_ON_ENABLE_AIM_HELPER', self.ev_g_is_avatar())
            if global_data.player.id == eid:
                global_data.mecha = mecha_entity
                if global_data.moveKeyboardMgr:
                    global_data.moveKeyboardMgr.stop_move_lock()
            ctrl_conf = {'driver': driver}
            if seat_name:
                ctrl_conf['seat_name'] = seat_name
            self.send_event('E_SET_CONTROL_TARGET', mecha_entity, ctrl_conf)
            myid = global_data.player.id
            if eid == myid and mecha_entity:
                global_data.player.logic.send_event('E_ENABLE_WATER_UPDATE', False)
                mecha_entity.logic.send_event('E_VEHICLE_COLLISION_SET', True)
                if is_driver:
                    mecha_entity.logic.send_event('E_CONTROL_MECHA_TWO', True)
                    mecha_entity.logic.send_event('E_RESET_STATE', is_vehicle=is_vehicle)
                else:
                    mecha_entity.logic.send_event('E_CONTROL_MECHA_TWO', True)
            elif global_data.cam_lplayer and global_data.cam_lplayer.id == eid:
                if mecha_entity and mecha_entity.logic:
                    mecha_entity.logic.send_event('E_VEHICLE_COLLISION_SET', True)
                    mecha_entity.logic.send_event('E_OBSERVE_CONTROL_MECHA_TWO')
        return

    def _on_join_mecha(self, mecha_id, hide_model=False):
        if self.ev_g_is_cam_target():
            global_data.game_mgr.scene.disable_vegetation()
        self.record_used_mecha()
        self._bind_mecha_id = mecha_id
        self._ctrl_mecha_id = mecha_id
        self.send_event('E_FIGHT_STATE_CHANGED', True)
        self.send_event('E_CLEAR_ACC_INFO')
        self.ev_g_status_try_trans(status_config.ST_MECHA_DRIVER)
        if self.ev_g_in_mecha():
            return
        else:
            if hide_model:
                self.send_event('E_HIDE_MODEL')
            target = EntityManager.getentity(mecha_id)
            if target is None:
                return
            mecha = target.logic
            mecha_type_id = mecha.share_data.ref_mecha_id
            mecha_fashion_id = mecha.ev_g_mecha_fashion_id()
            self._bind_mecha_type = mecha_type_id
            self.switch_to_state_change_ui(True)
            self._pre_process_event(target)
            self._selected_random_mecha_no = 0
            self._del_human_com()
            mecha.send_event('E_ON_JOIN_MECHA')
            self._setup_component(mecha)
            camera_state = get_mecha_camera_type(str(mecha_type_id), mecha_fashion_id)
            self.send_event('E_SET_CONTROL_TARGET', target, {'driver': self.unit_obj.id})
            if not self._get_need_play_join_anim() and not mecha.sd.ref_in_open_aim:
                self.send_event('E_TRY_SWITCH_CAM_STATE', 'E_MECHA_CAMERA', camera_state, force_trans_time=0)
                mecha.send_event('E_RESET_CAMERA_STATE')
            old_need_play_join_anim = self._need_play_join_anim
            self._need_play_join_anim = False
            self.send_event('E_HIDE_SKILL')
            if self.sd.ref_is_avatar:
                global_data.emgr.scene_set_control_drone_event.emit(mecha, False)
                f_yaw = mecha.sd.ref_logic_trans.yaw_target
                f_pitch = 0
                global_data.emgr.set_camera_yaw_pitch_with_slerp_event.emit(f_yaw, f_pitch)
                global_data.emgr.scene_target_changed_event.emit(mecha)
                global_data.emgr.enable_camera_yaw.emit(True)
            else:
                self.check_observe_cam_rotate_recover(mecha)
            mecha.send_event('E_ON_POST_JOIN_MECHA')
            mecha.send_event('E_TRY_DISABLE_MOVE_SYNC')
            if self._is_share_mecha or self.sd.ref_is_avatar:
                mecha.send_event('E_ENABLE_BEHAVIOR')
            if self.sd.ref_is_robot:
                self.send_event('E_COL_CHARACTER_OFF')
                self.send_event('E_HIDE_MODEL')
            self.send_event('E_CLEAR_JOIN_MECHA_ACTION')
            if self.ev_g_is_avatar():
                control_target = self.ev_g_control_target()
                if (self.ev_g_is_avatar() or self.sd.ref_is_agent) and control_target and control_target.logic and control_target.logic.__class__.__name__ == 'LMecha':
                    if not self.ev_g_is_enable_behavior():
                        self.send_event('E_ENABLE_BEHAVIOR')
            return

    def _try_leave_mecha(self, hint_pos=None):
        control_target = self.ev_g_control_target()
        if control_target is None or control_target.logic is None or not control_target.logic.is_valid():
            return
        else:
            check_result = control_target.logic.ev_g_check_off_pos(self.unit_obj.id, hint_pos=hint_pos)
            if not check_result:
                return
            has_block, off_pos = check_result
            if not has_block:
                self.send_event('E_CALL_SYNC_METHOD', 'try_leave_mecha', ((off_pos.x, off_pos.y, off_pos.z), 2), True)
                control_target.logic.send_event('E_LEAVE_MECHA_SENT', True)
            else:
                self.send_event('E_SHOW_MESSAGE', get_text_local_content(18236))
            return

    def _on_leave_mecha_start(self, offpoint, timestamp, is_die, share_mecha):
        self._high_eject = is_die and not self._is_pure_mecha and not self._is_hunter_mecha
        self._is_share_mecha = share_mecha
        control_target = self.ev_g_control_target()
        is_robot_agent = self.sd.ref_is_agent
        control_mecha = control_target and control_target.__class__.__name__ == 'Mecha'
        if is_robot_agent:
            global_data.game_mgr.delay_exec(0.5, lambda : self.send_event('E_ON_LEAVE_MECHA'))
            if not is_die and control_mecha and control_target.logic:
                control_target.logic.send_event('E_ON_LEAVE_MECHA_START')
            return
        if control_mecha:
            if is_die and self.unit_obj is global_data.cam_lplayer:
                if global_data.player.get_setting(uoc.CONF_SHAKE_KEY_PATTERN % uoc.CONF_SHAKE_MECHA_DESTROY):
                    if not global_data.vibrate_mgr:
                        from logic.comsys.vibrate.VibrateMgr import VibrateMgr
                        VibrateMgr()
                    global_data.vibrate_mgr.start_vibrate(DESTROYED_VIBRATE_LV)
            mecha = control_target.logic
            if not mecha:
                return
            delta_time = time_utility.time() - timestamp
            if delta_time >= 2:
                self.send_event('E_ON_LEAVE_MECHA')
                self._recover_human_com()
                return
            if mecha and not mecha.ev_g_death():
                mecha.send_event('E_ROCK_STOP')
                mecha.send_event('E_ON_LEAVE_MECHA_START')
                print('============ SENT LEAVE MECHA START ========================')
            elif not mecha.ev_g_execute():

                def cb(*args):
                    if self and self.is_valid():
                        self.send_event('E_ON_LEAVE_MECHA')

                if self.sd.ref_is_robot:
                    cb()
                else:
                    global_data.game_mgr.delay_exec(1, cb)
                    if self.ev_g_is_cam_target():
                        ui = global_data.ui_mgr.show_ui('MechaWarningUI', 'logic.comsys.mecha_ui')
                        if ui:
                            ui.enter_screen()
            self._recover_human_com()
        elif control_target and control_target.logic and control_target.logic.MASK & preregistered_tags.VEHICLE_TAG_VALUE:
            self._on_leave_mecha_vehicle(offpoint)
        else:
            self._on_leave_mecha()
            if self.ev_g_is_avatar():
                mecha_entity = self._get_bind_mecha_entity()
                if mecha_entity and mecha_entity.logic.ev_g_death():
                    global_data.emgr.camera_cancel_all_trk.emit()
                    global_data.emgr.camera_enable_follow_event.emit(True)
                    self.send_event('E_TO_THIRD_PERSON_CAMERA')
                    global_data.game_mgr.delay_exec(0.5, lambda : self._eject(mecha_entity.logic))
                self._recover_human_com()

    def _on_leave_mecha_vehicle(self, pos):
        if self.ev_g_is_cam_target():
            global_data.game_mgr.scene.recover_vegetation_enable()
        self.ev_g_cancel_state(status_config.ST_MECHA_DRIVER)
        if self.ev_g_get_state(status_config.ST_MECHA_PASSENGER):
            self.ev_g_cancel_state(status_config.ST_MECHA_PASSENGER)
        if self.ev_g_get_state(status_config.ST_VEHICLE_GUNNER):
            self.ev_g_cancel_state(status_config.ST_VEHICLE_GUNNER)
        if self.ev_g_get_state(status_config.ST_VEHICLE_PASSENGER):
            self.ev_g_cancel_state(status_config.ST_VEHICLE_PASSENGER)
        self.send_event('E_ON_STATUS_CHANGED')
        self.send_event('E_CLEAR_ACC_INFO')
        owner = self.unit_obj.get_owner()
        _pos = math3d.vector(*pos)
        ctrl_conf = {'reset_pos': _pos}
        target = self.ev_g_control_target()
        if not (target and target.logic):
            self.send_event('E_SET_CONTROL_TARGET', None, ctrl_conf)
            return
        else:
            target.logic.send_event('E_ON_LEAVE_MECHA')
            target.logic.send_event('E_MOVE_NO_FORCE')
            target.logic.send_event('E_STOP_CONTROL_VEHICLE')
            target.logic.send_event('E_CLEAR_SPEED')
            is_clear_behavior = True
            if target.logic.__class__.__name__ == 'LMotorcycle' and target.logic.sd.ref_driver_id != self.unit_obj.id:
                is_clear_behavior = False
            if is_clear_behavior:
                target.logic.send_event('E_CLEAR_BEHAVIOR')
                target.logic.send_event('E_DISABLE_BEHAVIOR')
            target.logic.send_event('E_LEAVE_MECHA_SENT', False)
            target.logic.send_event('E_ON_ENABLE_AIM_HELPER', False)
            self.send_event('E_SET_CONTROL_TARGET', None, ctrl_conf)
            if self.sd.ref_is_avatar:
                target.logic.send_event('E_UPDATE_LOD', 0)
                target.logic.send_event('E_PLAY_EFFECT_BY_STATUS', vehicle_const.MOVE_STOP)
            self.send_event('E_TO_THIRD_PERSON_CAMERA')
            self.send_event('E_ON_ACTION_LEAVE_VEHICLE')
            com_camera = self.scene.get_com('PartCamera')
            if self.ev_g_is_avatar():
                yaw = com_camera.get_yaw() if 1 else target.logic.ev_g_yaw()
                self.send_event('E_ACTION_SET_YAW', yaw)
                self.send_event('E_ACTION_SYNC_FORCE_YAW', yaw)
                if not self.ev_g_get_state(status_config.ST_SWIM):
                    self.send_event('E_FOOT_POSITION', _pos)
                if target.logic.ev_g_simulate_physics() or target.logic.ev_g_pattern() == mconst.MECHA_PATTERN_VEHICLE:
                    target.logic.send_event('E_VEHICLE_COLLISION_SET', False)
            if self.sd.ref_is_avatar:
                target.logic.send_event('E_CONTROL_MECHA_TWO', False)
                global_data.player.logic.send_event('E_ENABLE_WATER_UPDATE', True)
                from ...cdata import jump_physic_config
                gravity = jump_physic_config.gravity * NEOX_UNIT_SCALE
                self.send_event('E_GRAVITY', gravity)
                self.send_event('E_UNLIMIT_LOWER_HEIGHT')
                global_data.mecha = None

                def force_on_ground():
                    if self and self.is_valid() and self.sd.ref_character:
                        self.send_event('E_FORCE_ON_GROUND', 1, True)

                global_data.game_mgr.delay_exec(0.1, force_on_ground)
            return

    def _on_leave_mecha(self):
        if self.ev_g_is_cam_target():
            global_data.game_mgr.scene.recover_vegetation_enable()
        self._ctrl_mecha_id = None
        self.send_event('E_FIGHT_STATE_CHANGED', False)
        self.send_event('E_CLEAR_ACC_INFO')
        self.send_event('E_SHOW_MODEL')
        if self._is_share_mecha:
            self._bind_mecha_id = self._fixed_mecha_id
        if self.ev_g_death():
            return
        else:
            if not self.ev_g_in_mecha('Mecha') and self.ev_g_is_avatar():
                global_data.emgr.enable_camera_yaw.emit(True)
                self.ev_g_cancel_state(status_config.ST_MECHA_BOARDING, sync=True)
                if not global_data.ex_scene_mgr_agent.check_settle_scene_active():
                    global_data.ui_mgr.show_ui('StateChangeUI', 'logic.comsys.battle')
                    return
                self.send_event('E_FIGHT_STATE_CHANGED', False)
                return
            mecha = None
            control_target = self.ev_g_control_target()
            leave_mecha_in_ball = False
            is_diving = False
            water_height = 0
            if control_target and control_target.__class__.__name__ == 'Mecha':
                mecha = control_target.logic
                if mecha and mecha.is_valid():
                    is_diving = mecha.ev_g_is_diving()
                    water_height = mecha.ev_g_water_height() or 0
                    self._init_hp[0] = mecha.share_data.ref_hp
                    self._init_hp[1] = mecha.share_data.ref_max_hp
                    self._init_hp[2] = mecha.ev_g_shield()
                    self._init_hp[3] = mecha.ev_g_max_shield()
                    leave_mecha_in_ball = mecha.ev_g_leave_mecha_in_ball()
                    mecha.send_event('E_DISABLE_BEHAVIOR')
                    mecha.send_event('E_ON_LEAVE_MECHA')
                    self._del_component(mecha)
            from ...common_const.collision_const import MECHA_STAND_HEIGHT
            human_pos = self.ev_g_position()
            arg = {}
            if human_pos:
                offset_y = 1 if leave_mecha_in_ball else MECHA_STAND_HEIGHT / 3
                off_pos = math3d.vector(human_pos.x, human_pos.y + offset_y, human_pos.z)
                if is_diving:
                    chect_begin = human_pos
                    check_end = math3d.vector(off_pos)
                    check_end.y = water_height
                    col_model_obj_list = []
                    filter_col_ids = self.ev_g_human_col_id()
                    group = GROUP_STATIC_SHOOTUNIT
                    mask = -1
                    is_hit = character_ctrl_utils.hit_by_scene_collision(chect_begin, check_end, group, mask, filter_col_ids=filter_col_ids, col_model_obj_list=col_model_obj_list)
                    if is_hit:
                        off_pos = human_pos
                owner = self.unit_obj.get_owner()
                arg = {'reset_pos': off_pos}
                if self.sd.ref_is_robot and self._high_eject:
                    import logic.gcommon.common_utils.parachute_utils as putil
                    arg['parachute_stage'] = putil.STAGE_PARACHUTE_DROP
                    arg['use_phys'] = 0
                elif self.sd.ref_is_robot:
                    arg['is_agent'] = 1 if self.sd.ref_is_agent else 0
            self._simulate_fall(mecha)
            model = self.ev_g_model()
            if model and model.valid:
                model.remove_from_parent()
                if MODEL_SHADER_CTRL_SET_ENABLE:
                    model.set_inherit_parent_shaderctrl(True)
                self.scene.add_object(model)
            arg['leave_mecha'] = True
            self.send_event('E_SET_CONTROL_TARGET', None, arg)
            if not self.is_unit_obj_type('LPuppet') and not self.is_unit_obj_type('LPuppetRobot'):
                model = self.ev_g_model()
                if model and model.valid:
                    model.visible = False
            owner = self.unit_obj.get_owner()
            self.send_event('E_TO_THIRD_PERSON_CAMERA')
            if owner and owner.__class__.__name__ == 'Avatar':
                self._switch_to_mecha_ui(False, control_target)
                global_data.emgr.scene_set_control_drone_event.emit(global_data.player.logic, False)
                global_data.emgr.scene_target_changed_event.emit(global_data.player.logic)
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_MODEL, ()], True)
            if self._is_share_mecha:
                self._bind_mecha_type = self._fixed_mecha_type
            if self.ev_g_is_cam_target():
                global_data.emgr.scene_show_small_map_event.emit(False)
            self.send_event('E_RECOVER_SKILL')
            self._eject(mecha)
            if self.sd.ref_is_robot:
                self.send_event('E_COL_CHARACTER_ON')
            self.rechoose_mecha()
            if self._get_is_pure_mecha():
                self.send_event('E_HIDE_MODEL')
                self.send_event('E_FORCE_DEACTIVE')
            return

    def _switch_to_mecha_ui(self, mecha_ui=True, mecha_target=None):
        if global_data.ex_scene_mgr_agent.check_settle_scene_active():
            return
        else:
            ui_conf = confmgr.get('mecha_conf', 'UIConfig', 'Content')
            mecha_id = str(self._bind_mecha_type)
            if mecha_id not in ui_conf:
                return
            self.mecha_ui_list = [
             'MechaControlMain', 'MechaFuelUI', 'MechaHpInfoUI', 'MechaCockpitUI']
            pre_load_ui_list = copy.copy(self.mecha_ui_list)
            if self._is_share_mecha or mecha_target and mecha_target.is_share():
                self._refresh_share_ui(not mecha_ui)
            ui_info = ui_conf[mecha_id]
            self.mecha_ui_list.extend(ui_info['append_ui'])
            if mecha_ui and not self._mecha_ui:
                global_data.mecha = mecha_target
                if mecha_target:
                    skin_and_shiny_weapon = mecha_target.logic.ev_g_mecha_skin_and_shiny_weapon_id()
                    ui_change_conf = confmgr.get('mecha_ui_change_config', str(skin_and_shiny_weapon[0]), default=None)
                    if ui_change_conf is not None:
                        if str(skin_and_shiny_weapon[1]) in ui_change_conf:
                            ui_dict = ui_change_conf[str(skin_and_shiny_weapon[1])]
                            for idx, ui in enumerate(self.mecha_ui_list):
                                if ui in ui_dict:
                                    self.mecha_ui_list[idx] = ui_dict[ui]

                        elif 'common' in ui_change_conf:
                            ui_dict = ui_change_conf['common']
                            for idx, ui in enumerate(self.mecha_ui_list):
                                if ui in ui_dict:
                                    self.mecha_ui_list[idx] = ui_dict[ui]

                self.mecha_ui_load_list = copy.copy(self.mecha_ui_list)
                self._mecha_ui = True
                self.need_update = True
            elif not mecha_ui:
                if mecha_target:
                    skin_and_shiny_weapon = mecha_target.logic.ev_g_mecha_skin_and_shiny_weapon_id()
                    ui_change_conf = confmgr.get('mecha_ui_change_config', str(skin_and_shiny_weapon[0]), default=None)
                    if ui_change_conf is not None:
                        if str(skin_and_shiny_weapon[1]) in ui_change_conf:
                            ui_dict = ui_change_conf[str(skin_and_shiny_weapon[1])]
                            for idx, ui in enumerate(self.mecha_ui_list):
                                if ui in ui_dict:
                                    self.mecha_ui_list[idx] = ui_dict[ui]

                        elif 'common' in ui_change_conf:
                            ui_dict = ui_change_conf['common']
                            for idx, ui in enumerate(self.mecha_ui_list):
                                if ui in ui_dict:
                                    self.mecha_ui_list[idx] = ui_dict[ui]

                for ui_name in self.mecha_ui_list:
                    ui = global_data.ui_mgr.get_ui(ui_name)
                    if ui and hasattr(ui, 'disappear'):
                        ui.disappear()
                    elif ui and ui_name in pre_load_ui_list:
                        ui.leave_screen()
                    else:
                        global_data.ui_mgr.close_ui(ui_name)

                global_data.mecha = None
                self._mecha_ui = False
                self.need_update = False
            return

    def tick(self, delta):
        if len(self.mecha_ui_load_list) > 0:
            ui_name = self.mecha_ui_load_list[0]
            self.mecha_ui_load_list.pop(0)
            ui = global_data.ui_mgr.get_ui(ui_name)
            if ui:
                ui.leave_screen()
                ui.enter_screen()
            else:
                ui = global_data.ui_mgr.show_ui(ui_name, 'logic.comsys.mecha_ui')
                if global_data.player and global_data.player.in_local_battle():
                    if ui:
                        ui.enter_screen()
            lmecha = global_data.mecha.logic
            if lmecha:
                if hasattr(ui, 'on_mecha_setted'):
                    ui.on_mecha_setted(lmecha)
                from logic.gcommon.cdata.mecha_status_config import MC_TRANSFORM
                behavior = lmecha.ev_g_behavior_config()
                if behavior:
                    dynamic_ui_list = behavior.get(MC_TRANSFORM, {}).get('custom_param', {}).get('dynamic_ui_dict', {})
                    for action, visible in six.iteritems(dynamic_ui_list):
                        lmecha.send_event('E_SET_ACTION_VISIBLE', action, visible)

        else:
            self.need_update = False
            self.water_hide_filter()

    def water_hide_filter(self):
        lmecha = global_data.mecha.logic
        if not lmecha:
            return
        if not lmecha.ev_g_is_water_depth_over(water_const.H_WATER_MECHA_DIVING):
            return

    def _setup_component(self, mecha):
        owner = self.unit_obj.get_owner()
        if not owner:
            return
        owner_name = owner.__class__.__name__
        mecha.send_event('E_ENABLE_SYNC', owner_name == 'Avatar' or mecha.share_data.ref_is_agent)
        if not self.sd.ref_is_robot:
            com_list = get_on_mecha_utils.get_mecha_component('Avatar')
            self._uninstall_com(mecha, com_list)
            com_list = get_on_mecha_utils.get_mecha_component('Puppet')
            self._uninstall_com(mecha, com_list)
            com_list = get_on_mecha_utils.get_mecha_component(owner_name)
            self._install_com(mecha, com_list)

    def _del_component(self, mecha):
        com_list = get_on_mecha_utils.get_mecha_component('Avatar')
        self._uninstall_com(mecha, com_list)
        com_list = get_on_mecha_utils.get_mecha_component('Puppet')
        self._uninstall_com(mecha, com_list)

    def _simulate_fall(self, mecha):
        if not mecha or not mecha.is_valid():
            return
        com = mecha.get_com('ComCharacter')
        if not com:
            com = mecha.add_com('ComCharacter', 'client')
            com.init_from_dict(mecha, {'leave_mecha': True})
            com.char_ctrl.group = 65520 & ~(GROUP_SHOOTUNIT | GROUP_GRENADE)
            com.char_ctrl.mask = 65520 & ~(GROUP_SHOOTUNIT | GROUP_GRENADE)
            com.char_ctrl.enableForceSync = True
            com.active()
        com = mecha.get_com('ComDriver')
        if not com:
            from logic.gcommon.common_const.collision_const import MECHA_STAND_WIDTH, MECHA_STAND_HEIGHT
            com = mecha.add_com('ComDriver', 'client.com_character_ctrl')
            com.init_from_dict(mecha, {'char_size': (MECHA_STAND_WIDTH * 0.1, MECHA_STAND_HEIGHT * 0.9),'ignore_ongournd_cb': True})
        com = mecha.get_com('ComMechaStaticCollision')
        if not com and self._is_share_mecha:
            com = mecha.add_com('ComMechaStaticCollision', 'client')
            com.init_from_dict(mecha, {'simulate_fall': False})
        mecha.send_event('E_RESET_GRAVITY')

    def _pre_process_event(self, target):
        owner = self.unit_obj.get_owner()
        if owner and owner.__class__.__name__ == 'Avatar':
            self._switch_to_mecha_ui(True, target)
        if self.ev_g_is_cam_target():
            global_data.emgr.scene_show_small_map_event.emit(True)

    def _del_human_com(self):
        owner = self.unit_obj.get_owner()
        if not owner or not owner.logic.is_valid():
            return
        com_list = get_on_mecha_utils.HUMAN_COMPONENT_LIST[owner.__class__.__name__]
        owner = owner.logic
        self._uninstall_com(owner, com_list)

    def _recover_human_com(self):
        owner = self.unit_obj.get_owner()
        if not owner or not owner.logic.is_valid():
            return
        com_list = get_on_mecha_utils.HUMAN_COMPONENT_LIST[owner.__class__.__name__]
        owner = owner.logic
        self._install_com(owner, com_list)
        self.send_event('E_ON_HUMAN_COM_RECOVERED')

    def _install_com(self, owner, com_list):
        complete_list = []
        for com_info in com_list:
            com_name = com_info['component']
            cpath = 'client'
            if com_name.find('.') > 0:
                com_prefix, com_name = com_name.rsplit('.', 1)
                cpath = 'client.{}'.format(com_prefix)
            com = owner.get_com(com_name)
            getter = com or com_info.get('bdict_getter', None)
            if getter:
                bdict = getter(owner) if 1 else {}
                com = owner.add_com(com_name, cpath)
                com.init_from_dict(owner, bdict)
                init_func = com_info.get('init_func', None)
                if init_func:
                    init_func(owner, com)
                complete_list.append(com)

        for com in complete_list:
            com.on_init_complete()

        return

    def _uninstall_com(self, owner, com_list):
        for com_info in com_list:
            com_name = com_info['component']
            if com_name.find('.') > 0:
                _, com_name = com_name.rsplit('.', 1)
            owner.del_com(com_name)

    def _eject(self, mecha):
        self.ev_g_cancel_state(status_config.ST_MECHA_DRIVER)
        if not self.is_unit_obj_type('LAvatar') and not self.sd.ref_is_agent:
            return
        self.send_event('E_DISABLE_MOVE', True)
        self.send_event('E_ROTATE_MODEL_TO_CAMERA_DIR')
        if self._high_eject:
            if not self.sd.ref_is_robot:
                self.send_event('E_EJECT')
        else:
            self.send_event('E_FALL')
            if mecha and mecha.is_valid():
                model = mecha.ev_g_model()
                if model:
                    move_dir = model.rotation_matrix.forward
                    obstacle = mutils.is_leave_mecha_obstacle(model)
                    char_ctrl = self.sd.ref_character
                    return char_ctrl or None
                if obstacle:
                    rate = 0.4 if 1 else 1
                    h_speed = -move_dir * 5 * NEOX_UNIT_SCALE * rate
                    v_speed = 10 * NEOX_UNIT_SCALE * rate
                    self.send_event('E_CHARACTER_WALK', h_speed)
                    char_ctrl.verticalVelocity = v_speed
                    if self.ev_g_is_avatar():
                        rocker_dir = self.sd.ref_rocker_dir
                        if rocker_dir:
                            self.send_event('E_CHANGE_ANIM_MOVE_DIR', rocker_dir.x, rocker_dir.z)

            def resume(*args):
                if self and self.is_valid():
                    self.send_event('E_DISABLE_MOVE', False)

            global_data.game_mgr.delay_exec(1, resume)
        if self.ev_g_agony():
            self.send_event('E_DISABLE_MOVE', False)

    def _get_ctrl_mecha_id(self):
        return self._ctrl_mecha_id

    def _get_ctrl_mecha_obj(self):
        if self._ctrl_mecha_id:
            mecha_entity = EntityManager.getentity(self._ctrl_mecha_id)
            return mecha_entity
        else:
            return None

    def _get_recall_times(self):
        return self._recall_times

    def on_update_change_cd(self, cd_type, total_cd, left_time):
        self._recall_cd_type = cd_type
        self._recall_cd = total_cd
        self._recall_left_time = left_time
        self._recall_cd_end_timestamp = time_utility.get_server_time() + self._recall_left_time

    def set_recall_cd_type(self, cd_type):
        self._recall_cd_type = cd_type

    def check_observe_cam_rotate_recover(self, mecha):
        if self.ev_g_is_cam_target():
            if not self._get_need_play_join_anim():
                f_yaw = mecha.ev_g_attr_get('human_yaw', 0)
                if f_yaw is not None:
                    global_data.emgr.fireEvent('camera_set_yaw_event', f_yaw)
                f_pitch = mecha.ev_g_attr_get('head_pitch', 0)
                if f_pitch is not None:
                    global_data.emgr.fireEvent('camera_set_pitch_event', f_pitch)
                    mecha.send_event('E_CAM_PITCH', f_pitch)
            recorded_cam_state = self.ev_g_cam_state()
            from logic.client.const.camera_const import AIM_MODE
            if recorded_cam_state == AIM_MODE:
                return
            if recorded_cam_state:
                self.send_event('E_TRY_SWITCH_CAM_STATE', 'E_MECHA_CAMERA', recorded_cam_state)
        return

    def on_is_ctrl_share_mecha(self):
        return self._is_share_mecha

    def _select_random_mecha(self, mecha_no):
        self._selected_random_mecha_no = mecha_no
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_ON_SELECT_RANDOM_MECHA')

    def _get_selected_random_mecha(self):
        return self._selected_random_mecha_no

    def _get_is_first_calling(self):
        return self._is_first_calling

    def _set_is_first_calling(self, ret):
        self._is_first_calling = ret

    def _get_is_first_joining_vehicle_mecha(self):
        return self._is_first_joining_vehicle_mecha

    def _set_is_first_joining_vehicle_mecha(self, ret):
        self._is_first_joining_vehicle_mecha = ret

    def _trans_create_mecha_to_share(self):
        mecha = EntityManager().getentity(self._fixed_mecha_id)
        if mecha:
            mecha.trans_to_share()
        self._fixed_mecha_id = None
        self._is_share_mecha = True
        self._has_trans_created_to_share = True
        return

    @execute_by_mode(True, (game_mode_const.GAME_MODE_SURVIVALS,))
    def _on_revive(self, *arg):
        if self.ev_g_is_avatar():
            if self._fixed_mecha_id:
                self.switch_to_state_change_ui(mecha_state=False)
            self._refresh_stage()

    def _enter_states(self, new_state):
        if not self.ev_g_status_check_pass(status_config.ST_MECHA_BOARDING):
            self.cancel_join_share_mecha()

    def _get_enable_mecha_redress(self):
        return self._enable_mecha_redress