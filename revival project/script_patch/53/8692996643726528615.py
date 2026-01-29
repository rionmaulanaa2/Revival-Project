# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterStateLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
from logic.gcommon.common_const.character_anim_const import LOW_BODY
from logic.gcommon.cdata.pve_monster_status_config import MC_STAND
from common.utils.timer import CLOCK
from logic.gcommon.behavior.StateLogic import Die
import math3d

class MonsterBornBase(MonsterStateBase):
    B_SFX = 'effect/fx/monster/pve/monster_born.sfx'
    SOCKET = 'fx_root'
    DUR = 3.0

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterBornBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()

    def init_params(self):
        pass

    def enter(self, leave_states):
        super(MonsterBornBase, self).enter(leave_states)
        if self.born_anim:
            self.send_event('E_ANIM_RATE', LOW_BODY, self.born_anim_rate)
            self.send_event('E_POST_ACTION', self.born_anim, LOW_BODY, 1)
        if self.sfx_path:
            model = self.ev_g_model()
            if not model or not model.valid:
                return

            def cb(sfx):
                if model and model.valid:
                    model.visible = True

            global_data.sfx_mgr.create_sfx_on_model(self.sfx_path, model, self.SOCKET, duration=self.DUR, on_create_func=cb)

    def check_transitions(self):
        if self.born_anim_dur and self.elapsed_time > self.born_anim_dur / self.born_anim_rate:
            self.disable_self()
            return MC_STAND


class MonsterBorn(MonsterBornBase):

    def init_params(self):
        super(MonsterBorn, self).init_params()
        self.sfx_path = self.custom_param.get('sfx_path', '')
        self.born_anim = self.custom_param.get('born_anim', None)
        self.born_anim_rate = self.custom_param.get('born_anim_rate', 1.0)
        self.born_anim_dur = self.custom_param.get('born_anim_dur', 0)
        return


class MonsterDieBase(Die):
    D_SFX = 'effect/fx/monster/pve/monster_dying.sfx'
    SOCKET = 'fx_root'
    DUR = 3.0

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterDieBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()

    def init_params(self):
        self.delay_timer = None
        return

    def enter--- This code section failed: ---

  79       0  LOAD_GLOBAL           0  'super'
           3  LOAD_GLOBAL           1  'MonsterDieBase'
           6  LOAD_FAST             0  'self'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             2  'enter'
          15  LOAD_FAST             1  'leave_states'
          18  CALL_FUNCTION_1       1 
          21  POP_TOP          

  80      22  LOAD_FAST             0  'self'
          25  LOAD_ATTR             3  'die_anim'
          28  POP_JUMP_IF_FALSE    81  'to 81'

  81      31  LOAD_FAST             0  'self'
          34  LOAD_ATTR             4  'send_event'
          37  LOAD_CONST            1  'E_ANIM_RATE'
          40  LOAD_GLOBAL           5  'LOW_BODY'
          43  LOAD_FAST             0  'self'
          46  LOAD_ATTR             6  'die_anim_rate'
          49  CALL_FUNCTION_3       3 
          52  POP_TOP          

  82      53  LOAD_FAST             0  'self'
          56  LOAD_ATTR             4  'send_event'
          59  LOAD_CONST            2  'E_POST_ACTION'
          62  LOAD_FAST             0  'self'
          65  LOAD_ATTR             3  'die_anim'
          68  LOAD_GLOBAL           5  'LOW_BODY'
          71  LOAD_CONST            3  1
          74  CALL_FUNCTION_4       4 
          77  POP_TOP          
          78  JUMP_FORWARD          0  'to 81'
        81_0  COME_FROM                '78'

  84      81  LOAD_FAST             0  'self'
          84  LOAD_ATTR             7  'sfx_path'
          87  POP_JUMP_IF_FALSE   154  'to 154'

  85      90  LOAD_FAST             0  'self'
          93  LOAD_ATTR             8  'sfx_delay'
          96  POP_JUMP_IF_FALSE   141  'to 141'

  86      99  LOAD_GLOBAL           9  'global_data'
         102  LOAD_ATTR            10  'game_mgr'
         105  LOAD_ATTR            11  'register_logic_timer'
         108  LOAD_FAST             0  'self'
         111  LOAD_ATTR            12  'play_sfx'
         114  LOAD_FAST             0  'self'
         117  LOAD_ATTR             8  'sfx_delay'
         120  LOAD_CONST            0  ''
         123  LOAD_CONST            3  1
         126  LOAD_GLOBAL          14  'CLOCK'
         129  CALL_FUNCTION_5       5 
         132  LOAD_FAST             0  'self'
         135  STORE_ATTR           15  'delay_timer'
         138  JUMP_ABSOLUTE       154  'to 154'

  88     141  LOAD_FAST             0  'self'
         144  LOAD_ATTR            12  'play_sfx'
         147  CALL_FUNCTION_0       0 
         150  POP_TOP          
         151  JUMP_FORWARD          0  'to 154'
       154_0  COME_FROM                '151'

  90     154  LOAD_GLOBAL          16  'getattr'
         157  LOAD_GLOBAL           4  'send_event'
         160  LOAD_CONST            0  ''
         163  CALL_FUNCTION_3       3 
         166  POP_JUMP_IF_FALSE   215  'to 215'

  92     169  LOAD_GLOBAL           9  'global_data'
         172  LOAD_ATTR            17  'player'
         175  LOAD_ATTR            18  'get_battle'
         178  CALL_FUNCTION_0       0 
         181  LOAD_ATTR            19  'call_soul_method'
         184  LOAD_CONST            5  'call_sync_show_level_tip'
         187  LOAD_FAST             0  'self'
         190  LOAD_ATTR            20  'tip_type'
         193  LOAD_FAST             0  'self'
         196  LOAD_ATTR            21  'tip_text'
         199  LOAD_FAST             0  'self'
         202  LOAD_ATTR            22  'tip_text_2'
         205  BUILD_TUPLE_3         3 
         208  CALL_FUNCTION_2       2 
         211  POP_TOP          
         212  JUMP_FORWARD          0  'to 215'
       215_0  COME_FROM                '212'
         215  LOAD_CONST            0  ''
         218  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 163

    def exit(self, enter_states):
        super(MonsterDieBase, self).exit(enter_states)
        self.send_event('E_ON_STATE_EXIT', self.sid)

    def play_sfx(self):
        if self.sfx_path:
            model = self.ev_g_model()
            if not model:
                return
            global_data.sfx_mgr.create_sfx_on_model(self.sfx_path, model, self.SOCKET, duration=self.DUR)

    def destroy(self):
        super(MonsterDieBase, self).destroy()
        if self.delay_timer:
            global_data.game_mgr.unregister_logic_timer(self.delay_timer)
            self.delay_timer = None
        return


class MonsterDie(MonsterDieBase):

    def init_params(self):
        super(MonsterDie, self).init_params()
        self.sfx_path = self.custom_param.get('sfx_path', '')
        self.sfx_delay = self.custom_param.get('sfx_delay', 0)
        self.die_anim = self.custom_param.get('die_anim', None)
        self.die_anim_rate = self.custom_param.get('die_anim_rate', 1.0)
        self.tip_type = self.custom_param.get('tip_type', None)
        self.tip_text = self.custom_param.get('tip_text', None)
        self.tip_text_2 = self.custom_param.get('tip_text_2', 0)
        return


class MonsterBoomDie(MonsterDieBase):

    def init_params(self):
        super(MonsterBoomDie, self).init_params()
        self.sfx_path = self.custom_param.get('sfx_path', '')
        self.sfx_delay = self.custom_param.get('sfx_delay', 0)
        self.die_anim = self.custom_param.get('die_anim', None)
        self.die_anim_rate = self.custom_param.get('die_anim_rate', 1.0)
        self.boom_skill_id = self.custom_param.get('boom_skill_id', 0)
        self.boom_delay = self.custom_param.get('boom_delay', 0)
        self.boom_delay_timer = None
        return

    def enter(self, *args):
        super(MonsterBoomDie, self).enter(*args)
        if self.boom_skill_id:
            if self.boom_delay:
                self.boom_delay_timer = global_data.game_mgr.register_logic_timer(self.post_boom, self.boom_delay, None, 1, CLOCK)
            else:
                self.post_boom()
        return

    def post_boom(self):
        self.send_event('E_DO_SKILL', self.boom_skill_id)

    def destroy(self):
        super(MonsterBoomDie, self).destroy()
        if self.boom_delay_timer:
            global_data.game_mgr.unregister_logic_timer(self.boom_delay_timer)
            self.boom_delay_timer = None
        return


class MonsterEscapeBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }
    econf = {}
    DUR = 3.0

    def pre_check_param(self, state, *args):
        if state != self.sid:
            return
        else:
            if self.is_active:
                return False
            if not self.check_can_active():
                return False
            self.skill_id, self.target_id, self.target_pos = args
            self.target_pos = math3d.vector(*self.target_pos) if self.target_pos else None
            self.active_self()
            return

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterEscapeBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        is_bind and emgr.bind_events(self.econf) if 1 else emgr.unbind_events(self.econf)

    def init_params(self):
        self.delay_timer = None
        return

    def enter--- This code section failed: ---

 191       0  LOAD_GLOBAL           0  'super'
           3  LOAD_GLOBAL           1  'MonsterEscapeBase'
           6  LOAD_FAST             0  'self'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             2  'enter'
          15  LOAD_FAST             1  'leave_states'
          18  CALL_FUNCTION_1       1 
          21  POP_TOP          

 192      22  LOAD_FAST             0  'self'
          25  LOAD_ATTR             3  'escape_anim'
          28  POP_JUMP_IF_FALSE    81  'to 81'

 193      31  LOAD_FAST             0  'self'
          34  LOAD_ATTR             4  'send_event'
          37  LOAD_CONST            1  'E_ANIM_RATE'
          40  LOAD_GLOBAL           5  'LOW_BODY'
          43  LOAD_FAST             0  'self'
          46  LOAD_ATTR             6  'escape_anim_rate'
          49  CALL_FUNCTION_3       3 
          52  POP_TOP          

 194      53  LOAD_FAST             0  'self'
          56  LOAD_ATTR             4  'send_event'
          59  LOAD_CONST            2  'E_POST_ACTION'
          62  LOAD_FAST             0  'self'
          65  LOAD_ATTR             3  'escape_anim'
          68  LOAD_GLOBAL           5  'LOW_BODY'
          71  LOAD_CONST            3  1
          74  CALL_FUNCTION_4       4 
          77  POP_TOP          
          78  JUMP_FORWARD          0  'to 81'
        81_0  COME_FROM                '78'

 196      81  LOAD_FAST             0  'self'
          84  LOAD_ATTR             7  'sfx_path'
          87  POP_JUMP_IF_FALSE   154  'to 154'

 197      90  LOAD_FAST             0  'self'
          93  LOAD_ATTR             8  'sfx_delay'
          96  POP_JUMP_IF_FALSE   141  'to 141'

 198      99  LOAD_GLOBAL           9  'global_data'
         102  LOAD_ATTR            10  'game_mgr'
         105  LOAD_ATTR            11  'register_logic_timer'
         108  LOAD_FAST             0  'self'
         111  LOAD_ATTR            12  'play_sfx'
         114  LOAD_FAST             0  'self'
         117  LOAD_ATTR             8  'sfx_delay'
         120  LOAD_CONST            0  ''
         123  LOAD_CONST            3  1
         126  LOAD_GLOBAL          14  'CLOCK'
         129  CALL_FUNCTION_5       5 
         132  LOAD_FAST             0  'self'
         135  STORE_ATTR           15  'delay_timer'
         138  JUMP_ABSOLUTE       154  'to 154'

 200     141  LOAD_FAST             0  'self'
         144  LOAD_ATTR            12  'play_sfx'
         147  CALL_FUNCTION_0       0 
         150  POP_TOP          
         151  JUMP_FORWARD          0  'to 154'
       154_0  COME_FROM                '151'

 202     154  LOAD_GLOBAL          16  'getattr'
         157  LOAD_GLOBAL           4  'send_event'
         160  LOAD_CONST            0  ''
         163  CALL_FUNCTION_3       3 
         166  POP_JUMP_IF_FALSE   215  'to 215'

 204     169  LOAD_GLOBAL           9  'global_data'
         172  LOAD_ATTR            17  'player'
         175  LOAD_ATTR            18  'get_battle'
         178  CALL_FUNCTION_0       0 
         181  LOAD_ATTR            19  'call_soul_method'
         184  LOAD_CONST            5  'call_sync_show_level_tip'
         187  LOAD_FAST             0  'self'
         190  LOAD_ATTR            20  'tip_type'
         193  LOAD_FAST             0  'self'
         196  LOAD_ATTR            21  'tip_text'
         199  LOAD_FAST             0  'self'
         202  LOAD_ATTR            22  'tip_text_2'
         205  BUILD_TUPLE_3         3 
         208  CALL_FUNCTION_2       2 
         211  POP_TOP          
         212  JUMP_FORWARD          0  'to 215'
       215_0  COME_FROM                '212'
         215  LOAD_CONST            0  ''
         218  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 163

    def exit(self, enter_states):
        super(MonsterEscapeBase, self).exit(enter_states)

    def play_sfx(self):
        if self.sfx_path:
            model = self.ev_g_model()
            if not model:
                return
            global_data.sfx_mgr.create_sfx_on_model(self.sfx_path, model, self.sfx_socket, duration=self.DUR)

    def destroy(self):
        super(MonsterEscapeBase, self).destroy()
        self.process_event(False)
        if self.delay_timer:
            global_data.game_mgr.unregister_logic_timer(self.delay_timer)
            self.delay_timer = None
        return


class MonsterEscape(MonsterEscapeBase):

    def init_params(self):
        super(MonsterEscape, self).init_params()
        self.sfx_path = self.custom_param.get('sfx_path', None)
        self.sfx_socket = self.custom_param.get('sfx_socket', None)
        self.sfx_delay = self.custom_param.get('sfx_delay', 0)
        self.escape_anim = self.custom_param.get('escape_anim', '')
        self.escape_anim_rate = self.custom_param.get('escape_anim_rate', 1.0)
        self.tip_type = self.custom_param.get('tip_type', None)
        self.tip_text = self.custom_param.get('tip_text', None)
        self.tip_text_2 = self.custom_param.get('tip_text_2', 0)
        return