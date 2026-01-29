# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComLiftTrigger.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from common.cfg import confmgr
import collision
import math3d

class ComLiftTrigger(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': '_on_model_loaded',
       'E_POSITION': '_on_pos_changed',
       'E_UPDATE_LIFT_SPEED': 'update_lift_speed',
       'E_UPDATE_LIFT_USER': 'update_lift_user',
       'E_LIFT_ENABLE': 'enable_trigger'
       }

    def __init__(self):
        super(ComLiftTrigger, self).__init__()
        self.lift_trigger = None
        self.lift_out_trigger = None
        self.out_speed = None
        self.pos_offset1 = math3d.vector(0, 0, 0)
        self.pos_offset2 = math3d.vector(0, 0, 0)
        self.lift_users = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComLiftTrigger, self).init_from_dict(unit_obj, bdict)
        self.res_id = bdict.get('res_id', 0)
        self.res_conf = confmgr.get('machine_art_config', str(self.res_id), default={})
        self.trigger_info = self.res_conf.get('trigger_info')
        if self.trigger_info:
            trigger1 = self.trigger_info[0]
            self.pos_offset1 = math3d.vector(*trigger1['pos_offset'])
            trigger2 = self.trigger_info[1]
            self.pos_offset2 = math3d.vector(*trigger2['pos_offset'])
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self._on_pos_changed)

    def _on_model_loaded(self, model):
        if not model or not model.valid:
            return
        if not self.scene:
            return
        rot = model.world_rotation_matrix
        self.out_speed = rot.right * 200
        self.create_triggers(model)

    def create_triggers(self, model):
        if not self.trigger_info:
            return
        trigger1 = self.trigger_info[0]
        size = trigger1['size']
        box = math3d.vector(size[0] * 0.5, size[1] * 0.5, size[2] * 0.5)
        obj = collision.col_object(collision.BOX, box, 0, 0, 0)
        obj.set_trigger(self.ev_g_lift_enable())
        obj.set_trigger_callback(self._lift_callback)
        self.scene.scene_col.add_object(obj)
        obj.position = model.position + self.pos_offset1
        self.lift_trigger = obj
        trigger2 = self.trigger_info[1]
        size = trigger2['size']
        box = math3d.vector(size[0] * 0.5, size[1] * 0.5, size[2] * 0.5)
        out_trigger = collision.col_object(collision.BOX, box, 0, 0, 0)
        out_trigger.set_trigger(self.ev_g_lift_enable())
        out_trigger.set_trigger_callback(self._lift_out_callback)
        self.scene.scene_col.add_object(out_trigger)
        out_trigger.position = model.position + self.pos_offset2
        self.lift_out_trigger = out_trigger

    def _on_pos_changed(self, pos):
        if self.lift_trigger:
            self.lift_trigger.position = pos + self.pos_offset1
        if self.lift_out_trigger:
            self.lift_out_trigger.position = pos + self.pos_offset2

    def _lift_out_callback(self, *args):
        _, other_obj, flag = args
        if not other_obj:
            return
        user = global_data.emgr.scene_find_lift_user_event.emit(other_obj.cid)
        if not user or not user[0]:
            return
        user = user[0]
        if not flag:
            user.send_event('E_CHARACTER_WALK_LIFT', math3d.vector(0, 0, 0))
        else:
            user.send_event('E_CHARACTER_WALK_LIFT', self.out_speed)

    def _lift_callback(self, *args):
        _, other_obj, flag = args
        if not other_obj:
            return
        user = global_data.emgr.scene_find_lift_user_event.emit(other_obj.cid)
        if not user or not user[0]:
            return
        user = user[0]
        if not flag:
            user.send_event('E_CHARACTER_WALK_LIFT', math3d.vector(0, 0, 0))
        else:
            speed = self.ev_g_lift_speed()
            if not speed:
                return
            speed = speed
            user.send_event('E_CHARACTER_WALK_LIFT', speed)
        self.update_lift_user(other_obj.cid, user, flag)

    def update_lift_user(self, cid, user, flag):
        if flag:
            self.lift_users[cid] = user
            user.send_event('E_GET_ON_LIFT', self.unit_obj, True)
        elif cid in self.lift_users:
            user.send_event('E_GET_ON_LIFT', self.unit_obj, False)
            del self.lift_users[cid]

    def update_lift_speed(self, speed):
        for user in six.itervalues(self.lift_users):
            if user and user.is_valid():
                user.send_event('E_CHARACTER_WALK_LIFT', speed)

    def destroy(self):
        self.lift_users.clear()
        if self.scene:
            if self.lift_trigger:
                self.scene.scene_col.remove_object(self.lift_trigger)
            if self.lift_out_trigger:
                self.scene.scene_col.remove_object(self.lift_out_trigger)
        self.lift_trigger = None
        self.lift_out_trigger = None
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self._on_pos_changed)
        super(ComLiftTrigger, self).destroy()
        return

    def enable_trigger(self, is_enable):
        if not is_enable:
            for user in six.itervalues(self.lift_users):
                if user and user.is_valid():
                    user.send_event('E_CHARACTER_WALK_LIFT', math3d.vector(0, 0, 0))
                    user.send_event('E_GET_ON_LIFT', self.unit_obj, False)

            self.lift_users.clear()
        if self.lift_trigger:
            self.lift_trigger.set_trigger(is_enable)
        if self.lift_out_trigger:
            self.lift_out_trigger.set_trigger(is_enable)