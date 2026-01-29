# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/live/ccbased_live_agent.py
from __future__ import absolute_import
from .live_agent_interface import LiveAgentInterface
import json
from logic.gcommon.common_const import liveshow_const

class CCBasedLiveAgent(LiveAgentInterface):

    def __init__(self):
        super(CCBasedLiveAgent, self).__init__()
        import cclive
        self._player = cclive.player()
        self._set_up_callback()

    def init(self, live_data):
        super(CCBasedLiveAgent, self).init(live_data)

    def destroy(self):
        super(CCBasedLiveAgent, self).destroy()
        self._clear_callback()

    def play_live(self, url):
        self._player.play_vod(url)

    def login(self, usr_name, password):
        pass

    def get_vbr_list(self):
        source_list = self._live_data.get('source')
        cur_vbr = ''
        cur_url = ''
        available_vbr_list = []
        for sour in source_list:
            if not cur_url:
                cur_vbr = sour.get('vbr_channel')
                cur_url = sour.get('mobile_url')
            available_vbr_list.append(sour.get('vbr_channel'))

        global_data.emgr.live_url_change_event.emit(cur_url)
        global_data.emgr.live_get_vbr_list_event.emit(cur_vbr, available_vbr_list)

    def set_vbr(self, vbr_str):
        source_list = self._live_data.get('source')
        for sour in source_list:
            cur_vbr = sour.get('vbr_channel')
            if cur_vbr == vbr_str:
                cur_url = sour.get('mobile_url')
                global_data.emgr.live_vbr_change_event.emit(vbr_str)
                global_data.emgr.live_url_change_event.emit(cur_url)

    def pause(self):
        self._player.pause()

    def resume(self):
        self._player.resume()

    def stop(self):
        self._player.stop()

    def set_volume(self, vol):
        self._player.set_voume(vol)

    def fetch_data_provider(self):
        return self._player.fetch_data_provider()

    def _set_up_callback(self):
        self._player.get_vbr_list_callback = self._get_vbr_list_callback
        self._player.error_callback = self._error_callback
        self._player.video_ready_callback = self._video_ready_callback
        self._player.video_complete_callback = self._video_complete_callback
        self._player.report_stat_callback = self._report_stat_callback
        self._player.seek_complete_callback = self._seek_complete_callback

    def _clear_callback(self):
        if self._player:
            self._player.get_vbr_list_callback = None
            self._player.error_callback = None
            self._player.video_ready_callback = None
            self._player.video_complete_callback = None
            self._player.report_stat_callback = None
            self._player.seek_complete_callback = None
        return

    def _video_ready_callback(self, player):
        global_data.emgr.live_ready_event.emit()

    def _video_complete_callback(self, player):
        global_data.emgr.live_complete_event.emit()

    def _report_stat_callback(self, player, url):
        global_data.emgr.live_report_stat_event.emit()

    def _seek_complete_callback(self, player):
        global_data.emgr.live_seek_complete_event.emit()

    def _error_callback(self, player):
        global_data.emgr.live_error_event.emit()

    def _get_vbr_list_callback(self, player, cur_vbr, available_vbr_list):
        global_data.emgr.live_get_vbr_list_event.emit(cur_vbr, available_vbr_list)