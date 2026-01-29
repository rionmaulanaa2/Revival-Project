# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impFriend.py
from __future__ import absolute_import
import six
import sys
from mobile.common.RpcMethodArgs import Str
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, MailBox, Dict, Int, Bool, Uuid, List
from logic.gcommon import const
from logic.gutils.search_salog_utils import add_common_search_salog
from common.const.property_const import U_ID, U_LV, C_NAME, MIN_ADD_FRIEND_LV

class impFriend(object):

    def _init_friend_from_dict(self, bdict):
        self._disable_social_types = bdict.get('disable_social_types', [])
        self._receive_social_rewards = bdict.get('receive_social_rewards', [])
        self._daily_gold_gift_uids = bdict.get('daily_gold_gift_uids', [])
        frds_remark = bdict.get('frds_remark', {})
        self._frds_remark = {int(frd_uid):remark for frd_uid, remark in six.iteritems(frds_remark)}
        self._top_frds = bdict.get('top_frds', [])

    @rpc_method(CLIENT_STUB, ())
    def reset_friend_per_day(self):
        self._daily_gold_gift_uids = []

    def search_friend(self, frd_uid, frd_name):
        if len(frd_name) == 0:
            if frd_uid == self.uid:
                return False
            if not 0 < int(frd_uid) < sys.maxsize:
                return False
            self.call_server_method('search_friend_by_uid', (int(frd_uid),))
            return True
        else:
            if frd_name == self.get_name():
                return False
            add_common_search_salog(str(frd_name))
            self.call_server_method('search_friend_by_name', (str(frd_name),))
            return True

    def req_add_friend(self, frd_uid):
        if self.get_lv() < MIN_ADD_FRIEND_LV and not G_IS_NA_PROJECT and not global_data.channel.is_steam_channel():
            global_data.game_mgr.show_tip(635536)
            return
        self.req_add_to_list(const.FRD_KEY_FRDS, frd_uid)

    def agree_add_friend(self, frd_uid):
        self.call_server_method('try_agree_add_friend', (frd_uid,))

    def req_recommend_friend(self):
        self.call_server_method('req_recommend_frds', ())

    def req_friend_msg(self, frd_uid, frd_lv, frd_cid, msg, voice='', extra=None):
        if not isinstance(frd_lv, int):
            frd_lv = 1
        extra = {} if extra is None else extra
        frd_cid = -1 if frd_cid is None else frd_cid
        self.call_server_method('req_friend_msg', (frd_uid, frd_lv, frd_cid, msg, voice, extra))
        return

    def req_blessing_msg(self, frd_uid, frd_lv, frd_cid, msg, voice='', extra=None):
        if not isinstance(frd_lv, int):
            frd_lv = 1
        extra = {} if extra is None else extra
        frd_cid = -1 if frd_cid is None else frd_cid
        self.call_server_method('req_friend_blessing', (frd_uid, frd_lv, frd_cid, msg, voice, extra))
        return

    def req_add_to_list(self, list_type, uid):
        self.call_server_method('req_add_to_list', (list_type, uid))

    def req_del_from_list(self, list_type, uid):
        self.call_server_method('req_del_from_list', (list_type, uid))

    def test_get_online_state(self, extra=[], immediately=False, include_friends=True):
        filter_extra = []
        for uid in extra:
            try:
                filter_extra.append(int(uid))
            except:
                pass

        self.call_server_method('get_friends_state', (filter_extra, immediately, include_friends))

    def get_one_player_online_state(self, player_uid):
        self.call_server_method('get_one_player_state', (player_uid,))

    def request_player_role_head_info(self, uid_list=None):
        if uid_list:
            self.call_server_method('get_player_role_head', (uid_list,))

    def request_one_player_role_head_info(self, uid):
        self.call_server_method('get_one_player_role_head', (uid,))

    def query_uid_by_facebook_id_list(self, fb_id_list):
        self.call_server_method('query_uid_by_facebook_id_list', (fb_id_list,))

    def query_uid_by_social_id_list(self, id_type, social_id_list):
        self.call_server_method('query_uid_by_social_id_list', (id_type, social_id_list))

    def request_player_wish_debris_info(self, uid_list=None):
        if uid_list:
            self.call_server_method('get_player_pve_wished_debris_id', (uid_list,))

    @rpc_method(CLIENT_STUB, (List('friend_list'), Str('msg'), Dict('extra')))
    def cache_to_friend_chat(self, friend_list, msg, extra):
        message_data = global_data.message_data
        friends_data = global_data.message_data.get_friends()
        for friend_uid in friend_list:
            f_data = friends_data.get(friend_uid)
            if f_data:
                message_data.recv_to_friend_msg(f_data[U_ID], f_data[C_NAME], msg, f_data[U_LV], extra=extra)

    @rpc_method(CLIENT_STUB, (Str('list_type'), List('info_list')))
    def add_to_list(self, list_type, info_list):
        global_data.message_data.add_friend(list_type, info_list)

    @rpc_method(CLIENT_STUB, (Str('list_type'), Int('uid')))
    def del_from_list(self, list_type, uid):
        global_data.message_data.del_friend(list_type, uid)

    @rpc_method(CLIENT_STUB, (Dict('frds'),))
    def init_frds(self, frds):
        global_data.message_data.set_friends(frds)

    @rpc_method(CLIENT_STUB, (List('result'),))
    def search_friend_result(self, result):
        global_data.message_data.set_search_friends(result)

    @rpc_method(CLIENT_STUB, (List('frds'),))
    def on_recommend_friend(self, frds):
        global_data.message_data.set_recommend_friends(frds)

    @rpc_method(CLIENT_STUB, (Dict('data'),))
    def on_friend_msg(self, data):
        global_data.message_data.recv_friend_msg(data)

    @rpc_method(CLIENT_STUB, (Dict('frds_state'),))
    def on_friends_state(self, frds_state):
        global_data.message_data.set_player_online_state(frds_state)

    @rpc_method(CLIENT_STUB, (Dict('frds_state'),))
    def on_one_player_state(self, frds_state):
        for player_uid, state in six.iteritems(frds_state):
            if global_data.message_data.update_one_player_online_state(player_uid, state):
                simple_info = global_data.message_data.get_player_simple_inf(player_uid)
                if simple_info:
                    global_data.emgr.message_on_player_simple_inf.emit(simple_info)
                    global_data.emgr.message_friend_state.emit()

    @rpc_method(CLIENT_STUB, (Dict('role_head_info'),))
    def on_player_role_head_info(self, role_head_info):
        global_data.message_data.set_player_role_head_info(role_head_info)

    @rpc_method(CLIENT_STUB, (Int('frd_uid'), Str('new_name')))
    def friend_change_name(self, frd_uid, new_name):
        friends = global_data.message_data.get_friends()
        if frd_uid in friends:
            friends[frd_uid]['char_name'] = new_name
        friends = global_data.message_data.get_team_friends()
        if frd_uid in friends:
            friends[frd_uid]['char_name'] = new_name

    @rpc_method(CLIENT_STUB, (Dict('doc'),))
    def query_uid_by_facebook_id_result(self, doc):
        pass

    @rpc_method(CLIENT_STUB, (Dict('teammates_head_info'), Int('battle_type')))
    def on_recommend_friends_by_recruitment(self, teammates_head_info, battle_type):
        if len(teammates_head_info) > 0:

            def callback--- This code section failed: ---

 216       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('LobbyRecruimentEndAddFriend',)
           6  IMPORT_NAME           0  'logic.comsys.lobby.LobbyRecruimentEndAddFriend'
           9  IMPORT_FROM           1  'LobbyRecruimentEndAddFriend'
          12  STORE_FAST            0  'LobbyRecruimentEndAddFriend'
          15  POP_TOP          

 217      16  POP_TOP          
          17  PRINT_ITEM_TO    
          18  PRINT_ITEM_TO    
          19  LOAD_DEREF            0  'teammates_head_info'
          22  LOAD_CONST            4  'battle_type'
          25  LOAD_DEREF            1  'battle_type'
          28  CALL_FUNCTION_512   512 
          31  POP_TOP          

Parse error at or near `POP_TOP' instruction at offset 16

            self.add_advance_callback('LobbyRecruimentEndAddFriend', callback, hide_lobby_ui=False)

    @rpc_method(CLIENT_STUB, (Dict('wished_debris_info'),))
    def on_player_pve_wished_debris_id_info(self, wished_debris_info):
        global_data.message_data.set_player_wish_derbis_info(wished_debris_info)

    def is_social_enable(self, id_type):
        return id_type not in self._disable_social_types

    @rpc_method(CLIENT_STUB, (Str('id_type'), List('doc'), Dict('uid2sid')))
    def query_uid_by_social_id_result(self, id_type, doc, uid2sid):
        global_data.message_data.set_social_friends(id_type, doc, uid2sid)

    def request_unbind_social(self, id_type):
        self.call_server_method('request_unbind_social', (id_type,))

    def request_enable_social(self, id_type):
        if id_type not in self._disable_social_types:
            return
        self._disable_social_types.remove(id_type)
        self.call_server_method('request_enable_social', (id_type,))

    def request_disable_social(self, id_type):
        if id_type in self._disable_social_types:
            return
        self._disable_social_types.append(id_type)
        self.call_server_method('request_disable_social', (id_type,))

    def request_bind_social(self, id_type, social_ids):
        self.call_server_method('request_bind_social', (id_type, social_ids))
        return True

    @rpc_method(CLIENT_STUB, (Str('id_type'), Bool('result')))
    def respond_bind_social(self, id_type, result):
        if result and not self.is_receive_social_reward(id_type):
            self._receive_social_rewards.append(id_type)

    def is_receive_social_reward(self, id_type):
        return id_type in self._receive_social_rewards

    def click_season_like_btn(self):
        self.call_server_method('click_season_like_btn', ())

    def has_given_daily_gold_gift(self, uid):
        return uid in self._daily_gold_gift_uids

    def give_social_daily_gold_gift(self, id_type, taker_uid):
        self.call_server_method('give_social_daily_gold_gift', (id_type, taker_uid))

    @rpc_method(CLIENT_STUB, (Int('taker_uid'),))
    def update_daily_gold_gift(self, taker_uid):
        self._daily_gold_gift_uids.append(taker_uid)
        global_data.emgr.message_social_coins.emit(taker_uid)

    def remark_friend(self, frd_uid, remark):
        self.call_server_method('remark_friend', (frd_uid, remark))

    @rpc_method(CLIENT_STUB, (Int('frd_uid'), Str('remark')))
    def on_remark_friend(self, frd_uid, remark):
        self._frds_remark[frd_uid] = remark
        global_data.emgr.message_refresh_friends.emit()

    @rpc_method(CLIENT_STUB, (Int('frd_uid'),))
    def on_del_frd_remark(self, frd_uid):
        if frd_uid in self._frds_remark:
            self._frds_remark.pop(frd_uid)
            global_data.emgr.message_refresh_friends.emit()

    def set_top_friend(self, frd_uid):
        self.call_server_method('set_top_friend', (frd_uid,))

    def remove_top_friend(self, frd_uid):
        self.call_server_method('remove_top_friend', (frd_uid,))

    @rpc_method(CLIENT_STUB, (Int('frd_uid'),))
    def on_set_top_friend(self, frd_uid):
        self._top_frds.append(frd_uid)
        global_data.emgr.message_refresh_friends.emit()
        simple_info = global_data.message_data.get_player_simple_inf(frd_uid)
        global_data.emgr.message_on_player_simple_inf.emit(simple_info)

    @rpc_method(CLIENT_STUB, (Int('frd_uid'),))
    def on_remove_top_friend(self, frd_uid):
        if frd_uid in self._top_frds:
            self._top_frds.remove(frd_uid)
            global_data.emgr.message_refresh_friends.emit()
            simple_info = global_data.message_data.get_player_simple_inf(frd_uid)
            global_data.emgr.message_on_player_simple_inf.emit(simple_info)