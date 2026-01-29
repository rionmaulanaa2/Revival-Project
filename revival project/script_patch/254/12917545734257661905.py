# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanRankScore.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gutils import clan_utils
from logic.gutils import template_utils
from common.const.property_const import *
from logic.gcommon.common_const import rank_const
from logic.comsys.clan.ClanPageBase import ClanPageBase
from logic.gutils.template_utils import update_badge_node
from logic.gutils.InfiniteScrollHelper import InfiniteScrollHelper

class ClanRankScore(ClanPageBase):

    def __init__(self, dlg):
        self.global_events = {'clan_rank_data': self.on_rank_list,
           'message_on_players_detail_inf': self.on_members_detail_inf,
           'clan_rank_reward': self.on_update_reward
           }
        super(ClanRankScore, self).__init__(dlg)

    def on_init_panel(self):
        super(ClanRankScore, self).on_init_panel()
        self.panel.temp_bg.setVisible(False)
        self._rank_step = 30
        self._list_sview = None
        self._rank_list = []
        self._data_cache_dict = {}
        self._rank_type = ''
        self._cur_selected_rank_info = None
        self._menu_options = [{'name': 81168,'val': rank_const.RANK_TYPE_CLAN_WEEK_POINT,'requested': False}, {'name': 81166,'val': rank_const.RANK_TYPE_CLAN_SEASON_POINT,'requested': False}]
        self.init_widget()
        self.panel.PlayAnimation('show')
        return

    def on_finalize_panel(self):
        super(ClanRankScore, self).on_finalize_panel()
        if self._list_sview:
            self._list_sview.destroy()
            self._list_sview = None
        return

    def refresh_panel(self):
        super(ClanRankScore, self).refresh_panel()
        self.panel.temp_bg.setVisible(False)

    def init_menu(self):
        show_list = [
         False]

        def set_show_list():
            show_list[0] = not show_list[0]
            self.panel.season_list.setVisible(show_list[0])
            self.panel.temp_bg.setVisible(show_list[0])
            self.panel.img_icon.setScaleY(-1 if show_list[0] else 1)

        @self.panel.btn_season.unique_callback()
        def OnClick(btn, touch):
            set_show_list()

        def OnClick(touch):
            if show_list[0]:
                set_show_list()

        self.panel.temp_bg.OnClick = OnClick
        self.panel.season_list.setVisible(show_list[0])
        self.panel.img_icon.setScaleY(-1 if show_list[0] else 1)
        menu_options = self._menu_options

        def callback(index):
            info = menu_options[index]
            self.panel.btn_season.SetText(info['name'])
            set_show_list()
            self.request_rank_list(info['val'])
            self.show_desc(info['val'])

        template_utils.init_common_choose_list(self.panel.season_list, menu_options, callback)
        default_option = menu_options[0]
        self.panel.btn_season.SetText(default_option['name'])
        self.request_rank_list(default_option['val'])
        self.show_desc(default_option['val'])

    def show_desc(self, rank_type):
        import cc
        import time
        from logic.gcommon.cdata import season_data
        import logic.gcommon.time_utility as tutil

        @self.panel.btn_describe.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(608040, 800159)

        if rank_type == rank_const.RANK_TYPE_CLAN_WEEK_POINT:
            left_time = tutil.get_next_utc8_monday_time()
            self.panel.lab_tips.SetString(get_text_by_id(607014).format(tutil.get_readable_time(left_time)))
        else:
            left_time = season_data.get_end_timestamp(season_data.get_cur_battle_season()) - tutil.time()
            day, hour, minute, second = tutil.get_day_hour_minute_second(left_time)
            self.panel.lab_tips.SetString(get_text_by_id(800143).format(day))

    def init_widget(self):
        self.init_menu()

    def set_rank_type_req_state(self, rank_type):
        for info in self._menu_options:
            if info['val'] == rank_type:
                info['requested'] = True
                return

    def get_rank_type_req_state(self, rank_type):
        for info in self._menu_options:
            if info['val'] == rank_type:
                return info['requested']

        return False

    def on_rank_list(self, rank_type, start_rank, *args):
        if self._rank_type != rank_type:
            return
        self.set_rank_type_req_state(rank_type)
        if start_rank == 0:
            self.init_rank_list(rank_type)
        self.request_players_detail_inf()

    def on_members_detail_inf(self, datas):
        self.refresh_exsit_list()

    def on_update_reward(self):
        self.refresh_exsit_list()

    def request_rank_list(self, rank_type):
        old_rank_type = self._rank_type
        self._rank_type = rank_type
        has_req = self.get_rank_type_req_state(self._rank_type)
        rank_data = global_data.message_data.get_rank_data(self._rank_type)
        if not rank_data or not has_req:
            cur_rank_index = 0
            include_self = True
        else:
            cur_rank_index = rank_data['cur_count']
            include_self = False
            if old_rank_type != rank_type:
                self.init_rank_list(rank_type)
                return
            if cur_rank_index >= rank_data['max_count']:
                return
        more_index = cur_rank_index + self._rank_step
        global_data.player.request_clan_rank_list(self._rank_type, cur_rank_index, more_index, include_self=include_self)

    def request_players_detail_inf(self):
        if not self._list_sview:
            return
        uid_list = []
        for data_list in self._rank_list:
            rank_info = self.get_rank_info(data_list)
            uid = rank_info['commander_uid']
            role_info = global_data.message_data.get_player_detail_inf(uid)
            if not role_info:
                uid_list.append(uid)

        uid_list and global_data.player.request_players_detail_inf(uid_list)

    def init_rank_list(self, rank_type):
        self._data_cache_dict = {}
        rank_data = global_data.message_data.get_rank_data(rank_type)
        self._rank_list = rank_data['rank_list']
        if self._list_sview:
            self._list_sview.destroy()
            self._list_sview = None
        self._list_sview = InfiniteScrollHelper(self.panel.rank_list, self.panel)
        self._list_sview.set_template_init_callback(self.on_init_list_item)
        self._list_sview.update_data_list(self._rank_list)
        self._list_sview.update_scroll_view()
        self._list_sview.set_require_data_callback(lambda : self.request_rank_list(self._rank_type))
        if global_data.player.is_in_clan():
            self.on_init_list_item(self.panel.rank_mine, self.get_my_rank_info())
            self.panel.rank_mine.setVisible(True)
        else:
            self.panel.rank_mine.setVisible(False)
        return

    def refresh_exsit_list(self):
        if not self._list_sview:
            return
        refresh_list = self._list_sview.get_view_list()
        for info in refresh_list:
            item_widget, data = info
            self.on_refresh_role_info(item_widget, data)

        if global_data.player.is_in_clan():
            self.on_init_list_item(self.panel.rank_mine, self.get_my_rank_info())
            self.panel.rank_mine.setVisible(True)
        else:
            self.panel.rank_mine.setVisible(False)

    def get_rank_info(self, data_list):
        if type(data_list) == dict:
            return data_list
        id_list = id(data_list)
        if id_list in self._data_cache_dict:
            return self._data_cache_dict[id_list]
        rank = self._rank_list.index(data_list) + 1
        data = {'clan_id': data_list[0],'clan_info': data_list[1],'rank_data': data_list[2]}
        info_list = data['clan_info']
        rank_info = {'rank': rank,
           'clan_id': data_list[0],
           'clan_name': info_list[0],'commander_uid': info_list[1],
           'lv': info_list[2],'member_num': info_list[3],
           'value_list': data_list[2],'is_percent': False,
           'badge': info_list[4]}
        self._data_cache_dict[id_list] = rank_info
        return rank_info

    def get_my_rank_info(self):
        rank_data = global_data.message_data.get_rank_data(self._rank_type)
        clan_id = global_data.player.get_clan_id()
        clan_name = global_data.player.get_clan_name()
        commander_uid = global_data.player.get_clan_commander_uid()
        clan_lv = global_data.player.get_clan_lv()
        badge = global_data.player.get_clan_badge()
        count = len(global_data.player.get_clan_member_list())
        clan_info = global_data.player.get_clan_info()
        if rank_const.RANK_TYPE_CLAN_WEEK_POINT == self._rank_type:
            value = clan_info.get('week_point', 0)
        else:
            value = clan_info.get('season_point', 0)
        value_list = [
         value]
        rank_info = {'rank': rank_data.get('player_rank', 999) if rank_data else 999,
           'clan_id': clan_id,
           'clan_name': clan_name,'commander_uid': commander_uid,
           'lv': clan_lv,'member_num': count,
           'value_list': value_list,'is_percent': rank_data.get('player_data', False) if rank_data else False,
           'badge': badge
           }
        return rank_info

    def on_refresh_role_info(self, item_widget, data_list):
        from logic.gutils import role_head_utils
        rank_info = self.get_rank_info(data_list)
        uid = rank_info['commander_uid']
        role_info = global_data.message_data.get_player_detail_inf(uid)
        role_info = role_info if role_info else {}
        role_head_utils.init_role_head(item_widget.temp_head, role_info.get(HEAD_FRAME, None), role_info.get(HEAD_PHOTO, None))
        item_widget.lab_captain.SetString(role_info.get(C_NAME, ''))
        return

    def on_init_list_item(self, item_widget, data_list):
        from common.cfg import confmgr
        from logic.gcommon.cdata import clan_rank_data
        rank_info = self.get_rank_info(data_list)
        rank_info['item_widget'] = item_widget
        my_clan_id = global_data.player.get_clan_id()
        is_percent = rank_info.get('is_percent', False)
        rank = rank_info.get('rank', 0)
        if rank is None:
            rank = 999
        if not is_percent and rank <= 3:
            item_widget.img_rank.SetDisplayFrameByPath('', template_utils.get_clan_rank_num_icon(rank))
            item_widget.img_rank.setVisible(True)
            item_widget.lab_rank.SetString('')
        else:
            item_widget.img_rank.setVisible(False)
            if is_percent:
                item_widget.lab_rank.SetString(get_text_by_id(800134, ['%.2f' % rank]))
            else:
                item_widget.lab_rank.SetString(str(rank))
        level = rank_info.get('lv', 1)
        item_widget.lab_lv.setString('Lv.{}'.format(level))
        badge = rank_info.get('badge', 0)
        update_badge_node(badge, item_widget.temp_crew_logo)
        item_widget.lab_name.SetString(rank_info.get('clan_name', ''))
        item_widget.lab_score.SetString(str(rank_info['value_list'][0]))
        max_num = clan_utils.get_clan_person_limit(level)
        item_widget.lab_total.SetString('{0}/{1}'.format(rank_info.get('member_num', 1), max_num))
        show_rank = is_percent or rank if 1 else rank + 1000
        reward_id = clan_rank_data.get_rank_reward_id(self._rank_type, show_rank, rank)
        item_no, item_num = (0, 1)
        if reward_id != None:
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            if len(reward_list) <= 0:
                print('[ERROR] ClanRankScore [{}] has no reward_list'.format(reward_id))
            else:
                first_reward_info = reward_list[0]
                item_no, item_num = first_reward_info[0], first_reward_info[1]
        reward_visible = item_no > 0
        item_widget.temp_reward.setVisible(reward_visible)
        if reward_visible:
            can_reward = my_clan_id == rank_info.get('clan_id', 0) and global_data.player.is_offer_clan_rank_reward(self._rank_type)

            def callback():
                can_reward = my_clan_id == rank_info.get('clan_id', 0) and global_data.player.is_offer_clan_rank_reward(self._rank_type)
                if can_reward:
                    global_data.player.request_offer_clan_rank_reward(self._rank_type)

            if can_reward:
                item_widget.temp_reward.PlayAnimation('get_tips')
                template_utils.init_tempate_mall_i_item(item_widget.temp_reward, item_no, item_num=item_num, callback=callback)
            else:
                item_widget.temp_reward.StopAnimation('get_tips')
                template_utils.init_tempate_mall_i_item(item_widget.temp_reward, item_no, item_num=item_num, show_tips=True)
        self.on_refresh_role_info(item_widget, data_list)
        clan_id = rank_info.get('clan_id')

        @item_widget.btn_details.unique_callback()
        def OnClick(btn, touch, c_id=clan_id):
            if clan_id:
                from logic.gutils.jump_to_ui_utils import jump_to_clan_card
                jump_to_clan_card(c_id)

        @item_widget.unique_callback()
        def OnClick(btn, touch):
            if self.panel.rank_mine == item_widget:
                return
            else:
                my_clan_id = global_data.player.get_clan_id()
                if self._cur_selected_rank_info:
                    last_item_widget = self._cur_selected_rank_info.get('item_widget', None)
                    if last_item_widget and last_item_widget.isValid():
                        last_item_widget.img_bg_sel.setVisible(False)
                        last_item_widget.temp_reward.setVisible(reward_visible)
                        last_item_widget.PlayAnimation('disappear', force_resume=True)
                        if last_item_widget == item_widget:
                            self._cur_selected_rank_info = None
                            return
                item_widget.img_bg_sel.setVisible(True)
                item_widget.temp_reward.setVisible(False)
                item_widget.PlayAnimation('appear', force_resume=True)
                self._cur_selected_rank_info = rank_info
                return

        return