# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartBattle.py
from __future__ import absolute_import
import six
from . import ScenePart
from logic.gcommon.common_utils import battle_utils
from logic.comsys.battle.ShieldBloodUI import ShieldBloodUI
from logic.gcommon.common_utils import parachute_utils as putils
from common.uisys.basepanel import MECHA_AIM_UI_LSIT
from logic.gcommon.item import item_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.collision_const import CHARACTER_STAND_HEIGHT, CHARACTER_STAND_WIDTH, MECHA_STAND_HEIGHT, MECHA_STAND_WIDTH
from logic.comsys.battle.Settle import settle_system_utils
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.gutils.skate_appearance_utils import reset_skate_entity_id_recorder
from logic.client.const import game_mode_const
import collision
import math3d
import game3d
import time
from logic.gutils import scene_utils
from common.platform.perform_sdk import refresh_team_battle_info, battle_begin
HIDE_UI = ('BattleRightTopUI', 'ScalePlateUI', 'BattleFightCapacity')

class PartBattle(ScenePart.ScenePart):
    INIT_EVENT = {'show_death_replay_event': 'show_death_replay_ui',
       'settle_stage_event': '_create_settle_stage_ui',
       'celebrate_win_stage_event': 'on_celebrate_win_stage',
       'end_celebrate_win_state_event': 'on_end_celebrate_win_state',
       'judge_ob_settle_event': 'create_judge_ob_settle_ui',
       'battle_logic_ready_event': 'on_enter_battle',
       'scene_observed_player_setted_event': 'on_enter_observed',
       'on_observer_parachute_stage_changed': 'on_observer_parachute_stage_changed',
       'on_player_parachute_stage_changed': 'on_player_parachute_stage_changed',
       'weapon_bar_ui_ope_change_event': 'on_switch_weapon_bar_ope',
       'player_armor_changed': 'on_armor_changed',
       'net_disconnect_event': 'on_disconnect',
       'check_out_block_event': 'check_out_block_position'
       }

    def __init__(self, scene, name):
        super(PartBattle, self).__init__(scene, name)
        self.effect_id_list = []
        self._origin_z_range = None
        self._delay_timer = None
        self._poison_manager = None
        self._ccmini_aoi_manager = None
        self._battle_sound_ai_mgr = None
        self._last_check_time = 0
        self._settle_stage_ui_start_time_stamp = 0
        from logic.comsys.battle.Settle.SettleSystem import SettleSystem
        SettleSystem.finalize()
        global_data.ui_mgr.close_ui('EndEntireTeamUI')
        from logic.vscene import scene_type
        global_data.scene_type = scene_type.SCENE_TYPE_BATTLE
        if not global_data.anticheatsdk_mgr:
            from common.platform.AntiCheatSDKMgr import AntiCheatSDKMgr
            anticheat_sdk = AntiCheatSDKMgr()
            anticheat_sdk.init_acsdk()
            anticheat_sdk.set_acsdk_roleinfo()
        global_data.sound_mgr.close_ios_check_sys_mute()
        from logic.comsys.battle.BattleCheckPos import BattleCheckPos
        BattleCheckPos()
        global_data.battle_check_pos.reinit()
        from logic.comsys.battle.AimTransparentManager import AimTransparentManager
        AimTransparentManager()
        return

    def on_pre_load(self):
        module_path = 'logic.comsys.battle'
        module_path2 = 'logic.comsys.battle.BattleInfo'
        module_path3 = 'logic.comsys.mecha_display'
        module_mecha = 'logic.comsys.mecha_ui'
        module_common = 'logic.comsys.common_ui'
        module_chat = 'logic.comsys.chat'
        module_map = 'logic.comsys.map'
        self._part_ui_list = [
         (
          True, 'ScalePlateUI', module_map, ()),
         (
          True, 'NewChatPigeon', module_chat, ()),
         (
          True, 'FightSightUI', module_path, ()),
         (
          True, self._get_weapon_bar_name(), module_path, ()),
         (
          True, 'BattleBuffUI', module_path, ()),
         (
          True, 'BattleInfoMessageVisibleUI', module_path2, ()),
         (
          True, 'HpInfoUI', module_path, ()),
         (
          True, 'DrugUI', module_path, ()),
         (
          True, 'BattleRightTopUI', module_path2, ()),
         (
          True, 'BattleLeftBottomUI', module_path2, ()),
         (
          True, 'MechaChargeUI', module_path, ()),
         (
          True, 'MonsterBloodUI', module_path, ()),
         (
          True, 'FightStateUI', module_path, ()),
         (
          True, 'InjureInfoUI', module_path, ()),
         (
          True, 'InjureInfo3DUI', module_path, ()),
         (
          True, 'LobbyItemDescUI', module_path3, ()),
         (
          True, 'ModeNameUI', module_path, ()),
         (
          True, 'BattleScreenMarkUI', module_path, ()),
         (
          True, 'BattleBroadcastUI', module_path, ())]
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_GULAG_SURVIVAL):
            self._part_ui_list.append((True, 'GulagBattleInfoUI', module_path, ()))
        else:
            self._part_ui_list.append((True, 'BattleInfoUI', module_path, ()))
        if True:
            self._part_ui_list += [
             (
              False, 'MechaControlMain', module_mecha, ()),
             (
              False, 'MechaFuelUI', module_mecha, ()),
             (
              False, 'MechaHpInfoUI', module_mecha, ()),
             (
              False, 'MechaBuffUI', module_mecha, ()),
             (
              False, 'MechaCockpitUI', module_mecha, ()),
             (
              False, 'NetworkLagUI', module_common, ()),
             (
              False, 'MechaWarningUI', module_mecha, ())]
        if battle_utils.is_signal_logic() and not global_data.is_32bit:
            self._part_ui_list += [(False, 'BattleSignalInfoUI', module_path, ())]
        if not global_data.is_pc_mode:
            self._part_ui_list += [
             (
              True, 'SurviveInfoUI', module_path, ())]
        is_survivals = global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS)
        if is_survivals:
            extra = [
             (
              True, 'RogueGiftTopRightUI', module_path, ()),
             (
              True, 'DoubleMarkBlockUI', module_path, ()),
             (
              True, 'SoundVisibleUI', module_path, ()),
             (
              True, 'SoundVisible3DUI', module_path, ()),
             (
              True, 'FightBagUI', module_path, ()),
             (
              True, 'BattleFightMeow', module_path2, ())]
            self._part_ui_list.extend(extra)
        if global_data.game_mode and global_data.game_mode.is_ace_coin_enable():
            self._part_ui_list.extend([(True, 'BattleFightCapacity', module_path2, ())])
        if global_data.game_mode and global_data.game_mode.get_mode_type() in game_mode_const.GAME_MODE_DEATHS:
            self._part_ui_list.extend([(True, 'OnHookUI', module_path, ())])
        if global_data.game_mode and global_data.game_mode.get_mode_type() in game_mode_const.GAME_MODE_ROGUES:
            extra = [(True, 'DeathRogueGiftTopRightUI', module_path, ())]
            self._part_ui_list.extend(extra)
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SCAVENGE):
            extra = [(True, 'FightBagUI', module_path, ())]
            self._part_ui_list.extend(extra)
        if global_data.game_mode and global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_PVE, game_mode_const.GAME_MODE_PVE_EDIT)):
            extra = [(True, 'FightBagUI', module_path, ())]
            self._part_ui_list.extend(extra)
        self.add_to_loading_wrapper()

    def load_ui_per_frame(self, dont_load=False):
        if not global_data.battle:
            return True
        return super(PartBattle, self).load_ui_per_frame(dont_load)

    def on_load(self):
        self.on_create_part_ui()
        self.create_ccmini_aoi()

    def on_enter(self):
        import world
        if scene_utils.need_game_mode_outline():
            scene_utils.set_outline_process_enable(True, scene_utils.GAME_MODE_OUTLINE_MASK)
        self.create_poison_circle()
        if global_data.is_pc_mode:
            global_data.pc_ctrl_mgr.enable_PC_control(True)
        else:
            self.open_keyboard_control()
        reset_skate_entity_id_recorder()
        if hasattr(world, 'enable_update_budget'):
            world.enable_update_budget(False)
        if global_data.is_pc_mode:
            import nxapp
            if hasattr(nxapp, 'set_allow_shortKey_vk_win'):
                nxapp.set_allow_shortKey_vk_win(False)
            if hasattr(nxapp, 'set_allow_accessibility_shortcut_keys'):
                nxapp.set_allow_accessibility_shortcut_keys(False)
        if global_data.enable_perform_sdk:
            battle_begin()
            self.need_update = True
            self._last_check_time = time.time()
        global_data.battle_check_pos and global_data.battle_check_pos.check_pos_switch(True)
        self.check_start_musdk_checker()
        if global_data.is_inner_server:
            from sunshine.MontageEditor.MontageEditor import MontageEditor
            montage_editor = MontageEditor()
            montage_editor.setup_montage()
            montage_editor.on_scene_ready()

    def on_update(self, dt):
        super(PartBattle, self).on_update(dt)
        if global_data.enable_perform_sdk and time.time() - self._last_check_time > 5:
            self._last_check_time = time.time()
            refresh_team_battle_info()

    def on_exit(self):
        import world
        scene_utils.clear_outline_process()
        global_data.battle_check_pos.on_finalize()
        self.destroy_ui()
        self.destroy_poison_circle()
        self.destroy_ccmini_aoi()
        self.clear_timer()
        self.clear_effect()
        if global_data.is_pc_mode:
            if global_data.pc_ctrl_mgr:
                global_data.pc_ctrl_mgr.enable_PC_control(False)
        if hasattr(world, 'enable_update_budget'):
            world.enable_update_budget(False)
        if global_data.is_pc_mode:
            import nxapp
            if hasattr(nxapp, 'set_allow_shortKey_vk_win'):
                nxapp.set_allow_shortKey_vk_win(True)
            if hasattr(nxapp, 'set_allow_accessibility_shortcut_keys'):
                nxapp.set_allow_accessibility_shortcut_keys(True)
        if global_data.freefly_camera_mgr:
            global_data.freefly_camera_mgr.finalize()
        if global_data.move_rocker_simple:
            global_data.move_rocker_simple.finalize()
        if global_data.aim_transparent_mgr:
            global_data.aim_transparent_mgr.finalize()
        global_data.player and global_data.player.do_pending_survey()
        global_data.battle_check_pos and global_data.battle_check_pos.check_pos_switch(False)
        if global_data.feature_mgr.is_support_set_frametime():
            import render
            render.set_frametime(0)
        if global_data.montage_editor:
            global_data.montage_editor.finalize()

    def clear_timer(self):
        if self._delay_timer:
            global_data.game_mgr.get_post_logic_timer().unregister(self._delay_timer)
            self._delay_timer = None
        return

    def show_death_replay_ui(self, battle_type, group_num, settle_dict):
        from logic.comsys.battle.Settle.SettleSystem import SettleSystem
        replay_data = settle_dict.get('reply_data', {})
        SettleSystem().show_end_death_replay(group_num, replay_data)

    def game_over(self):
        from logic.comsys.battle.BattleUtils import stop_self_fire_and_movement
        stop_self_fire_and_movement()

    def _create_settle_stage_ui(self, *args):
        global_data.ui_mgr.close_ui('EndContinueUI')
        global_data.ui_mgr.close_ui('EndDeathReplayUI')
        if global_data.game_mgr.get_global_speed_rate() < 1.0:
            global_data.game_mgr.set_global_speed_rate(1.0)
        self.clear_timer()
        battle_type, group_num, settle_dict, battle_reward, team_dict, enemy_dict, achievement, total_fighter_num = args
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_RECOVER_KILLER_CAM')
            if not global_data.player.logic.ev_g_death() and not settle_dict.get('escape_battle', False) and not global_data.player.logic.ev_g_defeated():
                if global_data.mecha and global_data.mecha.logic:
                    global_data.mecha.logic.send_event('E_PLAY_VICTORY_CAMERA')
                global_data.player.logic.send_event('E_PLAY_VICTORY_CAMERA')
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.enable_PC_control(False)
        quit_from_spectate = settle_dict.get('quit_from_spectate', False)
        is_in_spectate = False
        if not global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_SURVIVALS,)):
            if global_data.player and global_data.player.logic:
                is_in_spectate = global_data.player.is_in_global_spectate() or global_data.player.logic.ev_g_is_in_spectate()
        if quit_from_spectate or is_in_spectate:
            self.close_ui_for_settle_sage()
            self.create_settle_stage_ui(*args)
        else:
            from common.utils import timer
            self._delay_timer = global_data.game_mgr.get_post_logic_timer().register(func=lambda : self.create_settle_stage_ui(*args), interval=2 * global_data.game_mgr.get_global_speed_rate(), times=1, mode=timer.CLOCK)

    def create_settle_stage_ui(self, battle_type, group_num, settle_dict, battle_reward, team_dict, enemy_dict, achievement, total_fighter_num):
        if global_data.game_mgr.get_global_speed_rate() < 1.0:
            global_data.game_mgr.set_global_speed_rate(1.0)
        self.game_over()
        statistics = settle_dict.get('statistics', {})
        move_dist = statistics.get('move_dist', 0)
        global_data.emgr.update_mileage_event.emit(int(move_dist))
        from logic.comsys.battle.Settle.SettleSystem import SettleSystem
        if battle_reward is None:
            replay_data = settle_dict.get('reply_data', {})
            SettleSystem().show_settle_teammate_alive(group_num, replay_data)
        else:
            from common.cfg import confmgr
            teammate_num = confmgr.get('battle_config', str(battle_type), default={}).get('cTeamNum', 1)
            SettleSystem().show_settle_final(group_num, settle_dict, battle_reward, teammate_num, team_dict, enemy_dict, achievement, total_fighter_num)
        return

    def on_celebrate_win_stage(self):
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.enable_PC_control(global_data.pc_ctrl_mgr.is_pc_control_enable())
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_EXIT_FOCUS_CAMERA')
            if global_data.mecha and global_data.mecha.logic:
                global_data.mecha.logic.send_event('E_EXIT_FOCUS_CAMERA')
        global_data.ui_mgr.close_ui('BattleSignalInfoUI')
        global_data.emgr.scene_clear_poison_circle_event.emit()
        self.create_fireworks_sfx()

    def on_end_celebrate_win_state(self):
        self.clear_effect()

    def clear_effect(self):
        for effect_id in self.effect_id_list:
            global_data.sfx_mgr.remove_sfx_by_id(effect_id)

        self.effect_id_list = []

    def create_fireworks_sfx(self):
        from logic.gutils import scene_utils
        self.clear_effect()
        if global_data.player:
            pos = global_data.player.logic.ev_g_position()
            sfx_paths = scene_utils.get_fireworks_path()
            for paths in sfx_paths:
                for path in paths:
                    fireworks_sfx = global_data.sfx_mgr.create_sfx_in_scene(path, pos=pos)
                    self.effect_id_list.append(fireworks_sfx)

    def create_judge_ob_settle_ui(self):

        def _next_step():
            self.close_ui_for_settle_sage()
            from logic.comsys.battle.Settle.SettleSystem import SettleSystem
            from common.utils import timer
            SettleSystem().show_judge_ob_settle()

        if global_data.is_in_judge_camera:
            global_data.emgr.try_switch_judge_camera_event.emit(False, is_force=True)
        self.game_over()
        global_data.emgr.camera_cancel_all_trk.emit()
        winner_names = []
        rank = self.get_rank()
        battle = global_data.player.get_battle()
        if battle and battle.ob_settle_info:
            team_settle_dict = battle.ob_settle_info[rank - 1]
            team_member_info_dict = team_settle_dict.get('member_info', {})
            for i, (key, member_info) in enumerate(six.iteritems(team_member_info_dict)):
                member_name = member_info.get('char_name', '')
                winner_names.append(member_name)

            from logic.comsys.observe_ui.BattleWinnersUI import BattleWinnersUI
            BattleWinnersUI()
            ui_inst = global_data.ui_mgr.get_ui('BattleWinnersUI')
            if ui_inst:
                ui_inst.set_winner_names(winner_names, rank)
                ui_inst.set_exit_callback(_next_step)
        else:
            _next_step()

    def get_rank(self):
        rank = 2 if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_death() else 1
        ob_id = global_data.cam_lplayer.id if global_data.cam_lplayer and global_data.cam_lplayer.id else None
        battle = global_data.player.get_battle()
        if ob_id and battle and battle.ob_settle_info:
            for team_settle_dict in battle.ob_settle_info:
                team_member_info_dict = team_settle_dict.get('member_settle_dict', {})
                ob_member_info = team_member_info_dict.get(ob_id, None)
                if ob_member_info:
                    rank = team_settle_dict.get('rank', rank)
                    break

        return rank

    def close_ui_for_settle_sage(self):
        if global_data.game_mgr.get_global_speed_rate() < 1.0:
            global_data.game_mgr.set_global_speed_rate(1.0)
        global_data.ui_mgr.close_all_ui(exceptions=(
         'BattleInfoUI',
         'HpInfoUI',
         'TeammateUI',
         'DrugUI',
         'BattleInfoMessageVisibleUI',
         'WeaponBarSelectUI',
         'RogueGiftTopRightUI',
         'DeathRogueGiftTopRightUI',
         'ScalePlateUI',
         'SmallMapUI',
         'FightKillNumberUI',
         'BattleRightTopUI',
         'BattleLeftBottomUI',
         'FightStateUI',
         'WizardTrace',
         'ProfileGraphUI',
         'DanmuLinesUI',
         'SoundVisibleUI',
         'SoundVisible3DUI',
         'InjureInfoUI',
         'InjureInfo3DUI',
         'BattleFightCapacity',
         'BattleFightMeow',
         'TopLevelConfirmUI2',
         'EndContinueUI',
         'EndStatisticsUI',
         'EndSceneUI',
         'SettleInteractionUI',
         'EndTransitionUI',
         settle_system_utils.get_end_exp_ui_cls().__name__,
         'EndAnimUI',
         'EndDeathReplayUI',
         'CreditReportResultFail',
         'CreditCompensateUI',
         'CreditReportResultSuccess',
         'LobbyConfirmUI2',
         'GranbelmRuneConfUI',
         'MagicRuneConfUI',
         'LobbyItemDescUI',
         'BattleSignalInfoUI',
         'FreeRecordUI',
         'BattleScreenMarkUI',
         'OnHookUI'))
        for ui_name in HIDE_UI:
            ui = global_data.ui_mgr.get_ui(ui_name)
            ui and ui.add_hide_count(self.__class__.__name__)

    def destroy_settle_stage_ui(self):
        from logic.comsys.battle.Settle.SettleSystem import SettleSystem
        settle = SettleSystem.get_instance()
        if settle is not None:
            settle.close_all_dlg()
        return

    def destroy_ui(self):
        self.on_destroy_part_ui()
        global_data.ui_mgr.close_ui('StateChangeUI')
        global_data.ui_mgr.close_ui('MechaUI')
        self.close_weapon_bar_ui()
        global_data.ui_mgr.close_ui('MobileInfoUI')
        global_data.ui_mgr.close_ui('BattleMatchUI')
        global_data.ui_mgr.close_ui('BattleReconnectUI')
        global_data.ui_mgr.close_ui('MainSettingUI')
        global_data.ui_mgr.close_ui('SecondConfirmDlg2')
        global_data.ui_mgr.close_ui('BattleGuidance')
        global_data.ui_mgr.close_ui('ShieldBloodUI')
        global_data.ui_mgr.close_ui('MechaTestSightUI')
        self.close_mecha_aim_ui()
        global_data.ui_mgr.close_ui('Mecha8004HeatUI')
        global_data.ui_mgr.close_ui('Mecha8006RushUI')
        global_data.ui_mgr.close_ui('Mecha8007SubUI')
        global_data.ui_mgr.close_ui('Mecha8007SubUI2')
        global_data.ui_mgr.close_ui('Mecha8011DragonUI')
        global_data.ui_mgr.close_ui('Mecha8014LockedUI')
        global_data.ui_mgr.close_ui('Mecha8018SubUI')
        global_data.ui_mgr.close_ui('Mecha8023SubUI')
        global_data.ui_mgr.close_ui('Mecha8024RushUI')
        global_data.ui_mgr.close_ui('Mecha8025SecondAimUI')
        global_data.ui_mgr.close_ui('Mecha8029RushUI')
        global_data.ui_mgr.close_ui('Mecha8035LockedUI')
        global_data.ui_mgr.close_ui('MechaBulletReloadUI')
        global_data.ui_mgr.close_ui('MechaJetUI')
        global_data.ui_mgr.close_ui('DummyTestUI')
        global_data.ui_mgr.close_ui('MechaExecute')
        global_data.ui_mgr.close_ui('MechaModuleSpSelectUI')
        self.destroy_settle_stage_ui()
        global_data.ui_mgr.close_ui('PrepareUI')
        global_data.ui_mgr.close_ui('AnchorVoiceTip')
        global_data.ui_mgr.close_ui('FollowDropUI')
        global_data.ui_mgr.close_ui('SOSUI')
        global_data.ui_mgr.close_ui('EndLevelUI')
        global_data.ui_mgr.close_ui('UserReportUI')
        global_data.ui_mgr.close_ui('BattleMvpUI')
        global_data.ui_mgr.close_ui('JudgeLoadingUI')
        global_data.ui_mgr.close_ui('JudgeObSettleUI')
        global_data.ui_mgr.close_ui('TitleContainerUI')
        global_data.ui_mgr.close_ui('PlayerListLoadingWidget')
        global_data.ui_mgr.close_ui('SnatchEggPlayerListLoadingWidget')
        global_data.ui_mgr.close_all_ui(exceptions=('WizardTrace', 'ProfileGraphUI',
                                                    'CreditReportResultFail', 'CreditCompensateUI',
                                                    'CreditReportResultSuccess',
                                                    'LobbyConfirmUI2', 'NormalConfirmUI2',
                                                    'FreeRecordUI', 'EndHighlightUI',
                                                    'VideoManualCtrlUI'))

    def close_mecha_aim_ui(self):
        for ui in MECHA_AIM_UI_LSIT:
            global_data.ui_mgr.close_ui(ui)

    def create_poison_circle(self):
        if not self._poison_manager:
            mgr = None
            if scene_utils.is_circle_poison():
                if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_GULAG_SURVIVAL):
                    from .GulagPoisonCircleManager import GulagPoisonCircleManager
                    mgr = GulagPoisonCircleManager()
                else:
                    from . import PoisonCircleManager
                    mgr = PoisonCircleManager.PoisonCircleManager()
            elif scene_utils.is_fixed_rect_poison():
                from . import PoisonFixedRectManager
                mgr = PoisonFixedRectManager.PoisonFixedRectManager()
            self._poison_manager = mgr
        global_data.emgr.on_scene_poision_mgr_updated.emit()
        return

    def open_keyboard_control(self):
        from logic.gutils.pc_utils import check_can_enable_pc_mode
        if not check_can_enable_pc_mode():
            return
        from logic.vscene.parts.ctrl.PCCtrlManager import PCCtrlManager
        inst = PCCtrlManager()
        global_data.pc_ctrl_mgr.enable_PC_control(False)
        inst.enable_keyboard_control(True)

    def get_poison_manager(self):
        return self._poison_manager

    def destroy_poison_circle(self):
        if self._poison_manager:
            self._poison_manager.destroy()
        self._poison_manager = None
        return

    def create_ccmini_aoi(self):
        from . import CCMiniAoiManager

    def destroy_ccmini_aoi(self):
        if self._ccmini_aoi_manager:
            self._ccmini_aoi_manager.destroy()
        self._ccmini_aoi_manager = None
        return

    def on_armor_changed(self, pos, armor):
        if pos == item_const.DRESS_POS_SHIELD:
            if armor:
                ShieldBloodUI().update_shield_info(armor)
            else:
                global_data.ui_mgr.close_ui('ShieldBloodUI')

    def on_observer_parachute_stage_changed(self, stage):
        self.on_stage_ui_changed(stage)
        self.on_stage_scene_changed(stage)

    def on_player_parachute_stage_changed(self, *args):
        self.check_prepare_ui()
        self.check_follow_drop_ui()
        self.check_need_sync_camera_for_follow()

    @execute_by_mode(True, game_mode_const.GAME_MODE_SURVIVALS)
    def check_prepare_ui(self):
        player = global_data.cam_lplayer
        from logic.gcommon.common_utils import parachute_utils
        if player and player.share_data.ref_parachute_stage in (parachute_utils.STAGE_LAUNCH_PREPARE, parachute_utils.STAGE_MECHA_READY, parachute_utils.STAGE_PLANE):
            from logic.comsys.prepare.PrepareUI import PrepareUI
            from logic.comsys.prepare.PrepareUIPC import PrepareUIPC
            if global_data.is_pc_mode:
                PrepareUIPC()
            else:
                PrepareUI()
        else:
            global_data.ui_mgr.close_ui('PrepareUI')
            global_data.ui_mgr.close_ui('MainSettingUI')

    @execute_by_mode(True, game_mode_const.GAME_MODE_SURVIVALS)
    def check_follow_drop_ui(self):
        player = global_data.cam_lplayer
        from logic.gcommon.common_utils import parachute_utils
        if player and player.share_data.ref_parachute_stage == parachute_utils.STAGE_PARACHUTE_DROP:
            if len(player.ev_g_groupmate()) > 1 and player.ev_g_parachute_follow_target() is not None:
                from logic.comsys.prepare.FollowDropUI import FollowDropUI
                ui = FollowDropUI()
                ui.set_follow_info(player)
                player.send_event('E_PARACHUTE_FOLLOW', True)
        else:
            global_data.ui_mgr.close_ui('FollowDropUI')
            if player:
                player.send_event('E_PARACHUTE_FOLLOW', False)
        return

    @execute_by_mode(True, game_mode_const.GAME_MODE_SURVIVALS)
    def check_need_sync_camera_for_follow(self):
        player = global_data.cam_lplayer
        from logic.gcommon.common_utils import parachute_utils
        if player and player.is_valid() and player.share_data.ref_parachute_stage == parachute_utils.STAGE_PARACHUTE_DROP:
            if player.ev_g_has_parachute_follower():
                player.send_event('E_HAS_PARACHUTE_FOLLOWER', True)
        elif player and player.is_valid():
            player.send_event('E_HAS_PARACHUTE_FOLLOWER', False)

    def on_stage_ui_changed(self, stage):
        if stage in (putils.STAGE_NONE, putils.STAGE_FREE_DROP, putils.STAGE_LAND, putils.STAGE_SORTIE_PREPARE):
            if not global_data.player or not global_data.cam_lplayer:
                return
        self.check_weapon_ui_visibility(stage)

    def check_weapon_ui_visibility(self, stage):
        if not global_data.player or not global_data.cam_lplayer:
            return
        if putils.is_hide_weapon_bar(stage, global_data.cam_lplayer.sd.ref_has_first_land) and not global_data.battle.is_in_island():
            self._show_weapon_bar_ui()
        else:
            self._hide_weapon_bar_ui()

    def on_stage_scene_changed(self, stage):
        if stage in (putils.STAGE_PLANE, putils.STAGE_NONE) and not global_data.battle.is_in_island():
            self.set_flying_env()
        else:
            self.set_delay_reconver()

    def on_enter_battle(self):
        from logic.comsys.battle.MobileInfoUI import MobileInfoUI
        MobileInfoUI()

    def set_delay_reconver(self):
        self.load_detail_scn()

    def load_detail_scn(self):
        scn = self.scene()
        scn.load_detail(True)

    def set_flying_env(self):
        scn = self.scene()
        self._origin_z_range = scn.active_camera.z_range

    def on_enter_observed(self, observe_target):
        hide_uis_while_observe = ('FightSightUI', 'PickUI', 'BagUI', 'BattleFightMeow')
        hide_key = self.__class__.__name__ + '_hide_uis_while_observe'
        if observe_target is None:
            for ui_name in hide_uis_while_observe:
                ui = global_data.ui_mgr.get_ui(ui_name)
                if ui:
                    ui.add_show_count(hide_key)

        else:
            self.clear_timer()
            for ui_name in hide_uis_while_observe:
                ui = global_data.ui_mgr.get_ui(ui_name)
                if ui:
                    ui.add_hide_count(hide_key)

        self.close_mecha_aim_ui()
        from logic.comsys.battle.Settle.SettleSystem import SettleSystem
        settle = SettleSystem.get_instance()
        if settle is not None:
            settle.close_all_dlg()
        from logic.comsys.battle.MobileInfoUI import MobileInfoUI
        MobileInfoUI()
        if not global_data.is_pc_mode:
            from logic.comsys.battle.SurviveInfoUI import SurviveInfoUI
            SurviveInfoUI()
        from logic.comsys.battle.BattleInfo.BattleInfoMessageVisibleUI import BattleInfoMessageVisibleUI
        BattleInfoMessageVisibleUI()
        from logic.comsys.battle.BattleBuffUI import BattleBuffUI
        from logic.comsys.battle.BattleBuffUIPC import BattleBuffUIPC
        if global_data.is_pc_mode:
            BattleBuffUIPC()
        else:
            BattleBuffUI()
        armor = observe_target.ev_g_amror_by_pos(item_const.DRESS_POS_SHIELD)
        self.on_armor_changed(item_const.DRESS_POS_SHIELD, armor)
        self.check_weapon_ui_visibility(observe_target.share_data.ref_parachute_stage)
        for ui_name in HIDE_UI:
            ui = global_data.ui_mgr.get_ui(ui_name)
            ui and ui.add_show_count(self.__class__.__name__)

        return

    def on_switch_weapon_bar_ope(self, new_ope):
        if not global_data.player or not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.id != global_data.player.id:
            return
        module_path = 'logic.comsys.battle'
        global_data.ui_mgr.show_ui('WeaponBarSelectUI', module_path)
        p_stage = global_data.cam_lplayer.share_data.ref_parachute_stage
        self.check_weapon_ui_visibility(p_stage)

    def _show_weapon_bar_ui(self):
        name = self._get_weapon_bar_name()
        from logic.gutils.template_utils import set_ui_list_visible_helper
        battle_ui_list = []
        battle_ui_list.append(name)
        set_ui_list_visible_helper(battle_ui_list, True, 'PARA')

    def _hide_weapon_bar_ui(self):
        name = self._get_weapon_bar_name()
        from logic.gutils.template_utils import set_ui_list_visible_helper
        battle_ui_list = []
        battle_ui_list.append(name)
        set_ui_list_visible_helper(battle_ui_list, False, 'PARA')

    def _get_weapon_bar_name(self):
        return 'WeaponBarSelectUI'

    def close_weapon_bar_ui(self):
        global_data.ui_mgr.close_ui('WeaponBarSelectUI')

    def on_disconnect(self, *args, **kwargs):
        import time
        global_data.last_bat_disconnect_time = time.time()

    def check_start_musdk_checker(self):
        if global_data.channel and global_data.channel.is_musdk():
            from logic.vscene.parts.ctrl.MuSdkMgr import MuSdkMgr
            MuSdkMgr()

    def check_out_block_position(self):
        player = global_data.player
        scn = self.scene()
        if not scn:
            return None
        else:
            if player and player.logic and player.logic.is_valid():
                scol = scn.scene_col
                pos = player.logic.ev_g_position()
                is_in_mecha = player.logic.ev_g_in_mecha()
                if is_in_mecha:
                    ctrl_target = player.logic.ev_g_control_target()
                    if ctrl_target and ctrl_target.logic:
                        pos = ctrl_target.logic.ev_g_position()
                    else:
                        return None
                return pos or None
            char_width = MECHA_STAND_WIDTH if is_in_mecha else CHARACTER_STAND_WIDTH
            if is_in_mecha:
                char_height = MECHA_STAND_HEIGHT if 1 else CHARACTER_STAND_HEIGHT
                start_pos = math3d.vector(pos.x, 9999 * NEOX_UNIT_SCALE, pos.z)
                end_pos = math3d.vector(pos.x, -9999 * NEOX_UNIT_SCALE, pos.z)
                test_capsule = collision.col_object(collision.CAPSULE, math3d.vector(char_width / 2, char_height / 2, 0), -1, -1)
                result = scol.sweep_test(test_capsule, start_pos, end_pos, -1, -1, -1, collision.INCLUDE_FILTER)
                if result[0]:
                    return result[1]
                return None
            return None