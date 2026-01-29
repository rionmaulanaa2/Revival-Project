# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impIntimacy.py
from __future__ import absolute_import
import six
import six_ex
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, Dict, List
from logic.gcommon.const import INTIMACY_MSG_TYPE_BUILD_REQUEST, INTIMACY_MSG_TYPE_BUILD_RECV, INTIMACY_MSG_TYPE_BUILD_AGREE, INTIMACY_MSG_TYPE_BUILD_REFUSE, INTIMACY_MSG_TYPE_DELETE_REQUEST, INTIMACY_MSG_TYPE_DELETE_RECV, INTIMACY_MSG_TYPE_DELETE_AGREE, INTIMACY_MSG_TYPE_DELETE_REFUSE, INTIMACY_MSG_TYPE_DELETE_FORCE, INTIMACY_MSG_TYPE_OPERATION_FAIL, INTIMACY_MSG_TYPE_CHANGE_RELATION_NAME, INTIMACY_MSG_TYPE_LEVEL_UP, IDX_INTIMACY_NAME, IDX_INTIMACY_TYPE, IDX_INTIMACY_LV, INTIMACY_RELATION_TYPE_SET, INTIMACY_MECHA_SHARE_LV
from common.const.property_const import INTIMACY_DATA, INTIMACY_MSG_DATA
from logic.gcommon.const import INTIMACY_RELATION_DEFAULT_ORDER
from logic.comsys.intimacy.IntimacyMgr import IntimacyMgr
from logic.gcommon.common_const.scene_const import SCENE_LOTTERY
from logic.gcommon.cdata.intimacy_data import UNLOCK_MEMORY_LV

class impIntimacy(object):

    def _init_intimacy_from_dict(self, bdict):
        self.intimacy_data = bdict.get('intimacy_data', {})
        self.intimacy_relation_data = bdict.get('intimacy_relation_data', {})
        self.intimacy_msg_data = bdict.get('intimacy_msg_data', {})
        self.intimacy_cd_data = bdict.get('intimacy_cd_data', {})
        self.intimacy_week_limit = bdict.get('intimacy_week_limit', {})
        self.intimacy_day_limit = bdict.get('intimacy_day_limit', {})
        self.intimacy_relation_order = bdict.get('intimacy_relation_order', []) or INTIMACY_RELATION_DEFAULT_ORDER
        self.enable_inti_mem_frds = bdict.get('enable_inti_mem_frds', [])
        self.intimacy_lv_up_msg = {}
        IntimacyMgr()
        self._check_open_intimacy_event_data()

    def is_intimacy_friend(self, uid):
        for intimacy_type, frd_list in six.iteritems(self.intimacy_relation_data):
            if int(uid) in frd_list:
                return True

        return False

    def is_mecha_share_friend(self, uid):
        uid = str(uid)
        if uid not in self.intimacy_data:
            return False
        intimacy_lv = self.intimacy_data[str(uid)][IDX_INTIMACY_LV]
        intimacy_type = self.intimacy_data[str(uid)][IDX_INTIMACY_TYPE]
        if not intimacy_type:
            return False
        if intimacy_lv >= INTIMACY_MECHA_SHARE_LV:
            return True
        return False

    def _check_open_intimacy_event_data(self):
        for uid, intimacy_info in self.intimacy_data.items():
            if intimacy_info[IDX_INTIMACY_LV] >= UNLOCK_MEMORY_LV and self.is_intimacy_friend(uid) and uid not in self.enable_inti_mem_frds:
                global_data.intimacy_mgr.try_add_intimacy_event_msg(uid)

    @rpc_method(CLIENT_STUB, (Int('uid'), Str('msg_type'), Dict('msg_data')))
    def recv_intimacy_msg(self, uid, msg_type, msg_data):
        uid = str(uid)
        if msg_type == INTIMACY_MSG_TYPE_BUILD_AGREE:
            intimacy_type = msg_data.get('intimacy_type', None)
            self.add_relation(uid, intimacy_type)
            self.clear_msg_by_uid_and_type(uid, (INTIMACY_MSG_TYPE_BUILD_RECV, INTIMACY_MSG_TYPE_BUILD_REQUEST))
            self.add_msg_data(msg_type, uid, msg_data)
            intimacy_data = self.intimacy_data.get(uid, None)
            if intimacy_data:
                self.add_lv_up_msg(uid, 0, intimacy_data[IDX_INTIMACY_LV])
        elif msg_type in (INTIMACY_MSG_TYPE_DELETE_AGREE, INTIMACY_MSG_TYPE_DELETE_FORCE):
            self.remove_relation(uid, msg_data.get('intimacy_type', None), msg_data.get('cancel_timestamp', None))
            self.clear_msg_by_uid_and_type(uid, (INTIMACY_MSG_TYPE_DELETE_RECV, INTIMACY_MSG_TYPE_DELETE_REQUEST))
        elif msg_type == INTIMACY_MSG_TYPE_BUILD_REFUSE:
            self.clear_msg_by_uid_and_type(uid, INTIMACY_MSG_TYPE_BUILD_REQUEST)
        elif msg_type == INTIMACY_MSG_TYPE_DELETE_REFUSE:
            self.clear_msg_by_uid_and_type(uid, INTIMACY_MSG_TYPE_DELETE_REQUEST)
        elif msg_type in (INTIMACY_MSG_TYPE_BUILD_RECV, INTIMACY_MSG_TYPE_DELETE_RECV, INTIMACY_MSG_TYPE_BUILD_REQUEST, INTIMACY_MSG_TYPE_DELETE_REQUEST):
            self.add_msg_data(msg_type, uid, msg_data)
        elif msg_type == INTIMACY_MSG_TYPE_OPERATION_FAIL:
            self.add_msg_data(msg_type, uid, msg_data)
        if msg_type == INTIMACY_MSG_TYPE_BUILD_RECV:
            intimacy_type = msg_data.get('intimacy_type', None)
            global_data.intimacy_mgr.try_add_intimacy_request_msg(uid, intimacy_type)
            ui = global_data.ui_mgr.get_ui('OpenIntimacyRequestUI')
            in_battle = global_data.player.is_in_battle()
            in_lottery = global_data.game_mgr.scene.scene_type == SCENE_LOTTERY
            if not in_battle and ui == None and not in_lottery:
                global_data.intimacy_mgr.check_show_intimacy_request_ui()
        return

    @rpc_method(CLIENT_STUB, (Int('uid'), Dict('msg_data')))
    def on_change_intimacy_name(self, uid, msg_data):
        new_name = msg_data.get('intimacy_name', None)
        if new_name is not None:
            self.intimacy_data[str(uid)][IDX_INTIMACY_NAME] = new_name
            global_data.emgr.message_refresh_intimacy_data.emit()
        return

    @rpc_method(CLIENT_STUB, (Int('uid'), List('intimacy_data')))
    def on_intimacy_data_change(self, uid, intimacy_data):
        uid = str(uid)
        old_data = self.intimacy_data.get(uid, None)
        if old_data and old_data[IDX_INTIMACY_TYPE]:
            old_lv = old_data[IDX_INTIMACY_LV]
            new_lv = intimacy_data[IDX_INTIMACY_LV]
            self.add_lv_up_msg(uid, old_lv, new_lv)
            if old_lv != new_lv:
                uidA = int(min(int(self.uid), int(uid)))
                uidB = int(max(int(self.uid), int(uid)))
                global_data.message_data.request_intimacy_event_data(uidA, uidB)
        self.intimacy_data[uid] = intimacy_data
        global_data.emgr.message_refresh_intimacy_data.emit()
        return

    @rpc_method(CLIENT_STUB, (Str('intimacy_type'), List('intimacy_relation_data')))
    def on_intimacy_relation_data_change(self, intimacy_type, intimacy_relation_data):
        self.intimacy_relation_data[intimacy_type] = intimacy_relation_data

    @rpc_method(CLIENT_STUB, (Int('uid'), Int('new_limit')))
    def update_intimacy_week_limit_by_uid(self, uid, new_limit):
        self.intimacy_week_limit[str(uid)] = new_limit

    @rpc_method(CLIENT_STUB, ())
    def reset_intimacy_week_limit(self):
        self.intimacy_week_limit = {}

    @rpc_method(CLIENT_STUB, (Int('uid'), Int('item_no'), Int('new_limit')))
    def update_intimacy_day_limit_by_uid(self, uid, item_no, new_limit):
        day_limit_by_uid = self.intimacy_day_limit.setdefault(str(uid), {})
        day_limit_by_uid.update({str(item_no): new_limit
           })

    @rpc_method(CLIENT_STUB, ())
    def reset_intimacy_day_limit(self):
        self.intimacy_day_limit = {}

    @rpc_method(CLIENT_STUB, (Int('uid'),))
    def clear_intimacy_by_uid(self, uid):
        if str(uid) in self.intimacy_data:
            self.intimacy_data.pop(str(uid))
        for intimacy_type, frd_list in six.iteritems(self.intimacy_relation_data):
            if int(uid) in frd_list:
                frd_list.remove(uid)

        self.clear_msg_by_uid_and_type(uid, (INTIMACY_MSG_TYPE_BUILD_REQUEST, INTIMACY_MSG_TYPE_BUILD_RECV, INTIMACY_MSG_TYPE_DELETE_REQUEST, INTIMACY_MSG_TYPE_DELETE_RECV))
        if str(uid) in six_ex.keys(self.intimacy_cd_data):
            self.intimacy_cd_data.pop(str(uid))
        if str(uid) in six_ex.keys(self.intimacy_week_limit):
            self.intimacy_week_limit.pop(str(uid))
        if str(uid) in six_ex.keys(self.intimacy_day_limit):
            self.intimacy_day_limit.pop(str(uid))
        global_data.emgr.message_refresh_intimacy_data.emit()

    @rpc_method(CLIENT_STUB, (Int('uid'), Dict('msg_data')))
    def remove_relation_by_system(self, uid, msg_data):
        self.remove_relation(uid, msg_data.get('intimacy_type', None), msg_data.get('cancel_timestamp', None))
        self.clear_msg_by_uid_and_type(uid, (INTIMACY_MSG_TYPE_BUILD_RECV, INTIMACY_MSG_TYPE_BUILD_REQUEST))
        global_data.emgr.message_refresh_intimacy_data.emit()
        return

    @rpc_method(CLIENT_STUB, (Dict('doc'),))
    def on_unlock_intimacy_memory(self, doc):
        uid_str = doc.get('_id')
        uid_list = uid_str.split('_')
        uidA = int(min(int(uid_list[1]), int(uid_list[2])))
        uidB = int(max(int(uid_list[1]), int(uid_list[2])))
        global_data.message_data.set_intimacy_event_data(doc, uidA, uidB)

    @rpc_method(CLIENT_STUB, (Str('msg_type'), Dict('msg_data_by_type')))
    def update_intimacy_msg_data_by_msg_type(self, msg_type, msg_data_by_type):
        self.intimacy_msg_data[msg_type] = msg_data_by_type
        global_data.emgr.message_refresh_intimacy_data.emit()

    @rpc_method(CLIENT_STUB, (List('enable_inti_mem_frds'),))
    def on_enable_inti_mem_frds_change(self, enable_inti_mem_frds):
        self.enable_inti_mem_frds = enable_inti_mem_frds

    def build_relation_req(self, intimacy_type, uid):
        self.call_server_method('send_intimacy_msg', (uid, INTIMACY_MSG_TYPE_BUILD_REQUEST, {'intimacy_type': intimacy_type}))

    def build_relation_agree(self, uid, intimacy_type):
        self.call_server_method('send_intimacy_msg', (uid, INTIMACY_MSG_TYPE_BUILD_AGREE, {'intimacy_type': intimacy_type}))

    def build_relation_refuse(self, uid, intimacy_type):
        self.call_server_method('send_intimacy_msg', (uid, INTIMACY_MSG_TYPE_BUILD_REFUSE, {}))
        self.clear_msg_by_uid_and_type(uid, (INTIMACY_MSG_TYPE_BUILD_RECV, INTIMACY_MSG_TYPE_BUILD_REQUEST))

    def delete_intimacy_req(self, uid, intimacy_type):
        self.call_server_method('send_intimacy_msg', (uid, INTIMACY_MSG_TYPE_DELETE_REQUEST, {'intimacy_type': intimacy_type}))

    def delete_intimacy_agree(self, uid, intimacy_type):
        self.call_server_method('send_intimacy_msg', (uid, INTIMACY_MSG_TYPE_DELETE_AGREE, {'intimacy_type': intimacy_type}))

    def delete_relation_refuse(self, uid, intimacy_type):
        self.call_server_method('send_intimacy_msg', (uid, INTIMACY_MSG_TYPE_DELETE_REFUSE, {}))
        self.clear_msg_by_uid_and_type(uid, (INTIMACY_MSG_TYPE_DELETE_RECV, INTIMACY_MSG_TYPE_DELETE_REQUEST))

    def delete_intimacy_force(self, uid, intimacy_type):
        self.call_server_method('send_intimacy_msg', (uid, INTIMACY_MSG_TYPE_DELETE_FORCE, {'intimacy_type': intimacy_type}))

    def change_intimacy_name(self, uid, intimacy_name):
        self.call_server_method('send_intimacy_msg', (int(uid), INTIMACY_MSG_TYPE_CHANGE_RELATION_NAME, {'intimacy_name': intimacy_name}))

    def change_intimacy_show_order(self, order_list):
        self.intimacy_relation_order = order_list
        self.call_server_method('set_intimacy_relation_order', (order_list,))

    def request_unlock_intimacy_memory(self, uid):
        print (
         'request_unlock_intimacy_memory', uid)
        self.add_enable_inti_mem_frds([uid])
        self.call_server_method('request_unlock_intimacy_memory', (int(uid),))

    def add_enable_inti_mem_frds(self, frd_uids):
        print (
         'add_enable_inti_mem_frds', frd_uids)
        self.call_server_method('add_enable_inti_mem_frds', (frd_uids,))

    def clear_msg_by_uid_and_type(self, uid, msg_type):
        if type(msg_type) not in (tuple, list):
            msg_type = [
             msg_type]
        uid = str(uid)
        need_refresh = False
        for mtype in msg_type:
            msg_dict = self.intimacy_msg_data.get(mtype, {})
            if uid in msg_dict:
                del msg_dict[uid]
                need_refresh = True

        if need_refresh:
            global_data.emgr.message_refresh_intimacy_msg.emit()
        global_data.message_data.remove_intimacy_event_data_by_uid(self.uid, uid)

    def add_relation(self, uid, intimacy_type):
        if intimacy_type not in INTIMACY_RELATION_TYPE_SET:
            return
        else:
            uid = str(uid)
            intimacy_data = self.intimacy_data.get(uid, None)
            if intimacy_data is not None:
                intimacy_data[IDX_INTIMACY_TYPE] = intimacy_type
            self.intimacy_relation_data.setdefault(intimacy_type, [])
            self.intimacy_relation_data[intimacy_type].append(int(uid))
            global_data.emgr.message_refresh_intimacy_data.emit()
            return

    def remove_relation(self, uid, intimacy_type, cancel_stamp):
        uid = int(uid)
        intimacy_relation_data = self.intimacy_relation_data.get(intimacy_type, [])
        if uid in intimacy_relation_data:
            intimacy_relation_data.remove(uid)
        uid = str(uid)
        self.clear_msg_by_uid_and_type(uid, (INTIMACY_MSG_TYPE_DELETE_REQUEST, INTIMACY_MSG_TYPE_DELETE_RECV))
        intimacy_data = self.intimacy_data.get(uid, None)
        if intimacy_data is not None:
            intimacy_data[IDX_INTIMACY_TYPE] = None
            intimacy_data[IDX_INTIMACY_NAME] = None
        if cancel_stamp is not None:
            self.intimacy_cd_data[uid] = cancel_stamp
        global_data.emgr.message_refresh_intimacy_data.emit()
        return

    def add_msg_data(self, msg_type, uid, msg_data):
        self.intimacy_msg_data.setdefault(msg_type, {})
        self.intimacy_msg_data[msg_type][uid] = msg_data
        global_data.emgr.message_refresh_intimacy_msg.emit()

    def add_lv_up_msg(self, uid, old_lv, new_lv):
        from logic.gcommon.cdata.intimacy_data import LV_CAP, LV_CAP_REWARD_LV
        if old_lv == new_lv:
            return
        if new_lv == UNLOCK_MEMORY_LV:
            in_battle = global_data.player.is_in_battle()
            global_data.intimacy_mgr.try_add_intimacy_event_msg(uid)
            in_lottery = global_data.game_mgr.scene.scene_type == SCENE_LOTTERY
            if not in_battle and not in_lottery:
                global_data.intimacy_mgr.check_show_intimacy_event_ui()
        if old_lv >= LV_CAP:
            last_reward_level = old_lv - (old_lv - LV_CAP) % LV_CAP_REWARD_LV
            if new_lv - last_reward_level < LV_CAP_REWARD_LV:
                return
        self.intimacy_msg_data.setdefault(INTIMACY_MSG_TYPE_LEVEL_UP, {})
        self.intimacy_msg_data[INTIMACY_MSG_TYPE_LEVEL_UP].setdefault(uid, [old_lv, new_lv])
        self.intimacy_msg_data[INTIMACY_MSG_TYPE_LEVEL_UP][uid][1] = new_lv
        global_data.emgr.message_refresh_intimacy_msg.emit()