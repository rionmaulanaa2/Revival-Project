# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/ScalePlateUI.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
import cc
from common.utils.cocos_utils import ccp
from common.const.uiconst import SCALE_PLATE_ZORDER, LOW_MESSAGE_ZORDER
from logic.gutils.team_utils import get_color_pic_path, get_mark_pic_path
from logic.gcommon.common_const.battle_const import MARK_DANGER, MARK_GOTO, MARK_NORMAL, MARK_RES, MARK_TYPE_TO_CLASS, MARK_CLASS_RES, MARK_CLASS_WARNING, MARK_CLASS_CNT
from math import pi
import logic.gcommon.const as const
from logic.gutils.team_utils import get_teammate_colors
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils import scene_utils
import math3d
import world
ANGLE_PER_LABEL = 15
from common.uisys.basepanel import BasePanel
import math

class ScaleMark(object):

    def __init__(self, parent_nd):
        self.parent_nd = parent_nd
        self._nd = global_data.uisystem.load_template_create('map/ccb_scale_mark')
        self.parent_nd.AddChild('', self._nd)

    def set_scale_mark(self, type, color):
        pic_path = get_mark_pic_path(type, color)
        self._nd.sp_mark.SetDisplayFrameByPath('', pic_path)
        pic_path = get_color_pic_path('gui/ui_res_2/battle/map/mark_angle_', color)
        self._nd.mark_angle.SetDisplayFrameByPath('', pic_path)

    def destroy(self):
        if self._nd:
            self._nd.removeFromParent()
            self._nd = None
        if self.parent_nd:
            self.parent_nd = None
        return

    def SetPosition(self, x, y):
        self._nd.SetPosition(x, y)

    def PlayAnimation(self, name):
        self._nd.PlayAnimation(name)

    def StopAnimation(self, name):
        self._nd.StopAnimation(name)

    def set_texiao_vis(self, vis):
        self._nd.texiao_small.setVisible(vis)
        self._nd.texiao_big.setVisible(vis)

    def update_mark_distance(self, distance):
        nd = self._nd.nd_distance
        nd.lab_distance.setString('%dm' % (distance / NEOX_UNIT_SCALE))
        old_sz = nd.getContentSize()
        new_width = nd.lab_distance.getContentSize().width + 6
        if new_width - old_sz.width > 0.1:
            nd.SetContentSize(new_width, old_sz.height)


from common.const import uiconst

class ScalePlateBaseUI(BasePanel):
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    PANEL_CONFIG_NAME = 'map/fight_angle'
    BG_CONFIG_NAME = 'map/fight_angle_part2'
    DLG_ZORDER = SCALE_PLATE_ZORDER
    BG_DLG_ZORDER = LOW_MESSAGE_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    RIGHT_DIRECT = 0
    LEFT_DIRECT = 1
    BOWEN_LEFT_ANI = 1
    BOWEN_RIGHT_ANI = 2
    OPACITY_EDGE = 135
    LABEL_NUM = 360 // ANGLE_PER_LABEL
    ACTION_TAG_LEFT = 21080401
    ACTION_TAG_RIGHT = 21080402

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.init_event()
        self.prepare_all_nds()
        self.set_opacity_shader()
        self.start_tick()

    def init_parameters(self):
        self.create_direction_scroll()
        self.safe_center = None
        self.player_pos = None
        self.player_color_info = {}
        self.poison_mgr = None
        self.last_mark_info = {}
        types = {0: 80052,45: 80123,90: 80122,135: 80124,180: 80263,225: 80411,270: 80409,315: 80410}
        self.LABEL_TEXTS = {}
        for ty, text_id in six.iteritems(types):
            self.LABEL_TEXTS[ty] = get_text_by_id(text_id)

        self._cur_update_index = 0
        return

    def on_finalize_panel(self):
        self.panel.stopAllActions()
        self.clear_all_marks()

    def on_player_pos_changed(self, pos):
        old_player_pos = self.player_pos
        self.player_pos = pos
        self.update_safe_area_visibility()
        if old_player_pos:
            if (pos - old_player_pos).length > 0.01:
                self._update_scale_mark_pos()

    def init_event(self):
        global_data.emgr.add_scene_mark += self.add_map_mark
        global_data.emgr.remove_scene_mark += self.clear_player_marks
        global_data.emgr.remove_scene_mark_by_type += self._del_scale_mark_by_type
        global_data.emgr.scene_clear_player_map_marks += self.clear_player_marks
        global_data.emgr.scale_plate_set_safe_center_event += self.set_safe_center
        global_data.emgr.scale_plate_set_show_player_ids_event += self.set_show_player_ids

    def create_direction_scroll(self):
        from collections import OrderedDict
        self.view_width, _ = self.panel.sv_direction.GetContentSize()
        self.direction_width = self.panel.sv_direction.GetInnerContentSize().width
        self.direction_anchor_x = self.panel.sv_direction.GetInnerContainer().getAnchorPoint().x
        self._direct_container = self.panel.sv_direction.GetContainer()
        self.direction_pos_y = self._direct_container.bar_1.getPosition().y
        self.panel.sv_direction.setTouchEnabled(False)
        self.cur_direction_bar = self.panel.sv_direction.GetContainer().bar_1
        self.bar_direction_width = self.cur_direction_bar.GetContentSize()[0]
        self.alternate_direction_bar = self.panel.sv_direction.GetContainer().bar_2
        self.cur_angle_label_index = None
        self.raw_yaw = 0.0
        self.center_yaw = 3.14
        self.text_yaw = 0
        self.scale_mark_dict = {}
        self.scale_mark_ani_order_dict = OrderedDict()
        self.is_location_left_ani_playing = False
        self.cur_left_ani_unit_id = None
        self.is_location_right_ani_playing = False
        self.cur_right_ani_unit_id = None
        return

    def OnLeftAnimationCallBack(self, *args):
        self.is_location_left_ani_playing = False
        self.cur_left_ani_unit_id = None
        if self._base_bg_panel:
            self._base_bg_panel.location_left.setVisible(False)
        self.play_next_location_ani(ScalePlateBaseUI.BOWEN_LEFT_ANI)
        return

    def OnRightAnimationCallBack(self, *args):
        self.is_location_right_ani_playing = False
        self.cur_right_ani_unit_id = None
        if self._base_bg_panel:
            self._base_bg_panel.location_right.setVisible(False)
        self.play_next_location_ani(ScalePlateBaseUI.BOWEN_RIGHT_ANI)
        return

    def cal_cur_angle_pos(self, yaw_world_angle):
        import math
        yaw = yaw_world_angle % (2 * math.pi)
        return yaw

    def center_direction_node_pos(self, yaw, direction):
        self.center_yaw = yaw
        container = self._direct_container
        pos_x = self._get_yaw_position(self.center_yaw)
        container.bar_1.setPosition(pos_x, self.direction_pos_y)

    def _get_yaw_position(self, yaw):
        import math
        x_percent = yaw / (2 * math.pi)
        pos_x = -1.0 * x_percent * self.bar_direction_width
        if pos_x < -0.5 * self.bar_direction_width:
            pos_x += self.bar_direction_width
        return pos_x

    def normalize_yaw_in_2_pi(self, yaw):
        return yaw % (2 * pi)

    def _get_bar_yaw_position(self, yaw):
        x_percent = yaw / (2 * pi)
        pos_x = x_percent * self.bar_direction_width
        return pos_x

    def on_camera_yaw_changed(self, yaw):
        if self.raw_yaw is not None and abs(yaw - self.raw_yaw) < 0.0001 and abs(yaw - self.text_yaw) < 0.0001:
            return
        else:
            old_raw_yaw = self.raw_yaw
            self.raw_yaw = yaw
            yaw = self.cal_cur_angle_pos(yaw)
            move_dir = self.RIGHT_DIRECT if self.raw_yaw > old_raw_yaw else self.LEFT_DIRECT
            self.center_direction_node_pos(yaw, move_dir)
            to_be_del_list = []
            for unit_id, type in six.iteritems(self.scale_mark_ani_order_dict):
                scale_mark_dict = self.last_mark_info.get(unit_id)
                if scale_mark_dict:
                    scale_mark_list = scale_mark_dict['mark_lst']
                    scale_mark = scale_mark_list[0]
                    yaw = self.get_scale_yaw_pos(scale_mark.world_pos)
                    if self.is_yaw_visible(yaw):
                        to_be_del_list.append(unit_id)

            for unit_id in to_be_del_list:
                self.cancel_player_ani_sequence(unit_id)

            self.on_highlight_cur_yaw(yaw)
            return

    def add_map_mark(self, player_id, type, v3d_map_pos, extra_args=None):
        self.update_position()
        wpos = math3d.vector(v3d_map_pos.x, 0, v3d_map_pos.z)
        is_init = False
        if extra_args:
            is_init = extra_args.get('is_init', False)
        self._add_scale_mark(player_id, wpos, type, is_init)

    def get_scale_yaw_pos(self, mark_pos):
        player_pos = self.player_pos
        if not player_pos:
            return 0
        player_pos = math3d.vector(player_pos.x, 0, player_pos.z)
        diff_vec = mark_pos - player_pos
        mark_yaw = diff_vec.yaw
        return self.normalize_yaw_in_2_pi(mark_yaw)

    def _get_or_create_player_scale_mark(self, player_id, mark_type):
        if player_id not in self.scale_mark_dict:
            self.scale_mark_dict[player_id] = {}
        if mark_type not in self.scale_mark_dict[player_id]:
            self.scale_mark_dict[player_id][mark_type] = []
        scale_mark_1 = ScaleMark(self.cur_direction_bar)
        scale_mark_2 = ScaleMark(self.alternate_direction_bar)
        scale_mark_dict = {'mark_lst': [scale_mark_1, scale_mark_2]}
        self.scale_mark_dict[player_id][mark_type].append(scale_mark_dict)
        return scale_mark_dict

    def _del_scale_mark_by_type(self, player_id, mark_type):
        if player_id not in self.scale_mark_dict:
            return
        if mark_type in self.scale_mark_dict[player_id] and self.scale_mark_dict[player_id][mark_type]:
            scale_mark = self.scale_mark_dict[player_id][mark_type].pop(0)
            if scale_mark:
                for mark in scale_mark['mark_lst']:
                    mark and mark.destroy()

            if not self.scale_mark_dict[player_id][mark_type]:
                del self.scale_mark_dict[player_id][mark_type]
        if not self.scale_mark_dict[player_id]:
            del self.scale_mark_dict[player_id]

    def _add_scale_mark(self, player_id, mark_pos, type, is_init):
        scale_mark_dict = self._get_or_create_player_scale_mark(player_id, type)
        if not scale_mark_dict:
            return
        self.last_mark_info[player_id] = scale_mark_dict
        scale_mark_list = scale_mark_dict['mark_lst']
        from mobile.common.EntityManager import EntityManager
        target = EntityManager.getentity(player_id)
        group_ids = target.logic.ev_g_groupmate()
        from logic.gcommon.common_const.battle_const import MAP_COL_BLUE
        if group_ids:
            mark_color = get_teammate_colors(group_ids)[player_id] if 1 else MAP_COL_BLUE
            yaw = self.get_scale_yaw_pos(mark_pos)
            local_pos_x = self._get_bar_yaw_position(yaw)
            nd_mark = self.cur_direction_bar.nd_mark
            for scale_mark in scale_mark_list:
                scale_mark.set_scale_mark(type, mark_color)
                scale_mark.world_pos = mark_pos
                scale_mark.unit_id = player_id
                anchor = scale_mark._nd.getAnchorPoint()
                height = nd_mark.getPosition().y - nd_mark.getContentSize().height * (1 - anchor.y)
                scale_mark.SetPosition(local_pos_x, height)
                if global_data.cam_lplayer and player_id == global_data.cam_lplayer.id:
                    scale_mark._nd.setLocalZOrder(1)
                scale_mark.StopAnimation('bowen')
                scale_mark.set_texiao_vis(False)
                if not is_init:
                    scale_mark.PlayAnimation('bowen')
                    scale_mark.set_texiao_vis(True)
                self._update_each_mark_pos(scale_mark)

            if is_init:
                return
            diff_yaw = self.is_yaw_visible(yaw) or yaw - self.center_yaw
            if diff_yaw < 0:
                diff_yaw += 2 * pi
            if diff_yaw > pi:
                self.add_location_ani(player_id, ScalePlateBaseUI.BOWEN_LEFT_ANI)
            else:
                self.add_location_ani(player_id, ScalePlateBaseUI.BOWEN_RIGHT_ANI)

    def _update_scale_mark_pos(self):
        for unit_id, scale_mark_infos in six.iteritems(self.scale_mark_dict):
            for mark_infos in six.itervalues(scale_mark_infos):
                for mark_dict in mark_infos:
                    mark_list = mark_dict['mark_lst']
                    for mark in mark_list:
                        self._update_each_mark_pos(mark)

    def _update_each_mark_pos(self, mark):
        world_pos = mark.world_pos
        yaw = self.get_scale_yaw_pos(world_pos)
        local_pos_x = self._get_bar_yaw_position(yaw)
        mark._nd.setPositionX(local_pos_x)

    def is_yaw_visible(self, yaw):
        sz = self.panel.sv_direction.GetContentSize()
        bar_sz = self.cur_direction_bar.GetContentSize()
        angle_range = sz[0] / bar_sz[0] * 2 * pi
        half = angle_range / 2.0
        jiajiao = self.normalize_yaw_in_2_pi(yaw - self.center_yaw)
        if jiajiao > pi:
            jiajiao = abs(jiajiao - 2 * pi)
        return jiajiao <= half

    def clear_player_marks(self, unit_id):
        if unit_id in self.scale_mark_dict:
            scale_mark_dict = self.scale_mark_dict[unit_id]
            for mark_list in six.itervalues(scale_mark_dict):
                for mark_dict in mark_list:
                    for scale_mark in mark_dict['mark_lst']:
                        scale_mark.destroy()

            del self.scale_mark_dict[unit_id]

    def add_location_ani(self, unit_id, ani_type):
        self.cancel_player_ani_sequence(unit_id)
        self.scale_mark_ani_order_dict[unit_id] = ani_type
        self.play_next_location_ani(ani_type)

    def play_next_location_ani(self, type):
        is_ok = type == ScalePlateBaseUI.BOWEN_LEFT_ANI and not self.is_location_left_ani_playing or type == ScalePlateBaseUI.BOWEN_RIGHT_ANI and not self.is_location_right_ani_playing
        if not is_ok:
            return
        for unit_id, tmp_type in six.iteritems(self.scale_mark_ani_order_dict):
            if tmp_type == type:
                self.real_play_unit_id_locate_ani(unit_id, type)
                del self.scale_mark_ani_order_dict[unit_id]
                break

    def real_play_unit_id_locate_ani(self, unit_id, type):
        if type == ScalePlateBaseUI.BOWEN_LEFT_ANI:
            self.cur_left_ani_unit_id = unit_id
            if self._base_bg_panel:
                self._base_bg_panel.location_left.setVisible(True)
                self._base_bg_panel.location_left.setOpacity(255)
                self._base_bg_panel.StopAnimation('bowen_left')
                self._base_bg_panel.PlayAnimation('bowen_left')
                self._base_bg_panel.SetTimeOut(self._base_bg_panel.GetAnimationMaxRunTime('bowen_left'), self.OnLeftAnimationCallBack, tag=self.ACTION_TAG_LEFT)
            self.is_location_left_ani_playing = True
        if type == ScalePlateBaseUI.BOWEN_RIGHT_ANI:
            self.cur_right_ani_unit_id = unit_id
            if self._base_bg_panel:
                self._base_bg_panel.location_right.setVisible(True)
                self._base_bg_panel.location_right.setOpacity(255)
                self._base_bg_panel.StopAnimation('bowen_right')
                self._base_bg_panel.PlayAnimation('bowen_right')
                self._base_bg_panel.SetTimeOut(self._base_bg_panel.GetAnimationMaxRunTime('bowen_right'), self.OnRightAnimationCallBack, tag=self.ACTION_TAG_RIGHT)
            self.is_location_right_ani_playing = True

    def cancel_player_ani_sequence(self, unit_id):
        if unit_id in self.scale_mark_ani_order_dict:
            del self.scale_mark_ani_order_dict[unit_id]
        if self.cur_left_ani_unit_id == unit_id:
            self.stop_scale_mark_ani(ScalePlateBaseUI.BOWEN_LEFT_ANI)
            self.cur_left_ani_unit_id = None
            self.play_next_location_ani(ScalePlateBaseUI.BOWEN_LEFT_ANI)
        elif self.cur_right_ani_unit_id == unit_id:
            self.stop_scale_mark_ani(ScalePlateBaseUI.BOWEN_RIGHT_ANI)
            self.cur_right_ani_unit_id = None
            self.play_next_location_ani(ScalePlateBaseUI.BOWEN_RIGHT_ANI)
        return

    def stop_scale_mark_ani(self, type):
        if type == ScalePlateBaseUI.BOWEN_LEFT_ANI:
            if self._base_bg_panel:
                self._base_bg_panel.StopAnimation('bowen_left')
                self._base_bg_panel.stopActionByTag(self.ACTION_TAG_LEFT)
                self._base_bg_panel.location_left.setVisible(False)
            self.is_location_left_ani_playing = False
        else:
            if self._base_bg_panel:
                self._base_bg_panel.StopAnimation('bowen_right')
                self._base_bg_panel.stopActionByTag(self.ACTION_TAG_RIGHT)
                self._base_bg_panel.location_right.setVisible(False)
            self.is_location_right_ani_playing = False

    def set_show_player_ids(self, player_ids, player_color_info, map_marks):
        self.player_color_info = player_color_info
        self.player_ids = player_ids
        self.set_map_marks(map_marks)

    def set_map_marks(self, map_marks):
        self.clear_all_marks()
        self.init_map_marks(map_marks)

    def init_map_marks(self, map_marks):
        if map_marks:
            for tid, mark_dict in six.iteritems(map_marks):
                for mark_type, mark_infos in six.iteritems(mark_dict):
                    for mark_info in mark_infos:
                        pos = mark_info.get('pos')
                        extra_args = mark_info.get('extra_args')
                        self.add_map_mark(tid, mark_type, pos, extra_args)

    def clear_all_marks(self):
        for player_id in six_ex.keys(self.scale_mark_dict):
            self.clear_player_marks(player_id)

        self.scale_mark_dict = {}

    def on_highlight_cur_yaw(self, yaw):
        import math
        if math.isnan(yaw):
            return
        LABEL_NUM = self.LABEL_NUM
        if self._cur_update_index == 0:
            degree = int(yaw * 180 / 3.1415)
            show_degree = str(degree) if degree not in self.LABEL_TEXTS else self.LABEL_TEXTS[degree]
            if self._base_bg_panel:
                self._base_bg_panel.lab_angle.setString(show_degree)
            self.text_yaw = yaw
        else:
            label_index = int(round(yaw * 180 / 3.1415 / ANGLE_PER_LABEL) % LABEL_NUM)
            self.set_angle_label_sel(label_index)
        self._cur_update_index += 1
        if self._cur_update_index > 1:
            self._cur_update_index = 0

    def index_to_label_name(self, label_index):
        return self.direction_bar_label_name_list[label_index]

    def set_angle_label_sel(self, label_index):
        if label_index == self.cur_angle_label_index:
            return
        else:
            if self.cur_angle_label_index is not None:
                label_name = self.index_to_label_name(self.cur_angle_label_index)
                self._set_angle_label_sel_helper(label_name, False)
            self.cur_angle_label_index = label_index
            label_name = self.index_to_label_name(self.cur_angle_label_index)
            self._set_angle_label_sel_helper(label_name, True)
            return

    def _set_angle_label_sel_helper(self, label_name, is_sel):
        bar_list = [self.cur_direction_bar, self.alternate_direction_bar]
        for bar in bar_list:
            lab_ui_item = getattr(bar, 'lab_' + label_name)
            active_ui_item = getattr(bar, 'active_' + label_name)
            if is_sel:
                lab_ui_item.setScale(1.3)
                active_ui_item.setVisible(True)
            else:
                lab_ui_item.setScale(1.0)
                active_ui_item.setVisible(False)

    def set_safe_area_mark_visible(self, is_visible):
        self.cur_direction_bar.nd_mark.setVisible(is_visible)
        self.alternate_direction_bar.nd_mark.setVisible(is_visible)

    def update_safe_area_mark_show(self, dist):
        if self.panel:
            from logic.gcommon.const import NEOX_UNIT_SCALE
            self.cur_direction_bar.nd_safe.tf_safe_area_dist.setString('{:.0f}'.format(dist / NEOX_UNIT_SCALE))
            self.alternate_direction_bar.nd_safe.tf_safe_area_dist.setString(str(int(dist / NEOX_UNIT_SCALE)))

    def _update_safe_area_mark_pos(self):
        if not self.cur_direction_bar.nd_mark.isVisible():
            return
        if self.safe_center:
            yaw = self.get_scale_yaw_pos(math3d.vector(self.safe_center.x, 0, self.safe_center.z))
            local_pos_x = self._get_bar_yaw_position(yaw)
            old_y = self.cur_direction_bar.nd_mark.getPosition().y
            self.cur_direction_bar.nd_mark.SetPosition(local_pos_x, old_y)
            self.alternate_direction_bar.nd_mark.SetPosition(local_pos_x, old_y)

    def tick_yaw(self):
        self.update_yaw()

    def tick_position(self):
        self.update_position()

    def update_yaw(self):
        if not global_data.cam_data:
            return
        yaw = global_data.cam_data.yaw
        if math.isinf(yaw) or math.isnan(yaw):
            return
        self.on_camera_yaw_changed(yaw)

    def update_position(self):
        if not global_data.cam_lctarget:
            return
        cam_lctarget = global_data.cam_lctarget
        pos = cam_lctarget.ev_g_position()
        if pos:
            self.on_player_pos_changed(pos)

    def start_tick(self):
        import cc
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.tick_yaw),
         cc.DelayTime.create(0.033)])))
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.tick_position),
         cc.DelayTime.create(0.5)])))

    def set_safe_center(self, safe_center):
        if safe_center:
            self.safe_center = safe_center
        else:
            self.safe_center = None
        if scene_utils.is_circle_poison():
            self.init_poison_mgr()
        return

    def init_poison_mgr(self):
        import weakref
        part_battle = self.scene.get_com('PartBattle')
        poison_mgr = part_battle.get_poison_manager()
        self.poison_mgr = weakref.ref(poison_mgr)

    def get_map_pos_in_world(self, map_pos):
        part_map = global_data.game_mgr.scene.get_com('PartMap')
        return part_map.get_map_pos_in_world(map_pos)

    def get_world_pos_in_map(self, wpos):
        part_map = global_data.game_mgr.scene.get_com('PartMap')
        return part_map.get_world_pos_in_map(wpos)

    def prepare_all_nds(self):
        self.prepare_label_name_list()
        self._start_lpos_x = self._get_yaw_position(0)
        nds = self.get_all_label_nds(self.cur_direction_bar)
        if self.alternate_direction_bar in nds:
            nds.remove(self.alternate_direction_bar)
        nds_2 = self.get_all_label_nds(self.alternate_direction_bar)
        nds.sort(key=lambda nd: nd.getPosition().x)
        _nds_pos_x = [ nd.getPosition().x - self.bar_direction_width for nd in nds ]
        nds_2.sort(key=lambda nd: nd.getPosition().x)
        _nds_2_pos_x = [ nd.getPosition().x for nd in nds_2 ]
        self._zero_nd_index = len(_nds_pos_x)
        _nds_pos_x.extend(_nds_2_pos_x)
        nds.extend(nds_2)
        self._sorted_nds = nds
        for nd in self._sorted_nds:
            nd.SetEnableCascadeOpacityRecursion(True)

        self._sorted_nds_pos_x = _nds_pos_x
        min_wpos = -(self.direction_width / 2) + ScalePlateBaseUI.OPACITY_EDGE
        max_wpos = self.direction_width / 2 - ScalePlateBaseUI.OPACITY_EDGE
        self._edge_min_lpos_x = min_wpos
        self._edge_max_lpos_x = max_wpos
        self._label_width = max(float(self.bar_direction_width) / self.LABEL_NUM, 1)

    def get_all_label_nds(self, bar):
        LABEL_NUM = self.LABEL_NUM
        label_indexes = list(range(LABEL_NUM))
        label_names = [ self.index_to_label_name(idx) for idx in label_indexes ]
        nds = [ getattr(bar, lname) for lname in label_names ]
        if None in nds:
            log_error("Can't find one of the label names %s in scale plate bar" % str(label_names))
            nds.remove(None)
        return nds

    def update_safe_area_visibility(self):
        if not self.poison_mgr:
            return
        poison_mgr = self.poison_mgr()
        if not poison_mgr:
            return
        cnt_circle_data = poison_mgr.get_cnt_circle_info()
        position = self.player_pos
        if cnt_circle_data.get('level', 0) == 0 or not position:
            self.set_safe_area_mark_visible(False)
            return
        safe_center = cnt_circle_data['safe_center']
        safe_center = math3d.vector(safe_center.x, 0.0, safe_center.z)
        position = math3d.vector(position.x, 0.0, position.z)
        c_p_direction = safe_center - position
        c_p_length = c_p_direction.length
        distance = c_p_length - cnt_circle_data['safe_radius']
        if distance < 0:
            self.set_safe_area_mark_visible(False)
        else:
            self.set_safe_area_mark_visible(True)
            self._update_safe_area_mark_pos()
        global_data.emgr.distance_to_safecricle.emit(distance)

    def prepare_label_name_list(self):
        self.direction_bar_label_name_list = []
        index_to_label_name_map = {0: 'n',
           3: 'ne',
           6: 'e',
           9: 'se',
           12: 's',
           15: 'sw',
           18: 'w',
           21: 'nw'
           }
        for label_index in range(0, self.LABEL_NUM):
            label_name = index_to_label_name_map.get(label_index, str(label_index * ANGLE_PER_LABEL))
            self.direction_bar_label_name_list.append(label_name)

    def set_opacity_shader(self):
        import cc
        from logic.comsys.effect.ui_effect import create_shader
        gl_swap_rgb = create_shader('labelnormal_opacity', 'labelnormal_opacity')
        program_swap_rgb = cc.GLProgramState.getOrCreateWithGLProgram(gl_swap_rgb)
        bar_list = [self.cur_direction_bar, self.alternate_direction_bar]
        for bar in bar_list:
            for label_name in self.direction_bar_label_name_list:
                lab_ui_item = getattr(bar, 'lab_' + label_name)
                lab_ui_item.getVirtualRenderer().setGLProgramState(program_swap_rgb)


class ScalePlateUI(ScalePlateBaseUI):
    PANEL_CONFIG_NAME = 'map/fight_angle'