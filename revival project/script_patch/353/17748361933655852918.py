# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/TeammateWidget/TeammateLocateUI.py
from __future__ import absolute_import
import six
import weakref
from common.framework import Functor
from common.utils.cocos_utils import getScreenSize
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.battle_const import LOCATE_RECOURSE, LOCATE_DEAD, TEAMMATE_LOCATE_UI
from .TeammateWidget import TeammateBloodBarUI, TeammateStatusUI, TeammateFullStatusUI
from common.utils.ui_utils import get_scale
from logic.gutils.team_utils import get_team_bottom_pic_path, get_team_knock_down_pic_path, get_color_hint_pic, get_team_dead_pic_path
from logic.gutils.item_utils import get_locate_circle_path
from logic.gutils.custom_ui_utils import get_cut_name
import time
import cc
import math3d
import math
import world
from logic.client.const.game_mode_const import GAME_MODE_EXERCISE
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
from logic.comsys.common_ui import CommonInfoUtils
from logic.client.const import game_mode_const
IGNORE_CONTROL_TARGET_CHANGE_ENTITIES = frozenset(['TVMissile'])

class TeammateLocateUI(object):
    DISTANCE_APPEAR_LENGTH = 20 * NEOX_UNIT_SCALE
    screen_size = getScreenSize()
    screen_angle_limit = math.atan(getScreenSize().height / 2.0 / (getScreenSize().width / 2.0)) * 180 / math.pi
    MODEL_HEIGHT = 1.9 * NEOX_UNIT_SCALE
    SCREEN_MARGIN = get_scale('40w')
    BIND_POINT = {'LAvatar': 's_xuetiao',
       'LPuppet': 's_xuetiao',
       'LMechaTrans': 'xuetiao',
       'LMotorcycle': {0: 'xuetiao_seat_1',1: 'xuetiao_seat_2',2: 'xuetiao_seat_3'}}

    def __init__(self, color, player_num, panel):
        self.panel = panel
        self._hide_reason_set = set()
        self._space_node = CCUISpaceNode.Create()
        self._nd = CommonInfoUtils.create_ui(TEAMMATE_LOCATE_UI, self._space_node, False, False)
        if self._nd.title.nd_title:
            self._nd.title.nd_title.setVisible(False)
        self.simple_status_ui = TeammateStatusUI(self._nd.nd_simple.locate, color, player_num)
        self.full_status_ui = TeammateFullStatusUI(self._nd.nd_full.locate.bar_locate, color)
        self._nd.nd_num.SetDisplayFrameByPath('', get_team_bottom_pic_path(color))
        self._color = color
        self._max_hp = 0
        self._binded_events = {}
        self._info = {}
        self._teammate = None
        self._teammate_control_target = None
        self.nd_type = None
        self.last_status_type = None
        self._nd.setPosition(0, 0)
        self._nd.SetEnableCascadeOpacityRecursion(True)
        self._nd.locate.SetEnableCascadeOpacityRecursion(True)
        self._is_full_state = False
        self.process_event(True)
        self._nd.RecordAnimationNodeState('dying')
        self._nd.setPosition(0, 0)
        self._binded_model = None
        self._binded_socket = None
        horizontal_margin = 140 * self.panel.getScale()
        vertical_margin = 80 * self.panel.getScale()
        top_margin = self.SCREEN_MARGIN
        self._space_node.set_enable_limit_in_screen(True, horizontal_margin, horizontal_margin, top_margin, vertical_margin)
        self._space_node.set_screen_check_margin(0, 0, top_margin, 0)
        self.pos_offset = math3d.vector(0, 0, 0)
        self._is_in_mecha = False
        self._ctrl_type = None
        self._last_distance_update_time = 0
        if self.panel.isVisible():
            self.show()
        else:
            self.hide()
        self.is_in_exercise = global_data.game_mode.is_mode_type(GAME_MODE_EXERCISE)
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_DEATHS):
            if global_data.aim_transparent_mgr:
                global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__, [self._nd])
        return

    def process_event(self, is_bind):
        if is_bind:
            global_data.emgr.teammate_control_target_change_event += self.on_teammate_ctrl_target_changed
            global_data.emgr.add_battle_group_msg_event += self.on_battle_group_msg
        else:
            global_data.emgr.teammate_control_target_change_event -= self.on_teammate_ctrl_target_changed
            global_data.emgr.add_battle_group_msg_event -= self.on_battle_group_msg

    def init_by_teammate_info(self, info):
        self._info = info
        self.set_teammate_name(self.get_teammate_name(), self._color)
        if self.simple_status_ui:
            self.simple_status_ui.init_by_teammate_dict(info)
        if self.full_status_ui:
            self.full_status_ui.init_by_teammate_dict(info)

    def set_teammate(self, teammate):
        if teammate:
            self._teammate = weakref.ref(teammate)
            self._is_in_mecha = teammate.ev_g_in_mecha()
            control_target = teammate.ev_g_control_target()
            if control_target and control_target.logic:
                self._teammate_control_target = weakref.ref(control_target.logic)
            self.set_teammate_name(self.get_teammate_name(), self._color)
        else:
            self._teammate = None
            self._is_in_mecha = False
        return

    def get_teammate_name(self):
        teammate = self.get_teammate_ent()
        if teammate:
            return teammate.ev_g_char_name()
        else:
            return self._info.get('char_name', '')

    def get_teammate_pos(self):
        mate_ctrl_target = self.get_control_target_ent()
        if not mate_ctrl_target:
            pos = self._info.get('pos')
            if pos:
                return math3d.vector(*pos)
        else:
            return mate_ctrl_target.ev_g_model_position()
        return None

    def get_teammate_control_target_model(self):
        mate_ctrl_target = self.get_control_target_ent()
        if not mate_ctrl_target:
            return (None, None)
        else:
            return (
             mate_ctrl_target.__class__.__name__, mate_ctrl_target.ev_g_model())
            return None

    def update_teammate(self):
        teammate = self.get_teammate_ent()
        if not teammate:
            return
        self.update_status(teammate)
        if not self._space_node:
            return
        is_in_screen = self._space_node.get_is_in_screen()
        self.check_transparent(is_in_screen)

    def update_nd_pos(self, cam, lplayer, lplayer_pos):
        ctarget_type, ctarget_model = self.get_teammate_control_target_model()
        if not lplayer_pos:
            return False
        else:
            if not ctarget_model:
                position = self.get_teammate_pos()
                if position:
                    if self._space_node:
                        self._space_node.set_assigned_world_pos(position)
                        self.pos_offset.y = self.MODEL_HEIGHT
                        self._space_node.set_pos_offset(self.pos_offset)
                    self.calc_nd_pos(cam, position, lplayer_pos)
                    return True
                return False
            position = ctarget_model.world_position
            if position is None:
                self._nd.setVisible(False)
                return True
            if ctarget_model.visible and not self._hide_reason_set:
                self.show()
            else:
                self.hide()
            bind_point = self.get_bind_point(ctarget_type)
            bind_point_offset = -3 if global_data.cam_lplayer == lplayer else 0
            self.pos_offset.y = bind_point_offset if bind_point else self.MODEL_HEIGHT * 3
            self.try_bind_model(ctarget_model, self.pos_offset, bind_point)
            self.calc_nd_pos(cam, position, lplayer_pos)
            return True
            return

    def get_bind_point(self, ctarget_type):
        bind_point = self.BIND_POINT.get(ctarget_type)
        if isinstance(bind_point, dict):
            mate_ctrl_target = self.get_control_target_ent()
            teammate = self.get_teammate_ent()
            if mate_ctrl_target and teammate:
                seat_index = mate_ctrl_target.ev_g_passenger_seat_index(teammate.id)
                seat_index = seat_index or 0
                return bind_point.get(seat_index, bind_point[0])
            else:
                return bind_point[0]

        else:
            return bind_point

    def get_control_target_pos(self, lentity):
        if lentity:
            con_target = lentity.ev_g_control_target()
            if con_target and con_target.logic:
                return

    def calc_nd_pos(self, cam, position, lplayer_pos):
        nd = self._nd
        if not self._space_node:
            return
        is_in_screen = self._space_node.get_is_in_screen()
        if is_in_screen:
            self.switch_full_or_simple_status(True)
        else:
            cam_lpos = cam.world_to_camera(position)
            self.switch_full_or_simple_status(False)
            angle = math.atan2(cam_lpos.y, cam_lpos.x)
            angle = angle * 180 / math.pi
            if angle < 0:
                angle += 360
            nd.nd_simple.locate.dir.setRotation(-(angle - 90))
        cur_time = time.time()
        if cur_time - self._last_distance_update_time > 1.0:
            dist = self.update_teammate_dist(nd, position, lplayer_pos, is_in_screen)
            self._last_distance_update_time = cur_time

    def try_bind_model(self, interact_model, pos_offset, socket=None):
        if not self._binded_model or self._binded_model() != interact_model or self._binded_socket != socket:
            space_node = self._space_node
            if not space_node:
                return
            if socket:
                space_node.bind_model(interact_model, socket)
                space_node.set_fix_xz(False)
            else:
                space_node.bind_space_object(interact_model)
            self._binded_model = weakref.ref(interact_model)
            self._binded_socket = socket
            if pos_offset:
                space_node.set_pos_offset(pos_offset)

    def reset_pos_offset(self):
        if self._space_node:
            self.pos_offset.y = 10
            self._space_node.set_pos_offset(self.pos_offset)

    def check_transparent(self, is_in_screen):
        if self._nd.getOpacity() == 60:
            return
        if not is_in_screen:
            self._nd.setOpacity(255)
        ui_list = [
         'SmallMapUI', 'TeamBloodUI', 'JudgeTeamBloodUI']
        node_list = ['abandon_teammate_name', 'nd_shield_teammate', 'nd_shield_teammate']
        vis_list = [False, True, True]
        wpos = self._nd.locate.ConvertToWorldSpacePercentage(50, 50)
        for idx, ui_name in enumerate(ui_list):
            ui_inst = global_data.ui_mgr.get_ui(ui_name)
            if ui_inst:
                node = getattr(ui_inst.panel, node_list[idx])
                if node.IsPointIn(wpos):
                    self._nd.setOpacity(127)
                    if self._nd.isVisible() != vis_list[idx]:
                        self._nd.setVisible(vis_list[idx])
                    break
        else:
            self._nd.setOpacity(255)

        if not self._nd.isVisible():
            self._nd.setVisible(True)

    def _cal_player_dist(self, mate_pos, lplayer_pos):
        return (lplayer_pos - mate_pos).length

    def update_teammate_dist(self, nd, pos, lplayer_pos, is_in_screen):
        dist = self._cal_player_dist(pos, lplayer_pos)
        if dist > 100000000.0:
            log_error('TeammateUI got an unexpected length, The teammate pos:%s', str(pos))
            return dist
        if dist > TeammateLocateUI.DISTANCE_APPEAR_LENGTH:
            nd.distance.setVisible(True)
            nd.distance.setString(str(int(dist / NEOX_UNIT_SCALE)) + 'm')
        else:
            nd.distance.setVisible(False)
        return dist

    def set_teammate_name(self, teammate_name, color):
        nd_name = self._nd.nd_details.name
        name = teammate_name
        name = six.text_type(name)
        cut_name = get_cut_name(name, 10)
        nd_name.SetString(cut_name)

    def update_health(self, teammate):
        if not self._is_full_state:
            pass

    def update_status(self, teammate):
        if not self._is_full_state:
            if self.simple_status_ui:
                status = self.simple_status_ui.update_status(teammate)
        elif self.full_status_ui:
            status = self.full_status_ui.update_status(teammate)
        self.update_dying(status)

    def set_hurt_visible(self, visible):
        if visible:
            self._nd.StopAnimation('hurt')
            self._nd.PlayAnimation('hurt')
            if self.full_status_ui:
                self.full_status_ui.set_nd_normal_visible(True)
            tag = 11002
            self._nd.SetTimeOut(3.0, Functor(self.set_hurt_visible, False), tag=tag)
        elif self.full_status_ui:
            self.full_status_ui.set_nd_normal_visible(False)

    def update_dying(self, new_type):
        if self.last_status_type != new_type:
            if new_type == LOCATE_RECOURSE:
                pic_path = get_team_knock_down_pic_path(self._color)
                self._nd.nd_num.SetDisplayFrameByPath('', pic_path)
                self._nd.nd_simple.locate.hp_progress.SetDisplayFrameByPath('', pic_path)
                self._nd.nd_simple.locate.lab_num.setVisible(False)
                self._nd.PlayAnimation('dying')
                self.full_status_ui and self.full_status_ui.set_nd_normal_visible(True)
            elif new_type == LOCATE_DEAD:
                pic_path = get_team_dead_pic_path(self._color)
                self._nd.nd_num.SetDisplayFrameByPath('', pic_path)
                self._nd.nd_simple.locate.hp_progress.SetDisplayFrameByPath('', pic_path)
                self._nd.nd_simple.locate.lab_num.setVisible(False)
                if self._nd.img_warn.isVisible():
                    self._nd.StopAnimation('dying')
                    self._nd.RecoverAnimationNodeState('dying')
            else:
                pic_path = get_team_bottom_pic_path(self._color)
                self._nd.nd_num.SetDisplayFrameByPath('', pic_path)
                pic_path = get_locate_circle_path(self._color)
                self._nd.nd_simple.locate.hp_progress.SetDisplayFrameByPath('', pic_path)
                self._nd.nd_simple.locate.lab_num.setVisible(True)
                if self._nd.img_warn.isVisible():
                    self._nd.StopAnimation('dying')
                    self._nd.RecoverAnimationNodeState('dying')
                    self.full_status_ui and self.full_status_ui.set_nd_normal_visible(False)
        self.last_status_type = new_type

    def on_teammate_hurted(self):
        self.set_hurt_visible(True)

    def destroy(self):
        self._hide_reason_set = set()
        CommonInfoUtils.destroy_ui(self._nd)
        self._nd = None
        if self._space_node:
            self._space_node.Destroy()
        self._space_node = None
        self.process_event(False)
        if self.simple_status_ui:
            self.simple_status_ui.destroy()
            self.simple_status_ui = None
        if self.full_status_ui:
            self.full_status_ui.destroy()
            self.full_status_ui = None
        return

    def get_teammate_ent(self):
        return self.get_weak_target_ent(self._teammate)

    def get_control_target_ent(self):
        return self.get_weak_target_ent(self._teammate_control_target)

    def get_weak_target_ent(self, ent_weak_ref):
        if ent_weak_ref:
            t = ent_weak_ref()
            if t and t.is_valid():
                return t
            return None
        else:
            return None
            return None

    def switch_full_or_simple_status(self, is_full):
        if is_full:
            self._nd.nd_full.setVisible(True)
            self._nd.nd_simple.setVisible(False)
            wpos = self._nd.nd_num.getParent().convertToWorldSpace(self._nd.nd_num.getPosition())
            lpos = self._nd.nd_vx.getParent().convertToNodeSpace(wpos)
            self._nd.nd_vx.setPosition(lpos)
        elif not self.is_in_exercise:
            self._nd.nd_full.setVisible(False)
            self._nd.nd_simple.setVisible(True)
            self._nd.PlayAnimation('out_win')
        else:
            self._nd.nd_full.setVisible(False)
            self._nd.nd_simple.setVisible(False)
            self._nd.PlayAnimation('out_win')
        if is_full != self._is_full_state:
            self.update_teammate()
        self._is_full_state = is_full

    def on_teammate_ctrl_target_changed(self, teammate_id, target_id, pos):
        teammate_ent = self.get_teammate_ent()
        if teammate_ent and teammate_ent.id == teammate_id:
            self._is_in_mecha = teammate_ent.ev_g_in_mecha()
            from mobile.common.EntityManager import EntityManager
            target = EntityManager.getentity(target_id)
            if target.__class__.__name__ in IGNORE_CONTROL_TARGET_CHANGE_ENTITIES:
                return
            if target and target.logic:
                self._teammate_control_target = weakref.ref(target.logic)

    def hide(self):
        if self._space_node:
            self._space_node.setVisible(False and self.panel.isVisible())

    def show(self):
        if self._space_node:
            self._space_node.setVisible(True and self.panel.isVisible())

    def on_battle_group_msg(self, unit_id, char_name, data):
        if not self.get_teammate_ent():
            return
        dmsg = data.get('msg', {})
        if self.get_teammate_ent().id != unit_id:
            return
        if 'sos_type' not in dmsg:
            return
        path = get_color_hint_pic(self._color, dmsg)
        self._nd.img_help.SetDisplayFrameByPath('', path)
        self._nd.vx_help.SetDisplayFrameByPath('', path)
        self._nd.StopAnimation('help')
        self._nd.PlayAnimation('help')

    def check_title(self, rank_use_title_dict):
        if not rank_use_title_dict:
            if self._nd.title.nd_title:
                self._nd.title.nd_title.setVisible(False)
                return
        if not self._nd.title.nd_title:
            global_data.uisystem.load_template_create('title/i_title_normal_2', parent=self._nd.title, name='nd_title')
        if self._nd.title.nd_title:
            self._nd.title.nd_title.setVisible(True)
            from logic.gutils import template_utils
            from logic.gcommon.common_const import rank_const
            title_type = rank_const.get_rank_use_title_type(rank_use_title_dict)
            rank_info = rank_const.get_rank_use_title(rank_use_title_dict)
            template_utils.init_rank_title(self._nd.title.nd_title, title_type, rank_info, icon_scale=0.85)

    def add_hide_reason_set(self, reason):
        self._hide_reason_set.add(reason)

    def remove_hide_reason_set(self, reason):
        if reason in self._hide_reason_set:
            self._hide_reason_set.remove(reason)