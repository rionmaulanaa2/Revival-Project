# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/Mecha8033CarUI.py
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
from logic.gcommon.common_const.collision_const import GROUP_STATIC_SHOOTUNIT, WATER_GROUP, GROUP_CHARACTER_INCLUDE
from logic.gcommon.common_const.skill_const import SKILL_8033_SCAN
from mobile.common.EntityManager import EntityManager
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.cdata import mecha_status_config
from common.utils.cocos_utils import ccp
from common.utils.timer import CLOCK
import time
import math
import math3d
import collision
from common.const import uiconst
ASSOCIATE_UI_LIST = [
 'FrontSightUI']
RADAR_RANGE = 300
MAX_DASH_ENERGY_PERCENT = 88
MIN_DASH_ENERGY_PERCENT = 62
ENERGY_PERCENT_GAP = MAX_DASH_ENERGY_PERCENT - MIN_DASH_ENERGY_PERCENT

class Mecha8033CarUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_hit_mech8033_car'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'temp_map.btn_cancel.OnClick': 'on_btn_cancel',
       'temp_map.btn_confirm.OnClick': 'on_btn_confirm',
       'temp_map.nd_touch.OnClick': 'on_btn_choose_pos'
       }
    IS_FULLSCREEN = True

    def on_init_panel(self):
        self.panel.nd_jet.setVisible(False)
        self.panel.temp_map.setVisible(False)
        self.panel.temp_map.frame_target.setVisible(False)
        self.panel.temp_map.btn_confirm.setVisible(False)
        self.panel.temp_map.btn_cancel.setVisible(False)
        self.panel.RecordAnimationNodeState('prog_full')
        self.panel.temp_map.RecordAnimationNodeState('guide')
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.init_parameters()
        self.hide_main_ui(ASSOCIATE_UI_LIST)
        self.scan_enemy_8033()
        self.update_radar_layer(False)

    def clear_radar_pos(self):
        nd = self.panel.temp_map.frame_target
        nd.setVisible(False)
        self.choose_radar_pos = None
        return

    def on_btn_cancel(self, *args):
        if not self.mecha:
            return
        self.mecha.send_event('E_MECHA_8033_RADAR_FIRE')
        self.clear_radar_pos()

    def on_btn_confirm(self, *args):
        if not self.mecha:
            return
        if not self.choose_radar_pos:
            return
        self.mecha.send_event('E_MECHA_8033_RADAR_FIRE', self.choose_radar_pos)
        self.clear_radar_pos()

    def on_btn_choose_pos(self, btn, touch):
        if not self.mecha:
            return
        nd = self.panel.temp_map.frame_target
        location = touch.getLocation()
        location = self.panel.temp_map.nd_touch.convertToNodeSpace(location)
        w, h = self.panel.temp_map.nd_touch.GetContentSize()
        pos_rate = RADAR_RANGE / (w * 0.5)
        center_pos = ccp(w * 0.5, h * 0.5)
        cur_pos = self.mecha.ev_g_position()
        choose_pos = math3d.vector(cur_pos.x + (location.x - center_pos.x) * pos_rate * NEOX_UNIT_SCALE, cur_pos.y, cur_pos.z + (location.y - center_pos.y) * pos_rate * NEOX_UNIT_SCALE)
        center_pos.subtract(location)
        if center_pos.length() < w * 0.5:
            nd.setPosition(location)
            nd.setVisible(True)
            self.choose_radar_pos = choose_pos
            global_data.achi_mgr.set_cur_user_archive_data('Mecha8033CarUI_END', True)
            self.panel.temp_map.nd_guide.setVisible(False)
            self.panel.temp_map.StopAnimation('guide')
            self.panel.temp_map.RecoverAnimationNodeState('guide')
            self.mecha.send_event('E_MECHA_8033_RADAR_FIRE', self.choose_radar_pos)
            self.clear_radar_pos()

    def on_finalize_panel(self):
        self.unbind_ui_event(self.player)
        self.show_main_ui()
        self.player = None
        if self.my_locate_timer:
            global_data.game_mgr.get_logic_timer().unregister(self.my_locate_timer)
        self.my_locate_timer = None
        self.clear_timer()
        return

    def init_parameters(self):
        self._timer_id = None
        self.player = None
        self.mecha = None
        self._drag_callback = None
        self.enemy_locate = []
        self.enemy_locate_timer = None
        self.my_locate_timer = None
        self.choose_radar_pos = None
        self.energy_percent = 0.01
        emgr = global_data.emgr
        if global_data.cam_lplayer:
            self.on_player_setted(global_data.cam_lplayer)
        emgr.scene_camera_player_setted_event += self.on_cam_lplayer_setted
        econf = {'camera_switch_to_state_event': self.on_camera_switch_to_state,
           'mecha_8033_scan_info': self.scan_enemy_8033
           }
        emgr.bind_events(econf)
        return

    def get_scan_infos(self):
        scn = global_data.game_mgr.scene
        if scn:
            part_map = scn.get_com('PartMap')
            if part_map:
                return part_map.get_mecha_8033_scan_enemy()
        return []

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
            regist_func('E_UPDATE_RADAR_UI', self.update_radar_layer)
            regist_func('E_ENERGY_CHANGE', self.on_energy_change)
            regist_func('E_SHOW_BUFF_PROGRESS', self._show_dash_progress)
            regist_func('E_CLOSE_BUFF_PROGRESS', self._clsoe_dash_progress)
            self.on_energy_change(SKILL_8033_SCAN, self.mecha.ev_g_energy(SKILL_8033_SCAN))

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
        if self.mecha and self.mecha.is_valid():
            mecha = self.mecha
            unregist_func = mecha.unregist_event
            unregist_func('E_UPDATE_RADAR_UI', self.update_radar_layer)
            unregist_func('E_ENERGY_CHANGE', self.on_energy_change)
            unregist_func('E_SHOW_BUFF_PROGRESS', self._show_dash_progress)
            unregist_func('E_CLOSE_BUFF_PROGRESS', self._clsoe_dash_progress)
        self.mecha = None
        return

    def clear_timer(self):
        if self._timer_id is not None:
            global_data.game_mgr.unregister_logic_timer(self._timer_id)
        self._timer_id = None
        return

    def _clsoe_dash_progress(self):
        self.panel.nd_jet.setVisible(False)
        self.clear_timer()

    def _show_dash_progress(self, buff_id, data, left_time):
        from logic.gcommon.common_const.buff_const import BUFF_ID_8033_CAR_DASH
        if buff_id != BUFF_ID_8033_CAR_DASH:
            return
        if buff_id:
            conf = confmgr.get('c_buff_data', str(buff_id))
            self._max_buff_duration = conf.get('MaxDuration', 3)
        else:
            self._max_buff_duration = left_time
        self.dash_full_time = left_time
        self.dash_start_time = time.time()
        self.panel.nd_jet.setVisible(True)
        self.clear_timer()
        self._timer_id = global_data.game_mgr.register_logic_timer(self._update_dash_progress, interval=0.03, times=-1, mode=CLOCK)

    def _update_dash_progress(self):
        cur_left_time = self.dash_full_time - (time.time() - self.dash_start_time)
        if cur_left_time <= 0:
            cur_left_time = 0
        if self.panel is not None:
            self.panel.prog_jet.setPercentage(MIN_DASH_ENERGY_PERCENT + ENERGY_PERCENT_GAP * cur_left_time / self._max_buff_duration)
        return

    def on_energy_change(self, key, percent):
        if key == SKILL_8033_SCAN:
            if self.energy_percent == percent:
                return
            self.energy_percent = percent
            self.panel.nd_prog.bar_prog.prog.SetPercent(percent * 100)
            if percent >= 1.0:
                self.panel.PlayAnimation('prog_full')
                global_data.sound_mgr.play_sound_2d('m_8033_transform_full_1p')
            else:
                self.panel.StopAnimation('prog_full')
                self.panel.RecoverAnimationNodeState('prog_full')

    def on_camera_switch_to_state(self, state, *args):
        from data.camera_state_const import OBSERVE_FREE_MODE
        self.cur_camera_state_type = state
        if self.cur_camera_state_type != OBSERVE_FREE_MODE:
            self.add_show_count('observe')
        else:
            self.add_hide_count('observe')

    def _enter_sprint(self):
        self.panel.PlayAnimation('ready_loop')

    def _exit_sprint(self):
        self.panel.StopAnimation('ready_loop')
        self.panel.RecoverAnimationNodeState('ready_loop')

    def update_radar_layer(self, state):
        self.panel.temp_map.setVisible(state)
        show_guide = global_data.achi_mgr.get_cur_user_archive_data('Mecha8033CarUI_END', False)
        self.panel.temp_map.nd_guide.setVisible(not show_guide)
        if not show_guide:
            self.panel.temp_map.PlayAnimation('guide')
        if state:
            global_data.mouse_mgr and global_data.mouse_mgr.add_cursor_show_count('8033_radar')
            global_data.emgr.enable_camera_yaw.emit(False)
            self.clear_all_enemy_locate()
            self.update_my_locate()
        else:
            global_data.mouse_mgr and global_data.mouse_mgr.add_cursor_hide_count('8033_radar')
            global_data.emgr.enable_camera_yaw.emit(True)
            self.clear_radar_pos()
        ui = global_data.ui_mgr.get_ui('MechaControlMain')
        if ui:
            if state:
                ui.add_hide_count('mecha_8033_radar')
                ui.all_actions_cancel()
            else:
                ui.add_show_count('mecha_8033_radar')

    def clear_all_enemy_locate(self):
        for nd in self.enemy_locate:
            nd.Destroy()

        self.enemy_locate = []

    def set_forward(self, dir):
        if not dir:
            return
        nd_touch = self.panel.temp_map.nd_touch
        nd = self.panel.temp_map.icon_self
        cc_dir = ccp(dir.x, dir.z)
        degree = cc_dir.getAngle(ccp(0, 1)) * 180 / math.pi
        nd_touch.setRotation(-degree)
        nd.setRotation(degree)

    def scan_enemy_8033(self):
        pos_infos = self.get_scan_infos()
        self.clear_all_enemy_locate()
        if not pos_infos:
            return
        if not self.mecha:
            return
        nd_touch = self.panel.temp_map.nd_touch
        nd_touch.setRotation(0)
        cur_pos = self.mecha.ev_g_position()
        w, h = nd_touch.GetContentSize()
        pos_rate = w * 0.5 / RADAR_RANGE
        for pos, is_hit in pos_infos:
            nd = global_data.uisystem.load_template_create('map/ccb_enemy_locate')
            nd_touch.AddChild('', nd)
            nd.SetPosition(w * 0.5 + (pos.x - cur_pos.x) / NEOX_UNIT_SCALE * pos_rate, h * 0.5 + (pos.z - cur_pos.z) / NEOX_UNIT_SCALE * pos_rate)
            if not is_hit:
                nd.icon_enemy.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/mech_attack/mech_8033/map/icon_mech_8033_enemy2.png')
            else:
                nd.icon_enemy.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/mech_attack/mech_8033/map/icon_mech_8033_enemy.png')
            self.enemy_locate.append(nd)

        self.update_my_locate()

    def update_my_locate(self):
        if not self.mecha:
            return
        scn = global_data.game_mgr.scene
        if not scn:
            return
        cam = scn.active_camera
        if not cam:
            return
        self.set_forward(cam.world_transformation.forward)