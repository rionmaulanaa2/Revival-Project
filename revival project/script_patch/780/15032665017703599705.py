# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaLobbyModuleWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.gutils.mecha_module_utils import get_module_card_name_and_desc, init_module_temp_item, get_module_card_name_and_desc
from logic.gutils.mall_utils import mecha_has_owned_by_mecha_id
from logic.gcommon.common_const import mecha_const
from logic.gutils.reinforce_card_utils import get_card_item_no
from logic.client.const.lobby_model_display_const import ROTATE_FACTOR
from logic.gutils import red_point_utils
LOBBY_MODULE_LEVEL = 3

class MechaLobbyModuleWidget(BaseUIWidget):
    slot_name_dict = {mecha_const.MODULE_ATTACK_SLOT: 18197,
       mecha_const.MODULE_DEFEND_SLOT: 18198,mecha_const.MODULE_MOVE_SLOT: 18199,
       mecha_const.SP_MODULE_SLOT: 18200}

    def __init__(self, parent_ui, panel, mecha_type):
        self.global_events = {'update_mecha_module_plan_result_event': self.update_mecha_module_plan,
           'on_update_mecha_module_plans': self.update_mecha_module_plans
           }
        super(MechaLobbyModuleWidget, self).__init__(parent_ui, panel)
        self._cur_mecha_id = mecha_type
        self._cur_seled_module_btn = None
        if global_data.player:
            self._module_plan_idx = global_data.player.get_mecha_module_cur_plan_index(self._cur_mecha_id)
        else:
            self._module_plan_idx = None
        return

    def init_widget(self, mecha_id):
        if not global_data.player:
            return
        if self._cur_mecha_id != mecha_id:
            self.set_selected_module_btn(False)
        self._cur_mecha_id = mecha_id
        has_own = mecha_has_owned_by_mecha_id(mecha_id)
        if not has_own:
            self.panel.nd_set_change.setVisible(False)
        else:
            self.panel.nd_set_change.setVisible(True)
        self.panel.nd_unlock.setVisible(True)
        self.panel.nd_lock.setVisible(False)
        self.hide_module_choose_panel()
        self._module_plan_idx = global_data.player.get_mecha_module_cur_plan_index(self._cur_mecha_id)
        self.init_module_plan_btns()
        self.refresh_module_plan(self._module_plan_idx)
        self.init_module_choose_btn()
        (
         self.panel.layer_module_choose.BindMethod('OnEnd', self._on_end_layer_module_choose),)
        self.panel.btn_describe.BindMethod('OnClick', self._on_click_rule_btn)
        if self.panel.nd_touch:
            self.panel.nd_touch.BindMethod('OnDrag', self._on_rotate_drag)
        if self.panel.btn_last_mech:
            self.panel.btn_last_mech.BindMethod('OnClick', self._on_show_last_mecha)
        if self.panel.btn_next_mech:
            self.panel.btn_next_mech.BindMethod('OnClick', self._on_show_next_mecha)
        if self.panel.lab_mecha_name:
            self.panel.nd_name.setVisible(True)
            mecha_name = confmgr.get('mecha_display', 'HangarConfig', 'Content', str(self._cur_mecha_id), 'name_mecha_text_id', default='')
            self.panel.lab_mecha_name.SetString(mecha_name)

    def on_switch_to_mecha_type(self, mecha_type):
        self.init_widget(mecha_type)

    def _on_end_layer_module_choose(self, *args):
        self.hide_module_choose_panel()

    def init_module_plan_btns(self):
        for idx in range(mecha_const.MODULE_PLAN_AMOUNT):
            btn = getattr(self.panel, 'btn_group_%d' % (idx + 1))
            if btn:

                def click_callback(btn, touch, plan_idx=idx):
                    if plan_idx == self._module_plan_idx:
                        return
                    global_data.game_mgr.show_tip(get_text_by_id(600001) % (plan_idx + 1))
                    if global_data.player:
                        global_data.player.update_mecha_module_plan_index(self._cur_mecha_id, plan_idx)
                        self.switch_cur_plan_index(plan_idx)

                btn.BindMethod('OnClick', click_callback)

    def _on_rotate_drag(self, layer, touch):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def _switch_plan_tab_btn(self, plan_index):
        for idx in range(mecha_const.MODULE_PLAN_AMOUNT):
            is_show = plan_index == idx
            btn = getattr(self.panel, 'btn_group_%d' % (idx + 1))
            if btn:
                btn.SetSelect(is_show)

    def switch_cur_plan_index(self, new_plan_index):
        self._module_plan_idx = new_plan_index
        self.hide_module_choose_panel()
        self.refresh_module_plan(new_plan_index)

    def refresh_module_plan(self, plan_idx):
        self._switch_plan_tab_btn(plan_idx)
        module_conf = global_data.player.get_mecha_module_plan(self._cur_mecha_id, plan_idx)
        if not module_conf:
            mecha_conf = confmgr.get('mecha_default_module_conf', default={})
            module_conf = mecha_conf.get(str(self._cur_mecha_id))
            slot_1 = module_conf.get('slot_pos1')
            slot_2 = module_conf.get('slot_pos2')
            slot_3 = module_conf.get('slot_pos3')
            slot_4 = module_conf.get('slot_pos4')
        else:
            slot_1 = module_conf.get(mecha_const.MODULE_ATTACK_SLOT)
            slot_2 = module_conf.get(mecha_const.MODULE_DEFEND_SLOT)
            slot_3 = module_conf.get(mecha_const.MODULE_MOVE_SLOT)
            slot_4 = module_conf.get(mecha_const.SP_MODULE_SLOT)
            if not slot_4 or len(slot_4) < mecha_const.MODULE_SP_SLOT_COUNT:
                mecha_conf = confmgr.get('mecha_default_module_conf', default={})
                module_conf = mecha_conf.get(str(self._cur_mecha_id))
                slot_4 = module_conf.get('slot_pos4')
        self.panel.nd_module_basic.list_ability.SetInitCount(len([slot_1, slot_2, slot_3]))
        ty_list = [mecha_const.MODULE_ATTACK_SLOT, mecha_const.MODULE_DEFEND_SLOT, mecha_const.MODULE_MOVE_SLOT]
        for idx, slot_info in enumerate([slot_1, slot_2, slot_3]):
            for card_id in slot_info:
                list_item = self.panel.nd_module_basic.list_ability.GetItem(idx)
                self.set_name_and_details(list_item.lab_name, None, card_id)
                slot = ty_list[idx]
                init_module_temp_item(list_item.temp_module, slot, card_id, LOBBY_MODULE_LEVEL)
                list_item.lab_sort.SetString(self.slot_name_dict.get(slot, 18197))

        self.panel.nd_module_special.list_ability.SetInitCount(mecha_const.MODULE_SP_SLOT_COUNT)
        for idx in range(mecha_const.MODULE_SP_SLOT_COUNT):
            if idx < len(slot_4):
                card_id = slot_4[idx]
            else:
                card_id = None
            sp_nd = self.panel.nd_module_special.list_ability.GetItem(idx)
            sp_nd.lab_sort.SetString(self.slot_name_dict.get(mecha_const.SP_MODULE_SLOT, 18197))
            if card_id:
                self.set_sp_name_and_details(sp_nd.nd_have.lab_name, None, card_id)
                init_module_temp_item(sp_nd.nd_have.temp_module, mecha_const.SP_MODULE_SLOT, card_id, LOBBY_MODULE_LEVEL)
            if card_id is None:
                sp_nd.nd_lock.setVisible(False)
                sp_nd.nd_have.setVisible(False)
                sp_nd.nd_empty.setVisible(True)
                sp_nd.btn_nml.SetEnable(True)
            else:
                sp_nd.nd_lock.setVisible(False)
                sp_nd.nd_have.setVisible(True)
                sp_nd.nd_empty.setVisible(False)
                sp_nd.btn_nml.SetEnable(True)

        return

    def set_name_and_details(self, name_nd, details_nd, card_id):
        card_name_desc, card_effect_desc = get_module_card_name_and_desc(card_id, None)
        name_nd.SetString(card_name_desc)
        if details_nd:
            details_nd.SetString(card_effect_desc)
        return

    def set_sp_name_and_details(self, name_nd, details_nd, card_id):
        if card_id:
            self.set_name_and_details(name_nd, details_nd, card_id)
        else:
            name_nd.SetString('')

    def hide_module_choose_panel(self):
        self.panel.temp_choose_list.setVisible(False)
        self.panel.layer_module_choose.setVisible(False)
        self.set_selected_module_btn(None)
        return

    def update_mecha_module_plan(self, mecha_id, plan_index):
        if mecha_id == self._cur_mecha_id and plan_index == self._module_plan_idx:
            self.refresh_module_plan(self._module_plan_idx)

    def update_mecha_module_plans(self, mecha_id, plans):
        if mecha_id == self._cur_mecha_id:
            if self._module_plan_idx < 0:
                self._module_plan_idx = global_data.player.get_mecha_module_cur_plan_index(self._cur_mecha_id)
            self.refresh_module_plan(self._module_plan_idx)
            self.init_module_choose_btn()

    def on_end_layer_module_choose(self, *args):
        self.hide_module_choose_panel()

    BTN_ATK_IDX = 0
    BTN_DFD_IDX = 1
    BTN_MOVE_IDX = 2
    BTN_SP1_IDX = 3
    BTN_SP2_IDX = 4

    def init_module_choose_btn(self):
        set_btn_list = [
         (
          mecha_const.MODULE_ATTACK_SLOT, 0, self.panel.nd_module_basic.list_ability, 0, self.BTN_ATK_IDX),
         (
          mecha_const.MODULE_DEFEND_SLOT, 0, self.panel.nd_module_basic.list_ability, 1, self.BTN_DFD_IDX),
         (
          mecha_const.MODULE_MOVE_SLOT, 0, self.panel.nd_module_basic.list_ability, 2, self.BTN_MOVE_IDX),
         (
          mecha_const.SP_MODULE_SLOT, 0, self.panel.nd_module_special.list_ability, 0, self.BTN_SP1_IDX),
         (
          mecha_const.SP_MODULE_SLOT, 1, self.panel.nd_module_special.list_ability, 1, self.BTN_SP2_IDX)]
        self.module_btn_list = []
        self.panel.nd_module_special.list_ability.SetInitCount(mecha_const.MODULE_SP_SLOT_COUNT)
        for module_slot, card_id_idx, module_list, module_btn_idx_in_list, module_btn_idx in set_btn_list:
            if module_btn_idx != len(self.module_btn_list):
                log_error('module_btn_idx value must match idx in set_btn_list!!!')
            module_node = module_list.GetItem(module_btn_idx_in_list)
            if not module_node:
                continue
            module_btn = module_node.btn_nml
            rp_item_nos = self.refresh_slot_red_point(module_btn, module_slot, module_btn_idx)

            def click_module_btn(btn, touch, m_slot=module_slot, card_id_idx=card_id_idx, rp_item_nos=rp_item_nos):
                self.set_selected_module_btn(btn)
                cur_plan = global_data.player.get_mecha_module_cur_plan(self._cur_mecha_id)
                plan_slot_id_list = cur_plan.get(m_slot, [])
                in_use_card_id_list = []
                if card_id_idx < len(plan_slot_id_list):
                    in_use_card_id_list.append(plan_slot_id_list[card_id_idx])
                self.init_module_choose_panel(m_slot, card_id_idx, in_use_card_id_list, plan_slot_id_list)
                self.panel.PlayAnimation('choose_appear')
                self.panel.layer_module_choose.setVisible(True)
                red_point_utils.show_red_point_template(btn.temp_red, False)
                for item_no in rp_item_nos:
                    if global_data.lobby_red_point_data.get_rp_by_no(item_no):
                        global_data.player.req_del_item_redpoint(item_no)

            module_btn.BindMethod('OnClick', click_module_btn)
            self.module_btn_list.append(module_btn)

    def select_module_btn--- This code section failed: ---

 248       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'None'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_3       3 
          12  POP_JUMP_IF_TRUE     19  'to 19'

 249      15  LOAD_CONST            0  ''
          18  RETURN_END_IF    
        19_0  COME_FROM                '12'

 250      19  LOAD_FAST             1  'module_btn_idx'
          22  LOAD_CONST            2  ''
          25  COMPARE_OP            0  '<'
          28  POP_JUMP_IF_TRUE     52  'to 52'
          31  LOAD_FAST             1  'module_btn_idx'
          34  LOAD_GLOBAL           2  'len'
          37  LOAD_FAST             0  'self'
          40  LOAD_ATTR             3  'module_btn_list'
          43  CALL_FUNCTION_1       1 
          46  COMPARE_OP            5  '>='
        49_0  COME_FROM                '28'
          49  POP_JUMP_IF_FALSE    56  'to 56'

 251      52  LOAD_CONST            0  ''
          55  RETURN_END_IF    
        56_0  COME_FROM                '49'

 252      56  LOAD_FAST             0  'self'
          59  LOAD_ATTR             3  'module_btn_list'
          62  LOAD_FAST             1  'module_btn_idx'
          65  BINARY_SUBSCR    
          66  STORE_FAST            2  'btn'

 253      69  LOAD_FAST             2  'btn'
          72  LOAD_ATTR             4  'OnClick'
          75  LOAD_FAST             2  'btn'
          78  CALL_FUNCTION_1       1 
          81  POP_TOP          
          82  LOAD_CONST            0  ''
          85  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9

    def refresh_slot_red_point(self, module_btn, module_slot, module_btn_idx):
        rp_item_nos = []
        mecha_slot_module_choices = global_data.player.get_module_card_choices_config(self._cur_mecha_id)
        slot_choices = mecha_slot_module_choices.get(module_slot, [])
        for card_id in slot_choices:
            item_no = get_card_item_no(card_id)
            rp_item_nos.append(item_no)

        has_red_point = False
        for rp_item_no in rp_item_nos:
            if global_data.lobby_red_point_data.get_rp_by_no(rp_item_no):
                has_red_point = True
                break

        red_point_utils.show_red_point_template(module_btn.temp_red, has_red_point)
        return rp_item_nos

    def set_selected_module_btn(self, btn):
        if self._cur_seled_module_btn:
            self._cur_seled_module_btn.SetSelect(False)
        self._cur_seled_module_btn = btn
        if self._cur_seled_module_btn:
            self._cur_seled_module_btn.SetSelect(True)

    def init_sp_lock_widget(self, lock_nd, mecha_id):
        if global_data.player:
            method_type = mecha_const.MODULE_CARD_GAIN_VIA_MECHA_PROFICIENCY_REWARD

            @lock_nd.btn_go.callback()
            def OnClick(btn, touch):
                self.show_to_gain_method_page(method_type)

    def show_to_gain_method_page(self, method_type, proficiency_level=None):
        global_data.emgr.show_to_gain_method_page_event.emit(method_type, proficiency_level=proficiency_level)

    def get_mecha_module_card_gain_method(self, card_id):
        method_2_text_id = {mecha_const.MODULE_CARD_GAIN_VIA_GOT_MECHA: 601009,
           mecha_const.MODULE_CARD_GAIN_VIA_MECHA_PROFICIENCY_REWARD: 601010,
           mecha_const.MODULE_CARD_GAIN_VIA_SHOP_LOTTERY: 601011
           }
        cards_conf = confmgr.get('mecha_reinforce_card', 'ModuleConfig', 'Content')
        gain_method = cards_conf[str(card_id)].get('gain_method', mecha_const.MODULE_CARD_GAIN_VIA_SHOP_LOTTERY)
        return (
         gain_method, method_2_text_id.get(gain_method, 601011))

    def init_module_choose_panel(self, slot, card_id_idx, cur_card_id_list, all_use_card_id_list):
        from logic.gutils.mecha_module_utils import init_module_temp_item, get_proficiency_level_by_card_id
        if not global_data.player:
            return
        else:
            cur_plan = global_data.player.get_mecha_module_plan(self._cur_mecha_id, self._module_plan_idx)
            if not cur_plan:
                cur_plan = []
            self.panel.temp_choose_list.lab_title.SetString(self.slot_name_dict.get(slot, 18197))
            mecha_slot_choices = global_data.player.get_module_card_choices_config(self._cur_mecha_id)
            has_own = mecha_has_owned_by_mecha_id(self._cur_mecha_id)
            if has_own:
                mecha_one_slot_choices = mecha_slot_choices.get(slot, []) if slot != mecha_const.SP_MODULE_SLOT else cur_card_id_list
            else:
                mecha_one_slot_choices = mecha_slot_choices.get(slot, [])
            mecha_one_slot_choices = sorted(mecha_one_slot_choices, key=lambda x: x not in cur_card_id_list)
            owned_mecha_module_cards = global_data.player.get_owned_mecha_module_cards(self._cur_mecha_id, slot)
            self.panel.temp_choose_list.list_choose.SetInitCount(len(mecha_one_slot_choices))
            all_item = self.panel.temp_choose_list.list_choose.GetAllItem()
            frame_list_sp = ['gui/ui_res_2/mech_display/pnl_module_bar_orange.png',
             'gui/ui_res_2/mech_display/pnl_module_bar_orange.png',
             'gui/ui_res_2/mech_display/pnl_module_bar_orange.png']
            frame_list_normal = ['gui/ui_res_2/mech_display/pnl_module_bar_purple.png',
             'gui/ui_res_2/mech_display/pnl_module_bar_purple.png',
             'gui/ui_res_2/mech_display/pnl_module_bar_purple.png']
            for idx, card_id in enumerate(mecha_one_slot_choices):
                ui_item = all_item[idx]
                red_point_utils.show_red_point_template(ui_item.temp_red, False)
                ui_item.btn_get.setVisible(False)
                ui_item.btn_choose.SetShowEnable(True)
                ui_item.img_ban.setVisible(False)
                ui_item.img_lock.setVisible(False)
                if slot == mecha_const.SP_MODULE_SLOT:
                    ui_item.btn_choose.SetFrames('', frame_list_sp, False, None)
                else:
                    ui_item.btn_choose.SetFrames('', frame_list_normal, False, None)
                self.set_name_and_details(ui_item.lab_name, ui_item.lab_details, card_id)
                init_module_temp_item(ui_item.temp_module, slot, card_id, LOBBY_MODULE_LEVEL)
                has_owned_card = True
                if card_id in cur_card_id_list:
                    ui_item.img_choose.setVisible(True)
                    ui_item.img_ban.setVisible(False)
                    ui_item.btn_choose.SetEnable(True)
                else:
                    ui_item.img_choose.setVisible(False)
                    if card_id in all_use_card_id_list:
                        ui_item.img_ban.setVisible(True)
                        ui_item.btn_choose.SetEnable(False)
                        item_no = get_card_item_no(card_id)
                        item_red_point = global_data.lobby_red_point_data.get_rp_by_no(item_no)
                        red_point_utils.show_red_point_template(ui_item.temp_red, item_red_point)
                    elif card_id in owned_mecha_module_cards:
                        ui_item.img_ban.setVisible(False)
                        ui_item.btn_choose.SetEnable(True)
                        item_no = get_card_item_no(card_id)
                        item_red_point = global_data.lobby_red_point_data.get_rp_by_no(item_no)
                        red_point_utils.show_red_point_template(ui_item.temp_red, item_red_point)
                    else:
                        has_owned_card = False
                        ui_item.img_lock.setVisible(True)
                        if mecha_has_owned_by_mecha_id(self._cur_mecha_id):
                            gain_method, text_id = global_data.player.get_mecha_module_card_gain_method(card_id)
                            ui_item.btn_get.SetText(text_id)
                            ui_item.btn_get.setVisible(True)
                        ui_item.btn_choose.SetShowEnable(False)

                @ui_item.btn_choose.callback()
                def OnClick(btn, touch, item_card_id=card_id, owned_card=has_owned_card):
                    if not global_data.player:
                        return
                    else:
                        if not owned_card:
                            global_data.game_mgr.show_tip(get_text_by_id(601012))
                            return
                        if item_card_id in all_use_card_id_list:
                            return
                        if slot not in cur_plan:
                            return
                        if card_id_idx >= len(cur_plan[slot]):
                            cur_plan[slot].append(item_card_id)
                        else:
                            cur_plan[slot][card_id_idx] = item_card_id
                        can_send = global_data.player.update_mecha_module_plan_config(self._cur_mecha_id, self._module_plan_idx, cur_plan)
                        if not can_send:
                            global_data.game_mgr.show_tip(get_text_by_id(600002))
                        else:
                            self.hide_module_choose_panel()
                            card_name, card_desc = get_module_card_name_and_desc(item_card_id, None)
                            global_data.game_mgr.show_tip(get_text_by_id(606047).format(card_name))
                        return

                @ui_item.btn_get.callback()
                def OnClick(btn, touch, item_card_id=card_id):
                    gain_method, text_id = global_data.player.get_mecha_module_card_gain_method(item_card_id)
                    self.show_to_gain_method_page(gain_method, proficiency_level=get_proficiency_level_by_card_id(item_card_id))

            return

    def destroy(self):
        super(MechaLobbyModuleWidget, self).destroy()

    def _on_click_rule_btn(self, btn, touch):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(get_text_local_content(600005), get_text_local_content(600004))

    def _on_show_last_mecha(self, btn, touch):
        ui = global_data.ui_mgr.get_ui('InscriptionMainUI')
        if ui:
            ui._on_show_last_mecha()

    def _on_show_next_mecha(self, btn, touch):
        ui = global_data.ui_mgr.get_ui('InscriptionMainUI')
        if ui:
            ui._on_show_next_mecha()