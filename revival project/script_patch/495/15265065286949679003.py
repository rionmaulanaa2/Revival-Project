# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/gvg/GVGBattleData.py
from __future__ import absolute_import
import six
from common.framework import Singleton
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.client.const import game_mode_const
from common.utils import timer
import cc

class GVGBattleData(Singleton):
    ALIAS_NAME = 'gvg_battle_data'

    def init(self):
        self.init_parameters()

    def init_parameters(self):
        self.settle_timestamp = None
        self.area_id = None
        self.mecha_use_dict = {}
        self.mecha_revice_ts_dict = {}
        self.score_details_dict = {}
        return

    def on_finalize(self):
        self.init_parameters()

    def set_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = settle_timestamp
        global_data.emgr.update_battle_timestamp.emit(settle_timestamp)

    def set_area_id(self, area_id):
        self.area_id = area_id

    def set_mecha_destroyed(self, soul_id, mecha_idx, mecha_revice_ts):
        self.mecha_use_dict[soul_id] = mecha_idx + 1
        self.mecha_revice_ts_dict[soul_id] = mecha_revice_ts
        global_data.emgr.update_battle_data.emit()

    def update_battle_data(self, mecha_use_dict, mecha_revice_ts_dict):
        self.mecha_use_dict = mecha_use_dict
        self.mecha_revice_ts_dict = mecha_revice_ts_dict
        global_data.emgr.update_battle_data.emit()

    def somebody_is_over(self, soul_id):
        return self.mecha_use_dict.get(soul_id, 0) >= game_mode_const.GVG_MECHA_NUM

    def player_req_spectate(self):
        if not (global_data.player and global_data.player.logic):
            return
        if global_data.player.is_in_global_spectate():
            return
        if self.somebody_is_over(global_data.player.id):
            global_data.player.logic.send_event('E_REQ_SPECTATE')

    def update_score_details_data(self, data):
        self.score_details_dict = data
        global_data.emgr.update_score_details.emit(data)

    def get_score_details_data(self):
        return self.score_details_dict

    def update_spawn_rebirth_data(self, data):
        for key in six.iterkeys(data):
            self.spawn_rebirth_dict[key] = data[key]

    def get_spawn_rebirth_data(self, spwan_id):
        return self.spawn_rebirth_dict.get(spwan_id, [0, 0])