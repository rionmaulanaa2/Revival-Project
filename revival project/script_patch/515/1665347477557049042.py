# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEMechaUpgradeWidget.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gutils.skin_define_utils import get_main_skin_id
from logic.gutils.pve_utils import get_attr_desc_text
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.item_utils import get_lobby_item_name, payment_item_pic
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gcommon.common_utils.text_utils import get_color_str
from common.utilities import get_rome_num
from common.utils.cocos_utils import ccp
from common.cfg import confmgr
import six_ex
NORMAL_TEMPLATE_PATH = 'pve/mecha/i_pve_mecha_btn_skill'
CURRENT_TEMPLATE_PATH = 'pve/mecha/i_pve_mecha_btn_skill2'
CAN_UPGRADE_COLOR = '0x04FA55FF'
CANT_UPGRADE_COLOR = '0xFF0000FF'

class PVEMechaUpgradeWidget(object):

    def __init__(self, parent, panel):
        self._parent = parent
        self._panel = panel
        self.init_params()
        self.init_ui()
        self.init_ui_event()
        self.process_events(True)

    def init_params(self):
        self._cur_add_level = None
        self._cur_select_effect = None
        self._conf = confmgr.get('mecha_upgrade_effect_data', default={})
        self._level_2_item = {}
        return

    def init_ui(self):
        self._nd_visible = self._panel.nd_visible
        self._mecha_id = None
        mecha_id, _ = self._parent.get_current_id()
        self._update_mecha_info(mecha_id)
        return

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_pve_mecha_show_changed': self._update_mecha_info,
           'on_pve_mecha_upgrade': self._update_mecha_info,
           'player_item_update_event': self._update_cost
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_ui_event(self):

        @self._nd_visible.btn_minus.callback()
        def OnClick(btn, touch):
            if self._cur_add_level == 1:
                return
            self._cur_add_level -= 1
            self._update_cost()

        @self._panel.btn_upgrade.callback()
        def OnClick(btn, touch):
            if self._cur_add_level == 0:
                return
            cost_list = global_data.player.get_upgrade_mecha_cost_list(self._mecha_id, self._cur_add_level)
            ex_cost_item_no, ex_cost_item_count = cost_list.get('ex_cost')
            ex_item_count = global_data.player.get_item_num_by_no(int(ex_cost_item_no))
            if ex_item_count < ex_cost_item_count:
                global_data.game_mgr.show_tip(get_text_by_id(426))
                return
            common_cost_item_no, common_cost_item_count = cost_list.get('common_cost')
            common_item_count = global_data.player.get_item_num_by_no(int(common_cost_item_no))
            if common_item_count < common_cost_item_count:
                global_data.game_mgr.show_tip(get_text_by_id(425))
                return
            global_data.player.do_pve_mecha_upgrade(self._mecha_id, self._cur_add_level)

        @self._nd_visible.btn_add.callback()
        def OnClick(btn, touch):
            if self._mecha_level + self._cur_add_level == len(self._effect_list):
                return
            self._cur_add_level += 1
            self._update_cost()

        @self._nd_visible.btn_max.callback()
        def OnClick(btn, touch):
            self._cur_add_level = global_data.player.get_max_upgrade_mecha_level(self._mecha_id)
            if self._cur_add_level == 0:
                self._cur_add_level = 1
            self._update_cost()

    def _update_mecha_info(self, mecha_id):
        self._mecha_id = mecha_id
        self._mecha_level = global_data.player.get_mecha_level_by_id(self._mecha_id)
        self._effect_list = global_data.player.get_mecha_all_effect(self._mecha_id)
        self._init_level = self._get_init_level()
        self._cur_add_level = 1
        self._update_nd_skill()
        self._update_effect_desc(self._init_level)
        self._update_cost()

    def _get_init_level(self):
        if self._mecha_level == len(self._effect_list):
            return len(self._effect_list)
        else:
            return self._mecha_level + 1

    def _update_nd_skill(self):
        list_skill = self._panel.list_skill
        list_skill.DeleteAllSubItem()
        for level, effect_info in six_ex.items(self._effect_list):
            if level == self._mecha_level + 1:
                template_conf = global_data.uisystem.load_template(CURRENT_TEMPLATE_PATH)
            else:
                template_conf = global_data.uisystem.load_template(NORMAL_TEMPLATE_PATH)
            effect_item = list_skill.AddItem(template_conf)
            self._level_2_item[level] = effect_item
            lab_unlock_level = effect_item.lab_unlock_level
            lab_unlock_level.SetString('Lv.{}'.format(level))
            bar_prog = effect_item.bar_prog
            is_unlock = self._mecha_level >= level
            if level == len(self._effect_list):
                bar_prog.setVisible(False)
            else:
                bar_prog.prog.SetPercent(100 if is_unlock else 0)
                bar_prog.setVisible(True)
            effect_item.nd_lock.setVisible(self._mecha_level < level)
            effect_item.nd_got.setVisible(is_unlock)
            effect_item.lab_skill_level.setString(get_rome_num(effect_info['effect_level']))
            conf = self._conf.get(str(effect_info['effect_id']))
            effect_item.icon_skill.SetDisplayFrameByPath('', conf.get('icon'))
            btn_choose = effect_item.btn_choose
            btn_choose.EnableCustomState(True)
            if level == self._init_level:
                self._cur_select_effect = btn_choose
                self._cur_select_effect.SetSelect(True)

            @btn_choose.callback()
            def OnClick(btn, touch, level=level):
                self._update_effect_desc(level)
                self._cur_add_level = level - self._mecha_level
                self._update_cost()
                self._update_select_state()

        old_inner_size = list_skill.GetInnerContentSize()
        list_skill.SetInnerContentSize(old_inner_size.width - 40, old_inner_size.height)
        init_item = list_skill.GetItem(self._init_level - 1)
        if init_item:
            w, h = init_item.GetContentSize()
            world_pos = init_item.convertToWorldSpace(ccp(w / 2 + 35, h / 2))
            scroll_pos = list_skill.GetInnerContainer().convertToNodeSpace(world_pos)
            list_skill.CenterWithPos(scroll_pos.x, scroll_pos.y)

    def _update_effect_desc(self, level):
        if not level:
            level = 1
        effect_info = self._effect_list.get(level)
        conf = self._conf.get(str(effect_info['effect_id']))
        title_str = get_text_by_id(conf.get('name_id')) + '(Lv.{})'.format(level)
        self._panel.lab_title.setString(title_str)
        attr_str = get_attr_desc_text(conf.get('desc_id'), conf.get('desc_params'))
        self._panel.lab_describe.setString(attr_str)

    def _update_cost(self):
        btn_upgrade = self._panel.btn_upgrade
        if self._mecha_level == len(self._effect_list):
            self._nd_visible.setVisible(False)
            btn_upgrade.SetEnable(False)
            btn_upgrade.SetText(get_text_by_id(81812))
            return
        if self._cur_add_level <= 0:
            self._nd_visible.setVisible(False)
            btn_upgrade.SetEnable(False)
            btn_upgrade.SetText(get_text_by_id(440))
            return
        self._nd_visible.setVisible(True)
        btn_upgrade.SetEnable(True)
        if self._cur_add_level == 1:
            btn_upgrade.SetText(get_text_by_id(423))
        else:
            btn_upgrade.SetText(get_text_by_id(441).format(self._cur_add_level + self._mecha_level))
        cost_list = global_data.player.get_upgrade_mecha_cost_list(self._mecha_id, self._cur_add_level)
        ex_cost_item_no, ex_cost_item_count = cost_list.get('ex_cost')
        init_tempate_mall_i_item(self._nd_visible.temp_item, ex_cost_item_no, show_tips=True)
        color = CAN_UPGRADE_COLOR if global_data.player.get_item_num_by_no(int(ex_cost_item_no)) >= ex_cost_item_count else CANT_UPGRADE_COLOR
        has_item_count = global_data.player.get_item_num_by_no(int(ex_cost_item_no))
        color_item_str = get_color_str(color, has_item_count)
        lab_quantity = self._nd_visible.temp_item.lab_quantity
        self._nd_visible.temp_item.lab_quantity.setString('{}/{}'.format(color_item_str, ex_cost_item_count))
        lab_quantity.setVisible(True)
        lab_cost = self._nd_visible.lab_cost
        common_cost_item_no, common_cost_item_count = cost_list.get('common_cost')
        color = CAN_UPGRADE_COLOR if global_data.player.get_item_num_by_no(int(common_cost_item_no)) >= common_cost_item_count else CANT_UPGRADE_COLOR
        color_item_str = get_color_str(color, common_cost_item_count)
        lab_cost.SetString(get_text_by_id(424).format(color_item_str))
        path = payment_item_pic(common_cost_item_no)
        lab_cost.nd_auto_fit.icon.SetDisplayFrameByPath('', path)

    def _update_select_state(self):
        for level, item in six_ex.items(self._level_2_item):
            if item and item.isValid():
                is_unlock = self._mecha_level >= level
                item.prog.SetPercent(100 if is_unlock else 0)
                if level <= self._cur_add_level + self._mecha_level and level > self._mecha_level:
                    item.btn_choose.SetSelect(True)
                    last_item = self._level_2_item.get(level - 1)
                    if last_item:
                        if last_item.isValid():
                            last_item.prog.SetPercent(100)
                else:
                    item.btn_choose.SetSelect(False)

    def destroy(self):
        self.process_events(False)