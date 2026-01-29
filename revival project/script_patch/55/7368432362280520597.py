# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVERadarMapUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.timer import CLOCK
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.common_const.pve_const import PVE_BOX_TYPE_ENERGY, PVE_BOX_TYPE_BREAK
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.time_utility import get_server_time, get_delta_time_str
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from .PVEMechaRadarWidget import PVEMechaRadarWidget
import math3d
import math
import six

class PVERadarMapUI(MechaDistortHelper, BasePanel):
    PANEL_CONFIG_NAME = 'pve/i_pve_map'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    T_POINT = 1
    T_PIZZA = 2
    NEAR = 30 * NEOX_UNIT_SCALE
    MID = 100 * NEOX_UNIT_SCALE
    TICK_DUR = 0.033
    DUR_MAP = {1: 0.033,
       2: 0.066,
       3: 0.1
       }
    TICK_CNT = 10
    RADIUS = 45.7
    CENTER = 50
    HALF_PI = math.pi * 0.5
    TWO_PI = math.pi * 2
    SECTOR_OFFSET = math.pi / 8.0
    SECTOR_SIZE = math.pi / 4.0
    BOX_TEMPLATE = {PVE_BOX_TYPE_ENERGY: 'pve/i_pve_map_box',
       PVE_BOX_TYPE_BREAK: 'pve/i_pve_map_box'
       }
    SHOP_TEMPLATE = 'pve/i_pve_map_shop'

    def on_init_panel(self, *args, **kwargs):
        super(PVERadarMapUI, self).on_init_panel(*args, **kwargs)
        self.init_params()
        self.init_ui_nds()
        self.init_level_text()
        self.init_custom_com()
        self.process_events(True)

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_params(self):
        ret = global_data.player and global_data.player.get_setting(uoc.PVE_RADAR_MAP_TYPE)
        if ret is None:
            ret = True
        uoc.PVE_RADAR_MAP_TYPE_ENABLE = ret
        self.map_type = self.T_POINT if uoc.PVE_RADAR_MAP_TYPE_ENABLE else self.T_PIZZA
        self.target_set = {}
        self.locate_widgets = {}
        self.locate_timers = {}
        self.teammate_set = {}
        self.tick_timer = None
        self.target_monsters = []
        self.tick_dur = self.TICK_DUR
        self.cur_set = set()
        self.has_monster_sector_set = set()
        self.last_has_monster_sector_set = set()
        self.enable_mecha_radar = global_data.player.get_setting(uoc.PVE_MECHA_RADAR) if global_data.player else uoc.PVE_MECHA_RADAR_NONE
        self.near_vis = False
        self.mid_vis = 0
        self.far_vis = 0
        self.bcp_set = set()
        self.m_tick_cnt = 0
        return

    def init_ui_nds(self):
        self.nd_near = self.panel.img_near
        self.nd_mid = self.panel.nd_mid
        self.nd_far = self.panel.nd_far
        self.nd_mid.setVisible(False)
        self.nd_far.setVisible(False)
        self.panel.bar_info.setVisible(False)
        self._mecha_radar_widget = None
        if self.enable_mecha_radar:
            self._mecha_radar_widget = PVEMechaRadarWidget(self.panel)
            self._mecha_radar_widget.set_setting(self.enable_mecha_radar)

        @self.panel.btn_map.unique_callback()
        def OnClick(btn, touch, *args):
            ret = global_data.player.get_setting(uoc.PVE_RADAR_MAP_TYPE)
            if ret is None:
                ret = True
            if ret and self.map_type == self.T_POINT:
                global_data.player.write_setting(uoc.PVE_RADAR_MAP_TYPE, False, True)
                uoc.PVE_RADAR_MAP_TYPE_ENABLE = False
                self.set_map_type(self.T_PIZZA)
            elif not ret and self.map_type == self.T_PIZZA:
                global_data.player.write_setting(uoc.PVE_RADAR_MAP_TYPE, True, True)
                uoc.PVE_RADAR_MAP_TYPE_ENABLE = True
                self.set_map_type(self.T_POINT)
            return

        return

    def on_enter_level(self, *args):
        self.init_level_text()

    def init_level_text(self):
        level = global_data.battle.get_cur_pve_level()
        if level:
            self.panel.bar_info.lab_level.SetString('%s%s-%s' % (get_text_by_id(83504), level[0], level[1]))
            self.panel.bar_info.setVisible(True)
        else:
            self.panel.bar_info.setVisible(False)
        self.panel.bar_info.lab_time.setVisible(False)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_player_setted_event': self.on_player_setted,
           'scene_camera_target_setted_event': self.on_cam_lctarget_setted,
           'battle_switch_scene_event': self.clear_all,
           'pve_monster_init': self.on_monster_init,
           'pve_set_target_monsters': self.set_target_monsters,
           'pve_monster_destroy': self.on_monster_destroy,
           'pve_monster_die': self.on_monster_destroy,
           'pve_box_open_event': self.on_track_box,
           'pve_box_close_event': self.on_cancel_box,
           'pve_box_opened_event': self.on_cancel_box,
           'pve_shop_closed_event': self.on_cancel_shop,
           'pve_shop_opened_event': self.on_track_shop,
           'pve_update_end_time': self.on_update_end_time,
           'mecha_init_event': self.on_mecha_init,
           'mecha_crashed_event': self.on_mecha_crashed,
           'player_user_setting_changed_event': self.on_user_setting_changed,
           'pve_enter_level_event': self.on_enter_level
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.clear_all()
        self.init_params()
        self.process_events(False)
        if self.custom_ui_com:
            self.custom_ui_com.destroy()
            self.custom_ui_com = None
        if self._mecha_radar_widget:
            self._mecha_radar_widget.destroy()
            self._mecha_radar_widget = None
        super(PVERadarMapUI, self).on_finalize_panel()
        return

    def clear_all(self):
        self.reset_tick_timer()
        self.clear_all_locate()
        self.panel.StopTimerAction()

    def set_map_type(self, t):
        self.map_type = t

    def on_player_setted(self, *args):
        self.clear_all()
        for guide_id, guide_pos in six.iteritems(global_data.battle.guide_data):
            self.set_guide_pos(guide_id, guide_pos)

        if global_data.battle:
            size = global_data.battle.get_pve_player_size_mode()
            self.tick_dur = self.DUR_MAP.get(size, self.TICK_DUR)
        self.init_tick()
        self.init_end_time()

    def on_cam_lctarget_setted(self, *args):
        pass

    def on_user_setting_changed(self, key, val):
        if key == uoc.PVE_MECHA_RADAR:
            self.enable_mecha_radar = val
            if not self._mecha_radar_widget and val:
                self._mecha_radar_widget = PVEMechaRadarWidget(self.panel)
            elif self._mecha_radar_widget and not val:
                self._mecha_radar_widget.refresh_visible()
            if self._mecha_radar_widget:
                self._mecha_radar_widget.set_setting(self.enable_mecha_radar)

    def init_end_time(self):
        end_time = global_data.battle.get_storyline_end_time()
        self.on_update_end_time(end_time)

    def on_update_end_time(self, end_time):
        self.panel.StopTimerAction()

        def tick(pass_time):
            left_time = int(dur - pass_time)
            left_time = get_delta_time_str(left_time)[3:]
            self.panel.bar_info.lab_time.SetString('%s%s' % (get_text_by_id(81754), left_time))

        dur = end_time - get_server_time()
        self.panel.TimerAction(tick, dur, None, 1.0)
        self.panel.bar_info.lab_time.setVisible(True)
        return

    def set_guide_pos(self, g_id, pos):
        self.show_locate(g_id, pos)

    def clear_guide_pos(self, g_id):
        self.clear_locate(g_id)

    def show_locate(self, g_id, pos):
        self.init_guide_widget(g_id)
        widget = self.locate_widgets[g_id]
        widget.setVisible(True)
        pos = math3d.vector(*pos)
        pos.y = 0
        self.reset_locate_timer(g_id)
        self.locate_timers[g_id] = global_data.game_mgr.register_logic_timer(lambda g=g_id, p=pos: self.calc_nd_pos(g, p), self.TICK_DUR, None, -1, CLOCK)
        return

    def init_guide_widget(self, g_id):
        if g_id in self.locate_widgets:
            self.clear_locate(g_id)
        widget = global_data.uisystem.load_template_create('pve/i_pve_map_locate', self.panel.img_map)
        widget.setVisible(False)
        self.locate_widgets[g_id] = widget

    def clear_locate(self, g_id):
        widget = self.locate_widgets.get(g_id, None)
        if widget:
            widget.setVisible(False)
            widget.Destroy()
            self.locate_widgets[g_id] = None
            self.locate_widgets.pop(g_id)
        self.reset_locate_timer(g_id)
        return

    def clear_all_locate(self):
        for i in self.locate_widgets:
            widget = self.locate_widgets[i]
            if widget:
                widget.setVisible(False)

        self.locate_widgets = {}
        for i in self.locate_timers:
            timer = self.locate_timers[i]
            if timer:
                global_data.game_mgr.unregister_logic_timer(timer)

        self.locate_timers = {}

    def reset_locate_timer(self, g_id):
        timer = self.locate_timers.get(g_id, None)
        if timer:
            global_data.game_mgr.unregister_logic_timer(timer)
            self.locate_timers.pop(g_id)
        return

    def calc_nd_pos(self, g_id, pos):
        if not global_data.cam_lctarget:
            return
        if not global_data.cam_data:
            return
        center = global_data.cam_lctarget.ev_g_position()
        if not center:
            return
        dire = pos - center
        dire.y = 0
        dis = dire.length
        if dire.is_zero:
            dire = math3d.vector(0, 1, 0)
        dire.normalize()
        yaw_diff = global_data.cam_data.yaw - dire.yaw
        radian = yaw_diff + self.HALF_PI
        widget = self.locate_widgets[g_id]
        ratio = min(dis / self.MID, 1.0)
        x = ratio * math.cos(radian) * self.RADIUS + self.CENTER
        y = ratio * math.sin(radian) * self.RADIUS + self.CENTER
        widget.SetPosition(str(x) + '%', str(y) + '%')

    def on_track_box(self, unit, show_tip=False):
        eid = unit.id
        box_type = unit.ev_g_pve_box_type()
        self.init_box_widget(eid, box_type)
        widget = self.locate_widgets[eid]
        widget.setVisible(True)
        model = unit.ev_g_model()
        if not model:
            return
        else:
            pos = math3d.vector(model.position)
            pos.y = 0
            self.reset_locate_timer(eid)
            self.locate_timers[eid] = global_data.game_mgr.register_logic_timer(lambda g=eid, p=pos: self.calc_nd_pos(g, p), self.TICK_DUR, None, -1, CLOCK)
            return

    def on_cancel_box(self, unit):
        eid = unit.id
        self.clear_locate(eid)

    def init_box_widget(self, eid, box_type):
        if eid in self.locate_widgets:
            self.clear_locate(eid)
        widget = global_data.uisystem.load_template_create(self.BOX_TEMPLATE[box_type], self.panel.img_map)
        widget.setVisible(False)
        self.locate_widgets[eid] = widget

    def on_track_shop(self, unit, show_tip=False):
        eid = unit.id
        self.init_shop_widget(eid)
        widget = self.locate_widgets[eid]
        widget.setVisible(True)
        model = unit.ev_g_model()
        if not model:
            return
        else:
            pos = math3d.vector(model.position)
            pos.y = 0
            self.reset_locate_timer(eid)
            self.locate_timers[eid] = global_data.game_mgr.register_logic_timer(lambda g=eid, p=pos: self.calc_nd_pos(g, p), self.TICK_DUR, None, -1, CLOCK)
            return

    def on_cancel_shop(self, unit):
        eid = unit.id
        self.clear_locate(eid)

    def init_shop_widget(self, eid):
        if eid in self.locate_widgets:
            self.clear_locate(eid)
        widget = global_data.uisystem.load_template_create(self.SHOP_TEMPLATE, self.panel.img_map)
        widget.setVisible(False)
        self.locate_widgets[eid] = widget

    def on_monster_init(self, unit):
        self.target_set[unit.id] = unit
        if unit.id in self.target_monsters:
            self.set_monster_track(unit, is_target=True)
        else:
            self.set_monster_track(unit)

    def on_monster_destroy(self, unit):
        if unit.id in self.target_set:
            self.target_set.pop(unit.id)
        if unit.id in self.cur_set:
            self.cur_set.remove(unit.id)
        if unit.id in self.bcp_set:
            self.bcp_set.remove(unit.id)
        if unit.id in self.target_monsters:
            self.cancel_monster_track(unit)
            self.target_monsters.remove(unit.id)
        else:
            self.cancel_monster_track(unit)

    def set_target_monsters(self, target_list):
        self.target_monsters = target_list
        reset_eids = []
        for eid in self.locate_widgets:
            if eid in self.target_monsters and eid in self.target_set:
                reset_eids.append(eid)

        if reset_eids:
            for eid in reset_eids:
                unit = self.target_set.get(eid)
                self.set_monster_track(unit, True)

    def set_monster_track(self, unit, is_target=False):
        eid = unit.id
        if is_target:
            if eid not in self.locate_widgets:
                self.init_guide_widget(eid)
        else:
            self.init_common_widget(eid)
        self.reset_locate_timer(eid)
        self.locate_timers[eid] = global_data.game_mgr.register_logic_timer(lambda u=unit: self.calc_monster_nd_pos(unit), self.tick_dur, None, -1, CLOCK)
        return

    def cancel_monster_track(self, unit):
        eid = unit.id
        self.clear_locate(eid)

    def calc_monster_nd_pos(self, unit):
        if not global_data.cam_lctarget:
            return
        else:
            if not global_data.cam_data:
                return
            eid = unit.id
            widget = self.locate_widgets.get(eid, None)
            if not widget:
                self.clear_locate(eid)
                return
            if self.map_type == self.T_PIZZA:
                widget.setVisible(False)
                return
            if eid not in self.target_monsters:
                if eid in self.bcp_set:
                    return
                if self.m_tick_cnt >= self.TICK_CNT:
                    return
                self.m_tick_cnt += 1
                self.bcp_set.add(eid)
            widget.setVisible(True)
            center = global_data.cam_lctarget.ev_g_position()
            pos = unit.ev_g_position()
            if not pos or not center:
                self.clear_locate(eid)
                return
            pos.y = 0
            dire = pos - center
            dire.y = 0
            dis = dire.length
            if dire.is_zero:
                dire = math3d.vector(0, 1, 0)
            dire.normalize()
            yaw_diff = global_data.cam_data.yaw - dire.yaw
            radian = yaw_diff + self.HALF_PI
            ratio = min(dis / self.MID, 1.0)
            x = ratio * math.cos(radian) * self.RADIUS + self.CENTER
            y = ratio * math.sin(radian) * self.RADIUS + self.CENTER
            widget.SetPosition(str(x) + '%', str(y) + '%')
            return

    def init_common_widget(self, g_id):
        if g_id in self.locate_widgets:
            self.clear_locate(g_id)
        widget = global_data.uisystem.load_template_create('pve/i_pve_map_point', self.panel.img_map)
        widget.setVisible(False)
        self.locate_widgets[g_id] = widget

    def init_tick(self, *args):
        self.nd_mid.setVisible(True)
        self.nd_far.setVisible(True)
        self.reset_tick_timer()
        self.tick_timer = global_data.game_mgr.register_logic_timer(self.tick_monster, self.tick_dur, None, -1, CLOCK)
        return

    def reset_tick_timer(self):
        if self.tick_timer:
            global_data.game_mgr.unregister_logic_timer(self.tick_timer)
            self.tick_timer = None
        return

    def tick_monster(self, *args):
        if not global_data.cam_lctarget:
            return
        if not global_data.cam_data:
            return
        is_pizza_type = self.map_type == self.T_PIZZA
        if not is_pizza_type:
            self.nd_near.setVisible(False)
            self.nd_mid.setVisible(False)
            self.nd_far.setVisible(False)
            if self.m_tick_cnt >= self.TICK_CNT:
                self.m_tick_cnt = 0
            else:
                self.bcp_set = set()
            if not self.enable_mecha_radar:
                return
        else:
            self.nd_mid.setVisible(True)
            self.nd_far.setVisible(True)
        center = global_data.cam_lctarget.ev_g_position()
        working_count = 0
        for unit_id, unit in six.iteritems(self.target_set):
            if working_count >= self.TICK_CNT:
                break
            if unit_id in self.cur_set:
                continue
            self.cur_set.add(unit_id)
            working_count += 1
            pos = unit.ev_g_position()
            if not pos:
                continue
            dire = pos - center
            dire.y = 0
            dis = dire.length
            if dire.is_zero:
                dire = math3d.vector(0, 1, 0)
            dire.normalize()
            yaw_diff = global_data.cam_data.yaw - dire.yaw
            sector = int((yaw_diff + self.SECTOR_OFFSET) / self.SECTOR_SIZE) % 8
            if 1 < sector < 7:
                self.has_monster_sector_set.add(sector)
            if is_pizza_type:
                if dis < self.NEAR:
                    self.near_vis = True
                elif dis < self.MID:
                    self.mid_vis = self.mid_vis | 1 << sector
                else:
                    self.far_vis = self.far_vis | 1 << sector

        if working_count < self.TICK_CNT:
            self.check_sync_data()
            self.cur_set = set()
            self.has_monster_sector_set = set()
            if is_pizza_type:
                self.nd_near.setVisible(self.near_vis)
                for i in range(8):
                    mid_bit = self.mid_vis & 1 << i
                    far_bit = self.far_vis & 1 << i
                    nd_mid = getattr(self.nd_mid, 'img_mid%d' % i)
                    nd_mid and nd_mid.setVisible(bool(mid_bit))
                    nd_far = getattr(self.nd_far, 'img_far%d' % i)
                    nd_far and nd_far.setVisible(bool(far_bit))

                self.near_vis = False
                self.mid_vis = 0
                self.far_vis = 0

    def check_sync_data(self):
        if not self.last_has_monster_sector_set ^ self.has_monster_sector_set:
            return
        if self._mecha_radar_widget:
            self._mecha_radar_widget.refresh_visible(self.has_monster_sector_set)
            self.last_has_monster_sector_set = self.has_monster_sector_set

    def on_mecha_init(self, unit):
        self.teammate_set[unit.id] = unit
        self.set_teammate_track(unit)

    def on_mecha_crashed(self, eid):
        if eid in self.teammate_set:
            self.teammate_set.pop(eid)
        self.cancel_teammate_track(eid)

    def set_teammate_track(self, unit):
        eid = unit.id
        self.init_teammate_widget(eid)
        self.reset_locate_timer(eid)
        self.locate_timers[eid] = global_data.game_mgr.register_logic_timer(lambda u=unit: self.calc_teammate_nd_pos(unit), self.TICK_DUR, None, -1, CLOCK)
        return

    def cancel_teammate_track(self, eid):
        self.clear_locate(eid)

    def init_teammate_widget(self, eid):
        if eid in self.locate_widgets:
            self.clear_locate(eid)
        widget = global_data.uisystem.load_template_create('pve/i_pve_map_teammate', self.panel.img_map)
        widget.setVisible(False)
        self.locate_widgets[eid] = widget

    def calc_teammate_nd_pos(self, unit):
        if not global_data.cam_lctarget:
            return
        else:
            if not global_data.cam_data:
                return
            eid = unit.id
            widget = self.locate_widgets.get(eid, None)
            if not widget:
                self.clear_locate(eid)
                return
            if eid == global_data.cam_lctarget.id:
                widget.setVisible(False)
                return
            widget.setVisible(True)
            center = global_data.cam_lctarget.ev_g_position()
            pos = unit.ev_g_position()
            if not pos or not center:
                self.clear_locate(eid)
                return
            pos.y = 0
            dire = pos - center
            dire.y = 0
            dis = dire.length
            if dire.is_zero:
                dire = math3d.vector(0, 1, 0)
            dire.normalize()
            yaw_diff = global_data.cam_data.yaw - dire.yaw
            radian = yaw_diff + self.HALF_PI
            ratio = min(dis / self.MID, 1.0)
            x = ratio * math.cos(radian) * self.RADIUS + self.CENTER
            y = ratio * math.sin(radian) * self.RADIUS + self.CENTER
            widget.SetPosition(str(x) + '%', str(y) + '%')
            t_forward = unit.ev_g_forward()
            t_forward.y = 0
            if t_forward.is_zero:
                t_forward = math3d.vector(0, 1, 0)
            t_forward.normalize()
            t_yaw_diff = t_forward.yaw - global_data.cam_data.yaw
            degree = math.degrees(t_yaw_diff)
            widget.setRotation(degree)
            return