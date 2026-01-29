# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impCompetition.py
from __future__ import absolute_import
from __future__ import print_function
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, MailBox, Dict, Int, Bool, Uuid, List, Float
from logic.gcommon import time_utility as tutil
from logic.gcommon.cdata.round_competition import get_nearliest_competition_open

class impCompetition(object):

    def _init_competition_from_dict(self, bdict):
        self.comp_id = bdict.get('comp_id', None)
        self.comp_round = bdict.get('comp_round', None)
        self.is_ob_competition = bdict.get('is_ob_competition', False)
        self.competition_attend_record = bdict.get('competition_attend_record', {})
        self.last_week_comp_result = None
        self.winter_cup_rank_result = None
        self.show_info = {}
        return

    def req_join_competition(self, comp_id, round):
        self.call_server_method('req_join_competition', (comp_id, round))

    @rpc_method(CLIENT_STUB, (Str('comp_id'), Int('round'), Bool('is_ob')))
    def join_competition_succ(self, comp_id, round, is_ob):
        self.comp_id = comp_id
        self.comp_round = round
        self.is_ob = is_ob
        global_data.emgr.enter_summer_peak_match_queue.emit()

    def cancel_join_competition(self, comp_id, round):
        self.call_server_method('cancel_join_competition', (comp_id, round))

    @rpc_method(CLIENT_STUB, ())
    def cancel_join_competition_succ(self):
        self.reset_join_state_on_dissolve_or_cancel()

    def get_competition_info(self):
        info = {'comp_id': self.comp_id,
           'comp_round': self.comp_round,
           'is_ob_competition': self.is_ob_competition
           }
        return info

    def get_player_competition_state(self):
        return self.comp_id and self.comp_round

    def get_player_join_competition_state(self):
        pass

    def clear_player_join_state(self):
        from logic.gcommon.cdata.round_competition import get_nearliest_competition_conf
        comp_id, round_id, _ = get_nearliest_competition_conf()
        if comp_id and self.comp_id:
            if round_id > self.comp_round:
                self.comp_id = None
                self.comp_round = None
                self.is_ob_competition = False
                global_data.emgr.cancel_summer_peak_match_queue.emit()
        return

    @rpc_method(CLIENT_STUB, (Str('comp_id'), Int('rela_day_no')))
    def on_attend_competition(self, comp_id, rela_day_no):
        self.competition_attend_record[comp_id] = rela_day_no

    def get_last_week_comp_result(self):
        return self.last_week_comp_result

    def request_last_week_comp_result(self):
        from logic.gcommon.cdata import week_competition as wcomp
        if self.last_week_comp_result:
            lst_comp_id = self.last_week_comp_result[-1][0]
            week_comp_conf = wcomp.get_weekcomp_info_by_comp_id(lst_comp_id)
            if not week_comp_conf:
                return
            start_ts = week_comp_conf[1]
            comp_week_no = wcomp.get_comp_week_no(start_ts)
            now_week_no = wcomp.get_comp_week_no()
            if comp_week_no >= now_week_no:
                return
        self.call_server_method('request_last_week_comp_result')

    @rpc_method(CLIENT_STUB, (List('last_week_comp_result'),))
    def reply_last_week_comp_result(self, last_week_comp_result):
        self.last_week_comp_result = last_week_comp_result
        global_data.emgr.reply_last_week_comp_result_event.emit()
        print('test---reply_last_week_comp_result: ', last_week_comp_result)
        global_data.emgr.refresh_activity_redpoint.emit()

    @rpc_method(CLIENT_STUB, (Dict('show_info'),))
    def req_round_comp_show_info_ret(self, show_info):
        self.show_info = show_info
        global_data.emgr.req_round_comp_show_info_ret_event.emit()

    def req_round_comp_show_info(self, comp_id, round):
        self.call_server_method('req_round_comp_show_info', (comp_id, round))

    def request_comp_show_entrance(self):
        comp_id, cur_round, round_conf = get_nearliest_competition_open()
        if self.show_info:
            _comp_id = self.show_info.get('comp_id', '')
            _cur_round = self.show_info.get('round', 1)
            if comp_id != _comp_id or cur_round != _cur_round:
                self.req_round_comp_show_info(comp_id, cur_round)
        else:
            self.req_round_comp_show_info(comp_id, cur_round)

    def is_show_competition_entrance(self, comp_id, cur_round):
        if not self.show_info:
            return False
        else:
            _comp_id = self.show_info.get('comp_id', '')
            _cur_round = self.show_info.get('round', 1)
            can_show = self.show_info.get('can_show', 0)
            if _comp_id == comp_id and _cur_round == cur_round:
                if can_show == 1:
                    return True
                return False
            return False

    def reset_join_state_on_dissolve_or_cancel(self):
        self.comp_id = None
        self.comp_round = None
        self.is_ob_competition = False
        global_data.emgr.cancel_summer_peak_match_queue.emit(need_clear_all_state=True)
        return

    def clear_camp_show_info(self):
        self.show_info = None
        return

    def get_notice_rank_list(self):
        self.call_server_method('get_notice_rank_list', ())

    def get_winter_cup_rank_result(self):
        return self.winter_cup_rank_result

    @rpc_method(CLIENT_STUB, (List('rank_list'), Dict('self_info')))
    def get_notice_rank_list_ret(self, rank_list, self_info):
        print('get_notice_rank_list_ret', rank_list, self_info)
        self.winter_cup_rank_result = (rank_list, self_info)
        global_data.emgr.on_winter_cup_rank.emit()