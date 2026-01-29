# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEMechaInfoWidget.py
from __future__ import absolute_import
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gutils.skin_define_utils import get_main_skin_id
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import mecha_skill_utils
from logic.comsys.mecha_display.MechaSkillInfoWidget import MechaSkillDetailWidget
from common.cfg import confmgr
import six
import six_ex
import math
ICON_PREFIX = 'gui/ui_res_2/battle/mech_main/'
PRIORITY_ICON_PATH = 'gui/ui_res_2/pve/mecha/icon_pve_mecha_info_{}.png'
HIGH_PRIORITY_INFO = {'hp': {'title': 409,'icon': 'durability','up_name': 'up_hp','max_name': 'max_hp','pet_add_name': 'hp_power'},'shield': {'title': 410,'icon': 'shield','up_name': 'up_shield','max_name': 'max_shield','pet_add_name': 'shd_power'},'atk': {'title': 408,'icon': 'atk','up_name': 'up_atk','max_name': 'max_atk','pet_add_name': 'atk_power'},'speed': {'title': 415,'icon': 'speed','up_name': '','max_name': 'max_speed','pet_add_name': 'spd_power'}}
NORMAL_PRIORITY_INFO = {'crit_rate': {'title': 411,'icon': 'critrate','is_percent': True,'is_decimals': False,'pet_add_name': 'crit_power'},'ex_crit_damage': {'title': 412,'icon': 'critdmg','is_percent': True,'is_decimals': False,'pet_add_name': 'ex_crit_power'},'fuel': {'title': 413,'icon': 'fuel','is_percent': False,'is_decimals': False,'pet_add_name': 'fuel_power'},'fuel_reg_speed': {'title': 414,'icon': 'recover','is_percent': False,'is_decimals': True,'pet_add_name': 'fuel_reg_power'}}

class PVEMechaInfoWidget(object):

    def __init__(self, parent, panel):
        self._parent = parent
        self._panel = panel
        self.init_params()
        self.init_ui()
        self.init_ui_event()
        self.process_events(True)

    def init_params(self):
        self._conf = None
        self._mecha_id = None
        self._mecha_info_conf = confmgr.get('mecha_init_data', default={})
        self._skill_conf = confmgr.get('mecha_display', 'HangarConfig_Skills', 'Content')
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self._pet_dict = global_data.player.get_pve_pet_dict() if global_data.player else {0: 0,1: 0,2: 0}
        return

    def init_ui(self):
        self._skill_node_lst = [ getattr(self._panel.nd_skill, 'nd_skill_%s' % x) for x in range(1, 5) ]
        self.skill_detail_widget = PVEMechaSkillDetailWidget(self._panel.temp_skill_desc)
        self._panel.nd_touch.setVisible(False)
        mecha_id, _ = self._parent.get_current_id()
        self._update_mecha_info(mecha_id)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_pve_mecha_show_changed': self._update_mecha_info,
           'on_pve_mecha_upgrade': self._update_mecha_info
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_ui_event(self):
        for node in self._skill_node_lst:

            @node.unique_callback()
            def OnClick(nd, touch):
                self.hide_skill_desc_widget()
                self.on_show_skill_desc_widget(nd)

        @self._panel.nd_touch.unique_callback()
        def OnClick(*args):
            self._panel.temp_skill_desc.setVisible(False)
            self._panel.nd_touch.setVisible(False)

        @self._parent.panel.btn_pet.unique_callback()
        def OnClick(*args):
            self._parent.panel.nd_mecha_add_attr.setVisible(True)

        @self._parent.panel.nd_mecha_add_attr.btn_close.unique_callback()
        def OnClick(*args):
            self._parent.panel.nd_mecha_add_attr.setVisible(False)

        @self._parent.panel.nd_mecha_add_attr.btn_describe.unique_callback()
        def OnClick(*args):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(860428, 860429)

    def _update_mecha_info(self, mecha_id):
        self._mecha_id = mecha_id
        self._mecha_level = global_data.player.get_mecha_level_by_id(self._mecha_id)
        self._conf = self._mecha_info_conf.get(str(self._mecha_id))
        self._update_add_attr_info()
        self._update_high_priority_info()
        self._update_normal_priority_info()
        self._update_list_skill()

    def _update_add_attr_info(self):
        self._add_attr_dict = {}
        effect_list = global_data.player.get_mecha_effect(self._mecha_id, self._mecha_level)
        for effect_id in effect_list:
            show_attr = confmgr.get('mecha_upgrade_effect_data', str(effect_id), 'show_attr')
            if show_attr:
                add_attr_handler_name = six_ex.keys(show_attr[0])[0]
                if not self._add_attr_dict.get(add_attr_handler_name):
                    self._add_attr_dict[add_attr_handler_name] = {}
                self._add_attr_dict[add_attr_handler_name] = six_ex.values(show_attr[0])[0]

    def _update_high_priority_info(self):
        list_info = self._panel.list_info_2
        list_info.DeleteAllSubItem()
        add_list_info = self._parent.panel.nd_mecha_add_attr.list_data.GetItem(0).list_info
        idx = 0
        for priority_name, info in six_ex.items(HIGH_PRIORITY_INFO):
            item = list_info.AddTemplateItem()
            add_attr_item = add_list_info.GetItem(idx)
            title = get_text_by_id(info.get('title'))
            item.lab_title.SetString(title)
            add_attr_item.lab_title.SetString(title)
            icon = PRIORITY_ICON_PATH.format(info.get('icon'))
            item.icon.SetDisplayFrameByPath('', icon)
            add_attr_item.icon.SetDisplayFrameByPath('', icon)
            lab_data = item.lab_data
            init_num = int(self._conf.get(priority_name))
            add_num = self._conf.get(info.get('up_name'), 0) * self._mecha_level
            skill_add_num = self.get_skill_add_attr(priority_name, init_num)
            pet_add_num = 0
            for pet_id in six_ex.values(self._pet_dict):
                pet_add_num += confmgr.get('c_pet_info', str(pet_id), 'add_attr', info.get('pet_add_name'), default=0)

            total_add_num = add_num + skill_add_num + pet_add_num
            total_num = init_num + total_add_num
            lab_data.SetString(str(total_num))
            add_attr_item.lab_data.SetString('+{}'.format(pet_add_num))
            color = 55551 if total_add_num > 0 else 14018047
            lab_data.SetColor(color)
            if pet_add_num > 0:
                color = 55551 if 1 else 14018047
                add_attr_item.lab_data.SetColor(color)
                bar_prog = item.bar_prog
                max_num = self._conf.get(info.get('max_name'))
                bar_prog.prog_add.SetPercentage(float(init_num + total_add_num) / max_num * 100)
                bar_prog.prog_normal.SetPercentage(float(init_num) / max_num * 100)
                idx += 1

    def _update_normal_priority_info(self):
        list_info = self._panel.list_info
        list_info.DeleteAllSubItem()
        add_list_info = self._parent.panel.nd_mecha_add_attr.list_data.GetItem(0).list_info
        idx = 0
        for priority_name, info in six_ex.items(NORMAL_PRIORITY_INFO):
            item = list_info.AddTemplateItem()
            add_attr_item = add_list_info.GetItem(idx + 4)
            title = get_text_by_id(info.get('title'))
            item.lab_title.SetString(title)
            add_attr_item.lab_title.SetString(title)
            icon = PRIORITY_ICON_PATH.format(info.get('icon'))
            item.icon.SetDisplayFrameByPath('', icon)
            add_attr_item.icon.SetDisplayFrameByPath('', icon)
            lab_data = item.lab_data
            init_num = self._conf.get(priority_name)
            skill_attr = self.get_skill_add_attr(priority_name, init_num)
            pet_add_num = 0
            for pet_id in six_ex.values(self._pet_dict):
                pet_add_num += confmgr.get('c_pet_info', str(pet_id), 'add_attr', info.get('pet_add_name'), default=0)

            total_add_num = skill_attr + pet_add_num
            total_num = init_num + total_add_num
            is_percent = info.get('is_percent')
            if is_percent:
                lab_data.SetString('{}%'.format(int(total_num * 100)))
                add_attr_item.lab_data.SetString('+{}%'.format(int(total_add_num * 100)))
            elif info.get('is_decimals'):
                lab_data.SetString('%.1f' % total_num)
                add_attr_item.lab_data.SetString('+%.1f' % pet_add_num)
            else:
                lab_data.SetString(str(int(total_num)))
                add_attr_item.lab_data.SetString(str(int(pet_add_num)))
            color = 55551 if total_add_num > 0 else 14018047
            lab_data.SetColor(color)
            if pet_add_num > 0:
                color = 55551 if 1 else 14018047
                add_attr_item.lab_data.SetColor(color)
                idx += 1

    def get_skill_add_attr(self, priority_name, init_num):
        for add_attr_handler_name, add_attr_param in six_ex.items(self._add_attr_dict):
            if add_attr_handler_name == priority_name:
                if priority_name == 'speed':
                    percent = float(add_attr_param[0]) / 100
                    return math.ceil(init_num * percent)
                else:
                    return add_attr_param[0]

        return 0

    def _update_list_skill(self):
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

    def _get_show_skill_list(self):
        mecha_skill_lst = self._mecha_conf[str(self._mecha_id)].get('mecha_skill_list')
        show_skill_list = [ x for x in mecha_skill_lst ]
        mecha_sp_skill_lst = self._mecha_conf[str(self._mecha_id)].get('mecha_sp_skill_list', [])
        if mecha_sp_skill_lst:
            show_skill_list.extend(mecha_sp_skill_lst)
        return show_skill_list

    def hide_skill_desc_widget(self):
        self._panel.nd_touch.setVisible(False)
        self._panel.temp_skill_desc.setVisible(False)

    def on_show_skill_desc_widget(self, cur_node):
        index = self._skill_node_lst.index(cur_node)
        for node in self._skill_node_lst:
            node.img_choose.setVisible(False)

        cur_node.img_choose.setVisible(True)
        show_skill_list = self._get_show_skill_list()
        skill_id = show_skill_list[index]
        skill_conf = self._skill_conf.get(str(skill_id))
        temp_skill_desc = self._panel.temp_skill_desc
        temp_skill_desc.setVisible(True)
        z_order = temp_skill_desc.getLocalZOrder() - 1
        nd_touch = self._panel.nd_touch
        nd_touch.setVisible(True)
        nd_touch.setLocalZOrder(z_order)
        self.skill_detail_widget.init_widget(skill_conf, self._add_attr_dict)

    def destroy(self):
        self.process_events(False)
        self._mecha_id = None
        self._mecha_level = None
        self._conf = None
        self._add_attr_dict = None
        if self.skill_detail_widget:
            self.skill_detail_widget.destroy()
            self.skill_detail_widget = None
        return


class PVEMechaSkillDetailWidget(MechaSkillDetailWidget):

    def init_widget(self, skill_info, add_attr_dict=None):
        self.skill_name_list = skill_info.get('extra_name_text_id_list', [])
        self.tab_name_list = skill_info.get('extra_tab_text_id_list', self.skill_name_list)
        self.skill_desc_brief = skill_info.get('desc_text_brief', '')
        pve_extra_desc_text_id_list = skill_info.get('pve_extra_desc_text_id_list', [])
        self.skill_desc_list = pve_extra_desc_text_id_list if pve_extra_desc_text_id_list else skill_info.get('extra_desc_text_id_list', [])
        self.weapon_list = skill_info.get('weapon_id_list', [])
        self.real_skill_id = skill_info.get('real_skill_id')
        pve_skill_show_attr = skill_info.get('pve_skill_show_attr', [])
        self.show_skill_attr = pve_skill_show_attr if pve_skill_show_attr else skill_info.get('skill_show_attr', [])
        self.bond_gift_text_id = skill_info.get('bond_gift_text_id', '')
        self.add_attr_dict = add_attr_dict
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
            add_attr_str = self.get_add_attr_str(skill_attr_id, skill_attr_param, attr_content)
            attr_item.lab_data.SetString(add_attr_str)

        if self.bond_gift_text_id:
            detail_item.list_data.nd_auto_fit.setVisible(True)
            detail_item.list_data.nd_auto_fit.lab_description_01.SetString(get_text_by_id(self.bond_gift_text_id))
        else:
            detail_item.list_data.nd_auto_fit.setVisible(False)

    def get_add_attr_str(self, attr_handler_name, skill_attr_param, attr_content):
        add_attr = 0
        for add_attr_handler_name, add_attr_param in six_ex.items(self.add_attr_dict):
            skill_add_attr_param = add_attr_param[0]
            if add_attr_handler_name == attr_handler_name and skill_add_attr_param == skill_attr_param:
                add_attr = add_attr_param[1]
                break

        if add_attr:
            if add_attr_handler_name == 'pve_clip_size':
                return str(attr_content + add_attr)
            if add_attr_handler_name == 'pve_cd_time':
                attr_content = float(attr_content)
                percent = float(100 - add_attr) / 100
                return str('%.1f' % (attr_content * percent)) + get_text_by_id(18534)
        return str(attr_content)