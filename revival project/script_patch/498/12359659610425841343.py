# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impSlotMachine.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, MailBox, Dict, Int, Bool, Uuid, List, Float
NUMBER_KEY = 'number'
DISCOUNT_KEY = 'discount'
INIT_NUMBER_KEY = 'init_number'

class impSlotMachine(object):

    def _init_slotmachine_from_dict(self, bdict):
        self.slot_machine_record = bdict.get('slot_machine_record', {})

    def start_slot_machine(self, lottery_id):
        self.call_server_method('start_slot_machine', (str(lottery_id),))

    @rpc_method(CLIENT_STUB, (Str('lottery_id'), Dict('record')))
    def receive_slot_machine_ret(self, lottery_id, record):
        self.slot_machine_record[lottery_id] = record
        global_data.emgr.receive_slot_machine_ret_event.emit()

    def get_slot_machine_record(self, lottery_id):
        return self.slot_machine_record.get(lottery_id, {})

    def get_slot_machine_init_number(self, lottery_id):
        return self.slot_machine_record.get(lottery_id, {}).get(INIT_NUMBER_KEY, 0)

    def get_slot_machine_number(self, lottery_id):
        return self.slot_machine_record.get(lottery_id, {}).get(NUMBER_KEY, 0)

    def get_slot_machine_discount(self, lottery_id):
        return self.slot_machine_record.get(lottery_id, {}).get(DISCOUNT_KEY, None)