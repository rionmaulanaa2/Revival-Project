# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impInscription.py
from __future__ import absolute_import
from six.moves import range
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Tuple, Bool, Dict
from logic.gcommon.item import item_const
from logic.gutils.system_unlock_utils import is_sys_unlocked, SYSTEM_INSCRIPTION

class impInscription(object):

    def _init_inscription_from_dict(self, bdict):
        self._component_conf = bdict.get('component_conf', {})
        self._mecha_page_conf = bdict.get('mecha_page_conf', {})
        self._part_slots_conf = bdict.get('part_slots_conf', {})
        self._component_test_plan = bdict.get('component_test_plan', 1)
        self._has_open_inscription = bdict.get('open_inscription', False)
        self._component_list = set(bdict.get('component_list', []))

    @rpc_method(CLIENT_STUB, ())
    def open_inscription(self):
        self._has_open_inscription = True
        global_data.emgr.notify_inscription_open_event.emit()

    def has_open_inscription(self, check_lv=True):
        if check_lv:
            return self._has_open_inscription and is_sys_unlocked(SYSTEM_INSCRIPTION)
        else:
            return self._has_open_inscription

    def has_owned_component(self, com_id):
        return com_id in self._component_list

    def get_mecha_component_list(self):
        return self._component_list

    def upload_component_page_by_dict(self, mecha_id, page_idx, part_dict, sync=True):
        mecha_id = str(mecha_id)
        page_idx = str(page_idx)
        self._component_conf.setdefault(mecha_id, {})
        self._component_conf[mecha_id][page_idx] = part_dict
        self.save_component_page(mecha_id, page_idx, sync)

    @rpc_method(CLIENT_STUB, (Str('mecha_id'), Str('page_idx'), Dict('part_dict')))
    def on_update_component_page(self, mecha_id, page_idx, part_dict):
        self.upload_component_page_by_dict(mecha_id, page_idx, part_dict, sync=False)

    def save_component_page(self, mecha_id, page_idx, sync=True):
        mecha_id = str(mecha_id)
        page_idx = str(page_idx)
        part_items = self._component_conf.get(mecha_id, {}).get(page_idx, {})
        sync and self.call_server_method('save_component_page', (mecha_id, page_idx, part_items))
        global_data.emgr.mecha_component_update_event.emit(int(mecha_id), page_idx)

    def buy_mecha_component(self, item_no):
        self.call_server_method('buy_component', (item_no,))

    @rpc_method(CLIENT_STUB, (Int('com_id'), Bool('ret')))
    def buy_mecha_component_ret(self, com_id, ret):
        if ret:
            self._component_list.add(com_id)
            self.on_buy_mecha_component_suc(com_id)

    def on_buy_mecha_component_suc(self, com_id):
        from logic.gcommon.cdata.mecha_component_conf import GIVE_COM_LIST
        if com_id not in GIVE_COM_LIST:
            self.offer_reward_imp({'item_dict': {com_id: 1}}, None)
        global_data.emgr.mecha_component_purchase_success.emit(com_id)
        return

    @rpc_method(CLIENT_STUB, (Str('part'), Int('slot_idx')))
    def unlock_part_slot_succ(self, part, slot_idx):
        self._part_slots_conf.setdefault(part, [0])
        self._part_slots_conf[part].append(slot_idx)
        self.notify_slot_unlocked(part, slot_idx)

    def notify_slot_unlocked(self, part, slot_idx):
        global_data.emgr.mecha_component_slot_unlocked_event.emit(part, slot_idx)

    def unlock_component_page(self, mecha_id):
        mecha_id = str(mecha_id)
        self.call_server_method('unlock_component_page', (mecha_id,))

    @rpc_method(CLIENT_STUB, (Str('mecha_id'),))
    def unlock_component_page_succ(self, mecha_id):
        self._mecha_page_conf.setdefault(mecha_id, ['0', item_const.MIN_MECHA_COMPONENT_PAGE_CNT, {}])
        self._mecha_page_conf[mecha_id][1] += 1
        self.notify_unlock_component_page_succ(mecha_id)

    def notify_unlock_component_page_succ(self, mecha_id):
        global_data.emgr.mecha_unlock_page_event.emit(mecha_id)

    def set_active_insc_page(self, mecha_id, page_idx):
        mecha_id = str(mecha_id)
        page_idx = str(page_idx)
        self.call_server_method('set_active_insc_page', (mecha_id, page_idx))
        self.on_active_insc_page_changed(mecha_id, page_idx)

    @rpc_method(CLIENT_STUB, (Bool('ret'), Str('mecha_id'), Str('page_idx')))
    def set_active_insc_page_ret(self, ret, mecha_id, page_idx):
        if not ret:
            return
        self.on_active_insc_page_changed(mecha_id, page_idx)

    def on_active_insc_page_changed(self, mecha_id, page_idx):
        self._mecha_page_conf.setdefault(mecha_id, ['0', item_const.MIN_MECHA_COMPONENT_PAGE_CNT, {}])
        self._mecha_page_conf[mecha_id][0] = page_idx
        global_data.emgr.mecha_component_change_active_page.emit(mecha_id, page_idx)

    def edit_component_page_name(self, mecha_id, page_idx, name):
        mecha_id = str(mecha_id)
        page_idx = str(page_idx)
        self.call_server_method('edit_component_page_name', (mecha_id, page_idx, name))
        self.on_component_page_name_changed(mecha_id, page_idx, name)

    def on_component_page_name_changed(self, mecha_id, page_idx, name):
        self._mecha_page_conf.setdefault(mecha_id, ['0', item_const.MIN_MECHA_COMPONENT_PAGE_CNT, {}])
        self._mecha_page_conf[mecha_id][2].update({page_idx: name})
        global_data.emgr.mecha_component_change_page_name.emit(mecha_id, page_idx, name)

    @rpc_method(CLIENT_STUB, (Str('mecha_id'), Str('page_idx'), Str('part'), Int('slot_idx'), Int('com_id')))
    def on_install_mecha_component(self, mecha_id, page_idx, part, slot_idx, com_id):
        self.install_mecha_component(mecha_id, page_idx, part, slot_idx, com_id, sync=False)

    def install_mecha_component(self, mecha_id, page_idx, part, slot_idx, com_id, sync=True):
        old_com_id = None
        mecha_id = str(mecha_id)
        page_idx = str(page_idx)
        part = str(part)
        sync and self.call_server_method('install_mecha_component', (mecha_id, page_idx, part, slot_idx, com_id))
        cur_mecha_page_conf = self._mecha_page_conf.get(mecha_id, {})
        if not cur_mecha_page_conf:
            self._mecha_page_conf.update({mecha_id: [page_idx, item_const.MIN_MECHA_COMPONENT_PAGE_CNT, {page_idx: ''}]})
        page_conf = self._mecha_page_conf[mecha_id][2]
        if not page_conf:
            page_conf.update({page_idx: ''})
        self._component_conf.setdefault(mecha_id, {})
        if page_idx not in self._component_conf[mecha_id]:
            self._component_conf[mecha_id].setdefault(page_idx, {})
        if not self._component_conf[mecha_id][page_idx].get(part):
            self._component_conf[mecha_id][page_idx].update({part: [ None for _ in range(item_const.COMPONENT_SLOT_CNT_PER_PART) ]})
        part_slot_conf = self._component_conf[mecha_id][page_idx][part]
        if slot_idx < len(part):
            old_com_id = part_slot_conf[slot_idx]
        else:
            old_com_id = None
        if slot_idx < item_const.COMPONENT_SLOT_CNT_PER_PART:
            part_slot_conf[slot_idx] = com_id
        else:
            log_error('unsupport component part slot idx', slot_idx)
        global_data.emgr.mecha_component_update_event.emit(int(mecha_id), page_idx)
        global_data.emgr.mecha_component_slot_update_event.emit(int(mecha_id), page_idx, part, slot_idx, com_id, old_com_id)
        return

    def check_is_valid_mecha_component_installation(self, mecha_id, page_idx, part, slot_idx, com_id):
        pass

    def get_mecha_component_page_conf(self, mecha_id):
        mecha_id = str(mecha_id)
        return self._mecha_page_conf.get(mecha_id, [])

    def get_mecha_component_page_num(self, mecha_id):
        mecha_id = str(mecha_id)
        if mecha_id not in self._mecha_page_conf:
            return item_const.MIN_MECHA_COMPONENT_PAGE_CNT
        return self._mecha_page_conf[mecha_id][1]

    def get_mecha_component_page_content_conf(self, mecha_id, page_index):
        mecha_id = str(mecha_id)
        page_index = str(page_index)
        return self._component_conf.get(mecha_id, {}).get(page_index, {})

    def get_unlock_slot_idx(self, part):
        return self._part_slots_conf.get(str(part), [])

    def get_mecha_cur_page_index(self, mecha_id):
        default_component_page_conf = self._mecha_page_conf.get(str(mecha_id), [])
        if not default_component_page_conf:
            page_index = str(0)
        else:
            page_index, _, _ = default_component_page_conf
        return page_index

    def get_mecha_all_component_conf(self, mecha_id):
        mecha_id = str(mecha_id)
        return self._component_conf.get(mecha_id, {})

    def change_mecha_component_page(self, mecha_id, page_idx):
        self.call_soul_method('change_mecha_component_page', (str(mecha_id), str(page_idx)))