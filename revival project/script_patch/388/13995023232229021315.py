# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Clone/CloneMechaSkillDetail.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from common.cfg import confmgr
ICON_PREFIX = 'gui/ui_res_2/battle/mech_main/'

class CloneMechaSkillDetail(BasePanel):
    PANEL_CONFIG_NAME = 'battle_clone/clone_details_skill'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self._skill_node_lst = [self.panel.temp_skill_1, self.panel.temp_skill_2,
         self.panel.temp_skill_3, self.panel.temp_skill_4, self.panel.temp_skill_5]
        self.panel.setLocalZOrder(1)

    def on_finalize_panel(self):
        pass

    def init_parameters(self):
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self._skill_conf = confmgr.get('mecha_display', 'HangarConfig_Skills', 'Content')

    def refresh_ui(self, mecha_id):
        show_skill_list = self._get_show_skill_list(mecha_id)
        for index, nd in enumerate(self._skill_node_lst):
            if index >= len(show_skill_list):
                nd.setVisible(False)
                continue
            skill_id = show_skill_list[index]
            skill_conf = self._skill_conf.get(str(skill_id))
            skill_icon = ''.join([ICON_PREFIX, skill_conf.get('icon_path'), '.png'])
            skill_name = skill_conf.get('name_text_id', '')
            skill_desc = skill_conf.get('desc_text_id', '')
            skill_desc_brief = skill_conf.get('desc_text_brief', '')
            nd.lab_name.SetString(skill_name)
            nd.lab_sort.SetString(skill_desc_brief)
            nd.lab_describe.SetString(skill_desc)
            nd.img_skill.SetDisplayFrameByPath('', skill_icon)
            nd.setVisible(True)

        if len(show_skill_list) == 4:
            self.panel.PlayAnimation('show_4')
        else:
            self.panel.PlayAnimation('show_5')

    def _get_show_skill_list(self, mecha_id):
        mecha_skill_lst = self._mecha_conf[str(mecha_id)].get('mecha_skill_list')
        mecha_sp_skill_lst = self._mecha_conf[str(mecha_id)].get('mecha_sp_skill_list', [])
        show_skill_list = [ x for x in mecha_skill_lst ]
        if mecha_sp_skill_lst:
            show_skill_list.extend(mecha_sp_skill_lst)
        return show_skill_list