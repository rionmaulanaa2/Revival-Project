# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8032RunUI.py
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
import time
import game3d
ASSOCIATE_UI_LIST = [
 'FrontSightUI']
from common.const import uiconst
MAX_DASH_ENERGY_PERCENT = 88
MIN_DASH_ENERGY_PERCENT = 62
ENERGY_PERCENT_GAP = MAX_DASH_ENERGY_PERCENT - MIN_DASH_ENERGY_PERCENT
MIN_SHOW_UI_PROG = 10

class Mecha8032RunUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8032_sub'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'layer_drive.OnDrag': 'on_drag_drive_layer',
       'layer_drive.OnBegin': 'on_begin_drive_layer',
       'layer_drive.OnEnd': 'on_end_drive_layer'
       }
    IS_FULLSCREEN = True

    def on_init_panel(self):
        self.panel.nd_jet.setVisible(False)
        self.panel.nd_drive.setVisible(False)
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.panel.RecordAnimationNodeState('ready_loop')
        self.btn_start_pos = self.panel.btn_speed.getPosition()
        self.init_parameters()
        self.hide_main_ui(ASSOCIATE_UI_LIST)

    def on_finalize_panel(self):
        self.unbind_ui_event(self.player)
        self.show_main_ui()
        self.player = None
        if self._timer_id is not None:
            global_data.game_mgr.unregister_logic_timer(self._timer_id)
            self._timer_id = None
        return

    def init_parameters(self):
        self.player = None
        self.mecha = None
        self._timer_id = None
        self._is_running = False
        self._is_run_ui_showed = False
        self._is_sprint_ui_showed = False
        self._drag_callback = None
        self.cur_start_time = 0.0
        self.run_start_time = 0.0
        self.run_to_sprint_time = 0.0
        self.cur_speed = 1.0
        self.last_drag_pos = None
        emgr = global_data.emgr
        if global_data.cam_lplayer:
            self.on_player_setted(global_data.cam_lplayer)
        emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state
           }
        emgr.bind_events(econf)
        return

    def on_cam_lplayer_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.player = player
        self.on_camera_switch_to_state(global_data.game_mgr.scene.get_com('PartCamera').get_cur_camera_state_type())

    def on_mecha_setted(self, mecha):
        if self.mecha:
            self.unbind_ui_event(self.player)
        if mecha:
            self.mecha = mecha
            regist_func = mecha.regist_event
            regist_func('E_UPDATE_RUNSTATE_UI', self.update_runstate)
            (regist_func('E_UPDATE_SPRINT_UI', self.update_drag_drive_layer),)
            regist_func('E_UPDATE_SPRINT_DASH_UI', self.update_sprint_dash_state)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_UPDATE_RUNSTATE_UI', self.update_runstate)
            unregist_func('E_UPDATE_SPRINT_UI', self.update_drag_drive_layer)
            unregist_func('E_UPDATE_SPRINT_DASH_UI', self.update_sprint_dash_state)
        self.mecha = None
        return

    def update_runstate(self, state, cur_time, left_time, speed=1.0):
        if state:
            self._show_run_progress(cur_time, left_time, speed)
        else:
            self._close_run_progress(cur_time, left_time, speed)

    def update_sprint_dash_state(self, state):
        self.panel.lab_tips.setVisible(state)

    def on_camera_switch_to_state(self, state, *args):
        from data.camera_state_const import OBSERVE_FREE_MODE
        self.cur_camera_state_type = state
        if self.cur_camera_state_type != OBSERVE_FREE_MODE:
            self.add_show_count('observe')
        else:
            self.add_hide_count('observe')

    def _show_run_progress(self, cur_time, left_time, speed=1.0):
        self.run_to_sprint_time = left_time
        self.run_start_time = time.time()
        self.cur_start_time = cur_time
        self.cur_speed = speed
        self._is_running = True
        if self._timer_id is None:
            self._is_run_ui_showed = False
            self._timer_id = global_data.game_mgr.register_logic_timer(self._update_dash_progress, interval=0.03, times=-1, mode=2)
        return

    def _close_run_progress(self, cur_time, left_time, speed=1.0):
        if not self._is_running:
            return
        else:
            self.run_to_sprint_time = left_time
            self.run_start_time = time.time()
            self.cur_start_time = cur_time
            self.cur_speed = speed
            if self._timer_id is None:
                self._timer_id = global_data.game_mgr.register_logic_timer(self._update_dash_progress, interval=0.03, times=-1, mode=2)
            return

    def _enter_sprint(self):
        self.panel.nd_jet.setVisible(True)
        self.panel.PlayAnimation('ready_loop')
        self.panel.prog_jet.setPercentage(100)

    def _exit_sprint(self):
        self.panel.nd_jet.setVisible(False)
        self.panel.StopAnimation('ready_loop')
        self.panel.RecoverAnimationNodeState('ready_loop')

    def _update_dash_progress(self):
        cur_left_time = (time.time() - self.run_start_time) * self.cur_speed + self.cur_start_time
        if cur_left_time >= self.run_to_sprint_time or cur_left_time < 0.0:
            self.panel and self.panel.isValid() and self.panel.nd_jet.setVisible(False)
            if self._timer_id is not None:
                global_data.game_mgr.unregister_logic_timer(self._timer_id)
                self._timer_id = None
                self._is_running = False
            return
        else:
            if self.panel is not None:
                prog = cur_left_time / self.run_to_sprint_time * 100.0
                if prog > MIN_SHOW_UI_PROG and not self._is_run_ui_showed:
                    self._is_run_ui_showed = True
                    self.panel.nd_jet.setVisible(True)
                self.panel.prog_jet.setPercentage(prog)
            return

    def update_drag_drive_layer(self, state, drag_cb=None):
        if state:
            self._enter_sprint()
        else:
            self._exit_sprint()
        if global_data.is_pc_mode:
            self.panel.nd_pc.setVisible(state)
        else:
            self._is_sprint_ui_showed = state
            self.panel.nd_drive.setVisible(state)
            self.panel.layer_drive.SetSwallowTouch(not self.mecha.sd.ref_drag_state)
            if not state:
                self.panel.layer_drive.SetSwallowTouch(False)
            self.last_drag_pos = None
            self.btn_start_pos = self.panel.btn_speed_start.getPosition()
        self._drag_callback = drag_cb
        self._recover_btn_speed()
        if self._timer_id is not None:
            global_data.game_mgr.unregister_logic_timer(self._timer_id)
            self._timer_id = None
        return

    def on_drag_drive_layer(self, layer, touch):
        if not self._is_sprint_ui_showed:
            return
        if not self.last_drag_pos:
            self.last_drag_pos = touch.getLocation()
        cur_wpos = touch.getLocation()
        cur_lpos = self.panel.btn_speed.getParent().convertToNodeSpace(cur_wpos)
        start_lpos = self.panel.btn_speed.getParent().convertToNodeSpace(self.last_drag_pos)
        y_delta = cur_lpos.y - start_lpos.y
        new_y = self.btn_start_pos.y + y_delta
        pos = self.panel.layer_valid.getPosition()
        sz = self.panel.layer_valid.getContentSize()
        max_y = self.panel.btn_speed_start.getPosition().y
        min_y = pos.y - sz.height * 0.5
        new_y = min(max(new_y, min_y), max_y)
        self.btn_start_pos.y = new_y
        self.panel.btn_speed.SetPosition(self.panel.btn_speed.getPosition().x, new_y)
        cur_btn_pos = self.panel.btn_speed.getParent().convertToWorldSpace(self.panel.btn_speed.getPosition())
        if self.panel.nd_speed_lock.IsPointIn(cur_btn_pos):
            if self._drag_callback:
                self._drag_callback()
        self.last_drag_pos = cur_wpos

    def on_end_drive_layer(self, layer, touch):
        if self.mecha and self.mecha.sd:
            self.mecha.sd.ref_drag_state = False
        if not self._is_sprint_ui_showed:
            return
        else:

            def cb():
                if self.panel and self.panel.layer_drive and self.panel.layer_drive:
                    self.panel.layer_drive.SetSwallowTouch(True)

            game3d.delay_exec(0.1, cb)
            self._recover_btn_speed()
            self.btn_start_pos = self.panel.btn_speed_start.getPosition()
            self.last_drag_pos = None
            return

    def on_begin_drive_layer(self, layer, touch, is_mock=False):
        if self.mecha and self.mecha.sd:
            self.mecha.sd.ref_drag_state = True
        if not self._is_sprint_ui_showed:
            return
        self.panel.btn_speed.SetSelect(True)
        self.panel.speed_lock.setVisible(False)
        if not self.panel.btn_speed.IsPointIn(touch.getLocation()):
            self.panel.btn_speed.setPosition(self.panel.btn_speed_start.getPosition())
        self.btn_start_pos = self.panel.btn_speed_start.getPosition()

    def _recover_btn_speed(self):
        old_x, _ = self.panel.btn_speed.GetPosition()
        wpos = self.panel.img_speed_bar.ConvertToWorldSpacePercentage(0, 100)
        lpos = self.panel.btn_speed.getParent().convertToNodeSpace(wpos)
        self.panel.btn_speed.SetPosition(old_x, lpos.y - 17)
        self.panel.btn_speed.SetSelect(True)
        self.panel.img_lock_hint.setVisible(False)
        self.panel.speed_lock.setVisible(True)