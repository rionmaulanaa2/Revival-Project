# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHideClient.py
from __future__ import absolute_import
import math3d
import logic.gcommon.const as g_const
from ..UnitCom import UnitCom
from ...cdata import status_config
APPEAR_POS_OFFSET = -1.0

class ComHideClient(UnitCom):
    BIND_EVENT = {'E_REQ_ENTER_HIDING': '_req_hide',
       'E_REQ_LEAVE_HIDING': '_req_leave',
       'E_ENTER_HIDING': '_on_hide',
       'E_LEAVE_HIDING': '_on_leave',
       'G_IS_IN_HIDING': '_is_in_hiding',
       'E_REQ_BUILD_HIDING': '_req_build_hiding'
       }

    def __init__(self):
        super(ComHideClient, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComHideClient, self).init_from_dict(unit_obj, bdict)
        self._hiding_id = bdict.get('hiding_id', None)
        return

    def _req_hide(self, hiding_id):
        self.send_event('E_CALL_SYNC_METHOD', 'req_enter_hiding', (hiding_id,))

    def _on_hide(self, hiding_id):
        from mobile.common.EntityManager import EntityManager
        self.unit_obj.send_event('E_MOVE_STOP')
        self._hiding_id = hiding_id
        target = EntityManager.getentity(self._hiding_id)
        if target and target.logic and target.logic.is_valid():
            pos = target.logic.ev_g_foot_position()
            self.unit_obj.send_event('E_FOOT_POSITION', pos)
            if G_POS_CHANGE_MGR:
                self.notify_pos_change(pos, True)
            else:
                self.unit_obj.send_event('E_POSITION', pos)
            self.unit_obj.send_event('E_SET_CONTROL_TARGET', target, {})
            self.unit_obj.send_event('E_TO_HIDING_CAMERA')
        self.unit_obj.send_event('E_HIDE_MODEL')
        self.unit_obj.send_event('E_COLLISION_ENABLE', False)
        main_player = global_data.player.logic
        if self.unit_obj.id == main_player.id:
            if global_data.ui_mgr.get_ui('HidingUI'):
                global_data.ui_mgr.close_ui('HidingUI')
            global_data.ui_mgr.show_ui('HidingUI', 'logic.comsys.battle')

    def _req_leave(self):
        pos = self._get_leave_land_pos()
        com_camera = self.scene.get_com('PartCamera')
        yaw = com_camera.get_yaw()
        self.send_event('E_CALL_SYNC_METHOD', 'req_leave_hiding', (pos, yaw))

    def _on_leave(self, pos, yaw):
        self.unit_obj.send_event('E_SHOW_MODEL')
        self.send_event('E_CTRL_STAND')
        self.unit_obj.send_event('E_MOVE_STOP')
        self.unit_obj.send_event('E_FOOT_POSITION', math3d.vector(*pos))
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(math3d.vector(*pos), True)
        else:
            self.unit_obj.send_event('E_POSITION', math3d.vector(*pos))
        self.unit_obj.send_event('E_SET_CONTROL_TARGET', None, {})
        self.ev_g_status_try_trans(status_config.ST_STAND)
        main_player = global_data.player.logic
        if self.unit_obj.id == main_player.id:
            global_data.ui_mgr.close_ui('HidingUI')
            self.unit_obj.send_event('E_TO_THIRD_PERSON_CAMERA')
        self.unit_obj.send_event('E_FOOT_POSITION', math3d.vector(*pos))
        if G_POS_CHANGE_MGR:
            self.notify_pos_change(math3d.vector(*pos), True)
        else:
            self.unit_obj.send_event('E_POSITION', math3d.vector(*pos))
        self.send_event('E_ACTION_SET_YAW', yaw)
        self.unit_obj.send_event('E_COLLISION_ENABLE', True)
        self._hiding_id = None
        return

    def _is_in_hiding(self):
        if self._hiding_id:
            return True
        return False

    def is_control_avatar(self):
        return self.is_unit_obj_type('LAvatar')

    def _req_build_hiding(self, hiding_id):
        self.send_event('E_CALL_SYNC_METHOD', 'build_hiding', (hiding_id,))

    def _get_leave_land_pos(self):
        vec = global_data.sound_mgr.get_listener_look_at()
        forward = math3d.vector(vec.x, 0.0, vec.z)
        forward.normalize()
        pos = global_data.player.logic.ev_g_position() + forward * APPEAR_POS_OFFSET * g_const.NEOX_UNIT_SCALE
        return (
         pos.x, pos.y, pos.z)