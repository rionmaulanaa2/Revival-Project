# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impRank.py
from __future__ import absolute_import
import six
import six_ex
from mobile.common.RpcMethodArgs import Str, Int, List, Dict, Bool, Tuple
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from logic.gcommon.common_const import rank_const
from logic.gcommon import time_utility as tutil

class impRank(object):

    def _init_rank_from_dict(self, bdict):
        self.rank_adcode = bdict.get('rank_adcode', None)
        self.rank_adcode_weekno = bdict.get('rank_adcode_weekno', -1)
        self.rank_title_dict = bdict.get('rank_title_dict', {})
        self.rank_use_title_dict = bdict.get('rank_use_title_dict', {})
        self.rank_use_title_type = None
        for title_type in six.iterkeys(self.rank_use_title_dict):
            self.rank_use_title_type = title_type
            break

        self.rank_reward_dict = bdict.get('rank_reward_dict', {})
        self.rank_reward_percent_dict = bdict.get('rank_reward_percent_dict', {})
        self.my_rank_mecha_data = {}
        return

    def get_my_rank_mecha_data(self, rank_type):
        return self.my_rank_mecha_data.get(str(rank_type), None)

    def has_set_rank_adcode(self):
        return self.rank_adcode is not None

    def can_set_rank_adcode(self):
        if not self.rank_adcode:
            return True
        now = tutil.time()
        week_no = tutil.get_rela_week_no(now, tutil.CYCLE_DATA_REFRESH_TYPE_2)
        week_start_ts = tutil.get_week_start_timestamp(now) + tutil.CYCLE_DATA_REFRESH_TIME[tutil.CYCLE_DATA_REFRESH_TYPE_2]
        week_end_ts = week_start_ts + 4 * tutil.ONE_DAY_SECONDS
        return self.rank_adcode_weekno != week_no and week_start_ts <= now <= week_end_ts

    def request_set_rank_adcode(self, rank_adcode):
        from logic.gcommon.cdata import adcode_data
        if self.rank_adcode == rank_adcode:
            return True
        else:
            if not adcode_data.is_adcode_valid(rank_adcode):
                rank_adcode = adcode_data.ADCODE_UNKNOW
            now = tutil.time()
            week_no = tutil.get_rela_week_no(now, tutil.CYCLE_DATA_REFRESH_TYPE_2)
            if self.can_set_rank_adcode():
                self.rank_adcode_weekno = week_no
                self.call_server_method('request_set_rank_adcode', (rank_adcode,))
                return True
            return False

    @rpc_method(CLIENT_STUB, (Bool('result'), Int('rank_adcode_weekno'), Str('rank_adcode')))
    def respon_set_rank_adcode(self, result, rank_adcode_weekno, rank_adcode):
        self.rank_adcode_weekno = rank_adcode_weekno
        if rank_adcode:
            self.rank_adcode = rank_adcode if 1 else None
            result or self.notify_client_message((pack_text(15072),))
        else:
            global_data.emgr.message_respond_set_adcode.emit()
        return

    def request_my_rank_service_data(self, rank_type):
        self.call_server_method('get_rank_service_data', (rank_type,))

    @rpc_method(CLIENT_STUB, (Str('rank_type'), List('rank_data')))
    def get_rank_service_data_result(self, rank_type, rank_data):
        self.my_rank_mecha_data[rank_type] = rank_data
        global_data.emgr.message_on_region_my_rank_data.emit()

    @rpc_method(CLIENT_STUB, (Dict('title_dict'),))
    def settle_rank_title(self, title_dict):
        from logic.comsys.rank import MechaRegionTitleUI
        title_type = title_dict['title_type']
        title_data = title_dict['title_data']
        settle_title = title_dict.get('settle_title', {})
        self.rank_title_dict[title_type] = title_data
        self.check_rank_title(title_type)
        if title_type == rank_const.RANK_TITLE_MECHA_REGION and settle_title and not global_data.player.has_advance_callback('MechaRegionTitleUI'):

            def callback():
                MechaRegionTitleUI.MechaRegionTitleUI(None, settle_title=settle_title)
                return

            global_data.player.add_advance_callback('MechaRegionTitleUI', callback, hide_lobby_ui=False)
        if title_type == rank_const.RANK_TITLE_ITEM and settle_title:
            reward_dict = {}
            for item_no in six_ex.keys(settle_title):
                reward_dict[int(item_no)] = 1

            global_data.emgr.receive_award_succ_event.emit(reward_dict, {})

    def check_rank_title(self, title_type):
        if title_type in self.rank_use_title_dict:
            is_valid, pack_title_data = rank_const.is_rank_title_valid(self.rank_title_dict, title_type, self.rank_use_title_dict[title_type])
            if not is_valid:
                del self.rank_use_title_dict[title_type]
                self.rank_use_title_type = None
            else:
                self.rank_use_title_dict[title_type] = pack_title_data
                self.rank_use_title_type = title_type
        return self.rank_use_title_dict.get(title_type, None)

    def request_set_mecha_region_rank_title(self, region_type, mecha_type):
        region_type = str(region_type)
        mecha_type = str(mecha_type)
        rank_data = self.rank_title_dict.get(rank_const.RANK_TITLE_MECHA_REGION, {}).get(region_type, {}).get(mecha_type, None)
        if not rank_data:
            return False
        else:
            rank_adcode, rank, rank_expire = rank_data
            title_data = (region_type, mecha_type, rank_adcode, rank, rank_expire)
            return self.request_set_rank_title(rank_const.RANK_TITLE_MECHA_REGION, title_data)

    def request_set_rank_title(self, title_type, title_data):
        if not title_data:
            self.call_server_method('request_set_rank_title', (title_type, ()))
            del self.rank_use_title_dict[title_type]
            self.rank_use_title_type = None
            global_data.emgr.message_on_set_rank_title.emit()
            return True
        else:
            is_valid, pack_title_data = rank_const.is_rank_title_valid(self.rank_title_dict, title_type, title_data)
            if is_valid:
                self.call_server_method('request_set_rank_title', (title_type, pack_title_data))
                return True
            return False
            return

    @rpc_method(CLIENT_STUB, (Bool('is_valid'), Str('title_type'), Tuple('title_data')))
    def respon_set_rank_title(self, is_valid, title_type, title_data):
        if is_valid:
            self.rank_use_title_dict.clear()
            self.rank_use_title_dict[title_type] = title_data
            self.rank_use_title_type = title_type
            global_data.emgr.message_on_set_rank_title.emit()

    def get_rank_use_title(self):
        if self.rank_use_title_type is not None:
            return self.check_rank_title(self.rank_use_title_type)
        else:
            return
            return

    def request_my_rank_data(self, rank_type):
        self.call_server_method('get_rank_data', (rank_type,))

    @rpc_method(CLIENT_STUB, (Str('rank_type'), List('rank_data')))
    def get_rank_data_result(self, rank_type, rank_data):
        global_data.message_data.set_seperate_my_rank_data(rank_type, rank_data)

    def request_rank_list(self, rank_type, start_rank, end_rank, include_self=False, rt_self=False):
        self.call_server_method('get_rank_list', (rank_type, start_rank, end_rank, include_self, rt_self))

    @rpc_method(CLIENT_STUB, (Str('rank_type'), List('rank_list_data')))
    def get_rank_list_result(self, rank_type, rank_list_data):
        if not rank_list_data:
            none_d = rank_const.RANK_DATA_NONE
            rank_list_data = [0, 0, 0, [], none_d, [none_d, none_d, none_d, none_d, none_d]]
        if len(rank_list_data) == 4:
            start_rank, end_rank, rank_version, rank_list = rank_list_data
            rank = None
            data = None
        else:
            start_rank, end_rank, rank_version, rank_list, rank, data = rank_list_data
        global_data.message_data.set_rank_data(rank_type, start_rank, end_rank, rank_version, rank_list, rank, data)
        return

    def request_friend_rank_data(self):
        global_data.player.call_server_method('query_friend_rank_data')

    @rpc_method(CLIENT_STUB, (Dict('frd_rank_data'),))
    def on_friend_rank_data(self, rank_data):
        global_data.message_data.update_friends_dan_info(rank_data)

    def request_rank_percent_list(self, rank_type, include_self=False, rt_self=False):
        self.call_server_method('get_rank_percent_list', (rank_type, include_self, rt_self))

    @rpc_method(CLIENT_STUB, (Str('rank_type'), List('rank_list_data')))
    def get_rank_percent_list_result(self, rank_type, rank_list_data):
        if not rank_list_data:
            none_d = rank_const.RANK_DATA_NONE
            rank_list_data = [0, [], none_d, none_d, [none_d, none_d, none_d, none_d, none_d]]
        if len(rank_list_data) == 2:
            rank_version, rank_list = rank_list_data
            my_rank = None
            rank_length = None
            my_rank_data = None
        else:
            rank_version, rank_list, my_rank, rank_length, my_rank_data = rank_list_data
        global_data.message_data.set_rank_percent_data(rank_type, rank_version, rank_list, my_rank, rank_length, my_rank_data)
        return

    def is_offer_rank_reward(self, rank_type):
        return rank_type in self.rank_reward_dict and self.rank_reward_dict[rank_type] > 0

    def request_offer_rank_reward(self, rank_type):
        if self.is_offer_rank_reward(rank_type):
            return
        self.call_server_method('request_offer_rank_reward', (rank_type,))

    @rpc_method(CLIENT_STUB, (Str('rank_type'), Int('rank')))
    def respon_offer_rank_reward(self, rank_type, rank):
        self.rank_reward_dict[rank_type] = rank
        if rank <= 0:
            global_data.game_mgr.show_tip(get_text_by_id(15043))
            global_data.emgr.receive_rank_reward_fail.emit()
        else:
            global_data.emgr.receive_rank_reward_success.emit()

    def is_not_participate_rank(self, rank_type):
        if rank_type not in self.rank_reward_dict:
            from logic.gcommon.common_const import rank_const, rank_activity_const
            participate_end_time = rank_activity_const.get_rank_participate_end_timestamp(rank_type)
            create_time = self.get_create_time() or 0
            return create_time > participate_end_time
        rank = self.rank_reward_dict[rank_type]
        if rank <= 0:
            return True
        return False

    def is_offer_rank_percent_reward(self, rank_type):
        rank_reward_percent_info = self.rank_reward_percent_dict.get(rank_type)
        return rank_reward_percent_info and rank_reward_percent_info.get('rank') > 0 and rank_reward_percent_info.get('rank_length') > 0

    def request_offer_rank_percent_reward(self, rank_type):
        self.call_server_method('request_offer_rank_percent_reward', (rank_type,))

    @rpc_method(CLIENT_STUB, (Str('rank_type'), Int('rank'), Int('rank_length')))
    def respon_offer_rank_percent_reward(self, rank_type, rank, rank_length):
        self.rank_reward_percent_dict[rank_type] = {'rank': rank,'rank_length': rank_length}
        if rank <= 0:
            global_data.game_mgr.show_tip(get_text_by_id(15043))
            global_data.emgr.receive_rank_percent_reward_fail.emit()
        else:
            global_data.emgr.receive_rank_percent_reward_success.emit()