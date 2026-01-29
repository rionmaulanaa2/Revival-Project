# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/QuickMarkUI.py
from __future__ import absolute_import
from __future__ import print_function
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.common_const.battle_const import MARK_NORMAL, MARK_GOTO, MARK_DANGER, MARK_RES, MARK_NONE, MARK_GATHER, MARK_WAY_QUICK
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.collision_const import GROUP_CAMERA_COLL
from logic.gutils.camera_utils import get_camera_hit_pos, get_camera_direction, get_camera_position
from logic.gutils import map_utils
from common.cfg import confmgr
from common.const import uiconst
import game3d

class QuickMarkUI(BasePanel):
    PANEL_CONFIG_NAME = 'map/mark_quick'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    ENABLE_DRAW_LINE = False

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.add_hide_count('QuickMarkUI')
        self.draw_line_timer_id = 0
        self.init_event()
        self.panel.setLocalZOrder(1)

    def init_event(self):
        global_data.emgr.scene_observed_player_setted_event += self.on_enter_observe

    def on_enter_observe(self, *args):
        global_data.ui_mgr.close_ui('QuickMarkUI')

    def init_parameters(self, **kwargs):
        self.is_mid_map_mark = False
        self.is_active = False
        self.cur_sel_mark_btn = None
        self.center_wpos = self.panel.btn_cancel.ConvertToWorldSpacePercentage(50, 50)
        self.mark_btn_type_dict = {MARK_NONE: self.panel.btn_cancel,
           MARK_GOTO: self.panel.btn_goto_locate,
           MARK_DANGER: self.panel.btn_danger_locate,
           MARK_RES: self.panel.btn_resource_locate,
           MARK_GATHER: self.panel.btn_gather
           }
        self.update_mark_btn_pos()
        return

    def update_mark_btn_pos(self):
        self.mark_btn_pos_dict = {}
        for k, v in six.iteritems(self.mark_btn_type_dict):
            if k == MARK_NONE:
                continue
            self.mark_btn_pos_dict[k] = v.ConvertToWorldSpacePercentage(50, 50)

    def draw_scene_direct_line(self):
        lavatar = global_data.cam_lplayer
        if not (lavatar and lavatar.is_valid()):
            return
        hit_point, model_cobj = get_camera_hit_pos(GROUP_CAMERA_COLL, 300)
        eye_mat = lavatar.ev_g_model_socket_pos('eye')
        if eye_mat and hit_point:
            global_data.emgr.scene_draw_leading_line_event.emit([eye_mat.translation, hit_point])

    def remove_scene_direct_line(self):
        global_data.emgr.scene_remove_leading_line_event.emit()

    def enable_mid_map(self, enable):
        self.is_mid_map_mark = enable

    def set_scene_map_mark(self, mark_type):
        if mark_type == MARK_NONE:
            return
        else:
            map_utils.send_mark_group_msg(mark_type)
            if self.is_mid_map_mark:
                global_data.emgr.on_mid_map_mark.emit(mark_type)
                return
            self.remove_scene_direct_line()
            if not (global_data.player and global_data.player.logic):
                return
            lavatar = global_data.player.logic
            if mark_type == MARK_GATHER:
                hit_point = lavatar.ev_g_position()
                lavatar.send_event('E_SHOW_MESSAGE', get_text_local_content(16029))
            else:
                hit_point, model_cobj = get_camera_hit_pos(GROUP_CAMERA_COLL, 300)
                inner_show_text = ''
                if global_data.is_inner_server and model_cobj:
                    model_col_name = getattr(model_cobj, 'model_col_name', None)
                    if model_col_name:
                        model = global_data.game_mgr.scene.get_model(model_col_name)
                        if model:
                            model_name = model.get_attr('model_name')
                            model_path = confmgr.get('model_name_to_path', model_name)
                            if model_path:
                                str_show = model_col_name + '  :  ' + model_path
                                global_data.game_mgr.show_tip(get_text_by_id(160).format(str_show))
                                inner_show_text += model_path
                if global_data.use_sunshine:
                    global_data.sunshine_mark_point = [
                     hit_point.x, hit_point.y + 5, hit_point.z]
                    from common.utils import hotkey
                    ret = True
                    print('mark check ctrl and alt', hotkey.ctrl_down, hotkey.alt_down, hotkey.shift_down)
                    if hotkey.ctrl_down:
                        ret = global_data.sunshine_editor.galaxy_plugin.OnCtrlChoosePoint()
                    else:
                        if hotkey.alt_down:
                            ret = global_data.sunshine_editor.galaxy_plugin.OnAltChoosePoint()
                        elif hotkey.shift_down:
                            ret = global_data.sunshine_editor.galaxy_plugin.OnShiftChoosePoint()
                        if not ret:
                            return
                    inner_show_text += ' %s %s %s' % (str(hit_point.x), str(hit_point.y), str(hit_point.z))
                if global_data.is_inner_server:
                    game3d.set_clipboard_text(inner_show_text)
                global_data.emgr.show_scene_quick_mark.emit(hit_point)
            if hit_point:
                lavatar.send_event('E_TRY_DRAW_MAP_MARK', mark_type, hit_point, None, MARK_WAY_QUICK)
            else:
                cam_pos = get_camera_position()
                cam_pos = (cam_pos.x, cam_pos.y, cam_pos.z)
                direction = get_camera_direction()
                direction = (direction.x, direction.y, direction.z)
                lavatar.send_event('E_CALL_SYNC_METHOD', 'try_ray_mark', (cam_pos, direction, mark_type, MARK_WAY_QUICK), True)
            return

    def on_press_tick(self):
        self.draw_scene_direct_line()

    def on_begin(self, wpos):
        self.is_active = True
        lpos = self.panel.nd_choose_mark.getParent().convertToNodeSpace(wpos)
        self.panel.nd_choose_mark.setPosition(lpos)
        self.update_mark_btn_pos()
        self.add_show_count('QuickMarkUI')
        self.set_select(MARK_NONE)
        if not self.ENABLE_DRAW_LINE:
            return
        self.draw_scene_direct_line()
        global_data.game_mgr.unregister_logic_timer(self.draw_line_timer_id)
        self.draw_line_timer_id = global_data.game_mgr.register_logic_timer(self.on_press_tick, 1)

    def on_end(self, wpos):
        self.add_hide_count('QuickMarkUI')
        mark_type = self.get_cur_sel_mark_type(wpos)
        self.set_scene_map_mark(mark_type)
        global_data.game_mgr.unregister_logic_timer(self.draw_line_timer_id)
        self.is_active = False

    def on_drag(self, wpos):
        mark_type = self.get_cur_sel_mark_type(wpos)
        self.set_select(mark_type)

    def set_select(self, mark_type):
        if self.cur_sel_mark_btn:
            self.cur_sel_mark_btn.SetSelect(False)
        if mark_type not in self.mark_btn_type_dict:
            return
        mark_btn = self.mark_btn_type_dict[mark_type]
        mark_btn.SetSelect(True)
        self.cur_sel_mark_btn = mark_btn

    def get_cur_sel_mark_type(self, wpos):
        mark_type = MARK_NONE
        if self.panel.btn_cancel.IsPointIn(wpos):
            mark_type = MARK_NONE
        else:
            min_dis = 1000000000
            for k, v in six.iteritems(self.mark_btn_pos_dict):
                diff_x = wpos.x - v.x
                diff_y = wpos.y - v.y
                diff_dis = diff_x * diff_x + diff_y * diff_y
                if diff_dis < min_dis:
                    mark_type = k
                    min_dis = diff_dis

        return mark_type

    def on_finalize_panel(self):
        global_data.game_mgr.unregister_logic_timer(self.draw_line_timer_id)