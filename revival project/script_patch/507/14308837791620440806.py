# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/rank/PVERankMechaPageUI.py
from __future__ import absolute_import
from logic.comsys.battle.pve.rank.PVESingleBaseRankWidget import PVESingleBaseRankWidget
from cocosui import cc, ccui, ccs
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_mecha_name_by_id
from logic.gutils.pve_utils import get_pve_mecha_id_list
from common.cfg import confmgr
from logic.gcommon.common_const.pve_const import PVE_RANK_MECHA
from logic.gcommon.common_const.rank_const import MONTH_REFRESH
from logic.gcommon.common_const.pve_const import HELL_DIFFICUTY, PVE_RANK_MECHA

class PVERankMechaPageUI(PVESingleBaseRankWidget):
    RANK_PAGE_TYPE = PVE_RANK_MECHA

    def __init__(self, parent_panel, parent_node, template_pos, rank_config):
        self.parent_panel = parent_panel
        self.parent = parent_node
        self.mecha_index = None
        self.mecha_id_list = get_pve_mecha_id_list()
        self.mecha_config = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
        page_config = self.get_default_config()
        super(PVERankMechaPageUI, self).__init__(rank_config, page_config)
        return

    def load_page_panel(self):
        self._template_root = global_data.uisystem.load_template_create('pve/rank/i_pve_rank_mecha', parent=self.parent)
        self.list_rank = self._template_root.list_rank_list
        self.temp_mine = self._template_root.temp_mine

    def init_choose_list(self):
        self.cur_sel_condition.init_friend_choose()
        self.cur_sel_condition.init_chapter_choose_list()
        self.init_top_panel()

    def get_default_config(self):
        cur_pve_mecha_id = global_data.player.get_pve_select_mecha_id()
        config = {'chapter': 1,
           'mecha': cur_pve_mecha_id,
           'difficulty': HELL_DIFFICUTY,
           'list_type': MONTH_REFRESH,
           'is_friend': False
           }
        return config

    def init_top_panel(self):
        self._template_root.nd_choose_mecha.setVisible(False)
        btn_mecha = self._template_root.btn_mecha

        @btn_mecha.unique_callback()
        def OnClick(*args):
            nd_choose_mecha = self._template_root.nd_choose_mecha
            nd_choose_mecha.setVisible(not nd_choose_mecha.isVisible())
            self._template_root.nd_auto_fit.ResizeAndPosition()

        default_show_idx = 0
        self._template_root.nd_auto_fit.ResizeAndPosition()
        self._template_root.list_mech_choose.DeleteAllSubItem()
        for index in range(len(self.mecha_id_list)):
            self.add_mecha_choose_item(index, default_show_idx)

        @self._template_root.nd_choose_mecha.unique_callback()
        def OnClick(btn, touch):
            self._template_root.nd_choose_mecha.setVisible(False)

    def refresh_top_title(self, mecha_id):
        img_path = self.mecha_config[mecha_id]['icon']
        self._template_root.img_mecha.setVisible(True)
        self._template_root.img_mecha.SetDisplayFrameByPath('', img_path)
        self._template_root.lab_name_mecha.setString(get_mecha_name_by_id(mecha_id))

    def add_mecha_choose_item(self, index, default_show_idx=0):
        panel = self._template_root.list_mech_choose.AddTemplateItem()
        mecha_id = self.mecha_id_list[index]
        img_path = 'gui/ui_res_2/item/role_head/3021%s.png' % mecha_id
        panel.img_mecha.SetDisplayFrameByPath('', img_path)
        panel.lab_name_mecha.setString(get_mecha_name_by_id(mecha_id))

        @panel.btn_mecha.unique_callback()
        def OnClick(btn, touch, _mecha_id=mecha_id):
            if self.mecha_index != index:
                self.mecha_index = index
                self.cur_sel_condition.switch_choose_mecha(_mecha_id)
                self.refresh_top_title(_mecha_id)
            self._template_root.nd_choose_mecha.setVisible(False)

        if index == default_show_idx:
            OnClick(panel, None, mecha_id)
        return