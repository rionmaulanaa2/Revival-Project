# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/live/douyulive_agent.py
from __future__ import absolute_import
from .live_agent_interface import LiveAgentInterface
from .ccbased_live_agent import CCBasedLiveAgent
import json
from logic.gcommon.common_const import liveshow_const

class DouyuLiveAgent(CCBasedLiveAgent):

    def __init__(self):
        super(DouyuLiveAgent, self).__init__()

    def init(self, live_data):
        super(DouyuLiveAgent, self).init(live_data)

    def destroy(self):
        super(DouyuLiveAgent, self).destroy()

    def play_live(self, url):
        self._player.play_vod(url)

    def login(self, usr_name, password):
        pass

    def _get_vbr_list_callback(self, player, cur_vbr, available_vbr_list):
        pass