# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Occupy/OccupyProgressUI.py
from __future__ import absolute_import
import six
import six_ex
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT
from logic.comsys.battle.Occupy.OccupyData import PART_FIGHT, PART_MY_SIDE
from common.utils.cocos_utils import getScreenSize
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.platform.device_info import DeviceInfo
from logic.gcommon import time_utility as tutil
from common.utils.ui_utils import get_scale
from logic.gutils import screen_utils
import math3d
import cc
import math
OCCUPY_SIDE_PIC = {'progress': ['gui/ui_res_2/battle_contention/point/prog_white.png',
              'gui/ui_res_2/battle_contention/point/prog_blue.png',
              'gui/ui_res_2/battle_contention/point/prog_red.png',
              '',
              'gui/ui_res_2/battle_contention/point/prog_yellow.png'],
   'icon': [
          'gui/ui_res_2/battle_contention/point/icon_point_white.png',
          'gui/ui_res_2/battle_contention/point/icon_point_blue.png',
          'gui/ui_res_2/battle_contention/point/icon_point_red.png',
          'gui/ui_res_2/battle_contention/point/icon_lock.png',
          'gui/ui_res_2/battle_contention/point/icon_point_yellow.png'],
   'bg': [
        'gui/ui_res_2/battle_contention/point/pnl_white.png',
        'gui/ui_res_2/battle_contention/point/pnl_blue.png',
        'gui/ui_res_2/battle_contention/point/pnl_red.png',
        'gui/ui_res_2/battle_contention/point/pnl_lock.png',
        'gui/ui_res_2/battle_contention/point/pnl_yellow.png']
   }
SIDE_ANI = [
 'word_white', 'word_blue', 'word_red', 'lock', 'word_yellow']
SIDE_TXT_ID = [8214, 8215, 8217, 8213, 8216]

class OccupyLocateUI(object):

    def __init__(self, parent, part_id):
        self.parent = parent
        self.part_id = part_id
        self._nd = global_data.uisystem.load_template_create('battle_contention/battle_state')
        self._nd.setVisible(False)
        self._nd.temp_icon.img_light.setVisible(False)
        self._nd.nd_simple.locate.img_light.setVisible(False)
        self.init_parameters()
        self.on_tick()

    def init_parameters(self):
        self.timestamp = 0
        self.run_timer = None
        self.screen_size = getScreenSize()
        self.position = None
        self.control_side = None
        self.update_act = None
        device_info = DeviceInfo()
        self.is_can_full_screen = device_info.is_can_full_screen()
        self.screen_size = getScreenSize()
        self.screen_angle_limit = math.atan(self.screen_size.height / 2.0 / (self.screen_size.width / 2.0)) * 180 / math.pi
        self.scale_data = {'scale_90': (get_scale('90w'), get_scale('280w')),'scale_40': (
                      get_scale('40w'), get_scale('120w')),
           'scale_left': (
                        get_scale('90w'), get_scale('300w')),
           'scale_right': (
                         get_scale('90w'), get_scale('200w')),
           'scale_up': (
                      get_scale('90w'), get_scale('120w')),
           'scale_low': (
                       get_scale('90w'), get_scale('120w'))
           }
        return

    def on_finalize_panel(self):
        self.clear_run_timer()
        self._nd and self._nd.Destroy()
        self._nd = None
        return

    def change_side(self):
        self._nd.setVisible(True)
        self._nd.lab_name.SetString(SIDE_TXT_ID[self.control_side])
        self.refresh_nd(self._nd.temp_icon)
        self.refresh_nd(self._nd.nd_simple.locate)

    def refresh_nd(self, nd):
        node = nd.prog_name
        path = OCCUPY_SIDE_PIC['progress'][self.control_side]
        if path:
            node.setVisible(True)
            node.SetProgressTexture(path)
        else:
            node.setVisible(False)
        node = nd.img_arrow
        path = OCCUPY_SIDE_PIC['icon'][self.control_side]
        if path:
            node.setVisible(True)
            node.SetDisplayFrameByPath('', path)
        else:
            node.setVisible(False)
        node = nd.pnl_bg
        path = OCCUPY_SIDE_PIC['bg'][self.control_side]
        if path:
            node.setVisible(True)
            node.SetDisplayFrameByPath('', path)
        else:
            node.setVisible(False)

    def update_wrapper(self):
        if not global_data.death_battle_data:
            return
        else:
            data_obj = global_data.death_battle_data.part_data.get(self.part_id)
            if not data_obj:
                return
            data = data_obj.data
            control_side = data_obj.control_side
            if control_side is None:
                return
            if self.control_side != control_side:
                self._nd.PlayAnimation('show_change')
                self._nd.PlayAnimation(SIDE_ANI[control_side])
                is_fight = control_side == PART_FIGHT
                self._nd.nd_focus.setVisible(is_fight)
                self._nd.nd_simple.locate.img_light.setVisible(is_fight)
                self._nd.temp_icon.img_light.setVisible(is_fight)
                if is_fight:
                    self._nd.PlayAnimation('focus_yellow')
                    self._nd.nd_simple.locate.PlayAnimation('loop_seize')
                    self._nd.temp_icon.PlayAnimation('loop_seize')
                else:
                    self._nd.StopAnimation('focus_yellow')
                    self._nd.nd_simple.locate.StopAnimation('loop_seize')
                    self._nd.temp_icon.StopAnimation('loop_seize')
            self.control_side = control_side
            self.timestamp = data['timestamp']
            self.position = data['position']
            self.control_group_id = data['control_group_id']
            self.change_side()
            return

    def update_nd_pos(self):
        if not self.position:
            return
        cam = global_data.game_mgr.scene.active_camera
        if not cam:
            return
        now_stamp = tutil.get_server_time()
        left_time = self.timestamp - now_stamp
        if left_time > 0:
            self._nd.lab_time.setVisible(True)
            self._nd.lab_time.SetString('%02d:%02d' % (left_time / 60, left_time % 60))
        else:
            self._nd.lab_time.setVisible(False)
        x, y, z = self.position
        position = math3d.vector(x, y, z)
        is_in_screen, end_pos, angle = screen_utils.world_pos_to_screen_pos(self._nd, position, self.screen_size, self.screen_angle_limit, self.is_can_full_screen, self.scale_data)
        dist = cam.position - position
        dist = dist.length / NEOX_UNIT_SCALE
        max_dist = 1000
        scale = max(0.5, (max_dist - dist) * 1.0 / max_dist)
        self._nd.setScale(scale)
        self._nd.setPosition(end_pos)
        lplayer = global_data.cam_lplayer
        if lplayer:
            player_pos = lplayer.ev_g_position()
            dist = (player_pos - position).length
            self._nd.lab_distance.SetString('%dm' % (int(dist) / NEOX_UNIT_SCALE))
            self._nd.temp_icon.setVisible(is_in_screen)
            self._nd.nd_simple.setVisible(not is_in_screen)
            if not is_in_screen:
                self._nd.nd_simple.dir.setRotation(angle + 90)

    def on_tick(self):
        self.clear_run_timer()
        self.run_timer = global_data.game_mgr.get_logic_timer().register(func=self.update_nd_pos, interval=1)

    def clear_run_timer(self):
        self.run_timer and global_data.game_mgr.get_logic_timer().unregister(self.run_timer)
        self.run_timer = None
        return


class OccupyProgressUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.process_event(True)
        self.panel.setLocalZOrder(1)
        self.update_control_point()

    def on_finalize_panel(self):
        for locate_wrapper in six.itervalues(self.part_progress_ui):
            locate_wrapper.on_finalize_panel()

        self.part_progress_ui = {}
        self.process_event(False)

    def init_parameters(self):
        self.part_progress_ui = {}

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_control_point': self.update_control_point,
           'occupy_my_score_up': self.occupy_my_score_up
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_control_point(self):
        if not global_data.death_battle_data:
            return
        control_point_dict = global_data.death_battle_data.part_data
        new_controls = set(six_ex.keys(control_point_dict))
        cur_controls = set(six_ex.keys(self.part_progress_ui))
        del_controls = cur_controls - new_controls
        for part_id in del_controls:
            locate_wrapper = self.part_progress_ui[part_id]
            locate_wrapper and locate_wrapper.on_finalize_panel()
            del self.part_progress_ui[part_id]

        for part_id in six.iterkeys(control_point_dict):
            if part_id in self.part_progress_ui:
                locate_wrapper = self.part_progress_ui[part_id]
            else:
                locate_wrapper = OccupyLocateUI(self, part_id)
                self.panel.AddChild('', locate_wrapper._nd)
                if global_data.aim_transparent_mgr:
                    global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__, [locate_wrapper._nd])
                self.part_progress_ui[part_id] = locate_wrapper
            locate_wrapper.update_wrapper()

    def occupy_my_score_up(self, score):
        for locate_wrapper in six.itervalues(self.part_progress_ui):
            if locate_wrapper.control_side == PART_MY_SIDE:
                locate_wrapper._nd.lab_up_blue.SetString('+%d' % score)
                locate_wrapper._nd.PlayAnimation('up_blue')