# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartBgSound.py
from __future__ import absolute_import
import game3d
from . import ScenePart
from logic.gcommon.common_const import battle_const
from logic.gcommon import time_utility as tutil
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
import common.utils.timer as timer
BATTLE_MUSIC_STATE_HUMAN = 0
BATTLE_MUSIC_STATE_LEAVE = 1
BATTLE_MUSIC_STATE_FIND_ENEMY = 2
BATTLE_MUSIC_STATE_FIGHT = 3
DEATH_MODE_CHANGE_MUSIC_TIME = 57

class PartBgSound(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartBgSound, self).__init__(scene, name)
        self.poison_level = 0
        self.battle_state = BATTLE_MUSIC_STATE_HUMAN
        self.battle_state_delay_exec_id = None
        self.player = None
        self.mecha = None
        self.first_call_mecha = False
        self.sound_mgr = global_data.sound_mgr
        self._music_obj = global_data.sound_mgr._music_obj
        self._cur_death_music = None
        self.delay_timer = None
        self.delay_gvg_timer = None
        self.is_bg_music_enable = False
        self.init_battle_event()
        self.pve_music_res = []
        return

    def on_enter(self):
        self.first_call_mecha = False
        if global_data.game_mode.get_mode_type() in (game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_DUEL):

            def callback():
                self.sound_mgr.stop_music()
                self.play_music('gvg')

            self.delay_gvg_timer = game3d.delay_exec(3000, callback)
        elif global_data.game_mode.is_pve():
            self.pve_music_res = global_data.battle.get_pve_bgm_path()

            def cb_pve():
                self.sound_mgr.stop_music('pve')
                self.sound_mgr.play_music(self.pve_music_res[0], 'pve')

            self.delay_gvg_timer = game3d.delay_exec(3000, cb_pve)

    def init_battle_event(self):
        if global_data.player.in_local_battle():
            return
        mode_type = global_data.game_mode.get_mode_type()
        if game_mode_const.is_mode_type(mode_type, (game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_DUEL)):
            global_data.emgr.scene_camera_player_setted_event += self.on_cam_player_setted_gvg
        elif game_mode_const.is_mode_type(mode_type, game_mode_const.TDM_BattleBGM):
            global_data.emgr.update_battle_timestamp += self.on_battle_timestamp
        elif game_mode_const.is_mode_type(mode_type, game_mode_const.GAME_MODE_PVES):
            global_data.emgr.pve_fight_state_changed += self.on_pve_fight_state_changed
        else:
            global_data.emgr.scene_camera_player_setted_event += self.on_cam_player_setted
            global_data.emgr.sound_visible_add += self.check_refresh_battle_state
            global_data.emgr.scene_reset_poison_level += self.set_poison_level
            global_data.emgr.scene_check_enter_battle_state += self.check_enter_battle_state_ex
            global_data.emgr.reset_join_mecha_bgm += self.reset_first_call_mecha
        global_data.emgr.scene_summon_mecha += self.on_summon_mecha

    def on_exit(self):
        if self.delay_timer:
            global_data.game_mgr.unregister_logic_timer(self.delay_timer)
        if self.delay_gvg_timer:
            game3d.cancel_delay_exec(self.delay_gvg_timer)
        self.exit_battle_event()
        mode = 'pve' if global_data.game_mode.is_pve() else None
        self.sound_mgr.stop_music(mode)
        return

    def exit_battle_event(self):
        mode_type = global_data.game_mode.get_mode_type()
        if game_mode_const.is_mode_type(mode_type, (game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_DUEL)):
            global_data.emgr.scene_camera_player_setted_event -= self.on_cam_player_setted_gvg
        elif game_mode_const.is_mode_type(mode_type, game_mode_const.TDM_BattleBGM):
            global_data.emgr.update_battle_timestamp -= self.on_battle_timestamp
        elif game_mode_const.is_mode_type(mode_type, game_mode_const.GAME_MODE_PVES):
            global_data.emgr.pve_fight_state_changed -= self.on_pve_fight_state_changed
        else:
            global_data.emgr.scene_camera_player_setted_event -= self.on_cam_player_setted
            global_data.emgr.sound_visible_add -= self.check_refresh_battle_state
            global_data.emgr.scene_reset_poison_level -= self.set_poison_level
            global_data.emgr.scene_check_enter_battle_state -= self.check_enter_battle_state_ex
            global_data.emgr.reset_join_mecha_bgm -= self.reset_first_call_mecha
        global_data.emgr.scene_summon_mecha -= self.on_summon_mecha

    def reset_first_call_mecha(self):
        if self.first_call_mecha:
            self.first_call_mecha = False

    def on_cam_player_setted_gvg(self):
        self.play_music('gvg')

    def on_cam_player_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.unbind_mecha_injured_event()
        self.bind_player_event(self.player, is_bind=False)
        self.player = player
        if self.player:
            self.bind_player_event(self.player, is_bind=True)

    def bind_player_event(self, target, is_bind=True):
        if target and target.is_valid():
            if is_bind:
                ope_func = target.regist_event
            else:
                ope_func = target.unregist_event
            ope_func('E_ON_JOIN_MECHA', self.bind_mecha_injured_event_by_id)
            ope_func('E_ON_LEAVE_MECHA', self.unbind_mecha_injured_event)
            if target.get_value('G_IN_MECHA'):
                control_target = target.get_value('G_CONTROL_TARGET')
                self.bind_mecha_injured_event_by_target(control_target)

    def unbind_mecha_injured_event(self, check_state=True):
        if self.mecha:
            ope_func = self.mecha.unregist_event
            ope_func('E_HITED_SHOW_HURT_DIR', self.check_enter_battle_state)
            self.mecha = None
            if check_state:
                self.mecha_state_change()
        return

    def bind_mecha_injured_event_by_id(self, mecha_id, *args, **kwargs):
        self.unbind_mecha_injured_event(False)
        from mobile.common.EntityManager import EntityManager
        target = EntityManager.getentity(mecha_id)
        if target is None:
            return
        else:
            self.mecha = target.logic
            ope_func = self.mecha.regist_event
            ope_func('E_HITED_SHOW_HURT_DIR', self.check_enter_battle_state)
            self.mecha_state_change()
            return

    def bind_mecha_injured_event_by_target(self, target):
        self.unbind_mecha_injured_event()
        self.mecha = target.logic
        if self.mecha:
            ope_func = self.mecha.regist_event
            ope_func('E_HITED_SHOW_HURT_DIR', self.check_enter_battle_state)

    def check_enter_battle_state(self, unit, pos, damage=0, is_mecha=False):
        if is_mecha:
            self.enter_battle_state()

    def check_refresh_battle_state(self, entity, pos, sound_type, distance_sqr, driver_id=None):
        import logic.gcommon.const as const
        if self.mecha and sound_type == const.SOUND_TYPE_MECHA_FOOTSTEP:
            self.reset_battle_state_downcount()

    def check_enter_battle_state_ex(self, triger):
        if self.player == triger.logic and self.mecha:
            self.enter_battle_state()

    @execute_by_mode(True, (game_mode_const.GAME_MODE_SURVIVALS,))
    def set_poison_level(self, level):
        self.poison_level = level
        if level >= battle_const.BATTLE_SOUND_STATE_HARD:
            if self.battle_state <= BATTLE_MUSIC_STATE_LEAVE:
                rtpc_value = 0
            elif self.battle_state == BATTLE_MUSIC_STATE_FIGHT:
                rtpc_value = 20
            elif self.battle_state == BATTLE_MUSIC_STATE_FIND_ENEMY:
                rtpc_value = 10
            self.sound_mgr.set_rtpc('battle_hard', rtpc_value, self._music_obj)
            self.play_music('battle_hard')
        elif self.poison_level >= battle_const.BATTLE_SOUND_STATE_MEDIUM:
            if self.battle_state == BATTLE_MUSIC_STATE_HUMAN:
                self.play_music('stop')
            else:
                if self.battle_state == BATTLE_MUSIC_STATE_LEAVE:
                    rtpc_value = 0
                elif self.battle_state == BATTLE_MUSIC_STATE_FIGHT:
                    rtpc_value = 20
                elif self.battle_state == BATTLE_MUSIC_STATE_FIND_ENEMY:
                    rtpc_value = 10
                self.sound_mgr.set_rtpc('battle_medium', rtpc_value, self._music_obj)
                self.play_music('battle_medium')
        elif self.poison_level >= battle_const.BATTLE_SOUND_STATE_LOW or self.first_call_mecha:
            if self.battle_state == BATTLE_MUSIC_STATE_HUMAN:
                self.play_music('stop')
            else:
                if self.battle_state == BATTLE_MUSIC_STATE_LEAVE:
                    rtpc_value = 0
                elif self.battle_state == BATTLE_MUSIC_STATE_FIGHT:
                    rtpc_value = 20
                elif self.battle_state == BATTLE_MUSIC_STATE_FIND_ENEMY:
                    rtpc_value = 10
                self.sound_mgr.set_rtpc('battle_low', rtpc_value, self._music_obj)
                self.play_music('battle_low')

    def mecha_state_change(self):
        from logic.gcommon.common_const import battle_const
        if self.mecha:
            if self.battle_state == BATTLE_MUSIC_STATE_HUMAN:
                self.battle_state = BATTLE_MUSIC_STATE_LEAVE
                if not self.first_call_mecha:

                    def callback():
                        if not self.first_call_mecha:
                            self.first_call_mecha = True

                    game3d.delay_exec(4000, callback)
                elif self.mecha:
                    self.resume_bg_sound()
                if self.poison_level >= battle_const.BATTLE_SOUND_STATE_HARD:
                    pass
                elif self.poison_level >= battle_const.BATTLE_SOUND_STATE_MEDIUM:
                    self.sound_mgr.set_rtpc('battle_medium', 0, self._music_obj)
                    self.play_music('battle_medium')
                elif self.poison_level >= battle_const.BATTLE_SOUND_STATE_LOW or self.first_call_mecha:
                    self.sound_mgr.set_rtpc('battle_low', 0, self._music_obj)
                    self.play_music('battle_low')
        elif self.battle_state == BATTLE_MUSIC_STATE_LEAVE:
            self.battle_state = BATTLE_MUSIC_STATE_HUMAN
            if self.poison_level < battle_const.BATTLE_SOUND_STATE_HARD:
                self.play_music('stop')
            else:
                self.sound_mgr.set_rtpc('battle_hard', 0, self._music_obj)

    def enter_battle_state(self):
        from logic.gcommon.common_const import battle_const
        if self.poison_level >= battle_const.BATTLE_SOUND_STATE_LOW or self.first_call_mecha:
            if self.poison_level >= battle_const.BATTLE_SOUND_STATE_HARD:
                self.sound_mgr.set_rtpc('battle_hard', 20, self._music_obj)
                self.play_music('battle_hard')
            elif self.poison_level >= battle_const.BATTLE_SOUND_STATE_MEDIUM:
                self.sound_mgr.set_rtpc('battle_medium', 20, self._music_obj)
                self.play_music('battle_medium')
            elif self.poison_level >= battle_const.BATTLE_SOUND_STATE_LOW or self.first_call_mecha:
                self.play_music('battle_low')
                self.sound_mgr.set_rtpc('battle_low', 20, self._music_obj)
            self.battle_state = BATTLE_MUSIC_STATE_FIGHT
            self.reset_battle_state_downcount()

    def reset_battle_state_downcount(self):
        from logic.gcommon.common_const import battle_const
        if self.battle_state == BATTLE_MUSIC_STATE_LEAVE or self.battle_state == BATTLE_MUSIC_STATE_HUMAN:
            self.battle_state = BATTLE_MUSIC_STATE_FIND_ENEMY
            if self.poison_level >= battle_const.BATTLE_SOUND_STATE_HARD:
                self.play_music('battle_hard')
                self.sound_mgr.set_rtpc('battle_hard', 10, self._music_obj)
            elif self.poison_level >= battle_const.BATTLE_SOUND_STATE_MEDIUM:
                self.play_music('battle_medium')
                self.sound_mgr.set_rtpc('battle_medium', 10, self._music_obj)
            elif self.poison_level >= battle_const.BATTLE_SOUND_STATE_LOW or self.first_call_mecha:
                self.play_music('battle_low')
                self.sound_mgr.set_rtpc('battle_low', 10, self._music_obj)
        if self.battle_state >= BATTLE_MUSIC_STATE_FIND_ENEMY:
            if self.battle_state_delay_exec_id:
                game3d.cancel_delay_exec(self.battle_state_delay_exec_id)
            self.battle_state_delay_exec_id = game3d.delay_exec(12000, self.exit_battle_state)

    def exit_battle_state(self):
        from logic.gcommon.common_const import battle_const
        self.battle_state_delay_exec_id = None
        if self.mecha:
            self.battle_state = BATTLE_MUSIC_STATE_LEAVE
            if global_data.player and global_data.player.logic:
                global_data.player.logic.send_event('E_GUIDE_MECHA_STATE_LEAVE')
        else:
            self.battle_state = BATTLE_MUSIC_STATE_HUMAN
        if self.poison_level >= battle_const.BATTLE_SOUND_STATE_HARD:
            self.play_music('battle_hard')
            self.sound_mgr.set_rtpc('battle_hard', 0, self._music_obj)
        elif self.poison_level >= battle_const.BATTLE_SOUND_STATE_MEDIUM:
            if self.battle_state == BATTLE_MUSIC_STATE_LEAVE:
                self.play_music('battle_medium')
                self.sound_mgr.set_rtpc('battle_medium', 0, self._music_obj)
            else:
                self.play_music('stop')
        elif self.poison_level >= battle_const.BATTLE_SOUND_STATE_LOW or self.first_call_mecha:
            if self.battle_state == BATTLE_MUSIC_STATE_LEAVE:
                self.play_music('battle_low')
                self.sound_mgr.set_rtpc('battle_low', 0, self._music_obj)
            else:
                self.play_music('stop')
        return

    def on_summon_mecha(self, mecha_id):
        if self.poison_level < battle_const.BATTLE_SOUND_STATE_LOW:
            music_name = 'mecha_board_' + str(mecha_id)
            self.play_music(music_name)
            if global_data.game_mode.is_mode_type(game_mode_const.TDM_BattleBGM):

                def callback():
                    self.play_music(self._cur_death_music)

                game3d.delay_exec(8000, callback)

    @execute_by_mode(True, game_mode_const.TDM_BattleBGM)
    def on_battle_timestamp(self, timestamp):
        revive_time = timestamp - tutil.get_server_time()
        if revive_time < 0:
            return
        if revive_time < DEATH_MODE_CHANGE_MUSIC_TIME:
            self.play_music('deathmatch_2')
            self._cur_death_music = 'deathmatch_2'
        else:
            self.play_music('deathmatch_1')
            self._cur_death_music = 'deathmatch_1'
            interval = revive_time - DEATH_MODE_CHANGE_MUSIC_TIME
            if self.delay_timer:
                global_data.game_mgr.unregister_logic_timer(self.delay_timer)

            def callback():
                self.play_music('deathmatch_2')
                self._cur_death_music = 'deathmatch_2'

            self.delay_timer = global_data.game_mgr.register_logic_timer(callback, interval=interval, times=1, mode=timer.CLOCK)

    def resume_bg_sound(self):
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            self.set_poison_level(self.poison_level)
        else:
            self.play_music(self._cur_death_music)

    def play_music(self, music_name):
        self.sound_mgr.play_music(music_name)
        music_enable = False if music_name == 'stop' else True
        if self.is_bg_music_enable != music_enable:
            self.is_bg_music_enable = music_enable
            global_data.emgr.battle_music_enable.emit(self.is_bg_music_enable)

    def on_pve_fight_state_changed(self, state, is_boss=False):
        if not self.pve_music_res:
            from logic.gcommon.common_const.pve_const import DEFAULT_PVE_MUSIC_RES
            self.pve_music_res = DEFAULT_PVE_MUSIC_RES
        if state:
            if is_boss and len(self.pve_music_res) > 2:
                global_data.sound_mgr.play_music(self.pve_music_res[2], 'pve')
            else:
                global_data.sound_mgr.play_music(self.pve_music_res[1], 'pve')
        else:
            global_data.sound_mgr.play_music(self.pve_music_res[0], 'pve')