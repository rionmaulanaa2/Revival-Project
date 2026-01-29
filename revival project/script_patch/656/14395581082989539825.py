# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaCockpitUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BG_ZORDER
import cc
from common.cfg import confmgr
import math
from common.const import uiconst
from logic.gutils.judge_utils import disable_execute_for_judge

class MechaCockpitUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/mech_dec_main'
    DLG_ZORDER = BG_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True

    def on_init_panel(self):
        self.orignal_pos_x, self.orignal_pos_y = self.panel.GetPosition()

    def on_finalize_panel(self):
        self.panel.stopAllActions()
        self._close_mecha_ui()
        if global_data.player and global_data.player.logic:
            unregist_func = global_data.player.logic.unregist_event
            unregist_func('E_SHOW_MECHA_UI', self._show_mecha_ui)
            unregist_func('E_CLOSE_MECHA_UI', self._close_mecha_ui)

    def on_resolution_changed(self):
        self.orignal_pos_x, self.orignal_pos_y = self.panel.GetPosition()

    @disable_execute_for_judge()
    def enter_screen(self):
        super(MechaCockpitUI, self).enter_screen()
        self.panel.PlayAnimation('show')
        self.init_events()
        self._show_mecha_ui()

    def leave_screen(self):
        super(MechaCockpitUI, self).leave_screen()
        self.on_finalize_panel()

    def init_events(self):
        if global_data.player and global_data.player.logic:
            regist_func = global_data.player.logic.regist_event
            regist_func('E_SHOW_MECHA_UI', self._show_mecha_ui)
            regist_func('E_CLOSE_MECHA_UI', self._close_mecha_ui)

    def _show_mecha_ui(self):
        self.is_show = True
        self.add_show_count(self.__class__.__name__)
        self._is_play_trk = False
        self._is_reseting_cockpit = False
        global_data.emgr.camera_play_added_trk_start += self._on_play_trk_start
        global_data.emgr.camera_trans_change += self._on_camera_trans_change
        global_data.emgr.camera_all_trk_play_end += self._on_all_trk_play_end
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.tick),
         cc.DelayTime.create(0.033)])))

    def _close_mecha_ui(self):
        self.is_show = False
        self.add_hide_count(self.__class__.__name__)
        self._is_play_trk = False
        self._is_reseting_cockpit = False
        global_data.emgr.camera_play_added_trk_start -= self._on_play_trk_start
        global_data.emgr.camera_trans_change -= self._on_camera_trans_change
        global_data.emgr.camera_all_trk_play_end -= self._on_all_trk_play_end

    def _on_play_trk_start(self, trk_tag):
        trk_conf = confmgr.get('camera_trk_sfx_conf', 'TrkConfig').get('Content').get(str(trk_tag), None)
        if not trk_conf:
            log_error("Can't find cam trk %s" % trk_tag)
            return
        else:
            self._is_play_trk = True
            self._is_reseting_cockpit = False
            self._last_cam_pos = self.scene.active_camera.world_position
            self._delay_cur_time = 0
            self._delay_follow_time = trk_conf.get('delay_follow_time', 0.5)
            self._translate_swing = trk_conf.get('translate_swing', 0.01)
            self._rotate_swing = trk_conf.get('rotate_swing', 1)
            self._sync_rotate = trk_conf.get('sync_rotate', 1)
            return

    def _on_all_trk_play_end(self):
        if not self._is_play_trk:
            return
        self._is_play_trk = False
        self._is_reseting_cockpit = True
        self._reset_time = 0.5
        self._reset_cur_time = 0
        self._per_fix_offset_caluated = False
        self._per_fix_offset_y = 0

    def _on_camera_trans_change(self, trans):
        if not self._is_play_trk or not self._sync_rotate:
            return
        cur_rotate3d = cc.Vec3(trans.rotation.pitch * 180 / math.pi, trans.rotation.yaw * 180 / math.pi, trans.rotation.roll * 180 / math.pi)
        self.panel.setRotation3D(cur_rotate3d)

    def _follow_cockpit_pos(self, delta):
        self._delay_cur_time += delta
        if self._delay_cur_time < self._delay_follow_time:
            cur_cam_pos = self.scene.active_camera.world_position
            offset_y = cur_cam_pos.y - self._last_cam_pos.y
            self._last_cam_pos = cur_cam_pos
            cur_pos_x, cur_pos_y = self.panel.GetPosition()
            max_offset_y = 20
            new_pos_y = cur_pos_y - offset_y
            if abs(new_pos_y - self.orignal_pos_y) > max_offset_y:
                if offset_y > 0:
                    new_pos_y = self.orignal_pos_y - max_offset_y
                else:
                    new_pos_y = self.orignal_pos_y + max_offset_y
            self.panel.setPosition(self.orignal_pos_x, new_pos_y)

    def _reset_cockpit_pos_gradually(self, delta):
        if not self._per_fix_offset_caluated:
            self._per_fix_offset_caluated = True
            cur_pos_x, cur_pos_y = self.panel.GetPosition()
            dis_pos_y = cur_pos_y - self.orignal_pos_y
            self._per_fix_offset_y = -dis_pos_y * (1 / self._reset_time)
        self._reset_cur_time += delta
        if self._reset_cur_time > self._reset_time:
            self._is_reseting_cockpit = False
            self._reset_cokpit_model_pos()
            return
        cur_pos_x, cur_pos_y = self.panel.GetPosition()
        new_pos_y = cur_pos_y + self._per_fix_offset_y * delta
        self.panel.setPosition(self.orignal_pos_x, new_pos_y)

    def _reset_cokpit_model_pos(self):
        self.panel.setPosition(self.orignal_pos_x, self.orignal_pos_y)
        self.panel.setRotation3D(cc.Vec3(0, 0, 0))

    def tick(self):
        if not self.is_show:
            return
        delta = 0.033
        if self._is_play_trk:
            self._follow_cockpit_pos(delta)
        elif self._is_reseting_cockpit:
            self._reset_cockpit_pos_gradually(delta)