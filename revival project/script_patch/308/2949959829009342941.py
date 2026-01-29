# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDataLogicLod.py
from __future__ import absolute_import
from logic.gcommon.component.share.ComDataBase import ComDataBase

class ComDataLogicLod(ComDataBase):

    def get_share_data_name(self):
        return 'ref_logic_lod'

    def __init__(self):
        super(ComDataLogicLod, self).__init__()
        self.logic_tick_step = 0
        self.dt_full_fps = 0
        self.dt_30_fps = 0
        self.need_tick = True
        self.need_tick_30fps = True
        self.calc_flag = 0

    def _do_cache(self):
        self.logic_tick_step = 0
        self.dt_full_fps = 0
        self.dt_30_fps = 0

    def _do_destroy(self):
        self.logic_tick_step = 0
        self.dt_full_fps = 0
        self.dt_30_fps = 0

    def activate_ecs(self):
        self.logic_tick_step = 0
        self.dt_full_fps = 0
        self.dt_30_fps = 0
        super(ComDataLogicLod, self).activate_ecs()

    def deactivate_ecs(self):
        self.logic_tick_step = 0
        self.dt_full_fps = 0
        self.dt_30_fps = 0
        super(ComDataLogicLod, self).deactivate_ecs()