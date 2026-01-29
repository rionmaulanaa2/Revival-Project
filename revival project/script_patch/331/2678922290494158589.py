# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Occupy/OccupyData.py
from __future__ import absolute_import
import six
import six_ex
from common.cfg import confmgr
from logic.comsys.battle.Death.DeathBattleData import DeathBattleData
PART_LOCK = -2
PART_FIGHT = -1
PART_NO_SIDE = 0
PART_MY_SIDE = 1
PART_E_ONE_SIDE = 2

class CPartData(object):

    def __init__(self, part_id):
        self.part_id = part_id
        self.init_parameters()

    def init_parameters(self):
        self.control_side = PART_NO_SIDE
        self.data = None
        return

    def set_data(self, data):
        self.data = data
        lplayer = global_data.cam_lplayer
        group_id = None
        if lplayer:
            group_id = lplayer.ev_g_group_id()
        control_group_id = self.data.get('control_group_id', PART_NO_SIDE)
        if control_group_id > 0:
            side = PART_MY_SIDE if group_id == control_group_id else PART_E_ONE_SIDE
        else:
            side = control_group_id
        self.control_side = side
        return


class OccupyData(DeathBattleData):

    def init_parameters(self):
        self.part_data = {}
        super(OccupyData, self).init_parameters()
        self.show_remind_point = {}
        self.show_remind_ani = False

    def update_control_point(self, control_point_dict):
        new_controls = set(six_ex.keys(control_point_dict))
        cur_controls = set(six_ex.keys(self.part_data))
        del_controls = cur_controls - new_controls
        for part_id in del_controls:
            del self.part_data[part_id]

        for part_id, data in six.iteritems(control_point_dict):
            if part_id not in self.part_data:
                self.part_data[part_id] = CPartData(part_id)
            self.part_data[part_id].set_data(data)

        global_data.emgr.update_control_point.emit()

    def get_part_data(self, part_id):
        if part_id not in self.part_data:
            return {}
        return self.part_data[part_id].data