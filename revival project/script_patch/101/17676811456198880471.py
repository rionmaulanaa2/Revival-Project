# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/AimTransparentManager.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
from logic.gcommon.item import item_const
from logic.gcommon.common_const.buff_const import COMMON_BUFF
from logic.gcommon.item import item_utility as iutil
from common.uisys.BaseUIWidget import BaseUIWidget
import cc
import math
from logic.gutils.client_unit_tag_utils import preregistered_tags
from logic.gutils.team_utils import limit_pos_in_screen
from common.utils.cocos_utils import neox_pos_to_cocos
from common.framework import Singleton
from data.camera_state_const import AIM_MODE
from common.utils.timer import CLOCK

class AimTransparentManager(Singleton):
    ALIAS_NAME = 'aim_transparent_mgr'

    def init(self):
        self._model_gun_no = 10046
        self._target_nodes_dict = {}
        self._frame_center = cc.Vec2(0, 0)
        self._frame_size = cc.Size(0, 0)
        self._timer = 0
        self.events_binded = False
        self.old_yaw = 0
        self.old_pitch = 0
        self.cal_frame_size()
        self.process_event(True)

    def process_event(self, flag):
        emgr = global_data.emgr
        e_conf = {'resolution_changed': self.on_resolution_changed,
           'net_login_reconnect_event': self.on_net_reconnect,
           'net_reconnect_event': self.on_net_reconnect
           }
        if flag == self.events_binded:
            return
        self.events_binded = flag
        if flag:
            emgr.bind_events(e_conf)
        else:
            emgr.unbind_events(e_conf)

    def on_resolution_changed(self):
        self.cal_frame_size()

    def cal_frame_size(self):
        sz = global_data.ui_mgr.design_screen_size
        width = sz.width
        height = sz.height
        from common.cfg import confmgr
        from logic.client.const.camera_const import THIRD_PERSON_MODEL, POSTURE_STAND
        x_fov = confmgr.get('camera_config', THIRD_PERSON_MODEL, POSTURE_STAND, 'fov', default=80)
        d = width / 2.0 / math.tan(math.radians(x_fov / 2.0))
        cell = 30
        y_fov = math.atan(cell / 2.0 / d) * 180 / math.pi * 2.0
        pixel_scale_value = cell / y_fov
        fAutoAimPitch = confmgr.get('firearm_config', str(self._model_gun_no), 'fAutoAimPitch', default=1.0)
        fAutoAimYaw = confmgr.get('firearm_config', str(self._model_gun_no), 'fAutoAimYaw', default=1.0)
        scale = 1.1
        self._frame_center = cc.Vec2(width / 2.0, height / 2.0)
        self._frame_size = cc.Size(fAutoAimYaw * 2 * pixel_scale_value * scale, fAutoAimPitch * 2 * pixel_scale_value * scale)

    def add_target_node(self, ui_name, node_list):
        self._target_nodes_dict.setdefault(ui_name, set())
        for n in node_list:
            n.SetEnableCascadeOpacityRecursion(True)
            self._target_nodes_dict[ui_name].add(n)

        if not self._timer:
            if any(six.itervalues(self._target_nodes_dict)):
                self.register_check_timer()

    def remove_target_node(self, ui_name, node_list):
        if ui_name not in self._target_nodes_dict:
            return
        for n in node_list:
            if n in self._target_nodes_dict[ui_name]:
                self._target_nodes_dict[ui_name].remove(n)

        if self._timer:
            if not any(six.itervalues(self._target_nodes_dict)):
                self.unregister_check_timer()

    def check_node_in_frames(self):
        if abs(global_data.cam_data.yaw - self.old_yaw) < 0.01 and abs(global_data.cam_data.pitch - self.old_pitch) < 0.01:
            return
        self.old_yaw = global_data.cam_data.yaw
        self.old_pitch = global_data.cam_data.pitch
        remove_nodes_dict = {}
        for ui_name, node_list in six.iteritems(self._target_nodes_dict):
            remove_nodes = []
            for node in node_list:
                if not (node and node.isValid()):
                    remove_nodes.append(node)
                    continue
                if not node.getParent():
                    continue
                pos = node.getParent().convertToWorldSpace(node.getPosition())
                if AimTransparentManager.get_is_in_aim() or abs(pos.x - self._frame_center.x) < self._frame_size.width / 2.0 and abs(pos.y - self._frame_center.y) < self._frame_size.height / 2.0:
                    node.setOpacity(60)
                else:
                    node.setOpacity(255)

            remove_nodes_dict[ui_name] = remove_nodes

        for ui_name, node_list in six.iteritems(remove_nodes_dict):
            self.remove_target_node(ui_name, node_list)

    def on_finalize(self):
        self._target_nodes_dict = []
        self.unregister_check_timer()
        self.process_event(False)

    def register_check_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_check_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.check_node_in_frames, interval=0.5, mode=CLOCK, times=-1)

    def unregister_check_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def on_net_reconnect(self, *args):
        self.unregister_check_timer()
        if any(six.itervalues(self._target_nodes_dict)):
            self.register_check_timer()

    @staticmethod
    def get_is_in_aim():
        return global_data.cam_data and global_data.cam_data.camera_state_type == AIM_MODE