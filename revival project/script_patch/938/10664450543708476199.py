# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impWebapp.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Bool, List, Dict
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from common.cfg import confmgr
from logic.gcommon.ctypes.Record import Record
from logic.gcommon.common_const import activity_const as acconst
from logic.gutils import task_utils

class impWebapp(object):
    WEBAPP_INFO_UP_HANDLE = {acconst.ACTIVITY_SPRING_CALL_FRIENDS: 'on_newyear_hongbao_update',
       acconst.ACTIVITY_EXCLUSIVE_MECHA: 'on_exclusive_mecha_update'
       }

    def _init_webapp_from_dict(self, bdict):
        self.webapp_reward_record = bdict.get('webapp_reward_record', {})

    def get_newyear_hongbao_draw_cnt(self, hongbao_id):
        hongbao_draw_dict = self.webapp_reward_record.get(acconst.ACTIVITY_SPRING_CALL_FRIENDS, {}).get('hongbao_draw', {})
        return hongbao_draw_dict.get(hongbao_id, 0)

    def get_newyear_task_dict(self):
        info = self.webapp_reward_record.get(acconst.ACTIVITY_SPRING_CALL_FRIENDS, {})
        return {'lucky_task_list': list(info.get('lucky_task_list', [])),
           'normal_task_list': list(info.get('normal_task_list', []))
           }

    def get_webapp_info(self, act_id):
        return self.webapp_reward_record.get(act_id, {})

    @rpc_method(CLIENT_STUB, (Str('act_id'), Dict('info')))
    def update_webapp_info(self, act_id, info):
        self.webapp_reward_record.setdefault(act_id, {})
        self.webapp_reward_record[act_id].update(info)
        handler = getattr(self, self.WEBAPP_INFO_UP_HANDLE[act_id])
        if handler:
            handler(info)
        global_data.emgr.on_web_app_info_update_event.emit(act_id)

    def on_newyear_hongbao_update(self, info):
        global_data.emgr.refresh_activity_list.emit()

    def query_newyear_hongbao_info(self):
        self.call_server_method('cus_game_query', (acconst.ACTIVITY_SPRING_CALL_FRIENDS,))

    def change_hongbao_task_reard(self, task_id):
        if task_id not in self.webapp_reward_record[acconst.ACTIVITY_SPRING_CALL_FRIENDS]['task_can_change']:
            return
        self.call_server_method('change_hongbao_task_reard', (task_id,))

    def receive_hongbao_task_reard(self, task_id):
        if task_id in self.webapp_reward_record.get(acconst.ACTIVITY_SPRING_CALL_FRIENDS, {}).get('lucky_task_list', []):
            self.call_server_method('receive_hongbao_task_reard', (task_id,))
            return
        received_normal_tasks = self.webapp_reward_record.get(acconst.ACTIVITY_SPRING_CALL_FRIENDS, {}).get('received_normal_tasks', [])
        if task_id in received_normal_tasks:
            return
        if len(received_normal_tasks) >= 2:
            return
        self.call_server_method('receive_hongbao_task_reard', (task_id,))

    def on_exclusive_mecha_update(self, info):
        pass

    def query_exclusive_mecha_info(self):
        self.call_server_method('cus_game_query', (acconst.ACTIVITY_EXCLUSIVE_MECHA,))