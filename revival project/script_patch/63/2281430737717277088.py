# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CCloneMode.py
from __future__ import absolute_import
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from mobile.common.EntityManager import EntityManager

class CCloneMode(CDeathMode):

    def __init__(self, map_id):
        super(CCloneMode, self).__init__(map_id)

    def process_event(self, is_bind):
        super(CCloneMode, self).process_event(is_bind)
        emgr = global_data.emgr
        econf = {'clone_mecha_destroyed': self.on_mecha_destroyed,
           'on_observer_global_join_mecha_start': self.on_observer_join_mecha_start,
           'on_observer_global_leave_mecha_start': self.on_observer_leave_mecha_start,
           'on_observer_global_killer_camera': self.on_observer_killer_camera,
           'on_observer_global_join_mecha': self.on_observer_join_mecha
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy_ui(self):
        super(CCloneMode, self).destroy_ui()
        global_data.ui_mgr.close_ui('CloneTopScoreUI')

    def create_death_ui(self):
        super(CCloneMode, self).create_death_ui()
        global_data.ui_mgr.close_ui('DeathTopScoreUI')

    def is_need_weapon_ui(self):
        return False

    def on_mecha_destroyed(self, soul_id, killer_info, revive_time):
        self.on_target_defeated(revive_time, killer_id=None, kill_info=killer_info)
        return

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
        global_data.ui_mgr.close_ui('DeathPlayBackUI')

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

    def _show_top_score_ui_in_ready(self):
        global_data.ui_mgr.show_ui('CloneTopScoreUI', 'logic.comsys.battle.Clone')

    def _show_top_score_ui_after_ready(self):
        global_data.ui_mgr.close_ui('CloneTopScoreUI')
        global_data.ui_mgr.show_ui('CloneTopScoreUI', 'logic.comsys.battle.Clone')