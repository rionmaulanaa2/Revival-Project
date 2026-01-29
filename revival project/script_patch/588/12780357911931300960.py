# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanRankFashion.py
from __future__ import absolute_import
import cc
from logic.gutils import clan_utils
from logic.gutils import template_utils
from common.const.property_const import *
from logic.gcommon.common_const import rank_const
from logic.comsys.clan.ClanPageBase import ClanPageBase
from logic.gutils.template_utils import update_badge_node
from logic.gutils.InfiniteScrollHelper import InfiniteScrollHelper
ROTATE_FACTOR = 850

class ClanRankFashion(ClanPageBase):

    def __init__(self, dlg):
        self.global_events = {'clan_rank_data': self.on_rank_list,
           'message_on_players_detail_inf': self.on_members_detail_inf
           }
        super(ClanRankFashion, self).__init__(dlg)

    def on_init_panel(self):
        super(ClanRankFashion, self).on_init_panel()
        self._rank_step = 30
        self._list_sview = None
        self._rank_list = []
        self._data_cache_dict = {}
        self._rank_type = rank_const.RANK_TYPE_CLAN_FASHION
        self._has_req = False
        self._cur_selected_rank_info = None
        self._selected_uid = None
        self._cur_role_info = None
        self._init_show_widget = None
        self.init_widget()
        self.panel.PlayAnimation('show')
        return

    def on_finalize_panel(self):
        super(ClanRankFashion, self).on_finalize_panel()
        if self._list_sview:
            self._list_sview.destroy()
            self._list_sview = None
        return

    def set_show(self, show):
        super(ClanRankFashion, self).set_show(show)
        if not show:
            global_data.emgr.change_model_display_scene_item.emit(None)
        else:
            self.show_model()
        return

    def refresh_panel(self):
        super(ClanRankFashion, self).refresh_panel()

    def show_desc(self):
        from logic.gcommon.time_utility import get_readable_time

        @self.panel.btn_describe.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(608040, 800159)

        self.panel.lab_tips.SetString('')

    def init_widget(self):
        self.panel.nd_model.setVisible(False)
        self.show_desc()
        self.request_rank_list(self._rank_type)

    def on_rank_list(self, rank_type, start_rank, *args):
        if self._rank_type != rank_type:
            return
        if start_rank == 0:
            self._has_req = True
            self.init_rank_list(rank_type)
        self.request_players_detail_inf()

    def on_members_detail_inf(self, datas):
        if self.panel.isVisible():
            self.show_role()

    def request_rank_list(self, rank_type):
        self._rank_type = rank_type
        rank_data = global_data.message_data.get_rank_data(self._rank_type)
        if not rank_data or not self._has_req:
            cur_rank_index = 0
            include_self = True
        else:
            cur_rank_index = rank_data['cur_count']
            include_self = False
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

    def select_rank_item(self, index):
        if not self._list_sview:
            return
        else:
            refresh_list = self._list_sview.get_view_list()
            for i, info in enumerate(refresh_list):
                if index == i:
                    item_widget, data = info
                    item_widget.OnClick(None)
                    break

            return

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
        self._init_role_display()
        return

    def _init_role_display(self):
        if not self._list_sview:
            return
        refresh_list = self._list_sview.get_view_list()
        if refresh_list:
            item_widget, data = refresh_list[0]
            rank_info = self.get_rank_info(data)
            item_widget.img_bg_sel.setVisible(True)
            self.show_role(rank_info.get('commander_uid'))
            self._init_show_widget = item_widget

    def refresh_exsit_list(self):
        if not self._list_sview:
            return
        refresh_list = self._list_sview.get_view_list()
        for info in refresh_list:
            item_widget, data = info

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
        value_list = [
         clan_info.get('fashion_value', 0)]
        rank_info = {'rank': rank_data.get('player_rank', 999),
           'clan_id': clan_id,
           'clan_name': clan_name,'commander_uid': commander_uid,
           'lv': clan_lv,'member_num': count,
           'value_list': value_list,'is_percent': rank_data.get('player_data', False),
           'badge': badge
           }
        return rank_info

    def on_init_list_item(self, item_widget, data_list):
        rank_info = self.get_rank_info(data_list)
        rank_info['item_widget'] = item_widget
        is_percent = rank_info.get('is_percent', False)
        rank = rank_info.get('rank', 0)
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
        item_widget.lab_fashion.SetString(str(rank_info['value_list'][0]))
        max_num = clan_utils.get_clan_person_limit(level)
        item_widget.lab_total.SetString('{0}/{1}'.format(rank_info.get('member_num', 1), max_num))
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
                if self._init_show_widget and self._init_show_widget.isValid():
                    self._init_show_widget.img_bg_sel.setVisible(False)
                if self._cur_selected_rank_info:
                    last_item_widget = self._cur_selected_rank_info.get('item_widget', None)
                    if last_item_widget and last_item_widget.isValid():
                        last_item_widget.img_bg_sel.setVisible(False)
                        last_item_widget.StopAnimation('disappear')
                        last_item_widget.StopAnimation('appear')
                        last_item_widget.PlayAnimation('disappear', force_resume=True)
                        if last_item_widget == item_widget:
                            self._cur_selected_rank_info = None
                            return
                item_widget.StopAnimation('disappear')
                item_widget.StopAnimation('appear')
                item_widget.img_bg_sel.setVisible(True)
                item_widget.PlayAnimation('appear', force_resume=True)
                self._cur_selected_rank_info = rank_info
                self.show_role(rank_info.get('commander_uid'))
                return

    def show_role(self, uid=None):
        if uid:
            self._selected_uid = uid
        else:
            uid = self._selected_uid
        if not uid:
            return
        role_info = global_data.message_data.get_player_detail_inf(uid)
        if not role_info:
            return
        self.panel.nd_model.setVisible(True)
        self.panel.lab_name.SetString(role_info.get(C_NAME, ''))

        @self.panel.btn_captain_info.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.message import PlayerSimpleInf
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            ui.refresh_by_uid(uid)
            ui.set_position(touch.getLocation(), anchor_point=cc.Vec2(0.5, 0.5))

        self.panel.btn_captain_info.setVisible(uid != global_data.player.uid)

        @self.panel.nd_model.unique_callback()
        def OnDrag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

        self.show_model(role_info)

    def show_model(self, role_info=None):
        from logic.gutils import lobby_model_display_utils
        if role_info:
            self._cur_role_info = role_info
        else:
            role_info = self._cur_role_info
        if not role_info:
            return
        role_fashion = role_info.get('role_fashion')
        if not role_fashion:
            return
        item_no = role_fashion.get('0', 0)
        if item_no <= 0:
            return
        model_data = lobby_model_display_utils.get_lobby_model_data(item_no)
        global_data.emgr.change_model_display_scene_item.emit(model_data)