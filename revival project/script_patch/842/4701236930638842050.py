# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLobby.py
from __future__ import absolute_import
import six
from six.moves import range
from . import ScenePart
import world
import render
from logic.gutils.scene_utils import UI_SCENE_BOX_PREFIX
from logic.gcommon.const import DEFAULT_ROLE_ID
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.item import item_const as iconst
from logic.gutils.ConnectHelper import ConnectHelper
from common.platform.dctool import interface
import game3d
from logic.gcommon.common_const.scene_const import LOBBY_EYE_ADAPT_FACTOR
from logic.gutils import item_utils
from logic.gutils import pc_utils
STATE_LOGIN = 0
STATE_RECONNECT = 1
STATE_NORMAL = 2
PLAYER_INDEX = 1

class PartLobby(ScenePart.ScenePart):
    INIT_EVENT = {'show_lobby_common_bg_event': 'show_lobby_common_bg',
       'lobby_state_init_event': 'on_lobby_state_inited',
       'lobby_state_to_prepare': 'on_lobby_state_to_prepare',
       'lobby_state_return_from_prepare': 'return_from_prepare',
       'player_join_team_event': 'on_lobby_state_to_prepare',
       'net_login_reconnect_event': 'on_login_reconnected',
       'avatar_reconnect_destroy_event': 'show_login_reconnect_protect_ui',
       'avatar_finish_create_event': 'on_avatar_finish_create',
       'player_dress_update_event': 'on_avatar_dress_update',
       'app_background_event': 'on_enter_background',
       'app_resume_event': 'on_enter_front',
       'lobby_bgm_change': 'lobby_bgm_change',
       'player_leave_visit_scene_event': 'on_leave_scene',
       'player_enter_visit_scene_event': 'on_enter_scene',
       'on_nile_token_update_event': 'process_nile_logic'
       }

    def __init__(self, scene, name):
        super(PartLobby, self).__init__(scene, name)
        self.state = STATE_NORMAL
        self.init_data_mgr()
        self.init_log_mgr()
        self.bg_music = None
        self.player_model_map = {}
        self.player_task_list = []
        self.ui_created = False
        self._cur_login_reconnect_timer = None
        self._has_notified_nile_enter_lobby = False
        from logic.vscene import scene_type
        global_data.scene_type = scene_type.SCENE_TYPE_LOBBY
        global_data.voice_mgr.init_ngvoice()
        if not global_data.anticheatsdk_mgr:
            from common.platform.AntiCheatSDKMgr import AntiCheatSDKMgr
            anticheat_sdk = AntiCheatSDKMgr()
            anticheat_sdk.init_acsdk()
            anticheat_sdk.set_acsdk_roleinfo()
        global_data.sound_mgr.close_ios_check_sys_mute()
        from logic.comsys.battle.BattleCheckPos import BattleCheckPos
        BattleCheckPos()
        global_data.battle_check_pos.reinit()
        return

    def init_data_mgr(self):
        from logic.comsys.lobby.LobbyRedPointData import LobbyRedPointData
        LobbyRedPointData()
        from logic.comsys.mall_ui.LobbyMallData import LobbyMallData
        LobbyMallData()
        from logic.comsys.home_message_board.MessageBoardManager import MessageBoardManager
        MessageBoardManager()

    def init_log_mgr(self):
        from logic.comsys.log.UILifetimeLogMgr import UILifetimeLogMgr
        UILifetimeLogMgr()
        if global_data.ui_lifetime_log_mgr:
            global_data.ui_lifetime_log_mgr.start_listener()

    def on_enter_scene(self, *args):
        self.lobby_bgm_change(-1)

    def on_leave_scene(self, *args):
        self.lobby_bgm_change(-1)

    def lobby_bgm_change(self, item_no=-1):
        if not global_data.player:
            return
        if item_no == -1:
            is_in_visit_mode = global_data.player.is_in_visit_mode()
            if is_in_visit_mode:
                cur_lobby_bgm = global_data.player.get_visit_lobby_bgm()
            else:
                cur_lobby_bgm = global_data.player.get_lobby_bgm()
            self.change_bgm_by_item_no(cur_lobby_bgm)
        else:
            self.change_bgm_by_item_no(item_no)

    def change_bgm_by_item_no(self, item_no):
        ui = global_data.ui_mgr.get_ui('MallMainUI')
        if ui and ui.isVisible():
            music = 'shop'
        else:
            from ext_package.ext_decorator import has_audio_ext
            if not has_audio_ext():
                music = 'M02_hall_Final'
            else:
                music = item_utils.get_lobby_item_res_path(item_no) or 'M02_hall_Final'
        global_data.sound_mgr.play_music(music)

    def on_enter(self):
        log_error('NX709S_on_partlobby_enter')
        try:
            if global_data.player and global_data.player.lobby and global_data.player.lobby._is_login:
                from logic.gutils.salog import SALog
                salog_writer = SALog.get_instance()
                salog_writer.write(SALog.LOAD_LOBBY)
        except:
            pass

        import wwise
        wwise.SoundEngine.SetRTPCValue('game_settlement', 0)
        global_data.ui_mgr.close_ui('LoginAnimationUI')
        self.lobby_bgm_change(-1)
        self.on_main_model_add_callback()
        from logic.comsys.share.ShareManager import ShareManager
        ShareManager().enable_screen_capture_share()
        log_error('NX709S_on_partlobby_enter_ShareManager')
        from logic.vscene.global_display_setting import GlobalDisplaySeting
        gds = GlobalDisplaySeting()
        gds.high_quality_tex_on()
        global_data.emgr.lobby_scene_pause_event.emit(False)
        render.enable_dynamic_culling(False)
        scn = self.scene()
        scn.set_adapt_factor(LOBBY_EYE_ADAPT_FACTOR)
        self.on_deep_link()
        global_data.game_mgr.post_exec(self.open_keyboard_control)
        global_data.deviceinfo.start_upload_proc_info_pc()
        global_data.game_voice_mgr.unload_bank()
        if not G_IS_NA_PROJECT:
            m = global_data.game_mgr.scene.get_model('zhujiemian_cj_tiehua_115')
            if m and m.valid:
                m.set_rendergroup_and_priority(world.RENDER_GROUP_ALPHATEST, -999)
            m = global_data.game_mgr.scene.get_model('dating_03_a_138')
            if m and m.valid:
                m.all_materials.enable_write_alpha = True
        global_data.battle_check_pos and global_data.battle_check_pos.check_pos_switch(True)
        log_error('NX709S_on_partlobby_enter_end')
        self.process_nile_logic()
        self.check_start_musdk_checker()

    def open_keyboard_control(self):
        if not pc_utils.check_can_enable_pc_mode():
            return
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.enable_PC_control(False)
            global_data.pc_ctrl_mgr.set_pc_control_switch_enabled(False)
            global_data.pc_ctrl_mgr.enable_keyboard_control(True)

    def init_bw_box(self):
        ref_box_index = UI_SCENE_BOX_PREFIX + str(PLAYER_INDEX)
        self.box_offset = {}
        scn = self.scene()
        ref_box_position = scn.get_model(ref_box_index).world_position
        for idx in range(1, 5):
            cnt_box_pos = scn.get_model(UI_SCENE_BOX_PREFIX + str(idx)).world_position
            self.box_offset[idx] = cnt_box_pos - ref_box_position

    def return_from_prepare(self):
        global_data.ui_mgr.show_ui('LobbyUI', 'logic.comsys.lobby')
        dresser_model = self.get_dresser_model(PLAYER_INDEX)
        if not dresser_model:
            return
        model = dresser_model.get_model()
        if model:
            model.clear_events()
            self.play_idle_animation(model, PLAYER_INDEX)

    def on_lobby_state_to_prepare(self, *args):
        dresser_model = self.get_dresser_model(PLAYER_INDEX)
        if not dresser_model:
            return
        model = dresser_model.get_model()
        if model:
            model.clear_events()
            self.play_sitting_animation(model, PLAYER_INDEX)

    def on_lobby_state_inited(self, state):
        self.state = state

    def show_lobby_common_bg(self, is_show):
        from logic.comsys.common_ui.LobbyCommonBgUI import LobbyCommonBgUI
        if is_show:
            LobbyCommonBgUI()
        else:
            global_data.ui_mgr.close_ui('LobbyCommonBgUI')

    def create_lobby_ui(self):
        if global_data.player is None:
            return
        else:
            global_data.temporary_force_image_sync = True
            log_error('NX709S_on_partlobby_create_lobby_ui')
            from logic.comsys.guide_ui.LobbyGuideManager import LobbyGuideManager
            LobbyGuideManager().start_show_guide()
            global_data.player.show_antiaddiction_msg()
            if global_data.is_pve_lobby:
                global_data.ui_mgr.show_ui('PVELobbyUI', 'logic.comsys.lobby')
            else:
                global_data.ui_mgr.show_ui('LobbyUI', 'logic.comsys.lobby')
            global_data.ui_mgr.show_ui('MainChat', 'logic.comsys.chat')
            global_data.ui_mgr.show_ui('NewChatPigeon', 'logic.comsys.chat')
            if global_data.message_data.get_seting_inf('lobby_guidance'):
                global_data.message_data.set_seting_inf('lobby_guidance', 0)
            global_data.ui_mgr.close_ui('BattleGuidance')
            global_data.ui_mgr.show_ui('LobbyItemDescUI', 'logic.comsys.mecha_display')
            if not global_data.is_32bit:
                global_data.ui_mgr.show_ui('ScreenTouchEffectUI', 'logic.comsys.common_ui')
                global_data.ui_mgr.show_ui('LobbyItemObtainDescUI', 'logic.comsys.mecha_display')
                global_data.ui_mgr.show_ui('CommonDescUI', 'logic.comsys.mall_ui')
                global_data.ui_mgr.show_ui('RewardPreviewUI', 'logic.comsys.reward')
                global_data.ui_mgr.show_ui('ReceiveRewardUI', 'logic.comsys.reward')
                global_data.ui_mgr.show_ui('LotteryBroadcastUI', 'logic.comsys.lottery')
                global_data.ui_mgr.show_ui('GetModelDisplayUI', 'logic.comsys.mall_ui')
                global_data.ui_mgr.show_ui('GetModelDisplayBeforeUI', 'logic.comsys.mall_ui')
                global_data.ui_mgr.show_ui('GetWeaponDisplayUI', 'logic.comsys.mall_ui')
            global_data.ui_mgr.show_ui('NetworkLagUI', 'logic.comsys.common_ui')
            global_data.emgr.lobby_ui_on_event.emit()
            self.ui_created = True
            log_error('NX709S_on_partlobby_create_lobby_ui_end')
            self.process_nile_logic()
            if global_data.player:
                global_data.player.check_auto_match_tid()
            global_data.temporary_force_image_sync = False
            from logic.comsys.setting_ui.UnderageHelper import check_underage_mode
            check_underage_mode()
            return

    def on_login_reconnected(self, *args):
        global_data.ui_mgr.close_ui('RoomCreateUI')
        global_data.ui_mgr.close_ui('RoomUI')
        global_data.ui_mgr.close_ui('RoomCreateUINew')
        global_data.ui_mgr.close_ui('RoomListUINew')
        global_data.ui_mgr.close_ui('RoomUINew')
        global_data.ui_mgr.close_ui('PlayerSimpleInf')
        global_data.ui_mgr.close_ui('MainSettingUI')
        global_data.emgr.hide_item_desc_ui_event.emit()
        global_data.emgr.close_reward_preview_event.emit()
        global_data.ui_mgr.close_ui('ReceiveRewardUI')
        global_data.ui_mgr.close_ui('LotteryBroadcastUI')
        global_data.ui_mgr.close_ui('TaskMainUI')
        global_data.ui_mgr.close_ui('NewbiePassUI')
        global_data.ui_mgr.close_ui('GetModelDisplayBeforeUI')
        global_data.ui_mgr.show_ui('ReceiveRewardUI', 'logic.comsys.reward')

    def get_dresser_model(self, index):
        return self.player_model_map.get(index, None)

    def add_player(self, uid, member, role=DEFAULT_ROLE_ID, dress_dict={}):
        index = self.get_player_model_index()
        self.add_player_model(index, role, dress_dict)

    def add_player_model(self, index, role=DEFAULT_ROLE_ID, dress_dict={}):
        if index >= 1 and index <= 4:
            if index not in self.player_model_map:
                self.player_model_map[index] = None
                from logic.gutils import dress_utils
                from logic.gcommon.item.item_const import DRESS_POS_FACE
                path = dress_utils.get_dress_path_by_item_no_and_part_id(dress_dict.get(DRESS_POS_FACE), DRESS_POS_FACE, role)
                self.player_task_list.append(world.create_model_async(path, self._load_model_complete, (index, role, dress_dict)))
        return

    def remove_player_model(self, index):
        if index in self.player_model_map:
            dresser = self.player_model_map[index]
            model = dresser.get_model() if dresser else None
            if model:
                model.clear_events()
                model.destroy()
            del self.player_model_map[index]
        return

    def remove_other_player_model(self):
        for i in range(2, 5):
            if i in self.player_model_map:
                self.remove_player_model(i)

    def _load_model_complete(self, model, udata, current_task):
        if current_task not in self.player_task_list:
            return
        index, role, clothing_dict = udata
        if index in self.player_model_map and self.player_model_map[index]:
            return
        self.player_task_list.remove(current_task)
        scn = self.scene()
        scn.add_object(model)
        pos_model = self.box_offset[index]
        model.world_position = pos_model
        from logic.gutils import dress_utils
        path = dress_utils.get_dress_path_by_item_no_and_part_id(clothing_dict.get(iconst.DRESS_POS_FACE), iconst.DRESS_POS_FACE, role)
        suit_id = dress_utils.get_suit_id_by_clothing(clothing_dict, role)
        dresser = dress_utils.DresserModel(model, role, iconst.LOD_H, dress_dict={iconst.DRESS_POS_FACE: path}, suit_id=suit_id)
        self.player_model_map[index] = dresser

        def callback():
            model.visible = True
            if index == PLAYER_INDEX:
                self.on_main_model_add_callback()
            else:
                self.play_sitting_animation(model, index)

        dresser.dress(clothing_dict, callback)

    def on_main_model_add_callback(self):
        log_error('NX709S_on_partlobby_on_main_model_add_callback')
        global_data.emgr.camera_inited_event.emit()
        self.create_lobby_ui()

    def get_player_model_index(self):
        for i in range(2, 5):
            if i not in self.player_model_map:
                return i

    def on_ani_changed(self, index, ani):
        if index == PLAYER_INDEX:
            global_data.emgr.play_main_camera_trk_event.emit(ani, False)

    def play_walking_animation(self, index):
        ani_name = 'bar_walk_into'
        model = self.player_model_map[index]
        model = model.get_model()
        if not model:
            return
        model.register_on_end_event(self.on_walking_ani_end, False, (index,))
        model.play_animation(ani_name)
        self.on_ani_changed(index, ani_name)

    def on_walking_ani_end(self, model, user_data):
        self.create_lobby_ui()
        self.play_idle_animation(model, user_data[0])

    def play_idle_animation(self, model, index):
        if not self.ui_created:
            self.create_lobby_ui()
        model.register_on_end_event(self._on_play_idle_animation, False, index)
        self._on_play_idle_animation(model, index)

    def _on_play_idle_animation(self, model, index):
        ani_name_list = [
         'bar_idle', 'bar_idle_01']
        camera_ani = 'bar_idle'
        idle_ratio = 0.8
        import random
        ratio = random.random()
        ani = ani_name_list[1] if ratio > idle_ratio else ani_name_list[0]
        ani = ani_name_list[1]
        model.play_animation(ani)
        self.on_ani_changed(index, camera_ani)

    def play_sitting_animation(self, model, index):
        if not self.ui_created:
            self.create_lobby_ui()
        self.play_idle_animation(model, index)

    def play_sitted_animation(self, model, index):
        ani_name = 'bar_sit_idle'
        model.play_animation(ani_name)
        self.on_ani_changed(index, ani_name)

    def on_exit(self):
        log_error('NX709S_on_partlobby_on_on_exit')
        global_data.battle_check_pos.on_finalize()
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        if global_data.player:
            global_data.player.clear_advance_sequence()
        global_data.ui_mgr.close_all_ui(exceptions=('WizardTrace', 'ProfileGraphUI',
                                                    'JudgeLoadingUI', 'FreeRecordUI',
                                                    'EndHighlightUI', 'VideoManualCtrlUI',
                                                    'PlayerListLoadingWidget', 'SnatchEggPlayerListLoadingWidget'))
        self.clear_models()
        self.clear_tasks()
        self.stop_login_reconnect_timer()
        from logic.comsys.share.ShareManager import ShareManager
        ShareManager().disable_screen_capture_share()
        global_data.emgr.lobby_scene_pause_event.emit(True)
        render.enable_dynamic_culling(global_data.feature_mgr.is_support_dyculling())
        from logic.vscene.global_display_setting import GlobalDisplaySeting
        gds = GlobalDisplaySeting()
        gds.high_quality_tex_off()
        global_data.item_cache_without_check.clear_cache()
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.set_pc_control_switch_enabled(True)
        if global_data.ui_lifetime_log_mgr:
            global_data.ui_lifetime_log_mgr.finish_all_record()
            global_data.ui_lifetime_log_mgr.send_record_log_to_server()
            global_data.ui_lifetime_log_mgr.stop_listener()
        if global_data.lobby_guide_mgr:
            global_data.lobby_guide_mgr.finalize()
        if global_data.live_platform_mgr:
            global_data.live_platform_mgr.clear_all_cache()
        global_data.battle_check_pos and global_data.battle_check_pos.check_pos_switch(False)
        log_error('NX709S_on_partlobby_on_on_end')
        if global_data.nile_sdk:
            global_data.nile_sdk.pause()
        if global_data.mecha_memory_stat_mgr:
            global_data.mecha_memory_stat_mgr.invalidate_mecha_memory_cur_and_all_season_data()
        if global_data.player:
            global_data.player.set_auto_match_tid(None)
        from common.crashhunter import crashhunter_utils
        crashhunter_utils.check_shader_compile_error()
        return

    def on_pause(self, flag):
        super(PartLobby, self).on_pause(flag)
        global_data.emgr.lobby_scene_pause_event.emit(flag)

    def clear_tasks(self):
        for task in self.player_task_list:
            task.cancel()

        self.player_task_list = []

    def clear_models(self):
        for idx, dress_model in six.iteritems(self.player_model_map):
            if dress_model:
                model = dress_model.get_model()
                model.clear_events()
                model.destroy()

        self.player_model_map = {}

    def show_login_reconnect_protect_ui(self, *args):
        import common.utils.timer as timer
        self._cur_login_reconnect_timer = global_data.game_mgr.register_logic_timer(self.select_login_reconnect_action, interval=3.0, times=-1, mode=timer.CLOCK)
        from logic.comsys.common_ui.NormalConfirmUI import BusyReconnectBg
        BusyReconnectBg()

    def stop_login_reconnect_timer(self):
        global_data.game_mgr.unregister_logic_timer(self._cur_login_reconnect_timer)
        global_data.ui_mgr.close_ui('BusyReconnectBg')

    def select_login_reconnect_action(self):
        from logic.comsys.common_ui.NormalConfirmUI import LoginReconnectConfirmDlg

        def cancel():
            ConnectHelper().pop_failed_confirm_fall_back_server_select()

        LoginReconnectConfirmDlg().confirm(content=get_text_local_content(134), cancel_callback=cancel)

    def on_avatar_finish_create(self):
        self.stop_login_reconnect_timer()
        global_data.ui_mgr.close_ui('LoginReconnectConfirmDlg')
        if not self.ui_created:
            self.create_lobby_ui()
        self.process_nile_logic()

    def on_avatar_dress_update(self, parts):
        player = global_data.player
        dresser = self.get_dresser_model(PLAYER_INDEX)
        for part_id in parts:
            item_no = player.get_clothing_by_part_id(part_id)
            dresser.dress({part_id: {'item_id': item_no}})

    def on_deep_link(self):
        from logic.gutils import deeplink_utils
        deeplink_utils.check_clipboard_text()
        deeplink_utils.on_deep_link()

    def on_enter_background(self):
        if global_data.share_mgr:
            global_data.share_mgr.disable_screen_capture_share()

    def on_enter_front(self):
        if global_data.share_mgr:
            global_data.share_mgr.enable_screen_capture_share()

    def process_nile_logic(self):
        if not global_data.nile_sdk:
            return
        if not global_data.nile_sdk.is_started():
            if global_data.player and global_data.player.get_nile_token():
                global_data.nile_sdk.on_update_state_with_token(global_data.player.get_nile_token())
            return
        if global_data.nile_sdk.is_paused():
            global_data.nile_sdk.resume()
        if not self._has_notified_nile_enter_lobby:
            global_data.nile_sdk.on_notify_enter_lobby()
            self._has_notified_nile_enter_lobby = True

    def check_start_musdk_checker(self):
        if global_data.channel and global_data.channel.is_musdk():
            from logic.vscene.parts.ctrl.MuSdkMgr import MuSdkMgr
            MuSdkMgr()