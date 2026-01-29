# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impPVEStory.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Bool, Int, List, Dict
from logic.gcommon.common_const.pve_const import PVE_STORY_REWARD_TYPE_CHAPTER, PVE_STORY_REWARD_TYPE_CLUE
from logic.gcommon.const import SHOP_PAYMENT_PVE_COIN, PLAYER_INFO_BRIEF
from common.const.property_const import C_NAME
from logic.gutils.item_utils import get_lobby_item_name
from common.utils.timer import CLOCK
import six_ex
REQUEST_RECEIVE_STORY_DEBRIS_INTERVAL = 10

class impPVEStory(object):

    def _init_pvestory_from_dict(self, bdict):
        self._pve_story_chapter_reward_get_list = bdict.get('pve_story_chapter_reward_get_list', [])
        self._pve_story_clue_reward_get_list = bdict.get('pve_story_clue_reward_get_list', [])
        self._pve_wished_debris_id = bdict.get('pve_wished_debris_id')
        self._unreceived_story_debris_dict = {}
        self._can_request_unreceived_story_debris = True

    def get_debris_reward_is_receive(self, reward_type, request_id):
        request_id = int(request_id)
        if reward_type == PVE_STORY_REWARD_TYPE_CHAPTER:
            return request_id in self._pve_story_chapter_reward_get_list
        if reward_type == PVE_STORY_REWARD_TYPE_CLUE:
            return request_id in self._pve_story_clue_reward_get_list
        return False

    def get_pve_wished_debris_id(self):
        return self._pve_wished_debris_id

    def get_unreceived_story_debris_dict(self):
        return self._unreceived_story_debris_dict

    def receive_story_debris_reward(self, reward_type, request_id):
        request_id = int(request_id)
        self.call_server_method('get_story_reward', (reward_type, request_id))

    def receive_all_story_debris_reward(self, receive_dict):
        self.call_server_method('request_receive_pve_story_all_reward', (receive_dict,))

    @rpc_method(CLIENT_STUB, (Bool('get_reward_succ'), Int('reward_type'), Int('request_id')))
    def on_get_story_reward(self, get_reward_succ, reward_type, request_id):
        if get_reward_succ:
            if reward_type == PVE_STORY_REWARD_TYPE_CHAPTER:
                self._pve_story_chapter_reward_get_list.append(request_id)
                global_data.emgr.on_pve_debris_chapter_reward_update.emit()
            elif reward_type == PVE_STORY_REWARD_TYPE_CLUE:
                self._pve_story_clue_reward_get_list.append(request_id)
                global_data.emgr.on_pve_debris_clue_reward_update.emit()

    @rpc_method(CLIENT_STUB, (Dict('receive_dict'),))
    def on_receive_pve_story_all_reward(self, receive_dict):
        receive_chapter_reward_list = receive_dict.get(PVE_STORY_REWARD_TYPE_CHAPTER)
        if receive_chapter_reward_list:
            self._pve_story_chapter_reward_get_list.extend(receive_chapter_reward_list)
            self._pve_story_chapter_reward_get_list = list(set(self._pve_story_chapter_reward_get_list))
        receive_clue_reward_list = receive_dict.get(PVE_STORY_REWARD_TYPE_CLUE)
        if receive_clue_reward_list:
            self._pve_story_clue_reward_get_list.extend(receive_clue_reward_list)
            self._pve_story_clue_reward_get_list = list(set(self._pve_story_clue_reward_get_list))
        global_data.emgr.on_receive_pve_story_all_reward_update.emit()

    def merge_story_debris(self, cost_dict, chapter_id):
        self.call_server_method('debris_merge', (cost_dict, int(chapter_id)))

    @rpc_method(CLIENT_STUB, (Bool('merge_succ'), Int('result_id')))
    def on_debris_merge(self, merge_succ, result_id):
        if merge_succ:
            global_data.emgr.on_pve_debris_merge.emit(result_id)
            from logic.comsys.battle.pve.PVEMainUIWidgetUI.PVEDebrisReceiveUI import PVEDebrisReceiveUI
            PVEDebrisReceiveUI(item_list=[result_id])
        self.check_cur_wished_debris()

    def donate_story_debris(self, debris_id, acceptor_uid):
        debris_id = int(debris_id)
        acceptor_uid = int(acceptor_uid)
        print ('donate_story_debris', debris_id, acceptor_uid)
        self.call_server_method('request_donate_pve_story_debris', (debris_id, acceptor_uid))

    @rpc_method(CLIENT_STUB, (Int('debris_id'), Int('acceptor_id')))
    def on_donate_story_debris_succ(self, debris_id, acceptor_id):
        data = global_data.message_data.get_player_inf(PLAYER_INFO_BRIEF, acceptor_id)
        acceptor_name = data.get(C_NAME)
        debris_name = get_lobby_item_name(debris_id)
        if acceptor_name and debris_name:
            global_data.game_mgr.show_tip(get_text_by_id(1400066).format(acceptor_name, debris_name))
        global_data.emgr.on_donate_story_debris_succ.emit(debris_id)

    def request_receive_pve_story_debris_by_donator(self, uid):
        uid = int(uid)
        print ('request_receive_pve_story_debris_by_donator', uid)
        self.call_server_method('request_receive_pve_story_debris_by_donator', (uid,))

    def receive_all_donate_story_debris(self):
        print 'receive_all_donate_story_debris'
        self.call_server_method('request_receive_all_pve_story_debris', ())

    def request_unreceived_story_debris(self):
        print 'request_unreceived_story_debris'
        if self._can_request_unreceived_story_debris:
            print 'call_server_method get_pve_story_debris_to_receive'
            self.call_server_method('get_pve_story_debris_to_receive', ())
            self._can_request_unreceived_story_debris = False
            self.request_timer = global_data.game_mgr.register_logic_timer(self.clear_request_story_debris_timer, interval=REQUEST_RECEIVE_STORY_DEBRIS_INTERVAL, times=1, mode=CLOCK)
        self.check_cur_wished_debris()

    def clear_request_story_debris_timer(self):
        self._can_request_unreceived_story_debris = True
        if self.request_timer:
            global_data.game_mgr.unregister_logic_timer(self.request_timer)
            self.request_timer = None
        return

    @rpc_method(CLIENT_STUB, (Int('donator_id'),))
    def on_receive_pve_story_debris_by_donator(self, donator_id):
        if self._unreceived_story_debris_dict.get(str(donator_id)):
            receive_reward_dict = self._unreceived_story_debris_dict.pop(str(donator_id))
        global_data.emgr.on_receive_pve_story_debris_by_donator.emit(donator_id)
        if receive_reward_dict:
            item_list = []
            origin_item_list = []
            for item_no, count in six_ex.items(receive_reward_dict):
                item_list.append([item_no, count])
                origin_item_list.append([])

            global_data.emgr.receive_award_succ_event_from_lottery.emit(item_list, origin_item_list)
        self.check_cur_wished_debris()

    @rpc_method(CLIENT_STUB, ())
    def on_receive_all_pve_story_debris(self):
        receive_reward_dict = {}
        item_list = []
        origin_item_list = []
        for debris_dict in six_ex.values(self._unreceived_story_debris_dict):
            for item_no, count in six_ex.items(debris_dict):
                if not receive_reward_dict.get(item_no):
                    receive_reward_dict[item_no] = 0
                receive_reward_dict[item_no] += count

        if receive_reward_dict:
            item_list = []
            origin_item_list = []
            for item_no, count in six_ex.items(receive_reward_dict):
                item_list.append([item_no, count])
                origin_item_list.append([])

            global_data.emgr.receive_award_succ_event_from_lottery.emit(item_list, origin_item_list)
        self._unreceived_story_debris_dict = {}
        global_data.emgr.on_receive_all_pve_story_debris.emit()
        self.check_cur_wished_debris()

    @rpc_method(CLIENT_STUB, (Dict('unreceived_story_debris_list'),))
    def on_get_pve_unreceived_story_debris(self, unreceived_story_debris_list):
        self._unreceived_story_debris_dict = unreceived_story_debris_list
        global_data.emgr.on_get_pve_unreceived_story_debris_update.emit()

    def request_change_pve_wished_debris_id(self, debris_id):
        print (
         'request_change_pve_wished_debris_id', debris_id)
        debris_id = int(debris_id)
        global_data.player.call_server_method('request_change_pve_wished_debris_id', (debris_id,))

    def check_cur_wished_debris(self):
        if self._pve_wished_debris_id:
            item_num = self.get_item_num_by_no(int(self._pve_wished_debris_id))
            if item_num > 0:
                self.request_change_pve_wished_debris_id(0)

    @rpc_method(CLIENT_STUB, (Int('debris_id'),))
    def on_change_pve_wished_debris(self, debris_id):
        self._pve_wished_debris_id = debris_id
        global_data.emgr.on_change_pve_wished_debris_id.emit()

    def decompose_story_debris(self, cost_dict, chapter_id):
        chapter_id = int(chapter_id)
        print ('decompose_story_debris', cost_dict, chapter_id)
        self.call_server_method('debris_decompose', (cost_dict, chapter_id))

    @rpc_method(CLIENT_STUB, (Bool('decompose_succ'), Int('get_num')))
    def on_debris_decompose(self, decompose_succ, get_num):
        if decompose_succ:
            global_data.emgr.on_pve_debris_decompose.emit()