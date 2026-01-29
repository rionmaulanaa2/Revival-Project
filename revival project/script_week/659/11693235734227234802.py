# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Hunting/EntityLocateUI.py
from __future__ import absolute_import
import six
import weakref
from common.framework import Functor
from common.utils.cocos_utils import getScreenSize
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.battle_const import LOCATE_RECOURSE, LOCATE_DEAD, TEAMMATE_LOCATE_UI
from common.utils.ui_utils import get_scale
from logic.gutils.team_utils import get_team_bottom_pic_path, get_team_knock_down_pic_path, get_color_hint_pic, get_team_dead_pic_path
from logic.gutils.custom_ui_utils import get_cut_name
import time
import cc
import math3d
import math
import world
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
from logic.comsys.common_ui import CommonInfoUtils
IGNORE_CONTROL_TARGET_CHANGE_ENTITIES = frozenset(['TVMissile'])

class EntityLocateUI(object):
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
        self._nd.nd_num.SetDisplayFrameByPath('', get_team_bottom_pic_path(color))
        self._nd.distance.setVisible(False)
        self._color = color
        self._binded_events = {}
        self._info = {}
        self._teammate = None
        self._teammate_control_target = None
        self._nd.setPosition(0, 0)
        self._nd.SetEnableCascadeOpacityRecursion(True)
        self._nd.locate.SetEnableCascadeOpacityRecursion(True)
        self.process_event(True)
        self._nd.setPosition(0, 0)
        self._binded_model = None
        self._binded_socket = None
        top_margin = self.SCREEN_MARGIN
        self._space_node.set_screen_check_margin(0, 0, top_margin, 0)

        def vis_callback(last_need_draw, cur_need_draw):
            if self._nd and self._nd.isValid():
                self._nd.setVisible(True if cur_need_draw else False)

        self._space_node.set_visible_callback(vis_callback)
        self.pos_offset = math3d.vector(0, 0, 0)
        self._is_in_mecha = False
        if self.panel.isVisible():
            self.show()
        else:
            self.hide()
        return

    def process_event(self, is_bind):
        if is_bind:
            global_data.emgr.common_control_target_change_event += self.on_teammate_ctrl_target_changed
        else:
            global_data.emgr.common_control_target_change_event -= self.on_teammate_ctrl_target_changed

    def init_by_teammate_info(self, info):
        self._info = info
        self.set_teammate_name(self.get_teammate_name(), self._color)

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

    def on_teammate_ctrl_target_changed(self, teammate_id, target_id, *args):
        teammate_ent = self.get_teammate_ent()
        if teammate_ent and teammate_ent.id == teammate_id:
            self._is_in_mecha = teammate_ent.ev_g_in_mecha()
            from mobile.common.EntityManager import EntityManager
            target = EntityManager.getentity(target_id)
            if target.__class__.__name__ in IGNORE_CONTROL_TARGET_CHANGE_ENTITIES:
                return
            if target and target.logic:
                self._teammate_control_target = weakref.ref(target.logic)

    def get_teammate_name(self):
        teammate = self.get_teammate_ent()
        if teammate:
            return teammate.ev_g_char_name()
        else:
            return self._info.get('char_name', '')

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

    def get_teammate_control_target_model(self):
        mate_ctrl_target = self.get_control_target_ent()
        if not mate_ctrl_target:
            return (None, None)
        else:
            return (
             mate_ctrl_target.__class__.__name__, mate_ctrl_target.ev_g_model())
            return None

    def get_teammate_pos(self):
        mate_ctrl_target = self.get_control_target_ent()
        if not mate_ctrl_target:
            pos = self._info.get('pos')
            if pos:
                return math3d.vector(*pos)
        else:
            return mate_ctrl_target.ev_g_model_position()
        return None

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
                    return True
                self.hide()
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
            return True
            return

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

    def set_teammate_name(self, teammate_name, color):
        nd_name = self._nd.nd_details.name
        name = teammate_name
        name = six.text_type(name)
        cut_name = get_cut_name(name, 10)
        nd_name.SetString(cut_name)

    def destroy(self):
        self._hide_reason_set = set()
        CommonInfoUtils.destroy_ui(self._nd)
        self._nd = None
        if self._space_node:
            self._space_node.Destroy()
        self._space_node = None
        self.process_event(False)
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

    def hide(self):
        if self._space_node:
            self._space_node.setVisible(False and self.panel.isVisible())

    def show(self):
        if self._space_node:
            self._space_node.setVisible(True and self.panel.isVisible())

    def add_hide_reason_set(self, reason):
        self._hide_reason_set.add(reason)

    def remove_hide_reason_set(self, reason):
        if reason in self._hide_reason_set:
            self._hide_reason_set.remove(reason)