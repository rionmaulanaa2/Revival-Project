# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impLuckScore.py
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Str, Dict
from common.cfg import confmgr

class impLuckScore(object):

    def _init_luckscore_from_dict(self, bdict):
        self.luck_score_likes_list = {}
        self.total_luck_dict = bdict.get('total_luck_dict', {})
        self.week_luck_dict = bdict.get('week_luck_dict', {})
        self.lucky_dog_times = bdict.get('lucky_dog_times', {})

    def get_luck_score_likes_data(self, reward_id, luck_type):
        return self.luck_score_likes_list.get(reward_id, {}).get(luck_type, {})

    def get_my_total_luck_dict(self, item_no=None):
        if not item_no:
            return {}
        return self.total_luck_dict.get(str(item_no), {})

    def get_my_week_luck_dict(self, item_no=None):
        if not item_no:
            return {}
        return self.week_luck_dict.get(str(item_no), {})

    def get_total_luck_by_reward_id(self, reward_id):
        return self.total_luck_dict.setdefault(str(reward_id), {})

    @rpc_method(CLIENT_STUB, (Int('reward_id'), Str('luck_type'), Dict('result')))
    def on_request_rank_likes(self, reward_id, luck_type, result):
        self.luck_score_likes_list.setdefault(reward_id, {}).setdefault(luck_type, {})
        for uid, data in result.items():
            self.luck_score_likes_list[reward_id][luck_type][uid] = {'like_num': data['like_num'],'liked': data['liked']}

        global_data.emgr.message_on_luck_rank_like_data.emit(luck_type)

    @rpc_method(CLIENT_STUB, (Int('target_uid'), Int('reward_id'), Str('luck_type')))
    def on_request_luck_rank_like(self, target_uid, reward_id, luck_type):
        self.request_rank_all_likes([target_uid], reward_id, luck_type)

    @rpc_method(CLIENT_STUB, (Int('target_uid'), Int('reward_id'), Str('luck_type')))
    def on_request_luck_rank_unlike(self, target_uid, reward_id, luck_type):
        self.request_rank_all_likes([target_uid], reward_id, luck_type)

    @rpc_method(CLIENT_STUB, (Int('reward_id'), Int('luck_score'), Dict('total_luck')))
    def update_total_luck_dict(self, reward_id, luck_score, total_luck):
        timestamp = total_luck.get('timestamp', 0)
        item_list = total_luck.get('item_list', {})
        luck_intervene_weight = total_luck.get('luck_intervene_weight', {})
        luck_exceed_percent = total_luck.get('luck_exceed_percent', 0)
        total_luck_dict = self.total_luck_dict.get(str(reward_id), {})
        total_luck_dict['luck_score'] = luck_score
        total_luck_dict['item_list'] = item_list
        total_luck_dict['timestamp'] = timestamp
        total_luck_dict['luck_intervene_weight'] = luck_intervene_weight
        total_luck_dict['luck_exceed_percent'] = luck_exceed_percent

    @rpc_method(CLIENT_STUB, (Int('reward_id'), Int('luck_score'), Dict('week_luck')))
    def update_week_luck_dict(self, reward_id, luck_score, week_luck):
        timestamp = week_luck.get('timestamp', 0)
        item_list = week_luck.get('item_list', {})
        luck_intervene_weight = week_luck.get('luck_intervene_weight', {})
        luck_exceed_percent = week_luck.get('luck_exceed_percent', 0)
        week_luck_dict = self.week_luck_dict.get(str(reward_id), {})
        week_luck_dict['luck_score'] = luck_score
        week_luck_dict['item_list'] = item_list
        week_luck_dict['timestamp'] = timestamp
        week_luck_dict['luck_intervene_weight'] = luck_intervene_weight
        week_luck_dict['luck_exceed_percent'] = luck_exceed_percent

    @rpc_method(CLIENT_STUB, (Int('lucky_dog_times'),))
    def update_lucky_dog_times(self, lucky_dog_times):
        self.lucky_dog_times = lucky_dog_times

    def request_luck_rank_like(self, uid, reward_id, luck_type):
        self.call_server_method('request_luck_rank_like', (uid, reward_id, luck_type))

    def request_luck_rank_unlike(self, uid, reward_id, luck_type):
        self.call_server_method('request_luck_rank_unlike', (uid, reward_id, luck_type))

    def request_rank_all_likes(self, uid_list, reward_id, luck_type):
        self.call_server_method('request_rank_all_likes', (uid_list, reward_id, luck_type))