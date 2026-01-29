# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/InjureInfo3DUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
import math
from common.const.uiconst import BASE_LAYER_ZORDER_1
import world
from mobile.common.EntityManager import EntityManager
import common.utilities
from . import InjureProcess
from . import LockProcess
from common.cfg import confmgr
from common.utils.cocos_utils import ccp
from logic.client.const import camera_const
from common.utils.cocos_utils import neox_pos_to_cocos
import game3d
import cc
from logic.client.const.camera_const import THIRD_PERSON_MODEL, POSTURE_STAND
import math3d
INJURE_TYPE_NORMAL = 0
INJURE_TYPE_WARN = 1
from common.const import uiconst

class InjureInfo3DUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/injure_3d_info'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}

    def on_init_panel(self):
        visible_conf = confmgr.get('sound_visible_const')
        max_injure_item_count = visible_conf['max_injure_item_count']
        max_lock_item_count = visible_conf['max_lock_item_count']
        lock_item_min_angle = visible_conf['lock_item_min_angle']
        injure_item_min_angle = visible_conf['injure_item_min_angle']
        lock_disappear_last_time = visible_conf['lock_disappear_last_time']
        injure_disappear_last_time = visible_conf['injure_disappear_last_time']
        lock_last_time = visible_conf['lock_last_time']
        injure_last_time = visible_conf['injure_last_time']
        self.enable_player_or_mecha = None
        self._is_in_aim = False
        self.camera_state = THIRD_PERSON_MODEL
        self.camera_posture = POSTURE_STAND
        self.panel.node_injure0.removeFromParent()
        panel_items = []
        item_conf = global_data.uisystem.load_template('battle/i_injure_3d')
        for index in range(max_injure_item_count):
            item = global_data.uisystem.create_item(item_conf, parent=self.panel.nd_perspective)
            item.setAnchorPoint(ccp(0.5, 0.5))
            panel_items.append(item)

        self._injure_process = InjureProcess.InjureProcess(self, INJURE_TYPE_NORMAL, injure_last_time, injure_disappear_last_time, max_injure_item_count, self.panel, panel_items, injure_item_min_angle, is_2d=False)
        panel_items = []
        item_conf = global_data.uisystem.load_template('battle/i_locked_warn')
        for index in range(max_lock_item_count):
            item = global_data.uisystem.create_item(item_conf, parent=self.panel)
            item.setAnchorPoint(ccp(0.5, 0))
            panel_items.append(item)

        self._lock_process = LockProcess.LockProcess(self, INJURE_TYPE_WARN, lock_last_time, lock_disappear_last_time, max_lock_item_count, self.panel, panel_items, lock_item_min_angle)
        from logic.gcommon.common_const.ui_operation_const import INJURE_VISIBLE_3D_KEY
        self.is_open_sound_visible3d = global_data.player.get_setting(INJURE_VISIBLE_3D_KEY)
        self.init_event()
        self.reset_center_positon()
        return

    def on_finalize_panel(self):
        global_data.emgr.scene_player_setted_event -= self.on_player_setted
        global_data.emgr.scene_observed_player_setted_event -= self.on_player_setted
        global_data.emgr.camera_yaw_changed -= self._on_camera_yaw_changed
        global_data.emgr.player_open_injure_visible3d -= self.on_open_injure_visible3d
        global_data.emgr.camera_switch_to_state_event -= self.on_camera_state
        global_data.emgr.switch_camera_posture_event -= self.on_camera_posture
        self.on_player_setted(None)
        self._injure_process.destroy()
        self._lock_process.destroy()
        return

    def init_event(self):
        self.player = None
        self.mecha = None
        self.on_cam_player_setted()
        global_data.emgr.scene_player_setted_event += self.on_player_setted
        global_data.emgr.scene_observed_player_setted_event += self.on_player_setted
        global_data.emgr.camera_yaw_changed += self._on_camera_yaw_changed
        global_data.emgr.player_open_injure_visible3d += self.on_open_injure_visible3d
        global_data.emgr.camera_switch_to_state_event += self.on_camera_state
        global_data.emgr.switch_camera_posture_event += self.on_camera_posture
        return

    def on_open_injure_visible3d(self, *args):
        from logic.gcommon.common_const.ui_operation_const import INJURE_VISIBLE_3D_KEY
        self.is_open_sound_visible3d = global_data.player.get_setting(INJURE_VISIBLE_3D_KEY)

    def on_cam_player_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.unbind_mecha_injured_event()
        self.bind_injured_event(self.player, is_bind=False)
        self.player = player
        if self.player:
            self.bind_injured_event(self.player, is_bind=True)
            self.mecha = self.player.ev_g_control_target().logic if self.player.ev_g_in_mecha() else None
        self.enable_player_or_mecha = self.mecha if self.mecha else self.player
        return

    def bind_injured_event(self, target, is_bind=True):
        if target and target.is_valid():
            if is_bind:
                ope_func = target.regist_event
            else:
                ope_func = target.unregist_event
            ope_func('E_HITED_SHOW_HURT_DIR', self.show_hurt_dir)
            ope_func('E_HITED_SHOW_LOCK_DIR', self.show_lock_dir)
            ope_func('E_ON_JOIN_MECHA', self.bind_mecha_injured_event)
            ope_func('E_ON_LEAVE_MECHA', self.unbind_mecha_injured_event)

    def bind_mecha_injured_event(self, mecha_id, *args, **kwargs):
        self.unbind_mecha_injured_event()
        target = EntityManager.getentity(mecha_id)
        if target is None:
            return
        else:
            self.mecha = target.logic
            ope_func = self.mecha.regist_event
            ope_func('E_HITED_SHOW_HURT_DIR', self.show_hurt_dir)
            ope_func('E_HITED_SHOW_LOCK_DIR', self.show_lock_dir)
            self.enable_player_or_mecha = self.mecha
            return

    def unbind_mecha_injured_event(self):
        if self.mecha:
            ope_func = self.mecha.unregist_event
            ope_func('E_HITED_SHOW_HURT_DIR', self.show_hurt_dir)
            ope_func('E_HITED_SHOW_LOCK_DIR', self.show_lock_dir)
            self.mecha = None
        self.enable_player_or_mecha = self.player
        return

    def _on_camera_yaw_changed(self, yaw):
        self._injure_process.refresh()
        self._lock_process.refresh()

    def show_hurt_dir(self, unit, pos, damage=0, is_mecha=False):
        if not self.is_open_sound_visible3d:
            return
        is_mecha = True if is_mecha else False
        self._injure_process.on_add_elem(unit, pos, damage, is_mecha)

    def show_lock_dir(self, unit, pos):
        self._lock_process.on_add_elem(unit, pos)

    def reset_center_positon(self):
        if not self.panel:
            return
        camera_posture_info = {}
        com_camera = global_data.game_mgr.scene.get_com('PartCamera')
        if com_camera:
            if com_camera.cam_manager:
                camera_posture_info = com_camera.cam_manager.get_state_enter_setting()
        camera = global_data.game_mgr.scene.active_camera
        pos = camera_posture_info.get('pos')
        if not pos:
            return
        world_pos = math3d.vector(-pos[0], -pos[1], -pos[2]) * camera.world_transformation
        pos_in_screen = camera.world_to_screen(world_pos)
        x, y = neox_pos_to_cocos(pos_in_screen[0], pos_in_screen[1])
        lpos = self.panel.convertToNodeSpace(cc.Vec2(x, y))
        if lpos.x > 0:
            self.panel.nd_perspective.SetPosition(lpos.x, '180')
        if self.mecha:
            scale = 0.9
        else:
            scale = 0.8
        self.panel.nd_perspective.setScaleX(scale)
        self.panel.nd_perspective.setScaleY(scale)

    def on_camera_state(self, new_cam_type, *args):
        if not self.panel:
            return
        self._is_in_aim = new_cam_type in [camera_const.AIM_MODE, camera_const.RIGHT_AIM_MODE]
        self.panel.setVisible(not self._is_in_aim)
        self.reset_center_positon()

    def on_camera_posture(self, posture):
        self.reset_center_positon()