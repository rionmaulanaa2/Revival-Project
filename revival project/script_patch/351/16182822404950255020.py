# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/TechAndModuleChooseWidget.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from logic.gutils import mecha_module_utils, template_utils, inscription_utils
from logic.gcommon.common_const import mecha_const
from logic.gcommon import const
from logic.gcommon.cdata.mecha_component_data import part2type
from logic.gcommon.cdata.mecha_component_conf import MAX_PAGE_NUM
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.client.const import game_mode_const
from logic.gutils.system_unlock_utils import is_sys_unlocked, SYSTEM_INSCRIPTION
from logic.gcommon.cdata.sys_unlock_data import get_system_unlock_lv
from logic.gcommon.item import item_const
from logic.comsys.battle.MechaSummonUI import SkillDetailsUI
BATTLE_MODULE_LEVEL = 3
PLAN_NAME_TEXT_IDS = [80750, 80751]
SUMMON_UI_LIST = ['MechaSummonUI', 'MechaSummonAndChooseSkinUI']

class TechAndModuleChooseWidget(object):

    def __init__(self, panel):
        self.panel = panel
        self.select_module_plan_node = None
        self.select_component_page_node = None
        self.init_widgets()
        self.process_event(True)
        return

    def destroy(self):
        self.process_event(False)
        self.select_module_plan_node = None
        self.select_component_page_node = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'hide_tech_and_module_choose_widget': self.hide,
           'click_mecha_btn_in_summon_ui': self.on_change_selected_mecha_btn
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def hide(self):
        if not self.panel.nd_change:
            return
        if self.panel.nd_change.nd_module.isVisible():
            self.hide_nd_module()
            return
        if self.panel.nd_change.nd_tech.isVisible():
            self.hide_nd_tech()
            return

    def hide_nd_module(self, play_anim=True):
        self.panel.nd_change.nd_module.setVisible(False)
        self.select_module_plan_node = None
        self.select_component_page_node = None
        play_anim and self.panel.PlayAnimation('disappear_module')
        return

    def hide_nd_tech(self, play_anim=True):
        self.panel.nd_change.nd_tech.setVisible(False)
        self.select_module_plan_node = None
        self.select_component_page_node = None
        play_anim and self.panel.PlayAnimation('disappear_tech')
        return

    def init_widgets(self):
        if self.should_hide_entry_btns():
            self.panel.nd_change.setVisible(False)
            return
        self.init_entry_btns()

    def should_hide_entry_btns(self):
        if global_data.player.in_local_battle():
            return True
        mode_type = global_data.game_mode.get_mode_type()
        if mode_type in (game_mode_const.GAME_MODE_FFA, game_mode_const.GAME_MODE_MECHA_DEATH, game_mode_const.GAME_MODE_EXERCISE, game_mode_const.GAME_MODE_ARMRACE, game_mode_const.GAME_MODE_GOOSE_BEAR):
            return True
        return False

    def get_mecha_summon_ui(self):
        for ui_name in SUMMON_UI_LIST:
            summon_ui = global_data.ui_mgr.get_ui(ui_name)
            if summon_ui:
                return summon_ui

        return None

    def init_entry_btns(self):
        player = global_data.player
        if not player or not player.logic:
            return
        else:
            summon_ui = self.get_mecha_summon_ui()
            if not summon_ui:
                return
            default_mecha_id = summon_ui.get_default_select_mecha_id()
            if not default_mecha_id:
                return
            cur_module_plan_index = player.logic.ev_g_mecha_cur_module_plan_index(default_mecha_id)
            if cur_module_plan_index is None:
                default_mecha_id = 8001
                cur_module_plan_index = player.logic.ev_g_mecha_cur_module_plan_index(default_mecha_id)
            self.panel.nd_change.nd_btn.btn_module.lab_module.SetString(PLAN_NAME_TEXT_IDS[cur_module_plan_index])
            cur_tech_page_index = player.logic.ev_g_mecha_cur_page_index(default_mecha_id)
            page_index = int(cur_tech_page_index) + 1
            page_name = get_text_by_id(81789).format(page_index)
            self.panel.nd_change.nd_btn.btn_tech.lab_tech.SetString(page_name)

            @self.panel.nd_change.nd_btn.btn_module.unique_callback()
            def OnClick(*args):
                self.on_click_btn_module()

            @self.panel.nd_change.nd_btn.btn_tech.unique_callback()
            def OnClick(*args):
                self.on_click_btn_tech()

            @self.panel.nd_change.nd_tech.unique_callback()
            def OnClick(*args):
                self.hide()

            @self.panel.nd_change.nd_module.unique_callback()
            def OnClick(*args):
                self.hide()

            return

    def on_click_btn_module(self, *args):
        if self.panel.nd_change.nd_tech.isVisible():
            self.hide_nd_tech(play_anim=False)
        if self.panel.nd_change.nd_module.isVisible():
            self.hide_nd_module(play_anim=True)
            return
        summon_ui = self.get_mecha_summon_ui()
        if not summon_ui:
            return
        mecha_id = summon_ui.get_select_mecha_id()
        if not mecha_id:
            return
        battle = global_data.battle
        if not battle:
            return
        if not battle.avatar_has_mecha(mecha_id):
            return
        global_data.emgr.hide_skill_detail_event.emit(['skill_detail', SkillDetailsUI])
        self.init_module_list(mecha_id)
        self.panel.nd_change.nd_module.setVisible(True)
        self.panel.PlayAnimation('show_module')

    def on_click_btn_tech(self, *args):
        if self.panel.nd_change.nd_module.isVisible():
            self.hide_nd_module(play_anim=False)
        if self.panel.nd_change.nd_tech.isVisible():
            self.hide_nd_tech(play_anim=True)
            return
        if not is_sys_unlocked(SYSTEM_INSCRIPTION):
            unlock_lv = get_system_unlock_lv(SYSTEM_INSCRIPTION)
            global_data.game_mgr.show_tip(get_text_by_id(81866, {'lv': unlock_lv}), True)
            return
        summon_ui = self.get_mecha_summon_ui()
        if not summon_ui:
            return
        mecha_id = summon_ui.get_select_mecha_id()
        if not mecha_id:
            return
        battle = global_data.battle
        if not battle:
            return
        if not battle.avatar_has_mecha(mecha_id):
            return
        global_data.emgr.hide_skill_detail_event.emit(['skill_detail', SkillDetailsUI])
        self.init_tech_list(mecha_id)
        self.panel.nd_change.nd_tech.setVisible(True)
        self.panel.PlayAnimation('show_tech')

    def update_btn_module(self, plan_idx):
        self.panel.nd_change.nd_btn.btn_module.lab_module.SetString(PLAN_NAME_TEXT_IDS[plan_idx])

    def update_btn_tech(self, page_idx):
        page_name = get_text_by_id(81789).format(page_idx + 1)
        self.panel.nd_change.nd_btn.btn_tech.lab_tech.SetString(page_name)

    def on_change_selected_mecha_btn(self, mecha_id):
        if not self.panel.nd_change:
            return
        else:
            own_mecha = global_data.battle and global_data.battle.avatar_has_mecha(mecha_id)
            self.panel.nd_btn.setVisible(own_mecha)
            if not own_mecha:
                return
            cur_module_plan_index = global_data.player.logic.ev_g_mecha_cur_module_plan_index(mecha_id)
            cur_tech_page_index = global_data.player.logic.ev_g_mecha_cur_page_index(mecha_id)
            if cur_tech_page_index is None or cur_module_plan_index is None:
                return
            self.update_btn_module(cur_module_plan_index)
            self.update_btn_tech(int(cur_tech_page_index))
            return

    def init_module_list(self, mecha_id):
        mecha_module_plans = global_data.player.get_mecha_all_module_plan(mecha_id)
        self.panel.nd_change.nd_module.list_module.DeleteAllSubItem()
        self.panel.nd_change.nd_module.list_module.SetInitCount(len(mecha_module_plans))
        cur_module_plan_index = global_data.player.logic.ev_g_mecha_cur_module_plan_index(mecha_id)
        for idx, module_plan in enumerate(mecha_module_plans):
            module_plan_node = self.panel.nd_change.nd_module.list_module.GetItem(idx)
            is_selected = cur_module_plan_index == idx
            if is_selected:
                self.select_module_plan_node = module_plan_node
            self.init_mecha_module_plan(idx, module_plan_node, module_plan, selected=is_selected)

            @module_plan_node.btn_choose.unique_callback()
            def OnClick(btn, touch, temp_node=module_plan_node, cur_mecha_id=mecha_id, plan_idx=idx):
                self.on_click_module_plan_btn(temp_node, cur_mecha_id, plan_idx)

    def init_tech_list(self, mecha_id):
        mecha_component_conf = global_data.player.get_mecha_all_component_conf(mecha_id)
        page_num = global_data.player.get_mecha_component_page_num(mecha_id)
        self.panel.nd_change.nd_tech.list_tech.DeleteAllSubItem()
        self.panel.nd_change.nd_tech.list_tech.SetInitCount(MAX_PAGE_NUM)
        cur_tech_page_index = global_data.player.logic.ev_g_mecha_cur_page_index(mecha_id)
        mecha_page_conf = global_data.player.get_mecha_component_page_conf(mecha_id)
        for page_idx in range(MAX_PAGE_NUM):
            component_conf = mecha_component_conf.get(str(page_idx))
            is_lock = not mecha_component_conf or not component_conf and page_num == 1 and page_idx != 0
            page_node = self.panel.nd_change.nd_tech.list_tech.GetItem(int(page_idx))
            is_selected = page_idx == int(cur_tech_page_index)
            if is_selected:
                self.select_component_page_node = page_node
                self.init_tech_desc(page_idx)
            if mecha_page_conf and isinstance(mecha_page_conf, list) and len(mecha_page_conf) == 3:
                custom_page_name = mecha_page_conf[-1].get(str(page_idx))
            else:
                custom_page_name = None
            self.init_mecha_tech_page(page_idx, page_node, component_conf, is_lock, custom_page_name, selected=is_selected)

            @page_node.btn_choose.unique_callback()
            def OnClick(btn, touch, page_idx=page_idx, temp_node=page_node, cur_mecha_id=mecha_id, locked=is_lock):
                self.on_click_component_page_btn(page_idx, temp_node, cur_mecha_id, locked)

        return

    def init_mecha_module_plan(self, plan_idx, temp_node, module_plan, selected=False):
        temp_node.nd_content.lab_title.SetString(PLAN_NAME_TEXT_IDS[plan_idx])
        sp_bar_item_node_names = [
         'bar_item_1', 'bar_item_2']
        sp_desc_node_names = ['up', 'down']
        for slot_no, card_ids in six.iteritems(module_plan):
            module_node_name = 'temp_module_%s' % slot_no
            module_node = getattr(temp_node, module_node_name)
            if slot_no == mecha_const.SP_MODULE_SLOT:
                for idx, card_id in enumerate(card_ids):
                    card_name, card_desc = mecha_module_utils.get_module_card_name_and_desc(card_id, BATTLE_MODULE_LEVEL)
                    card_pic = template_utils.get_talent_card_pic(card_id)
                    module_pic = mecha_module_utils.get_module_item_bar_pic(slot_no, BATTLE_MODULE_LEVEL, '')
                    bar_item_node = getattr(module_node, sp_bar_item_node_names[idx])
                    lab_name_node = getattr(module_node, 'lab_name_%s' % sp_desc_node_names[idx])
                    lab_details_node = getattr(module_node, 'lab_details_%s' % sp_desc_node_names[idx])
                    bar_item_node.bar_item.SetDisplayFrameByPath('', module_pic)
                    bar_item_node.img_skill.SetDisplayFrameByPath('', card_pic)
                    lab_name_node.SetString(card_name)
                    lab_details_node.SetString(card_desc)

            else:
                card_name, card_desc = mecha_module_utils.get_module_card_name_and_desc(card_ids[0], BATTLE_MODULE_LEVEL)
                card_pic = template_utils.get_module_slot_pic(card_ids[0], slot_no, BATTLE_MODULE_LEVEL)
                module_pic = mecha_module_utils.get_module_item_bar_pic(slot_no, BATTLE_MODULE_LEVEL, '')
                module_node.bar_item.bar_item.SetDisplayFrameByPath('', module_pic)
                module_node.bar_item.img_skill.SetDisplayFrameByPath('', card_pic)
                module_node.lab_name.SetString(card_name)
                module_node.lab_details1.SetString(card_desc)

        if selected:
            self.update_mecha_module_plan_bar(temp_node, True)

    def init_mecha_tech_page(self, page_idx, temp_node, component_conf, is_lock, custom_page_name, selected=False):
        temp_node.nd_content.setVisible(not is_lock)
        temp_node.nd_lock.setVisible(is_lock)
        self.update_mecha_tech_page(temp_node, selected)
        if not custom_page_name:
            page_name = get_text_by_id(81789).format(page_idx + 1)
        else:
            page_name = custom_page_name
        if is_lock:
            temp_node.nd_lock.lab_plan.SetString(page_name)
            return
        else:
            temp_node.nd_content.nd_item_name.lab_item_name.SetString(page_name)
            part_list = const.MECHA_COMPONENT_PART_LIST
            temp_node.list_item.SetInitCount(len(part_list))
            temp_node.list_item.setTouchEnabled(False)
            for idx, part_no in enumerate(part_list):
                unlock_slot_list = global_data.player.get_unlock_slot_idx(str(part_no))
                slot_index = idx % item_const.COMPONENT_SLOT_CNT_PER_PART
                com_node = temp_node.list_item.GetItem(idx)
                if not component_conf:
                    com_id = None
                elif str(part_no) not in six_ex.keys(component_conf):
                    com_id = None
                else:
                    com_id = component_conf[str(part_no)][0]
                com_type = part2type(int(part_no))
                is_slot_locked = slot_index not in unlock_slot_list
                inscription_utils.init_component_slot_temp(com_node.temp_item, com_id, is_lock=is_slot_locked, com_type=com_type)

            return

    def on_click_module_plan_btn(self, module_plan_node, mecha_id, plan_idx):
        if self.select_module_plan_node:
            self.update_mecha_module_plan_bar(self.select_module_plan_node, False)
        self.update_mecha_module_plan_bar(module_plan_node, True)
        self.select_module_plan_node = module_plan_node
        player = global_data.player
        if not player:
            return
        player.call_soul_method('change_mecha_module_plan', (mecha_id, plan_idx))
        self.update_btn_module(plan_idx)
        player.logic and player.logic.send_event('E_MECHA_CUR_MODULE_PLAN_INDEX', mecha_id, plan_idx)

    def on_click_component_page_btn(self, page_idx, page_node, mecha_id, is_lock):
        if is_lock:
            return
        if self.select_component_page_node:
            self.update_mecha_tech_page(self.select_component_page_node, False)
        self.update_mecha_tech_page(page_node, True)
        self.select_component_page_node = page_node
        player = global_data.player
        if not player:
            return
        player.call_soul_method('change_mecha_component_page', (str(mecha_id), str(page_idx)))
        self.update_btn_tech(page_idx)
        player.logic and player.logic.send_event('E_MECHA_CUR_PAGE_INDEX', str(mecha_id), str(page_idx))
        self.init_tech_desc(page_idx)

    def update_mecha_module_plan_bar(self, temp_node, selected):
        SHOW_SLOT_LIST = [
         mecha_const.MODULE_ATTACK_SLOT, mecha_const.MODULE_DEFEND_SLOT, mecha_const.MODULE_MOVE_SLOT, mecha_const.SP_MODULE_SLOT]
        for slot_no in SHOW_SLOT_LIST:
            module_node_name = 'temp_module_%s' % slot_no
            module_node = getattr(temp_node, module_node_name)
            if slot_no == mecha_const.SP_MODULE_SLOT:
                module_bar_pic = 'gui/ui_res_2/battle_mech/pnl_module_sp.png' if selected else 'gui/ui_res_2/battle_mech/pnl_module_sp_useless.png'
                module_node.bar.SetDisplayFrameByPath('', module_bar_pic)
            elif selected:
                module_bar_pic = 'gui/ui_res_2/battle_mech/pnl_module_normal.png' if 1 else 'gui/ui_res_2/battle_mech/pnl_module_normal_useless.png'
                module_node.bar.SetDisplayFrameByPath('', module_bar_pic)

        temp_node.btn_choose.SetSelect(selected)
        temp_node.nd_using.setVisible(selected)
        if selected:
            temp_node.nd_content.lab_title.SetColor('#SK')
        else:
            temp_node.nd_content.lab_title.SetColor('#SW')

    def update_mecha_tech_page(self, temp_node, selected):
        temp_node.btn_choose.SetSelect(selected)
        temp_node.nd_using.setVisible(selected)
        if selected:
            temp_node.nd_content.nd_item_name.lab_item_name.SetColor('#SK')
        else:
            temp_node.nd_content.nd_item_name.lab_item_name.SetColor('#SW')

    def init_tech_desc(self, page_idx):
        summon_ui = self.get_mecha_summon_ui()
        if not summon_ui:
            return
        mecha_id = summon_ui.get_select_mecha_id()
        if not mecha_id:
            return
        cur_page_item_id_list = inscription_utils.get_used_com_item_id_list(mecha_id, page_idx)
        page_attr_dict = inscription_utils.get_component_list_inscr_add_dict(cur_page_item_id_list)
        inscription_utils.set_ability_list(self.panel.nd_change.nd_tech.nd_tech_detail.list_num, self.panel.nd_change.nd_tech.nd_tech_detail.nd_empty, page_attr_dict)
        self.panel.nd_change.nd_tech.nd_tech_detail.setVisible(True)
        self.panel.nd_change.nd_tech.nd_tech_detail.lab_tech_name.SetString(81792)