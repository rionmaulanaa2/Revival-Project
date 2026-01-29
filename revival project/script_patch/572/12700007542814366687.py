# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/observe_ui/ObserveUI.py
from __future__ import absolute_import
import six_ex
import six
from functools import cmp_to_key
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gutils.custom_ui_utils import get_cut_name
from data.camera_state_const import OBSERVE_FREE_MODE
from logic.gcommon.common_const.ui_operation_const import FIRST_SWITCH_OBSERVE_CAM
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.chat.DanmuButtonWidget import DanmuButtonWidget
from logic.gutils.observe_utils import LiveObserveUIHelper, format_popular_num, check_has_battle_observe_bet
from logic.client.const import game_mode_const
from logic.gutils import battle_flag_utils
import cc
from logic.gutils import judge_utils
LIKED_PIC_PATH = 'gui/ui_res_2/battle_observe/icon_like_2.png'
FOLLOW_VIEW_PIC_PATH = 'gui/ui_res_2/battle_observe/icon_observe_camera.png'
FREE_VIEW_PIC_PATH = 'gui/ui_res_2/battle_observe/icon_observe_camera_dark.png'
RANK_PIC = [
 'gui/ui_res_2/battle_observe/observe_rank_first.png',
 'gui/ui_res_2/battle_observe/observe_rank_second.png',
 'gui/ui_res_2/battle_observe/observe_rank_third.png',
 'gui/ui_res_2/battle_observe/observe_rank_fourth.png']
from common.const import uiconst

class ObserveCameraWidget(object):
    WHITE_LIST = [
     'ScopePlayerUI', 'JudgeObserveUINew', 'JudgeObserveUINewPCNoticeUI', 'BattleReconnectUI',
     'NormalConfirmUI2', 'JudgeObSettleUI', 'EndTransitionUI', 'SurviveInfoUI', 'SurviveInfoUIPC',
     'TopLevelConfirmUI2', 'SecondConfirmDlg2', 'ExitConfirmDlg', 'BusyReconnectBg', 'MainSettingUI',
     'FFABeginCountDown', 'FFAFinishCountDown',
     'ObserveUI', 'ObserveUIPC', 'BattleSceneOnlyUI', 'EndContinueUI',
     'BattleWinnersUI', 'EndAnimUI', 'DeathEndUI', 'NewbieStageEndUI', 'DeathObserveEndUI', 'CrystalEndUI', 'ADCrystalEndUI', 'GVGEndUI', 'SnatchEggEndUI', 'TrainEndUI', 'TrainObserveEndUI', 'ADCrystalObserveEndUI', 'GVGObserveEndUI']

    def __init__(self, ui_name, panel, btn_hide, btn_hide_2, btn_lock, btn_free, btn_change):
        self._is_playing_ani = False
        self._played_ani = None
        self._is_hide_btn_show = True
        self._is_hide_other_ui = False
        self._is_lock_on_target = True
        self._ui_name = ui_name
        self.panel = panel
        self.btn_change = btn_change
        self.btn_hide = btn_hide
        self.btn_hide_2 = btn_hide_2
        self.btn_lock = btn_lock
        self.btn_free = btn_free
        self.btn_change.BindMethod('OnClick', self.on_click_free_sight_btn)
        self.btn_hide.BindMethod('OnClick', self.on_click_btn_hide)
        self.btn_hide_2.BindMethod('OnClick', self.on_click_btn_hide_2)
        self.btn_free.BindMethod('OnClick', self.on_click_btn_free)
        self.btn_lock.BindMethod('OnClick', self.on_click_btn_lock)
        self.btn_change.EnableCustomState(True)
        self.btn_change.SetSelect(True)
        self.btn_free.setVisible(False)
        if global_data.battle and global_data.battle.is_customed_battle() or global_data.is_judge_ob:
            self.btn_free.setVisible(True)
        self.update_ui_show()
        return

    def destroy(self):
        global_data.ui_mgr.remove_ui_show_whitelist(self.__class__.__name__)
        self.btn_change.UnBindMethod('OnClick')
        self.btn_hide.UnBindMethod('OnClick')
        self.btn_hide_2.UnBindMethod('OnClick')
        self.btn_free.UnBindMethod('OnClick')
        self.btn_lock.UnBindMethod('OnClick')
        self.panel = None
        self.btn_change = None
        self.btn_hide = None
        self.btn_hide_2 = None
        self.btn_lock = None
        self.btn_free = None
        self._played_ani = None
        self._is_playing_ani = False
        self._is_hide_btn_show = True
        self._is_hide_other_ui = False
        return

    def on_click_free_sight_btn(self, *args):
        partcam = global_data.game_mgr.scene.get_com('PartCamera')
        if self.panel.img_tips.isVisible():
            if global_data.player:
                global_data.player.write_setting(FIRST_SWITCH_OBSERVE_CAM, False)
                global_data.player.save_settings_to_file()
            self.panel.img_tips.setVisible(False)
        self.panel.img_tips.setVisible(False)
        if not partcam:
            return
        cur_cam_type = partcam.get_cur_camera_state_type()
        from data.camera_state_const import OBSERVE_FREE_MODE
        if cur_cam_type != OBSERVE_FREE_MODE:
            self.on_switch_observe_camera_type(True)
            self.btn_change.img_change.SetDisplayFrameByPath('', FREE_VIEW_PIC_PATH)
        else:
            self.on_switch_observe_camera_type(False)
            self.btn_change.img_change.SetDisplayFrameByPath('', FOLLOW_VIEW_PIC_PATH)

    def on_switch_observe_camera_type(self, is_in_free_observe):
        if is_in_free_observe:
            global_data.emgr.camera_enter_free_observe_event.emit()
        else:
            global_data.emgr.camera_leave_free_observe_event.emit()

    def on_resolution_changed(self):
        if not self._played_ani:
            return
        if self._is_playing_ani:
            return
        self.on_play_hide_btn_ani()

    def show_camera_control_ui(self):
        from logic.comsys.share.BattleSceneOnlyUI import BattleSceneOnlyUI
        ui = BattleSceneOnlyUI()
        if ui:
            ui.set_left_center_btns_vis(False)
            ui.hide_grid()
            ui.block_ui_show(white_list=self.WHITE_LIST)
        if not (self.panel and self.panel.isValid()):
            return
        if self.panel.nd_control:
            self.panel.nd_control.setVisible(False)

    def on_click_btn_free(self, btn, touch):
        if not (self.panel and self.panel.isValid()):
            return
        if global_data.judge_camera_mgr:
            if not global_data.judge_camera_mgr.check_can_enable():
                return
        global_data.emgr.try_switch_judge_camera_event.emit(not bool(global_data.is_in_judge_camera))
        global_data.ui_mgr.close_ui('BattleSceneOnlyUI')
        if global_data.is_in_judge_camera:
            self.show_camera_control_ui()
            ui = global_data.ui_mgr.get_ui('BattleSceneOnlyUI')
            if ui:
                ui.set_close_cb(self.exit_free_camera)
                ui.set_is_direction_helper(True)
                if global_data.judge_camera_mgr:
                    global_data.judge_camera_mgr.set_move_direction_generator(ui)
        else:
            global_data.ui_mgr.close_ui('BattleSceneOnlyUI')

    def exit_free_camera(self):
        ui = global_data.ui_mgr.get_ui(self._ui_name)
        if ui:
            ui.exit_free_camera()
        global_data.emgr.try_switch_judge_camera_event.emit(False)

    def exit_lock_camera(self):
        ui = global_data.ui_mgr.get_ui(self._ui_name)
        if ui:
            ui.exit_lock_camera()
        global_data.emgr.camera_leave_free_observe_event.emit()

    def on_click_btn_lock(self, btn, touch):
        cur_cam_type = global_data.cam_data.camera_state_type
        from data.camera_state_const import OBSERVE_FREE_MODE
        if not global_data.ui_mgr.get_ui('BattleSceneOnlyUI'):
            self.on_switch_observe_camera_type(True)
            global_data.ui_mgr.close_ui('BattleSceneOnlyUI')
            self.show_camera_control_ui()
            ui = global_data.ui_mgr.get_ui('BattleSceneOnlyUI')
            if ui:
                ui.set_close_cb(self.exit_lock_camera)
                ui.set_move_ranges((-500, 500), (-500, 500), (-500, 500))
        else:
            global_data.ui_mgr.close_ui('BattleSceneOnlyUI')

    def on_camera_state_changed(self, new_type, old_type, *args):
        from data.camera_state_const import OBSERVE_FREE_MODE
        if new_type != OBSERVE_FREE_MODE:
            self.btn_change.img_change.SetDisplayFrameByPath('', FREE_VIEW_PIC_PATH)
        else:
            self.btn_change.img_change.SetDisplayFrameByPath('', FOLLOW_VIEW_PIC_PATH)

    def on_click_btn_hide_2(self, btn, touch):
        if self._is_playing_ani:
            return
        self._is_hide_btn_show = not self._is_hide_btn_show
        self.on_play_hide_btn_ani()

    def on_click_btn_hide(self, btn, touch):
        if self._is_playing_ani:
            return
        self._is_hide_other_ui = not self._is_hide_other_ui
        self.update_ui_show()

    def on_play_hide_btn_ani(self):
        animate = 'show_btn' if self._is_hide_btn_show else 'hide_btn'
        self._played_ani = animate
        self._is_playing_ani = True
        self.panel.PlayAnimation(animate)
        animation_time = self.panel.GetAnimationMaxRunTime(animate)

        def finished_show():
            self._is_playing_ani = False

        self.panel.SetTimeOut(animation_time, finished_show)

    def update_ui_show(self):
        icon = 'gui/ui_res_2/battle_observe/icon_observe_eye.png' if self._is_hide_other_ui else 'gui/ui_res_2/battle_observe/icon_observe_eye_dark.png'
        self.btn_hide.icon_hide.SetDisplayFrameByPath('', icon)
        if self._is_hide_other_ui:
            white_ls = self.WHITE_LIST
            from logic.gutils.pc_ui_utils import MOBILE_2_PC_UI_DICT, PC_2_MOBILE_UI_DICT
            for ui_name in white_ls:
                if ui_name in MOBILE_2_PC_UI_DICT:
                    white_ls.append(MOBILE_2_PC_UI_DICT[ui_name])

            global_data.ui_mgr.add_ui_show_whitelist(white_ls, self.__class__.__name__)
            self.panel.nd_non_hide.setVisible(False)
            self.btn_hide_2.setVisible(True)
        else:
            global_data.ui_mgr.remove_ui_show_whitelist(self.__class__.__name__)
            self.panel.nd_non_hide.setVisible(True)
            self.btn_hide_2.setVisible(False)

    def set_camera_state(self, camera_state):
        if camera_state != OBSERVE_FREE_MODE:
            self.btn_change.SetSelect(True)
            self.btn_change.img_change.SetDisplayFrameByPath('', FREE_VIEW_PIC_PATH)
        else:
            self.btn_change.SetSelect(False)
            self.btn_change.img_change.SetDisplayFrameByPath('', FOLLOW_VIEW_PIC_PATH)


class ObserveUI(BasePanel):
    PANEL_CONFIG_NAME = 'observe/observe'
    DLG_ZORDER = BASE_LAYER_ZORDER
    HIDE_LIST = ['DrugUIPC', 'ThrowRockerUIPC', 'BattleFightCapacityPC', 'BattleFightCapacity']
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'panel.OnClick': 'on_click_panel',
       'btn_exit.OnClick': 'on_click_exit_btn',
       'btn_cur_observer.OnClick': 'on_click_teammate_list',
       'layer_observe.OnBegin': 'on_begin_layer_observe',
       'layer_observe.OnDrag': 'on_drag_layer_observe',
       'btn_like.OnClick': 'on_click_btn_like',
       'btn_report.OnClick': 'on_click_report_btn',
       'btn_flag.OnClick': 'on_click_flag_btn',
       'btn_audience.OnBegin': 'on_audience_btn_begin',
       'btn_audience.OnEnd': 'on_audience_btn_end',
       'btn_follow.OnClick': 'on_click_btn_follow',
       'btn_guess.OnClick': 'on_click_btn_guess',
       'btn_search.OnClick': 'on_click_btn_search'
       }
    MAX_OB_TEAMMATE_NUM = 3
    REFRESH_TIME_MIN_INTERVAL = 4
    GLOBAL_EVENT = {'show_danmu_btn_event': 'enable_danmu_input',
       'on_follow_result': 'on_follow_result',
       'on_undo_follow_result': 'on_undo_follow_result',
       'on_update_spectate_cnt': 'on_update_spectate_cnt',
       'on_update_spectate_like_num': 'on_update_spectate_like_num',
       'on_update_spectate_hot_info': 'on_update_spectate_hot_info',
       'camera_switch_to_state_event': 'on_camera_state_changed'
       }

    def on_click_exit_btn(self, *args):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
        if global_data.player and global_data.player.is_battle_replaying():

            def confirm_callback():
                if global_data.player.battle_replay_stop():
                    if global_data.player.logic:
                        global_data.player.quit_battle()
                    global_data.ui_mgr.close_ui('ObserveUI')

        else:

            def confirm_callback():
                if not global_data:
                    return
                if global_data.player and global_data.player.logic:
                    from logic.gutils import judge_utils
                    is_ob = judge_utils.is_ob()
                    need_show_end_stat = False if is_ob else True
                    global_data.player.quit_battle(not need_show_end_stat)
                global_data.ui_mgr.close_ui('ObserveUI')

        txt_id = 19152
        if global_data.player and not global_data.player.is_in_global_spectate() and global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_DUEL)):
            txt_id = 19492
        SecondConfirmDlg2().confirm(content=get_text_local_content(txt_id), confirm_callback=confirm_callback)

    def on_init_panel(self, *args, **kwargs):
        self.observe_target = None
        self.battle_flag = None
        self.camera_state = None
        self.can_guess = False
        from logic.gcommon.common_const.ui_operation_const import OBSERVE_UI_ZORDER
        self.panel.setLocalZOrder(OBSERVE_UI_ZORDER)
        self.init_event()
        self.is_single_model = self.is_in_single_model_battle()
        self.is_ob = True
        self.all_item = None
        self.src_star_info_list = None
        if global_data.player:
            self._top_player_infos = global_data.player.get_spectate_battle_top_player_infos()
        else:
            self._top_player_infos = None
        self._selected_flag = False
        if global_data.player and global_data.player.logic:
            from logic.gutils import judge_utils
            self.is_ob = judge_utils.is_ob()
        self.req_update_battle_stars()
        self.set_observe_list_visible(False)
        self.panel.img_expend.setVisible(False)
        self._can_click_observer_player_item = True
        self.observe_camera_widget = ObserveCameraWidget(self.__class__.__name__, self.panel, self.panel.btn_hide, self.panel.btn_hide_2, self.panel.btn_lock, self.panel.btn_free, self.panel.btn_change)
        partcam = global_data.game_mgr.scene.get_com('PartCamera')
        if partcam:
            cur_cam_type = partcam.get_cur_camera_state_type()
            self.set_camera_state(cur_cam_type)
        if global_data.player and global_data.player.get_setting(FIRST_SWITCH_OBSERVE_CAM):
            self.panel.img_tips.setVisible(True)
        else:
            self.panel.img_tips.setVisible(False)
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.update_status),
         cc.DelayTime.create(1.0)])))
        if global_data.player and global_data.player.is_in_global_spectate() or self.is_ob:
            send_group_message_either = False
        else:
            send_group_message_either = True
        self.danmu_button_widget = DanmuButtonWidget(self.panel.temp_danmu, send_group_message_either)
        if global_data.player and global_data.player.is_in_global_spectate() or self.is_ob:
            self.panel.temp_danmu.setVisible(False)
        self.panel.DelayCall(ObserveUI.REFRESH_TIME_MIN_INTERVAL / 2, self._tick_spectate_hot_info)
        self._refresh_ui_controls_visibility()
        to_hide_exit_btn = False
        if global_data.game_mode:
            if global_data.game_mode.get_mode_type() == game_mode_const.GAME_MODE_IMPROVISE:
                if global_data.player and not global_data.player.is_in_global_spectate():
                    to_hide_exit_btn = True
        if to_hide_exit_btn:
            self.panel.btn_exit.setVisible(False)
        self.hide_main_ui(self.HIDE_LIST)
        if global_data.ui_mgr.get_ui('BattleSceneOnlyUI') and global_data.ui_mgr.get_ui('BattleSceneOnlyUI').isValid():
            self.observe_camera_widget.show_camera_control_ui()
        if not global_data.game_mode.is_pve():
            self.panel.btn_search.setVisible(False)
        else:
            self.panel.btn_search.setVisible(True)
            self.panel.btn_lock.setVisible(False)
            self.panel.btn_hide.setVisible(False)
            self.panel.img_tips.setVisible(False)
        return

    def on_resolution_changed(self):
        self.observe_camera_widget and self.observe_camera_widget.on_resolution_changed()

    def init_event(self):
        global_data.emgr.update_battle_stars_event += self.update_battle_star_event
        global_data.emgr.update_spectate_top_player_infos += self._on_update_spectate_top_player_infos
        global_data.emgr.update_alive_player_num_event += self.update_alive_player_num
        global_data.emgr.update_player_kill_num_event += self.update_teammate_kill_num
        global_data.emgr.on_target_kill_mecha_event += self.on_target_kill_mecha
        global_data.emgr.camera_switch_to_state_event += self.set_camera_state
        global_data.emgr.on_target_observer_num_changed += self.set_observe_num
        global_data.emgr.judge_cache_add_player += self._on_judge_cache_add_player
        global_data.emgr.update_cur_observe_ui += self.update_cur_observe_ui
        global_data.emgr.death_playback_ui_lifetime += self._on_death_playback_ui_lifetime
        global_data.emgr.fight_plasma_weapon_ui_lifetime += self._on_fight_plasma_weapon_ui_lifetime
        global_data.emgr.spectate_manual_switch_succeed += self._on_spectate_manual_switch_succeed
        global_data.emgr.spectate_manual_switch_fail += self._on_spectate_manual_switch_fail
        global_data.emgr.live_my_bet_info_ret += self._on_my_bet_info_ret

    def on_finalize_panel(self):
        self.switch_observe_target(None)
        global_data.emgr.update_battle_stars_event -= self.update_battle_star_event
        global_data.emgr.update_spectate_top_player_infos -= self._on_update_spectate_top_player_infos
        global_data.emgr.update_alive_player_num_event -= self.update_alive_player_num
        global_data.emgr.update_player_kill_num_event -= self.update_teammate_kill_num
        global_data.emgr.on_target_kill_mecha_event -= self.on_target_kill_mecha
        global_data.emgr.camera_switch_to_state_event -= self.set_camera_state
        global_data.emgr.on_target_observer_num_changed -= self.set_observe_num
        global_data.emgr.judge_cache_add_player -= self._on_judge_cache_add_player
        global_data.emgr.update_cur_observe_ui -= self.update_cur_observe_ui
        global_data.emgr.death_playback_ui_lifetime -= self._on_death_playback_ui_lifetime
        global_data.emgr.fight_plasma_weapon_ui_lifetime -= self._on_fight_plasma_weapon_ui_lifetime
        global_data.emgr.spectate_manual_switch_succeed -= self._on_spectate_manual_switch_succeed
        global_data.emgr.spectate_manual_switch_fail -= self._on_spectate_manual_switch_fail
        global_data.emgr.live_my_bet_info_ret -= self._on_my_bet_info_ret
        self.panel.stopAllActions()
        self.destroy_widget('danmu_button_widget')
        self.destroy_widget('observe_camera_widget')
        self.show_main_ui()
        return

    def _refresh_ui_controls_visibility(self):
        if self.is_ob:
            self.panel.nd_flag.setVisible(False)
            self.panel.nd_follow.setVisible(False)
            self.panel.nd_like.setVisible(False)
            self.panel.nd_report.setVisible(False)
            self.panel.nd_audience.setVisible(False)
        else:
            self.panel.nd_flag.setVisible(True)
            self.panel.nd_follow.setVisible(True)
            self.panel.nd_like.setVisible(True)
            self.panel.nd_report.setVisible(True)
            self.panel.nd_audience.setVisible(True)
        self._refresh_cam_btn_visibility()

    def _refresh_cam_btn_visibility(self):
        show_change = not global_data.ui_mgr.get_ui('DeathPlayBackUI') and not global_data.ui_mgr.get_ui('FightPlasmaWeaponUI') and not global_data.ui_mgr.get_ui('MechaDeathPlayBackUI')
        if show_change:
            self.panel.nd_observe_change.setVisible(True)
        else:
            self.panel.nd_observe_change.setVisible(False)

    def _on_death_playback_ui_lifetime(self, _open):
        self._refresh_cam_btn_visibility()

    def _on_fight_plasma_weapon_ui_lifetime(self, _open):
        self._refresh_cam_btn_visibility()

    def _on_spectate_manual_switch_succeed(self):
        self._can_click_observer_player_item = True

    def _on_spectate_manual_switch_fail(self):
        self._can_click_observer_player_item = True

    def _on_judge_cache_add_player(self, pid):
        if not self.is_ob:
            return
        self.update_cur_observe_ui()

    def switch_observe_target(self, observe_target):
        if self.observe_target:
            self.observe_target.unregist_event('E_CONNECT_STATE', self.sync_connect_state)
        self.observe_target = observe_target
        self.battle_flag = None
        if self.observe_target:
            self.sync_connect_state(self.observe_target.ev_g_connect_state())
            self.observe_target.regist_event('E_CONNECT_STATE', self.sync_connect_state)
            self.battle_flag = self.observe_target.ev_g_battle_flag()
            if self.battle_flag:
                self.battle_flag['show_uid'] = True
                battle_flag_utils.init_battle_flag_template_new(self.battle_flag, self.panel.temp_flag, enable_click=False, from_battle=True)
        self.update_cur_observe_ui()
        if self.observe_target and global_data.battle:
            _comp_id, _comp_round = global_data.battle.get_round_competition_data()
            if _comp_id and (_comp_id == 'SUMMER23_CN' or _comp_id == 'SUMMER23_US' or _comp_id == 'SUMMER23_NA'):
                from logic.gcommon.cdata.round_competition import gen_bet_item, gen_bet_item_list
                bet_list = gen_bet_item_list(_comp_id, _comp_round)
                if bet_list:
                    self.panel.btn_guess.setVisible(True)
                    global_data.player.pull_my_bet_info()
                else:
                    self.panel.btn_guess.setVisible(False)
            else:
                self.panel.btn_guess.setVisible(False)
        return

    def update_cur_observe_ui(self):
        from logic.gutils.team_utils import is_all_death
        if not self.observe_target:
            return
        self.set_observe_list_visible(False)
        if self._check_need_show_global_spectate_top_players():
            self._update_global_spectate_top_players(self._top_player_infos)
        elif self.check_need_show_star():
            if self.src_star_info_list:
                self.update_battle_star_event(self.src_star_info_list)
        else:
            self.show_observe_players_ui()
        self.update_cure_observer()
        self.update_like_data(0)
        self.set_observe_num(1, 10)
        self._update_follow_icon()
        self._update_like_btn()

    def on_click_teammate_list(self, btn, touch):
        if self.panel.nd_screen.isVisible():
            self.set_observe_list_visible(False)
        elif self.panel.img_expend.isVisible():
            self.set_observe_list_visible(True)

    def set_observe_list_visible(self, is_vis):
        self.panel.nd_screen.setVisible(is_vis)

    def update_cure_observer(self, rank_idx=3):
        if not self.observe_target:
            return
        nd = self.panel.btn_cur_observer
        char_name = self.observe_target.ev_g_char_name()
        nd.lab_name.SetString(get_cut_name(six.text_type(char_name), 12))
        kill_num = self.get_player_kill_num(self.observe_target.id)
        nd.lab_kill_no.SetString(str(kill_num))
        nd.player_id = self.observe_target.id
        nd.img_rank.SetDisplayFrameByPath('', RANK_PIC[rank_idx])

    def is_in_single_model_battle(self):
        bat = global_data.player.get_battle()
        if bat:
            return bat.is_single_person_battle()
        else:
            return True

    def get_player_kill_num(self, player_id):
        if global_data.player:
            battle = global_data.player.get_joining_battle() or global_data.player.get_battle()
            battle_stat = {} if battle is None else battle.statistics
            player_statistics = battle_stat.get(player_id, {})
            return player_statistics.get('kill', 0) + player_statistics.get('kill_mecha', 0)
        else:
            return 0

    def update_teammate_kill_num(self, player_id, statics):
        nd = self.panel.btn_cur_observer
        if hasattr(nd, 'player_id') and nd.player_id and nd.player_id == player_id:
            nd.lab_kill_no.SetString(str(statics.get('kill', 0) + statics.get('kill_mecha', 0)))
        if self.all_item:
            for idx, ui_item in enumerate(self.all_item):
                if hasattr(ui_item, 'player_id') and ui_item.player_id and ui_item.player_id == player_id:
                    ui_item.lab_kill_no.SetString(str(statics.get('kill', 0) + statics.get('kill_mecha', 0)))

    def on_target_kill_mecha(self, mecha_killer_id, mecha_injured_id, mecha_killer_statics):
        self.update_teammate_kill_num(mecha_killer_id, mecha_killer_statics)
        self.req_update_battle_stars()

    def set_killer_id(self, killer_id):
        from logic.gcommon.common_utils.local_text import get_text_by_id
        if self.observe_target:
            if not (global_data.player and global_data.player.logic):
                return
            if self.observe_target.id == killer_id and not global_data.player.logic.ev_g_is_groupmate(killer_id):
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(19155))
            else:
                char_name = self.observe_target.ev_g_char_name()
                if global_data.player.logic.ev_g_is_groupmate(self.observe_target.id):
                    global_data.emgr.battle_show_message_event.emit(get_text_by_id(19156, {'name': char_name}))
                else:
                    global_data.emgr.battle_show_message_event.emit(get_text_by_id(19157, {'name': char_name}))

    def sync_connect_state(self, conn_state):
        self.panel.nd_offline.setVisible(not conn_state)

    @staticmethod
    def _judge_pid_sorter(aid, bid):
        pinfo_a = judge_utils.get_global_player_info(aid)
        pinfo_b = judge_utils.get_global_player_info(bid)
        group_id_a = pinfo_a.get('group', None)
        group_id_b = pinfo_b.get('group', None)
        if group_id_a is not None and group_id_b is not None:
            return six_ex.compare(group_id_a, group_id_b)
        else:
            if group_id_a is not None:
                return -1
            if group_id_b is not None:
                return 1
            return 0
            return

    def get_other_observable_teammates(self):
        if self.is_ob and global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.TDM_OB):
            ret_ids = list(six_ex.keys(judge_utils.get_all_global_player_info()))
            if global_data.player and global_data.player.id in ret_ids:
                ret_ids.remove(global_data.player.id)
            if self.observe_target.id in ret_ids:
                ret_ids.remove(self.observe_target.id)
            ret_ids.sort(key=cmp_to_key(self._judge_pid_sorter))
            return ret_ids
        else:
            ret_ids = self.observe_target.ev_g_groupmate()
            if not ret_ids:
                return []
            ret_ids = list(ret_ids)
            if global_data.player and global_data.player.id in ret_ids:
                ret_ids.remove(global_data.player.id)
            if self.observe_target.id in ret_ids:
                ret_ids.remove(self.observe_target.id)
            return ret_ids

    def show_observe_players_ui(self):
        player_ids = self.get_other_observable_teammates()
        if len(player_ids) < 1:
            self.panel.img_expend.setVisible(False)
            return
        if not self.need_show_expend_ui():
            self.panel.img_expend.setVisible(False)
            return
        self.panel.img_expend.setVisible(True)
        self.panel.lv_star_list.DeleteAllSubItem()
        self.all_item = self.panel.lv_star_list.GetAllItem()
        for idx, tid in enumerate(player_ids):
            self.init_observe_player_ui_item(tid, show_team_color=self.is_ob and global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.TDM_OB))

        if self.panel.lv_star_list.GetItemCount() < 1:
            self.panel.img_expend.setVisible(False)
            return
        sw, sh = self.panel.lv_star_list.GetContentSize()
        self.panel.nd_change_list.SetContentSize(sw, sh)
        self.panel.nd_change_list.ResizeAndPosition(include_self=False)
        self.panel.lv_star_list._refreshItemPos()

    def init_observe_player_ui_item(self, player_id, show_team_color=False):
        entiy = EntityManager.getentity(player_id)
        if entiy and entiy.logic:
            player_unit = entiy.logic
            ui_item = self.panel.lv_star_list.AddTemplateItem()
            ui_item.setVisible(True)
            format_name = get_cut_name(six.text_type(player_unit.ev_g_char_name()), 12)
            ui_item.lab_name.SetString(format_name)
            ui_item.lab_kill_no.SetString(str(self.get_player_kill_num(player_unit.id)))
            ui_item.player_id = player_unit.id
            if not show_team_color:
                ui_item.img_rank.SetDisplayFrameByPath('', RANK_PIC[3])
            else:
                my_group_id = None
                if self.observe_target:
                    my_group_id = self.observe_target.ev_g_group_id()
                if my_group_id is None:
                    ui_item.img_rank.SetDisplayFrameByPath('', RANK_PIC[3])
                elif my_group_id == player_unit.ev_g_group_id():
                    ui_item.img_rank.SetDisplayFrameByPath('', RANK_PIC[2])
                else:
                    ui_item.img_rank.SetDisplayFrameByPath('', RANK_PIC[0])
            if player_unit.ev_g_death():
                ui_item.nd_dead.setVisible(True)

            @ui_item.button_star.unique_callback()
            def OnClick(btn, touch, player_unit=player_unit):
                if player_unit and player_unit.is_valid():
                    if player_unit.ev_g_death():
                        global_data.emgr.battle_show_message_event.emit(get_text_local_content(19454 if self.is_ob else 19154))
                        return
                    if self.is_ob and global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.TDM_OB):
                        if player_unit.ev_g_defeated():
                            name = get_cut_name(six.text_type(player_unit.ev_g_char_name()), 24)
                            global_data.emgr.battle_show_message_event.emit(get_text_local_content(19606))
                            return
                if self.observe_target and self.observe_target.id == player_unit.id:
                    return
                if not self.is_ob:
                    if global_data and global_data.player.logic:
                        if global_data.player.logic.ev_g_is_groupmate(player_unit.id):
                            global_data.player.logic.send_event('E_REQ_SPECTATE_GROUPMATE', player_unit.id)
                        else:
                            global_data.player.logic.send_event('E_REQ_SPECTATE_STAR', player_unit.id)
                elif global_data.player and global_data.player.logic:
                    global_data.player.logic.send_event('E_SET_JUDGE_OB_TARGET', player_unit.id)

        return

    def update_status(self):
        if not self._check_need_show_global_spectate_top_players() and not self.check_need_show_star() and self.all_item:
            for idx, ui_item in enumerate(self.all_item):
                if hasattr(ui_item, 'player_id') and ui_item.player_id:
                    entiy = EntityManager.getentity(ui_item.player_id)
                    if not entiy or not entiy.logic or entiy.logic.ev_g_death():
                        self.update_cur_observe_ui()
                        return

    def update_battle_star_event(self, star_info_list):
        self.src_star_info_list = star_info_list
        if not self.check_need_show_star():
            return
        rank_list = [0, 1, 2, 3]
        star_info_list = list(star_info_list)
        cur_ob_idx = 0
        for idx, star_info in enumerate(star_info_list):
            s_id = star_info.get('id')
            if self.observe_target and s_id == self.observe_target.id:
                star_info_list.remove(star_info)
                cur_ob_idx = idx if idx <= 3 else 3
                if cur_ob_idx not in rank_list:
                    log_error('cur_ob_idx is not in rank_list, cur_ob_idx = %s, star_info_list = %s' % (cur_ob_idx, star_info_list))
                    return
                rank_list.remove(cur_ob_idx)
                break

        self.update_cure_observer(cur_ob_idx)
        star_num = len(star_info_list)
        MAX_STAR_NUM = 3
        star_num = star_num if star_num < MAX_STAR_NUM else MAX_STAR_NUM
        if star_num == 0 or not self.need_show_expend_ui():
            self.set_observe_list_visible(False)
            self.panel.img_expend.setVisible(False)
            return
        self.panel.img_expend.setVisible(True)
        self.panel.lv_star_list.SetInitCount(star_num)
        self.all_item = self.panel.lv_star_list.GetAllItem()
        for idx, ui_item in enumerate(self.all_item):
            star_info = star_info_list[idx]
            self.init_star_ui_item(ui_item, star_info, rank_list, idx)

        sw, sh = self.panel.lv_star_list.GetContentSize()
        self.panel.nd_change_list.SetContentSize(sw, sh)
        self.panel.nd_change_list.ResizeAndPosition(include_self=False)
        self.panel.lv_star_list._refreshItemPos()

    def init_star_ui_item(self, ui_item, star_info, rank_list, idx):
        s_id = star_info.get('id')
        char_name = star_info.get('char_name', '')
        kill_cnt = star_info.get('kill_cnt', 0)
        ui_item.setVisible(True)
        ui_item.nd_dead.setVisible(False)
        ui_item.player_id = s_id
        ui_item.lab_name.SetString(get_cut_name(six.text_type(char_name), 12))
        ui_item.lab_kill_no.SetString(str(kill_cnt))
        ui_item.button_star.EnableCustomState(True)
        ui_item.img_rank.SetDisplayFrameByPath('', RANK_PIC[rank_list[idx]])

        @ui_item.button_star.unique_callback()
        def OnClick(btn, touch):
            if global_data.player and global_data.player.logic:
                if self.observe_target and self.observe_target.id == s_id:
                    return
                global_data.player.logic.send_event('E_REQ_SPECTATE_STAR', s_id)

    def update_alive_player_num(self, *args):
        self.req_update_battle_stars()

    def req_update_battle_stars(self):
        if not self.check_need_show_star():
            return
        if global_data.player and global_data.player.logic:
            global_data.player.logic.ev_g_battle_stars()

    def check_need_show_star(self):
        if self.is_ob:
            return False
        if self._check_need_show_global_spectate_top_players():
            return False
        if not self.is_single_model:
            if global_data.player and global_data.player.logic:
                teammates = global_data.player.logic.ev_g_groupmate()
                from logic.gutils.team_utils import is_all_death
                if teammates and is_all_death(teammates):
                    return True
                else:
                    return False

        else:
            return True
        return False

    def _check_need_show_global_spectate_top_players(self):
        if not global_data.player:
            return False
        if not global_data.player.is_in_global_spectate():
            return False
        from logic.gcommon.common_const.battle_const import DEFAULT_COMPETITION_TID_LIST, PLAY_TYPE_IMPROVISE
        from logic.gcommon.common_utils import battle_utils
        is_competition = global_data.battle and global_data.battle.get_battle_tid() in DEFAULT_COMPETITION_TID_LIST
        play_type = battle_utils.get_play_type_by_battle_id(global_data.battle.get_battle_tid())
        is_imporvise = True if play_type == PLAY_TYPE_IMPROVISE else False
        return is_competition or is_imporvise

    def _on_update_spectate_top_player_infos(self, battle_id, top_player_infos):
        if global_data.player and global_data.player.get_spectate_battle_id() == battle_id:
            self._top_player_infos = top_player_infos
            if self._check_need_show_global_spectate_top_players():
                self._update_global_spectate_top_players(top_player_infos)

    def _update_global_spectate_top_players(self, top_player_infos):
        list_num = len(top_player_infos) if top_player_infos else 0
        if list_num == 0:
            self.set_observe_list_visible(False)
            self.panel.img_expend.setVisible(False)
            return
        self.panel.img_expend.setVisible(True)
        self.panel.lv_star_list.SetInitCount(list_num)
        self.all_item = self.panel.lv_star_list.GetAllItem()
        for idx, ui_item in enumerate(self.all_item):
            info = top_player_infos[idx]
            self.init_top_player_ui_item(ui_item, idx, info)

        sw, sh = self.panel.lv_star_list.GetContentSize()
        self.panel.nd_change_list.SetContentSize(sw, sh)
        self.panel.nd_change_list.ResizeAndPosition(include_self=False)
        self.panel.lv_star_list._refreshItemPos()

    def init_top_player_ui_item(self, ui_item, idx, player_info):
        p_objid = player_info[0]
        u_id = player_info[1]
        char_name = player_info[2]
        ui_item.player_id = p_objid
        ui_item.player_uid = u_id
        ui_item.setVisible(True)
        ui_item.nd_dead.setVisible(False)
        ui_item.lab_name.SetString(get_cut_name(six.text_type(char_name), 12))
        kill_num = self.get_player_kill_num(p_objid)
        ui_item.lab_kill_no.SetString(str(kill_num))
        ui_item.button_star.EnableCustomState(True)
        if idx >= 0 and idx < len(RANK_PIC):
            ui_item.img_rank.setVisible(True)
            ui_item.img_rank.SetDisplayFrameByPath('', RANK_PIC[idx])
        else:
            ui_item.img_rank.setVisible(False)

        @ui_item.button_star.unique_callback()
        def OnClick(btn, touch, _player_info=player_info):
            if not self._can_click_observer_player_item:
                if global_data.is_inner_server:
                    pass
                return
            p_objid = _player_info[0]
            u_id = _player_info[1]
            if self.observe_target and self.observe_target.id == p_objid:
                return
            if global_data.player:
                from mobile.common.IdManager import IdManager
                global_data.player.req_global_spectate_switch(IdManager.id2str(p_objid), u_id)
                self._can_click_observer_player_item = False

    def on_begin_layer_observe(self, *args):
        if self.camera_state == OBSERVE_FREE_MODE:
            return True
        else:
            return False

    def on_drag_layer_observe(self, layer, touch):
        import world
        scene = world.get_active_scene()
        ctrl = scene.get_com('PartCtrl')
        vec_temp = touch.getDelta()
        x_delta = vec_temp.x
        y_delta = vec_temp.y
        if not ctrl:
            return
        else:
            ctrl.on_touch_slide(x_delta, y_delta, None, touch.getLocation(), True)
            return

    def set_camera_state(self, state, *args):
        if self.camera_state == OBSERVE_FREE_MODE and state != OBSERVE_FREE_MODE:
            self.panel.layer_observe.SetEnableTouch(False)
            self.panel.layer_observe.SetEnableTouch(True)
            self.panel.layer_observe.setVisible(False)
        else:
            self.panel.layer_observe.setVisible(True)
        self.camera_state = state
        self.observe_camera_widget.set_camera_state(state)

    def on_camera_state_changed(self, new_type, old_type, *args):
        if self.observe_camera_widget:
            self.observe_camera_widget.on_camera_state_changed(new_type, old_type)

    def update_like_data(self, like_cnt):
        self.panel.btn_like.SetText(str(like_cnt))
        self._update_like_btn()

    def on_click_btn_like(self, btn, touch):
        uid = self._get_spectate_target_uid()
        if uid <= 0:
            return
        if global_data.player and global_data.player.logic:
            if not global_data.player.can_do_specate_like(uid):
                self._update_like_btn()
                return
            global_data.player.do_global_spectate_like(uid)
            self.inc_btn_like_num()
            self._update_like_btn()

    def on_click_btn_follow(self, btn, touch):
        uid = self._get_spectate_target_uid()
        if uid <= 0:
            return
        if global_data.player and global_data.player.logic:
            if global_data.player.has_follow_player(uid):
                global_data.player.try_unfollow(uid)
            else:
                global_data.player.try_follow(uid)

    def _on_my_bet_info_ret(self, bet_info_list):
        info_list = bet_info_list or []
        if self.observe_target and global_data.battle:
            _comp_id, _comp_round = global_data.battle.get_round_competition_data()
            _battle_id = str(global_data.battle.id)
            _player_id = global_data.player.get_global_spectate_player_uid()
            if _comp_id and (_comp_id == 'SUMMER23_CN' or _comp_id == 'SUMMER23_US' or _comp_id == 'SUMMER23_NA'):
                self.panel.btn_guess.setVisible(True)
            else:
                self.panel.btn_guess.setVisible(False)
            self.can_guess = True

    def on_click_btn_guess(self, btn, touch):
        if not self.observe_target or not global_data.battle or not (global_data.player and global_data.player.logic):
            return
        else:
            _battle_id = str(global_data.battle.id)
            uid = global_data.player.get_global_spectate_player_uid()
            _bet_info_list = global_data.player.get_my_bet_info_list()
            for info in _bet_info_list:
                if info and info.get('battle_id', None) and info.get('battle_id') == _battle_id:
                    uid = info.get('uid', None)
                    break

            global_data.player.pull_bet_player_show_info(str(_battle_id), uid)
            return

    def enable_danmu_input(self, enable):
        if global_data.player and global_data.player.is_in_global_spectate() or self.is_ob:
            self.panel.temp_danmu.setVisible(False)
            return
        self.panel.temp_danmu.setVisible(enable)

    def on_follow_result(self, uid):
        spectate_uid = self._get_spectate_target_uid()
        if uid != spectate_uid:
            return
        self._update_follow_icon()

    def _get_spectate_target_uid(self):
        if not self.observe_target or not self.observe_target.get_owner():
            return 0
        return self.observe_target.get_owner().uid

    def _update_follow_icon(self):
        spectate_uid = self._get_spectate_target_uid()
        if global_data.player and global_data.player.has_follow_player(spectate_uid):
            self.panel.btn_follow.SetText(get_text_by_id(10342))
            self.icon_follow.SetDisplayFrameByPath('', 'gui/ui_res_2/common/icon/icon_follow_sel.png')
        else:
            self.panel.btn_follow.SetText(get_text_by_id(10344))
            self.icon_follow.SetDisplayFrameByPath('', 'gui/ui_res_2/common/icon/icon_follow_nml.png')

    def on_undo_follow_result(self, uid):
        spectate_uid = self._get_spectate_target_uid()
        if uid != spectate_uid:
            return
        self._update_follow_icon()

    def _update_like_btn(self):
        spectate_uid = self._get_spectate_target_uid()
        if global_data.player and global_data.player.can_do_specate_like(spectate_uid, show_tip=False):
            self.panel.btn_like.img_like.SetDisplayFrameByPath('', 'gui/ui_res_2/common/icon/icon_like.png')
        else:
            self.panel.btn_like.img_like.SetDisplayFrameByPath('', 'gui/ui_res_2/common/icon/icon_like2.png')

    def on_click_report_btn(self, btn, touch):
        if self.observe_target:
            from logic.gcommon.common_const.log_const import REPORT_CLASS_BATTLE, REPORT_FROM_TYPE_SPECTATE
            char_name = self.observe_target.ev_g_char_name()
            ui = global_data.ui_mgr.show_ui('UserReportUI', 'logic.comsys.report')
            ui.report_battle_users([{'eid': self.observe_target.id,'name': char_name}])
            ui.set_report_class(REPORT_CLASS_BATTLE)
            ui.set_extra_report_info('', '', REPORT_FROM_TYPE_SPECTATE)

    def on_click_panel(self, btn, touch):
        self.set_select_flag(force_flag=False)

    def set_select_flag(self, force_flag=None):
        if force_flag == None:
            self._selected_flag = not self._selected_flag
        else:
            self._selected_flag = force_flag
        self.panel.btn_flag.SetSelect(self._selected_flag)
        if self._selected_flag:
            if self.observe_target and self.battle_flag:
                battle_flag_utils.init_battle_flag_template_new(self.battle_flag, self.panel.temp_flag, enable_click=False, from_battle=True)
                self.panel.temp_flag.setVisible(True)
            else:
                self.panel.temp_flag.setVisible(False)
        else:
            self.panel.temp_flag.setVisible(False)
        return

    def on_click_flag_btn(self, btn, touch):
        self.set_select_flag()

    def on_update_spectate_cnt(self, cur_specator_cnt):
        self.panel.btn_audience.SetText(str(cur_specator_cnt))
        self.panel.lab_audience.SetString(get_text_by_id(19420).format(num=cur_specator_cnt))

    def on_update_spectate_like_num(self, cur_likenum, total_likenum):
        self.panel.btn_like.SetText(str(total_likenum + cur_likenum))

    def on_update_spectate_hot_info(self, obj_uid, info):
        if obj_uid != self._get_spectate_target_uid():
            return
        battle_mode = global_data.game_mode.get_mode_type()
        hot_val = LiveObserveUIHelper.calculate_popular_num(info, battle_mode)
        spectator_cnt = info.get('spectator_cnt', 1)
        bat_spectator_cnt = int(info.get('bat_spectator_cnt', 0))
        self.set_observe_num(spectator_cnt + bat_spectator_cnt, hot_val)
        like_cnt = info.get('cur_likenum', 0) + info.get('total_likenum', 0)
        self.update_like_data(like_cnt)
        if type(hot_val) is not int:
            log_error('ObserveUI on_update_spectate_hot_info invalid obj_uid=%s, info=%s, hot_val=%s', obj_uid, info, hot_val)

    def inc_btn_like_num(self):
        old_text = self.panel.btn_like.GetText()
        if old_text and old_text.isdigit():
            old_num = int(old_text)
            self.panel.btn_like.SetText(str(old_num + 1))

    def _tick_spectate_hot_info(self):
        if not self.observe_target:
            return
        if not global_data.player:
            return
        global_data.player.req_global_spectate_hot_info(self._get_spectate_target_uid())
        self.panel.DelayCall(ObserveUI.REFRESH_TIME_MIN_INTERVAL, self._tick_spectate_hot_info)

    def set_observe_num(self, cnt, hot_val):
        if type(hot_val) is int and hot_val >= 0:
            hot_val_str = format_popular_num(hot_val)
            self.panel.btn_audience.SetText(hot_val_str)
            self.panel.lab_audience.SetString(get_text_by_id(19468).format(num=hot_val_str))

    def on_audience_btn_begin(self, *args):
        if not self.observe_target:
            return
        self.panel.nd_audience_details.setVisible(True)

    def on_audience_btn_end(self, *args):
        self.panel.nd_audience_details.setVisible(False)

    def need_show_expend_ui(self):
        if global_data.player:
            if global_data.player.is_in_global_spectate():
                return False
            else:
                return True

        return False

    def exit_free_camera(self):
        panel = self.panel
        if panel and panel.isValid():
            if panel.nd_control:
                panel.nd_control.setVisible(True)

    def exit_lock_camera(self):
        panel = self.panel
        if panel and panel.isValid():
            if panel.nd_control:
                panel.nd_control.setVisible(True)

    def on_click_btn_search(self, *args):
        if global_data.game_mode.is_pve():
            ui = global_data.ui_mgr.get_ui('PVEInfoUI')
            if not ui:
                ui = global_data.ui_mgr.show_ui('PVEInfoUI', 'logic.comsys.control_ui')
            ui.appear()