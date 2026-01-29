# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/SysMapPlayerMgr.py
from __future__ import absolute_import
from logic.vscene.part_sys.ScenePartSysBase import ScenePartSysBase

class SysMapPlayerMgr(ScenePartSysBase):

    def __init__(self):
        super(SysMapPlayerMgr, self).__init__()
        self._concerned_target_ids = []
        self.init_event()

    def init_event(self):
        pass

    def destroy(self):
        pass