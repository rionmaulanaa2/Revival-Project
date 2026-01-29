# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEDescribeUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_VKB_CLOSE
from common.cfg import confmgr
from logic.gutils.pve_utils import get_effect_desc_text
from logic.gcommon.common_utils.local_text import get_text_by_id

class PVEDescribeUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/pve_describe'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, *args):
        super(PVEDescribeUI, self).on_init_panel(*args)
        self.on_init_btn()

    def on_finalize_panel(self):
        super(PVEDescribeUI, self).on_finalize_panel()

    def on_init_btn(self):

        @self.panel.callback()
        def OnClick(btn, touch):
            self.close()

    def update_describe(self, desc_info):
        self.cur_level = desc_info['cur_level']
        self.desc_lst = desc_info['desc_lst']
        lenth = len(self.desc_lst)
        list_item = self.panel.list_describe
        list_item.SetInitCount(lenth)
        for idx in range(lenth):
            ui_item = list_item.GetItem(idx)
            info = self.desc_lst[idx]
            self.init_describe_item(ui_item, self.cur_level, info)

    def init_describe_item(self, item, cur_level, desc_info):
        line_level = desc_info['level']
        item.lab_describe.SetColor('#SW' if line_level >= cur_level else 8432076)
        item.lab_describe.SetString(desc_info['desc'])
        item.list_dot.SetInitCount(desc_info['level'])
        item.lab_level.setVisible(False)
        if desc_info['level'] == cur_level:
            item.lab_level.setVisible(True)
            item.lab_level.SetColor(2156983)
            item.lab_level.SetString(get_text_by_id(635275))
        elif desc_info['level'] == cur_level + 1:
            item.lab_level.setVisible(True)
            item.lab_level.SetColor(14893377)
            item.lab_level.SetString(get_text_by_id(635276))