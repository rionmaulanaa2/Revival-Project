# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impNewbieEnlist.py
from __future__ import absolute_import
import six
import logic.gcommon.common_const.activity_const as acconst
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Str, Bool, Dict
from logic.gcommon import time_utility as tutil
from logic.gutils import activity_utils
from logic.gcommon.item import item_const
import six_ex
from logic.gcommon.common_utils.local_text import get_text_by_id

class impNewbieEnlist(object):

    def _init_newbieenlist_from_dict(self, bdict):
        self.newbie_enlist_data = bdict.get('newbie_enlist_data', {})

    def get_newbie_enlist_data(self, scope):
        return self.newbie_enlist_data.get(scope, {})

    def get_newbie_enlist_code(self, scope):
        newbie_enlist_data = self.get_newbie_enlist_data(scope)
        return newbie_enlist_data.get(scope, {}).get('code', 0)

    def check_is_newbie_on_start(self, scope):
        newbie_enlist_data = self.get_newbie_enlist_data(scope)
        return newbie_enlist_data.get('is_newbie_on_start', 0)

    def get_newbie_enlist_from_uid(self, scope):
        newbie_enlist_data = self.get_newbie_enlist_data(scope)
        return newbie_enlist_data.get('enlist_from_uid', 0)

    def get_binding_newbie_enlist_score(self, scope):
        newbie_enlist_data = self.get_newbie_enlist_data(scope)
        return newbie_enlist_data.get('enlist_newbie_score', 0)

    def check_binding_reward_has_receive(self, scope, score):
        newbie_enlist_data = self.get_newbie_enlist_data(scope)
        if score in newbie_enlist_data.get('enlist_newbie_reward_sts', []):
            return True
        else:
            return False

    def get_recruit_newbie_enlist_score(self, scope):
        enlist_score = activity_utils.get_activity_conf_ui_data(scope, 'enlist_score', 10)
        max_team_score = activity_utils.get_activity_conf_ui_data(scope, 'max_team_score', 50)
        newbie_enlist_data = self.get_newbie_enlist_data(scope)
        enlist_data = newbie_enlist_data.get('enlist_data', {})
        return sum(six_ex.values(enlist_data)) + min(max_team_score, len(enlist_data) * enlist_score)

    def get_recruit_newbie_enlist_uid_list(self, scope):
        newbie_enlist_data = self.get_newbie_enlist_data(scope)
        return six_ex.keys(newbie_enlist_data.get('enlist_data', {}))

    def get_recruit_newbie_enlist_count(self, scope):
        newbie_enlist_enlist_uid_list = self.get_recruit_newbie_enlist_uid_list(scope)
        return len(newbie_enlist_enlist_uid_list)

    def get_recruit_newbie_enlist_data(self, scope, uid):
        newbie_enlist_data = self.get_newbie_enlist_data(scope)
        return newbie_enlist_data.get('enlist_data', {}).get(uid, 0)

    def check_recruit_reward_has_receive(self, scope, score):
        newbie_enlist_data = self.get_newbie_enlist_data(scope)
        if score in newbie_enlist_data.get('enlist_reward_sts', []):
            return True
        else:
            return False

    def try_newbie_enlist_from_code(self, scope, enlist_code):
        print (
         'try_newbie_enlist_from_code', str(scope), enlist_code)
        self.call_server_method('try_newbie_enlist_from_code', (str(scope), enlist_code))

    def receive_newbie_enlist_bind_reward(self, scope, score):
        print (
         'receive_newbie_enlist_bind_reward', (scope, score))
        self.call_server_method('receive_newbie_enlist_bind_reward', (scope, score))

    def receive_newbie_enlist_reward(self, scope, score):
        print (
         'receive_newbie_enlist_reward', (scope, score))
        self.call_server_method('receive_newbie_enlist_reward', (scope, score))

    @rpc_method(CLIENT_STUB, (Str('scope'), Int('from_uid')))
    def on_newbie_enlist_verify(self, scope, from_uid):
        print ('message_on_newbie_enlist_verify', scope, from_uid)
        if from_uid <= 0:
            if from_uid == -1:
                global_data.game_mgr.show_tip(get_text_by_id(634840))
            elif from_uid == -4:
                global_data.game_mgr.show_tip(get_text_by_id(634839))
            else:
                global_data.game_mgr.show_tip(get_text_by_id(634831))
        else:
            newbie_enlist_data = self.get_newbie_enlist_data(scope)
            newbie_enlist_data['enlist_from_uid'] = from_uid
            global_data.emgr.message_on_newbie_enlist_verify.emit()
            global_data.game_mgr.show_tip(get_text_by_id(634830))

    @rpc_method(CLIENT_STUB, (Str('scope'), Int('score')))
    def update_newbie_enlist_newbie_score(self, scope, score):
        print ('update_newbie_enlist_newbie_score', scope, score)
        newbie_enlist_data = self.get_newbie_enlist_data(scope)
        newbie_enlist_data['enlist_newbie_score'] = score
        global_data.emgr.message_on_update_newbie_enlist_newbie_score.emit()

    @rpc_method(CLIENT_STUB, (Str('scope'), Int('ret'), Int('score')))
    def receive_newbie_enlist_bind_reward_ret(self, scope, ret_code, score):
        print ('receive_newbie_enlist_bind_reward_ret', scope, ret_code, score)
        if ret_code:
            newbie_enlist_data = self.get_newbie_enlist_data(scope)
            newbie_enlist_data.get('enlist_newbie_reward_sts', []).append(score)
            global_data.emgr.message_on_receive_newbie_enlist_bind_reward.emit()

    @rpc_method(CLIENT_STUB, (Str('scope'), Int('to_uid')))
    def on_newbie_enlist_succ(self, scope, to_uid):
        print ('on_newbie_enlist_succ', scope, to_uid)
        newbie_enlist_data = self.get_newbie_enlist_data(scope)
        newbie_enlist_data.get('enlist_data', {})[str(to_uid)] = 0
        global_data.emgr.message_on_newbie_enlist_succ.emit()

    @rpc_method(CLIENT_STUB, (Str('scope'), Dict('enlist_data')))
    def update_newbie_enlist_team_score(self, scope, enlist_data):
        print ('update_newbie_enlist_team_score', scope, enlist_data)
        newbie_enlist_data = self.get_newbie_enlist_data(scope)
        newbie_enlist_data.get('enlist_data').update(enlist_data)
        global_data.emgr.message_on_update_newbie_enlist_team_score.emit()

    @rpc_method(CLIENT_STUB, (Str('scope'), Int('ret_code'), Int('score')))
    def receive_newbie_enlist_reward_ret(self, scope, ret_code, score):
        print ('receive_newbie_enlist_reward_ret', scope, ret_code, score)
        if ret_code:
            newbie_enlist_data = self.get_newbie_enlist_data(scope)
            newbie_enlist_data.get('enlist_reward_sts', []).append(score)
            global_data.emgr.message_on_spec_enlist_verify_gift.emit()
        global_data.emgr.message_on_receive_newbie_enlist_reward_ret.emit()

    def pull_cswz_jimu_url(self):
        self.call_server_method('pull_cswz_jimu_url', ())

    @rpc_method(CLIENT_STUB, (Str('url'),))
    def resp_cswz_jimu_url(self, url):
        print (
         'url:', url)
        global_data.emgr.on_resp_cswz_jimu_url.emit(url)

    def pull_jimu_url(self, s_activity_id):
        self.call_server_method('pull_jimu_url', (s_activity_id,))

    @rpc_method(CLIENT_STUB, (Str('url'),))
    def resp_jimu_url(self, url):
        print (
         'url:', url)
        global_data.emgr.on_resp_cswz_jimu_url.emit(url)