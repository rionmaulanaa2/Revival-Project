# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/rank/CharmRankWidget.py
from __future__ import absolute_import
from logic.comsys.rank.BaseRankWidget import BaseRankWidget
from logic.gcommon.common_const import rank_const
from logic.gutils import role_head_utils
from logic.gutils import season_utils
from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_TEAM
from cocosui import cc, ccui, ccs
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import friend_const, chat_const
from logic.gutils import template_utils
from logic.gutils import follow_utils

class CharmRankWidget(BaseRankWidget):

    def __init__(self, parent_panel, nd, template_pos, rank_info):
        super(CharmRankWidget, self).__init__(rank_info)
        self.parent_panel = parent_panel
        self.nd = nd
        self._template_root = global_data.uisystem.load_template_create('rank/i_rank_charm_list', parent=nd)
        self._template_root.setPosition(template_pos)
        self.list_rank = self._template_root.list_rank_list
        self.cur_rank_type = rank_const.RANK_TYPE_CHARM
        self.cur_rank_area = None
        self.init_list()
        self.init_rank_area_choose()
        return

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
        social_friend = self._message_data.get_social_friend_by_uid(friend_const.SOCIAL_ID_TYPE_LINEGAME, data[0])
        if self.cur_rank_area == rank_const.LINE_FRIEND_RANK and social_friend and data[0] != global_data.player.uid:
            icon = '<img="{}",scale=0.65>'.format(chat_const.LINE_ICON)
            desc_content = '#SW{}#n#DG{}#n'.format(icon, self._message_data.get_line_friend_name(social_friend.get('social_id')))
            panel.lab_dec.SetString(desc_content)
            panel.lab_dec.setVisible(True)
            panel.lab_player_name.SetPosition('50%-82', '50%+10')
        else:
            panel.lab_dec.setVisible(False)
            panel.lab_player_name.SetPosition('50%-82', '50%-2')
        rank = data[2][0]
        if rank == rank_const.RANK_DATA_OUTSIDE:
            text = get_text_by_id(15016)
        elif rank == rank_const.RANK_DATA_NONE:
            text = '-'
        else:
            text = str(rank)
        follow_utils.refresh_rank_list_follow_status(panel, data[0], str(data[1][0]))
        panel.lab_number.setString(text)
        self.add_player_simple_callback(panel.player_role_head, data, self._template_root.img_list_pnl)
        self.add_reques_model_info(panel, data[0])