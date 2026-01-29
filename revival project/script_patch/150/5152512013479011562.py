# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/vibrate/VibrateMgr.py
from __future__ import absolute_import
import six
import game3d
import math3d
import world
from common.framework import Singleton
from logic.gcommon import time_utility
from common.cfg import confmgr

class VibrateMgr(Singleton):
    ALIAS_NAME = 'vibrate_mgr'

    def init(self):
        self._vibrate_allow_time_map = {}

    def start_vibrate(self, priority):
        cur_time = time_utility.time()
        for inner_priority, priority_cd in six.iteritems(self._vibrate_allow_time_map):
            if priority > inner_priority:
                continue
            elif priority_cd > cur_time:
                return

        vibrate_conf = confmgr.get('vibrate_conf')
        conf = vibrate_conf.get(str(priority), {})
        last_time = conf.get('fLastTime', 0)
        cd = conf.get('fCD', 0)
        if last_time:
            game3d.start_vibrate(int(last_time * 1000))
        if cd:
            self._vibrate_allow_time_map[int(priority)] = cur_time + cd