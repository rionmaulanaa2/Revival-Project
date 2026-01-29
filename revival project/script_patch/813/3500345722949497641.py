# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanApplyList.py
from __future__ import absolute_import
from logic.gutils import clan_utils
from common.const.property_const import *
from logic.comsys.clan.ClanPageBase import ClanPageBase
from logic.gutils.InfiniteScrollHelper import InfiniteScrollHelper

class ClanApplyList(ClanPageBase):

    def __init__(self, dlg):
        self.global_events = {'clan_members_request_list': self.init_widget,
           'message_on_players_detail_inf': self.init_apply_list
           }
        super(ClanApplyList, self).__init__(dlg)

    def on_init_panel(self):
        super(ClanApplyList, self).on_init_panel()
        self._list_sview = None
        global_data.player.request_clan_request()
        self.panel.PlayAnimation('show')
        return

    def on_finalize_panel(self):
        super(ClanApplyList, self).on_finalize_panel()
        if self._list_sview:
            self._list_sview.destroy()
            self._list_sview = None
        return

    def refresh_panel(self):
        super(ClanApplyList, self).refresh_panel()
        global_data.player.request_clan_request()

    def request_player_detail_info(self, uid_list):
        r_uid_list = []
        for uid in uid_list:
            player_info = global_data.message_data.get_player_detail_inf(uid)
            if not player_info:
                r_uid_list.append(uid)

        if r_uid_list:
            global_data.player.request_players_detail_inf(r_uid_list)
        else:
            self.init_apply_list(None)
        return

    def init_widget(self):

        @self.panel.btn_agree_all.btn_common.unique_callback()
        def OnClick(btn, touch):
            global_data.player.accept_clan_request(global_data.player.get_request_member_list())

        @self.panel.btn_ignore_all.btn_common.unique_callback()
        def OnClick(btn, touch):
            global_data.player.reject_clan_request(global_data.player.get_request_member_list())

        request_member_list = global_data.player.get_request_member_list()
        if len(request_member_list) > 0:
            self.panel.btn_agree_all.btn_common.SetEnable(True)
            self.panel.btn_ignore_all.btn_common.SetEnable(True)
            self.panel.lab_empty.setVisible(False)
        else:
            self.panel.btn_agree_all.btn_common.SetEnable(False)
            self.panel.btn_ignore_all.btn_common.SetEnable(False)
            self.panel.lab_empty.setVisible(True)
        self.request_player_detail_info(request_member_list)

    def init_apply_list(self, _):
        if self._list_sview:
            self._list_sview.destroy()
            self._list_sview = None
        self._list_sview = InfiniteScrollHelper(self.panel.i_vsrolllist_applicationlist, self.panel, up_limit=500, down_limit=500)
        self._list_sview.set_template_init_callback(self.on_init_list_item)
        self._list_sview.update_data_list(global_data.player.get_request_member_list(True))
        self._list_sview.update_scroll_view()
        return

    def on_init_list_item(self, item_widget, uid):
        from common import utilities
        from logic.gutils import season_utils
        from logic.gcommon.cdata import dan_data
        from logic.gutils import role_head_utils
        from logic.gcommon.common_const import rank_const
        str_uid = str(uid)
        request_message_dict = global_data.player.get_request_message_dict()
        player_info = global_data.message_data.get_player_detail_inf(uid)
        role_head_utils.init_role_head(item_widget.temp_head, player_info.get(HEAD_FRAME, None), player_info.get(HEAD_PHOTO, None))
        item_widget.lab_name.SetString(player_info.get(C_NAME, ''))
        dan_info = player_info.get('dan_info', {})
        dan_inf = dan_info.get(dan_data.DAN_SURVIVAL, {})
        role_head_utils.set_role_dan(item_widget.temp_tier, player_info.get('dan_info'))
        item_widget.lab_content1.SetString(season_utils.get_dan_lv_name(dan_inf.get('dan', dan_data.BROZE), lv=dan_inf.get('lv', dan_data.get_lv_num(dan_data.BROZE))))
        item_widget.lab_content2.SetString('{}'.format(request_message_dict.get(str_uid, {}).get('request_content', '')))

        @item_widget.btn_ignore.unique_callback()
        def OnClick(btn, touch):
            global_data.player.reject_clan_request([uid])

        @item_widget.btn_agree.unique_callback()
        def OnClick(btn, touch):
            global_data.player.accept_clan_request([uid])

        return