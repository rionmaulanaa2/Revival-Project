# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/live/live_agent_mgr.py
from __future__ import absolute_import
from common.framework import Singleton
from logic.gcommon.common_const import liveshow_const
from .cclive_agent import CCLiveAgent
from .huyalive_agent import HuyaLiveAgent
from .douyulive_agent import DouyuLiveAgent
from .blbl_live_agent import BLBLLiveAgent
from .kuaishou_live_agent import KuaiShouLiveAgent
agent_factory = {liveshow_const.CC_LIVE: CCLiveAgent,
   liveshow_const.HUYA_LIVE: HuyaLiveAgent,
   liveshow_const.DOUYU_LIVE: DouyuLiveAgent,
   liveshow_const.BILIBILI_LIVE: BLBLLiveAgent,
   liveshow_const.KUAISHOU_LIVE: KuaiShouLiveAgent
   }

class LiveAgentMgr(Singleton):

    def init(self):
        self._live_agent = None
        self.cur_live_agent_type = None
        self._has_channel_login = {}
        return

    def destroy(self):
        if self._live_agent:
            self._live_agent.destroy()
            self._live_agent = None
            self.cur_live_agent_type = None
        return

    def get_live_agent(self):
        return self._live_agent

    def switch_live_agent(self, live_type, live_data):
        if self._live_agent:
            self._live_agent.destroy()
            self._live_agent = None
            self._has_channel_login[live_type] = False
        agent_class = agent_factory.get(live_type)
        if agent_class:
            self._live_agent = agent_class()
            self.cur_live_agent_type = live_type
        self._live_agent.init(live_data)
        if not self._has_channel_login.get(live_type, False):
            self._has_channel_login[live_type] = True
            user_name = self.generate_cc_channel_account_id()
            self._live_agent.login(user_name, '')
        return

    def generate_cc_channel_account_id(self):
        channel = global_data.channel
        if not channel:
            return ''
        else:
            guest_uid = channel.get_prop_str('ORIGIN_GUEST_UID')
            if guest_uid != '':
                uid = guest_uid
                return '%s@%s.%s.win.163.com' % (uid, channel.platform, channel.name)
            uid = channel.get_prop_str('UID')
            return '%s@%s.%s.sdk.ano.163.com' % (uid, channel.platform, channel.name)