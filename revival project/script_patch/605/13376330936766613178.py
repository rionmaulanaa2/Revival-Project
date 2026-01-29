# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/MechaRankWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.rank.BaseRankWidget import BaseRankWidget
from logic.gcommon.common_const.rank_mecha_const import mecha_rank_list
from logic.gcommon.common_const import rank_const
from logic.gutils import role_head_utils
from logic.gutils import season_utils
from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_TEAM
from cocosui import cc, ccui, ccs
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import template_utils
from logic.gutils import follow_utils
from logic.gutils.item_utils import get_mecha_name_by_id
FRIEND_RANK = 0
ALL_AREA_RANK = 1

class MechaRankWidget(BaseRankWidget):

    def __init__(self, parent_panel, nd, template_pos, rank_info):
        super(MechaRankWidget, self).__init__(rank_info)
        self.parent_panel = parent_panel
        self.nd = nd
        self._template_root = global_data.uisystem.load_template_create('rank/i_rank_mecha_list', parent=nd)
        self._template_root.setPosition(template_pos)
        self.list_rank = self._template_root.list_rank_list
        self._template_root.temp_top.btn_all.setVisible(False)
        self.cur_rank_type = None
        self.cur_rank_area = rank_const.ALL_AREA_RANK
        self.rank_index = None
        self.mecha_id_list = []
        self.init_mecha_id_list()
        self.init_list()
        self.init_top_panel()
        self.init_expire_panel()
        return

    def init_mecha_id_list(self):
        open_mecha_list = global_data.player.read_mecha_open_info()['opened_order']
        self.mecha_id_list = [ str(mecha_id) for mecha_id in open_mecha_list if str(mecha_id) in mecha_rank_list ]

    def init_top_panel(self):
        temp_top = self._template_root.temp_top
        self._template_root.nd_choose.setVisible(False)

        @temp_top.btn_chose_mode.unique_callback()
        def OnClick(*args):
            flag = self._template_root.nd_choose.isVisible()
            self._template_root.nd_choose.setVisible(not flag)
            temp_top.open.icon_open.setRotation(0 if flag else 180)

        default_show_idx = 0
        last_read_mecha_battle_id = global_data.achi_mgr.get_cur_user_archive_data(rank_const.RANK_MECHA_READ_RECORD_KEY, default=-1)
        if last_read_mecha_battle_id != -1:
            rank_idx = self.get_rank_idx_by_mecha_battle_id(last_read_mecha_battle_id)
            if rank_idx != -1:
                default_show_idx = rank_idx
        self._template_root.list_mech_choose.DeleteAllSubItem()
        for index in range(len(self.mecha_id_list)):
            self.add_mecha_choose_item(index, default_show_idx)

        self._template_root.nd_choose.img_bg.ResizeAndPosition()

    def init_expire_panel(self):

        @self._template_root.nd_idle.btn_idle_question.unique_callback()
        def OnClick(*args):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(15053), get_text_by_id(15052))

    def refresh_top_title(self, mecha_id):
        temp_top = self._template_root.temp_top
        temp_top.player_mech_head.setVisible(True)
        img_path = 'gui/ui_res_2/mall/10100%s_2.png' % mecha_id
        temp_top.player_mech_head.SetDisplayFrameByPath('', img_path)
        temp_top.lab_player_name.setString(get_mecha_name_by_id(mecha_id))

    def add_mecha_choose_item(self, index, default_show_idx=0):
        panel = self._template_root.list_mech_choose.AddTemplateItem()
        mecha_id = self.mecha_id_list[index]
        img_path = 'gui/ui_res_2/mall/10100%s_2.png' % mecha_id
        panel.mach_head.SetDisplayFrameByPath('', img_path)
        panel.lab_mech_name.setString(get_mecha_name_by_id(mecha_id))
        temp_top = self._template_root.temp_top

        @panel.btn_shose_mech.unique_callback()
        def OnClick(*args):
            if self.rank_index != index:
                self.rank_index = index
                self.cur_rank_type = mecha_id
                global_data.achi_mgr.set_cur_user_archive_data(rank_const.RANK_MECHA_READ_RECORD_KEY, int(mecha_id))
                self.request_rank_data()
                self.refresh_top_title(mecha_id)
            self._template_root.nd_choose.setVisible(False)
            temp_top.open.icon_open.setRotation(0)

        if index == default_show_idx:
            OnClick()

    def get_rank_idx_by_mecha_battle_id(self, mecha_id):
        if mecha_id is None:
            return -1
        else:
            for idx, info in enumerate(self.mecha_id_list):
                _mecha_id = int(info)
                if mecha_id == _mecha_id:
                    return idx

            return -1

    def refresh_my_data(self, data, rank):
        panel = super(MechaRankWidget, self).refresh_my_data(data, rank)
        if data[2][2]:
            panel.lab_number.SetColor('#SR')
            self._template_root.nd_idle.setVisible(True)
        else:
            panel.lab_number.SetColor('#SK')
            self._template_root.nd_idle.setVisible(False)

    def refresh_item(self, panel, data):
        rank = int(data[3] + 1)
        if rank >= 1 and rank <= 3:
            panel.img_rank.SetDisplayFrameByPath('', template_utils.get_clan_rank_num_icon(rank))
            panel.img_rank.setVisible(True)
            panel.lab_rank.setVisible(False)
        else:
            panel.img_rank.setVisible(False)
            panel.lab_rank.setVisible(True)
            panel.lab_rank.setString(str(rank))
        panel.lab_player_name.setString(str(data[1][0]))
        role_head_utils.init_role_head(panel.player_role_head, data[1][2], data[1][3])
        if data[2]:
            panel.lab_number.setString(str(data[2][0]))
        else:
            panel.lab_number.SetString(15051)
        follow_utils.refresh_rank_list_follow_status(panel, data[0], str(data[1][0]))
        self.add_player_simple_callback(panel.player_role_head, data, self._template_root.img_list_pnl)
        self.add_reques_model_info(panel, data[0])