# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Flag/FlagBaseMarkWidget.py
from __future__ import absolute_import
from common.const.uiconst import SMALL_MAP_ZORDER
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.uisys.basepanel import BasePanel
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility as tutil
import weakref
import copy
import math
from common.utils.cocos_utils import getScreenSize
import math3d
import common.utils.timer as timer
from common.const import uiconst
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
from logic.comsys.common_ui import CommonInfoUtils
from logic.gcommon.common_const.battle_const import FLAG_BATTLE_FLAG_BASE_BLUE_LOCATE_UI, FLAG_BATTLE_FLAG_BASE_RED_LOCATE_UI, FLAG_BATTLE_FLAG_LOCATE_UI
from common.utils.ui_utils import get_scale
import common.utils.cocos_utils as cocos_utils

class FlagBaseMarkWidgetUI(object):
    screen_size = getScreenSize()
    screen_angle_limit = math.atan(getScreenSize().height / 2.0 / (getScreenSize().width / 2.0)) * 180 / math.pi
    SCREEN_MARGIN = get_scale('40w')
    TYPE_TO_UI = {'flag_base_blue': FLAG_BATTLE_FLAG_BASE_BLUE_LOCATE_UI,
       'flag_base_red': FLAG_BATTLE_FLAG_BASE_RED_LOCATE_UI
       }
    TYPE_TO_BIND_NODE = {'flag_base_blue': 'fx_root',
       'flag_base_red': 'fx_root'
       }
    TYPE_TO_OFFSET = {'flag_base_blue': math3d.vector(0, 4 * NEOX_UNIT_SCALE, 0),
       'flag_base_red': math3d.vector(0, 4 * NEOX_UNIT_SCALE, 0)
       }

    def __init__(self, target_type, target_id, panel):
        self.on_init(target_type, target_id, panel)

    def on_init(self, target_type, target_id, panel):
        self.init_parameters(target_type, target_id, panel)
        self.init_node()
        self.init_timer()

    def init_node(self):
        self.space_node = CCUISpaceNode.Create()
        ui_key = self.TYPE_TO_UI.get(self.target_type)
        self.base_node = CommonInfoUtils.create_ui(ui_key, self.space_node, False, False)
        self.base_node.setPosition(0, 0)
        if global_data.aim_transparent_mgr:
            global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__, [self.base_node])
        self.pos_node = self.base_node.nd_mark
        self.nd_rotate = self.pos_node.nd_rotate
        horizontal_margin = 140 * self.panel.getScale()
        vertical_margin = 80 * self.panel.getScale()
        top_margin = self.SCREEN_MARGIN
        self.space_node.set_enable_limit_in_screen(True, horizontal_margin, horizontal_margin, top_margin, vertical_margin)
        self.space_node.set_screen_check_margin(0, 0, top_margin, 0)

    def init_parameters(self, target_type, target_id, panel):
        self.target_type = target_type
        self.target_id = target_id
        self.panel = panel
        self.bind_node = self.TYPE_TO_BIND_NODE.get(self.target_type)
        faction_to_flag_base_id = global_data.death_battle_data.faction_to_flag_base_id
        scn = global_data.game_mgr.scene
        self.camera = weakref.ref(scn.active_camera)
        self._binded_model = None
        self._binded_socket = None
        self.space_node = None
        self.base_node = None
        self.nd_rotate = None
        self.icon_update_timer = None
        self.pos_offset = self.TYPE_TO_OFFSET.get(target_type, math3d.vector(0, 0, 0))
        return

    def init_timer(self):
        self.process_update_timer(True)

    def update_follow_target(self, target_type, target_id):
        self.target_type = target_type
        self.target_id = target_id
        self.bind_node = self.TYPE_TO_BIND_NODE.get(self.target_type)
        self._binded_model = None
        self._binded_socket = None
        return

    def _on_update_pos_and_rot(self):
        cam_lplayer = global_data.cam_lplayer
        lplayer_pos = self.get_target_pos(cam_lplayer)
        if not cam_lplayer:
            return
        self.update_nd_pos_and_rot(self.camera(), cam_lplayer, lplayer_pos, self.target_id)

    def get_target_pos(self, ltarget):
        if ltarget:
            control_target = ltarget.sd.ref_ctrl_target
            if control_target and control_target.logic:
                pos = control_target.logic.ev_g_model_position()
                return pos
        return None

    def update_nd_pos_and_rot(self, camera, cam_lplayer, lplayer_pos, target_eid):
        target_ent = global_data.battle.get_entity(target_eid)
        if not target_ent:
            return
        target_model = target_ent.logic.ev_g_model()
        if not target_model:
            return False
        if not lplayer_pos:
            return False
        target_position = target_model.world_position
        if not target_position:
            return False
        self.try_bind_model(self.space_node, target_model, self.pos_offset, self.bind_node)
        self.update_rot(camera, target_position, lplayer_pos)
        return True

    def update_rot(self, camera, target_position, lplayer_pos):
        target_camera_pos = camera.world_to_camera(target_position)
        angle = math.atan2(target_camera_pos.y, target_camera_pos.x)
        angle = angle * 180 / math.pi
        if angle < 0:
            angle += 360
        self.nd_rotate.setRotation(-(angle - 90))

    def try_bind_model(self, node, interact_model, pos_offset=None, socket=None):
        if not node:
            return
        if not self._binded_model or self._binded_model() != interact_model or self._binded_socket != socket:
            if not node:
                return
            if socket:
                node.bind_model(interact_model, socket)
                node.set_fix_xz(False)
            else:
                node.bind_space_object(interact_model)
            self._binded_model = weakref.ref(interact_model)
            self._binded_socket = socket
            if pos_offset:
                node.set_pos_offset(pos_offset)

    def process_update_timer(self, tag=True):
        if tag:
            if not self.icon_update_timer:
                self.icon_update_timer = global_data.game_mgr.register_logic_timer(self._on_update_pos_and_rot, 0.05, mode=timer.CLOCK)
        elif self.icon_update_timer:
            global_data.game_mgr.unregister_logic_timer(self.icon_update_timer)
            self.icon_update_timer = None
        return

    def on_finalize(self):
        self.process_update_timer(False)
        self.panel = None
        self.nd_rotate = None
        self.base_node = None
        if self.space_node:
            self.space_node.Destroy()
        self.space_node = None
        self.pos_offset = None
        return