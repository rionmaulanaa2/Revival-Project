# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartCtrl.py
from __future__ import absolute_import
from __future__ import print_function
import six
from . import ScenePart
from data.camera_state_const import FREE_MODEL, AIM_MODE, OBSERVE_FREE_MODE, DEBUG_MODE, RIGHT_AIM_MODE, JUDGE_MODE
from logic.client.const import camera_const
from logic.client.const.camera_const import FREE_CAMERA_LIST
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.common_utils import parachute_utils
from mobile.common.EntityManager import EntityManager
from common.utils.cocos_utils import cocos_pos_to_neox
from logic.gutils import map_utils
import cc
import math
import math3d
from logic.gutils.camera_utils import get_touch_target
from logic.gcommon import const
from logic.gcommon.time_utility import time
import logic.vscene.parts.ctrl.GamePyHook as game_hook
from logic.gcommon.common_const import weapon_const
import game3d
from logic.gutils import mecha_utils
from logic.gutils.client_unit_tag_utils import preregistered_tags
from logic.client.const import game_mode_const
from copy import deepcopy
from logic.gcommon.behavior.StateBase import clamp
from logic.gcommon.time_utility import get_server_time
from common.utils.pc_platform_utils import is_pc_control
TWO_PI = 2 * math.pi
ROTATE_IGNORE_MODE = frozenset([OBSERVE_FREE_MODE, JUDGE_MODE])
CAM_ROTATION_CLAMP_ENABLED = False
MAX_CAM_ROTATION_DELTA_VALUE_PER_SECOND = 0.01
LAST_ROTATION_CLAMP_TIME = -1

def enable_clamp_cam_rotation(enabled, max_delta_val_under_30_frame=0.01):
    global LAST_ROTATION_CLAMP_TIME
    global CAM_ROTATION_CLAMP_ENABLED
    global MAX_CAM_ROTATION_DELTA_VALUE_PER_SECOND
    CAM_ROTATION_CLAMP_ENABLED = enabled
    MAX_CAM_ROTATION_DELTA_VALUE_PER_SECOND = max_delta_val_under_30_frame * 30
    LAST_ROTATION_CLAMP_TIME = -1


class PartCtrl(ScenePart.ScenePart):
    ENTER_EVENT = {'scene_player_setted_event': 'on_player_setted',
       'camera_switch_to_state_event': 'on_camera_switch_to_state',
       'sst_common_changed_event': 'on_sst_common_changed',
       'camera_on_acc_input_update': 'on_acc_input_update',
       'touch_pixel_rotate_camera_event': 'on_touch_rotate_camera',
       'settle_stage_event': 'show_settle_stage_ui',
       'app_lost_focus_event': 'on_app_lost_focus',
       'scene_camera_player_setted_event': 'on_camera_target_setted',
       'on_observer_parachute_stage_changed': '_on_observer_parachute_stage_changed',
       'enable_camera_yaw': 'enable_rotate_camera',
       'net_reconnect_event': 'on_reconnect',
       'scene_camera_target_setted_event': 'on_camera_targetted_setted',
       'scene_observed_player_setted_event': '_on_scene_observed_player_setted_event',
       'mecha_sens_val_changed': '_on_mecha_sens_val_changed',
       'player_user_setting_changed_event': '_on_player_user_setting_changed',
       'double_click_mark_change_event': 'on_double_click_mark_changed'
       }

    def __init__(self, scene, name):
        super(PartCtrl, self).__init__(scene, name)
        self.cur_camera_state_type = None
        self.sst_setting_map = {}
        self.player = None
        global_data.ctrl_target_id = 0
        self._enable_slide_helper = False
        self._enable_adapt_scope_times = False
        self._enable_double_click_mark = False
        self.init_config_data()
        self.sensor_modify = 1.0
        self.init_keys()
        self._enable_rotate_camera = True
        self.key_ctrls = []
        self.update_count_in_one_frame = 0
        self.dx_frame = 0
        self.dy_frame = 0
        self.need_update = True
        self.com_camera = None
        self._prev_touch_list = []
        self._max_touch_list_length = 10
        self._cur_mecha_type_id = None
        self._cur_mecha_screen_sens_val = None
        self._cur_mecha_screen_scoped_sens_val = None
        self._cur_mecha_screen_sp_form_sens_val = None
        self.shoot_mecha_action = ['action1', 'action2', 'action4']
        self.touching_scene = False
        self.clamp_cam_rotation_enabled = False
        self.max_cam_rotation_delta_value = 0.01
        return

    def on_update(self, *args):
        pass

    def rotate_player_camera(self, dx, dy):
        global LAST_ROTATION_CLAMP_TIME
        if abs(dx) > TWO_PI:
            dx %= TWO_PI
        if abs(dy) > TWO_PI:
            dy %= TWO_PI
        player = global_data.cam_lplayer
        if player:
            if player.ev_g_death() or player.ev_g_defeated() or player.ev_g_is_pure_mecha() and not player.ev_g_get_bind_mecha():
                return
            if not global_data.battle.is_in_island() and player.share_data.ref_parachute_stage is not None and player.share_data.ref_parachute_stage & parachute_utils.BAN_ROTATE_CAMERA_STAGE:
                return
            cur_state = self.com_camera.get_cur_camera_state_type()
            if cur_state not in ROTATE_IGNORE_MODE and not player.ev_g_is_avatar():
                return
            if CAM_ROTATION_CLAMP_ENABLED:
                if LAST_ROTATION_CLAMP_TIME < 0:
                    max_delta_value = MAX_CAM_ROTATION_DELTA_VALUE_PER_SECOND / game3d.get_frame_rate()
                else:
                    max_delta_value = MAX_CAM_ROTATION_DELTA_VALUE_PER_SECOND * (global_data.game_time - LAST_ROTATION_CLAMP_TIME)
                LAST_ROTATION_CLAMP_TIME = global_data.game_time
                dx = clamp(dx, -max_delta_value, max_delta_value)
                dy = clamp(dy, -max_delta_value, max_delta_value)
            yaw_res = self.com_camera.yaw(dx)
            pitch_res = self.com_camera.pitch(dy * -1)
            if cur_state not in FREE_CAMERA_LIST and cur_state not in ROTATE_IGNORE_MODE:
                if yaw_res:
                    player.send_event('E_DELTA_YAW', yaw_res)
                if pitch_res:
                    player.send_event('E_DELTA_PITCH', pitch_res)
        return

    def _on_player_user_setting_changed(self, *args):
        if not is_pc_control() and global_data.player:
            self._enable_slide_helper = str(global_data.player.get_setting_2(uoc.SST_AUTO_HELP_KEY)) == str(True)
        if global_data.player:
            self._enable_adapt_scope_times = str(global_data.player.get_setting_2(uoc.SST_ADAPT_MAGNIFICATION)) == str(True)

    def init_config_data(self):
        from common.cfg import confmgr
        adjust_conf = confmgr.get('slide_adjust_conf')
        self.set_ctrl_adjust_val_from_config(adjust_conf)
        self._on_player_user_setting_changed()

    def set_ctrl_adjust_val_from_config(self, adjust_conf):
        self.adjust_touch_interval = adjust_conf['SLIDE_ADJUST_INTERVAL']
        self.min_adjust_touch_ratio_low_bound = adjust_conf.get('MIN_ADJUST_RATIO_LOW_BOUND', 0.1)
        self.min_adjust_touch_ratio_high_bound = adjust_conf.get('MIN_ADJUST_RATIO_HIGH_BOUND', 0.6)
        self.max_adjust_touch_ratio_low_bound = adjust_conf.get('MAX_ADJUST_RATIO_LOW_BOUND', 1.5)
        self.max_adjust_touch_ratio_high_bound = adjust_conf.get('MAX_ADJUST_RATIO_HIGH_BOUND', 2.5)
        self.min_adjust_distance_threshold = adjust_conf.get('MIN_ADJUST_DISTANCE_THRESHOLD', 40)
        self.max_adjust_distance_threshold = adjust_conf.get('MAX_ADJUST_DISTANCE_THRESHOLD', 400)

    def test_set_adjust_val(self, a, b, c, d, e, f, g):
        adjust_conf = {'SLIDE_ADJUST_INTERVAL': a,
           'MIN_ADJUST_RATIO_LOW_BOUND': b,
           'MIN_ADJUST_RATIO_HIGH_BOUND': c,
           'MAX_ADJUST_RATIO_LOW_BOUND': d,
           'MAX_ADJUST_RATIO_HIGH_BOUND': e,
           'MIN_ADJUST_DISTANCE_THRESHOLD': f,
           'MAX_ADJUST_DISTANCE_THRESHOLD': g
           }
        self.set_ctrl_adjust_val_from_config(adjust_conf)

    def init_keys(self):
        import game
        self._down_reg_keys = [
         game.VK_W, game.VK_S, game.VK_A, game.VK_D, game.VK_G, game.VK_R,
         game.VK_F, game.VK_M, game.VK_N, game.VK_LEFT,
         game.VK_RIGHT, game.VK_UP, game.VK_DOWN, game.VK_1, game.VK_2, game.VK_SHIFT,
         game.VK_ALT, game.VK_Q, game.VK_B, game.VK_X, game.VK_J, game.VK_K, game.VK_T, game.VK_Z, game.VK_F9]
        self._up_reg_keys = [
         game.VK_W, game.VK_S, game.VK_A, game.VK_D,
         game.VK_G, game.VK_R, game.VK_SHIFT, game.VK_ALT, game.VK_Q, game.VK_B, game.VK_SPACE, game.VK_X, game.VK_J,
         game.VK_K, game.VK_T, game.VK_Z, game.VK_F9]

    def on_enter(self):
        self.com_camera = self.scene().get_com('PartCamera')
        self.create_ui()
        self.register_keys()
        self.init_events()

    def on_exit(self):
        self.on_player_setted(None)
        self.destroy_ui()
        self.unregister_keys()
        self.key_ctrls = []
        return

    def _on_observer_parachute_stage_changed(self, stage):
        self._update_related_uis_visibiity(stage)
        if stage == parachute_utils.STAGE_LAND and global_data.sound_mgr._cur_music_name == 'flight':
            global_data.sound_mgr.play_music('stop')

    def _update_related_uis_visibiity(self, stage):
        observer_unit = global_data.cam_lplayer
        is_island = global_data.battle.is_in_island()
        is_prepare = observer_unit and observer_unit.ev_g_is_parachute_prepare()
        is_flying = observer_unit and observer_unit.ev_g_in_carrier_or_plane()
        is_in_land = observer_unit and observer_unit.ev_g_is_parachute_stage_land()
        is_in_battle = observer_unit and observer_unit.ev_g_is_parachute_battle_land()
        is_ready_battle = observer_unit and observer_unit.ev_g_is_parachute_ready_battle()
        is_hide_wp_bar = observer_unit and parachute_utils.is_hide_weapon_bar(observer_unit.sd.ref_parachute_stage, observer_unit.sd.ref_has_first_land)
        self.show_parachute_info_ui(parachute_utils.is_parachuting(stage))
        from logic.gutils.template_utils import set_ui_list_visible_helper
        if is_island:
            island_hide_ui_list = ['FireRockerUI', 'FightLeftShotUI', 'ThrowRockerUI', 'FrontSightUI', 'BulletReloadUI',
             'BattleBuffUI', 'MechaUI', 'WeaponBarSelectUI', 'WeaponBarSelectUIPC', 'BattleFightCapacity', 'FightBagUI',
             'TeamBloodUI', 'BattleFightMeow']
            set_ui_list_visible_helper(island_hide_ui_list, False, 'PARACHUTE')
            island_show_ui_list = ['MoveRockerUI', 'PostureControlUI', 'BattleControlUIPC']
            set_ui_list_visible_helper(island_show_ui_list, True, 'PARACHUTE')
        else:
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
                survival_show_ui_list = [
                 'FightBagUI', 'TeamBloodUI']
                set_ui_list_visible_helper(survival_show_ui_list, True, 'PARACHUTE')
            battle_ui_list = ['FireRockerUI', 'FightLeftShotUI', 'ThrowRockerUI', 'SceneInteractionUI', 'FrontSightUI', 'BulletReloadUI']
            set_ui_list_visible_helper(battle_ui_list, is_in_battle or is_ready_battle, 'PARACHUTE')
            set_ui_list_visible_helper([
             'PostureControlUI', 'BattleControlUIPC', 'BattleBuffUI', 'MechaUI',
             'WeaponBarSelectUIPC', 'BattleFightCapacity', 'RogueGiftTopRightUI', 'BattleFightMeow'], is_in_land or is_ready_battle, 'PARACHUTE')
            set_ui_list_visible_helper(['WeaponBarSelectUI'], is_hide_wp_bar or is_ready_battle, 'PARACHUTE')

    def on_pre_load(self):
        module_path = 'logic.comsys.control_ui'
        module_path_2 = 'logic.comsys.battle'
        self._part_ui_list = (
         (
          True, 'AimRockerUI', module_path, ()),
         (
          True, 'SceneInteractionUI', module_path, ()),
         (
          True, 'ThrowRockerUI', module_path, ()),
         (
          True, 'FrontSightUI', module_path_2, ()),
         (
          True, 'BulletReloadProgressUI', module_path_2, ()),
         (
          True, 'FightReadyTipsUI', module_path_2, ()),
         (
          True, 'MechaModuleEffectiveUI', 'logic.comsys.mecha_ui', ()))
        if not global_data.is_32bit:
            self._part_ui_list += (
             (
              False, 'ParachuteInfoUI', 'logic.comsys.parachute_ui', ()),)
        if not global_data.is_pc_mode:
            self._part_ui_list += (
             (
              True, 'PostureControlUI', module_path, ()),
             (
              True, 'BulletReloadUI', module_path_2, ()),
             (
              True, 'FireRockerUI', module_path, ()),
             (
              True, 'FightLeftShotUI', module_path, ()),
             (
              True, 'MoveRockerUI', module_path, ()),
             (
              True, 'MechaTransMoveHelperUI', module_path, ()))
        else:
            self._part_ui_list += (
             (
              True, 'BattleControlUIPC', module_path, ()),)
        self.add_to_loading_wrapper()

    def on_load(self):
        self.on_create_part_ui()

    def show_parachute_info_ui(self, visible):
        from logic.gutils import judge_utils
        if judge_utils.is_ob():
            return
        if global_data.ex_scene_mgr_agent and global_data.ex_scene_mgr_agent.check_settle_scene_active():
            return
        ui = global_data.ui_mgr.show_ui('ParachuteInfoUI', 'logic.comsys.parachute_ui')
        if not ui:
            return
        if visible:
            ui.enter_screen()
        else:
            ui.leave_screen()

    def create_ui(self):
        pass

    def destroy_ui(self):
        self.on_destroy_part_ui()
        global_data.ui_mgr.close_ui('DriveUI')
        global_data.ui_mgr.close_ui('HidingUI')
        global_data.ui_mgr.close_ui('AttachableDriveUI')
        global_data.ui_mgr.close_ui('AirshipDriveUI')
        global_data.ui_mgr.close_ui('MechaTransUI')
        global_data.ui_mgr.close_ui('MechaCancelUI')
        global_data.ui_mgr.close_ui('HumanCancelUI')
        global_data.ui_mgr.close_ui('MechaTransMoveHelperUI')

    def init_events(self):
        self.cur_aim_lens = None
        import world
        scn = world.get_active_scene()
        player = scn.get_player()
        if player:
            self.on_player_setted(player)
        return

    def on_reconnect(self, *args):
        self.enable_rotate_camera(True)

    def enable_rotate_camera(self, enable):
        self._enable_rotate_camera = enable

    def on_player_setted(self, player):
        self.setup_control_target_event(self.player, False)
        self.player = player
        if player:
            self.init_sst_setting_map()
            self.setup_control_target_event(player, True)
            self.update_control_target_status(player)
            self.on_double_click_mark_changed()

    def init_sst_setting_map(self):
        if global_data.player:
            self.sst_setting_map = {}
            sst_ket_list = [
             uoc.SST_SCR_KEY, uoc.SST_AIM_RD_KEY, uoc.SST_AIM_2M_KEY, uoc.SST_AIM_4M_KEY, uoc.SST_AIM_6M_KEY,
             uoc.SST_MECHA_07_KEY, uoc.SST_FROCKER_KEY]
            for key in sst_ket_list:
                setting = list(global_data.player.get_setting(key))
                base_value = setting[uoc.SST_IDX_BASE]
                if math.isnan(base_value) or math.isinf(base_value):
                    default_value = global_data.player.get_default_setting(key)
                    global_data.player.write_setting_2(key, default_value, True)
                    base_value = default_value[uoc.SST_IDX_BASE]
                    setting[uoc.SST_IDX_BASE] = base_value
                self.sst_setting_map[key] = setting

    def on_acc_input_update(self, dx, dy):
        self.rotate_camera(dx, dy, True, camera_const.CAM_ROT_INPUT_SRC_SENSOR)

    def rotate_camera(self, dx, dy, global_delta=True, input_src=camera_const.CAM_ROT_INPUT_SRC_SLIDE, force=False, ignore_aim_ratio=False):
        if not self._enable_rotate_camera and not force:
            return
        else:
            player = global_data.cam_lplayer
            if player is None:
                return
            modify_ratio = 1.0
            if not ignore_aim_ratio and player and input_src != camera_const.CAM_ROT_INPUT_SRC_LOOK_AT:
                modify_ratio = player.sd.ref_modify_ratio or 1.0
                control_target = player.ev_g_control_target()
                if player.ev_g_is_in_mecha() and control_target.logic:
                    modify_ratio *= control_target.logic.sd.ref_modify_ratio or 1.0
            dx *= modify_ratio
            dy *= modify_ratio
            self.rotate_player_camera(dx, dy)
            return

    def puppet_rotate_camera(self, dx, dy):
        two_pi = 2 * math.pi
        if abs(dx) > two_pi:
            dx %= two_pi
        if abs(dy) > two_pi:
            dy %= two_pi
        scn = self.scene()
        com_camera = scn.get_com('PartCamera')
        com_camera.yaw(dx)
        com_camera.pitch(dy * -1)

    def judge_rotate_camera(self, dx, dy):
        self.puppet_rotate_camera(dx, dy)

    def is_human_fire(self):
        player = global_data.player
        if not player:
            return False
        lplayer = global_data.player.logic
        return lplayer and lplayer.ev_g_is_keep_down_fire()

    def is_mecha_fire(self):
        mecha = global_data.mecha
        if not (mecha and mecha.logic):
            return (False, ())
        else:
            mecha_id = mecha.logic.share_data.ref_mecha_id
            action_id_to_setting_key = {'action1': uoc.SST_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY,
               'action2': uoc.SST_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY,
               'action4': uoc.SST_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY
               }
            action_id_to_as_screen_and_value_keys = {'action1': (
                         uoc.SST_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY, uoc.SST_MAIN_WEAPON_STICK_MECHA_VAL_KEY),
               'action2': (
                         uoc.SST_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY, uoc.SST_MAIN_WEAPON_STICK_MECHA_VAL_KEY),
               'action4': (
                         uoc.SST_SUB_WEAPON_ROCKER_AS_SCREEN_KEY, uoc.SST_SUB_WEAPON_STICK_MECHA_VAL_KEY)
               }
            shoot_stick_switch_val = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SHOOT_STICK_SWITCH_MECHA_VAL_KEY)
            if not shoot_stick_switch_val:
                for key in six.iterkeys(action_id_to_setting_key):
                    action_id_to_setting_key[key] = None

            if self.cur_camera_state_type == AIM_MODE:
                if not mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SCOPE_SAME_AS_NORMAL_KEY):
                    if self._scope_main_weapon_sensitivity_opened:
                        key = uoc.SST_SCOPE_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY
                        action_id_to_setting_key['action1'] = key
                        action_id_to_setting_key['action2'] = key
                        keys = (uoc.SST_SCOPE_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY, uoc.SST_SCOPE_MAIN_WEAPON_STICK_MECHA_VAL_KEY)
                        action_id_to_as_screen_and_value_keys['action1'] = keys
                        action_id_to_as_screen_and_value_keys['action2'] = keys
                    if self._scope_sub_weapon_sensitivity_opened:
                        action_id_to_setting_key['action4'] = uoc.SST_SCOPE_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY
                        action_id_to_as_screen_and_value_keys['action4'] = (
                         uoc.SST_SCOPE_SUB_WEAPON_ROCKER_AS_SCREEN_KEY, uoc.SST_SCOPE_SUB_WEAPON_STICK_MECHA_VAL_KEY)
            elif global_data.mecha.logic.sd.ref_use_mecha_special_form_sensitivity:
                if not mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SPECIAL_FORM_SAME_AS_NORMAL_KEY):
                    if self._special_form_main_weapon_sensitivity_opened:
                        key = uoc.SST_SPECIAL_FORM_MAIN_WEAPON_STICK_SWITCH_MECHA_VAL_KEY
                        action_id_to_setting_key['action1'] = key
                        action_id_to_setting_key['action2'] = key
                        keys = (uoc.SST_SPECIAL_FORM_MAIN_WEAPON_ROCKER_AS_SCREEN_KEY, uoc.SST_SPECIAL_FORM_MAIN_WEAPON_STICK_MECHA_VAL_KEY)
                        action_id_to_as_screen_and_value_keys['action1'] = keys
                        action_id_to_as_screen_and_value_keys['action2'] = keys
                    if self._special_form_sub_weapon_sensitivity_opened:
                        action_id_to_setting_key['action4'] = uoc.SST_SPECIAL_FORM_SUB_WEAPON_STICK_SWITCH_MECHA_VAL_KEY
                        action_id_to_as_screen_and_value_keys['action4'] = (
                         uoc.SST_SPECIAL_FORM_SUB_WEAPON_ROCKER_AS_SCREEN_KEY, uoc.SST_SPECIAL_FORM_SUB_WEAPON_STICK_MECHA_VAL_KEY)
            for action_id, setting_key in six.iteritems(action_id_to_setting_key):
                if setting_key and mecha.logic.ev_g_is_action_down(action_id):
                    return (mecha_utils.get_mecha_sens_setting_val(mecha_id, setting_key), action_id_to_as_screen_and_value_keys[action_id])

            return (
             False, ())

    def is_aiming(self):
        if not self._cur_mecha_type_id:
            return self.cur_camera_state_type in (AIM_MODE, RIGHT_AIM_MODE)
        return self.cur_camera_state_type == RIGHT_AIM_MODE

    def modify_rocker_slide_sensitivity(self, x_delta, y_delta, touch_pos, kwargs):
        if self.is_aiming():
            return (x_delta, y_delta, False)
        else:
            mecha_fire, as_screen_and_value_keys = self.is_mecha_fire()
            if mecha_fire and kwargs.get('as_screen', False):
                return (x_delta, y_delta, False)
            if not (self.is_human_fire() or mecha_fire):
                return (x_delta, y_delta, False)
            if mecha_fire and kwargs.get('setting', None) is None:
                kwargs['setting'] = list(global_data.player.logic.get_owner().get_setting(uoc.SST_FROCKER_KEY))
            if mecha_fire and kwargs.get('base_val', None) is None:
                as_screen_key, sens_value_key = as_screen_and_value_keys
                mecha_id = global_data.mecha.logic.share_data.ref_mecha_id
                as_screen = mecha_utils.get_mecha_sens_setting_val(mecha_id, as_screen_key)
                if as_screen:
                    return (x_delta, y_delta, False)
                kwargs['base_val'] = mecha_utils.get_mecha_sens_setting_val(mecha_id, sens_value_key)
            win_w, win_h = global_data.ui_mgr.slide_screen_size.width, global_data.ui_mgr.slide_screen_size.height
            arg_center = kwargs.get('center_pos', None)
            center_pos = arg_center or math3d.vector2(win_w * 0.5, win_h * 0.5)
            settings = kwargs.get('setting', None) or self.sst_setting_map[uoc.SST_FROCKER_KEY]
            base_val = kwargs.get('base_val', None) or settings[uoc.SST_IDX_BASE]
            x_scale = settings[uoc.SST_IDX_RIGHT] if touch_pos.x >= center_pos.x else settings[uoc.SST_IDX_LEFT]
            x_delta *= base_val * x_scale
            y_scale = settings[uoc.SST_IDX_UP] if touch_pos.y >= center_pos.y else settings[uoc.SST_IDX_DOWN]
            y_delta *= base_val * y_scale
            return (
             x_delta, y_delta, True)

    def on_touch_slide(self, dx, dy, touches, touch_pos, adjust_sensitivity=True, need_check_speed=True, kwargs={}):
        args = deepcopy(kwargs)
        if global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.is_pc_control_enable():
            return
        dx, dy, adjusted = self.modify_rocker_slide_sensitivity(dx, dy, touch_pos, args)
        adjust_sensitivity = adjust_sensitivity or adjusted
        self.on_touch_rotate_camera(dx, dy, touches, touch_pos, adjust_sensitivity, need_check_speed)
        player = global_data.cam_lplayer
        if player:
            player.send_event('E_TOUCH_SLIDE')

    def on_touch_rotate_camera(self, dx, dy, touches, touch_pos, adjust_sensitivity=True, need_check_speed=True):
        t_pos = math3d.vector2(touch_pos.x, touch_pos.y)
        original_dx = dx or 0.0
        original_dy = dy or 0.0
        if adjust_sensitivity:
            dx, dy = self.modify_rotate_dist_by_sensitivity(dx, dy, t_pos)
        ratio = 1.0
        if need_check_speed and self._enable_slide_helper:
            ratio = self.modify_sense_by_dist(original_dx, original_dy, dx, dy, t_pos)
        win_h = global_data.ui_mgr.slide_screen_size.height
        win_w = global_data.ui_mgr.slide_screen_size.width
        dx *= ratio / win_w
        dy *= ratio / win_h
        if not global_data.is_in_judge_camera:
            self.rotate_camera(dx, dy)
        else:
            self.judge_rotate_camera(dx, dy)

    def touch_target_point(self, touches):
        location = touches.getLocation()
        x, y = cocos_pos_to_neox(location.x, location.y)
        from logic.gutils.scene_utils import screen_pos_to_world_pos, get_land_height
        hit_pos = screen_pos_to_world_pos(x, y)
        if hit_pos is None:
            return
        else:
            target = get_touch_target(x, y)
            if target and target.logic.is_valid():
                if target.logic.is_robot():
                    agent_robot = global_data.agent_robot
                    if agent_robot and agent_robot.logic.is_valid():
                        agent_robot.logic.send_event('E_ENABLE_SEE_THROUGHT', False)
                    global_data.agent_robot = target
                    target.logic.send_event('E_ENABLE_SEE_THROUGHT', True)
                if target.logic.is_mecha():
                    agent_mecha = global_data.agent_mecha
                    if agent_mecha and agent_mecha.logic.is_valid():
                        agent_mecha.logic.send_event('E_ENABLE_SEE_THROUGHT', False)
                    global_data.agent_mecha = target
                    target.logic.send_event('E_ENABLE_SEE_THROUGHT', True)
                return
            height = get_land_height(hit_pos.x, hit_pos.z)
            hit_pos.y = height
            global_data.emgr.touch_target_point_event.emit([hit_pos.x, hit_pos.y, hit_pos.z])
            logic = global_data.agent_robot.logic if global_data.agent_robot else None
            if logic:
                logic.send_event('E_CTRL_MOVE_TO', hit_pos)
            logic = global_data.agent_mecha.logic if global_data.agent_mecha else None
            if logic:
                logic.send_event('E_CTRL_MOVE_TO', hit_pos)
            return

    def on_touch_doubletap(self, touches):
        if not self._enable_double_click_mark:
            return
        if global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.is_pc_control_enable():
            return
        ui = global_data.ui_mgr.get_ui('DoubleMarkBlockUI')
        if not ui:
            return
        for node in ui.panel.GetChildren():
            if node.IsPointIn(touches.getLocation()):
                return

        self.mark_touch_item(touches)
        if const.ROBOT_DEBUG:
            self.touch_target_point(touches)

    def mark_touch_item(self, touches):
        if not map_utils.check_can_draw_mark_or_route():
            return
        else:
            from logic.gcommon.common_const.battle_const import MARK_GOTO, MARK_RES, MARK_WAY_DOUBLE_CLICK
            from logic.gutils.scene_utils import screen_pos_to_world_pos
            from logic.gutils import item_utils
            player = self.player
            if not player:
                return
            location = touches.getLocation()
            x, y = cocos_pos_to_neox(location.x, location.y)
            if global_data.feature_mgr.is_support_scene_pick_bounding_box_offset():
                model = self.scene().pick_ex(x, y, 'pickable_item', 1, None, None, math3d.vector(1, 1, 1))[0]
            else:
                model = self.scene().pick(x, y, 'pickable_item', 1)[0]
            hit_pos = None
            extra_args = None
            if model:
                mark_type = MARK_RES
                hit_pos = model.world_position
                entity_ids = global_data.pickable_model_mgr.get_model_entity_id(model)
                if not entity_ids:
                    return
                entity_id = entity_ids[0]
                if entity_id:
                    entity = EntityManager.getentity(entity_id)
                    if entity and entity.logic and bool(entity.logic.ev_g_camp_id()):
                        return
                house_entity_id = None
                if len(entity_ids) > 1:
                    house_entity_id = entity_ids[1]
                _, extra_args = item_utils.get_mark_pick_info(entity_id, house_entity_id=house_entity_id)
            else:
                mark_type = MARK_GOTO
                hit_pos = screen_pos_to_world_pos(x, y)
            map_utils.send_mark_group_msg(mark_type, extra_args)
            if hit_pos:
                player.send_event('E_TRY_DRAW_MAP_MARK', mark_type, hit_pos, extra_args, MARK_WAY_DOUBLE_CLICK)
            else:
                start_pt, dir = self.scene().active_camera.screen_to_world(x, y)
                start_pos = (start_pt.x, start_pt.y, start_pt.z)
                direction = (dir.x, dir.y, dir.z)
                player.send_event('E_CALL_SYNC_METHOD', 'try_ray_mark', (start_pos, direction, mark_type, MARK_WAY_DOUBLE_CLICK), True)
            return

    def get_min_max_sense_ratio(self):
        base_val = self.get_scale_base_val()
        ratio = (base_val - uoc.SST_RANGE[0]) / (uoc.SST_RANGE[1] - uoc.SST_RANGE[0])
        min_sense_ratio = (self.min_adjust_touch_ratio_high_bound - self.min_adjust_touch_ratio_low_bound) * (1.0 - ratio) + self.min_adjust_touch_ratio_low_bound
        max_sense_ratio = (self.max_adjust_touch_ratio_high_bound - self.max_adjust_touch_ratio_low_bound) * (1.0 - ratio) + self.max_adjust_touch_ratio_low_bound
        return (
         min_sense_ratio, max_sense_ratio)

    def modify_sense_by_dist(self, original_dx, original_dy, dx, dy, touch_pos):
        cnt_time = time()
        ratio = 1.0
        cnt_distance = int(abs(original_dx) + abs(original_dy))
        new_touch_list = []
        for item in self._prev_touch_list:
            if cnt_time - item[1] < self.adjust_touch_interval:
                new_touch_list.append(item)

        new_touch_length = len(new_touch_list)
        if new_touch_length > self._max_touch_list_length:
            new_touch_list = new_touch_list[new_touch_length - self._max_touch_list_length:]
        new_touch_list.append([cnt_distance, cnt_time])
        self._prev_touch_list = new_touch_list
        avr_touch_distance = 0
        min_sense_ratio, max_sense_ratio = self.get_min_max_sense_ratio()
        for item in self._prev_touch_list:
            avr_touch_distance += item[0]

        avr_touch_distance /= len(self._prev_touch_list)
        if avr_touch_distance <= self.min_adjust_distance_threshold:
            if self.is_valid_down_speed_mode():
                ratio = min_sense_ratio
        elif avr_touch_distance >= self.max_adjust_distance_threshold:
            ratio = max_sense_ratio
        return ratio

    def register_keys(self):
        import game
        game_hook.add_key_handler(game.MSG_KEY_DOWN, self._down_reg_keys, self._key_handler)
        game_hook.add_key_handler(game.MSG_KEY_UP, self._up_reg_keys, self._key_handler)
        self._cur_md_dir = None
        if global_data.is_inner_server:
            from .keyboard import MechaKeyboard, CommonKeyboard
            self.key_ctrls = [
             MechaKeyboard.MechaKeyboard(), CommonKeyboard.CommonKeyboard()]
            for key_ctrl in self.key_ctrls:
                key_ctrl.install()
                key_ctrl.enable()

        return

    def unregister_keys(self):
        import game
        game_hook.remove_key_handler(game.MSG_KEY_DOWN, self._down_reg_keys, self._key_handler)
        game_hook.remove_key_handler(game.MSG_KEY_UP, self._up_reg_keys, self._key_handler)
        for key_ctrl in self.key_ctrls:
            key_ctrl.disable()
            key_ctrl.uninstall()

        self.key_ctrls = []
        self._cur_md_dir = None
        return

    def move_toward(self, direction):
        move_vec = camera_const.DIR_VECS[direction]
        scn = self.scene()
        player = scn.get_player()
        player.send_event('E_MOVE', move_vec)

    def _key_handler--- This code section failed: ---

 722       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'game'
           9  STORE_FAST            3  'game'

 723      12  LOAD_CONST            1  ''
          15  LOAD_CONST            0  ''
          18  IMPORT_NAME           1  'math'
          21  STORE_FAST            4  'math'

 725      24  LOAD_FAST             3  'game'
          27  LOAD_ATTR             2  'VK_SHIFT'
          30  BUILD_LIST_1          1 
          33  STORE_FAST            5  'state_keys'

 727      36  BUILD_MAP_4           4 

 728      39  LOAD_GLOBAL           3  'camera_const'
          42  LOAD_ATTR             4  'MOVE_DIR_0'
          45  LOAD_FAST             3  'game'
          48  LOAD_ATTR             5  'VK_W'
          51  STORE_MAP        

 729      52  LOAD_GLOBAL           3  'camera_const'
          55  LOAD_ATTR             6  'MOVE_DIR_180'
          58  LOAD_FAST             3  'game'
          61  LOAD_ATTR             7  'VK_S'
          64  STORE_MAP        

 730      65  LOAD_GLOBAL           3  'camera_const'
          68  LOAD_ATTR             8  'MOVE_DIR_270'
          71  LOAD_FAST             3  'game'
          74  LOAD_ATTR             9  'VK_A'
          77  STORE_MAP        

 731      78  LOAD_GLOBAL           3  'camera_const'
          81  LOAD_ATTR            10  'MOVE_DIR_90'
          84  LOAD_FAST             3  'game'
          87  LOAD_ATTR            11  'VK_D'
          90  STORE_MAP        
          91  STORE_FAST            6  'gamemap'

 734      94  LOAD_FAST             0  'self'
          97  LOAD_ATTR            12  'scene'
         100  CALL_FUNCTION_0       0 
         103  STORE_FAST            7  'scn'

 735     106  LOAD_FAST             7  'scn'
         109  LOAD_ATTR            13  'get_player'
         112  CALL_FUNCTION_0       0 
         115  STORE_FAST            8  'player'

 737     118  LOAD_FAST             1  'msg'
         121  LOAD_FAST             3  'game'
         124  LOAD_ATTR            14  'MSG_KEY_DOWN'
         127  COMPARE_OP            2  '=='
         130  POP_JUMP_IF_FALSE   192  'to 192'

 738     133  LOAD_FAST             2  'keycode'
         136  LOAD_FAST             6  'gamemap'
         139  COMPARE_OP            6  'in'
         142  POP_JUMP_IF_FALSE   161  'to 161'

 739     145  LOAD_GLOBAL          15  'True'
         148  LOAD_GLOBAL          16  'global_data'
         151  LOAD_ATTR            17  'keys'
         154  LOAD_FAST             2  'keycode'
         157  STORE_SUBSCR     
         158  JUMP_FORWARD          0  'to 161'
       161_0  COME_FROM                '158'

 740     161  LOAD_FAST             2  'keycode'
         164  LOAD_FAST             5  'state_keys'
         167  COMPARE_OP            6  'in'
         170  POP_JUMP_IF_FALSE   266  'to 266'

 741     173  LOAD_GLOBAL          15  'True'
         176  LOAD_GLOBAL          16  'global_data'
         179  LOAD_ATTR            17  'keys'
         182  LOAD_FAST             2  'keycode'
         185  STORE_SUBSCR     
         186  JUMP_ABSOLUTE       266  'to 266'
         189  JUMP_FORWARD         74  'to 266'

 743     192  LOAD_FAST             1  'msg'
         195  LOAD_FAST             3  'game'
         198  LOAD_ATTR            18  'MSG_KEY_UP'
         201  COMPARE_OP            2  '=='
         204  POP_JUMP_IF_FALSE   266  'to 266'

 744     207  LOAD_FAST             2  'keycode'
         210  LOAD_FAST             6  'gamemap'
         213  COMPARE_OP            6  'in'
         216  POP_JUMP_IF_FALSE   235  'to 235'

 745     219  LOAD_GLOBAL          19  'False'
         222  LOAD_GLOBAL          16  'global_data'
         225  LOAD_ATTR            17  'keys'
         228  LOAD_FAST             2  'keycode'
         231  STORE_SUBSCR     
         232  JUMP_FORWARD          0  'to 235'
       235_0  COME_FROM                '232'

 746     235  LOAD_FAST             2  'keycode'
         238  LOAD_FAST             5  'state_keys'
         241  COMPARE_OP            6  'in'
         244  POP_JUMP_IF_FALSE   266  'to 266'

 747     247  LOAD_GLOBAL          19  'False'
         250  LOAD_GLOBAL          16  'global_data'
         253  LOAD_ATTR            17  'keys'
         256  LOAD_FAST             2  'keycode'
         259  STORE_SUBSCR     
         260  JUMP_ABSOLUTE       266  'to 266'
         263  JUMP_FORWARD          0  'to 266'
       266_0  COME_FROM                '263'
       266_1  COME_FROM                '189'

 749     266  LOAD_CONST            1  ''
         269  LOAD_CONST            2  ('can_run_debug_key_logic',)
         272  IMPORT_NAME          20  'logic.gutils.pc_utils'
         275  IMPORT_FROM          21  'can_run_debug_key_logic'
         278  STORE_FAST            9  'can_run_debug_key_logic'
         281  POP_TOP          

 750     282  LOAD_FAST             9  'can_run_debug_key_logic'
         285  CALL_FUNCTION_0       0 
         288  UNARY_NOT        
         289  POP_JUMP_IF_TRUE    301  'to 301'
         292  LOAD_GLOBAL          16  'global_data'
         295  LOAD_ATTR            22  'is_yunying'
       298_0  COME_FROM                '289'
         298  POP_JUMP_IF_FALSE   305  'to 305'

 751     301  LOAD_CONST            0  ''
         304  RETURN_END_IF    
       305_0  COME_FROM                '298'

 753     305  LOAD_FAST             8  'player'
         308  LOAD_CONST            0  ''
         311  COMPARE_OP            8  'is'
         314  POP_JUMP_IF_FALSE   321  'to 321'

 754     317  LOAD_CONST            0  ''
         320  RETURN_END_IF    
       321_0  COME_FROM                '314'

 755     321  LOAD_FAST             1  'msg'
         324  LOAD_FAST             3  'game'
         327  LOAD_ATTR            14  'MSG_KEY_DOWN'
         330  COMPARE_OP            2  '=='
         333  POP_JUMP_IF_FALSE   728  'to 728'

 756     336  LOAD_GLOBAL          16  'global_data'
         339  LOAD_ATTR            24  'freefly_camera_mgr'
         342  UNARY_NOT        
         343  POP_JUMP_IF_TRUE    362  'to 362'
         346  LOAD_GLOBAL          16  'global_data'
         349  LOAD_ATTR            24  'freefly_camera_mgr'
         352  LOAD_ATTR            25  'is_enable'
         355  CALL_FUNCTION_0       0 
         358  UNARY_NOT        
       359_0  COME_FROM                '343'
         359  POP_JUMP_IF_FALSE   728  'to 728'

 757     362  LOAD_FAST             3  'game'
         365  LOAD_ATTR            26  'VK_LEFT'
         368  LOAD_FAST             2  'keycode'
         371  COMPARE_OP            2  '=='
         374  POP_JUMP_IF_TRUE    392  'to 392'
         377  LOAD_FAST             3  'game'
         380  LOAD_ATTR            27  'VK_RIGHT'
         383  LOAD_FAST             2  'keycode'
         386  COMPARE_OP            2  '=='
       389_0  COME_FROM                '374'
         389  POP_JUMP_IF_FALSE   542  'to 542'

 759     392  LOAD_GLOBAL          16  'global_data'
         395  LOAD_ATTR            28  'debug_camera_delta_y_angle'
         398  JUMP_IF_TRUE_OR_POP   404  'to 404'
         401  LOAD_CONST            3  5
       404_0  COME_FROM                '398'
         404  STORE_FAST           10  'DELTA_Y_ANGLE'

 760     407  LOAD_FAST             3  'game'
         410  LOAD_ATTR            26  'VK_LEFT'
         413  LOAD_FAST             2  'keycode'
         416  COMPARE_OP            2  '=='
         419  POP_JUMP_IF_FALSE   428  'to 428'
         422  LOAD_CONST            4  -1
       425_0  COME_FROM                '419'
         425  JUMP_IF_TRUE_OR_POP   431  'to 431'
         428  LOAD_CONST            5  1
       431_0  COME_FROM                '425'
         431  STORE_FAST           11  'sign'

 761     434  LOAD_FAST            11  'sign'
         437  LOAD_FAST            10  'DELTA_Y_ANGLE'
         440  BINARY_MULTIPLY  
         441  LOAD_FAST             4  'math'
         444  LOAD_ATTR            29  'pi'
         447  BINARY_MULTIPLY  
         448  LOAD_CONST            6  180.0
         451  BINARY_DIVIDE    
         452  STORE_FAST           12  'dx'

 762     455  LOAD_FAST             7  'scn'
         458  LOAD_ATTR            30  'get_com'
         461  LOAD_CONST            7  'PartCamera'
         464  CALL_FUNCTION_1       1 
         467  STORE_FAST           13  'com_camera'

 763     470  LOAD_FAST            13  'com_camera'
         473  LOAD_ATTR            31  'get_cur_camera_state_type'
         476  CALL_FUNCTION_0       0 
         479  LOAD_GLOBAL          32  'FREE_MODEL'
         482  LOAD_GLOBAL          33  'DEBUG_MODE'
         485  BUILD_LIST_2          2 
         488  COMPARE_OP            6  'in'
         491  POP_JUMP_IF_FALSE   510  'to 510'

 764     494  LOAD_FAST            13  'com_camera'
         497  LOAD_ATTR            34  'yaw'
         500  LOAD_FAST            12  'dx'
         503  CALL_FUNCTION_1       1 
         506  POP_TOP          
         507  JUMP_ABSOLUTE       542  'to 542'

 766     510  LOAD_FAST            13  'com_camera'
         513  LOAD_ATTR            34  'yaw'
         516  LOAD_FAST            12  'dx'
         519  CALL_FUNCTION_1       1 
         522  POP_TOP          

 767     523  LOAD_FAST             8  'player'
         526  LOAD_ATTR            35  'send_event'
         529  LOAD_CONST            8  'E_DELTA_YAW'
         532  LOAD_FAST            12  'dx'
         535  CALL_FUNCTION_2       2 
         538  POP_TOP          
         539  JUMP_FORWARD          0  'to 542'
       542_0  COME_FROM                '539'

 769     542  LOAD_FAST             3  'game'
         545  LOAD_ATTR            36  'VK_UP'
         548  LOAD_FAST             2  'keycode'
         551  COMPARE_OP            2  '=='
         554  POP_JUMP_IF_TRUE    572  'to 572'
         557  LOAD_FAST             3  'game'
         560  LOAD_ATTR            37  'VK_DOWN'
         563  LOAD_FAST             2  'keycode'
         566  COMPARE_OP            2  '=='
       569_0  COME_FROM                '554'
         569  POP_JUMP_IF_FALSE   725  'to 725'

 770     572  LOAD_GLOBAL          16  'global_data'
         575  LOAD_ATTR            38  'debug_camera_delta_x_angle'
         578  JUMP_IF_TRUE_OR_POP   584  'to 584'
         581  LOAD_CONST            9  2
       584_0  COME_FROM                '578'
         584  STORE_FAST           14  'DELTA_X_ANGLE'

 771     587  LOAD_FAST             3  'game'
         590  LOAD_ATTR            36  'VK_UP'
         593  LOAD_FAST             2  'keycode'
         596  COMPARE_OP            2  '=='
         599  POP_JUMP_IF_FALSE   608  'to 608'
         602  LOAD_CONST            4  -1
       605_0  COME_FROM                '599'
         605  JUMP_IF_TRUE_OR_POP   611  'to 611'
         608  LOAD_CONST            5  1
       611_0  COME_FROM                '605'
         611  STORE_FAST           11  'sign'

 772     614  LOAD_FAST            11  'sign'
         617  LOAD_FAST            14  'DELTA_X_ANGLE'
         620  BINARY_MULTIPLY  
         621  LOAD_FAST             4  'math'
         624  LOAD_ATTR            29  'pi'
         627  BINARY_MULTIPLY  
         628  LOAD_CONST            6  180.0
         631  BINARY_DIVIDE    
         632  STORE_FAST           12  'dx'

 773     635  LOAD_FAST             7  'scn'
         638  LOAD_ATTR            30  'get_com'
         641  LOAD_CONST            7  'PartCamera'
         644  CALL_FUNCTION_1       1 
         647  STORE_FAST           13  'com_camera'

 774     650  LOAD_FAST            13  'com_camera'
         653  LOAD_ATTR            31  'get_cur_camera_state_type'
         656  CALL_FUNCTION_0       0 
         659  LOAD_GLOBAL          32  'FREE_MODEL'
         662  LOAD_GLOBAL          33  'DEBUG_MODE'
         665  BUILD_LIST_2          2 
         668  COMPARE_OP            6  'in'
         671  POP_JUMP_IF_FALSE   690  'to 690'

 775     674  LOAD_FAST            13  'com_camera'
         677  LOAD_ATTR            39  'pitch'
         680  LOAD_FAST            12  'dx'
         683  CALL_FUNCTION_1       1 
         686  POP_TOP          
         687  JUMP_ABSOLUTE       722  'to 722'

 777     690  LOAD_FAST            13  'com_camera'
         693  LOAD_ATTR            39  'pitch'
         696  LOAD_FAST            12  'dx'
         699  CALL_FUNCTION_1       1 
         702  POP_TOP          

 778     703  LOAD_FAST             8  'player'
         706  LOAD_ATTR            35  'send_event'
         709  LOAD_CONST           10  'E_DELTA_PITCH'
         712  LOAD_FAST            12  'dx'
         715  CALL_FUNCTION_2       2 
         718  POP_TOP          
         719  JUMP_ABSOLUTE       725  'to 725'
         722  JUMP_ABSOLUTE       728  'to 728'
         725  JUMP_FORWARD          0  'to 728'
       728_0  COME_FROM                '725'

 779     728  LOAD_FAST             2  'keycode'
         731  LOAD_FAST             3  'game'
         734  LOAD_ATTR            40  'VK_F'
         737  COMPARE_OP            2  '=='
         740  POP_JUMP_IF_FALSE   812  'to 812'
         743  LOAD_FAST             1  'msg'
         746  LOAD_FAST             3  'game'
         749  LOAD_ATTR            14  'MSG_KEY_DOWN'
         752  COMPARE_OP            2  '=='
       755_0  COME_FROM                '740'
         755  POP_JUMP_IF_FALSE   812  'to 812'

 780     758  LOAD_GLOBAL          16  'global_data'
         761  LOAD_ATTR            41  'game_mode'
         764  LOAD_ATTR            42  'is_mode_type'
         767  LOAD_GLOBAL          43  'game_mode_const'
         770  LOAD_ATTR            44  'GAME_MODE_PVE_EDIT'
         773  CALL_FUNCTION_1       1 
         776  POP_JUMP_IF_FALSE   783  'to 783'

 781     779  LOAD_CONST            0  ''
         782  RETURN_END_IF    
       783_0  COME_FROM                '776'

 782     783  LOAD_CONST            1  ''
         786  LOAD_CONST           11  ('scene_utils',)
         789  IMPORT_NAME          45  'logic.gutils'
         792  IMPORT_FROM          46  'scene_utils'
         795  STORE_FAST           15  'scene_utils'
         798  POP_TOP          

 783     799  LOAD_FAST            15  'scene_utils'
         802  LOAD_ATTR            47  'show_scene_collision'
         805  CALL_FUNCTION_0       0 
         808  POP_TOP          
         809  JUMP_FORWARD          0  'to 812'
       812_0  COME_FROM                '809'

 784     812  LOAD_FAST             2  'keycode'
         815  LOAD_FAST             3  'game'
         818  LOAD_ATTR            48  'VK_1'
         821  COMPARE_OP            2  '=='
         824  POP_JUMP_IF_FALSE   846  'to 846'
         827  LOAD_FAST             1  'msg'
         830  LOAD_FAST             3  'game'
         833  LOAD_ATTR            14  'MSG_KEY_DOWN'
         836  COMPARE_OP            2  '=='
       839_0  COME_FROM                '824'
         839  POP_JUMP_IF_FALSE   846  'to 846'

 786     842  LOAD_CONST            0  ''
         845  RETURN_END_IF    
       846_0  COME_FROM                '839'

 788     846  LOAD_FAST             2  'keycode'
         849  LOAD_FAST             3  'game'
         852  LOAD_ATTR            49  'VK_2'
         855  COMPARE_OP            2  '=='
         858  POP_JUMP_IF_FALSE   880  'to 880'
         861  LOAD_FAST             1  'msg'
         864  LOAD_FAST             3  'game'
         867  LOAD_ATTR            14  'MSG_KEY_DOWN'
         870  COMPARE_OP            2  '=='
       873_0  COME_FROM                '858'
         873  POP_JUMP_IF_FALSE   880  'to 880'

 790     876  LOAD_CONST            0  ''
         879  RETURN_END_IF    
       880_0  COME_FROM                '873'

 792     880  LOAD_FAST             2  'keycode'
         883  LOAD_FAST             3  'game'
         886  LOAD_ATTR            50  'VK_N'
         889  COMPARE_OP            2  '=='
         892  POP_JUMP_IF_FALSE  1094  'to 1094'
         895  LOAD_FAST             1  'msg'
         898  LOAD_FAST             3  'game'
         901  LOAD_ATTR            14  'MSG_KEY_DOWN'
         904  COMPARE_OP            2  '=='
       907_0  COME_FROM                '892'
         907  POP_JUMP_IF_FALSE  1094  'to 1094'

 794     910  LOAD_CONST            1  ''
         913  LOAD_CONST           12  ('vehicle_const',)
         916  IMPORT_NAME          51  'logic.gcommon.common_const'
         919  IMPORT_FROM          52  'vehicle_const'
         922  STORE_FAST           16  'vehicle_const'
         925  POP_TOP          

 795     926  LOAD_GLOBAL          16  'global_data'
         929  LOAD_ATTR            53  'player'
         932  STORE_FAST            8  'player'

 796     935  LOAD_FAST             8  'player'
         938  LOAD_ATTR            54  'logic'
         941  LOAD_ATTR            55  'ev_g_control_target'
         944  CALL_FUNCTION_0       0 
         947  STORE_FAST           17  'ctrl_target'

 797     950  LOAD_FAST             8  'player'
         953  LOAD_FAST            17  'ctrl_target'
         956  COMPARE_OP            3  '!='
         959  POP_JUMP_IF_FALSE  1094  'to 1094'

 799     962  LOAD_FAST            17  'ctrl_target'
         965  LOAD_ATTR            54  'logic'
         968  LOAD_ATTR            56  'ev_g_passenger_info'
         971  CALL_FUNCTION_0       0 
         974  STORE_FAST           18  'passengers'

 800     977  LOAD_FAST            18  'passengers'
         980  LOAD_FAST             8  'player'
         983  LOAD_ATTR            57  'id'
         986  BINARY_SUBSCR    
         987  STORE_FAST           19  'seat_name'

 801     990  LOAD_CONST           13  'seat_1'
         993  STORE_FAST           20  'change_seat'

 802     996  LOAD_FAST            19  'seat_name'
         999  LOAD_CONST           13  'seat_1'
        1002  COMPARE_OP            2  '=='
        1005  POP_JUMP_IF_FALSE  1017  'to 1017'

 803    1008  LOAD_CONST           14  'seat_2'
        1011  STORE_FAST           20  'change_seat'
        1014  JUMP_FORWARD          0  'to 1017'
      1017_0  COME_FROM                '1014'

 805    1017  BUILD_MAP_3           3 

 806    1020  LOAD_FAST            17  'ctrl_target'
        1023  LOAD_ATTR            57  'id'
        1026  LOAD_CONST           15  'vid'
        1029  STORE_MAP        

 807    1030  LOAD_FAST            16  'vehicle_const'
        1033  LOAD_ATTR            58  'CH_SEAT_INFO'
        1036  LOAD_CONST           16  'change_type'
        1039  STORE_MAP        

 808    1040  BUILD_MAP_1           1 

 809    1043  LOAD_FAST            20  'change_seat'
        1046  LOAD_FAST             8  'player'
        1049  LOAD_ATTR            57  'id'
        1052  STORE_MAP        
        1053  LOAD_CONST           17  'data'
        1056  STORE_MAP        
        1057  STORE_FAST           21  'info'

 812    1060  LOAD_FAST             8  'player'
        1063  LOAD_ATTR            54  'logic'
        1066  LOAD_ATTR            35  'send_event'
        1069  LOAD_CONST           18  'E_CALL_SYNC_METHOD'
        1072  LOAD_CONST           19  'change_vehicle_data'
        1075  LOAD_FAST            21  'info'
        1078  BUILD_TUPLE_1         1 
        1081  LOAD_GLOBAL          15  'True'
        1084  CALL_FUNCTION_4       4 
        1087  POP_TOP          
        1088  JUMP_ABSOLUTE      1094  'to 1094'
        1091  JUMP_FORWARD          0  'to 1094'
      1094_0  COME_FROM                '1091'

 814    1094  LOAD_FAST             2  'keycode'
        1097  LOAD_FAST             3  'game'
        1100  LOAD_ATTR            59  'VK_M'
        1103  COMPARE_OP            2  '=='
        1106  POP_JUMP_IF_FALSE  1128  'to 1128'
        1109  LOAD_FAST             1  'msg'
        1112  LOAD_FAST             3  'game'
        1115  LOAD_ATTR            14  'MSG_KEY_DOWN'
        1118  COMPARE_OP            2  '=='
      1121_0  COME_FROM                '1106'
        1121  POP_JUMP_IF_FALSE  1128  'to 1128'

 817    1124  LOAD_CONST            0  ''
        1127  RETURN_END_IF    
      1128_0  COME_FROM                '1121'

 819    1128  LOAD_GLOBAL          60  'hasattr'
        1131  LOAD_GLOBAL          20  'logic.gutils.pc_utils'
        1134  CALL_FUNCTION_2       2 
        1137  POP_JUMP_IF_TRUE   1152  'to 1152'

 820    1140  BUILD_MAP_0           0 
        1143  LOAD_FAST             0  'self'
        1146  STORE_ATTR           61  'keyState'
        1149  JUMP_FORWARD          0  'to 1152'
      1152_0  COME_FROM                '1149'

 822    1152  LOAD_FAST             1  'msg'
        1155  LOAD_FAST             3  'game'
        1158  LOAD_ATTR            14  'MSG_KEY_DOWN'
        1161  COMPARE_OP            2  '=='
        1164  POP_JUMP_IF_FALSE  1664  'to 1664'

 823    1167  LOAD_FAST             0  'self'
        1170  LOAD_ATTR            61  'keyState'
        1173  LOAD_ATTR            62  'get'
        1176  LOAD_FAST             2  'keycode'
        1179  LOAD_GLOBAL          19  'False'
        1182  CALL_FUNCTION_2       2 
        1185  POP_JUMP_IF_TRUE   1204  'to 1204'

 824    1188  LOAD_GLOBAL          15  'True'
        1191  LOAD_FAST             0  'self'
        1194  LOAD_ATTR            61  'keyState'
        1197  LOAD_FAST             2  'keycode'
        1200  STORE_SUBSCR     
        1201  JUMP_FORWARD          4  'to 1208'

 826    1204  LOAD_CONST            0  ''
        1207  RETURN_VALUE     
      1208_0  COME_FROM                '1201'

 828    1208  LOAD_FAST             3  'game'
        1211  LOAD_ATTR            63  'VK_J'
        1214  LOAD_FAST             2  'keycode'
        1217  COMPARE_OP            2  '=='
        1220  POP_JUMP_IF_FALSE  1378  'to 1378'

 829    1223  LOAD_GLOBAL          16  'global_data'
        1226  LOAD_ATTR            64  'mecha'
        1229  POP_JUMP_IF_FALSE  1254  'to 1254'

 830    1232  LOAD_GLOBAL          16  'global_data'
        1235  LOAD_ATTR            64  'mecha'
        1238  LOAD_ATTR            54  'logic'
        1241  LOAD_ATTR            65  'ev_g_action_down'
        1244  LOAD_CONST           21  'action1'
        1247  CALL_FUNCTION_1       1 
        1250  POP_TOP          
        1251  JUMP_ABSOLUTE      1378  'to 1378'

 832    1254  LOAD_GLOBAL          16  'global_data'
        1257  LOAD_ATTR            66  'ui_mgr'
        1260  LOAD_ATTR            67  'get_ui'
        1263  LOAD_CONST           22  'FireRockerUI'
        1266  CALL_FUNCTION_1       1 
        1269  STORE_DEREF           0  'a'

 833    1272  LOAD_DEREF            0  'a'
        1275  POP_JUMP_IF_TRUE   1282  'to 1282'

 834    1278  LOAD_CONST            0  ''
        1281  RETURN_END_IF    
      1282_0  COME_FROM                '1275'

 836    1282  LOAD_CONST           23  'TouchSimu'
        1285  LOAD_GLOBAL          68  'object'
        1288  BUILD_TUPLE_1         1 
        1291  LOAD_CLOSURE          0  'a'
        1297  LOAD_CONST               '<code_object TouchSimu>'
        1300  MAKE_CLOSURE_0        0 
        1303  CALL_FUNCTION_0       0 
        1306  BUILD_CLASS      
        1307  STORE_FAST           22  'TouchSimu'

 842    1310  LOAD_DEREF            0  'a'
        1313  LOAD_ATTR            69  'panel'
        1316  LOAD_ATTR            70  'shot_bar'
        1319  LOAD_ATTR            71  'OnBegin'
        1322  LOAD_FAST            22  'TouchSimu'
        1325  CALL_FUNCTION_0       0 
        1328  CALL_FUNCTION_1       1 
        1331  POP_TOP          

 843    1332  LOAD_GLOBAL          16  'global_data'
        1335  LOAD_ATTR            53  'player'
        1338  LOAD_ATTR            54  'logic'
        1341  LOAD_ATTR            55  'ev_g_control_target'
        1344  CALL_FUNCTION_0       0 
        1347  STORE_FAST           23  'control_target'

 844    1350  LOAD_FAST            23  'control_target'
        1353  POP_JUMP_IF_FALSE  1378  'to 1378'

 845    1356  LOAD_FAST            23  'control_target'
        1359  LOAD_ATTR            54  'logic'
        1362  LOAD_ATTR            35  'send_event'
        1365  LOAD_CONST           25  'MAIN_WEAPON_ATTACK'
        1368  CALL_FUNCTION_1       1 
        1371  POP_TOP          
        1372  JUMP_ABSOLUTE      1378  'to 1378'
        1375  JUMP_FORWARD          0  'to 1378'
      1378_0  COME_FROM                '1375'

 847    1378  LOAD_FAST             3  'game'
        1381  LOAD_ATTR            72  'VK_K'
        1384  LOAD_FAST             2  'keycode'
        1387  COMPARE_OP            2  '=='
        1390  POP_JUMP_IF_FALSE  1505  'to 1505'

 848    1393  LOAD_GLOBAL          16  'global_data'
        1396  LOAD_ATTR            64  'mecha'
        1399  POP_JUMP_IF_FALSE  1424  'to 1424'

 849    1402  LOAD_GLOBAL          16  'global_data'
        1405  LOAD_ATTR            64  'mecha'
        1408  LOAD_ATTR            54  'logic'
        1411  LOAD_ATTR            65  'ev_g_action_down'
        1414  LOAD_CONST           26  'action4'
        1417  CALL_FUNCTION_1       1 
        1420  POP_TOP          
        1421  JUMP_ABSOLUTE      1505  'to 1505'

 851    1424  LOAD_GLOBAL          16  'global_data'
        1427  LOAD_ATTR            66  'ui_mgr'
        1430  LOAD_ATTR            67  'get_ui'
        1433  LOAD_CONST           27  'AimRockerUI'
        1436  CALL_FUNCTION_1       1 
        1439  STORE_DEREF           0  'a'

 852    1442  LOAD_DEREF            0  'a'
        1445  POP_JUMP_IF_TRUE   1452  'to 1452'

 853    1448  LOAD_CONST            0  ''
        1451  RETURN_END_IF    
      1452_0  COME_FROM                '1445'

 855    1452  LOAD_CONST           23  'TouchSimu'
        1455  LOAD_GLOBAL          68  'object'
        1458  BUILD_TUPLE_1         1 
        1461  LOAD_CLOSURE          0  'a'
        1467  LOAD_CONST               '<code_object TouchSimu>'
        1470  MAKE_CLOSURE_0        0 
        1473  CALL_FUNCTION_0       0 
        1476  BUILD_CLASS      
        1477  STORE_FAST           22  'TouchSimu'

 861    1480  LOAD_DEREF            0  'a'
        1483  LOAD_ATTR            69  'panel'
        1486  LOAD_ATTR            73  'aim_button'
        1489  LOAD_ATTR            71  'OnBegin'
        1492  LOAD_FAST            22  'TouchSimu'
        1495  CALL_FUNCTION_0       0 
        1498  CALL_FUNCTION_1       1 
        1501  POP_TOP          
        1502  JUMP_FORWARD          0  'to 1505'
      1505_0  COME_FROM                '1502'

 862    1505  LOAD_FAST             3  'game'
        1508  LOAD_ATTR            74  'VK_T'
        1511  LOAD_FAST             2  'keycode'
        1514  COMPARE_OP            2  '=='
        1517  POP_JUMP_IF_FALSE  2688  'to 2688'

 863    1520  LOAD_GLOBAL          16  'global_data'
        1523  LOAD_ATTR            53  'player'
        1526  STORE_FAST           24  'debug_target'

 864    1529  LOAD_GLOBAL          16  'global_data'
        1532  LOAD_ATTR            53  'player'
        1535  LOAD_ATTR            54  'logic'
        1538  LOAD_ATTR            55  'ev_g_control_target'
        1541  CALL_FUNCTION_0       0 
        1544  STORE_FAST           23  'control_target'

 865    1547  LOAD_FAST            23  'control_target'
        1550  POP_JUMP_IF_FALSE  1581  'to 1581'
        1553  LOAD_FAST            23  'control_target'
        1556  LOAD_ATTR            54  'logic'
        1559  LOAD_ATTR            75  'MASK'
        1562  LOAD_GLOBAL          76  'preregistered_tags'
        1565  LOAD_ATTR            77  'MECHA_VEHICLE_TAG_VALUE'
        1568  BINARY_AND       
      1569_0  COME_FROM                '1550'
        1569  POP_JUMP_IF_FALSE  1581  'to 1581'

 866    1572  LOAD_FAST            23  'control_target'
        1575  STORE_FAST           24  'debug_target'
        1578  JUMP_FORWARD          0  'to 1581'
      1581_0  COME_FROM                '1578'

 868    1581  LOAD_FAST            24  'debug_target'
        1584  LOAD_ATTR            54  'logic'
        1587  LOAD_ATTR            35  'send_event'
        1590  LOAD_CONST           29  'E_SHOW_FULLBODY_ANIMATION'
        1593  CALL_FUNCTION_1       1 
        1596  POP_TOP          

 870    1597  LOAD_FAST             0  'self'
        1600  LOAD_ATTR            78  'com_camera'
        1603  POP_JUMP_IF_FALSE  1661  'to 1661'

 871    1606  LOAD_FAST             0  'self'
        1609  LOAD_ATTR            78  'com_camera'
        1612  LOAD_ATTR            79  'get_cam_trk_component'
        1615  CALL_FUNCTION_0       0 
        1618  STORE_FAST           25  'cam_trk_component'

 872    1621  LOAD_FAST            25  'cam_trk_component'
        1624  POP_JUMP_IF_FALSE  1658  'to 1658'

 873    1627  LOAD_GLOBAL          16  'global_data'
        1630  LOAD_ATTR            80  'emgr'
        1633  LOAD_ATTR            81  'update_camera_debug_info'
        1636  LOAD_ATTR            82  'emit'
        1639  LOAD_FAST            25  'cam_trk_component'
        1642  LOAD_ATTR            83  'get_playing_trk_info_list'
        1645  CALL_FUNCTION_0       0 
        1648  CALL_FUNCTION_1       1 
        1651  POP_TOP          
        1652  JUMP_ABSOLUTE      1658  'to 1658'
        1655  JUMP_ABSOLUTE      1661  'to 1661'
        1658  JUMP_ABSOLUTE      2688  'to 2688'
        1661  JUMP_FORWARD       1024  'to 2688'

 875    1664  LOAD_FAST             1  'msg'
        1667  LOAD_FAST             3  'game'
        1670  LOAD_ATTR            18  'MSG_KEY_UP'
        1673  COMPARE_OP            2  '=='
        1676  POP_JUMP_IF_FALSE  2688  'to 2688'

 876    1679  LOAD_GLOBAL          19  'False'
        1682  LOAD_FAST             0  'self'
        1685  LOAD_ATTR            61  'keyState'
        1688  LOAD_FAST             2  'keycode'
        1691  STORE_SUBSCR     

 877    1692  LOAD_FAST             3  'game'
        1695  LOAD_ATTR            63  'VK_J'
        1698  LOAD_FAST             2  'keycode'
        1701  COMPARE_OP            2  '=='
        1704  POP_JUMP_IF_FALSE  1873  'to 1873'

 878    1707  LOAD_GLOBAL          16  'global_data'
        1710  LOAD_ATTR            64  'mecha'
        1713  POP_JUMP_IF_FALSE  1741  'to 1741'

 879    1716  LOAD_GLOBAL          16  'global_data'
        1719  LOAD_ATTR            64  'mecha'
        1722  LOAD_ATTR            54  'logic'
        1725  LOAD_ATTR            35  'send_event'
        1728  LOAD_CONST           30  'E_ACTION_UP'
        1731  LOAD_CONST           21  'action1'
        1734  CALL_FUNCTION_2       2 
        1737  POP_TOP          
        1738  JUMP_ABSOLUTE      1873  'to 1873'

 881    1741  LOAD_GLOBAL          16  'global_data'
        1744  LOAD_ATTR            66  'ui_mgr'
        1747  LOAD_ATTR            67  'get_ui'
        1750  LOAD_CONST           22  'FireRockerUI'
        1753  CALL_FUNCTION_1       1 
        1756  STORE_DEREF           0  'a'

 883    1759  LOAD_CONST           23  'TouchSimu'
        1762  LOAD_GLOBAL          68  'object'
        1765  BUILD_TUPLE_1         1 
        1768  LOAD_CLOSURE          0  'a'
        1774  LOAD_CONST               '<code_object TouchSimu>'
        1777  MAKE_CLOSURE_0        0 
        1780  CALL_FUNCTION_0       0 
        1783  BUILD_CLASS      
        1784  STORE_FAST           22  'TouchSimu'

 895    1787  LOAD_DEREF            0  'a'
        1790  POP_JUMP_IF_FALSE  1827  'to 1827'
        1793  LOAD_DEREF            0  'a'
        1796  LOAD_ATTR            69  'panel'
      1799_0  COME_FROM                '1790'
        1799  POP_JUMP_IF_FALSE  1827  'to 1827'

 896    1802  LOAD_DEREF            0  'a'
        1805  LOAD_ATTR            69  'panel'
        1808  LOAD_ATTR            70  'shot_bar'
        1811  LOAD_ATTR            84  'OnEnd'
        1814  LOAD_FAST            22  'TouchSimu'
        1817  CALL_FUNCTION_0       0 
        1820  CALL_FUNCTION_1       1 
        1823  POP_TOP          
        1824  JUMP_FORWARD          0  'to 1827'
      1827_0  COME_FROM                '1824'

 897    1827  LOAD_GLOBAL          16  'global_data'
        1830  LOAD_ATTR            53  'player'
        1833  LOAD_ATTR            54  'logic'
        1836  LOAD_ATTR            55  'ev_g_control_target'
        1839  CALL_FUNCTION_0       0 
        1842  STORE_FAST           23  'control_target'

 898    1845  LOAD_FAST            23  'control_target'
        1848  POP_JUMP_IF_FALSE  1873  'to 1873'

 899    1851  LOAD_FAST            23  'control_target'
        1854  LOAD_ATTR            54  'logic'
        1857  LOAD_ATTR            35  'send_event'
        1860  LOAD_CONST           32  'E_ATTACK_END'
        1863  CALL_FUNCTION_1       1 
        1866  POP_TOP          
        1867  JUMP_ABSOLUTE      1873  'to 1873'
        1870  JUMP_FORWARD          0  'to 1873'
      1873_0  COME_FROM                '1870'

 901    1873  LOAD_FAST             3  'game'
        1876  LOAD_ATTR            72  'VK_K'
        1879  LOAD_FAST             2  'keycode'
        1882  COMPARE_OP            2  '=='
        1885  POP_JUMP_IF_FALSE  2011  'to 2011'

 902    1888  LOAD_GLOBAL          16  'global_data'
        1891  LOAD_ATTR            64  'mecha'
        1894  POP_JUMP_IF_FALSE  1922  'to 1922'

 903    1897  LOAD_GLOBAL          16  'global_data'
        1900  LOAD_ATTR            64  'mecha'
        1903  LOAD_ATTR            54  'logic'
        1906  LOAD_ATTR            35  'send_event'
        1909  LOAD_CONST           30  'E_ACTION_UP'
        1912  LOAD_CONST           26  'action4'
        1915  CALL_FUNCTION_2       2 
        1918  POP_TOP          
        1919  JUMP_ABSOLUTE      2011  'to 2011'

 905    1922  LOAD_GLOBAL          16  'global_data'
        1925  LOAD_ATTR            66  'ui_mgr'
        1928  LOAD_ATTR            67  'get_ui'
        1931  LOAD_CONST           27  'AimRockerUI'
        1934  CALL_FUNCTION_1       1 
        1937  STORE_DEREF           0  'a'

 907    1940  LOAD_CONST           23  'TouchSimu'
        1943  LOAD_GLOBAL          68  'object'
        1946  BUILD_TUPLE_1         1 
        1949  LOAD_CLOSURE          0  'a'
        1955  LOAD_CONST               '<code_object TouchSimu>'
        1958  MAKE_CLOSURE_0        0 
        1961  CALL_FUNCTION_0       0 
        1964  BUILD_CLASS      
        1965  STORE_FAST           22  'TouchSimu'

 919    1968  LOAD_DEREF            0  'a'
        1971  POP_JUMP_IF_FALSE  2011  'to 2011'
        1974  LOAD_DEREF            0  'a'
        1977  LOAD_ATTR            69  'panel'
      1980_0  COME_FROM                '1971'
        1980  POP_JUMP_IF_FALSE  2011  'to 2011'

 920    1983  LOAD_DEREF            0  'a'
        1986  LOAD_ATTR            69  'panel'
        1989  LOAD_ATTR            73  'aim_button'
        1992  LOAD_ATTR            84  'OnEnd'
        1995  LOAD_FAST            22  'TouchSimu'
        1998  CALL_FUNCTION_0       0 
        2001  CALL_FUNCTION_1       1 
        2004  POP_TOP          
        2005  JUMP_ABSOLUTE      2011  'to 2011'
        2008  JUMP_FORWARD          0  'to 2011'
      2011_0  COME_FROM                '2008'

 922    2011  LOAD_FAST             3  'game'
        2014  LOAD_ATTR            85  'VK_B'
        2017  LOAD_FAST             2  'keycode'
        2020  COMPARE_OP            2  '=='
        2023  POP_JUMP_IF_FALSE  2580  'to 2580'

 923    2026  LOAD_GLOBAL          86  'print'
        2029  LOAD_CONST           34  'test--VK_B'
        2032  CALL_FUNCTION_1       1 
        2035  POP_TOP          

 924    2036  LOAD_CONST            1  ''
        2039  LOAD_CONST            0  ''
        2042  IMPORT_NAME          87  'world'
        2045  STORE_FAST           26  'world'

 927    2048  LOAD_FAST             8  'player'
        2051  LOAD_ATTR            55  'ev_g_control_target'
        2054  CALL_FUNCTION_0       0 
        2057  STORE_FAST           23  'control_target'

 929    2060  LOAD_FAST            23  'control_target'
        2063  POP_JUMP_IF_FALSE  2290  'to 2290'
        2066  LOAD_FAST            23  'control_target'
        2069  LOAD_ATTR            54  'logic'
        2072  LOAD_ATTR            75  'MASK'
        2075  LOAD_GLOBAL          76  'preregistered_tags'
        2078  LOAD_ATTR            77  'MECHA_VEHICLE_TAG_VALUE'
        2081  BINARY_AND       
      2082_0  COME_FROM                '2063'
        2082  POP_JUMP_IF_FALSE  2290  'to 2290'

 934    2085  LOAD_GLOBAL          86  'print'
        2088  LOAD_CONST           35  'test--VK_B--step1--control_target ='
        2091  LOAD_FAST            23  'control_target'
        2094  LOAD_CONST           36  '--control_target.logic ='
        2097  LOAD_FAST            23  'control_target'
        2100  LOAD_ATTR            54  'logic'
        2103  LOAD_CONST           37  '--is_enable_behavior ='
        2106  LOAD_FAST            23  'control_target'
        2109  LOAD_ATTR            54  'logic'
        2112  LOAD_ATTR            88  'ev_g_is_enable_behavior'
        2115  CALL_FUNCTION_0       0 
        2118  BUILD_TUPLE_6         6 
        2121  CALL_FUNCTION_1       1 
        2124  POP_TOP          

 935    2125  LOAD_FAST            23  'control_target'
        2128  LOAD_ATTR            54  'logic'
        2131  LOAD_ATTR            35  'send_event'
        2134  LOAD_CONST           38  'E_DUMP_STATE'
        2137  CALL_FUNCTION_1       1 
        2140  POP_TOP          

 936    2141  LOAD_FAST            23  'control_target'
        2144  LOAD_ATTR            54  'logic'
        2147  LOAD_ATTR            35  'send_event'
        2150  LOAD_CONST           39  'E_CHARACTER_ATTR'
        2153  LOAD_CONST           40  'animator_info'
        2156  LOAD_GLOBAL          15  'True'
        2159  CALL_FUNCTION_3       3 
        2162  POP_TOP          

 937    2163  LOAD_FAST            23  'control_target'
        2166  LOAD_ATTR            54  'logic'
        2169  LOAD_ATTR            35  'send_event'
        2172  LOAD_CONST           39  'E_CHARACTER_ATTR'
        2175  LOAD_CONST           41  'dump_character'
        2178  LOAD_CONST            5  1
        2181  CALL_FUNCTION_3       3 
        2184  POP_TOP          

 939    2185  LOAD_FAST            23  'control_target'
        2188  LOAD_ATTR            54  'logic'
        2191  LOAD_ATTR            35  'send_event'
        2194  LOAD_CONST           42  'E_HIDE_FULLBODY_ANIMATION'
        2197  CALL_FUNCTION_1       1 
        2200  POP_TOP          

 941    2201  LOAD_FAST            23  'control_target'
        2204  LOAD_ATTR            54  'logic'
        2207  LOAD_ATTR            89  'ev_g_model'
        2210  CALL_FUNCTION_0       0 
        2213  STORE_FAST           27  'model'

 942    2216  LOAD_GLOBAL          16  'global_data'
        2219  LOAD_ATTR            90  'debug_gpu_skin'
        2222  POP_JUMP_IF_FALSE  2262  'to 2262'
        2225  LOAD_FAST            27  'model'
        2228  POP_JUMP_IF_FALSE  2262  'to 2262'
        2231  LOAD_GLOBAL          60  'hasattr'
        2234  LOAD_FAST            27  'model'
        2237  LOAD_CONST           43  'enable_debug_skin'
        2240  CALL_FUNCTION_2       2 
      2243_0  COME_FROM                '2228'
      2243_1  COME_FROM                '2222'
        2243  POP_JUMP_IF_FALSE  2262  'to 2262'

 943    2246  LOAD_FAST            27  'model'
        2249  LOAD_ATTR            91  'enable_debug_skin'
        2252  LOAD_GLOBAL          15  'True'
        2255  CALL_FUNCTION_1       1 
        2258  POP_TOP          
        2259  JUMP_FORWARD          0  'to 2262'
      2262_0  COME_FROM                '2259'

 945    2262  LOAD_GLOBAL          86  'print'
        2265  LOAD_CONST           44  'test--model.filename ='
        2268  LOAD_FAST            27  'model'
        2271  LOAD_ATTR            92  'filename'
        2274  LOAD_CONST           45  '--entity_id ='
        2277  LOAD_FAST            23  'control_target'
        2280  LOAD_ATTR            57  'id'
        2283  CALL_FUNCTION_4       4 
        2286  POP_TOP          
        2287  JUMP_ABSOLUTE      2580  'to 2580'

 948    2290  LOAD_GLOBAL          86  'print'
        2293  LOAD_CONST           46  'test--VK_B--step2--control_target ='
        2296  LOAD_FAST            23  'control_target'
        2299  LOAD_CONST           36  '--control_target.logic ='
        2302  LOAD_FAST            23  'control_target'
        2305  LOAD_ATTR            54  'logic'
        2308  BUILD_TUPLE_4         4 
        2311  CALL_FUNCTION_1       1 
        2314  POP_TOP          

 956    2315  LOAD_FAST             8  'player'
        2318  LOAD_ATTR            35  'send_event'
        2321  LOAD_CONST           38  'E_DUMP_STATE'
        2324  CALL_FUNCTION_1       1 
        2327  POP_TOP          

 957    2328  LOAD_FAST             8  'player'
        2331  LOAD_ATTR            35  'send_event'
        2334  LOAD_CONST           39  'E_CHARACTER_ATTR'
        2337  LOAD_CONST           40  'animator_info'
        2340  LOAD_GLOBAL          15  'True'
        2343  CALL_FUNCTION_3       3 
        2346  POP_TOP          

 959    2347  LOAD_FAST             8  'player'
        2350  LOAD_ATTR            35  'send_event'
        2353  LOAD_CONST           39  'E_CHARACTER_ATTR'
        2356  LOAD_CONST           41  'dump_character'
        2359  LOAD_CONST            5  1
        2362  CALL_FUNCTION_3       3 
        2365  POP_TOP          

 960    2366  LOAD_FAST             8  'player'
        2369  LOAD_ATTR            89  'ev_g_model'
        2372  CALL_FUNCTION_0       0 
        2375  STORE_FAST           27  'model'

 961    2378  LOAD_FAST            27  'model'
        2381  LOAD_ATTR            93  'world_rotation_matrix'
        2384  STORE_FAST           28  'model_rotation_matrix'

 962    2387  LOAD_FAST             8  'player'
        2390  LOAD_ATTR            55  'ev_g_control_target'
        2393  CALL_FUNCTION_0       0 
        2396  STORE_FAST           23  'control_target'

 963    2399  LOAD_FAST            23  'control_target'
        2402  LOAD_ATTR            54  'logic'
        2405  LOAD_ATTR            89  'ev_g_model'
        2408  CALL_FUNCTION_0       0 
        2411  STORE_FAST           29  'target_model'

 964    2414  LOAD_FAST            29  'target_model'
        2417  LOAD_ATTR            93  'world_rotation_matrix'
        2420  STORE_FAST           30  'target_model_rotation_matrix'

 965    2423  LOAD_FAST            28  'model_rotation_matrix'
        2426  LOAD_ATTR            34  'yaw'
        2429  STORE_FAST           31  'model_yaw'

 966    2432  LOAD_FAST            30  'target_model_rotation_matrix'
        2435  LOAD_ATTR            34  'yaw'
        2438  STORE_FAST           32  'target_model_yaw'

 967    2441  LOAD_FAST            31  'model_yaw'
        2444  LOAD_FAST            32  'target_model_yaw'
        2447  BINARY_SUBTRACT  
        2448  STORE_FAST           33  'diff_model_yaw'

 968    2451  LOAD_FAST            31  'model_yaw'
        2454  LOAD_GLOBAL          16  'global_data'
        2457  LOAD_ATTR            94  'cam_data'
        2460  LOAD_ATTR            34  'yaw'
        2463  BINARY_SUBTRACT  
        2464  STORE_FAST           34  'diff_cam_yaw'

 969    2467  LOAD_GLOBAL          86  'print'
        2470  LOAD_CONST           47  'test--diff_model_yaw ='
        2473  LOAD_FAST            33  'diff_model_yaw'
        2476  LOAD_CONST           48  '--diff_cam_yaw ='
        2479  LOAD_FAST            34  'diff_cam_yaw'
        2482  LOAD_CONST           49  '--diff_cam_angle ='
        2485  LOAD_FAST             4  'math'
        2488  LOAD_ATTR            95  'degrees'
        2491  LOAD_FAST            34  'diff_cam_yaw'
        2494  CALL_FUNCTION_1       1 
        2497  LOAD_CONST           50  '--model_yaw ='
        2500  LOAD_FAST            31  'model_yaw'
        2503  LOAD_CONST           51  '--global_data.cam_data.yaw ='
        2506  LOAD_GLOBAL          16  'global_data'
        2509  LOAD_ATTR            94  'cam_data'
        2512  LOAD_ATTR            34  'yaw'
        2515  LOAD_CONST           52  '--target_model_yaw ='
        2518  LOAD_FAST            32  'target_model_yaw'
        2521  LOAD_CONST           53  '--model.filename ='
        2524  LOAD_FAST            29  'target_model'
        2527  LOAD_ATTR            92  'filename'
        2530  LOAD_CONST           54  '--target_model.filename ='
        2533  LOAD_FAST            27  'model'
        2536  LOAD_ATTR            92  'filename'
        2539  LOAD_CONST           55  '--model.world_position ='
        2542  LOAD_FAST            27  'model'
        2545  LOAD_ATTR            96  'world_position'
        2548  LOAD_CONST           45  '--entity_id ='
        2551  LOAD_FAST            23  'control_target'
        2554  LOAD_ATTR            57  'id'
        2557  BUILD_TUPLE_20       20 
        2560  CALL_FUNCTION_1       1 
        2563  POP_TOP          

 970    2564  LOAD_FAST             8  'player'
        2567  LOAD_ATTR            35  'send_event'
        2570  LOAD_CONST           42  'E_HIDE_FULLBODY_ANIMATION'
        2573  CALL_FUNCTION_1       1 
        2576  POP_TOP          
        2577  JUMP_FORWARD          0  'to 2580'
      2580_0  COME_FROM                '2577'

 977    2580  LOAD_FAST             3  'game'
        2583  LOAD_ATTR            97  'VK_Z'
        2586  LOAD_FAST             2  'keycode'
        2589  COMPARE_OP            2  '=='
        2592  POP_JUMP_IF_FALSE  2688  'to 2688'

 978    2595  LOAD_GLOBAL          86  'print'
        2598  LOAD_CONST           56  'test--VK_Z'
        2601  CALL_FUNCTION_1       1 
        2604  POP_TOP          

 979    2605  LOAD_GLOBAL          16  'global_data'
        2608  LOAD_ATTR            53  'player'
        2611  STORE_FAST           24  'debug_target'

 980    2614  LOAD_GLOBAL          16  'global_data'
        2617  LOAD_ATTR            53  'player'
        2620  LOAD_ATTR            54  'logic'
        2623  LOAD_ATTR            55  'ev_g_control_target'
        2626  CALL_FUNCTION_0       0 
        2629  STORE_FAST           23  'control_target'

 981    2632  LOAD_FAST            23  'control_target'
        2635  POP_JUMP_IF_FALSE  2666  'to 2666'
        2638  LOAD_FAST            23  'control_target'
        2641  LOAD_ATTR            54  'logic'
        2644  LOAD_ATTR            75  'MASK'
        2647  LOAD_GLOBAL          76  'preregistered_tags'
        2650  LOAD_ATTR            77  'MECHA_VEHICLE_TAG_VALUE'
        2653  BINARY_AND       
      2654_0  COME_FROM                '2635'
        2654  POP_JUMP_IF_FALSE  2666  'to 2666'

 982    2657  LOAD_FAST            23  'control_target'
        2660  STORE_FAST           24  'debug_target'
        2663  JUMP_FORWARD          0  'to 2666'
      2666_0  COME_FROM                '2663'

 984    2666  LOAD_FAST            24  'debug_target'
        2669  LOAD_ATTR            54  'logic'
        2672  LOAD_ATTR            35  'send_event'
        2675  LOAD_CONST           57  'E_REVERT_FULLBODY_ANIMATION'
        2678  CALL_FUNCTION_1       1 
        2681  POP_TOP          
        2682  JUMP_ABSOLUTE      2688  'to 2688'
        2685  JUMP_FORWARD          0  'to 2688'
      2688_0  COME_FROM                '2685'
      2688_1  COME_FROM                '1661'
        2688  LOAD_CONST            0  ''
        2691  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 1134

    def is_valid_down_speed_mode(self):
        return self.cur_camera_state_type == AIM_MODE and self.cur_aim_lens in weapon_const.aim_type_dict

    def get_scale_base_val(self):
        base_val = 1.0
        if self._cur_mecha_type_id:
            if self.cur_camera_state_type == AIM_MODE:
                if self._cur_mecha_screen_scoped_sens_val:
                    base_val = self._cur_mecha_screen_scoped_sens_val
                elif self.cur_aim_lens and self.cur_aim_lens in weapon_const.aim_type_dict:
                    setting_key = weapon_const.aim_type_dict[self.cur_aim_lens]
                    base_val = self.sst_setting_map[setting_key][uoc.SST_IDX_BASE]
            elif self._cur_mecha_screen_sp_form_sens_val and global_data.mecha and global_data.mecha.logic and global_data.mecha.logic.sd.ref_use_mecha_special_form_sensitivity:
                base_val = self._cur_mecha_screen_sp_form_sens_val
            elif self._cur_mecha_screen_sens_val:
                base_val = self._cur_mecha_screen_sens_val
            elif uoc.SST_SCR_KEY in self.sst_setting_map:
                base_val = self.sst_setting_map[uoc.SST_SCR_KEY][uoc.SST_IDX_BASE]
        elif self.cur_camera_state_type == AIM_MODE:
            if self.cur_aim_lens and self.cur_aim_lens in weapon_const.aim_type_dict:
                setting_key = weapon_const.aim_type_dict[self.cur_aim_lens]
                base_val = self.sst_setting_map[setting_key][uoc.SST_IDX_BASE]
        elif uoc.SST_SCR_KEY in self.sst_setting_map:
            base_val = self.sst_setting_map[uoc.SST_SCR_KEY][uoc.SST_IDX_BASE]
        return base_val

    def modify_rotate_dist_by_sensitivity(self, x_delta, y_delta, pos):
        win_w, win_h = global_data.ui_mgr.slide_screen_size.width, global_data.ui_mgr.slide_screen_size.height
        base_val = self.get_scale_base_val()
        if self.cur_camera_state_type == AIM_MODE:
            if self.cur_aim_lens is None:
                log_error('[PartCtrl] There is not lens when get aim rocker move!')
                return (
                 x_delta, y_delta)
            if self.cur_aim_lens not in weapon_const.aim_type_dict:
                log_error('Unsupport lens!')
            setting_key = weapon_const.aim_type_dict.get(self.cur_aim_lens, uoc.SST_AIM_RD_KEY)
            settings = self.sst_setting_map[setting_key]
            x_scale = settings[uoc.SST_IDX_RIGHT] if pos.x > win_w / 2.0 else settings[uoc.SST_IDX_LEFT]
            x_delta *= base_val * x_scale
            y_scale = settings[uoc.SST_IDX_UP] if pos.y > win_h / 2.0 else settings[uoc.SST_IDX_DOWN]
            y_delta *= base_val * y_scale
            if self._enable_adapt_scope_times:
                cam_state = self.scene().get_com('PartCamera').cam_manager.cam_state
                get_magnification_triplet = getattr(cam_state, '_get_magnification_triplet', None)
                if callable(get_magnification_triplet):
                    cur_times, min_times, max_times = get_magnification_triplet()
                    times_scale = min_times / cur_times
                    x_delta *= times_scale
                    y_delta *= times_scale
        elif uoc.SST_SCR_KEY in self.sst_setting_map:
            settings = self.sst_setting_map[uoc.SST_SCR_KEY]
            x_scale = settings[uoc.SST_IDX_SCR_LEFT_RIGHT_2] if pos.x > win_w / 2.0 else settings[uoc.SST_IDX_SCR_LEFT_RIGHT]
            x_delta *= base_val * x_scale
            y_scale = settings[uoc.SST_IDX_UP]
            y_delta *= base_val * y_scale
        return (x_delta, y_delta)

    def on_sst_common_changed(self, sst_type, settings):
        self.sst_setting_map[sst_type] = settings

    def on_camera_switch_to_state(self, state, *args):
        scn = self.scene()
        player = scn.get_player()
        self.cur_camera_state_type = state
        if player and self.cur_camera_state_type == AIM_MODE:
            target = player.ev_g_control_target()
            if target and target.logic and target.logic.MASK & preregistered_tags.MECHA_VEHICLE_TAG_VALUE:
                self.cur_aim_lens = target.logic.ev_g_aim_lens()
                if not self.cur_aim_lens:
                    len_attr_data = player.ev_g_attachment_attr(1)
                    if len_attr_data:
                        self.cur_aim_lens = len_attr_data.get('iType')
            else:
                len_attr_data = player.ev_g_attachment_attr(1)
                if len_attr_data:
                    self.cur_aim_lens = len_attr_data.get('iType')
        else:
            self.cur_aim_lens = None
        return

    def on_app_lost_focus(self):
        pass

    def update_control_target_status(self, player):
        if player:
            cur_control_target = player.ev_g_control_target()
            self.on_switch_control_target(cur_control_target.id, None)
        return

    def on_switch_control_target(self, target_id, pos, *args):
        target = EntityManager.getentity(target_id)
        self.update_world_zhujue(target_id)
        if target and target.logic and target.logic.is_valid():
            if target.__class__.__name__ == 'Mecha':
                self._cur_mecha_type_id = target.logic.share_data.ref_mecha_id
            else:
                self._cur_mecha_type_id = None
            self._update_cur_mecha_screen_sens_val()
        return

    def setup_control_target_event(self, target, is_bind):
        if target and target.is_valid():
            if is_bind:
                ope_func = target.regist_event
                ope_func('E_ON_CONTROL_TARGET_CHANGE', self.on_switch_control_target, 10)
            else:
                ope_func = target.unregist_event
                ope_func('E_ON_CONTROL_TARGET_CHANGE', self.on_switch_control_target)

    BATTLE_STAGE_UIS = ('MoveRockerUI',
     'ThrowRockerUI',
     'PostureControlUI',
     'BattleControlUIPC',
     'FightLeftShotUI',
     'FireRockerUI',
     'BulletReloadUI',
     'QuickMarkBtn',
     'AimRockerUI',
     'SceneInteractionUI',
     'GMHelperUI',
     'MechaControlMain',
     'MechaCancelUI')

    def on_camera_target_setted(self, *args):
        hidden = global_data.cam_lplayer is None or global_data.cam_lplayer.id != global_data.player.id
        from logic.gutils.template_utils import set_ui_list_visible_helper
        set_ui_list_visible_helper(self.BATTLE_STAGE_UIS, not hidden, 'OBSERVE')
        if not self.sst_setting_map:
            self.init_sst_setting_map()
        return

    def show_settle_stage_ui(self, *args):
        pass

    def on_camera_targetted_setted(self):
        self.update_world_zhujue(global_data.cam_lctarget.id if global_data.cam_lctarget else None)
        return

    def _on_scene_observed_player_setted_event(self, lplayer):
        stage = parachute_utils.STAGE_NONE
        if lplayer:
            stage = lplayer.share_data.ref_parachute_stage
        self._update_related_uis_visibiity(stage)

    def _on_mecha_sens_val_changed(self, mecha_id, val_key):
        if self._cur_mecha_type_id != mecha_id:
            return
        else:
            if val_key is None or val_key == uoc.SST_SCR_MECHA_VAL_KEY or val_key == uoc.SST_SCR_SCOPE_MECHA_VAL_KEY or val_key == uoc.SST_SCR_SPECIAL_FORM_MECHA_VAL_KEY:
                self._update_cur_mecha_screen_sens_val()
            return

    def _update_cur_mecha_screen_sens_val(self):
        if not self._cur_mecha_type_id:
            self._cur_mecha_screen_sens_val = None
            self._cur_mecha_screen_scoped_sens_val = None
            self._cur_mecha_screen_sp_form_sens_val = None
            self._scope_sensitivity_opened = False
            self._scope_main_weapon_sensitivity_opened = False
            self._scope_sub_weapon_sensitivity_opened = False
            self._special_form_sensitivity_opened = False
            self._special_form_main_weapon_sensitivity_opened = False
            self._special_form_sub_weapon_sensitivity_opened = False
        else:
            from logic.gutils import mecha_utils
            from data import mecha_sens_open_scheme
            mecha_id = self._cur_mecha_type_id
            self._cur_mecha_screen_sens_val = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SCR_MECHA_VAL_KEY)
            self._scope_sensitivity_opened = mecha_sens_open_scheme.check_scope_sensitivity_opened(mecha_id)
            if self._scope_sensitivity_opened:
                self._cur_mecha_screen_scoped_sens_val = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SCR_SCOPE_MECHA_VAL_KEY)
            self._scope_main_weapon_sensitivity_opened = mecha_sens_open_scheme.check_scope_main_weapon_sensitivity_opened(mecha_id)
            self._scope_sub_weapon_sensitivity_opened = mecha_sens_open_scheme.check_scope_sub_weapon_sensitivity_opened(mecha_id)
            self._special_form_sensitivity_opened = mecha_sens_open_scheme.check_special_form_sensitivity_opened(mecha_id)
            if self._special_form_sensitivity_opened:
                self._cur_mecha_screen_sp_form_sens_val = mecha_utils.get_mecha_sens_setting_val(mecha_id, uoc.SST_SCR_SPECIAL_FORM_MECHA_VAL_KEY)
            self._special_form_main_weapon_sensitivity_opened = mecha_sens_open_scheme.check_special_form_main_weapon_sensitivity_opened(mecha_id)
            self._special_form_sub_weapon_sensitivity_opened = mecha_sens_open_scheme.check_special_form_sub_weapon_sensitivity_opened(mecha_id)
        return

    def set_temporary_mecha_screen_sens_val(self, val):
        if self._cur_mecha_screen_sens_val:
            self._cur_mecha_screen_sens_val = val

    def update_world_zhujue(self, target_id):
        target = EntityManager.getentity(target_id)
        original_target = EntityManager.getentity(global_data.ctrl_target_id)
        if original_target and original_target.logic and original_target.logic.is_valid():
            original_target.logic.send_event('S_ZHUJUE_MODEL', False)
        if target and target.logic and target.logic.is_valid():
            global_data.ctrl_target_id = target_id
            target.logic.send_event('S_ZHUJUE_MODEL', True)

    def on_touch_begin(self, touches):
        self.touching_scene = True
        global_data.emgr.scene_on_touched.emit(True)

    def on_touch_end(self, touches):
        self.touching_scene = False
        global_data.emgr.scene_on_touched.emit(False)

    def is_touching_scene(self):
        return self.touching_scene

    def on_double_click_mark_changed(self):
        if global_data.player:
            self._enable_double_click_mark = str(global_data.player.get_setting_2(uoc.DOUBLE_CLICK_MARK_KEY)) == str(True)