# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CGooseBearMode.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import battle_const

class CGooseBearMode(CDeathMode):
    FORBIDDEN_ACTIONS = ('action1', 'action2', 'action3', 'action7', 'action8')

    def __init__(self, map_id):
        super(CGooseBearMode, self).__init__(map_id)
        self.welcome_ui_showed = False

    def on_finalize(self):
        super(CGooseBearMode, self).on_finalize()
        global_data.gravity_sur_battle_mgr.finalize()

    def init_death_data_mgr(self):
        super(CGooseBearMode, self).init_death_data_mgr()
        from logic.comsys.battle.Gravity.GravitySurvivalBattleMgr import GravitySurvivalBattleMgr
        GravitySurvivalBattleMgr()

    def process_event(self, is_bind):
        super(CGooseBearMode, self).process_event(is_bind)
        emgr = global_data.emgr
        econf = {'mecha_death_mecha_destroyed': self.on_mecha_destroyed,
           'mecha_death_revive': self.on_mecha_revive,
           'on_observer_global_join_mecha_start': self.on_observer_join_mecha_start,
           'on_observer_global_leave_mecha_start': self.on_observer_leave_mecha_start,
           'on_observer_global_killer_camera': self.on_observer_killer_camera,
           'on_observer_global_join_mecha': self.on_observer_join_mecha,
           'death_begin_count_down_over': self._create_welcome_ui,
           'mecha_control_main_ui_event': self._forbid_main_weapon
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _forbid_main_weapon(self):
        ui = global_data.ui_mgr.get_ui('MechaControlMain')
        if not ui:
            return
        for action in self.FORBIDDEN_ACTIONS:
            ui.on_set_action_forbidden(action, True)

    def _create_welcome_ui(self):
        if self.welcome_ui_showed:
            return
        tip_type = battle_const.GOOSEBEAR_GAME_START_TIP
        text = get_text_by_id(17367)
        message = {'i_type': tip_type,'content_txt': text,'in_anim': 'break','out_anim': 'break_out'}
        global_data.emgr.show_battle_med_message.emit((message,), battle_const.MED_NODE_RECRUIT_COMMON_INFO)
        show_guide = global_data.achi_mgr.get_cur_user_archive_data('GooseBearHappyPushGuideUI_END', False)
        if not show_guide:
            guide_ui = global_data.ui_mgr.show_ui('GooseBearHappyPushGuideUI', 'logic.comsys.battle.GooseBearHappyPush')
            guide_ui and guide_ui.delay_show(5)
        self.welcome_ui_showed = True

    def destroy_ui(self):
        super(CGooseBearMode, self).destroy_ui()
        global_data.ui_mgr.close_ui('MechaDeathTopScoreUI')
        global_data.ui_mgr.close_ui('MechaDeathPlayBackUI')

    def create_death_ui(self):
        super(CGooseBearMode, self).create_death_ui()
        if global_data.battle:
            global_data.battle.init_rechoose_mecha_ui()

    def is_need_weapon_ui(self):
        return False

    def on_mecha_destroyed(self, soul_id, killer_info, revive_time):
        self.on_target_defeated(revive_time, killer_id=None, kill_info=killer_info)
        return

    def on_mecha_revive(self, *args):
        self.cam_enable(True)
        self.on_target_revive()

    def on_observer_join_mecha_start(self, *args, **kwargs):
        self.cam_enable(True)
        self.recover_death_cam()

    def on_observer_leave_mecha_start(self, *args, **kwargs):
        self.cam_enable(False)

    def on_observer_killer_camera(self, *args, **kwargs):
        self.cam_enable(False)

    def recover_death_cam(self):
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_RECOVER_KILLER_CAM')
            global_data.cam_lplayer.send_event('E_TO_THIRD_PERSON_CAMERA')
        global_data.ui_mgr.close_ui('MechaDeathPlayBackUI')

    def cam_enable(self, enable):
        if enable:
            global_data.emgr.camera_lock_enable_follow_event.emit(False)
            global_data.emgr.camera_enable_follow_event.emit(True)
        else:
            global_data.emgr.camera_lock_enable_follow_event.emit(False)
            global_data.emgr.camera_enable_follow_event.emit(False)
            global_data.emgr.camera_lock_enable_follow_event.emit(True)
        global_data.emgr.camera_added_trk_enable.emit(enable)
        global_data.emgr.switch_cam_state_enable_event.emit(enable)

    def on_observer_join_mecha(self, *args, **kargs):
        if global_data.cam_lplayer:
            mecha_entity_id = global_data.cam_lplayer.ev_g_ctrl_mecha()
            mecha_entity = EntityManager.getentity(mecha_entity_id)
            if mecha_entity and mecha_entity.logic:
                new_yaw = mecha_entity.logic.ev_g_yaw()
                global_data.emgr.fireEvent('camera_set_yaw_event', new_yaw)
                global_data.emgr.fireEvent('camera_set_pitch_event', 0)

    def on_target_defeated(self, revive_time, killer_id, kill_info):
        if self.game_over:
            return
        reply_data = kill_info.get('reply_data', {})
        ui = global_data.ui_mgr.show_ui('DeathBeginCountDown', 'logic.comsys.battle.Death')
        ui.on_delay_close(revive_time)
        ui = global_data.ui_mgr.show_ui('MechaDeathPlayBackUI', 'logic.comsys.battle.MechaDeath')
        ui.set_play_back_info(reply_data)
        ui.set_revive_time(revive_time)
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('S_ATTR_SET', 'death_mode_leave_base_firstly', True)

    def _on_apply_suicide_back_home(self):
        player = global_data.player
        if not player:
            return
        if player.is_battle_replaying() or player.is_in_global_spectate():
            return
        bat = player.get_battle()
        if not (bat and hasattr(bat, 'start_suicide')):
            return
        bat.start_suicide()

    def on_target_revive(self):
        super(CGooseBearMode, self).on_target_revive()
        global_data.ui_mgr.close_ui('MechaDeathPlayBackUI')

    def _show_top_score_ui_in_ready(self):
        global_data.ui_mgr.show_ui('MechaDeathTopScoreUI', 'logic.comsys.battle.MechaDeath')

    def _show_top_score_ui_after_ready(self):
        global_data.ui_mgr.close_ui('MechaDeathTopScoreUI')
        global_data.ui_mgr.show_ui('MechaDeathTopScoreUI', 'logic.comsys.battle.MechaDeath')