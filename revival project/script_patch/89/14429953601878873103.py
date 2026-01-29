# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterMoveLogic.py
from __future__ import absolute_import
from .MoveLogic import Walk, Run
from common.cfg import confmgr
from common.utils.timer import CLOCK

class MonsterWalk(Walk):
    BIND_EVENT = Walk.BIND_EVENT.copy()
    BIND_EVENT.update({'E_MOVE_TO_LIST': 'on_set_move_list',
       'E_SET_MOVE_TARGET': 'on_set_move_target',
       'E_MONSTER_SPEED_SCALE': 'on_speed_scale'
       })
    LERP_DUR = 0.8

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterWalk, self).init_from_dict(unit_obj, bdict, sid, info)
        self.pos_list = []
        self.lerp_tag = False
        self.lerp_timer = None
        self.lerp_count = 0
        self.move_target = None
        self.last_move_target = None
        self.last_dire = None
        return

    def on_init_complete(self):
        move_ratio = self.ev_g_move_ratio()
        if move_ratio:
            self.walk_speed *= move_ratio
            self.dynamic_speed_rate *= move_ratio

    def on_speed_scale(self, scale):
        self.walk_speed *= scale
        self.dynamic_speed_rate *= scale

    def update(self, dt):
        super(MonsterWalk, self).update(dt)

    def exit(self, enter_states):
        self.reset_lerp_timer()
        super(MonsterWalk, self).exit(enter_states)

    def destroy(self):
        self.reset_lerp_timer()
        super(MonsterWalk, self).destroy()

    def on_set_move_list(self, pos_list):
        if self.pos_list != pos_list:
            self.lerp_tag = True
            self.pos_list = pos_list
        if not pos_list:
            self.lerp_tag = False
            self.move_target = None
            self.last_move_target = None
            self.reset_lerp_timer()
        return

    def on_set_move_target(self, move_target):
        self.last_move_target = self.move_target
        if self.last_move_target and move_target:
            if self.lerp_tag:
                self.init_lerp_timer()
        self.move_target = move_target

    def reset_lerp_timer(self):
        if self.lerp_timer:
            global_data.game_mgr.unregister_logic_timer(self.lerp_timer)
            self.lerp_timer = None
        return

    def init_lerp_timer(self):
        self.reset_lerp_timer()
        self.lerp_count = 0
        cur_pos = self.ev_g_position()
        self.last_dire = self.last_move_target - cur_pos
        self.last_dire.normalize()
        self.lerp_timer = global_data.game_mgr.register_logic_timer(self.tick_lerp, 0.016, None, -1, CLOCK, True)
        return

    def tick_lerp(self, dt):
        if not self.is_active:
            return
        self.lerp_count += dt
        cur_pos = self.ev_g_position()
        target_dir = self.move_target - cur_pos
        target_dir.normalize()
        if self.lerp_count > self.LERP_DUR:
            self.lerp_count = self.LERP_DUR
            self.reset_lerp_timer()
        self.last_dire.intrp(self.last_dire, target_dir, self.lerp_count / self.LERP_DUR)
        ret_dir = self.last_dire
        yaw = ret_dir.yaw
        self.send_event('E_CAM_YAW', yaw)
        self.send_event('E_ACTION_SYNC_YAW', yaw)


class MonsterRun(Run):
    BIND_EVENT = Run.BIND_EVENT.copy()
    BIND_EVENT.update({'E_MOVE_TO_LIST': 'on_set_move_list',
       'E_SET_MOVE_TARGET': 'on_set_move_target',
       'E_MONSTER_SPEED_SCALE': 'on_speed_scale'
       })
    LERP_DUR = 0.8

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterRun, self).init_from_dict(unit_obj, bdict, sid, info)
        self.pos_list = []
        self.lerp_tag = False
        self.lerp_timer = None
        self.lerp_count = 0
        self.move_target = None
        self.last_move_target = None
        self.last_dire = None
        return

    def on_init_complete(self):
        move_ratio = self.ev_g_move_ratio()
        if move_ratio:
            self.walk_speed *= move_ratio
            self.run_speed *= move_ratio
            self.dynamic_speed_rate *= move_ratio

    def on_speed_scale(self, scale):
        self.walk_speed *= scale
        self.run_speed *= scale
        self.dynamic_speed_rate *= scale

    def update(self, dt):
        super(MonsterRun, self).update(dt)

    def exit(self, enter_states):
        self.reset_lerp_timer()
        super(MonsterRun, self).exit(enter_states)

    def destroy(self):
        self.reset_lerp_timer()
        super(MonsterRun, self).destroy()

    def on_set_move_list(self, pos_list):
        if self.pos_list != pos_list:
            self.lerp_tag = True
            self.pos_list = pos_list
        if not pos_list:
            self.lerp_tag = False
            self.move_target = None
            self.last_move_target = None
            self.reset_lerp_timer()
        return

    def on_set_move_target(self, move_target):
        self.last_move_target = self.move_target
        if self.last_move_target and move_target:
            if self.lerp_tag:
                self.init_lerp_timer()
        self.move_target = move_target

    def reset_lerp_timer(self):
        if self.lerp_timer:
            global_data.game_mgr.unregister_logic_timer(self.lerp_timer)
            self.lerp_timer = None
        return

    def init_lerp_timer(self):
        self.reset_lerp_timer()
        self.lerp_count = 0
        cur_pos = self.ev_g_position()
        self.last_dire = self.last_move_target - cur_pos
        self.last_dire.normalize()
        self.lerp_timer = global_data.game_mgr.register_logic_timer(self.tick_lerp, 0.016, None, -1, CLOCK, True)
        return

    def tick_lerp(self, dt):
        if not self.is_active:
            return
        self.lerp_count += dt
        cur_pos = self.ev_g_position()
        target_dir = self.move_target - cur_pos
        target_dir.normalize()
        if self.lerp_count > self.LERP_DUR:
            self.lerp_count = self.LERP_DUR
            self.reset_lerp_timer()
        self.last_dire.intrp(self.last_dire, target_dir, self.lerp_count / self.LERP_DUR)
        ret_dir = self.last_dire
        yaw = ret_dir.yaw
        self.send_event('E_CAM_YAW', yaw)
        self.send_event('E_ACTION_SYNC_YAW', yaw)