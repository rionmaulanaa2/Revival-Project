# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MutiOccupy/MutiOccupyData.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
from logic.comsys.battle import BattleUtils
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from logic.comsys.battle.Occupy.OccupyData import CPartData
from logic.comsys.battle.Death.DeathBattleData import DeathBattleData
from logic.gcommon.common_const.battle_const import STATE_OCCUPY_EMPTY, STATE_OCCUPY_SELF, STATE_OCCUPY_ENEMY, STATE_OCCUPY_SNATCH, OCCUPY_POINT_STATE_IDLE, OCCUPY_POINT_STATE_DEC, OCCUPY_POINT_STATE_INC

class SingleOccupy(object):

    def __init__(self):
        self.server_data = {}
        self.base_data = {}

    def init_data(self, data):
        if not data:
            return
        self.base_data['yaw'] = data['yaw']
        self.base_data['c_size'] = data['size']
        self.base_data['c_center'] = data['position']
        self.update_data(data)

    def update_data(self, data):
        lplayer = global_data.cam_lplayer
        group_id = None
        if lplayer:
            group_id = lplayer.ev_g_group_id()
        control_group_id = data.get('group_id', STATE_OCCUPY_EMPTY)
        if control_group_id == None:
            side = STATE_OCCUPY_EMPTY
        elif group_id == control_group_id:
            side = STATE_OCCUPY_SELF
        else:
            side = STATE_OCCUPY_ENEMY
        is_occupy = self.server_data.get('is_occupy', None)
        if is_occupy is not None and data.get('occupy', False) != is_occupy and data.get('occupy', False) == True:
            global_data.emgr.update_occupy_left_tips.emit(side, data.get('idx', '1'))
        self.server_data['idx'] = data.get('idx', '1')
        self.server_data['progress'] = data.get('progress', 0)
        self.server_data['group_id'] = side
        self.server_data['state'] = data.get('state', OCCUPY_POINT_STATE_IDLE)
        self.server_data['is_occupy'] = data.get('occupy', False)
        self.server_data['player_cnt'] = data.get('player_cnt', [])
        return

    def get_occupy_server_data(self):
        return self.server_data

    def get_occupy_base_data(self):
        return self.base_data

    def on_finalize(self):
        self.is_init = False
        self.base_data = {}
        self.server_data = {}


class MutiOccupyData(DeathBattleData):

    def init_parameters(self):
        super(MutiOccupyData, self).init_parameters()
        self.occupy_data = {}

    def init_occupy_data(self, occupy_point_dict):
        if not occupy_point_dict:
            return
        for idx, data in six.iteritems(occupy_point_dict):
            info = SingleOccupy()
            info.init_data(data)
            self.occupy_data[idx] = info

    def update_occupy_point_info(self, occupy_point_dict):
        if not occupy_point_dict:
            return
        for point_key, point_info in six.iteritems(occupy_point_dict):
            info = self.occupy_data.get(point_key)
            if not info:
                continue
            info.update_data(point_info)

        global_data.emgr.update_occupy_point_state.emit()

    def on_finalize(self):
        super(MutiOccupyData, self).on_finalize()
        for point_key, point_info in six.iteritems(self.occupy_data):
            point_info.on_finalize()

        self.occupy_data = {}