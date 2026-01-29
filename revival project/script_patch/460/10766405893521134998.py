# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/Lobby.py
from __future__ import absolute_import
from __future__ import print_function
from logic.entities.BaseClientEntity import BaseClientEntity
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const import lobby_const
import six_ex

class Lobby(BaseClientEntity):
    ST_LOADING = -1
    ST_RUNNING = 0
    ST_CLOSED = 1

    def __init__(self, entityid):
        super(Lobby, self).__init__(entityid)
        global_data.emgr.net_reconnect_event += self.on_reconnected
        global_data.emgr.net_login_reconnect_event += self.on_reconnected
        global_data.emgr.need_show_room_ui_event += self.on_need_show_room_ui
        global_data.emgr.lobby_ui_on_event += self.on_lobby_ui_on
        global_data.emgr.settle_ui_exit += self.load_scene
        global_data.emgr.change_lobby_scene += self.switch_pve_lobby_scene
        self._lobby_status = Lobby.ST_LOADING
        self.is_lobby_ui_on = False

    def init_from_dict(self, bdict):
        player = global_data.player
        if player:
            player.reset_lobby(self)
            if player.local_battle:
                player.quit_local_battle()
                player.clear_local_battle_data()
                return
            if player.new_local_battle:
                player.quit_new_local_battle()
                return
            player.enter_place(lobby_const.PLACE_LOBBY)
        self._is_login = bdict.get('is_login', False)
        self._is_from_global_spectate = bdict.get('from_global_spectate', False)
        self._is_from_newbie_stage = bdict.get('from_newbie_stage', False)
        combat_state = bdict.get('combat_state', battle_const.COMBAT_STATE_NONE)
        print('init lobby entity')
        self.load_scene(combat_state)
        global_data.had_enter_lobby = True

    def destroy(self):
        if global_data.player:
            global_data.player.reset_lobby(None)
        if self._lobby_status == Lobby.ST_CLOSED:
            return
        else:
            self._lobby_status = Lobby.ST_CLOSED
            if global_data.scene_background:
                global_data.scene_background.leave_lobby()
            super(Lobby, self).destroy()
            return

    def on_reconnected(self, *args):
        from logic.comsys.battle.Settle.SettleSystem import SettleSystem
        SettleSystem.finalize()
        self.destroy()

    def load_scene(self, combat_state=battle_const.COMBAT_STATE_NONE):
        from logic.comsys.battle.Settle.SettleSystem import SettleSystem
        if SettleSystem.get_instance() is not None:
            SettleSystem.finalize()
        from logic.gutils.salog import SALog
        salog_writer = SALog.get_instance()
        salog_writer.set_before_load_time()
        from common.cfg import confmgr
        if global_data.is_pve_lobby:
            scene_type = 'PVELobby'
            scene_conf = confmgr.get('scenes', scene_type)
        else:
            scene_type = 'Lobby'
            scene_conf = confmgr.get('scenes', scene_type)
        if self.is_in_lobby_scene():
            self.load_lobby_finish(combat_state)
        else:
            print('load lobby scene')
            global_data.game_mgr.load_scene(scene_type, scene_conf, lambda : self.load_lobby_finish(combat_state))
            global_data.game_mgr.next_exec(lambda : global_data.ex_scene_mgr_agent and global_data.ex_scene_mgr_agent.pop_settle_scene())
        return

    def switch_pve_lobby_scene(self):
        from data.battle_trans_anim import Getmecha_boarding_tdm
        from common.cinematic.movie_controller import MovieController
        self.close_lobby_ui()
        MovieController().start(Getmecha_boarding_tdm(), lambda : self.load_scene())

    def close_lobby_ui(self):
        global_data.ui_mgr.close_ui('PVELobbyUI')
        global_data.ui_mgr.close_ui('LobbyUI')
        global_data.ui_mgr.close_ui('MatchMode')
        global_data.ui_mgr.close_ui('MainChat')
        global_data.ui_mgr.close_ui('MainFriend')
        global_data.ui_mgr.close_ui('MainRank')
        global_data.ui_mgr.close_ui('PlayerInfoUI')
        global_data.ui_mgr.close_ui('ActivityMain')
        global_data.ui_mgr.close_ui('ActivityCenterMainUI')
        global_data.ui_mgr.close_ui('ActivityGranbelmMainUI')
        global_data.ui_mgr.close_ui('LobbyCommonBgUI')
        global_data.ui_mgr.close_ui('ModelArrowUI')
        if global_data.redpoint_mgr:
            global_data.redpoint_mgr.remove_all_elems()

    def is_in_lobby_scene(self):
        cnt_scene = global_data.game_mgr.scene
        if not cnt_scene:
            return False
        from logic.gutils.scene_utils import is_lobby_relatived_scene
        if is_lobby_relatived_scene(cnt_scene.scene_type):
            return True
        return False

    def load_settle_finish(self):
        global_data.emgr.battle_logic_ready_event.emit()
        global_data.emgr.camera_inited_event.emit()
        from logic.comsys.battle.Settle.SettleSystem import SettleSystem
        if SettleSystem.get_instance() is not None and SettleSystem().show_entire_team():
            SettleSystem.finalize()
        else:
            SettleSystem.finalize()
            self.load_scene()
        return

    def is_lobby_loaded(self):
        return self._lobby_status == Lobby.ST_RUNNING

    def load_lobby_finish(self, combat_state):
        self._lobby_status = Lobby.ST_RUNNING
        from logic.vscene.parts import PartLobby
        lobby_inited_state = PartLobby.STATE_NORMAL
        if self._is_login:
            lobby_inited_state = PartLobby.STATE_LOGIN
            from logic.gutils.salog import SALog
            salog_writer = SALog.get_instance()
            salog_writer.write(SALog.LOAD)
        if self._is_from_global_spectate:
            global_data.player and global_data.player.reset_global_spectate_on_disconnect()
        if combat_state == battle_const.COMBAT_STATE_NONE:
            global_data.new_sys_open_mgr.active_check_addition()
            global_data.player and global_data.player.check_open_live_medal()
            global_data.player and global_data.player.start_show_advance()
            global_data.new_sys_open_mgr.check_show_ui()
            global_data.sys_unlock_mgr.check_show_ui()
            global_data.player and global_data.player.show_reserve_info()
        elif combat_state == battle_const.COMBAT_STATE_DIE:
            global_data.new_sys_open_mgr.active_check_addition()
            global_data.player and global_data.player.check_open_live_medal()
            global_data.player and global_data.player.start_show_advance()
            global_data.new_sys_open_mgr.check_show_ui()
            global_data.sys_unlock_mgr.check_show_ui()
            self.inform_avatar_battle_is_finish()
            global_data.player and global_data.player.show_reserve_info()
        elif combat_state == battle_const.COMBAT_STATE_FIGHT or combat_state == battle_const.COMBAT_STATE_SPECTATE:
            lobby_inited_state = PartLobby.STATE_RECONNECT
        global_data.emgr.lobby_state_init_event.emit(lobby_inited_state)
        if global_data.player:
            global_data.player.fix_shiny_weapon_id_error()
        self.re_enter_local_battle()
        from common.uisys.BackgroundManager import SceneBackground
        SceneBackground()
        from logic.gcommon.common_const import scene_const
        load_lobby_relatived_scene = [
         scene_const.SCENE_LUCKY_HOUSE,
         scene_const.SCENE_LUCKY_HOUSE_FLASH,
         scene_const.SCENE_LOTTERY,
         scene_const.SCENE_MECHA_RECONSTRUCT,
         scene_const.SCENE_SKIN_DEFINE,
         scene_const.SCENE_JIEMIAN_COMMON,
         scene_const.SCENE_GET_MECHA_MODEL_DISPLAY,
         scene_const.SCENE_GET_WEAPON_DISPLAY]
        for scene_type in load_lobby_relatived_scene:
            global_data.ex_scene_mgr_agent.load_lobby_relatived_scene(scene_type)

        load_lobby_relatived_scene_extra_data = {scene_const.SCENE_PVE_MAIN_UI: {'callback': self.on_need_jump_to_pve_main_ui,'scene_data': None}}
        for scene_type, extra_data in six_ex.items(load_lobby_relatived_scene_extra_data):
            global_data.ex_scene_mgr_agent.load_lobby_relatived_scene(scene_type, extra_data.get('callback'), extra_data.get('scene_data'))

        global_data.emgr.refresh_lottery_btn_enable.emit(True)
        if lobby_inited_state == PartLobby.STATE_NORMAL:
            from logic.gutils.salog import SALog
            salog_writer = SALog.get_instance()
            salog_writer.send_saved_battle_archive()
        from logic.gutils.guide_utils import is_quality_level_initial
        if not is_quality_level_initial() and global_data.player:
            global_data.ui_mgr.show_ui('QualityLevelInitialUI', 'logic.comsys.setting_ui')
        try:
            import game3d
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                import os
                _path = os.path.join(game3d.get_doc_dir(), 'entered_lobby_flag')
                if not os.path.exists(_path):
                    f = open(_path, 'w+')
                    f.write('success')
                    f.close()
        except:
            pass

        if self._is_login:
            global_data.emgr.on_login_enter_lobby.emit()
        global_data.ui_mgr.close_ui('PlayerListLoadingWidget')
        global_data.ui_mgr.close_ui('SnatchEggPlayerListLoadingWidget')
        return

    def inform_avatar_battle_is_finish(self):
        from logic.gcommon.common_utils.local_text import get_text_by_id
        from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
        NormalConfirmUI2(content=get_text_by_id(123))

    def on_need_jump_to_pve_main_ui(self):
        from logic.gutils.jump_to_ui_utils import jump_to_pve_level_select, jump_to_pve_main_ui
        from logic.gcommon.common_const.pve_const import MATCH_AGAIN_TYPE_AUTO_MATCH
        if global_data.rematch_pve_tag:
            if not global_data.player:
                return
            if not global_data.player.is_leader(False):
                import game3d
                game3d.delay_exec(30, global_data.player.rematch_pve_battle)
            if global_data.player.is_in_team() or global_data.rematch_pve_tag == MATCH_AGAIN_TYPE_AUTO_MATCH:
                jump_to_pve_level_select()
            return
        if global_data.refresh_pve_settle_tag:
            jump_to_pve_main_ui()

    def on_need_show_room_ui(self):
        if not global_data.player:
            return
        if not global_data.ui_mgr.get_ui('LobbyUI'):
            return
        room_info = global_data.player.get_cur_custom_room_info()
        if room_info:
            self.on_show_room_ui(room_info)
            global_data.emgr.on_show_room_ui_event.emit()
        if global_data.player.get_room_dissolved_in_battle():
            global_data.game_mgr.show_tip(get_text_by_id(19304), True)
            global_data.player.set_room_dissolved_in_battle(False)
        if global_data.player.get_player_kicked_in_battle():
            global_data.game_mgr.show_tip(get_text_by_id(19332), True)
            global_data.player.set_player_kicked_in_battle(False)

    def on_show_room_ui(self, _room_info):
        room_type = global_data.player.get_room_type(_room_info.get('battle_type', None))
        if room_type == 1:
            room_ui = global_data.ui_mgr.get_ui('RoomUI')
            if not room_ui:
                from logic.comsys.room.RoomUI import RoomUI
                RoomUI(None, _room_info)
            else:
                room_ui.init_room(_room_info)
        else:
            room_ui = global_data.ui_mgr.get_ui('RoomUINew')
            if not room_ui:
                from logic.comsys.room.RoomUINew import RoomUINew
                RoomUINew(None, _room_info)
            else:
                room_ui.init_room(_room_info)
        return

    def on_lobby_ui_on(self):
        self.on_need_show_room_ui()

    def re_enter_local_battle(self):
        player = global_data.player
        if player and player.in_local_battle():
            player.clear_local_battle_data()
        if not self._is_login and self._is_from_newbie_stage and player:
            ui = global_data.ui_mgr.show_ui('CertificateMainUI', 'logic.comsys.guide_ui')
            ui and ui.pass_assessment()