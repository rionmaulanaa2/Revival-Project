# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityPeakWeekendMatch.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gcommon.const import ACTIVITY_PEAK_WEEKEND_MATCH_KEY, ACTIVITY_PEAK_WEEKEND_MATCH_KEY_NEW
from logic.gcommon.cdata.week_competition import get_week_competition_conf, get_week_competition_conf_by_date

class ActivityPeakWeekendMatch(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityPeakWeekendMatch, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        pass

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'reply_last_week_comp_result_event': self.on_recieve_comp_result
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
        from logic.gcommon.cdata.dan_data import get_dan_name_id
        ret = self.get_neareast_competition()
        if ret[0] != -1:
            i, competition_id, start_ts, battle_info, reward_info = ret
            limit_dan = battle_info.get('limit_dan', 6)
            rule = get_text_by_id(19297, {'dan': limit_dan})
            self.set_show_rule(rule)
        else:
            rule = get_text_by_id(19297)
            self.set_show_rule(rule)
        conf = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        lab_time_conf = conf.get('lab_time_text', {})
        if lab_time_conf:
            host_num = global_data.channel.get_host_num()
            for text_id, host_num_list in six.iteritems(lab_time_conf):
                if host_num in host_num_list:
                    self.panel.lab_time.SetString(int(text_id))
                    break

        self.panel.nd_empty.setVisible(True)
        self.panel.list_item.setVisible(False)
        self.panel.list_btn.setVisible(False)
        if not global_data.player:
            return
        competition_list = global_data.player.get_last_week_comp_result()
        if competition_list:
            self.refresh_competition_list(competition_list)
        global_data.player.request_last_week_comp_result()
        if self.panel.btn_question:

            @self.panel.btn_question.unique_callback()
            def OnClick(btn, touch, *args):
                desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
                from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
                dlg = GameRuleDescUI()
                dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(607171)))

    def get_neareast_competition(self):
        from logic.gcommon import time_utility as tutil
        from logic.gcommon.cdata.week_competition import get_week_competition_conf
        return get_week_competition_conf()

    def on_recieve_comp_result(self):
        self.refresh_competition_list(global_data.player.get_last_week_comp_result())

    def refresh_competition_list(self, competition_list):
        from logic.gcommon.cdata import week_competition as wcomp
        from logic.gcommon import time_utility as tutil
        self.competition_list = competition_list
        self.write_local_data()
        comp_count = len(competition_list)
        for comp_idx in range(comp_count):
            comp_id = competition_list[comp_idx][0]
            week_comp_conf = wcomp.get_weekcomp_info_by_comp_id(comp_id)
            if not week_comp_conf:
                self.panel.nd_empty.setVisible(True)
                self.panel.list_item.setVisible(False)
                self.panel.list_btn.setVisible(False)
                return

        if not competition_list:
            self.panel.nd_empty.setVisible(True)
            self.panel.list_item.setVisible(False)
            self.panel.list_btn.setVisible(False)
            return
        else:
            self.panel.nd_empty.setVisible(False)
            self.panel.list_item.setVisible(True)
            self.panel.list_btn.setVisible(True)
            self.panel.list_btn.SetInitCount(comp_count)
            import time as sys_time
            for comp_idx in range(comp_count):
                ui_item = self.panel.list_btn.GetItem(comp_idx)
                comp_id = competition_list[comp_idx][0]
                comp_data = competition_list[comp_idx][1]
                week_comp_conf = wcomp.get_weekcomp_info_by_comp_id(comp_id)
                start_ts = week_comp_conf[1]
                time_tuple = sys_time.localtime(start_ts)
                ui_item.btn_top.SetText(str('%d.%02d' % (time_tuple[1], time_tuple[2])))

                @ui_item.btn_top.callback()
                def OnClick(btn, touch, comp_idx=comp_idx):
                    allItems = self.panel.list_btn.GetAllItem()
                    for _ui_item in allItems:
                        _ui_item.btn_top.SetSelect(False)

                    btn.SetSelect(True)
                    self._refresh_competition_list(comp_idx)

            first_ui_item = self.panel.list_btn.GetItem(0)
            first_ui_item.btn_top.OnClick(None)
            return

    def write_local_data(self):
        from logic.gcommon import time_utility as tutil
        comp_id_list = [ comp_info[0] for comp_info in self.competition_list ]
        global_data.achi_mgr.get_general_archive_data().set_field(ACTIVITY_PEAK_WEEKEND_MATCH_KEY, comp_id_list)
        _, competition_id, start_time, _, _ = get_week_competition_conf_by_date()
        cur_time = int(tutil.get_server_time())
        if tutil.is_same_day(cur_time, start_time):
            cache_comp_id_list_new = global_data.achi_mgr.get_general_archive_data().get_field(ACTIVITY_PEAK_WEEKEND_MATCH_KEY_NEW, [])
            competition_id = str(competition_id)
            if competition_id not in cache_comp_id_list_new:
                cache_comp_id_list_new.append(competition_id)
                global_data.achi_mgr.get_general_archive_data().set_field(ACTIVITY_PEAK_WEEKEND_MATCH_KEY_NEW, cache_comp_id_list_new)
        global_data.emgr.refresh_activity_redpoint.emit()

    def _refresh_competition_list(self, comp_idx):
        competition_list = self.competition_list
        if comp_idx >= len(competition_list):
            return
        comp_id = competition_list[comp_idx][0]
        comp_data = competition_list[comp_idx][1]
        self.panel.list_item.SetInitCount(len(comp_data))
        rank_key_list = sorted(six_ex.keys(comp_data))
        rank_list = [ comp_data[k] for k in rank_key_list ]
        for i in range(len(rank_list)):
            ui_item = self.panel.list_item.GetItem(i)
            self.init_player_info(ui_item, i + 1, rank_list[i])

    def init_player_info(self, ui_item, rank, player_data):
        from logic.gutils import template_utils
        from logic.gutils.role_head_utils import get_head_photo_res_path, get_role_default_photo
        if rank >= 1 and rank <= 3:
            ui_item.img_rank.SetDisplayFrameByPath('', template_utils.get_clan_rank_num_icon(rank))
            ui_item.img_rank.setVisible(True)
            ui_item.lab_rank.setVisible(False)
        else:
            ui_item.img_rank.setVisible(False)
            ui_item.lab_rank.setVisible(True)
            ui_item.lab_rank.SetString(str(rank))
        ui_item.lab_name.SetString(player_data.get('char_name', ''))
        if rank > 3:
            ui_item.lab_title.SetString(get_text_by_id(19409).format(**{'rank': rank}))
        else:
            rank_dict = {1: 609762,
               2: 609763,
               3: 609764
               }
            ui_item.lab_title.SetString(rank_dict.get(rank), 609765)
        role_id = player_data.get('role_id')
        mecha_id_type = player_data.get('mecha_id')
        show_icons = []
        if role_id:
            photo_no = get_role_default_photo(role_id)
            icon = get_head_photo_res_path(photo_no)
            show_icons.append(icon)
        if mecha_id_type:
            icon = 'gui/ui_res_2/item/role_head/3021%s.png' % str(mecha_id_type)
            show_icons.append(icon)
        ui_item.list_head.SetInitCount(len(show_icons))
        for idx in range(len(show_icons)):
            head_item = ui_item.list_head.GetItem(idx)
            head_item.img_head.SetDisplayFrameByPath('', show_icons[idx])