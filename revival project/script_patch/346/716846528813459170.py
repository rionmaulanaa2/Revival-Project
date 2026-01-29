# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/SmallMapCircleStateWidget.py
from __future__ import absolute_import
from logic.gcommon.common_const.poison_circle_const import POISON_CIRCLE_STATE_STABLE, POISON_CIRCLE_STATE_REDUCE
import math3d
from logic.gutils.math_utils import poly1d
from logic.gcommon import time_utility
from logic.gutils.map_utils import get_map_dist
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.comsys.guide_ui.GuideUI import GuideUI, PCGuideUI
TIME_STR_FMT = '%(min)01d:%(sec)02d'
UNSAVE_PLAYER_FRAME = 'gui/ui_res_2/battle/map/icon_flag_2.png'
SAVE_PLAYER_FRAME = 'gui/ui_res_2/battle/map/icon_flag.png'
OVERVIEW_SCALE_UP = 0
OVERVIEW_SCALE_DOWN = 1
OVERVIEW_SCALE_WAIT = 2

class SmallMapCircleStateWidget(object):
    TIME_TAG = 190313

    def __init__(self, panel):
        super(SmallMapCircleStateWidget, self).__init__()
        self.map_panel = panel
        self.poison_widget = panel.nd_hide
        self._is_valid = True
        self.player_widget = panel.player
        self.in_over_view = False
        self.player_progress = 0
        self._time_poison_data = None
        self.time_color = '#SW'
        self.init_event()
        self.update_widget()
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.update_widget, 30)
        self.smooth_scale_timer_id = 0
        self.overview_state = OVERVIEW_SCALE_UP
        self.wait_timer = 0
        return

    def update_widget(self):
        if not self._is_valid:
            return
        else:
            poison_mgr = self.map_panel.poison_mgr()
            if not poison_mgr:
                return
            poison_data = poison_mgr.get_cnt_circle_info()
            if poison_data.get('state', None) not in [POISON_CIRCLE_STATE_REDUCE, POISON_CIRCLE_STATE_STABLE]:
                self.poison_widget.setVisible(False)
                self._time_poison_data = None
                return
            self.poison_widget.setVisible(True)
            self.check_poison_data_time(poison_data)
            self.update_progress(poison_data)
            self.update_player_progress(poison_data)
            return

    def check_poison_data_time(self, poison_data):
        if self._time_poison_data != poison_data:
            self._time_poison_data = poison_data
            self.update_circle_time()

    def init_event(self):
        global_data.emgr.scene_poison_updated_event += self.on_posion_changed
        global_data.emgr.net_login_reconnect_event += self.on_reconnect
        global_data.emgr.nbomb_show_map_overview += self.show_nbomb_overview

    def uninit_event(self):
        global_data.emgr.scene_poison_updated_event -= self.on_posion_changed
        global_data.emgr.net_login_reconnect_event -= self.on_reconnect
        global_data.emgr.nbomb_show_map_overview -= self.show_nbomb_overview

    def on_reconnect(self, *args):
        global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = global_data.game_mgr.register_logic_timer(self.update_widget, 30)

    def on_posion_changed(self, force=False):
        self.update_widget()
        poison_mgr = self.map_panel.poison_mgr()
        if not poison_mgr:
            return
        else:
            poison_data = poison_mgr.get_cnt_circle_info()
            if force or poison_data.get('state', None) == POISON_CIRCLE_STATE_STABLE:
                self.show_reduce_overview(poison_data)
            return

    def update_circle_time(self):
        poison_data = self._time_poison_data
        if not poison_data:
            return
        cur_time = time_utility.time()
        cur_local_time = poison_data['start_time'] + poison_data['last_time'] - cur_time
        if cur_local_time < 0:
            cur_local_time = 0
        time_str = time_utility.get_delta_time_str(cur_local_time, fmt=TIME_STR_FMT)
        if cur_local_time <= 10:
            color = '#SR'
        elif poison_data['state'] == POISON_CIRCLE_STATE_REDUCE:
            color = '#SO'
        else:
            color = '#SW'
        if color != self.time_color:
            self.time_color = color
            self.map_panel.time.SetColor(self.time_color)
        self.map_panel.time.SetString(time_str)
        time_delta = cur_local_time - int(cur_local_time)
        if cur_local_time > 0:
            self.map_panel.time.SetTimeOut(time_delta + 0.003, self.update_circle_time, self.TIME_TAG)

    def update_player_progress(self, poison_data):
        if not self._is_valid:
            return
        if self.player_widget and not self.player_widget.isValid():
            raise RuntimeError('invalid self.player_widget!', self.map_panel.isValid())
        cam_lplayer = global_data.cam_lplayer
        if not (cam_lplayer and poison_data['level']):
            self.player_widget.setVisible(False)
            return
        player_pos = cam_lplayer.ev_g_position() or cam_lplayer.ev_g_model_position()
        if not player_pos:
            self.player_widget.setVisible(False)
            return
        self.player_widget.setVisible(True)
        self.player_progress = 0
        t_p_length = 0
        player_pos = math3d.vector(player_pos)
        player_pos.y = 0
        player_distance = (player_pos - poison_data['safe_center']).length
        original_radius = poison_data['original_radius']
        target_radius = poison_data['safe_radius']
        dist = 0
        if player_distance < target_radius:
            self.player_progress = 100.0
        elif player_distance > original_radius:
            self.player_progress = 0.0
        else:
            dist, self.player_progress = self.calc_player_progress(original_radius, target_radius, player_pos, poison_data['safe_center'], poison_data['original_center'])
        self.player_widget.SetPosition('%d%%' % int(self.player_progress), self.player_widget.getPosition().y)
        self.player_widget.SetDisplayFrameByPath('', SAVE_PLAYER_FRAME if self.player_progress >= 100.0 else UNSAVE_PLAYER_FRAME)
        self.on_distance_to_safecricle(dist)

    def on_distance_to_safecricle(self, dist):
        self.map_panel.bar_distance1.setVisible(False)
        self.map_panel.bar_distance2.setVisible(False)
        if dist > 0:
            indext = 1 if self.player_progress < 50 else 2
            bar_node = getattr(self.map_panel, 'bar_distance%d' % indext)
            bar_node.setVisible(True)
            lab_node = getattr(self.map_panel, 'lab_distance%d' % indext)
            lab_node.SetString('%dm' % int(dist / NEOX_UNIT_SCALE))
            tw, th = bar_node.GetContentSize()
            bw, bh = lab_node.GetContentSize()
            bar_node.SetContentSize(bw + 2, th)
            bar_node.RecursionReConfPosition()

    def calc_player_progress(self, original_radius, target_radius, player_pos, target_center, original_center):
        center_outer_distance = 0
        target_center = math3d.vector(target_center.x, 0.0, target_center.z)
        original_center = math3d.vector(original_center.x, 0.0, original_center.z)
        player_pos = math3d.vector(player_pos.x, 0.0, player_pos.z)
        target_original_vec = target_center - original_center
        t_o_length = target_original_vec.length
        if t_o_length == 0:
            center_outer_distance = original_radius
        else:
            t_o_norm = math3d.vector(target_original_vec)
            t_o_norm.normalize()
            t_p_vec = target_center - player_pos
            t_p_norm = math3d.vector(t_p_vec)
            t_p_norm.normalize()
            cos_value = t_o_norm.dot(t_p_norm)
            b = -2 * t_o_length * cos_value
            c = t_o_length * t_o_length - original_radius * original_radius
            center_outer_distance = max(*poly1d(1, b, c))
        t_p_length = (target_center - player_pos).length
        return (
         t_p_length - target_radius, 100 * (1.0 - (t_p_length - target_radius) / (center_outer_distance - target_radius)))

    def update_progress(self, poison_data):
        if poison_data['state'] == POISON_CIRCLE_STATE_REDUCE:
            original_radius = poison_data['original_radius']
            target_radius = poison_data['safe_radius']
            cur_radius = poison_data['harm_radius']
            if original_radius is None or target_radius is None or cur_radius is None:
                return
            delta_radius = original_radius - target_radius
            if delta_radius != 0:
                percent = (original_radius - cur_radius) * 1.0 / delta_radius
            else:
                percent = 1
            self.map_panel.poison_progress.SetPercent(percent * 100)
            if percent < 1:
                self.map_panel.poison_progress.img_poison_light.setVisible(True)
                x, y = self.map_panel.poison_progress.img_poison_light.CalcPosition('%d%%' % (percent * 100), 0)
                self.map_panel.poison_progress.img_poison_light.setPositionX(x)
            else:
                self.map_panel.poison_progress.img_poison_light.setVisible(False)
        else:
            self.map_panel.poison_progress.SetPercent(0)
            self.map_panel.poison_progress.img_poison_light.setVisible(False)
        return

    def destroy(self):
        if self.map_panel and self._is_valid:
            self.map_panel.time.stopAllActions()
        self._is_valid = False
        self.map_panel = None
        self.poison_widget = None
        self.player_widget = None
        self._time_poison_data = None
        global_data.game_mgr.unregister_logic_timer(self.update_timer_id)
        self.update_timer_id = 0
        global_data.game_mgr.unregister_logic_timer(self.smooth_scale_timer_id)
        self.smooth_scale_timer_id = 0
        self.uninit_event()
        return

    def set_overview_mode(self, mode):
        self.in_over_view = mode
        self.map_panel.player_info_widget.set_follow_player_enable(not mode)

    def show_reduce_overview(self, poison_data):
        if 0 < poison_data['level'] <= 3:
            if self.in_over_view:
                return
            viewer = global_data.cam_lplayer
            if not viewer:
                return
            pos = viewer.ev_g_position()
            if not pos:
                return
            self.set_overview_mode(True)
            original_center = poison_data['original_center']
            circle_widget = self.map_panel.circle_widget
            map_original_center = circle_widget.trans_world_position(original_center)
            pos = math3d.vector(pos)
            pos.y = 0
            p_c_distance = (pos - original_center).length
            show_radius = max(p_c_distance, poison_data['original_radius']) + 2000
            show_ratio = show_radius * 2.0 / get_map_dist()
            min_scale = self.map_panel.min_map_scale
            max_scale = self.map_panel.max_map_scale
            target_scale = min_scale / show_ratio
            target_scale = min(max_scale, max(target_scale, min_scale))
            original_scale = self.map_panel.cur_map_scale
            self.overview_state = OVERVIEW_SCALE_UP
            if target_scale > original_scale:
                return
            self.set_overview_mode(True)
            delta_scale = (target_scale - original_scale) / 15
            global_data.game_mgr.unregister_logic_timer(self.smooth_scale_timer_id)
            self.smooth_scale_timer_id = global_data.game_mgr.register_logic_timer(self.do_smooth_map_scale, 1, args=(target_scale, original_scale, map_original_center, delta_scale))

    def show_nbomb_overview(self, nbomb_data):
        if self.in_over_view:
            return
        viewer = global_data.cam_lplayer
        if not viewer:
            return
        viewer_pos = viewer.ev_g_position()
        if not viewer_pos:
            return
        viewer_pos.y = 0
        tpl_target_center = nbomb_data.get('target_pos')
        if not tpl_target_center:
            return
        vec_target_center = math3d.vector(*tpl_target_center)
        map_target_center = self.map_panel.circle_widget.trans_world_position(vec_target_center)
        dist = (viewer_pos - vec_target_center).length
        show_radius = dist + 2000
        show_ratio = show_radius * 2.0 / get_map_dist()
        min_scale = self.map_panel.min_map_scale
        max_scale = self.map_panel.max_map_scale
        target_scale = min_scale / show_ratio
        target_scale = min(max_scale, max(target_scale, min_scale))
        original_scale = self.map_panel.cur_map_scale
        self.overview_state = OVERVIEW_SCALE_UP
        if target_scale > original_scale:
            return
        self.set_overview_mode(True)
        delta_scale = (target_scale - original_scale) / 15
        global_data.game_mgr.unregister_logic_timer(self.smooth_scale_timer_id)
        self.smooth_scale_timer_id = global_data.game_mgr.register_logic_timer(self.do_smooth_map_scale, 1, args=(target_scale, original_scale, map_target_center, delta_scale))
        if global_data.is_pc_mode:
            guide_ui = PCGuideUI()
        else:
            guide_ui = GuideUI()
        guide_ui and guide_ui.show_small_map_overview_tip(1)

    def do_smooth_map_scale(self, target_scale, from_scale, center, delta_scale, wait_time=2.0):
        if self.overview_state == OVERVIEW_SCALE_UP:
            if self.map_panel.cur_map_scale == target_scale:
                self.overview_state = OVERVIEW_SCALE_WAIT
                self.wait_timer = time_utility.time()
                return
            new_scale = max(self.map_panel.cur_map_scale + delta_scale, target_scale)
            self.map_panel.set_map_scale(new_scale)
            self.map_panel.sv_map.CenterWithPos(center.x * new_scale, center.y * new_scale)
        elif self.overview_state == OVERVIEW_SCALE_WAIT:
            if time_utility.time() - self.wait_timer > wait_time:
                self.overview_state = OVERVIEW_SCALE_DOWN
        elif self.overview_state == OVERVIEW_SCALE_DOWN:
            if self.map_panel.cur_map_scale == from_scale:
                global_data.game_mgr.unregister_logic_timer(self.smooth_scale_timer_id)
                self.set_overview_mode(False)
                return
            new_scale = min(self.map_panel.cur_map_scale - delta_scale, from_scale)
            self.map_panel.set_map_scale(new_scale)
            viewer = global_data.cam_lplayer
            if not viewer:
                return
            pos = viewer.ev_g_position()
            if not pos:
                return
            circle_widget = self.map_panel.circle_widget
            player_map_pos = circle_widget.trans_world_position(pos)
            self.map_panel.sv_map.CenterWithPos(player_map_pos.x * new_scale, player_map_pos.y * new_scale)


class SmallMapCircleStateWidgetPC(SmallMapCircleStateWidget):

    def update_widget(self):
        if not self._is_valid:
            return
        else:
            poison_mgr = self.map_panel.poison_mgr()
            if not poison_mgr:
                return
            poison_data = poison_mgr.get_cnt_circle_info()
            if poison_data.get('state', None) not in [POISON_CIRCLE_STATE_REDUCE, POISON_CIRCLE_STATE_STABLE]:
                self.poison_widget.setVisible(False)
                self.map_panel.lab_time_text.setVisible(False)
                self.map_panel.time.setVisible(False)
                self._time_poison_data = None
                return
            self.poison_widget.setVisible(True)
            self.map_panel.lab_time_text.setVisible(True)
            self.map_panel.time.setVisible(True)
            self.check_poison_data_time(poison_data)
            self.update_progress(poison_data)
            self.update_player_progress(poison_data)
            return