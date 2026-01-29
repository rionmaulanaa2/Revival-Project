# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityWinterCupScoreRank.py
from __future__ import absolute_import
import six
import six_ex
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
import cc
from logic.gcommon.common_utils.local_text import get_text_by_id

class ActivityWinterCupScoreRank(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityWinterCupScoreRank, self).__init__(dlg, activity_type)
        self.init_event()

    def init_event(self):
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)

    def set_activity_info(self, *args):
        global_data.player.get_notice_rank_list()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_winter_cup_rank': self.on_recieve_comp_result
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        self.on_init_panel()

    def set_show_rule(self, rule):
        import cc
        self.panel.list_rule.SetInitCount(1)
        text_item = self.panel.list_rule.GetItem(0)
        text_item.lab_describe.SetString(rule)
        text_item.lab_describe.formatText()
        sz = text_item.lab_describe.GetTextContentSize()
        sz.height += 20
        old_sz = text_item.getContentSize()
        text_item.setContentSize(cc.Size(old_sz.width, sz.height))
        text_item.RecursionReConfPosition()
        old_inner_size = self.panel.list_rule.GetInnerContentSize()
        self.panel.list_rule.SetInnerContentSize(old_inner_size.width, sz.height)
        self.panel.list_rule.GetContainer()._refreshItemPos()
        self.panel.list_rule._refreshItemPos()

    def on_init_panel(self):
        item = self.panel.list_rule.GetItem(0)
        item.lab_describe.SetString(get_text_by_id(635232))
        size_text = item.lab_describe.getContentSize()
        item.lab_describe.formatText()
        sz = item.lab_describe.GetTextContentSize()
        old_sz = item.getContentSize()
        item.setContentSize(cc.Size(old_sz.width, sz.height + 20))
        item.RecursionReConfPosition()
        old_inner_size = self.panel.list_rule.GetInnerContentSize()
        self.panel.list_rule.SetInnerContentSize(old_inner_size.width, sz.height)
        self.panel.list_rule.GetContainer()._refreshItemPos()
        self.panel.list_rule._refreshItemPos()
        if not global_data.player:
            return
        self.refresh_competition_list(global_data.player.get_winter_cup_rank_result())

    def on_recieve_comp_result(self):
        self.refresh_competition_list(global_data.player.get_winter_cup_rank_result())

    def refresh_competition_list(self, competition_info):
        if not competition_info:
            return
        rank_list, self_info = competition_info
        self.refresh_self_rank(self_info)
        if not rank_list:
            self.panel.nd_empty.setVisible(True)
            self.panel.list_item.setVisible(False)
            return
        self.panel.nd_empty.setVisible(False)
        self.panel.list_item.setVisible(True)
        self.panel.list_item.SetInitCount(len(rank_list))
        for i in range(len(rank_list)):
            role_info = rank_list[i]
            ui_item = self.panel.list_item.GetItem(i)
            self.init_player_info(ui_item, role_info.get('rank'), role_info)

    def refresh_self_rank(self, rank_info):
        self.panel.temp_mine.setVisible(False)
        if rank_info:
            self.panel.temp_mine.setVisible(True)
            self.init_player_info(self.panel.temp_mine, rank_info.get('rank'), rank_info)

    def init_player_info(self, ui_item, rank, player_data):
        from logic.gutils import template_utils
        from logic.gutils.role_head_utils import get_head_photo_res_path, get_role_default_photo, init_role_head
        if rank is not None:
            if rank >= 1 and rank <= 3:
                ui_item.img_rank.SetDisplayFrameByPath('', template_utils.get_clan_rank_num_icon(rank))
                ui_item.img_rank.setVisible(True)
                ui_item.lab_rank.setVisible(False)
            else:
                ui_item.img_rank.setVisible(False)
                ui_item.lab_rank.setVisible(True)
                ui_item.lab_rank.SetString(str(rank))
        else:
            ui_item.img_rank.setVisible(False)
            ui_item.lab_rank.setVisible(False)
        ui_item.lab_name.SetString(player_data.get('char_name', ''))
        ui_item.lab_score.SetString(str(int(player_data.get('score', 0))))
        show_icons = [
         (
          player_data.get('head_frame', None), player_data.get('head_photo', None))]
        ui_item.list_head.SetInitCount(len(show_icons))
        for idx in range(len(show_icons)):
            head_item = ui_item.list_head.GetItem(idx)
            head_info = show_icons[idx]
            init_role_head(head_item, head_info[0], head_info[1])

        return