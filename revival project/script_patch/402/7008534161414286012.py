# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/test/ProfileGraphUI.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import GUIDE_LAYER_ZORDER
from common.uisys.uielment.CCLayer import CCLayer
from common.uisys.uidebug.CocosDrawer import CocosDrawer
from logic.gcommon import time_utility
import time
import profiling
import cc
from common.const import uiconst
WHITE_COLOR = cc.Color4F(1.0, 1.0, 1.0, 1.0)
BLUE_COLOR = cc.Color4F(36 / 255.0, 196 / 255.0, 1.0, 1)
from common.utils.cocos_utils import ccc4fFromHex, ccc3fFromHex
from common.uisys.color_table import get_color_val
import world

class ProfileGraphUI(BasePanel):
    PANEL_CONFIG_NAME = 'test/frame_viewer'
    DLG_ZORDER = GUIDE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_close.btn_common.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self):
        self.panel.lab_frame_rate.setString('\xe5\x88\x9d\xe5\xa7\x8b\xe6\x95\xb0\xe6\x8d\xae\xe7\xa7\xaf\xe7\xb4\xaf\xe4\xb8\xad')
        self._graph_list = []
        self._label_list = {}
        self._ave_label_dict = {}
        self.set_graph()

    def set_graph(self):
        self._ave_label_dict['1'] = '\xe5\xb9\xb3\xe5\x9d\x87\xe5\xb8\xa7\xe7\x8e\x87\xef\xbc\x9a%.1f'
        gd = self.add_graph('1', lambda : profiling.get_logic_rate())
        gd.set_color(WHITE_COLOR, WHITE_COLOR)
        start = -330
        offset = 70 + start
        gd.drawer.set_axis_offset(cc.Vec2(0, 0), cc.Vec2(offset, 0))
        self._ave_label_dict['2'] = 'dp \xe6\x95\xb0\xef\xbc\x9a%.1f'
        gd2 = self.add_graph('2', lambda : profiling.get_dp_num())
        offset = 150 + start
        gd2.set_color(ccc3fFromHex(get_color_val('#SY')), ccc3fFromHex(get_color_val('#SY')))
        gd2.drawer.set_axis_offset(cc.Vec2(0, 0), cc.Vec2(offset, 0))
        self._ave_label_dict['3'] = '\xe9\x9d\xa2 \xe6\x95\xb0\xef\xbc\x9a%.1f'
        gd2 = self.add_graph('3', lambda : profiling.get_prim_num())
        offset = 270 + start
        gd2.set_color(ccc3fFromHex(get_color_val('#SR')), ccc3fFromHex(get_color_val('#SR')))
        gd2.drawer.set_axis_offset(cc.Vec2(0, 0), cc.Vec2(offset, 0))
        self._ave_label_dict['4'] = 'submesh \xef\xbc\x9a%.1f'
        gd2 = self.add_graph('4', lambda : self.cal_submesh())
        offset = 340 + start
        gd2.set_color(ccc3fFromHex(get_color_val('#SP')), ccc3fFromHex(get_color_val('#SP')))
        gd2.drawer.set_axis_offset(cc.Vec2(0, 0), cc.Vec2(offset, 0))
        legend_data_list = [
         ('\xe5\xb8\xa7\xe7\x8e\x87', '#SW'), ('dp', '#SY'), ('\xe9\x9d\xa2\xe6\x95\xb0', '#SR'), ('submesh', '#SP')]
        self.panel.sv_legend.SetInitCount(len(legend_data_list))
        for idx, legend in enumerate(legend_data_list):
            legend_data = legend_data_list[idx]
            ui_item = self.panel.sv_legend.GetItem(idx)
            ui_item.SetColor(legend_data[1])
            ui_item.lab_name.SetString(legend_data[0])

    def cal_submesh(self):
        scn = world.get_active_scene()
        t = 0
        md = {}
        for m in scn.get_models():
            if m.visible and m.is_visible_in_this_frame():
                t += m.get_submesh_count()

        return t

    def on_finalize_panel(self):
        for g in self._graph_list:
            g.destroy()

        self._graph_list = []
        self._label_list = {}

    def on_click_close_btn(self, btn, touch):
        self.close()

    def add_graph(self, key, y_func):
        gd = GraphDrawer(self.panel)
        gd.set_data_func(y_func, lambda t: self.on_label_info_callback(key, t))
        self._graph_list.append(gd)
        return gd

    def on_label_info_callback(self, key, label):
        self._label_list[key] = label
        msg_list = []
        cur_fps = profiling.get_logic_rate()
        cur_render_fps = profiling.get_render_rate()
        for l in sorted(six_ex.keys(self._label_list)):
            if l in self._ave_label_dict:
                msg_list.append(self._ave_label_dict[l] % self._label_list.get(l, 0))

        msg = '\xe7\x9e\xac\xe6\x97\xb6\xe5\xb8\xa7\xe7\x8e\x87(logic:%.1f, render:%.1f)' % (cur_fps, cur_render_fps)
        msg_list.append(msg)
        self.panel.lab_frame_rate.setString(' '.join(msg_list))


class GraphDrawer(object):

    def __init__(self, panel):
        self.panel = panel
        from logic.gutils.hot_key_utils import get_ui_mouse_scroll_sensitivity
        self.ui_scroll_sensitivity = get_ui_mouse_scroll_sensitivity(self.__class__.__name__)
        self._label_callback = None
        self._y_func = None
        self._axis_y_label_range = None
        self.on_init_panel()
        return

    def set_axis_y_label_range(self, y_range):
        self._axis_y_label_range = y_range

    def set_color(self, axis_y_color, line_color):
        self.drawer.axis_color = axis_y_color
        self.drawer.line_color = line_color

    def set_data_func(self, y_func, label_callback):
        self._y_func = y_func
        self._label_callback = label_callback

    def destroy(self):
        self.set_data_func(None, None)
        self.panel = None
        return

    def on_init_panel(self):
        self.drawer = CocosDrawer(self.panel.layer_touch)
        touch_mgr = global_data.touch_mgr_agent
        touch_mgr.register_wheel_event(self.__class__.__name__, self.on_mouse_scroll)
        self._scroll_center_percent = 0.5
        self._cur_mouse_dist = 0
        self._time_list = []
        self._fps_list = []
        self.x_data = []
        self.y_data = []

        @self.panel.layer_touch.callback()
        def OnClick(btn, touch):
            wpos = touch.getLocation()
            self._scroll_center_percent = self.drawer.get_touch_x_percent(wpos)

        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.tick),
         cc.DelayTime.create(1.0)])))

    def show_data(self, x_data, y_data):
        self.x_data = x_data
        self.y_data = y_data
        self.scale = 1
        self._show_data_helper(self.x_data, self.y_data)

    def _show_data_helper(self, x_data, y_data):
        x_label = CocosDrawer.cal_label_list(x_data, 6)
        x_formated_label = []
        for per, x in x_label:
            if x:
                label = time_utility.get_time_string('%M:%S', x) if 1 else x
                x_formated_label.append((per, label))

        self.drawer.clear()
        if not self._axis_y_label_range:
            y_label_data = [
             max(int(min(y_data) * 0.8 / 10.0) * 10, 0), max(60, int(max(y_data) * 1.2 / 10.0) * 10)]
        else:
            y_label_data = self._axis_y_label_range
        self.drawer.draw_graph_axis(x_formated_label, CocosDrawer.cal_num_label_list(y_label_data, 6))
        self.drawer.draw_graph(x_data, y_data)

    def on_finalize_panel(self):
        touch_mgr = global_data.touch_mgr_agent
        touch_mgr.unregister_wheel_event(self.__class__.__name__)
        if self.drawer:
            self.drawer.destroy()
            self.drawer = None
        return

    def test3(self):
        import random
        x = [ 'X' + str(x) for x in range(0, 600) ]
        y = [ random.randrange(0, 30) for i in range(600) ]
        self.show_data(x, y)

    def on_mouse_scroll(self, msg, delta, key_state):
        if not self.x_data:
            return
        dist = -delta
        self._cur_mouse_dist += dist
        if abs(self._cur_mouse_dist) > self.ui_scroll_sensitivity:
            changed_index = int(self._cur_mouse_dist / self.ui_scroll_sensitivity)
            changed_index = max(-1, changed_index)
            if changed_index > 0:
                self.scale *= 2.0
            else:
                self.scale /= 2.0
            self._cur_mouse_dist = 0
            self.scale = min(self.scale, 1.0)
            if self.scale == 1.0:
                self._show_data_helper(self.x_data, self.y_data)
            else:
                all_data_len = len(self.x_data)
                show_data_len = max(min(all_data_len * self.scale, all_data_len), 10)
                center_index = int(self._scroll_center_percent * all_data_len)
                start_index = int(max(center_index - show_data_len / 2.0, 0))
                end_index = int(min(center_index + show_data_len / 2.0, all_data_len - 1))
                x_show_data = self.x_data[start_index:end_index + 1]
                y_show_data = self.y_data[start_index:end_index + 1]
                self._show_data_helper(x_show_data, y_show_data)

    def tick(self):
        if not callable(self._y_func):
            return
        cur_fps = self._y_func()
        cur_time = time.time()
        self._time_list.append(cur_time)
        self._fps_list.append(cur_fps)
        if len(self._time_list) > 60:
            start_time = self._time_list[0]
            end_time = self._time_list[-1]
            if end_time - start_time > 300:
                self._time_list = self._time_list[30:]
                self._fps_list = self._fps_list[30:]
        if len(self._time_list) > 5:
            self._show_data_helper(self._time_list, self._fps_list)
        if callable(self._label_callback):
            if len(self._time_list) > 1:
                label_info = float(sum(self._fps_list)) / len(self._fps_list)
                self._label_callback(label_info)