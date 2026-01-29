# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaSkillInfoWidget.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.gutils.mecha_skill_utils import get_lobby_mecha_fuel_percent, get_lobby_mecha_hp_percent, get_lobby_mecha_shield_percent, get_mecha_weapon_speed_tag, get_mecha_weapon_damage_tag
from logic.gutils import mecha_skill_utils
import cc
ICON_PREFIX = 'gui/ui_res_2/battle/mech_main/'
MECHA_ABILITY_DESC_TEXT = {0: [
     80752, 607541],
   1: [
     12037, 607542],
   2: [
     607500, 607543],
   3: [
     607501, 607544],
   4: [
     607502, 607545],
   5: [
     607503, 607546]
   }

class MechaSkillInfoWidget(BaseUIWidget):

    def __init__(self, parent, panel, mecha_type):
        super(MechaSkillInfoWidget, self).__init__(parent, panel)
        self.init_param()
        self.init_ui_event()
        self.skill_detail_widget = MechaSkillDetailWidget(self.panel.temp_skill_desc)
        self.on_switch_to_mecha_type(mecha_type)

    def on_switch_to_mecha_type(self, mecha_type):
        self._cur_mecha_id = mecha_type
        self.update_all_ability_widgets()
        self.update_all_skill_nodes()
        self.hide_skill_desc_widget()
        self.hide_trait_desc_widget()

    def on_show_ability_desc_widget(self, index):
        title = get_text_by_id(MECHA_ABILITY_DESC_TEXT[index][0])
        desc = get_text_by_id(MECHA_ABILITY_DESC_TEXT[index][1])
        self.panel.temp_ability_desc.lab_title.SetString(title)
        self.panel.temp_ability_desc.lab_des.SetString(desc)
        self.panel.temp_ability_desc.setVisible(True)
        cur_x, cur_y = self.panel.temp_ability_desc.GetPosition()
        to_x, to_y = self._ability_node_list[index].GetPosition()
        cur_ability_node = self._ability_node_list[index]
        _, d_y = cur_ability_node.GetContentSize()
        self.panel.temp_ability_desc.SetPosition(cur_x, to_y + d_y / 2.0)

    def on_show_skill_desc_widget(self, cur_node):
        index = self._skill_node_lst.index(cur_node)
        for node in self._skill_node_lst:
            node.img_choose.setVisible(False)

        cur_node.img_choose.setVisible(True)
        show_skill_list = self._get_show_skill_list()
        skill_id = show_skill_list[index]
        skill_conf = self._skill_conf.get(str(skill_id))
        self.panel.temp_skill_desc.setVisible(True)
        self.panel.nd_touch.setVisible(True)
        self.skill_detail_widget.init_widget(skill_conf)

    def hide_skill_desc_widget(self):
        self.panel.nd_touch.setVisible(False)
        self.panel.temp_skill_desc.setVisible(False)

    def hide_trait_desc_widget(self):
        self.panel.nd_touch.setVisible(False)
        self.panel.img_desc_trait.setVisible(False)

    def init_bkg_click(self):

        @self.panel.nd_touch.unique_callback()
        def OnClick(*args):
            self.panel.temp_skill_desc.setVisible(False)
            self.panel.img_desc_trait.setVisible(False)
            self.panel.nd_touch.setVisible(False)

    def init_trait_touch(self):
        for btn_trait in self._trait_node_list:

            @btn_trait.unique_callback()
            def OnClick(*args):
                self.hide_skill_desc_widget()
                self.panel.nd_touch.setVisible(True)
                self.panel.img_desc_trait.setVisible(True)

    def init_ability_touch(self):
        for node in self._ability_node_list:

            @node.btn_des.unique_callback()
            def OnBegin(btn, touch):
                self.hide_skill_desc_widget()
                self.hide_trait_desc_widget()
                nd_parent = btn.GetParent()
                self.on_show_ability_desc_widget(self._ability_node_list.index(nd_parent))

            @node.btn_des.unique_callback()
            def OnEnd(*args):
                self.panel.temp_ability_desc.setVisible(False)

    def init_skill_click(self):
        for node in self._skill_node_lst:

            @node.unique_callback()
            def OnClick(nd, touch):
                self.hide_trait_desc_widget()
                self.hide_skill_desc_widget()
                self.on_show_skill_desc_widget(nd)

    def update_all_ability_widgets(self):
        hangar_config = self._mecha_conf[str(self._cur_mecha_id)]
        basic_config = self._mecha_info_conf[str(self._cur_mecha_id)]
        fuel_config = self._mecha_fuel_conf[str(self._cur_mecha_id)]
        shield_config = self._mecha_shield_conf[str(self._cur_mecha_id)]
        trait_list = hangar_config.get('desc_trait', [])
        for btn_trait in self._trait_node_list:
            btn_trait.setVisible(False)

        for index, trait in enumerate(trait_list):
            btn_trait = self._trait_node_list[index]
            tag_info = self.tag_conf.get(trait, {})
            tag_icon_path_list = tag_info.get('tag_icon_path')
            btn_trait.SetFrames('', [tag_icon_path_list[0], tag_icon_path_list[0]], False, None)
            btn_trait.setVisible(True)

        spec_list = hangar_config.get('desc_speciality', [])
        self.panel.nd_speciality.img_speciality_1.setVisible(False)
        self.panel.nd_speciality.img_speciality_2.setVisible(False)
        for index, spec in enumerate(spec_list):
            img_spec = getattr(self.panel.nd_speciality, 'img_speciality_%s' % (index + 1))
            lab_spec = getattr(img_spec, 'lab_speciality_%s' % (index + 1))
            spec_param = self._mecha_desc_conf.get(spec, {})
            img_spec.SetDisplayFrameByPath('', spec_param.get('tag_icon_path', '')[0])
            lab_spec.SetString(get_text_by_id(spec_param.get('tag_name_text_id')))
            img_spec.setVisible(True)

        range_list = hangar_config.get('desc_range', [])
        move_list = hangar_config.get('desc_move', [])
        desc_list = [range_list, move_list]
        for index in range(1, 3):
            node = self._ability_node_list[index]
            desc = desc_list[index - 1]
            desc_param = self._mecha_desc_conf.get(desc[0], {})
            node.lab_level.SetString(get_text_by_id(desc_param.get('tag_name_text_id')))
            node.nd_location.SetPosition(desc_param.get('tag_val'), '50%0')

        val_list = [
         get_lobby_mecha_hp_percent(self._cur_mecha_id), get_lobby_mecha_shield_percent(self._cur_mecha_id), get_lobby_mecha_fuel_percent(self._cur_mecha_id)]
        real_val_list = [basic_config.get('health', 0), int(shield_config.get('max_shield', 0)), int(fuel_config.get('max_fuel', 0))]
        for index in range(3, 6):
            node = self._ability_node_list[index]
            node.lab_num.SetString(str(real_val_list[index - 3]))
            node.prog_mech_ability.SetPercentage(val_list[index - 3])

        return

    def update_all_skill_nodes(self):
        show_skill_list = self._get_show_skill_list()
        for idx, skill_node in enumerate(self._skill_node_lst):
            skill_node.img_choose.setVisible(False)
            if idx >= len(show_skill_list):
                skill_node.setVisible(False)
                continue
            skill_id = show_skill_list[idx]
            skill_icon = ICON_PREFIX + self._skill_conf.get(str(skill_id)).get('icon_path') + '.png'
            skill_node.img_skill.SetDisplayFrameByPath('', skill_icon)
            skill_node.setVisible(True)

    def init_param(self):
        self._mecha_info_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
        self._mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self._skill_conf = confmgr.get('mecha_display', 'HangarConfig_Skills', 'Content')
        self._skill_node_lst = [ getattr(self.panel, 'nd_skill_%s' % x) for x in range(1, 6) ]
        self._ability_node_list = [self.panel.nd_speciality, self.panel.temp_1, self.panel.temp_2, self.panel.temp_3, self.panel.temp_4, self.panel.temp_5]
        self._trait_node_list = [self.panel.btn_trait_1, self.panel.btn_trait_2]
        self._cur_mecha_id = None
        self._mecha_desc_conf = confmgr.get('mecha_display', 'HangarDescConf', 'Content')
        self._mecha_fuel_conf = confmgr.get('mecha_conf', 'FuelConfig', 'Content')
        self._mecha_shield_conf = confmgr.get('mecha_conf', 'ShieldConfig', 'Content')
        self.tag_conf = confmgr.get('mecha_display', 'HangarDescConf', 'Content')
        return

    def init_ui_event(self):
        self.init_ability_touch()
        self.init_trait_touch()
        self.init_skill_click()
        self.init_bkg_click()

    def _get_show_skill_list(self):
        mecha_skill_lst = self._mecha_conf[str(self._cur_mecha_id)].get('mecha_skill_list')
        show_skill_list = [ x for x in mecha_skill_lst ]
        mecha_sp_skill_lst = self._mecha_conf[str(self._cur_mecha_id)].get('mecha_sp_skill_list', [])
        if mecha_sp_skill_lst:
            show_skill_list.extend(mecha_sp_skill_lst)
        return show_skill_list


class MechaSkillDetailWidget(object):

    def __init__(self, ui_panel):
        self.panel = ui_panel
        self.title_item = self.panel.temp_skill_desc
        init_w, init_h = self.title_item.GetContentSize()
        self.init_w = init_w
        self.list_tab_dict = {2: self.panel.nd_special.list_tab_2,3: self.panel.nd_special.list_tab_3}
        self.weapon_conf = confmgr.get('firearm_config')
        self.tag_conf = confmgr.get('mecha_display', 'HangarDescConf', 'Content')
        self.skill_attr_conf = confmgr.get('mecha_display', 'HangarSkillShowAttr', 'Content')
        self.cur_show_tag = None
        return

    def destroy(self):
        pass

    def init_widget(self, skill_info):
        self.skill_name_list = skill_info.get('extra_name_text_id_list', [])
        self.tab_name_list = skill_info.get('extra_tab_text_id_list', self.skill_name_list)
        self.skill_desc_brief = skill_info.get('desc_text_brief', '')
        self.skill_desc_list = skill_info.get('extra_desc_text_id_list', [])
        self.weapon_list = skill_info.get('weapon_id_list', [])
        self.real_skill_id = skill_info.get('real_skill_id')
        self.show_skill_attr = skill_info.get('skill_show_attr', [])
        self.bond_gift_text_id = skill_info.get('bond_gift_text_id', '')
        self.is_special = len(self.weapon_list) >= 2
        self.panel.nd_common.setVisible(not self.is_special)
        self.panel.nd_special.setVisible(self.is_special)
        show_node = self.panel.nd_special.list_content_2 if self.is_special else self.panel.nd_common.list_content_1
        self.show_node = show_node
        weapon_cnt = len(self.weapon_list)
        list_tab = self.list_tab_dict.get(weapon_cnt)
        if list_tab:
            list_tab.DeleteAllSubItem()
            list_tab.SetInitCount(weapon_cnt)
            for wp_cnt, tab_item in six.iteritems(self.list_tab_dict):
                tab_item.setVisible(wp_cnt == weapon_cnt)

        else:
            for _, tab_item in six.iteritems(self.list_tab_dict):
                tab_item.setVisible(False)

        self.init_tab_list(list_tab)

    def init_title_item(self, skill_index=0):
        if skill_index < 0 or skill_index >= len(self.skill_name_list):
            skill_index = 0
        self.title_item.lab_action_name.SetString(get_text_by_id(self.skill_name_list[skill_index]))
        self.title_item.lab_skill_kind.SetString(get_text_by_id(self.skill_desc_brief))
        is_weapon_skill = False
        if self.weapon_list and isinstance(self.weapon_list, list):
            if len(self.weapon_list) > skill_index:
                is_weapon_skill = self.weapon_list[skill_index] > 0
        if not is_weapon_skill:
            self.title_item.btn_tag_1.setVisible(False)
            self.title_item.btn_tag_2.setVisible(False)
            self.show_node.SetPosition('50%', '50%145')
            return
        else:
            self.title_item.btn_tag_1.setVisible(True)
            self.title_item.btn_tag_2.setVisible(True)
            self.show_node.SetPosition('50%', '50%95')
            weapon_id = self.weapon_list[skill_index]
            speed_tag = get_mecha_weapon_speed_tag(weapon_id)
            speed_tag_info = self.tag_conf.get(speed_tag, {})
            speed_tag_name = get_text_by_id(speed_tag_info.get('tag_name_text_id'))
            speed_tag_icon = speed_tag_info.get('tag_icon_path')
            self.title_item.btn_tag_1.lab_tag_1.SetString(speed_tag_name)
            self.title_item.btn_tag_1.SetFrames('', [speed_tag_icon[0], speed_tag_icon[0]], False, None)
            dmg_tag = get_mecha_weapon_damage_tag(weapon_id)
            if dmg_tag is not None:
                dmg_tag_info = self.tag_conf.get(dmg_tag, {})
                dmg_tag_name = get_text_by_id(dmg_tag_info.get('tag_name_text_id'))
                dmg_tag_icon = dmg_tag_info.get('tag_icon_path')
                self.title_item.btn_tag_2.lab_tag_2.SetString(dmg_tag_name)
                self.title_item.btn_tag_2.SetFrames('', [dmg_tag_icon[0], dmg_tag_icon[0]], False, None)
                self.title_item.btn_tag_2.setVisible(True)
            else:
                self.title_item.btn_tag_2.setVisible(False)

            @self.title_item.btn_tag_1.unique_callback()
            def OnClick(btn, touch):
                self.on_click_tag(speed_tag, 0)

            @self.title_item.btn_tag_2.unique_callback()
            def OnClick(btn, touch):
                self.on_click_tag(dmg_tag, 1)

            return

    def init_detail_item(self, skill_index=0):
        if skill_index < 0 or skill_index >= len(self.skill_desc_list):
            skill_index = 0
        detail_item = self.add_detail_item()
        detail_item.lab_description.SetString(get_text_by_id(self.skill_desc_list[skill_index]))
        if len(self.show_skill_attr) <= 0 or skill_index >= len(self.show_skill_attr):
            detail_item.list_data.setVisible(False)
            return
        cur_skill_attr_list = self.show_skill_attr[skill_index]
        detail_item.list_data.DeleteAllSubItem()
        detail_item.list_data.SetInitCount(len(cur_skill_attr_list))
        for idx, skill_attr in enumerate(cur_skill_attr_list):
            skill_attr_id = six_ex.keys(skill_attr)[0]
            skill_attr_param = six_ex.values(skill_attr)[0]
            skill_attr_info = self.skill_attr_conf.get(skill_attr_id, {})
            attr_name = get_text_by_id(skill_attr_info.get('attr_name_text_id'))
            attr_handler_name = skill_attr_info.get('attr_handler')
            attr_handler = getattr(mecha_skill_utils, attr_handler_name)
            attr_content = attr_handler(skill_attr_param)
            attr_item = detail_item.list_data.GetItem(idx)
            attr_item.lab_title.SetString(attr_name)
            attr_item.lab_data.SetString(str(attr_content))

        if self.bond_gift_text_id:
            detail_item.list_data.nd_auto_fit.setVisible(True)
            detail_item.list_data.nd_auto_fit.lab_description_01.SetString(get_text_by_id(self.bond_gift_text_id))
        else:
            detail_item.list_data.nd_auto_fit.setVisible(False)

    def add_detail_item(self):
        self.show_node.DeleteAllSubItem()
        self.show_node.SetInitCount(0)
        detail_temp = global_data.uisystem.load_template('mech_display/i_skill_desc_list_item_2')
        self.show_node.AddItem(detail_temp, bRefresh=True)
        return self.show_node.GetItem(0)

    def init_tab_list(self, list_tab):
        if list_tab and self.is_special:
            all_tabs = list_tab.GetAllItem()
            for idx, tab in enumerate(all_tabs):
                tab.btn_tab.SetText(get_text_by_id(self.tab_name_list[idx]))

                @tab.btn_tab.unique_callback()
                def OnClick(btn, touch):
                    nd_parent = btn.GetParent()
                    self.on_click_tab(all_tabs, index=list_tab.getIndexByItem(nd_parent))

            self.on_click_tab(all_tabs)
        else:
            self.on_click_tab()

    def update_tab_list_status(self, tab_list, select_idx):
        if tab_list is None:
            return
        else:
            for idx, tab in enumerate(tab_list):
                tab.btn_tab.SetSelect(idx == select_idx)

            return

    def on_click_tab(self, all_tabs=None, index=0):
        self.update_tab_list_status(all_tabs, index)
        self.cur_show_tag = None
        self.init_title_item(skill_index=index)
        self.init_detail_item(skill_index=index)
        return

    def hide_tag_desc(self):
        self.cur_show_tag = None
        return

    def on_click_tag(self, tag_id, tag_pos):
        if tag_id is None:
            return
        else:
            if self.cur_show_tag == tag_id:
                self.cur_show_tag = None
                self.show_node.DeleteItemIndex(0, bRefresh=True)
                return
            tag_info = self.tag_conf.get(tag_id, {})
            tag_type_name = get_text_by_id(tag_info.get('tag_type_name_text_id'))
            tag_type_desc = get_text_by_id(tag_info.get('tag_type_explain_text_id'))
            if self.cur_show_tag is None:
                tag_desc_temp = global_data.uisystem.load_template('mech_display/i_skill_desc_list_item_3')
                self.show_node.AddItem(tag_desc_temp, 0, bRefresh=True)
            tag_desc_item = self.show_node.GetItem(0)
            tag_desc_item.lab_title.SetString(tag_type_name)
            tag_desc_item.lab_des.SetString(tag_type_desc)
            tag_desc_item.img_des_1.setVisible(tag_pos == 0)
            tag_desc_item.img_des_2.setVisible(tag_pos == 1)
            h_title = tag_desc_item.lab_title.getVirtualRendererSize().height
            h_des = tag_desc_item.lab_des.getVirtualRendererSize().height
            item_w, _ = tag_desc_item.GetContentSize()
            tag_desc_item.SetContentSize(item_w, h_title + h_des + 25)
            tag_desc_item.ChildResizeAndPosition()
            self.show_node._container._refreshItemPos()
            self.show_node._refreshItemPos()
            self.show_node.ScrollToTop()
            self.cur_show_tag = tag_id
            return