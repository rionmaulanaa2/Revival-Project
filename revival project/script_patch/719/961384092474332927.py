# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impMechaModule.py
from __future__ import absolute_import
import six
from six.moves import range
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Dict, Bool, Dict, Int, List, Str
from logic.gcommon.common_const import mecha_const
from common.cfg import confmgr

class impMechaModule(object):

    def _init_mechamodule_from_dict(self, bdict):
        self._mecha_module_plans = bdict.get('mecha_module_plans', {})
        self._mecha_module_plan_indices = bdict.get('mecha_module_plan_indices', {})
        self._mecha_temp_module_plans = {}

    def get_mecha_module_plan(self, mecha_id, plan_index):
        module_plans = self._mecha_module_plans.get(mecha_id, [])
        if not module_plans:
            return {}
        if 0 <= plan_index < len(module_plans):
            return module_plans[plan_index]
        return {}

    def get_mecha_module_cur_plan_index(self, mecha_id):
        return self._mecha_module_plan_indices.get(mecha_id, -1)

    def get_mecha_module_cur_plan(self, mecha_id):
        plan_index = self._mecha_module_plan_indices.get(mecha_id, -1)
        return self.get_mecha_module_plan(mecha_id, plan_index)

    def get_mecha_all_module_plan(self, mecha_id):
        return self._mecha_module_plans.get(mecha_id, [])

    def update_mecha_module_plan_config(self, mecha_id, plan_index, module_plan):
        if not self._is_valid_module_plan(mecha_id, plan_index, module_plan):
            return False
        if self._mecha_temp_module_plans:
            return False
        if mecha_id not in self._mecha_temp_module_plans:
            self._mecha_temp_module_plans[mecha_id] = {}
        self._mecha_temp_module_plans[mecha_id][plan_index] = module_plan
        self.call_server_method('update_mecha_module_plan_config', (mecha_id, plan_index, module_plan))
        return True

    @rpc_method(CLIENT_STUB, (Bool('result'), Int('mecha_id'), Int('plan_index')))
    def update_mecha_module_plan_result(self, result, mecha_id, plan_index):
        try:
            if result:
                self._mecha_module_plans[mecha_id][plan_index] = self._mecha_temp_module_plans[mecha_id][plan_index]
        except:
            pass

        self._mecha_temp_module_plans = {}
        self.on_update_mecha_module_plan_result(result, mecha_id, plan_index)

    @rpc_method(CLIENT_STUB, (Int('mecha_id'), List('module_plans'), Int('plan_index')))
    def update_mecha_module_plans(self, mecha_id, module_plans, plan_index):
        if not mecha_id or not module_plans:
            return
        self._mecha_module_plans[mecha_id] = module_plans
        self._mecha_module_plan_indices[mecha_id] = plan_index
        global_data.emgr.on_update_mecha_module_plans.emit(mecha_id, module_plans)

    def on_update_mecha_module_plan_result(self, result, mecha_id, plan_index):
        if result:
            global_data.emgr.update_mecha_module_plan_result_event.emit(mecha_id, plan_index)

    def _is_valid_module_plan(self, mecha_id, plan_index, module_plan):
        if not mecha_id or plan_index is None or not module_plan:
            return False
        else:
            if plan_index < 0 or plan_index >= mecha_const.MODULE_PLAN_AMOUNT:
                return False
            if len(module_plan) != mecha_const.MODULE_MAX_SLOT_COUNT:
                return False
            mecha_module_card_choice = self.get_owned_mecha_module_cards(mecha_id)
            if not mecha_module_card_choice:
                return False
            card_counter = []
            for slot_pos, card_id_list in six.iteritems(module_plan):
                if type(card_id_list) is not list:
                    return False
                for card_id in card_id_list:
                    if card_id in card_counter:
                        return False
                    if card_id not in mecha_module_card_choice.get(int(slot_pos), []):
                        return False
                    card_counter.append(card_id)

            return True

    def get_module_card_choices_config(self, mecha_id):
        from common.cfg import confmgr
        mecha_module_card_choice_config = {}
        card_choose_conf = confmgr.get('mecha_reinforce_card', 'CardChoiceConfig', 'Content')
        slot_prefix = 'slot_pos%d'
        common_conf = card_choose_conf.get('0', {})
        mecha_specific_conf = card_choose_conf.get(str(mecha_id), {})
        for slot in range(1, mecha_const.MODULE_MAX_SLOT_COUNT + 1):
            slot_key = slot_prefix % slot
            temp_list = []
            temp_list.extend(common_conf.get(slot_key, []))
            temp_list.extend(mecha_specific_conf.get(slot_key, []))
            mecha_module_card_choice_config[slot] = temp_list

        return mecha_module_card_choice_config

    def get_owned_mecha_module_cards(self, mecha_id, slot_pos=None):
        module_card_choice_config = self.get_module_card_choices_config(mecha_id)
        if not module_card_choice_config:
            log_error('impMechaModule get_owned_mecha_module_cards failed to get module card choice config with mecha_id=%s', mecha_id)
            return {}
        else:
            cards_conf = confmgr.get('mecha_reinforce_card', 'ModuleConfig', 'Content')
            total_own_cards = {}
            for slot, card_id_list in six.iteritems(module_card_choice_config):
                own_cards = []
                for card_id in card_id_list:
                    need_item_no = cards_conf.get(str(card_id), {}).get('item_no', None)
                    if need_item_no and self.has_item_by_no(need_item_no):
                        own_cards.append(card_id)

                total_own_cards[slot] = own_cards

            if not slot_pos:
                return total_own_cards
            return total_own_cards.get(slot_pos, [])
            return

    def get_mecha_module_card_gain_method(self, card_id):
        method_2_text_id = {mecha_const.MODULE_CARD_GAIN_VIA_GOT_MECHA: 601009,
           mecha_const.MODULE_CARD_GAIN_VIA_MECHA_PROFICIENCY_REWARD: 601010,
           mecha_const.MODULE_CARD_GAIN_VIA_SHOP_LOTTERY: 601011
           }
        cards_conf = confmgr.get('mecha_reinforce_card', 'ModuleConfig', 'Content')
        gain_method = cards_conf[str(card_id)].get('gain_method', mecha_const.MODULE_CARD_GAIN_VIA_SHOP_LOTTERY)
        return (
         gain_method, method_2_text_id.get(gain_method, 601011))

    def update_mecha_module_plan_index(self, mecha_id, plan_index):
        if 0 <= plan_index < mecha_const.MODULE_PLAN_AMOUNT:
            self._mecha_module_plan_indices[mecha_id] = plan_index
            self.call_server_method('update_mecha_module_plan_index', (mecha_id, plan_index))

    @rpc_method(CLIENT_STUB, (Bool('ret'), Int('mecha_id'), Int('plan_index')))
    def update_mecha_module_plan_index_ret(self, ret, mecha_id, plan_index):
        if not ret:
            return
        if 0 <= plan_index < mecha_const.MODULE_PLAN_AMOUNT:
            self._mecha_module_plan_indices[mecha_id] = plan_index

    def change_mecha_module_plan(self, mecha_id, plan_idx):
        self.call_soul_method('change_mecha_module_plan', (str(mecha_id), int(plan_idx)))