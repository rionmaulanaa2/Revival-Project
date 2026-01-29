# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impInteraction.py
from __future__ import absolute_import
from __future__ import print_function
import six
from common.cfg import confmgr
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Dict, Str, Int, Bool
from logic.gcommon.item import item_const as iconst
from logic.gcommon.common_const import interaction_const as ia_const
from copy import deepcopy
from logic.gcommon.common_const import role_const
from logic.gutils.mecha_skin_utils import get_mecha_skin_no_by_item_no

class impInteraction(object):
    MAX_INTERACTION_IDX_COUNT = 8

    def _init_interaction_from_dict(self, bdict):
        ia_data = bdict.get('interaction', {})
        self._ia_data = self._key_str_to_int(ia_data)
        self._auto_ia_data = bdict.get('auto_interaction', {})

    def _key_str_to_int(self, raw_data):
        res = {}
        for aid, raw_info in six.iteritems(raw_data):
            info = {}
            for idx, value in six.iteritems(raw_info):
                info[int(idx)] = value

            res[aid] = info

        return res

    def _idx_str_to_int(self, str_idx_data):
        res = {}
        for str_idx, item_no in six.iteritems(str_idx_data):
            res[int(str_idx)] = item_no

        return res

    def get_interaction_data(self, is_auto_mode=False):
        if not is_auto_mode:
            return self._ia_data
        return self._auto_ia_data

    def get_role_interaction_data(self, role_id, is_auto_mode=False):
        _role_id = role_const.INTERACTION_KEY
        if not is_auto_mode:
            return self._ia_data.get(str(_role_id), {})
        return self._auto_ia_data.get(str(_role_id), {})

    def try_set_interaction_data(self, actor_id, idx, item_no):
        if idx is None or item_no is None or actor_id is None:
            log_error('impInteraction input error: actor_id=%s, idx=%s, item_no=%s', actor_id, idx, item_no)
            return
        else:
            if isinstance(idx, int) and (idx < 0 or idx >= self.MAX_INTERACTION_IDX_COUNT):
                log_error('impInteraction idx error: actor_id=%s, idx=%s, item_no=%s', actor_id, idx, item_no)
                return
            actor_id = role_const.INTERACTION_KEY
            idx = str(idx)
            self.call_server_method('try_set_interaction_data', (actor_id, idx, item_no))
            return

    def is_dict_diff(self, dict1, dict2):
        print(dict1, dict1)
        for k, v in six.iteritems(dict1):
            v2 = dict2.get(k, None)
            if v2 != v:
                return True

        for k, v in six.iteritems(dict2):
            v2 = dict1.get(k, None)
            if v2 != v:
                return True

        return

    @rpc_method(CLIENT_STUB, (Str('actor_id'), Dict('update_dict'), Bool('is_auto_mode')))
    def on_set_interaction_data(self, actor_id, update_dict, is_auto_mode):
        if is_auto_mode:
            self.on_set_auto_interaction_data(actor_id, update_dict)
            return
        update_dict = self._idx_str_to_int(update_dict)
        self._ia_data.setdefault(actor_id, {})
        original_dict = deepcopy(self._ia_data[actor_id])
        self._ia_data[actor_id].update(update_dict)
        new_dict = self._ia_data[actor_id]
        if self.is_dict_diff(original_dict, new_dict):
            self.on_change_interaction_data(actor_id, update_dict)

    def on_set_auto_interaction_data(self, actor_id, update_dict):
        self._auto_ia_data.setdefault(actor_id, {})
        original_dict = deepcopy(self._auto_ia_data[actor_id])
        self._auto_ia_data[actor_id].update(update_dict)
        new_dict = self._auto_ia_data[actor_id]
        if self.is_dict_diff(original_dict, new_dict):
            self.on_change_interaction_data(actor_id, update_dict)

    @rpc_method(CLIENT_STUB, (Int('ret'), Str('str_idx'), Int('item_no')))
    def on_set_interaction_failed(self, ret, str_idx, item_no):
        print('set result failed')

    def on_change_interaction_data(self, actor_id, update_dict):
        global_data.emgr.on_change_interaction_data.emit(actor_id)

    def on_try_spray(self, bdict):
        spray_id = bdict['spray_id']
        lst_pos = bdict['position']
        lst_elr_rot = bdict['euler_rotation']
        ex_data = {'create_time': bdict['create_time']}
        self.sync_visit_action('on_spray', (spray_id, lst_pos, lst_elr_rot, ex_data))

    def on_try_gesture(self, gesture_id):
        self.sync_visit_action('on_gesture', (self.get_role(), gesture_id))

    def on_try_emoji(self, emoji_id):
        mecha_skin_no, mecha_skin_kill_cnt = (None, None)
        belong_id = confmgr.get('lobby_item', str(emoji_id), 'belong_id')
        if belong_id:
            mecha_skin_no = get_mecha_skin_no_by_item_no(emoji_id)
            mecha_skin_kill_cnt = global_data.player.get_mecha_skin_kill_cnt(belong_id).get('total_kill', 0)
        self.sync_visit_action('on_emoji', (emoji_id, mecha_skin_no, mecha_skin_kill_cnt))
        return None