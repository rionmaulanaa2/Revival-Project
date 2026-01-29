# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEPetBuffUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_NO_EFFECT
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pve_utils import get_attr_desc_text
from logic.gutils.pet_utils import get_pet_skill_level, get_pet_max_skill_level
from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
import six_ex

class PVEPetBuffUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/pet/open_pve_pet_setting'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        super(PVEPetBuffUI, self).on_init_panel(*args, **kwargs)
        self.init_params()
        self.init_ui()
        self.init_ui_event()

    def init_params(self):
        self._pet_conf = confmgr.get('c_pet_info', default={})
        self._pet_skill_conf = confmgr.get('pet_skill', default={})

    def init_ui(self):
        self._init_pet_widget()

    def init_ui_event(self):

        @self.panel.btn_close.unique_callback()
        def OnClick(btn, touch):
            self.close()

        @self.panel.btn_describe.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(860346, 860347)

        @self.panel.btn_setting.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_pve_pet
            jump_to_pve_pet()
            self.close()

    def _init_pet_widget(self):
        pet_dict = global_data.player.get_pve_pet_dict() if global_data.player else {}
        list_skill = self.panel.list_skill
        list_skill.DeleteAllSubItem()
        has_pet = False
        for index, pet_id in six_ex.items(pet_dict):
            if pet_id:
                has_pet = True
                item = list_skill.AddTemplateItem()
                item.img_tag_fight.setVisible(index == 0)
                item.img_tag_ready.setVisible(index != 0)
                item.img_item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(pet_id))
                pet_conf = self._pet_conf.get(str(pet_id))
                skill_id = str(pet_conf.get('skill_id'))
                skill_conf = self._pet_skill_conf.get(skill_id)
                if not skill_conf:
                    log_error('skill_id\xe9\x94\x99\xe8\xaf\xaf\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5525\xe5\x8f\xb7\xe8\xa1\xa8\xef\xbc\x9a\xe5\xae\xa0\xe7\x89\xa9id\xef\xbc\x9a{}\xef\xbc\x8c\xe6\x8a\x80\xe8\x83\xbdid\xef\xbc\x9a{}'.format(skin_id, skill_id))
                    continue
                item.icon_skill.SetDisplayFrameByPath('', skill_conf['icon'])
                skill_level = get_pet_skill_level(pet_id)
                skill_max_level = get_pet_max_skill_level(pet_id)
                list_prog_dot = item.prog_dot
                list_prog_dot.DeleteAllSubItem()
                for index in range(skill_max_level):
                    item_prog_dot = list_prog_dot.AddTemplateItem()
                    btn_dot = item_prog_dot.btn_dot
                    btn_dot.EnableCustomState(True)
                    level = index + 1
                    if skill_level >= level:
                        btn_dot.SetSelect(True)
                    else:
                        btn_dot.SetSelect(False)

                item.lab_name_skill.setString(get_text_by_id(skill_conf['name_id']))
                attr_str = get_attr_desc_text(skill_conf['long_desc_id'], skill_conf['long_desc_params'], skill_level)
                item.lab_describe.setString(attr_str)

        self.panel.nd_empty.setVisible(not has_pet)