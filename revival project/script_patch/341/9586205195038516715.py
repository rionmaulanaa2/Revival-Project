# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/assistant_utils.py
from __future__ import absolute_import
import world
import math3d
import math
from logic.gcommon.common_const import assistant_const as ast_arg
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.assistant_const import SHOW_UP_EFFECT
UNIT_Y = math3d.vector(0, 1, 0)
FOLLOW_OFFSET = ((10, 10, 8), (-10, 10, 8), (0, 18, 0))
FOLLOW_OFFSET_CRAWL = ((7, 2, 4), (-7, 2, 4), (0, 4, 0))

def reset_position(target):
    m = target.unit_obj.ev_g_model()
    if not target or not m:
        return
    foward, right = m.world_transformation.forward, m.world_transformation.right
    valid_pos = math3d.vector(m.position)
    valid_pos += right * FOLLOW_OFFSET[0][0]
    valid_pos.y += FOLLOW_OFFSET[0][1]
    direct = m.world_transformation.forward
    target.model.rotation_matrix = math3d.matrix.make_orient(direct, UNIT_Y)
    target.model.position = valid_pos


def reset_direction(target):
    m = target.unit_obj.ev_g_model()
    if not m or not m.valid:
        return
    if not target.model or not target.model.valid:
        return
    direct = m.world_transformation.forward
    target.model.rotation_matrix = math3d.matrix.make_orient(direct, UNIT_Y)


TOLERANCE = 0.9

def move_to_dest(target, valid_pos, delta, cb):
    if not target:
        return
    model = target.model
    direct = valid_pos - model.position
    dist = direct.length
    if dist >= 5 * NEOX_UNIT_SCALE and not target.disable_auto_follow:
        target.send_event('E_ASSIST_BLINK')
        cur_pos = model.position
        cur_pos.y += 3

        def create_cb(sfx):
            sfx.scale = math3d.vector(0.3, 0.3, 0.3)

        global_data.sfx_mgr.create_sfx_in_scene(SHOW_UP_EFFECT, cur_pos, duration=1.5, on_create_func=create_cb)
        model.position = valid_pos
        target.send_event('E_ASSISTANT_FLY', False)
        return cb()
    if direct.is_zero or dist < 0.5:
        target.send_event('E_ASSISTANT_FLY', False)
        return cb()
    direct.normalize()
    forward = model.rotation_matrix.forward
    move_dir = math3d.vector(direct)
    direct.y, forward.y = (0, 0)
    if not (direct.is_zero or forward.is_zero):
        (
         direct.normalize(), forward.normalize())
        if direct.dot(forward) < TOLERANCE:
            ori_rot = math3d.matrix_to_rotation(math3d.matrix.make_orient(forward, UNIT_Y))
            tar_rot = math3d.matrix_to_rotation(math3d.matrix.make_orient(direct, UNIT_Y))
            rot = math3d.rotation(0, 0, 0, 1)
            rot.slerp(ori_rot, tar_rot, delta * 5, True)
            model.rotation_matrix = math3d.rotation_to_matrix(rot)
            target.send_event('E_ASSISTANT_FLY', False)
            return
        rot = math3d.matrix_to_rotation(math3d.matrix.make_orient(direct, UNIT_Y))
        model.rotation_matrix = math3d.rotation_to_matrix(rot)
        target.send_event('E_ASSISTANT_FLY', True)
    human_speed = target.unit_obj.ev_g_speed()
    speed = 1 + human_speed * dist / 10
    speed = min(speed, human_speed)
    pos = model.position
    move_delta = move_dir * speed * delta
    if move_delta.length > dist:
        model.position = valid_pos
    else:
        model.position = pos + move_delta
    target.unit_obj.send_event('E_ASSIST_SPEED', speed * 1.0 / human_speed)


def get_actionlist_by_orders(unit_obj, order_list):
    mod = globals()
    action_list = ActionList()
    for order in order_list:
        order_name, params = order[0], order[1]
        klass = mod.get(order_name)
        if klass is None:
            return
        action_list.add(klass(unit_obj, **params))

    return action_list


def get_on_vehicle(m_vehicle, m_assist):
    if not m_vehicle or not m_assist:
        return
    m_assist.remove_from_parent()
    m_vehicle.bind('cat_pos', m_assist, world.BIND_TYPE_ALL)
    m_assist.position = math3d.vector(0, 0, 0)
    mat = m_assist.rotation_matrix
    mat.set_identity()
    m_assist.rotation_matrix = mat


class ActionList(object):

    def __init__(self):
        self.action_list = []
        self.action_idx = 0

    def add(self, action):
        self.action_list.append(action)

    def updateAction(self):
        action = self.action_list[self.action_idx]
        if action.execute():
            self.action_idx += 1

    def done(self):
        if self.action_idx >= len(self.action_list):
            for action in self.action_list:
                action.destroy()

            return True
        return False


class ActionBase(object):

    def __init__(self, unit_obj):
        self.unit_obj = unit_obj
        self.start = False
        self.end = False

    def finish_cb(self):
        self.end = True

    def execute(self):
        if not self.start:
            self.start = True
            self.execute_action()
        return self.end

    def execute_action(self):
        raise Exception('Action execute not implement')

    def destroy(self):
        self.unit_obj = None
        return


class ActionCallback(ActionBase):

    def __init__(self, unit_obj, cb):
        super(ActionCallback, self).__init__(unit_obj)
        self.cb = cb

    def execute_action(self):
        if self.cb:
            self.cb()
        self.finish_cb()


class ActionFlyTo(ActionBase):

    def __init__(self, unit_obj=None, pos=None):
        super(ActionFlyTo, self).__init__(unit_obj)
        self.destination = pos

    def execute_action(self):
        self.unit_obj.send_event('E_ASSISTANT_MOVE_TO', self.destination, self.finish_cb)


class ActionExcute(ActionBase):
    ACTION_TYPE = None

    def __init__(self, unit_obj=None):
        super(ActionExcute, self).__init__(unit_obj)

    def execute_action(self):
        self.unit_obj.send_event('E_ASSISTANT_SUMMON', self.finish_cb, self.ACTION_TYPE)


class ActionSummon(ActionExcute):
    ACTION_TYPE = ast_arg.SUMMON_TOOLS


class Action3dPrint(ActionExcute):
    ACTION_TYPE = ast_arg.BUILD_3D_PRINT


class ActionSignal(ActionExcute):
    ACTION_TYPE = ast_arg.SHOOT_SINGAL


class ActionDriveMounts(ActionBase):
    DRIVE_TYPE = None

    def __init__(self, unit_obj=None, pos=None, parent=None):
        super(ActionDriveMounts, self).__init__(unit_obj)
        self.destination = pos
        self.parent = parent
        self.get_off = False

    def execute_action(self):
        if self.destination:
            self.unit_obj.send_event('E_ASSISTANT_MOVE_TO', self.destination, self.finish_cb)
        else:
            self.finish_cb()

    def execute(self):
        if self.end:
            return self.get_off
        if not self.start:
            self.start = True
            self.execute_action()
        return False

    def finish_cb(self):
        if self.parent and self.parent.is_valid():
            m_assist = self.unit_obj.ev_g_assistant_model()
            m_parent = self.parent.ev_g_mounts()
            get_on_vehicle(m_parent, m_assist)
            self.unit_obj.send_event('E_ASSISTANT_DRIVE', self.DRIVE_TYPE)
            self.end = True
            target = self.unit_obj
            if target and target.is_valid():
                regist_func = target.regist_event
                regist_func('E_ASSIST_GET_OFF_DONE', self.on_get_off)

    def on_get_off(self):
        self.get_off = True
        target = self.unit_obj
        if target and target.is_valid():
            unregist_func = target.unregist_event
            unregist_func('E_ASSIST_GET_OFF_DONE', self.on_get_off)


class ActionDriveMusicPlayer(ActionDriveMounts):
    DRIVE_TYPE = ast_arg.DRIVE_MUSIC_PLAYER


class ActionDriveSentryGun(ActionDriveMounts):
    DRIVE_TYPE = ast_arg.DRIVE_SENTRY_GUN


class ActionDriveDrone(ActionDriveMounts):
    DRIVE_TYPE = ast_arg.DRIVE_DRONE

    def finish_cb(self):
        super(ActionDriveDrone, self).finish_cb()
        if self.unit_obj.id == global_data.player.id:
            self.parent.send_event('E_END_SHOW_CONTROL_DRONE')