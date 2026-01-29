# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleScreenMarkUI.py
from __future__ import absolute_import
import math
import math3d
import weakref
from common.utils.cocos_utils import getScreenSize
from common.utils.ui_utils import get_scale
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER, UI_VKB_NO_EFFECT
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.platform.device_info import DeviceInfo
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
from logic.comsys.common_ui import CommonInfoUtils
from logic.gutils import screen_utils

class MarkNode(object):

    def __init__(self, panel, ui_template):
        self.panel = panel
        self._nd = global_data.uisystem.load_template_create(ui_template)
        self._nd.setVisible(False)
        self.panel.AddChild('', self._nd)
        self.init_parameter()
        self.init_timer()

    def init_parameter(self):
        self.pos = None
        self._is_bind = False
        self._timer = None
        self.target_id = None
        self.only_show_out_screen = False
        self.screen_size = getScreenSize()
        device_info = DeviceInfo()
        self.is_can_full_screen = device_info.is_can_full_screen()
        self.screen_angle_limit = math.atan(self.screen_size.height / 2.0 / (self.screen_size.width / 2.0)) * 180 / math.pi
        self.scale_data = {'scale_90': (get_scale('90w'), get_scale('280w')),'scale_40': (
                      get_scale('40w'), get_scale('120w')),
           'scale_left': (
                        get_scale('90w'), get_scale('300w')),
           'scale_right': (
                         get_scale('90w'), get_scale('200w')),
           'scale_up': (
                      get_scale('90w'), get_scale('120w')),
           'scale_low': (
                       get_scale('90w'), get_scale('120w'))
           }
        return

    def init_timer(self):
        self.clear_run_timer()
        self._timer = global_data.game_mgr.register_logic_timer(self.update_nd, interval=0.05, times=-1, mode=2)

    def set_follow_target(self, target_id, only_show_out_screen=False):
        self.target_id = target_id
        self.only_show_out_screen = only_show_out_screen

    def update_nd(self):
        self.update_nd_pos_and_rot()

    def update_nd_pos_and_rot(self):
        if not global_data.battle:
            return
        cam = global_data.game_mgr.scene.active_camera
        if not cam:
            return
        if not self.target_id:
            return
        target_ent = global_data.battle.get_entity(self.target_id)
        if not target_ent:
            return
        target_pos = target_ent.logic.ev_g_position()
        if not target_pos:
            return
        if self._nd.IsDestroyed():
            return
        target_pos.y += 100
        self._nd.setVisible(True)
        is_in_screen, end_pos, angle = screen_utils.world_pos_to_screen_pos(self._nd, target_pos, self.screen_size, self.screen_angle_limit, self.is_can_full_screen, self.scale_data)
        if self.only_show_out_screen:
            self._nd.setVisible(not is_in_screen)
        dist = cam.position - target_pos
        dist = dist.length / NEOX_UNIT_SCALE
        self._nd.setPosition(end_pos)
        self._nd.nd_dir.setVisible(not is_in_screen)
        self._nd.nd_dir.setRotation(angle + 90)

    def clear_run_timer(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
        self._timer = None
        return

    def destroy(self):
        self.clear_run_timer()
        if self._nd:
            self._nd.Destroy()


class BattleScreenMarkUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.process_event(True)
        self.panel.setLocalZOrder(1)

    def on_finalize_panel(self):
        self.node_dict = {}
        self.process_event(False)

    def init_parameters(self):
        self.node_dict = {}

    def on_add_entity_screen_mark(self, entity_id, template_path, only_show_out_screen=False):
        old_mark = self.node_dict.get(entity_id, None)
        if old_mark:
            old_mark.destroy()
        self.node_dict[entity_id] = MarkNode(self.panel, template_path)
        self.node_dict[entity_id].set_follow_target(entity_id, only_show_out_screen)
        return

    def on_del_entity_screen_mark(self, entity_id):
        if entity_id not in self.node_dict:
            return
        else:
            old_mark = self.node_dict.get(entity_id, None)
            if old_mark:
                old_mark.destroy()
            del self.node_dict[entity_id]
            return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'add_entity_screen_mark': self.on_add_entity_screen_mark,
           'del_entity_screen_mark': self.on_del_entity_screen_mark
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)