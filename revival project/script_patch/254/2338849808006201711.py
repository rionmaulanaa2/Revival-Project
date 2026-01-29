# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impClanPoint.py
from __future__ import absolute_import
from common.cfg import confmgr
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Bool, Dict
from logic.gcommon.item import item_const
from logic.gcommon.cdata import clan_point_reward_conf as clan_conf

class impClanPoint(object):

    def _init_clanpoint_from_dict(self, bdict):
        self.clan_point = bdict.get('clan_point', 0)
        self.day_clan_point = bdict.get('day_clan_point', 0)
        self.day_clan_point_reward_record = bdict.get('day_clan_point_reward_record', {})
        self.week_clan_point = bdict.get('week_clan_point', 0)
        self.week_clan_point_reward_record = bdict.get('week_clan_point_reward_record', {})

    def get_day_clan_point(self):
        return self.day_clan_point

    def get_day_clan_reward_st(self, lv):
        reward_point = clan_conf.get_day_reward_point(lv)
        if str(lv) in self.day_clan_point_reward_record:
            return self.day_clan_point_reward_record[str(lv)]
        else:
            if self.day_clan_point < reward_point:
                return item_const.ITEM_UNGAIN
            return item_const.ITEM_UNRECEIVED

    def get_week_clan_point(self):
        return self.week_clan_point

    def get_week_clan_reward_st(self, lv):
        reward_point = clan_conf.get_week_reward_point(lv)
        if str(lv) in self.week_clan_point_reward_record:
            return self.week_clan_point_reward_record[str(lv)]
        else:
            if self.week_clan_point < reward_point:
                return item_const.ITEM_UNGAIN
            return item_const.ITEM_UNRECEIVED

    def receive_day_clan_point_reward(self, lv):
        reward_st = self.get_day_clan_reward_st(lv)
        if reward_st != item_const.ITEM_UNRECEIVED:
            return
        self.call_server_method('receive_day_clan_reward', (int(lv),))

    def receive_week_clan_point_reward(self, lv):
        reward_st = self.get_week_clan_reward_st(lv)
        if reward_st != item_const.ITEM_UNRECEIVED:
            return
        self.call_server_method('receive_week_clan_reward', (int(lv),))

    @rpc_method(CLIENT_STUB, (Int('lv'), Bool('ret')))
    def receive_day_clan_reward_ret(self, lv, ret):
        if ret:
            self.day_clan_point_reward_record[str(lv)] = item_const.ITEM_RECEIVED
            global_data.emgr.clan_task_day_reward.emit()

    @rpc_method(CLIENT_STUB, (Int('lv'), Bool('ret')))
    def receive_week_clan_reward_ret(self, lv, ret):
        if ret:
            self.week_clan_point_reward_record[str(lv)] = item_const.ITEM_RECEIVED
            global_data.emgr.clan_task_week_reward.emit()

    @rpc_method(CLIENT_STUB, (Int('day_clan_point'),))
    def reset_day_clan_point(self, day_clan_point):
        self.day_clan_point = day_clan_point
        global_data.emgr.clan_task_day_reward.emit()

    @rpc_method(CLIENT_STUB, (Int('week_clan_point'), Dict('reward_record')))
    def reset_week_clan_point(self, week_clan_point, reward_record):
        self.week_clan_point = week_clan_point
        self.week_clan_point_reward_record = reward_record
        global_data.emgr.clan_task_week_reward.emit()