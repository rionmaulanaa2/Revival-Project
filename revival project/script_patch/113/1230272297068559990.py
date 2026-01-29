# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/live/live_agent_interface.py
from __future__ import absolute_import
from common.framework import Singleton
import logic.gcommon.const as const
import json
import time
import common.utils.timer as timer
import game3d
import voice
import os

class LiveAgentInterface(object):

    def __init__(self):
        self._player = None
        self._live_data = {}
        return

    def init(self, live_data):
        self._live_data = live_data

    def play_live(self, url):
        pass

    def login(self, usr_name, password):
        pass

    def get_vbr_list(self):
        pass

    def set_vbr(self, vbr_str):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def clear_live_room_msg(self):
        pass

    def stop(self):
        pass

    def set_volume(self, vol):
        pass

    def fetch_data_provider(self):
        pass

    def destroy(self):
        self._player = None
        return

    def sub_msg(self):
        pass

    def unsub_msg(self):
        pass

    def send_live_dammu(self, msg):
        pass