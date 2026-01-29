# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/GlRankContentWidget.py
from __future__ import absolute_import
from logic.gcommon.common_const import rank_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.role_head_utils import init_role_head

class GlRankContentWidget(object):

    def __init__(self, parent_panel, panel, check_sview_callback=None, *args, **kargs):
        self.panel = panel
        self.parent_panel = parent_panel
        self._rank_sview_height = self.panel.getContentSize().height
        self._rank_data = []
        self._sview_index = 0
        self._is_check_sview = False
        self.check_sview_callback = check_sview_callback

        def scroll_callback(sender, eventType):
            if self._is_check_sview == False:
                self._is_check_sview = True
                self.panel.SetTimeOut(0.021, self.check_sview)

        self.panel.addEventListener(scroll_callback)

    def check_sview(self):
        msg_count = len(self._rank_data)
        self._sview_index = self.panel.AutoAddAndRemoveItem(self._sview_index, self._rank_data, msg_count, self.add_rank_elem, 300, 300)
        self._is_check_sview = False
        if self.check_sview_callback:
            self.check_sview_callback(self._sview_index, msg_count)

    def add_rank_elem(self, data, is_back_item=True, index=-1):
        if is_back_item:
            panel = self.panel.AddTemplateItem(bRefresh=True)
        else:
            panel = self.panel.AddTemplateItem(0, bRefresh=True)
        if (data[3] + 1) % 2:
            panel.img_bg.setVisible(False)
        if global_data.player and global_data.player.uid == data[0]:
            panel.img_bg_self.setVisible(True)
            panel.img_bg.setVisible(False)
        else:
            panel.img_bg_self.setVisible(False)
        self._refresh_item_rank_data(panel, data, False)

        @panel.unique_callback()
        def OnClick(btn, *args):
            if global_data.player and data[0] == global_data.player.uid:
                return
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            if ui:
                ui.refresh_by_uid(data[0])
                pos = self.panel.ConvertToWorldSpacePercentage(100, 50)
                pos.x -= 345
                pos.y += 215
                ui.nd_tips.SetPosition(pos.x, pos.y)

        panel.temp_head.setSwallowTouches(False)
        return panel

    def refresh_rank_content(self, rank_data):
        self.panel.DeleteAllSubItem()
        self.refresh_self_rank_data(rank_data['player_rank'], rank_data['player_data'])
        self._rank_data = rank_data['rank_list']
        data_count = len(self._rank_data)
        self._sview_index = 0
        all_height = 0
        index = 0
        while all_height < self._rank_sview_height + 100 and index < data_count:
            data = self._rank_data[index]
            panel = self.add_rank_elem(data)
            all_height += panel.getContentSize().height
            index += 1

        self._sview_index = index - 1

    def clear_content(self):
        self.panel.DeleteAllSubItem()

    def refresh_self_rank_data(self, player_rank, player_data):
        my_player_nd = self.parent_panel.rank_player
        self._refresh_item_rank_data(my_player_nd, player_data, True, player_rank)

    def _refresh_item_rank_data(self, nd_item, data, is_self_rank=False, player_rank=None):
        if is_self_rank:
            if player_rank == rank_const.RANK_DATA_OUTSIDE:
                text = get_text_by_id(15016)
            elif player_rank == rank_const.RANK_DATA_NONE:
                text = '-'
            else:
                text = str(player_rank) if player_rank <= 1000 else get_text_by_id(15016)
            head_frame = global_data.player.get_head_frame()
            head_photo = global_data.player.get_head_photo()
            init_role_head(nd_item.temp_head, head_frame, head_photo)
            nd_item.lab_name.setString(global_data.player.get_name() if global_data.player else '')
            nd_item.lab_rank.setString(text)
        else:
            char_name, role_id, head_frame, head_photo = data[1]
            init_role_head(nd_item.temp_head, head_frame, head_photo)
            nd_item.lab_name.setString(str(char_name))
            nd_item.lab_rank.setString(str(data[3] + 1))
        nd_item.lab_number.setString(str(data[2][0]))

    def destroy(self):
        self.panel = None
        self.parent_panel = None
        self._rank_data = []
        self.check_sview_callback = None
        return