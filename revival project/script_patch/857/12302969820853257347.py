# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impSpecEnlist.py
from __future__ import absolute_import
import six
import logic.gcommon.common_const.activity_const as acconst
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Str, Bool, Dict
from logic.gcommon import time_utility as tutil
from logic.gutils import activity_utils
from logic.gcommon.item import item_const

class impSpecEnlist(object):

    def _init_specenlist_from_dict(self, bdict):
        self.spec_enlist_from_uid = bdict.get('spec_enlist_from_uid', 0)
        self.spec_enlist_data = bdict.get('spec_enlist_data', {})
        self.spec_enlist_uids = [ int(uid) for uid in six.iterkeys(self.spec_enlist_data) ]
        self.spec_team_score = bdict.get('spec_team_score', 0)
        self.ai_help_score = bdict.get('ai_help_score', 0)
        self.spec_team_score = sum([ team_score for team_score in six.itervalues(self.spec_enlist_data) ])
        self.spec_enlist_score = len(self.spec_enlist_data) * 25
        self.total_spec_enlist_score = self.ai_help_score + self.spec_team_score + self.spec_enlist_score
        self.spec_enlist_reward_sts = set(bdict.get('spec_enlist_reward_sts', []))
        self.spec_enlist_verify_gift = bdict.get('spec_enlist_verify_gift', 0)
        self._enlist_reward_score = activity_utils.get_activity_conf_ui_data(acconst.ACTIVITY_KIZUNA_AI_RECRUIT, 'enlist_score', 25)

    def get_total_spec_enlist_score(self):
        return self.total_spec_enlist_score

    def get_spec_team_score(self):
        return self.spec_team_score

    def get_spec_enlist_score(self):
        return self.spec_enlist_score

    def get_ai_help_score(self):
        return self.ai_help_score

    def get_spec_enlist_uids(self):
        return self.spec_enlist_uids

    def has_spec_enlist_verify_gift(self):
        if not self.spec_enlist_verify_gift and self.spec_enlist_from_uid:
            return True
        return False

    def get_spec_enlist_from_uid(self):
        return self.spec_enlist_from_uid

    def get_spec_enlist_data(self, uid):
        return self.spec_enlist_data.get(str(uid), 0)

    def generate_spec_enlist_code(self):
        return hex(self.uid)[2:]

    def get_spec_enlist_reward_st(self, score):
        if score in self.spec_enlist_reward_sts:
            return item_const.ITEM_RECEIVED
        else:
            if score <= self.total_spec_enlist_score:
                return item_const.ITEM_UNRECEIVED
            return item_const.ITEM_UNGAIN

    def try_spec_enlist_from_code(self, enlist_code):
        self.call_server_method('try_spec_enlist_from_code', (enlist_code,))

    def query_ai_help_score(self):
        self.call_server_method('query_ai_help_score')

    @rpc_method(CLIENT_STUB, (Int('score'),))
    def update_ai_help_score(self, score):
        self.total_spec_enlist_score += score - self.ai_help_score
        self.ai_help_score = score
        global_data.emgr.message_on_spec_enlist_score.emit()

    @rpc_method(CLIENT_STUB, (Int('to_uid'),))
    def on_spec_enlist_succ(self, to_uid):
        self.spec_enlist_data[str(to_uid)] = 0
        if to_uid not in self.spec_enlist_uids:
            self.spec_enlist_uids.append(to_uid)
        self.total_spec_enlist_score += self._enlist_reward_score
        self.spec_enlist_score += self._enlist_reward_score
        global_data.emgr.message_on_spec_enlist_score.emit()

    @rpc_method(CLIENT_STUB, (Int('from_uid'),))
    def on_spec_enlist_verify(self, from_uid):
        if from_uid == -1:
            pass
        else:
            self.spec_enlist_from_uid = from_uid
        global_data.emgr.message_on_spec_enlist_verify.emit()

    @rpc_method(CLIENT_STUB, (Dict('team_data'),))
    def update_spec_enlist_team_score(self, team_data):
        self.spec_enlist_data.update(team_data)
        self.spec_team_score = sum([ team_score for team_score in six.itervalues(self.spec_enlist_data) ])
        self.total_spec_enlist_score = self.spec_team_score + self.ai_help_score + self.spec_enlist_score
        global_data.emgr.message_on_spec_enlist_score.emit()

    def receive_spec_enlist_reward(self, score):
        if score in self.spec_enlist_reward_sts:
            return
        if score > self.total_spec_enlist_score:
            return
        self.call_server_method('receive_spec_enlist_reward', (score,))

    @rpc_method(CLIENT_STUB, (Bool('ret'), Int('score')))
    def receive_spec_enlist_reward_ret(self, ret, score):
        if ret:
            self.spec_enlist_reward_sts.add(score)
        global_data.emgr.message_on_spec_enlist_reward.emit()

    def receive_spec_enlist_verify_gift(self):
        if self.spec_enlist_verify_gift or not self.spec_enlist_from_uid:
            return
        self.call_server_method('receive_spec_enlist_verify_gift')

    @rpc_method(CLIENT_STUB, (Int('reward_id'), Bool('ret')))
    def receive_spec_enlist_verify_gift_ret(self, reward_id, ret):
        if ret:
            self.spec_enlist_verify_gift = reward_id
        global_data.emgr.message_on_receive_newbie_enlist_bind_reward.emit()