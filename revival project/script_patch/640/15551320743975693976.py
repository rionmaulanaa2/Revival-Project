# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/QuickMarkUIPC.py
from __future__ import absolute_import
import six
from .QuickMarkUI import QuickMarkUI
from common.utils.cocos_utils import ccp
import cc
import math
from logic.gcommon.common_const.battle_const import MARK_NORMAL, MARK_GOTO, MARK_DANGER, MARK_RES, MARK_NONE, MARK_GATHER, MARK_WAY_QUICK
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.battle_const import MARK_NORMAL, MARK_GOTO, MARK_DANGER, MARK_RES, MARK_NONE, MARK_GATHER, MARK_WAY_QUICK
MARK_TYPE_TEXT_ID_DICT = {MARK_NONE: -1,
   MARK_GOTO: 16008,
   MARK_DANGER: 80390,
   MARK_RES: 80511,
   MARK_GATHER: 80681
   }

class QuickMarkUIPC(QuickMarkUI):
    PANEL_CONFIG_NAME = 'map/mark_quick_pc'
    HOT_KEY_FUNC_MAP = {'close_wheel_panel': 'mouse_close_wheel_panel'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'switch_scene_mark': {'node': 'nd_hint.nd_hint_1.temp_pc'},'close_wheel_panel': {'node': 'nd_hint.nd_hint_2.temp_pc'}}

    def on_init_panel(self, *args, **kwargs):
        super(QuickMarkUIPC, self).on_init_panel(*args, **kwargs)
        self._mouse_listener = None
        pos_x, pos_y = self.panel.nd_choose_mark.GetPosition()
        self._wheel_center = self.panel.ConvertToWorldSpace(pos_x, pos_y)
        self._last_delta_vec = None
        self._register_mouse_event()
        self.init_tips()
        return

    def _register_mouse_event(self):
        if self._mouse_listener:
            return
        self._mouse_listener = cc.EventListenerMouse.create()
        self._mouse_listener.setOnMouseMoveCallback(self._on_mouse_move)
        cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(self._mouse_listener, self.panel.get())

    def _on_mouse_move(self, event):
        from common.utils.cocos_utils import neox_pos_to_cocos
        wpos = event.getLocationInView()
        wpos = cc.Vec2(*neox_pos_to_cocos(wpos.x, wpos.y))
        delta_vec = ccp(wpos.x - self._wheel_center.x, wpos.y - self._wheel_center.y)
        if delta_vec.length() > 0:
            if delta_vec != self._last_delta_vec:
                self._last_delta_vec = delta_vec
                delta_vec.normalize()
                angle = math.degrees(math.atan2(delta_vec.x, delta_vec.y))
                self.panel.nd_select.setRotation(angle)
        self.update_tips()

    def _unregister_mouse_event(self):
        if self._mouse_listener:
            cc.Director.getInstance().getEventDispatcher().removeEventListener(self._mouse_listener)
            self._mouse_listener = None
        return

    def on_finalize_panel(self):
        super(QuickMarkUIPC, self).on_finalize_panel()
        self._unregister_mouse_event()

    def init_parameters(self, **kwargs):
        self.is_mid_map_mark = False
        self.is_active = False
        self.cur_sel_mark_btn = None
        self.mark_btn_type_dict = {MARK_GOTO: self.panel.btn_goto,
           MARK_DANGER: self.panel.btn_danger,
           MARK_RES: self.panel.btn_resource,
           MARK_GATHER: self.panel.btn_gather_sel
           }
        self.update_mark_btn_pos()
        self.mark_dir_dict = {MARK_GOTO: cc.Vec2(0, 1),
           MARK_DANGER: cc.Vec2(1, 0),
           MARK_RES: cc.Vec2(-1, 0),
           MARK_GATHER: cc.Vec2(0, -1)
           }
        return

    def get_cur_sel_mark_type(self, wpos):
        mark_type = MARK_NONE
        if self.panel.bar_center.IsPointIn(wpos):
            mark_type = MARK_NONE
        else:
            min_angle = 10000000
            wpos.subtract(self._wheel_center)
            for k, v in six.iteritems(self.mark_dir_dict):
                cur_angle = math.fabs(wpos.getAngle(v))
                if cur_angle < min_angle:
                    mark_type = k
                    min_angle = cur_angle

        return mark_type

    def mouse_close_wheel_panel(self, *args):
        self.close()

    def init_tips(self):
        tip_1 = self.panel.nd_hint.nd_hint_1.temp_pc.pc_tip_list.GetItem(0)
        tip_2 = self.panel.nd_hint.nd_hint_2.temp_pc.pc_tip_list.GetItem(0)
        if tip_1:
            tip_1.lab_hint1.SetString(get_text_by_id(920823))
            tip_1.lab_hint2.SetString(get_text_by_id(80137))
            tip_1.lab_pc.setVisible(True)
            tip_1.lab_pc.nd_auto_fit.setVisible(False)
            tip_1.lab_pc.SetString('')
        if tip_2:
            tip_2.lab_hint1.SetString(get_text_by_id(920824))
            tip_2.lab_hint2.SetString(get_text_by_id(80137))
            tip_2.lab_pc.setVisible(True)
            tip_2.lab_pc.nd_auto_fit.setVisible(False)
            tip_2.lab_pc.SetString('')

    def set_select(self, mark_type):
        super(QuickMarkUIPC, self).set_select(mark_type)
        cur_text_id = MARK_TYPE_TEXT_ID_DICT.get(mark_type, -1)
        if cur_text_id == -1:
            self.panel.lab_item.SetString('')
        else:
            self.panel.lab_item.SetString(get_text_by_id(cur_text_id))

    def update_tips(self):
        tip_1 = self.panel.nd_hint.nd_hint_1.temp_pc.pc_tip_list.GetItem(0)
        tip_2 = self.panel.nd_hint.nd_hint_2.temp_pc.pc_tip_list.GetItem(0)
        if tip_1:
            tip_1.lab_pc.setVisible(True)
            tip_1.lab_hint2.SetString(get_text_by_id(80137))
            tip_1.lab_pc.nd_auto_fit.setVisible(False)
            tip_1.lab_pc.SetString('')
        if tip_2:
            tip_2.lab_pc.setVisible(True)
            tip_2.lab_hint2.SetString(get_text_by_id(80595))
            tip_2.lab_pc.nd_auto_fit.setVisible(False)
            tip_2.lab_pc.SetString('')

    def on_hot_key_closed_state(self):
        pass