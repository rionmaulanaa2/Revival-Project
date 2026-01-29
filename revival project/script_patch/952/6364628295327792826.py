# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impSpectate.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Dict, Bool, Dict, Int, List, Float, Str
from logic.gutils.SpectateMgr import SpectateMgr
from logic.gutils.ConnectHelper import ConnectHelper
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import spectate_const as sp_const
from collections import defaultdict
from logic.gcommon.ctypes.SpectateData import DECODE
from common.utils.timer import CLOCK
from logic.comsys.observe_ui.JudgeObservationListWidget import JudgeObservationListWidget, OB_LIST_TYPE_NEARBY, OB_LIST_TYPE_ALL_MAP
from logic.client.const import game_mode_const
from logic.gcommon.common_utils.local_text import get_text_by_id
import six

class impSpectate(object):
    CHECK_BATTLE_FOR_OB_SPECTATE_INTERVAL = 2

    def _init_spectate_from_dict(self, bdict):
        self._spectate_mgr = None
        self._has_liked = bdict.get('has_liked', [])
        self._spectate_likenum_per_day = bdict.get('spectate_likenum_per_day', {})
        local_spectate_mgr = EntityManager.get_entities_by_type('SpectateMgr')
        self._cached_spectate_brief_info = defaultdict(list)
        self._uid_2_recommend = {}
        self._check_ob_spectate_timer = None
        self._ob_try_times = 0
        self._ob_list_type = OB_LIST_TYPE_ALL_MAP
        self._can_req_manual_switch = True
        self.manual_required_spectate_id = None
        return

    def request_global_spectate_brief_list(self, list_type, uid_list=None):
        if list_type:
            if uid_list is None:
                uid_list = []
            self.call_server_method('request_global_spectate_brief_list', (list_type, uid_list))
        return

    def request_global_spectate_details(self, list_type, uid_list):
        if list_type and uid_list:
            self.call_server_method('request_global_spectate_details', (list_type, uid_list))

    @rpc_method(CLIENT_STUB, (Int('list_type'), List('info_list'), Dict('uid_2_recommend')))
    def respon_global_spectate_brief_list(self, list_type, info_list, uid_2_recommend):
        cached_list_info = self._cached_spectate_brief_info[list_type]
        del cached_list_info[:]
        cached_list_info.extend(info_list)
        if list_type == sp_const.SPECTATE_LIST_RECOMMEND:
            self._uid_2_recommend = uid_2_recommend
        global_data.emgr.on_received_global_spectate_brief_list.emit(list_type)

    @rpc_method(CLIENT_STUB, (Int('list_type'), List('info_list')))
    def respon_global_spectate_details(self, list_type, info_list):
        global_data.emgr.on_received_global_spectate_list.emit(list_type, info_list)

    def req_global_spectate(self, obj_id, obj_uid, shard_mb, stub_mb, battle_id, recommend_text, ask_for_caching=False, spectate_type=0):
        self.call_server_method('req_global_spectate', (obj_id, obj_uid, shard_mb, stub_mb, battle_id, recommend_text, ask_for_caching, spectate_type))

    @rpc_method(CLIENT_STUB, (Int('obj_uid'), Dict('detail')))
    def start_global_spectate(self, obj_uid, detail):
        self.do_start_global_spectate(detail)

    def req_stop_global_spectate(self):
        if not self._spectate_mgr:
            return
        self.call_server_method('finish_global_spectate', ())

    @rpc_method(CLIENT_STUB, (Int('msg_type'), Float('msg_time'), List('msg')))
    def global_spectate_msg(self, msg_type, msg_time, msg):
        self.do_global_spectate_add_msg(msg_type, msg_time, msg)

    def do_start_global_spectate(self, detail, from_file=False):
        if self._spectate_mgr:
            self.destroy_global_spectate()
        init_data = detail.get('battle_init_dict')
        if isinstance(init_data, six.binary_type):
            init_data = ConnectHelper().get_proto_encoder().decode(init_data)
        self._spectate_mgr = SpectateMgr()
        self._spectate_mgr.load_battle(detail['battle_id'], detail['battle_entity_type'], init_data, detail['soul_id'], from_file=from_file)

    def do_global_spectate_add_msg(self, msg_type, msg_time, msg):
        if self._spectate_mgr is None:
            return
        else:
            self._spectate_mgr.add_msg(msg_type, msg_time, msg)
            return

    def do_global_spectate_speed_up(self, key_frame_num):
        if self._spectate_mgr is None:
            return
        else:
            return self._spectate_mgr.speed_up(key_frame_num)

    def get_global_spectate_cached_size(self):
        if self._spectate_mgr:
            return self._spectate_mgr.get_cached_msg_size()
        return 0

    def is_in_global_spectate(self):
        return self._spectate_mgr is not None

    def global_spectate_start(self):
        if not self._spectate_mgr:
            return
        self._spectate_mgr.start()

    def search_spectate_by_uid(self, uid):
        self.call_server_method('search_spectate_by_uid', (uid,))

    def search_spectate_by_name(self, name):
        self.call_server_method('search_spectate_by_name', (name,))

    def destroy_global_spectate(self):
        if self._spectate_mgr:
            self._spectate_mgr.destroy()
            self._spectate_mgr = None
        self._has_liked = []
        return

    def reset_global_spectate_on_disconnect(self):
        from logic.gcommon import time_utility
        time_utility.reset_stamp_delta_battle()
        self._can_req_manual_switch = True

    def do_global_spectate_like(self, obj_uid):
        if not self.can_do_specate_like(obj_uid):
            return
        self._has_liked.append(obj_uid)
        self._spectate_likenum_per_day[obj_uid] = self._spectate_likenum_per_day.get(obj_uid, 0) + 1
        self.call_server_method('do_global_spectate_like', (obj_uid,))

    def on_global_spectate_timeout(self, from_ob=False, timeout_times=0):
        if not self._spectate_mgr:
            return
        self.call_server_method('global_spectate_time_out', (from_ob,))
        if timeout_times < 1:
            if from_ob:
                global_data.game_mgr.show_tip(get_text_by_id(19711), True)
            else:
                global_data.game_mgr.show_tip(get_text_by_id(19459), True)
        global_data.emgr.on_cancel_loading_spectate.emit()

    def can_do_specate_like(self, obj_uid, show_tip=True):
        if obj_uid in self._has_liked:
            return False
        like_num_today = self._spectate_likenum_per_day.get(obj_uid, 0)
        if like_num_today >= sp_const.SPECTATE_SAME_PLAYER_LIKE_MAX_NUM_PER_DAY:
            if show_tip:
                global_data.game_mgr.show_tip(get_text_by_id(19469))
            return False
        return True

    def req_global_spectate_hot_info(self, obj_uid):
        self.call_server_method('req_global_spectate_hot_info', (obj_uid,))

    @rpc_method(CLIENT_STUB, (Int('obj_uid'), Dict('info')))
    def on_global_spectate_hot_info(self, obj_uid, info):
        global_data.emgr.on_update_spectate_hot_info.emit(obj_uid, info)

    @rpc_method(CLIENT_STUB, (Int('reason'),))
    def on_global_spectate_fail(self, reason):
        global_data.game_mgr.show_tip(get_text_by_id(reason), True)
        global_data.emgr.on_cancel_loading_spectate.emit()

    @rpc_method(CLIENT_STUB, ())
    def reset_spectate_likenum_per_day(self):
        self._spectate_likenum_per_day = {}

    def clear_global_spectate_cached(self):
        self._cached_spectate_brief_info.clear()

    @rpc_method(CLIENT_STUB, (Int('num'), Str('name')))
    def local_be_like_info(self, num, name):
        global_data.emgr.on_be_like_num_changed.emit(num, name)

    def get_global_specate_brief_info(self, list_type):
        return self._cached_spectate_brief_info[list_type]

    def get_global_spectate_recommend_key(self, uid):
        from logic.gcommon.common_const import rank_const
        recommend_key = None
        if uid in self._uid_2_recommend:
            recommend_key = self._uid_2_recommend[uid]
        elif str(uid) in self._uid_2_recommend:
            recommend_key = self._uid_2_recommend[str(uid)]
        return recommend_key or rank_const.RANK_TYPE_MATCH_SCORE

    def get_global_spectate_player_uid(self):
        if self._spectate_mgr:
            return self._spectate_mgr.get_spectate_target_uid()
        return 0

    def get_global_spectate_player_id(self):
        if self._spectate_mgr:
            return self._spectate_mgr.get_spectate_target_id()
        else:
            return None

    def get_player_info_for_ob(self, soul_id, attr_name, default=None):
        if self._spectate_mgr:
            return self._spectate_mgr.get_player_info_for_ob(soul_id, attr_name, default)
        else:
            return None
            return None

    def req_global_spectate_switch(self, str_obj_id, obj_uid):
        if not self._can_req_manual_switch:
            if global_data.is_inner_server:
                pass
            return
        self.call_server_method('req_global_spectate_switch', (str_obj_id, obj_uid))
        self.manual_required_spectate_id = str_obj_id
        self._can_req_manual_switch = False

    @rpc_method(CLIENT_STUB, (Int('reason'),))
    def on_global_spectate_manual_switch_fail(self, reason):
        global_data.game_mgr.show_tip(get_text_by_id(reason), True)
        self._can_req_manual_switch = True
        global_data.emgr.spectate_manual_switch_fail.emit()

    @rpc_method(CLIENT_STUB, (Int('new_obj_uid'),))
    def on_global_spectate_manual_switch_success(self, new_obj_uid):
        if self._spectate_mgr is None or not new_obj_uid:
            return
        else:
            self._spectate_mgr.do_manual_switch(new_obj_uid)
            return

    def get_spectate_battle_id(self):
        if self._spectate_mgr is None:
            return
        else:
            return self._spectate_mgr.get_battle_id()

    def get_spectate_battle_top_player_infos(self):
        if self._spectate_mgr is None:
            return
        else:
            return self._spectate_mgr.get_top_player_infos()

    def on_global_spectate_switch_timeout(self, from_ob):
        global_data.game_mgr.show_tip(get_text_by_id(19608), True)
        self.call_server_method('global_spectate_time_out', (from_ob,))

    def reset_spectate_can_req_manual_switch(self):
        self._can_req_manual_switch = True

    @rpc_method(CLIENT_STUB, (Dict('battle_info'),))
    def on_ob_start_battle(self, battle_info):
        self._check_ob_spectate_timer = global_data.game_mgr.register_logic_timer(self._check_ob_spectate_cb, interval=impSpectate.CHECK_BATTLE_FOR_OB_SPECTATE_INTERVAL, times=-1, mode=CLOCK)
        self._check_ob_spectate_cb()
        global_data.ui_mgr.show_ui('JudgeLoadingUI', 'logic.comsys.observe_ui')
        self._can_req_manual_switch = True

    def _safely_unregist_check_ob_spectate_timer(self):
        if self._check_ob_spectate_timer is not None:
            global_data.game_mgr.unregister_logic_timer(self._check_ob_spectate_timer)
        self._check_ob_spectate_timer = None
        self._ob_try_times = 0
        return

    def _check_ob_spectate_cb(self):
        if self._ob_try_times > sp_const.SPECTATE_OB_MAX_TRY_TIMES:
            self._safely_unregist_check_ob_spectate_timer()
            return
        self.call_server_method('request_ob_global_spectate', ())
        self._ob_try_times += 1

    @rpc_method(CLIENT_STUB, (Dict('detail'),))
    def start_ob_global_spectate(self, detail):
        self._safely_unregist_check_ob_spectate_timer()
        if self._spectate_mgr:
            self.destroy_global_spectate()
        init_data = DECODE(detail.get('battle_init_dict'))
        self._spectate_mgr = SpectateMgr()
        self._spectate_mgr.load_battle(detail['battle_id'], detail['battle_entity_type'], init_data, detail.get('soul_id'), for_ob=True)
        self._ob_list_type = OB_LIST_TYPE_ALL_MAP

    @rpc_method(CLIENT_STUB, (Int('reason'),))
    def on_ob_global_spectate_fail(self, reason):
        self._safely_unregist_check_ob_spectate_timer()
        global_data.game_mgr.show_tip(get_text_by_id(reason), True)
        global_data.emgr.on_cancel_loading_spectate.emit()
        global_data.ui_mgr.close_ui('JudgeLoadingUI')

    def is_in_judge_ob(self):
        if self._spectate_mgr:
            return self._spectate_mgr.is_judge_spectate()
        return False

    def get_ob_list_type(self):
        return self._ob_list_type

    def set_ob_list_type(self, ob_list_type):
        if not self.is_in_judge_ob():
            return
        oldone = self._ob_list_type
        changed = ob_list_type != oldone
        self._ob_list_type = ob_list_type
        if changed:
            global_data.emgr.ob_list_type_changed.emit(oldone, ob_list_type)

    def get_all_player_info_for_ob(self):
        if not self.is_in_judge_ob():
            return {}
        if self._spectate_mgr:
            return self._spectate_mgr.get_all_player_info_for_ob()
        return {}

    def get_all_team_info_for_ob(self):
        if not self.is_in_judge_ob():
            return {}
        if self._spectate_mgr:
            return self._spectate_mgr.get_all_team_info_for_ob()
        return {}

    @rpc_method(CLIENT_STUB, (Int('result'),))
    def on_ob_send_battle_message_ret(self, result):
        if result < 0:
            self.notify_client_message((get_text_by_id(19602),))

    @rpc_method(CLIENT_STUB, (Int('result'),))
    def on_ob_kick_out_player_ret(self, result):
        if result < 0:
            log_error('ob_kick_out_player fail, ret: %s', result)

    def req_ob_operate_god_camera(self, operation_type, operation_data):
        if not self.is_in_judge_ob():
            return
        self.call_server_method('req_ob_operate_god_camera', (operation_type, operation_data))

    @rpc_method(CLIENT_STUB, (Int('operation_type'), Int('ret')))
    def on_ob_operate_god_camera_ret(self, operation_type, ret):
        if self._spectate_mgr is None:
            return
        else:
            return