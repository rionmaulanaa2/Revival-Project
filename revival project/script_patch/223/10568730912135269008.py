# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/PetSkillWidget.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gutils.skin_define_utils import get_main_skin_id
from logic.gutils.pve_utils import get_attr_desc_text
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.item_utils import get_lobby_item_name, payment_item_pic
from logic.gcommon.item.item_const import FASHION_POS_SUIT
from logic.gcommon.common_utils.text_utils import get_color_str
from logic.gutils.pet_utils import get_pet_level, get_pet_skill_level, get_pet_max_skill_level, get_skill_unlock_pet_level
from common.utilities import get_rome_num
from common.utils.cocos_utils import ccp
from common.cfg import confmgr
import six_ex
from logic.gutils.item_utils import get_item_rare_degree, RARE_DEGREE_5
NORMAL_TEMPLATE_PATH = 'pet/i_pet_skill_item_small'
CURRENT_TEMPLATE_PATH = 'pet/i_pet_skill_item_big'
CAN_UPGRADE_COLOR = '0x04FA55FF'
CANT_UPGRADE_COLOR = '0xFF0000FF'

class PetSkillWidget(object):

    def __init__(self, panel):
        self.panel = panel
        self.init_params()
        self.process_events(True)

    def init_params(self):
        self._pet_skill_conf = confmgr.get('pet_skill', default={})
        self._pet_conf = confmgr.get('c_pet_info', default={})
        self._skin_id = None
        self._skill_conf = None
        self._max_level = None
        self._cur_level = None
        self._init_level = None
        self._cur_select_btn = None
        self.is_ss = False
        return

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'pet_info_updated': self._on_pet_info_updated
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def _on_pet_info_updated(self):
        cur_level = get_pet_skill_level(self._skin_id)
        if cur_level != self._cur_level:
            self._cur_level = cur_level
            self._init_level = self._get_init_level()
            self._update_skill_widget()

    def update_skin_id(self, skin_id):
        self._skin_id = skin_id
        rare_degree = get_item_rare_degree(self._skin_id)
        self.is_ss = rare_degree == RARE_DEGREE_5
        pet_conf = self._pet_conf.get(str(skin_id))
        skill_id = str(pet_conf.get('skill_id'))
        self._skill_conf = self._pet_skill_conf.get(skill_id)
        if not self._skill_conf:
            log_error('skill_id\xe9\x94\x99\xe8\xaf\xaf\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5525\xe5\x8f\xb7\xe8\xa1\xa8\xef\xbc\x9a\xe5\xae\xa0\xe7\x89\xa9id\xef\xbc\x9a{}\xef\xbc\x8c\xe6\x8a\x80\xe8\x83\xbdid\xef\xbc\x9a{}'.format(skin_id, skill_id))
            return
        else:
            self._max_level = get_pet_max_skill_level(skin_id)
            self._cur_level = get_pet_skill_level(self._skin_id)
            self._init_level = self._get_init_level()
            self._cur_select_btn = None
            self._update_skill_widget()
            return

    def _get_init_level(self):
        if self._cur_level >= self._max_level:
            return self._max_level
        else:
            if self._cur_level > 0:
                return self._cur_level
            return 1

    def _update_skill_widget(self):
        self._update_nd_skill()
        self._update_effect_desc(self._init_level)

    def _update_nd_skill(self):
        list_skill = self.panel.list_skill
        list_skill.DeleteAllSubItem()
        for index in range(self._max_level):
            level = index + 1
            template_conf = global_data.uisystem.load_template(NORMAL_TEMPLATE_PATH)
            skill_item = list_skill.AddItem(template_conf)
            prog_dot = skill_item.prog_dot
            prog_dot.DeleteAllSubItem()
            for dot_index in range(self._max_level):
                dot_level = dot_index
                dot_item = prog_dot.AddTemplateItem()
                btn_dot = dot_item.btn_dot
                btn_dot.EnableCustomState(True)
                if level > dot_level:
                    btn_dot.SetSelect(True)
                else:
                    btn_dot.SetSelect(False)

            bar_prog = skill_item.bar_prog
            is_unlock = self._cur_level >= level
            if level == self._max_level:
                bar_prog.setVisible(False)
            else:
                bar_prog.prog.SetPercent(100 if is_unlock else 0)
                bar_prog.setVisible(True)
            skill_unlock_pet_level = get_skill_unlock_pet_level(level)
            if skill_unlock_pet_level and skill_unlock_pet_level > get_pet_level(self._skin_id) or not is_unlock:
                skill_item.lab_lock.setString(get_text_by_id(860336).format(skill_unlock_pet_level))
                skill_item.nd_lock.setVisible(True)
            else:
                skill_item.lab_lock.setString('')
                skill_item.nd_lock.setVisible(False)
            skill_item.img_skill.SetDisplayFrameByPath('', self._skill_conf['icon'])
            btn_choose = skill_item.btn_choose
            btn_choose.EnableCustomState(True)
            if level == self._init_level:
                if self._cur_select_btn and level != self._max_level:
                    self._cur_select_btn.SetSelect(False)
                self._cur_select_btn = btn_choose
                self._cur_select_btn.GetParent().setScale(1)
                self._cur_select_btn.SetSelect(True)
            pnl_png = 'gui/ui_res_2/pet/bar_pve_skill_item.png'
            if self.is_ss and level == self._max_level:
                pnl_png = 'gui/ui_res_2/pet/bar_pve_skill_item_big.png'
            skill_item.bar.SetDisplayFrameByPath('', pnl_png)

            @btn_choose.callback()
            def OnClick(btn, touch, level=level, skill_item=skill_item):
                self._update_effect_desc(level)
                self._cur_select_btn.SetSelect(False)
                self._cur_select_btn.GetParent().setScale(0.74)
                self._cur_select_btn = btn
                btn.SetSelect(True)
                btn.GetParent().setScale(1)
                self._set_left_pos(skill_item, level)

        self.panel.lab_name_skill.setString(get_text_by_id(self._skill_conf['name_id']))
        init_item = list_skill.GetItem(self._init_level - 1)
        self._set_left_pos(init_item, self._init_level - 1)

    def _set_left_pos(self, item, index):
        if not item:
            return
        list_skill = self.panel.list_skill
        w, h = item.GetContentSize()
        viewSize = list_skill.getContentSize()
        contentSize = list_skill.getInnerContainerSize()
        max_off_x = contentSize.width - viewSize.width
        pos_x = -min(max((index - 2) * (w - 11), 0), max_off_x)
        self.panel.SetTimeOut(0.1, lambda : list_skill.SetContentOffsetInDuration(ccp(pos_x, 0), 0.1), 999)

    def _update_effect_desc(self, level):
        if not level:
            level = 1
        self.panel.lab_level_skill.setString(get_text_by_id(860352).format(get_rome_num(int(level))))
        attr_str = get_attr_desc_text(self._skill_conf['long_desc_id'], self._skill_conf['long_desc_params'], level)
        self.panel.lab_describe.setString(attr_str)

    def destroy(self):
        self.process_events(False)