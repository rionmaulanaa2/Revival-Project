# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaModule.py
from __future__ import absolute_import
import six
from six.moves import range
from ..UnitCom import UnitCom
from common.cfg import confmgr
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import mecha_const as mconst
from logic.gutils.MechaCardHandler import MechaCardHandler
import logic.gutils.reinforce_card_utils as card_util
from logic.gcommon.item import item_const
slot_prefix = 'slot_pos'

class ComMechaModule(UnitCom):
    BIND_EVENT = {'G_MECHA_CAN_INSTALL_MODULE': '_check_can_install_module',
       'E_MECHA_UNINSTALL_MODULE': '_uninstall_module',
       'E_MECHA_INSTALL_MODULE_RESULT': '_on_install_module_result',
       'E_MECHA_UNINSTALL_MODULE_RESULT': '_on_uninstall_module_result',
       'E_MECHA_CLEAR_MODULE_DATA': '_on_uninstall_all_module',
       'G_MECHA_INSTALLED_MODULE': '_get_installed_module',
       'G_MECHA_MODULE_CONFIG': '_get_module_config',
       'G_MECHA_ALL_INSTALLED_MODULE': '_get_all_installed_module',
       'G_MECHA_MODULE_SLOT_CONF': '_get_mecha_module_slot_conf',
       'G_MECHA_MODULE_SP_SLOT_PLAN': '_get_mecha_module_sp_slot_plan',
       'G_MECHA_SP_LOCKED_CARD_ID': '_get_sp_locked_card_id',
       'E_ON_JOIN_MECHA': ('_on_join_mecha', -10),
       'E_ON_LEAVE_MECHA': ('_on_leave_mecha', 10),
       'E_REFRESH_MECHA_MODULE': '_on_refresh_mecha_module',
       'G_MODULE_ITEM_SLOT_LV': '_get_module_slot_level',
       'G_AVAILABLE_MODULE': '_get_available_module',
       'G_REPLICATE_MODULE_PLANS': '_get_replicate_module_plans',
       'G_MECHA_CUR_MODULE_PLAN_INDEX': '_get_mecha_cur_module_plan_index',
       'G_MECHA_CUR_PAGE_INDEX': '_get_mecha_cur_page_index',
       'E_MECHA_CUR_MODULE_PLAN_INDEX': '_set_mecha_cur_module_plan_index',
       'E_MECHA_CUR_PAGE_INDEX': '_set_mecha_cur_page_index',
       'E_RECHOOSE_MECHA_MODULE_PLAN': '_update_replicate_module_plans'
       }

    def __init__(self):
        super(ComMechaModule, self).__init__(need_update=False)

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaModule, self).init_from_dict(unit_obj, bdict)
        self._module_config = {}
        self._module_plan = {}
        self._installed_modules = bdict.get('module_installed', {}) or {}
        self._sp_locked_card_id = bdict.get('sp_locked_card_id', None)
        self._module_card_slot_lv_dict = {}
        self._card_handler = MechaCardHandler()
        self.prepare_module_card_lv_dict()
        self._replicate_module_plans = bdict.get('replicate_module_plans', {})
        self._mecha_module_plan_indices = bdict.get('mecha_module_plan_indices', {})
        self._mecha_page_conf = bdict.get('mecha_page_conf', {})
        self._share_mecha_modules = bdict.get('share_mecha_modules', {})
        self._competition_mecha_modules = bdict.get('competition_mecha_modules', {})
        return

    def prepare_module_card_lv_dict(self):
        mecha_slot_conf = confmgr.get('mecha_reinforce_card', 'CardActivateItemConfig', 'Content')
        for slot_pos, slot_conf in six.iteritems(mecha_slot_conf):
            if slot_pos.startswith(slot_prefix):
                slot_pos = int(slot_pos[len(slot_prefix)])
            for idx, module_id in enumerate(slot_conf.get('activate_items', [])):
                if module_id not in mconst.SP_MODULE_ITEM_ALL_IDS:
                    module_lv = idx + 1 if 1 else 1
                    self._module_card_slot_lv_dict[module_id] = (
                     slot_pos, module_lv)

    def on_post_init_complete(self, bdict):
        if self.is_unit_obj_type('LAvatar'):
            global_data.emgr.on_update_mecha_module_plans += self.on_plan_update
            self.on_plan_update()

    def destroy(self):
        if self.is_unit_obj_type('LAvatar'):
            global_data.emgr.on_update_mecha_module_plans -= self.on_plan_update
        super(ComMechaModule, self).destroy()

    def on_plan_update(self, *args):
        if self.is_valid():
            mecha_id_type = self.ev_g_get_bind_mecha_type()
            if mecha_id_type:
                self._on_changed_mecha_type(mecha_id_type)

    def _get_installed_module(self, module_item_id):
        return self._installed_modules.get(module_item_id, None)

    def _on_install_module_result(self, result, slot_pos, card_id, item_id):
        if result:
            self._installed_modules[slot_pos] = [
             card_id, item_id]
            import logic.gcommon.common_const.mecha_const as m_const
            if item_id == m_const.SP_MODULE_CHOOSE_ITEM_ID:
                self._sp_locked_card_id = card_id
                self.check_need_activate_sp_module()
            self._on_add_module(card_id, item_id)
            self.send_event('E_NOTIFY_MODULE_CHANGED')
            self._send_mecha_event()

    def _send_mecha_event(self):
        bind_mecha_id = self.ev_g_get_bind_mecha()
        from mobile.common.EntityManager import EntityManager
        cont_mecha = EntityManager.getentity(bind_mecha_id)
        if cont_mecha and cont_mecha.logic:
            cont_mecha.logic.send_event('E_NOTIFY_MODULE_CHANGED')

    def _on_add_module(self, card_id, item_id):
        if not self._card_handler or not self._card_handler.can_handle_card():
            return
        else:
            card_effect_config = card_util.get_card_effect_config(card_id)
            if not card_effect_config:
                return
            for hander_name, effect_config in six.iteritems(card_effect_config):
                add_handler = getattr(self._card_handler, hander_name, None)
                if add_handler:
                    add_handler(card_id, item_id, effect_config)
                else:
                    log_error('ComMechaModule _on_add_module hander=%s not found ,card_id=%s', hander_name, card_id)

            return

    def _on_remove_module(self, card_id, item_id):
        if not self._card_handler or not self._card_handler.can_handle_card():
            return
        else:
            card_effect_config = card_util.get_card_effect_config(card_id)
            if not card_effect_config:
                return
            for hander_name, effect_config in six.iteritems(card_effect_config):
                remove_handler = getattr(self._card_handler, 'undo_' + hander_name, None)
                if remove_handler:
                    remove_handler(card_id, item_id, effect_config)
                else:
                    log_error('ComMechaModule _on_remove_module hander=%s not found ,card_id=%s', hander_name, card_id)

            return

    def _can_uninstall_module(self, slot_pos):
        return slot_pos in self._installed_modules

    def _uninstall_module(self, slot_pos):
        if not self._can_uninstall_module(slot_pos):
            return False
        else:
            valid_pos = None
            if global_data.mecha and global_data.mecha.logic:
                model = global_data.mecha.logic.ev_g_model()
                pos = global_data.mecha.logic.ev_g_position()
                from logic.gutils import item_utils
                valid_pos = item_utils.get_valid_drop_pos(self.scene, pos, model)
            on_train, tmp_train_carriage = global_data.carry_mgr.is_player_on_train()
            if on_train and tmp_train_carriage and tmp_train_carriage.logic:
                valid_pos_vec = global_data.player.logic.ev_g_position()
                valid_pos = [valid_pos_vec.x, valid_pos_vec.y, valid_pos_vec.z]
                cargo_info = tmp_train_carriage.logic.ev_g_pack_cargo_info(valid_pos)
            else:
                cargo_info = None
            global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'try_uninstall_mecha_module', (slot_pos, valid_pos, cargo_info), True, True)
            return

    def _on_uninstall_module_result(self, result, slot_pos, card_id, clear_item):
        if result:
            if slot_pos in self._installed_modules:
                card_id, item_id = self._installed_modules[slot_pos]
                if slot_pos in self._installed_modules and clear_item:
                    del self._installed_modules[slot_pos]
                self._on_remove_module(card_id, item_id)
                self.send_event('E_NOTIFY_MODULE_CHANGED')
                self._send_mecha_event()
            else:
                log_error('_on_uninstall_module_result keyError', slot_pos, self._installed_modules)

    def _on_uninstall_all_module(self):
        for slot_pos in six.iterkeys(self._installed_modules):
            card_id, item_id = self._installed_modules[slot_pos]
            self._on_remove_module(card_id, item_id)

        self._installed_modules = {}
        self.send_event('E_NOTIFY_MODULE_CHANGED')
        self._send_mecha_event()

    def _get_module_config(self):
        return self._module_config

    def _get_all_installed_module(self):
        return self._installed_modules

    def _get_sp_locked_card_id(self):
        return self._sp_locked_card_id

    def _on_join_mecha(self, mecha_id, *args, **kwargs):
        target = EntityManager.getentity(mecha_id)
        if target is None:
            return
        else:
            self._card_handler.set_mecha_obj(target)
            mecha = target.logic
            mecha_type_id = mecha.share_data.ref_mecha_id
            self._on_changed_mecha_type(mecha_type_id, is_share=target.is_share())
            for card_id, item_id in six.itervalues(self._installed_modules):
                self._on_add_module(card_id, item_id)

            global_data.game_mgr.delay_exec(0.03, self.check_need_activate_sp_module)
            return

    def _on_leave_mecha(self):
        if global_data.player and self.unit_obj and global_data.player.id == self.unit_obj.id:
            global_data.ui_mgr.close_ui('MechaModuleSpSelectUI')

    def check_need_activate_sp_module(self):
        import logic.gcommon.common_const.mecha_const as m_const
        if m_const.SP_MODULE_SLOT in self._installed_modules:
            cur_card_id, item_id = self._installed_modules[m_const.SP_MODULE_SLOT]
            if cur_card_id or item_id in mconst.SP_MODULE_NO_CHOOSE_ITEM_IDS:
                return
            if global_data.player and self.unit_obj and global_data.player.id == self.unit_obj.id and self.ev_g_get_bind_mecha_type():
                if self.ev_g_in_mecha('Mecha'):
                    slot_conf = self._get_mecha_module_slot_conf(m_const.SP_MODULE_SLOT)
                    if len(slot_conf) >= 2:
                        global_data.ui_mgr.close_ui('MechaModuleSpSelectUI')
                        if global_data.battle and not global_data.battle.is_settled():
                            global_data.ui_mgr.show_ui('MechaModuleSpSelectUI', 'logic.comsys.mecha_ui')
                    elif len(slot_conf) > 0:
                        sel_card_id, _ = slot_conf[0]
                        self.send_event('E_CALL_SYNC_METHOD', 'activate_module', (m_const.SP_MODULE_SLOT, sel_card_id), True, True)

    def _get_sp_no_choose_item_activate_card_id(self, item_id):
        plan_card_list = self._module_plan.get(mconst.SP_MODULE_SLOT, [])
        if not plan_card_list:
            return 0
        item_index = mconst.SP_MODULE_NO_CHOOSE_ITEM_IDS.index(item_id)
        sel_card_id = plan_card_list[item_index] if item_index < len(plan_card_list) else 0
        return sel_card_id

    def _on_changed_mecha_type(self, mecha_type, is_share=False):
        mecha_slot_conf = confmgr.get('mecha_reinforce_card', 'CardActivateItemConfig', 'Content')
        if not self.is_unit_obj_type('LAvatar'):
            return
        self._module_config = {}
        self._module_plan = {}
        if not global_data.player:
            return
        self._module_plan = global_data.player.get_mecha_module_cur_plan(int(mecha_type))
        if not self._module_plan and is_share:
            mecha_specific_conf = confmgr.get('mecha_reinforce_card', 'CardChoiceConfig', 'Content').get(str(mecha_type), {})
            _module_plan = {}
            slot_prefix_txt = 'slot_pos%d'
            for slot in range(1, mconst.MODULE_MAX_SLOT_COUNT + 1):
                slot_key = slot_prefix_txt % slot
                slots = mecha_specific_conf.get(slot_key, [])
                def_slot = []
                if slots:
                    def_slot = [
                     slots[0]]
                    if slot == mconst.SP_MODULE_SLOT and len(slots) >= 2:
                        def_slot.append(slots[1])
                self._module_plan[slot] = def_slot

        elif not self._module_plan and int(mecha_type) in self._share_mecha_modules:
            self._module_plan = self._share_mecha_modules[int(mecha_type)]
        elif not self._module_plan and int(mecha_type) in self._competition_mecha_modules:
            self._module_plan = self._competition_mecha_modules[int(mecha_type)]
        for slot_pos, plan_card_list in six.iteritems(self._module_plan):
            item_ids = mecha_slot_conf.get(slot_prefix + str(slot_pos), {}).get('activate_items', [])
            if slot_pos != mconst.SP_MODULE_SLOT:
                self._module_config[slot_prefix + str(slot_pos)] = [ [card_id, item_id] for item_id in item_ids for card_id in plan_card_list ]
            else:
                self._module_config[slot_prefix + str(slot_pos)] = [ [plan_card_list[i], mconst.SP_MODULE_NO_CHOOSE_ITEM_IDS[i]] for i in range(len(plan_card_list)) ]

    def _on_refresh_mecha_module(self, left_modules):
        self._installed_modules = left_modules
        self.send_event('E_NOTIFY_MODULE_CHANGED')
        self._send_mecha_event()

    def _get_mecha_module_slot_conf(self, slot):
        slot_pos_key = slot_prefix + str(slot)
        return self._module_config.get(slot_pos_key, [])

    def _get_mecha_module_sp_slot_plan(self):
        if not self._module_plan:
            return []
        else:
            return self._module_plan.get(mconst.SP_MODULE_SLOT, [])

    def _get_module_slot_level(self, ref_item_id):
        return self._module_card_slot_lv_dict.get(ref_item_id, (None, None))

    def _get_available_module(self, item_id):
        pos, lv = self._get_module_slot_level(item_id)
        if lv is None:
            return False
        else:
            data = self._installed_modules.get(pos)
            if not data:
                return True
            card_id, item_id = data
            _, installed_lv = self._get_module_slot_level(item_id)
            if installed_lv is None:
                return False
            return installed_lv < lv

    def _check_can_install_module(self, item_id):
        if item_id == mconst.SP_MODULE_CHOOSE_ITEM_ID:
            return True
        else:
            pos, lv = self._get_module_slot_level(item_id)
            if lv is None or pos is None:
                return False
            data = self._installed_modules.get(pos)
            if not data:
                return True
            installed_card_id, installed_item_id = data
            if item_id in mconst.SP_MODULE_NO_CHOOSE_ITEM_IDS:
                if installed_item_id == item_id:
                    return False
                activate_card_id = self._get_sp_no_choose_item_activate_card_id(item_id)
                return installed_card_id <= 0 or activate_card_id != installed_card_id
            _, installed_lv = self._get_module_slot_level(installed_item_id)
            if installed_lv is None:
                return False
            return lv > installed_lv

    def _get_replicate_module_plans(self):
        return self._replicate_module_plans

    def _get_mecha_cur_module_plan_index(self, mecha_id):
        return self._mecha_module_plan_indices.get(mecha_id)

    def _get_mecha_cur_page_index(self, mecha_id):
        page_conf = self._mecha_page_conf.get(str(mecha_id))
        if not page_conf or not isinstance(page_conf, list):
            return 0
        return page_conf[0]

    def _set_mecha_cur_module_plan_index(self, mecha_id, plan_index):
        self._mecha_module_plan_indices[mecha_id] = plan_index

    def _set_mecha_cur_page_index(self, mecha_id, page_idx):
        self._mecha_page_conf.setdefault(str(mecha_id), ['0', item_const.MIN_MECHA_COMPONENT_PAGE_CNT, {}])
        self._mecha_page_conf[str(mecha_id)][0] = str(page_idx)

    def _update_replicate_module_plans(self, mecha_id, new_module_plan):
        self._replicate_module_plans[mecha_id] = new_module_plan