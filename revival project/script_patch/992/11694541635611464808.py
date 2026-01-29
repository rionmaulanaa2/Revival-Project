# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impClan.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from logic.gcommon.common_utils.local_text import get_text_by_id
import math
import sys
from mobile.common.RpcMethodArgs import Str, Dict, Int, List, Bool
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from logic.gcommon import const
from logic.gcommon.common_const import clan_const
from common.const.property_const import *
from logic.gcommon import time_utility as tutil
from common.cfg import confmgr
from logic.gutils.search_salog_utils import add_common_search_salog
from logic.gutils import clan_utils

class impClan(object):

    def _init_clan_from_dict(self, bdict):
        self.clan_id = bdict.get('clan_id', -1)
        self._quit_clan_timestamp = bdict.get('quit_clan_timestamp', 0)
        self._join_clan_timestamp = bdict.get('join_clan_timestamp', 0)
        self._request_clan_list = bdict.get('request_clan_list', [])
        self.new_clan_intro = bdict.get('new_clan_intro', False)
        self.new_clan_intro_msg = bdict.get('new_clan_intro_msg', False)
        self._clan_info_cache = {}
        self._clan_info = {}
        self._clan_member_dict_cache = {}
        self._request_all_member_detail = False
        self._request_member_list = []
        self._request_message_dict = {}
        global_data.emgr.message_friend_state += self.update_member_list_state
        global_data.emgr.message_on_players_detail_inf += self.update_member_list_cache
        global_data.emgr.message_on_player_detail_inf += self._update_my_clan_info_cache

    def _destroy_clan(self):
        global_data.emgr.message_friend_state -= self.update_member_list_state
        global_data.emgr.message_on_players_detail_inf -= self.update_member_list_cache
        global_data.emgr.message_on_player_detail_inf -= self._update_my_clan_info_cache
        self._reset_clan_info()

    def _reset_clan_info(self):
        self._request_clan_list = []
        self._clan_info = {}
        self._clan_member_dict_cache = {}
        self._request_all_member_detail = False
        self._request_member_list = []
        self._request_message_dict = {}
        self._clan_info_cache = {}
        global_data.emgr.clan_main_info_reset.emit()

    def _on_login_clan_success(self):
        if self.is_in_clan():
            self.request_clan_info(is_silent=True)
            self.request_player_info(const.PLAYER_INFO_DETAIL, self.uid, force=True)

    def get_clan_id(self):
        return self.clan_id

    def is_in_clan(self):
        return self.clan_id > 0

    def is_same_clan(self, clan_id):
        return self.is_in_clan() and self.clan_id == clan_id

    def get_my_request_clan_lst(self):
        pass

    def get_clan_info(self):
        return self._clan_info

    def get_clan_name(self):
        if not self._clan_info:
            return self._clan_info_cache.get('clan_name', '')
        return self._clan_info.get('clan_name', '')

    def get_clan_badge(self):
        if not self._clan_info:
            return self._clan_info_cache.get('badge', clan_const.get_default_badge())
        return self._clan_info.get('badge', clan_const.get_default_badge())

    def get_clan_lv(self):
        if not self._clan_info:
            return self._clan_info_cache.get('lv', 1)
        return self._clan_info.get('lv', 1)

    def get_clan_commander_uid(self):
        member_list = self.get_clan_member_list()
        for info in member_list:
            if info['title'] == clan_const.COMMANDER:
                return info['uid']

        return 0

    def get_clan_member_list(self):
        if not self._clan_info:
            return []
        return self._clan_info.get('member_list', [])

    def get_clan_member_data(self):
        return self._clan_member_dict_cache

    def get_request_member_list(self, check_info=False):
        if check_info:
            return [ uid for uid in self._request_member_list if global_data.message_data.get_player_detail_inf(uid) ]
        else:
            return self._request_member_list

    def get_request_message_dict(self):
        return self._request_message_dict

    def get_my_clan_info(self):
        return self.get_member_clan_info(self.uid)

    def get_member_clan_info(self, uid):
        member_list = self.get_clan_member_list()
        if not member_list:
            return {}
        for info in member_list:
            if info['uid'] == uid:
                return info

        return {}

    def get_member_data(self, uid):
        return self._clan_member_dict_cache.get(uid, {})

    def get_clan_active(self):
        if not self._clan_info:
            return 0
        return self._clan_info.get('active', 0)

    def duplicate_member_list(self, old_member_list, new_member_list):
        old_member_dict = {info['uid']:info for info in old_member_list}
        new_member_dict = {info['uid']:info for info in new_member_list}
        duplicate_set = set(six_ex.keys(old_member_dict)) & set(six_ex.keys(new_member_dict))
        for uid in duplicate_set:
            if uid in old_member_dict:
                old_member_dict[uid].update(new_member_dict[uid])

        return [ old_member_dict.get(uid, None) or new_member_dict.get(uid) for uid in list(duplicate_set) ]

    def set_clan_info(self, clan_info):
        new_member_list = clan_info['member_list']
        if self._clan_info:
            clan_info['member_list'] = self.duplicate_member_list(self.get_clan_member_list(), new_member_list)
        self._clan_info = clan_info

    def search_clan_by_limit(self, apply_approval_limit, apply_dan_limit, apply_lv_limit, skip, open_ui=False, lang_limit=-1, active_limit=0):
        self.call_server_method('search_clan_by_limit', (lang_limit, active_limit, apply_approval_limit, apply_dan_limit, apply_lv_limit, skip, open_ui))

    def search_clan_by_cid(self, clan_id):
        if not 0 < int(clan_id) < sys.maxsize:
            return False
        self.call_server_method('search_clan_by_cid', (clan_id,))
        return True

    def search_clan_by_name(self, clan_name):
        add_common_search_salog(clan_name)
        self.call_server_method('search_clan_by_name', (clan_name,))

    @rpc_method(CLIENT_STUB, (List('clan_list'), Bool('open_ui')))
    def search_clan_result(self, clan_list, open_ui):
        global_data.emgr.update_clan_recommend_lst.emit(clan_list)
        if open_ui:
            global_data.ui_mgr.show_ui('ClanJoinMainUI', 'logic.comsys.clan')

    def request_create_clan(self, clan_name, clan_intro, apply_reject_limit=0, apply_approval_limit=0, apply_dan_limit=-1, apply_lv_limit=-1, clan_lang=None, clan_badge=0):
        from logic.gcommon.common_utils.local_text import get_cur_text_lang
        clan_lang = get_cur_text_lang() if clan_lang is None else clan_lang
        if clan_lang is None or clan_lang < -1:
            clan_lang = -1
        self.call_server_method('request_create_clan', (clan_name, clan_badge, clan_intro, clan_lang, apply_reject_limit, apply_approval_limit, apply_dan_limit, apply_lv_limit))
        return

    @rpc_method(CLIENT_STUB, (Int('clan_id'), Int('err_code')))
    def respon_create_clan(self, clan_id, err_code):
        if err_code < 0:
            self.clan_id = clan_id
            self._reset_clan_info()
            self._join_clan_timestamp = tutil.get_server_time()
            global_data.emgr.create_clan_success.emit()
            global_data.game_mgr.show_tip(get_text_by_id(800008))
        else:
            if self.clan_id == clan_id:
                self.clan_id = -1
            global_data.emgr.create_clan_failed.emit()
            self.notify_client_message((pack_text(err_code),))

    def request_join_clan(self, cidlist, request_data={'request_content': get_text_by_id(358)}):
        if self.is_in_clan():
            self.notify_client_message((pack_text(800011),))
            return False
        now = int(tutil.time())
        cd = int(self._quit_clan_timestamp + confmgr.get('clan_data', 'avt_quit_limit') + 5 - now)
        if cd > 0:
            cd_minute = int(math.ceil(cd / tutil.ONE_MINUTE_SECONDS))
            global_data.game_mgr.show_tip(get_text_by_id(800026).format(cd_minute))
            return False
        request_lst = []
        for clan_id in cidlist:
            for idx, (_clan_id, timestamp) in enumerate(self._request_clan_list):
                if clan_id == _clan_id:
                    if now - timestamp >= tutil.ONE_HOUR_SECONS:
                        request_lst.append(clan_id)
                        self._request_clan_list[idx][1] = now
                    break
            else:
                request_lst.append(clan_id)
                self._request_clan_list.append([clan_id, now])
                avt_request_limit = confmgr.get('clan_data', 'avt_request_limit')
                if len(self._request_clan_list) >= avt_request_limit:
                    self._request_clan_list.pop(0)

        self.call_server_method('request_join_clan', (request_lst, request_data))
        return True

    def has_requested_join(self, clan_id):
        now = int(tutil.time())
        for idx, (_clan_id, timestamp) in enumerate(self._request_clan_list):
            if clan_id == _clan_id:
                if now - timestamp <= tutil.ONE_HOUR_SECONS:
                    return True
                break

        return False

    @rpc_method(CLIENT_STUB, (Int('clan_id'), Int('err_code'), Bool('show_tip')))
    def respon_join_clan(self, clan_id, err_code, show_tip):
        if err_code > 0:
            for idx, (_clan_id, timestamp) in enumerate(self._request_clan_list):
                if clan_id == _clan_id:
                    self._request_clan_list.pop(idx)
                    if show_tip:
                        self.notify_client_message((pack_text(err_code),))
                    break

        else:
            self.clan_id = clan_id
            self._join_clan_timestamp = tutil.get_server_time()
            self._reset_clan_info()
            global_data.emgr.create_join_success.emit()

    @rpc_method(CLIENT_STUB, (Int('clan_id'), Dict('member_dict')))
    def notify_join_clan(self, clan_id, member_dict):
        if self.clan_id != clan_id:
            return
        uid_list = []
        if member_dict['uid'] not in self._clan_member_dict_cache:
            uid_list.append(member_dict['uid'])
        self._add_member(member_dict)
        if uid_list:
            self.request_players_detail_inf(uid_list)
        global_data.emgr.clan_member_join.emit()

    def request_clan_request(self):
        if not self.is_in_clan():
            return
        self.call_server_method('request_clan_request')

    def reject_clan_request(self, uidlist):
        if not self.is_in_clan():
            return
        if not uidlist:
            return
        self.call_server_method('reject_clan_request', (uidlist,))

    @rpc_method(CLIENT_STUB, (List('request_list'), Dict('request_message_dict'), Int('err_code')))
    def respon_clan_request(self, request_list, request_message_dict, err_code):
        if err_code > 0:
            self.notify_client_message((pack_text(err_code),))
        else:
            self._request_member_list = request_list
            self._request_message_dict = request_message_dict
            global_data.emgr.clan_members_request_list.emit()

    def accept_clan_request(self, uidlist):
        if not self.is_in_clan():
            return
        if not uidlist:
            return
        self.call_server_method('accept_clan_request', (uidlist,))

    @rpc_method(CLIENT_STUB, (List('request_list'), List('new_uidlist'), Dict('request_message_dict'), Int('err_code')))
    def respon_accept_clan(self, request_list, new_uidlist, request_message_dict, err_code):
        if err_code > 0:
            self.notify_client_message((pack_text(err_code),))
        else:
            self._request_member_list = request_list
            self._request_message_dict = request_message_dict
            global_data.emgr.clan_members_request_list.emit()

    def is_advise_quit_clan(self):
        if not self.is_in_clan():
            return False
        if not global_data.enable_clan_quit_advise:
            return False
        if self.get_clan_active() > clan_utils.get_quit_active_limit():
            return False
        if self._join_clan_timestamp + tutil.ONE_WEEK_SECONDS * 2.0 > tutil.get_server_time():
            return False
        return True

    def request_quit_clan(self, is_advice=False):
        if not self.is_in_clan():
            return
        self.call_server_method('request_quit_clan', (is_advice,))

    @rpc_method(CLIENT_STUB, (Int('clan_id'), Int('quit_clan_timestamp')))
    def respon_quit_clan(self, clan_id, quit_clan_timestamp):
        self.clan_id = -1
        self._join_clan_timestamp = -1
        self._quit_clan_timestamp = quit_clan_timestamp
        self._reset_clan_info()
        global_data.ui_mgr.close_ui('ClanMainUI')
        global_data.achi_mgr.set_cur_user_archive_data('ignore_clan_inactive_confirm', -1)

    def request_clan_info(self, open_ui=False, is_silent=False):
        if not self.is_in_clan():
            return
        if is_silent:
            self.call_server_method('request_clan_info_silent', (open_ui,))
        else:
            self.call_server_method('request_clan_info', (open_ui,))

    @rpc_method(CLIENT_STUB, (Dict('clan_info'), Bool('open_ui')))
    def respon_clan_info(self, clan_info, open_ui):
        self.clan_id = clan_info['clan_id']
        self.set_clan_info(clan_info)
        uid_list = []
        member_list = self.get_clan_member_list()
        for i, info in enumerate(member_list):
            if info['uid'] not in self._clan_member_dict_cache:
                uid_list.append(info['uid'])
            self._add_member(info, do_append=False)

        global_data.emgr.clan_main_info.emit(self._clan_info)
        if not self._request_all_member_detail:
            uid_list = [ info['uid'] for info in member_list ]
        self._request_all_member_detail = True
        if uid_list:
            self.request_players_detail_inf(uid_list)
        if open_ui:
            global_data.ui_mgr.show_ui('ClanMainUI', 'logic.comsys.clan')

    def is_members_info_finished(self):
        member_list = self.get_clan_member_list()
        if not member_list:
            return False
        for i, info in enumerate(member_list):
            if C_NAME not in info:
                return False

        return True

    def update_member_list_state(self):
        member_list = self.get_clan_member_list()
        if not member_list:
            return
        else:
            changed = False
            players_online_state_dict = global_data.message_data.get_player_online_state()
            for i, info in enumerate(member_list):
                uid = info[U_ID]
                state = players_online_state_dict.get(uid, None)
                if state != None:
                    info[ONLINE_STATE] = state
                    info['offline_time'] = global_data.message_data.get_player_offline_time(uid)
                    changed = True

            if changed:
                global_data.emgr.clan_member_mod_info.emit()
            return

    def _update_my_clan_info_cache(self, data):
        if int(data.get(U_ID, 0)) == self.uid:
            clan_info = data.get('clan_info', {})
            self._clan_info_cache = clan_info

    def update_member_list_cache(self, member_detail_list):
        if not self._request_all_member_detail:
            return
        else:
            for data in member_detail_list:
                uid = int(data[U_ID])
                if uid in self._clan_member_dict_cache:
                    info = self._clan_member_dict_cache[uid]
                    info[ROLE_ID] = data.get(ROLE_ID, 0)
                    info[C_NAME] = data.get(C_NAME, '')
                    info[HEAD_PHOTO] = data.get(HEAD_PHOTO, None)
                    info[HEAD_FRAME] = data.get(HEAD_FRAME, None)
                    info[U_LV] = data.get(U_LV, 1)
                    info[ONLINE_STATE] = data.get(ONLINE_STATE, 0)
                    info['offline_time'] = global_data.message_data.get_player_offline_time(uid)
                    info['dan_info'] = data.get('dan_info', {})
                    info['fashion_value'] = data.get('fashion_value', 0)

            global_data.emgr.clan_member_data.emit()
            return

    def _set_member_title(self, uid, title):
        if uid in self._clan_member_dict_cache:
            self._clan_member_dict_cache[uid]['title'] = title

    def _remove_member(self, uid):
        member_list = self.get_clan_member_list()
        for i in range(len(member_list)):
            info = member_list[i]
            if info['uid'] == uid:
                member_list.pop(i)
                del self._clan_member_dict_cache[uid]
                break

    def _add_member(self, info, do_append=True):
        if not self._clan_info:
            return
        member_list = self.get_clan_member_list()
        if info['uid'] in self._clan_member_dict_cache:
            self._clan_member_dict_cache[info['uid']].update(info)
        else:
            self._clan_member_dict_cache[info['uid']] = info
            if do_append:
                member_list.append(info)

    def change_clan_setup(self, reject_lmt, approval_lmt, dan_lmt, lv_lmt):
        if not self.is_in_clan():
            return
        r_lmt = self._clan_info.get('apply_reject_limit')
        a_lmt = self._clan_info.get('apply_approval_limit')
        d_lmt = self._clan_info.get('apply_dan_limit', -1)
        l_lmt = self._clan_info.get('apply_lv_limit', 0)
        if reject_lmt == r_lmt and approval_lmt == a_lmt and dan_lmt == d_lmt and lv_lmt == l_lmt:
            return
        self.call_server_method('change_clan_setup', (reject_lmt, approval_lmt, dan_lmt, lv_lmt))

    @rpc_method(CLIENT_STUB, (Int('apply_reject_limit'), Int('apply_approval_limit'), Int('apply_dan_limit'), Int('apply_lv_limit'), Int('err_code')))
    def respon_clan_setup(self, apply_reject_limit, apply_approval_limit, apply_dan_limit, apply_lv_limit, err_code):
        if err_code > 0:
            self.notify_client_message((pack_text(err_code),))
        elif self._clan_info:
            self._clan_info['apply_reject_limit'] = apply_reject_limit
            self._clan_info['apply_approval_limit'] = apply_approval_limit
            self._clan_info['apply_dan_limit'] = apply_dan_limit
            self._clan_info['apply_lv_limit'] = apply_lv_limit

    def change_clan_name(self, clan_name):
        if not self.is_in_clan():
            return
        self.call_server_method('change_clan_name', (clan_name,))

    @rpc_method(CLIENT_STUB, (Str('clan_name'), Int('err_code')))
    def respon_clan_name(self, clan_name, err_code):
        if err_code > 0:
            self.notify_client_message((pack_text(err_code),))
        else:
            if self._clan_info:
                self._clan_info['clan_name'] = clan_name
            global_data.game_mgr.show_tip(get_text_by_id(800131).format(clan_name))
            global_data.emgr.clan_mod_name.emit()

    def change_clan_badge(self, clan_badge):
        if not self.is_in_clan():
            return
        if self._clan_info.get('badge') == clan_badge:
            return
        self.call_server_method('change_clan_badge', (clan_badge,))

    @rpc_method(CLIENT_STUB, (Int('clan_badge'), Int('err_code')))
    def respon_clan_badge(self, clan_badge, err_code):
        if err_code > 0:
            self.notify_client_message((pack_text(err_code),))
        else:
            if self._clan_info:
                self._clan_info['badge'] = clan_badge
            global_data.emgr.clan_change_badge_suc.emit()

    def change_clan_intro(self, clan_intro):
        if not self.is_in_clan():
            return
        self.call_server_method('change_clan_intro', (clan_intro,))

    @rpc_method(CLIENT_STUB, (Str('clan_intro'), Int('err_code')))
    def respon_clan_intro(self, clan_intro, err_code):
        if err_code > 0:
            self.notify_client_message((pack_text(err_code),))
        else:
            if self._clan_info:
                self._clan_info['intro'] = clan_intro
            global_data.emgr.clan_mod_intro.emit()

    @rpc_method(CLIENT_STUB, (Str('clan_intro'),))
    def receive_new_clan_intro(self, clan_intro):
        self.new_clan_intro = True
        self.new_clan_intro_msg = True
        if self._clan_info != None:
            self._clan_info['intro'] = clan_intro
        global_data.emgr.clan_main_info.emit()
        return

    def confirm_new_clan_intro(self):
        self.new_clan_intro = False
        self.call_server_method('confirm_new_intro', ())

    def get_new_clan_intro(self):
        return self.new_clan_intro

    def confirm_new_clan_intro_msg(self):
        self.new_clan_intro_msg = False
        self.call_server_method('confirm_new_intro_msg', ())

    def get_new_clan_intro_msg_cnt(self):
        if self.new_clan_intro_msg:
            return 1
        return 0

    def get_clan_intro(self):
        if self._clan_info:
            return str(self._clan_info.get('intro', ''))
        return ''

    def change_clan_lang(self, clan_lang):
        if not self.is_in_clan():
            return
        if self._clan_info.get('lang') == clan_lang:
            return
        self.call_server_method('change_clan_lang', (clan_lang,))

    @rpc_method(CLIENT_STUB, (Int('clan_lang'), Int('err_code')))
    def respon_clan_lang(self, clan_lang, err_code):
        if err_code > 0:
            self.notify_client_message((pack_text(err_code),))
        elif self._clan_info:
            self._clan_info['lang'] = clan_lang

    def request_appoint_title(self, appointee_uid, title):
        if not self.is_in_clan() or self.uid == appointee_uid:
            return
        self.call_server_method('request_appoint_title', (appointee_uid, title))

    @rpc_method(CLIENT_STUB, (Int('appointee_uid'), Int('title'), Int('err_code')))
    def respon_appoint_title(self, appointee_uid, title, err_code):
        if err_code > 0:
            self.notify_client_message((pack_text(err_code),))
        else:
            self._set_member_title(appointee_uid, title)
            global_data.emgr.clan_member_mod_info.emit()

    @rpc_method(CLIENT_STUB, (Int('appointee_uid'), Int('title')))
    def notify_appoint_title(self, appointee_uid, title):
        if title == clan_const.COMMANDER:
            member_list = self.get_clan_member_list()
            for info in member_list:
                if info['title'] == clan_const.COMMANDER:
                    self._set_member_title(info['uid'], clan_const.MASS)

        self._set_member_title(appointee_uid, title)
        global_data.emgr.clan_member_mod_info.emit()

    def request_kick_member(self, executee_uid):
        if not self.is_in_clan() or self.uid == executee_uid:
            return
        self.call_server_method('request_kick_member', (executee_uid,))

    @rpc_method(CLIENT_STUB, (Int('executee_uid'), Int('err_code')))
    def respon_kick_member(self, executee_uid, err_code):
        if err_code > 0:
            self.notify_client_message((pack_text(err_code),))
        else:
            self._remove_member(executee_uid)
            global_data.emgr.clan_member_kick.emit(executee_uid)

    @rpc_method(CLIENT_STUB, (Int('clan_id'),))
    def notify_kick_clan(self, clan_id):
        if self.clan_id != clan_id:
            return
        self.clan_id = -1
        self._reset_clan_info()
        global_data.ui_mgr.close_ui('ClanMainUI')

    def query_clan_info(self, clan_id):
        self.call_server_method('query_clan_info', (clan_id,))

    @rpc_method(CLIENT_STUB, (Int('clan_id'), Dict('clan_info')))
    def reply_clan_info(self, clan_id, clan_info):
        if clan_info:
            global_data.emgr.global_message_on_query_clan_info.emit(clan_id, clan_info)