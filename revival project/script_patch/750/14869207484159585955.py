# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEMonsterAttributesUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gutils.pve_utils import get_min_monster_level_by_chapter_id_and_difficulty
from logic.gcommon.common_const.pve_const import DIFFICULTY_TEXT_LIST, NORMAL_DIFFICUTY
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.uisys.basepanel import BasePanel
from common.cfg import confmgr
import six_ex
DIFFICULTY_ICON_PATH_LIST = {1: 'gui/ui_res_2/pve/catalogue/open/txt_pve_catalogue_dot_difficulty_0.png',
   2: 'gui/ui_res_2/pve/catalogue/open/txt_pve_catalogue_dot_difficulty_1.png',
   3: 'gui/ui_res_2/pve/catalogue/open/txt_pve_catalogue_dot_difficulty_2.png'
   }

class PVEMonsterAttributesUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/catalogue/open_pve_catalogue_info'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, chapter_id=None, monster_conf=None, *args, **kwargs):
        super(PVEMonsterAttributesUI, self).on_init_panel(*args, **kwargs)
        self.init_params(chapter_id, monster_conf)
        self.init_ui()
        self.init_ui_event()

    def init_params(self, chapter_id, monster_conf):
        self._chapter_id = chapter_id
        self._monster_conf = monster_conf
        self._monster_id = self._monster_conf.get('monster_id')
        self._monster_level_conf = confmgr.get('monster_level_data', str(self._monster_id), 'Content', default={})

    def init_ui(self):
        self._init_monster_widget()

    def init_ui_event(self):

        @self.panel.btn_close.unique_callback()
        def OnClick(btn, touch):
            self.close()

    def _init_monster_widget(self):
        list_info = self.panel.list_info
        for index, info_item in enumerate(list_info.GetAllItem()):
            difficulty = index + 1
            info_item.lab_difficulty.SetString(get_text_by_id(DIFFICULTY_TEXT_LIST[difficulty]))
            info_item.txt_difficulty.SetDisplayFrameByPath('', DIFFICULTY_ICON_PATH_LIST[difficulty])
            list_item = info_item.list_item
            list_item.DeleteAllSubItem()
            if global_data.player:
                has_unlock = global_data.player.has_unlock_difficulty_monster_book(difficulty, self._monster_id) if 1 else False
                item = has_unlock or list_item.AddTemplateItem()
                item.lab_title.SetString(get_text_by_id(860367))
                item.lab_data.SetString('\xef\xbc\x9f\xef\xbc\x9f')
                item.prog.SetPercentage(0)
                item = list_item.AddTemplateItem()
                item.lab_title.SetString(get_text_by_id(860368))
                item.lab_data.SetString('\xef\xbc\x9f\xef\xbc\x9f')
                item.prog.SetPercentage(0)
            else:
                monster_level = get_min_monster_level_by_chapter_id_and_difficulty(self._chapter_id, difficulty)
                monster_conf = self._monster_level_conf.get(str(monster_level))
                if monster_conf:
                    item = list_item.AddTemplateItem()
                    item.lab_title.SetString(get_text_by_id(860367))
                    monster_hp = monster_conf.get('Hp', 0)
                    item.lab_data.setString(str(monster_hp))
                    max_monster_hp = self._monster_conf.get('max_hp', 1)
                    item.prog.SetPercentage(float(monster_hp) / max_monster_hp * 100)
                    item = list_item.AddTemplateItem()
                    item.lab_title.SetString(get_text_by_id(860368))
                    monster_armor = monster_conf.get('Initial_Armor', 0)
                    item.lab_data.setString(str(monster_armor))
                    max_monster_armor = self._monster_conf.get('max_armor', 1)
                    item.prog.SetPercentage(float(monster_armor) / max_monster_armor * 100)