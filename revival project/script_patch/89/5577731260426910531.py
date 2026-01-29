# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartObserve.py
from __future__ import absolute_import
from . import ScenePart
from logic.comsys.battle.Settle import settle_system_utils
from logic.client.const import game_mode_const
from logic.gutils import judge_utils
from logic.gutils.client_unit_tag_utils import register_unit_tag
import six_ex
WEIRD_MECHA_VEHICLE_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaTrans'))

class PartObserve(ScenePart.ScenePart):
    ENTER_EVENT = {'scene_observed_player_setted_event': '_on_scene_observed_player_setted',
       'show_battle_report_event': 'parse_my_killer_id',
       'add_teammate_name_event': 'on_add_player',
       'set_observe_target_id_event': 'set_observe_target_id',
       'spectate_battle_finish_event': 'show_spectate_battle_winner',
       'puppet_destroy_event': 'on_puppet_destroy',
       'scene_player_setted_event': 'on_player_setted',
       'extra_scene_added': 'on_extra_scene_added'
       }

    def __init__(self, scene, name):
        super(PartObserve, self).__init__(scene, name)
        self.to_be_observed_target_id = None
        self.cur_observe_id = None
        self._has_registered_control_target_id = None
        return

    def on_enter(self):
        global_data.ui_mgr.show_ui('FightChatUI', 'logic.comsys.chat')
        global_data.emgr.show_danmu_btn_event.emit(False)
        dlg = global_data.ui_mgr.show_ui('DanmuLinesUI', 'logic.comsys.observe_ui')
        self.check_spec_target()

    def check_spec_target(self):
        from mobile.common.EntityManager import EntityManager
        if global_data.player and global_data.player.logic:
            obj_id = global_data.player.logic.ev_g_spectate_target_id()
            if obj_id:
                self.set_observe_target_id(obj_id)

    def on_player_setted(self, player):
        if not player:
            return
        if global_data.player and global_data.player.logic:
            obj_id = global_data.player.logic.ev_g_spectate_target_id()
            if obj_id != self.to_be_observed_target_id:
                self.check_spec_target()

    def on_extra_scene_added(self, scene_type):
        from logic.gcommon.common_const.scene_const import SCENE_NORMAL_SETTLE, SCENE_NIGHT_SETTLE
        if scene_type not in (SCENE_NORMAL_SETTLE, SCENE_NIGHT_SETTLE):
            return
        global_data.ui_mgr.close_ui('ObserveUI')

    def on_exit(self):
        global_data.ui_mgr.close_ui('ObserveUI')
        global_data.ui_mgr.close_ui('JudgeLoadingUI')
        global_data.ui_mgr.close_ui('FightChatUI')
        global_data.ui_mgr.close_ui('FightChatUIPC')
        global_data.ui_mgr.close_ui('BattleWinnersUI')
        global_data.ui_mgr.close_ui('WeaponBarSelectUI')
        global_data.ui_mgr.close_ui('RogueGiftTopRightUI')
        global_data.ui_mgr.close_ui('DeathRogueGiftTopRightUI')
        global_data.ui_mgr.close_ui('SceneTouchBlockUI')

    def set_observe_target_id(self, eid, allow_none_target=False, new_cam_lplayer=None):
        from mobile.common.EntityManager import EntityManager
        if self._has_registered_control_target_id:
            self.unregister_control_target_listen_event()
        if eid is None:
            self._set_observe_target(None, allow_none_target, new_cam_lplayer)
        else:
            ent = EntityManager.getentity(eid)
            if ent and ent.logic:
                con_target = ent.logic.ev_g_control_target()
                if con_target and con_target.logic:
                    self._set_observe_target(ent.logic)
                else:
                    self._has_registered_control_target_id = eid
                    ent.logic.regist_event('E_SET_CONTROL_TARGET', self._on_observer_added_control_target, 1000)
            else:
                self.to_be_observed_target_id = eid
                global_data.emgr.need_wait_observed_player_loaded_event.emit(eid)
        return

    def _on_scene_observed_player_setted(self, observe_target):
        import wwise
        wwise.SoundEngine.SetRTPCValue('game_settlement', 0)
        ui_inst = global_data.ui_mgr.get_ui('BattleWinnersUI')
        if ui_inst:
            return
        else:
            if observe_target is not None:
                self.cur_observe_id = observe_target.id
                if global_data.is_pc_mode:
                    global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.enable_PC_control(False)
                if not judge_utils.is_ob():
                    global_data.ui_mgr.show_ui('ObserveUI', 'logic.comsys.observe_ui')
                global_data.ui_mgr.show_ui('WeaponBarSelectUI', 'logic.comsys.battle')
                global_data.ui_mgr.show_ui('FrontSightUI', 'logic.comsys.battle')
                global_data.emgr.show_danmu_btn_event.emit(True)
                global_data.ui_mgr.show_ui('SceneTouchBlockUI', 'logic.comsys.common_ui')
            else:
                self.cur_observe_id = None
                if global_data.is_pc_mode:
                    global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.enable_PC_control(True)
                global_data.ui_mgr.close_ui('BattleSceneOnlyUI')
                global_data.ui_mgr.close_ui('ObserveUI')
                global_data.emgr.show_danmu_btn_event.emit(False)
                global_data.ui_mgr.close_ui('SceneTouchBlockUI')
            if not (global_data.player and global_data.player.logic):
                return
            ui_inst = global_data.ui_mgr.get_ui('ObserveUI')
            if ui_inst:
                ui_inst.switch_observe_target(observe_target)
                if observe_target is not None and observe_target.id == global_data.player.id:
                    ui_inst.set_killer_id(global_data.player.logic.ev_g_killer_id())
            global_data.ui_mgr.show_ui('FightChatUI', 'logic.comsys.chat')
            return

    def parse_my_killer_id(self, report_dict):
        from logic.gcommon.common_utils import battle_utils
        no_kill_camera = report_dict.get('no_kill_camera', False)
        if not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_PURE_MECHA):
            killer_id, injured_id, killer_name = battle_utils.parse_battle_report_death(report_dict)
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_HUNTING):
                if not injured_id:
                    killer_id, injured_id, killer_name = battle_utils.parse_pure_mecha_battle_report_death(report_dict)
        else:
            killer_id, injured_id, killer_name = battle_utils.parse_pure_mecha_battle_report_death(report_dict)
        if not no_kill_camera and injured_id:
            from mobile.common.EntityManager import EntityManager
            target = EntityManager.getentity(injured_id)
            if target and target.logic and target.logic.MASK & WEIRD_MECHA_VEHICLE_TAG_VALUE:
                driver_id = target.logic.sd.ref_driver_id
                target = EntityManager.getentity(driver_id)
            if target and target.logic:
                target.logic.send_event('E_SET_KILLER_ID_NAME', killer_id, killer_name)

    def on_add_player(self, lplayer, name):
        to_be_observed_target_id = self.to_be_observed_target_id
        if lplayer and lplayer.id == to_be_observed_target_id:
            self._set_observe_target(lplayer)

    def get_cur_observe_id(self):
        return self.cur_observe_id

    def _set_observe_target(self, lplayer, allow_none_target=False, new_cam_lplayer=None):
        if self.cur_observe_id is not None:
            from mobile.common.EntityManager import EntityManager
            ent = EntityManager.getentity(self.cur_observe_id)
            if ent and ent.logic:
                ent.logic.send_event('E_ON_BEING_OBSERVE', False)
                control_t = ent.logic.ev_g_control_target()
                if control_t and control_t.logic and control_t != ent:
                    control_t.logic.send_event('E_ON_BEING_OBSERVE', False)
        if lplayer:
            self.to_be_observed_target_id = None
            global_data.emgr.enable_special_target_pos_logic.emit(False)
            self.cur_observe_id = lplayer.id
            global_data.emgr.scene_observed_player_setted_for_cam.emit(lplayer)
            global_data.emgr.scene_observed_player_setted_event.emit(lplayer)
            lplayer.send_event('E_ON_BEING_OBSERVE', True)
            control_t = lplayer.ev_g_control_target()
            if control_t and control_t.logic and control_t.logic != lplayer:
                control_t.logic.send_event('E_ON_BEING_OBSERVE', True)
            if global_data.player and global_data.player.logic:
                global_data.player.logic.send_event('E_OBSERVE_TARGET_LOADED')
        else:
            self.cur_observe_id = None
            if allow_none_target:
                global_data.emgr.scene_observed_player_setted_for_cam.emit(None, new_cam_lplayer)
                global_data.emgr.scene_observed_player_setted_event.emit(None)
        global_data.emgr.scene_refresh_death_sfx_event.emit()
        return

    def _close_ui_before_show_spectate_settle_for_tdm_likes(self):
        global_data.ui_mgr.close_all_ui(exceptions=('BattleInfoUI', 'HpInfoUI', 'TeammateUI',
                                                    'BattleInfoMessageVisibleUI',
                                                    'ScalePlateUI', 'SmallMapUI',
                                                    'FightKillNumberUI', 'BattleRightTopUI',
                                                    'BattleLeftBottomUI', 'FightStateUI',
                                                    'WizardTrace', 'ProfileGraphUI',
                                                    'DanmuLinesUI', 'SoundVisibleUI',
                                                    'SoundVisible3DUI', 'InjureInfoUI',
                                                    'InjureInfo3DUI', 'BattleFightCapacity',
                                                    'ModeNameUI', 'FreeRecordUI',
                                                    'EndHighlightUI', 'VideoManualCtrlUI'))

    def show_spectate_battle_winner(self, battle_type, winner_names, rank=None, detail_info=None):
        from logic.gcommon.common_utils.battle_utils import get_play_type_by_battle_id
        from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN, PLAY_TYPE_DEATH, PLAY_TYPE_GVG, PLAY_TYPE_DEATH_IMBA, PLAY_TYPE_DEATH_AGRAVITY, PLAY_TYPE_IMPROVISE, PLAY_TYPE_ZOMBIEFFA, PLAY_TYPE_HTDM, PLAY_TYPE_CONTROL, PLAY_TYPE_FLAG, PLAY_TYPE_CROWN, PLAY_TYPE_MUTIOCCUPY, PLAY_TYPE_ADCRYSTAL, PLAY_TYPE_CRYSTAL, PLAY_TYPE_SCAVENGE, PLAY_TYPE_TRAIN, PLAY_TYPE_FLAG2, PLAY_TYPE_SNATCHEGG, PLAY_TYPE_DUEL, PLAY_TYPE_GOOSEBEAR, PLAY_TYPE_MECHA_DEATH, PLAY_TYPE_CLONE
        play_type = get_play_type_by_battle_id(battle_type)
        if play_type in {PLAY_TYPE_CRYSTAL, PLAY_TYPE_MECHA_DEATH, PLAY_TYPE_CLONE, PLAY_TYPE_DEATH_IMBA, PLAY_TYPE_DEATH_AGRAVITY, PLAY_TYPE_DEATH, PLAY_TYPE_HTDM, PLAY_TYPE_CONTROL, PLAY_TYPE_FLAG, PLAY_TYPE_CROWN, PLAY_TYPE_MUTIOCCUPY, PLAY_TYPE_SCAVENGE, PLAY_TYPE_FLAG2, PLAY_TYPE_GOOSEBEAR}:
            self._close_ui_before_show_spectate_settle_for_tdm_likes()
            global_data.ui_mgr.show_ui('DeathObserveEndUI', 'logic.comsys.observe_ui')
            ui = global_data.ui_mgr.get_ui('DeathObserveEndUI')
            if ui:
                ui.begin_show(detail_info)
        elif play_type == PLAY_TYPE_SNATCHEGG:
            self._close_ui_before_show_spectate_settle_for_tdm_likes()
            is_in_this_battle = False
            if global_data.player and global_data.battle:
                group_dict = global_data.battle.get_group_loading_dict()
                a_group_id = None
                for gid, g_info in six_ex.items(group_dict):
                    if global_data.player.id in g_info:
                        a_group_id = gid
                        break

                if a_group_id:
                    is_in_this_battle = True
            if is_in_this_battle:
                if global_data.player is not None:
                    global_data.player.quit_battle(False)
                    return
            from logic.comsys.battle.SnatchEgg.SnatchEggEndUI import SnatchEggEndObserveUI

            def cb():
                if global_data.player is not None:
                    global_data.player.quit_battle(False)
                return

            ui = global_data.ui_mgr.get_ui('SnatchEggEndObserveUI')
            if not ui:
                SnatchEggEndObserveUI(None, None, cb)
            ui = global_data.ui_mgr.get_ui('SnatchEggEndObserveUI')
            if ui:
                ui.begin_show(detail_info, cb)
        elif play_type in [PLAY_TYPE_GVG, PLAY_TYPE_DUEL]:
            if global_data.player.is_in_global_spectate():
                self._close_ui_before_show_spectate_settle_for_tdm_likes()
                global_data.ui_mgr.show_ui('GVGObserveEndUI', 'logic.comsys.observe_ui')
                ui = global_data.ui_mgr.get_ui('GVGObserveEndUI')
                if ui:
                    detail_info['rank'] = rank
                    ui.begin_show(detail_info)
        elif play_type == PLAY_TYPE_IMPROVISE:
            self._close_ui_before_show_spectate_settle_for_tdm_likes()
            is_draw = detail_info.get('is_draw', False)
            self_group_id = detail_info.get('watching_group_id', None)
            group_points_dict_int_key = detail_info.get('group_points', {})
            from logic.comsys.battle.Improvise.ImproviseRoundSettleUI import SETTLE_WIN, SETTLE_DRAW, SETTLE_LOSE
            if is_draw:
                settle_result = SETTLE_DRAW
            elif rank == 1:
                settle_result = SETTLE_WIN
            else:
                settle_result = SETTLE_LOSE

            def cb():
                global_data.player and global_data.player.quit_battle(True)

            from logic.comsys.battle.Improvise.ImproviseRoundSettleUI import ImproviseRoundSettleUI
            ImproviseRoundSettleUI(None, settle_result, group_points_dict_int_key, self_group_id, click_close_cb=cb)
        elif play_type == PLAY_TYPE_ZOMBIEFFA:
            self._close_ui_before_show_spectate_settle_for_tdm_likes()
            ui = global_data.ui_mgr.show_ui('ZombieFFAObserveEnd', 'logic.comsys.observe_ui')
            if ui:
                ui.begin_show(detail_info)
        elif play_type == PLAY_TYPE_ADCRYSTAL:
            ui = global_data.ui_mgr.show_ui('ADCrystalObserveEndUI', 'logic.comsys.battle.ADCrystal')
            ui and ui.begin_show(detail_info)
        elif play_type == PLAY_TYPE_TRAIN:
            ui = global_data.ui_mgr.show_ui('TrainObserveEndUI', 'logic.comsys.battle.Train')
            ui and ui.begin_show(detail_info)
        elif global_data.player and global_data.player.logic:
            end_continue_ui = global_data.ui_mgr.get_ui('EndContinueUI')
            end_statistics_ui = global_data.ui_mgr.get_ui('EndStatisticsUI')
            end_exp_ui = global_data.ui_mgr.get_ui(settle_system_utils.get_end_exp_ui_cls().__name__)
            end_anim_ui = global_data.ui_mgr.get_ui('EndAnimUI')
            end_transition_ui = global_data.ui_mgr.get_ui('EndTransitionUI')
            death_replay_ui = global_data.ui_mgr.get_ui('EndDeathReplayUI')
            if end_continue_ui or end_statistics_ui or end_exp_ui or end_anim_ui or end_transition_ui or death_replay_ui:
                return
            from logic.comsys.observe_ui.BattleWinnersUI import BattleWinnersUI
            BattleWinnersUI()
            ui_inst = global_data.ui_mgr.get_ui('BattleWinnersUI')
            if ui_inst:
                ui_inst.set_winner_names(winner_names, rank)
        global_data.ui_mgr.close_ui('ObserveUI')
        global_data.ui_mgr.close_ui('JudgeLoadingUI')
        return

    def on_puppet_destroy(self, unit_id):
        if unit_id == self._has_registered_control_target_id:
            self.unregister_control_target_listen_event()
        if self.cur_observe_id and self.cur_observe_id == unit_id:
            self.cur_observe_id = None
            global_data.emgr.scene_observed_player_setted_for_cam.emit(None)
            global_data.emgr.scene_observed_player_setted_event.emit(None)
        return

    def _on_observer_added_control_target(self, target, *args):
        if not (target and target.logic):
            return
        if target.logic.ev_g_driver() == self._has_registered_control_target_id:
            global_data.game_mgr.post_exec(self.unregister_control_target_listen_event)
            from mobile.common.EntityManager import EntityManager
            _ent = EntityManager.getentity(self._has_registered_control_target_id)
            if _ent and _ent.logic:
                self._set_observe_target(_ent.logic)

    def unregister_control_target_listen_event(self):
        from mobile.common.EntityManager import EntityManager
        last_ent = EntityManager.getentity(self._has_registered_control_target_id)
        if last_ent and last_ent.logic:
            last_ent.logic.unregist_event('E_SET_CONTROL_TARGET', self._on_observer_added_control_target)
        self._has_registered_control_target_id = None
        return