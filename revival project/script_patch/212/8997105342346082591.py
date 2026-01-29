# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impNewSysPrompt.py
from __future__ import absolute_import
from logic.gcommon import time_utility as tutil
import common.utils.timer as timer

class impNewSysPrompt(object):

    def _init_newsysprompt_from_dict(self, bdict):
        self._shown_system_tips = set(bdict.get('shown_system_tips', []))
        from logic.comsys.lobby.NewSystemOpenMgr import NewSystemOpenMgr
        inst = NewSystemOpenMgr()

    def _destroy_newsysprompt(self):
        self._shown_system_tips.clear()

    def mark_sys_prompt_read(self, sys_type):
        if not isinstance(sys_type, int):
            return
        if sys_type in self._shown_system_tips:
            return
        self.call_server_method('on_show_system_advance', (sys_type,))
        self._shown_system_tips.add(sys_type)

    def has_read_sys_prompt(self, sys_type):
        return sys_type in self._shown_system_tips