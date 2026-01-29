# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/monster_skill/MonsterSkill.py
from __future__ import absolute_import
from six.moves import range
from mobile.common.IdManager import IdManager
import data.s_grenade_data as s_grenade_data
from logic.gcommon import time_utility as tutil
from logic.gcommon.monster_skill.MonsterAction import Action
from logic.gutils import delay
from logic.gcommon.common_const import monster_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from math3d import vector
import logic.gcommon.common_utils.bcast_utils as bcast

class MonsterSkill(object):

    def __init__(self, skill_id, unit_obj, cfg):
        self.skill_id = skill_id
        self.unit_obj = unit_obj
        self.owner_id = unit_obj.get_owner().id
        self.cool_down = cfg['cool_down']
        self.cast_range = cfg['range'] * NEOX_UNIT_SCALE
        self.cast_time = 0
        self.cast_num = cfg['multi_cast_num']
        self.timer = None
        self.cur_action = None
        self.frames = None
        self.init_frames(cfg)
        self.explosive_id = cfg['explosive']
        self.explosive_delay = cfg['explosive_delay']
        self.explosive_height = cfg['explosive_height'] * NEOX_UNIT_SCALE
        self.explosive = None
        self.mark_id = cfg['mark']
        self.explosive_delay_timer = None
        self.target = None
        self.target_pos = None
        return

    def init_frames(self, cfg):
        frames = []
        frames.append([None, 0.2])
        self.init_cast_begin_frame(cfg, frames)
        self.init_cast_frame(cfg, frames)
        self.init_cast_end_frame(cfg, frames)
        self.frames = frames
        return

    def init_cast_begin_frame(self, cfg, frames):
        frame = cfg['cast_begin_frame']
        frames.append([self.cast_begin_logic, frame])

    def init_cast_frame(self, cfg, frames):
        frame = cfg['cast_frame']
        num = cfg['multi_cast_num']
        for i in range(num):
            frames.append([self.cast_logic, frame])

    def init_cast_end_frame(self, cfg, frames):
        frame = cfg['cast_end_frame']
        frames.append([self.cast_end_logic, frame])

    def cast_begin_logic(self, *_):
        self.on_cast_action(monster_const.CAST_PRE)
        return self.cast_num

    def cast_logic(self, num):
        if not self.unit_obj:
            return num
        cast_pos = self.target_pos
        self.create_mask(cast_pos)
        self.delay_create_explosive(cast_pos)
        self.on_cast_action(monster_const.CAST_FIRE)
        num -= 1
        if num > 0:
            target = self.target
            if target and target.logic and target.logic.is_valid() and target.logic.is_alive():
                m_pos = self.unit_obj.get_owner().get_position()
                t_pos = target.get_position()
                dist = (m_pos - t_pos).length
                if dist < self.cast_range and not self.is_cast_hit(t_pos):
                    battle = self.unit_obj.get_battle()
                    y = battle.get_height(t_pos.x, t_pos.z)
                    y = y if y else t_pos.y
                    self.target_pos = [t_pos.x, y, t_pos.z]
        return num

    def cast_end_logic(self, *_):
        self.on_cast_action(monster_const.CAST_POST)

    def on_cast_action(self, *args):
        if self.unit_obj:
            self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_MONSTER_CAST_ACTION, args), True, True, True)

    def is_kill_ready(self):
        if self.cur_action:
            return False
        return tutil.get_time() >= self.cool_down + self.cast_time

    def is_cast_hit(self, start_pos):
        if not self.unit_obj:
            return False
        end_pos = start_pos + vector(0, self.explosive_height, 0)
        return not self.unit_obj.get_battle().can_shoot(start_pos, end_pos)

    def do_skill(self, target):
        if not self.unit_obj:
            return
        self.cast_time = tutil.get_time()
        self.cur_action = self.cast_explosive()
        self.target = target
        pos = target.get_position()
        battle = self.unit_obj.get_battle()
        y = battle.get_height(pos.x, pos.z)
        y = y if y else pos.y
        self.target_pos = [pos.x, y, pos.z]
        self.cur_action.start()

    def end_skill(self):
        self.cur_action = None
        self.target = None
        self.target_pos = None
        if self.unit_obj:
            self.unit_obj.send_event('E_END_MONSTER_SKILL', self.skill_id)
        return

    def break_skill(self):
        if self.cur_action:
            self.cur_action.exit()
            self.cur_action = None
            self.target = None
            self.target_pos = None
        if self.timer:
            delay.cancel(self.timer)
            self.timer = None
        if self.explosive_delay_timer:
            delay.cancel(self.explosive_delay_timer)
            self.explosive_delay_timer = None
        self.unit_obj = None
        self.target = None
        self.frames = None
        return

    @Action
    def cast_explosive(self):
        frames = self.frames
        last_frame_ret = None
        for info in frames:
            logic, frame = info
            frame_ret = None
            if logic:
                frame_ret = logic(last_frame_ret)
            self.timer = None
            self.timer = delay.call(frame, lambda r=frame_ret: self.resume_action(r))
            last_frame_ret = yield

        self.end_skill()
        return

    def resume_action(self, frame_ret):
        self.timer = None
        if self.cur_action:
            self.cur_action.resume(frame_ret)
        return

    def delay_create_explosive(self, cast_pos):
        pos = [cast_pos[0], cast_pos[1] + self.explosive_height, cast_pos[2]]
        self.explosive_delay_timer = delay.call(self.explosive_delay, lambda p=pos: self.create_explosive(p))

    def create_explosive(self, cast_pos):
        self.explosive_delay_timer = None
        if not self.unit_obj:
            return
        else:
            explosive_id = self.explosive_id
            item_info = {'item_id': explosive_id,
               'item_itype': explosive_id,
               'position': cast_pos,
               'uniq_key': IdManager.genid(),
               'dir': (0, -1, 0),
               'owner_id': self.owner_id,
               'trigger_id': self.owner_id
               }
            item_conf = s_grenade_data.data.get(explosive_id, None)
            item_info['last_time'] = item_conf.get('fTimeFly', 0)
            self.unit_obj.send_event('E_SKILL_EXPLOSIVE_ITEM', item_info, True)
            return

    def create_mask(self, cast_pos):
        if not self.unit_obj:
            return
        battle = self.unit_obj.get_battle()
        battle.add_mark(self.mark_id, cast_pos, self.owner_id)