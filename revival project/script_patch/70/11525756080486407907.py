# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_character_ctrl/ComStateData.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import mecha_const
from ....cdata.mecha_status_config import *
from common.utils.timer import CLOCK

class ComStateData(UnitCom):
    BIND_EVENT = {'E_JUMP_STAGE': 'set_jump_stage',
       'G_JUMP_STAGE': 'get_jump_stage',
       'E_ATTACK_STAGE': 'set_attack_stage',
       'G_ATTACK_STAGE': 'get_attack_stage',
       'E_ADVANCED_JUMP': 'set_advanced_jump',
       'G_ADVANCED_JUMP': 'get_advanced_jump',
       'E_BEGIN_ATTACK_STAGE': 'begin_clear_stage'
       }

    def __init__(self):
        super(ComStateData, self).__init__()
        self._attack_stage = 0
        self._advanced_jump = False
        self._stage_reset_timer = 0
        self._reset_time = 1.5
        self._reset_callback = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComStateData, self).init_from_dict(unit_obj, bdict)
        self._jump_stage = 0

    def on_init_complete(self):
        pass

    def destroy(self):
        self.clear_stage_timer()
        super(ComStateData, self).destroy()

    def set_jump_stage(self, stage):
        self._jump_stage = stage

    def get_jump_stage(self):
        return self._jump_stage

    def set_attack_stage(self, stage, auto_clear_stage=True):
        self._attack_stage = stage
        self.clear_stage_timer()
        if auto_clear_stage:
            self._stage_reset_timer = global_data.game_mgr.register_logic_timer(self.reset_stage, interval=self._reset_time, times=1, mode=CLOCK)

    def begin_clear_stage(self, callback=None):
        self.clear_stage_timer()
        self._reset_callback = callback
        self._stage_reset_timer = global_data.game_mgr.register_logic_timer(self.reset_stage, interval=self._reset_time, times=1, mode=CLOCK)

    def get_attack_stage(self):
        return self._attack_stage

    def set_advanced_jump(self, flag):
        self._advanced_jump = flag

    def get_advanced_jump(self):
        return self._advanced_jump

    def clear_stage_timer(self):
        if self._stage_reset_timer:
            global_data.game_mgr.unregister_logic_timer(self._stage_reset_timer)
            self._stage_reset_timer = 0

    def reset_stage(self):
        self._attack_stage = 0
        if self._reset_callback:
            self._reset_callback()