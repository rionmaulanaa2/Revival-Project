# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/career/CareerBadgePromptMgr.py
from __future__ import absolute_import
from common.framework import Singleton

class CareerBadgePromptMgr(Singleton):
    ALIAS_NAME = 'career_badge_prompt_mgr'

    def init(self):
        self._msg_list = []

    def on_finalize(self):
        del self._msg_list[:]

    def push(self, msg):
        self._msg_list.extend(msg)

    def play(self, finish_cb=None):
        from logic.gutils import career_utils
        medals, non_medals = career_utils.filter_out_medal_badge(self._msg_list)
        if non_medals:
            inst = global_data.ui_mgr.get_ui('CareerBadgePromptUI')
            if not inst:
                inst = global_data.ui_mgr.show_ui('CareerBadgePromptUI', 'logic.comsys.career')
            inst.push(non_medals)
        if medals:
            inst = global_data.ui_mgr.get_ui('CareerBadgePromptUI')
            if not inst:
                inst = global_data.ui_mgr.show_ui('CareerBadgePromptUI', 'logic.comsys.career')
            inst.push(medals)
        inst = global_data.ui_mgr.get_ui('CareerBadgePromptUI')
        if inst:
            inst.set_finish_cb(finish_cb)
        elif callable(finish_cb):
            finish_cb()
        del self._msg_list[:]