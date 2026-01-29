# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/PlayerSimpleInf.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import ui_operation_const
from logic.gcommon.common_const.battle_const import DEFAULT_INVITE_TID
import common.const.uiconst
from common.const.property_const import *
from logic.gcommon import const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import role_head_utils
from logic.gutils import template_utils
from logic.gcommon.const import AVATAR_SEX_NONE, PRIV_SHOW_BADGE, PRIV_SHOW_PURPLE_ID
from logic.gutils.template_utils import set_sex_node_img, update_badge_node
from logic.gcommon.cdata.privilege_data import COLOR_NAME
BTN_TYPE_PLAYER_INF = 10001
BTN_TYPE_ADD_Friend = 10002
BTN_TYPE_CHAT = 10003
BTN_TYPE_TEAM = 10004
BTN_TYPE_JOIN_TEAM = 10283
BTN_TYPE_BLACK_LIST = 10005
BTN_TYPE_DEL_FRIEND = 10006
BTN_TYPE_DEL_BLACK_LIST = 10007
BTN_TYPE_ROOM_AS_JUDGE = 19321
BTN_TYPE_ROOM_KICK_OUT = 19322
BTN_TYPE_ROOM_RETURN_WAITING = 19323
BTN_TYPE_TEAM_KICK_OUT = 13023
BTN_TYPE_REPORT = 80878
BTN_TYPE_MOD_CLAN_TITLE = 800035
BTN_TYPE_CLAN_KICK = 800036
BTN_TYPE_CLAN = 800043
BTN_TYPE_FOLLOW = 10344
BTN_TYPE_UN_FOLLOW = 10343
BTN_TYPE_TRANSFER_OWNERSHIP = 862015
BTN_TYPE_CHANGE_SEAT = 862013
BTN_TYPE_JUDGEMENT_ADJUST_SEAT = 609220
BTN_TYPE_MODIFY_NAME = 81300
BTN_TYPE_INTIMACY = 3214
BTN_TYPE_HOMELAND = 611550
from common.const import uiconst
HISTORY_UI_LIST = ('TrainEndStatisticsShareUI', 'MutiOccupyStatisticsUI', 'CrownStatisticsShareUI',
                   'FlagStatisticsShareUI', 'DeathStatisticsShareUI', 'FFAStatisticsShareUI',
                   'GVGStatisticsShareUI', 'ImproviseHistoryStatUI', 'EndStatisticsShareUI',
                   'DeathEndTransitionUI', 'ArmRaceStatisticsShareUI', 'OccupyStatisticsShareUI',
                   'GoldenEggEndStatisticsShareUI', 'GooseBearEndStatisticsShareUI',
                   'LuckScoreRankListUI', 'IntimacyHistoricalEventUI')

class PlayerSimpleInf(BasePanel):
    PANEL_CONFIG_NAME = 'message/player_simple_inf'
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    BORDER_INDENT = 24
    UI_ACTION_EVENT = {'btn_lobby.OnClick': 'on_click_bth_home',
       'btn_add.OnClick': 'on_click_add_btn',
       'btn_chat.OnClick': 'on_click_chat_btn'
       }

    def on_init_panel(self, *args, **kargs):
        if not global_data.player:
            self.close()
            return
        else:
            self._my_uid = global_data.player.uid
            self._cur_uid = None
            self._need_update_button = None
            self._need_update_button_name = None
            self.need_close_history_ui = False
            self.show_btn_more = True
            self.show_btn_del = False
            self._chat_source = {}
            self._init_pnl_width, self._init_pnl_height = self.panel.nd_tips.GetContentSize()
            self._message_data = global_data.message_data
            self.process_event(True)

            @self.panel.callback()
            def OnClick(*args):
                self.close()

            self.init_btns()
            self.panel.nd_tips.lv_btn.DeleteAllSubItem()
            self._btns = [
             BTN_TYPE_PLAYER_INF, BTN_TYPE_TEAM, BTN_TYPE_BLACK_LIST]
            self._extra_btns = []
            return

    def on_finalize_panel(self):
        self.btns_map = {}
        self._btns = []
        self._need_update_button = None
        self.process_event(False)
        return

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = {'message_on_player_simple_inf': self.on_refresh_player_inf,
           'message_refresh_intimacy_data': self.on_refresh_intimacy_data,
           'team_invite_count_down_event': self.update_team_button,
           'close_simple_inf_ui': self.close_for_team_info_changed
           }
        if flag:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def custom_show_btns_func(self, custom_btn_map):
        self.btns_map.update(custom_btn_map)

    def custom_show_btn(self, show_btns):
        self._btns = show_btns

    def hide_btn_chat(self):
        self.panel.btn_chat.setVisible(False)

    def del_btn(self, btn):
        if btn in self._btns:
            self._btns.remove(btn)

    def set_extra_btns(self, btns):
        for btn in btns:
            if btn not in self.btns_map:
                log_error('unsupport extra btns', btns)
                return

        self._extra_btns = btns

    def refresh_by_uid(self, uid, show_btn_more=True, show_btn_del=False):
        self._cur_uid = uid
        self.show_btn_more = show_btn_more
        self.show_btn_del = show_btn_del
        self.player_inf = self._message_data.get_player_simple_inf(self._cur_uid)
        if self.player_inf:
            self.on_refresh_player_inf(self.player_inf)
        else:
            self.panel.setVisible(False)
        global_data.player.get_one_player_online_state(self._cur_uid)
        self.on_refresh_intimacy_data()

    def on_refresh_intimacy_data(self):
        from logic.gcommon.cdata.intimacy_data import get_intimacy_pt
        from logic.gutils.intimacy_utils import init_intimacy_icon_with_uid
        from logic.gcommon.const import IDX_INTIMACY_LV
        self.panel.temp_intimacy.setVisible(False)
        self.panel.nd_intimacy.setVisible(False)
        if not self._cur_uid or not self._message_data.is_friend(self._cur_uid):
            return
        else:
            show_intimacy = init_intimacy_icon_with_uid(self.panel.temp_intimacy, self._cur_uid, team_show_limit=False)
            intimacy_data = global_data.player.intimacy_data.get(str(self._cur_uid), None)
            if show_intimacy:

                @self.panel.temp_intimacy.btn_touch.callback()
                def OnClick(*args):
                    global_data.game_mgr.show_tip(get_text_by_id(3285, {'name': self.player_inf[C_NAME],'n': str(intimacy_data[IDX_INTIMACY_LV])}))

            if not show_intimacy:
                self.panel.nd_intimacy.setVisible(True)
                pt = get_intimacy_pt(intimacy_data)
                self.panel.nd_intimacy.lab_value_num.SetString(str(pt))

                @self.panel.nd_intimacy.callback()
                def OnClick(*args):
                    global_data.game_mgr.show_tip(get_text_by_id(3284, {'name': self.player_inf[C_NAME],'n': str(pt)}))

            return

    def on_refresh_player_inf(self, player_inf):
        if player_inf[U_ID] != self._cur_uid:
            return
        else:
            self.panel.setVisible(True)
            self.player_inf = player_inf
            more_btns = []
            if self.show_btn_more:
                if global_data.message_data.is_friend(self._cur_uid):

                    def on_btn_remark--- This code section failed: ---

 188       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('ChangeRemarkName',)
           6  IMPORT_NAME           0  'logic.comsys.message.ChangeName'
           9  IMPORT_FROM           1  'ChangeRemarkName'
          12  STORE_FAST            0  'ChangeRemarkName'
          15  POP_TOP          

 189      16  POP_TOP          
          17  PRINT_ITEM_TO    
          18  PRINT_ITEM_TO    
          19  LOAD_DEREF            0  'self'
          22  LOAD_ATTR             2  '_cur_uid'
          25  LOAD_CONST            4  'u_name'
          28  LOAD_DEREF            0  'self'
          31  LOAD_ATTR             3  'player_inf'
          34  LOAD_GLOBAL           4  'C_NAME'
          37  BINARY_SUBSCR    
          38  CALL_FUNCTION_512   512 
          41  POP_TOP          

 190      42  LOAD_DEREF            0  'self'
          45  LOAD_ATTR             5  'close'
          48  CALL_FUNCTION_0       0 
          51  POP_TOP          

Parse error at or near `POP_TOP' instruction at offset 16

                    more_btns.append((610880, on_btn_remark))

                    def on_btn_top():
                        if self._cur_uid in global_data.player._top_frds:
                            global_data.player.remove_top_friend(self._cur_uid)
                        else:
                            global_data.player.set_top_friend(self._cur_uid)

                    more_btns.append((11516 if self._cur_uid in global_data.player._top_frds else 610884, on_btn_top))
            if self.show_btn_del:
                if str(self._cur_uid) in global_data.message_data._chat_friend:

                    def on_btn_del_record():
                        global_data.message_data.del_record(self._cur_uid)
                        global_data.message_data.del_chat_data(self._cur_uid)
                        self.close()

                    more_btns.append((611315, on_btn_del_record))
            more_btn_names = []
            if global_data.player and BTN_TYPE_FOLLOW not in more_btn_names:
                more_btn_names.append(BTN_TYPE_FOLLOW)
            more_btn_names = [ self.btn_name_checker(i) for i in more_btn_names ]
            more_btn_names = [ _f for _f in more_btn_names if _f ]
            for btn_name in more_btn_names:
                more_btns.append((btn_name, self.btns_map.get(btn_name)))

            self.panel.btn_more.setVisible(bool(more_btns))
            if more_btns:

                @self.panel.btn_more.callback()
                def OnClick(*args):
                    self.panel.nd_more.setVisible(not self.panel.nd_more.isVisible())

                self.panel.nd_more.list_button.SetInitCount(len(more_btns))
                for i, (btn_name, btn_func) in enumerate(more_btns):
                    btn_item = self.panel.nd_more.list_button.GetItem(i)
                    btn_item.btn_common.SetText(btn_name)

                    @btn_item.btn_common.callback()
                    def OnClick(btn, touch, func=btn_func):
                        func()

            nd_tips = self.panel.nd_tips
            nd_tips.lv_btn.DeleteAllSubItem()
            if G_IS_NA_USER:
                nd_tips.lab_id.SetString(str(player_inf.get('bind_uid', self._cur_uid)))
            else:
                show_id = int(player_inf.get('bind_uid', self._cur_uid))
                show_id -= global_data.uid_prefix
                nd_tips.lab_id.SetString(str(show_id))
            battle_pass_lv = player_inf.get('battlepass_lv', 1)
            nd_tips.nd_bp_level.lab_bp_level.setString(str(battle_pass_lv))
            if player_inf.get('intro', ''):
                nd_tips.lab_sign.setString(str(player_inf.get('intro')))
            else:
                nd_tips.lab_sign.SetString(10048)
            clan_info = player_inf.get('clan_info', {})
            if not clan_info:
                if self.player_inf.get(CLAN_ID, -1) > 0:
                    global_data.player.request_player_info(const.PLAYER_INFO_BRIEF, self._cur_uid)
                nd_tips.nd_crew.setVisible(False)
            else:
                nd_tips.nd_crew.setVisible(True)
                nd_tips.nd_crew.lab_crew.SetString(str(clan_info.get('clan_name')))
                nd_tips.nd_crew.lab_crew_level.SetString(str(clan_info.get('lv', 0)))
                update_badge_node(clan_info.get('badge', 0), nd_tips.nd_crew.temp_crew_logo)

                @nd_tips.nd_crew.btn_crew.unique_callback()
                def OnClick(btn, touch, clan_id=clan_info['clan_id']):
                    from logic.gutils.jump_to_ui_utils import jump_to_clan_card
                    jump_to_clan_card(clan_id)

            role_head_utils.init_role_head_auto(nd_tips.temp_role_head, self._cur_uid, 0, player_inf)

            @nd_tips.temp_role_head.callback()
            def OnClick(btn, touch):
                self.on_detail_inf()

            uid = player_inf.get('uid')
            role_head_utils.init_dan_info(nd_tips.temp_tier, uid, player_inf)
            replace_dict = {}
            if global_data.player.get_team_info() is not None:
                if global_data.player.is_teammate(self._cur_uid):
                    if global_data.player.is_leader():
                        replace_dict = {BTN_TYPE_TEAM: BTN_TYPE_TEAM_KICK_OUT}
                    else:
                        replace_dict = {BTN_TYPE_TEAM: None}
            else:
                friend_online_state = global_data.message_data.get_player_online_state()
                state = int(friend_online_state.get(int(self._cur_uid), const.STATE_OFFLINE))
                if state == const.STATE_TEAM:
                    replace_dict = {BTN_TYPE_TEAM: BTN_TYPE_JOIN_TEAM}
                else:
                    replace_dict = {BTN_TYPE_JOIN_TEAM: BTN_TYPE_TEAM}
            for idx, but_name in enumerate(list(self._btns)):
                if but_name in replace_dict:
                    self._btns[idx] = replace_dict[but_name]

            is_friend = self._message_data.is_friend(self._cur_uid)
            if is_friend:
                if BTN_TYPE_DEL_FRIEND not in self._btns:
                    self._btns.append(BTN_TYPE_DEL_FRIEND)
            self._need_update_button = None
            if global_data.player and global_data.player.is_in_clan() and BTN_TYPE_CLAN not in self._btns and BTN_TYPE_CLAN_KICK not in self._btns and self.player_inf.get(CLAN_ID, -1) == -1:
                self._btns.append(BTN_TYPE_CLAN)
            if BTN_TYPE_REPORT not in self._btns:
                self._btns.append(BTN_TYPE_REPORT)
            for btn in self._extra_btns:
                if btn not in self._btns:
                    self._btns.append(btn)

            for but_name in self._btns:
                self.add_button(but_name)

            self.ajust_panel_size()
            nd_tips.lab_name.SetString(str(player_inf[C_NAME]))
            remark = global_data.player._frds_remark.get(uid, '')
            nd_tips.lab_name2.setVisible(bool(remark))
            if remark:
                nd_tips.lab_name2.SetString('(%s)' % remark)
            sex = player_inf.get('sex', AVATAR_SEX_NONE)
            set_sex_node_img(nd_tips.lab_name.nd_auto_fit.img_gender, sex)
            if not is_friend:
                self.panel.btn_add.SetEnable(True)
                self.panel.btn_add.img_tick.setVisible(False)
                self.panel.btn_add.lab_add.SetString(13025)
            else:
                self.panel.btn_add.SetEnable(False)
                self.panel.btn_add.img_tick.setVisible(True)
                self.panel.btn_add.lab_add.SetString(13026)
            count_down_data = global_data.player.get_count_down()
            self.update_team_button(count_down_data)
            role_head_utils.init_privilege_name_color_and_badge(nd_tips.lab_name, nd_tips.temp_role_head, player_inf)
            return

    def ajust_panel_size(self):
        import math
        btn_count = self.panel.nd_tips.lv_btn.GetItemCount()
        lines = int(math.ceil(float(btn_count) / 2))
        add_lines = lines - 2
        if add_lines > 0:
            _, btn_height = self.panel.nd_tips.lv_btn.GetItem(0).GetContentSize()
            btn_height += self.panel.nd_tips.lv_btn.GetVertIndent()
            self.panel.nd_tips.SetContentSize(self._init_pnl_width, self._init_pnl_height + btn_height * add_lines)
            self.panel.nd_tips.img_bg.ResizeAndPosition()
            self.panel.nd_tips.ChildRecursionRePosition()

    def btn_name_checker(self, btn_name):
        from logic.gutils import clan_utils
        from logic.gcommon.common_const import clan_const
        if btn_name is None:
            return
        else:
            if btn_name == BTN_TYPE_ADD_Friend:
                if self._cur_uid == self._my_uid or self._message_data.is_black_friend(self._cur_uid):
                    return
                if self._message_data.is_friend(self._cur_uid):
                    btn_name = BTN_TYPE_DEL_FRIEND
            elif btn_name == BTN_TYPE_BLACK_LIST:
                if self._cur_uid == self._my_uid:
                    return
                if self._message_data.is_black_friend(self._cur_uid):
                    btn_name = BTN_TYPE_DEL_BLACK_LIST
            elif btn_name == BTN_TYPE_CLAN:
                if self._cur_uid == self._my_uid:
                    return
            elif btn_name == BTN_TYPE_MOD_CLAN_TITLE:
                if self._cur_uid == self._my_uid:
                    return
                cur_title = clan_utils.get_clan_member_info_by_field(self._cur_uid, 'title', default=clan_const.MASS)
                if not clan_utils.get_permission('appoint_permission_titles', title=cur_title):
                    return
            elif btn_name == BTN_TYPE_CLAN_KICK:
                if self._cur_uid == self._my_uid:
                    return
                cur_title = clan_utils.get_clan_member_info_by_field(self._cur_uid, 'title', default=clan_const.MASS)
                if not clan_utils.get_permission('kick_permission_titles', title=cur_title):
                    return
            elif btn_name == BTN_TYPE_FOLLOW:
                if self._cur_uid == self._my_uid:
                    return
                if global_data.player and global_data.player.has_follow_player(self._cur_uid):
                    btn_name = BTN_TYPE_UN_FOLLOW
            elif btn_name == BTN_TYPE_INTIMACY:
                if not self._message_data.is_friend(self._cur_uid):
                    return
            return btn_name

    def add_button(self, btn_name):
        btn_name = self.btn_name_checker(btn_name)
        if btn_name is None:
            return
        else:
            panel = self.panel.nd_tips.lv_btn.AddTemplateItem()
            panel.btn_player_info.SetText(get_text_by_id(btn_name))
            if btn_name == BTN_TYPE_TEAM or btn_name == BTN_TYPE_JOIN_TEAM:
                self._need_update_button = panel
                self._need_update_button_name = btn_name

            @panel.btn_player_info.callback()
            def OnClick(*args):
                self.btns_map[btn_name]()

            return

    def update_team_button(self, count_down_dict):
        if self._cur_uid not in count_down_dict:
            return
        if self._need_update_button and self._need_update_button.isValid():
            count_down = count_down_dict[self._cur_uid]
            text = get_text_by_id(self._need_update_button_name)
            if count_down > 0:
                self._need_update_button.btn_player_info.SetEnable(False)
                text += '({}s)'.format(count_down)
            else:
                self._need_update_button.btn_player_info.SetEnable(True)
            self._need_update_button.btn_player_info.SetText(text)

    def close_for_team_info_changed(self, uid):
        if type(uid) in (list, tuple):
            for i in uid:
                if i == self._cur_uid:
                    self.close()

        elif uid == self._cur_uid:
            self.close()

    def init_btns(self):

        def on_addfriend():
            global_data.player.req_add_friend(self._cur_uid)
            self.close()

        def on_delfriend():
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            from logic.gutils.friend_utils import del_friend_with_intimacy_confirm

            def confirm_callback():
                del_friend_with_intimacy_confirm(self._cur_uid)

            SecondConfirmDlg2().confirm(content=get_text_by_id(10008), confirm_callback=confirm_callback)
            self.close()

        def on_chat():
            ui = global_data.ui_mgr.show_ui('MainFriend', 'logic.comsys.message')
            role_id = self.player_inf.get(ROLE_ID, const.DEFAULT_ROLE_ID)
            dan_info = self.player_inf.get('dan_info', {})
            ui.open_new_chat_dialog(self._cur_uid, self.player_inf[C_NAME], self.player_inf[U_LV], role_id, dan_info)
            self.close()

        def on_team():
            from logic.gutils import team_utils
            team_utils.on_team(self.player_inf)

        def on_join_team():
            from logic.gutils import team_utils
            team_utils.on_join_team(self.player_inf)

        def on_blacklist():
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            from logic.gutils.friend_utils import black_friend_with_intimacy_confirm

            def confirm_callback():
                black_friend_with_intimacy_confirm(self._cur_uid)

            SecondConfirmDlg2().confirm(content=get_text_by_id(10009), confirm_callback=confirm_callback)
            self.close()

        def on_del_blacklist():
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

            def confirm_callback():
                global_data.player.req_del_from_list(const.FRD_KEY_BALCLIST, self._cur_uid)

            SecondConfirmDlg2().confirm(content=get_text_by_id(10010), confirm_callback=confirm_callback)
            self.close()

        def on_kickout():
            if global_data.player.is_leader():
                global_data.player.kick_teammate(self._cur_uid)
            self.close()

        def on_detail_inf():
            self.on_detail_inf()

        def on_report_user():
            from logic.gcommon.common_const.log_const import REPORT_FROM_TYPE_CHAT, REPORT_CLASS_NORMAL, REPORT_FROM_TYPE_LOBBY_NORMAL
            if self._cur_uid and self.player_inf:
                ui = global_data.ui_mgr.show_ui('UserReportUI', 'logic.comsys.report')
                ui.report_users([{'uid': self._cur_uid,'name': self.player_inf[C_NAME],'intro': self.player_inf.get('intro', '')}])
                ui.set_report_class(REPORT_CLASS_NORMAL)
                extra_info = self._chat_source.get(str(self._cur_uid), {})
                report_from = REPORT_FROM_TYPE_CHAT if extra_info.get('channel', '') else REPORT_FROM_TYPE_LOBBY_NORMAL
                ui.set_extra_report_info(extra_info.get('channel', ''), extra_info.get('chat', ''), report_from)
                self.close()

        def on_mod_clan_title--- This code section failed: ---

 531       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('ClanChangeTitleUI',)
           6  IMPORT_NAME           0  'logic.comsys.clan.ClanChangeTitleUI'
           9  IMPORT_FROM           1  'ClanChangeTitleUI'
          12  STORE_FAST            0  'ClanChangeTitleUI'
          15  POP_TOP          

 532      16  POP_TOP          
          17  PRINT_ITEM_TO    
          18  PRINT_ITEM_TO    
          19  LOAD_DEREF            0  'self'
          22  LOAD_ATTR             2  '_cur_uid'
          25  CALL_FUNCTION_256   256 
          28  POP_TOP          

 533      29  LOAD_DEREF            0  'self'
          32  LOAD_ATTR             3  'close'
          35  CALL_FUNCTION_0       0 
          38  POP_TOP          

Parse error at or near `POP_TOP' instruction at offset 16

        def on_clan_kick():
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

            def confirm_callback():
                global_data.player.request_kick_member(self._cur_uid)

            SecondConfirmDlg2().confirm(content=get_text_by_id(800107, {'name': self.player_inf[C_NAME]}), confirm_callback=confirm_callback)
            self.close()

        def on_clan_invite():
            if not global_data.player or not global_data.player.is_in_clan():
                return
            global_data.game_mgr.show_tip(get_text_by_id(800044))
            clan_name = global_data.player.get_clan_name()
            clan_id = global_data.player.get_clan_id()
            show_text = get_text_by_id(800045, (clan_name,))
            msg_str = '<link=3,clan_id=%d,clan_name="%s">%s</link>' % (clan_id, clan_name, show_text)
            global_data.message_data.recv_to_friend_msg(self._cur_uid, self.player_inf[C_NAME], msg_str)
            player_c_id = self.player_inf.get(CLAN_ID, -1)
            global_data.player.req_friend_msg(self._cur_uid, self.player_inf[U_LV], player_c_id, msg_str)

        def on_btn_un_follow():
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

            def click_unfollow():
                global_data.player and global_data.player.try_unfollow(self._cur_uid)

            if global_data.player and global_data.player.has_follow_player(self._cur_uid):
                SecondConfirmDlg2().confirm(content=get_text_by_id(10345), confirm_callback=click_unfollow)
            self.close()

        def on_btn_follow():
            if global_data.player and not global_data.player.has_follow_player(self._cur_uid):
                global_data.player.try_follow(self._cur_uid)
            self.close()

        def on_btn_intimacy():
            from .MainFriend import FRIEND_TAB_INTIMACY
            _, type, _, lv, _ = global_data.player.intimacy_data.get(str(self._cur_uid), (0,
                                                                                          None,
                                                                                          None,
                                                                                          0,
                                                                                          -1))
            if lv <= 0:
                global_data.game_mgr.show_tip(3243)
            else:

                def ui_init_finish_cb():
                    sub_panel = ui.touch_tab_by_index(FRIEND_TAB_INTIMACY)
                    sub_panel.panel_widget.touch_tab_by_index(None, 0 if type else 1)
                    return

                ui = global_data.ui_mgr.get_ui('MainFriend')
                if ui:
                    ui_init_finish_cb()
                else:
                    ui = global_data.ui_mgr.show_ui('MainFriend', 'logic.comsys.message')
                    ui.set_ui_init_finish_cb(FRIEND_TAB_INTIMACY, ui_init_finish_cb)
                self.close()
            return None

        def on_btn_homeland(*args):
            player = global_data.player
            if not player:
                return
            global_data.ui_mgr.close_ui('LotteryMainUI')
            self.close_history_ui()
            player.request_visit_player(self._cur_uid)

        self.btns_map = {BTN_TYPE_ADD_Friend: on_addfriend,
           BTN_TYPE_DEL_FRIEND: on_delfriend,
           BTN_TYPE_CHAT: on_chat,
           BTN_TYPE_TEAM: on_team,
           BTN_TYPE_JOIN_TEAM: on_join_team,
           BTN_TYPE_TEAM_KICK_OUT: on_kickout,
           BTN_TYPE_BLACK_LIST: on_blacklist,
           BTN_TYPE_DEL_BLACK_LIST: on_del_blacklist,
           BTN_TYPE_PLAYER_INF: on_detail_inf,
           BTN_TYPE_REPORT: on_report_user,
           BTN_TYPE_MOD_CLAN_TITLE: on_mod_clan_title,
           BTN_TYPE_CLAN_KICK: on_clan_kick,
           BTN_TYPE_CLAN: on_clan_invite,
           BTN_TYPE_FOLLOW: on_btn_follow,
           BTN_TYPE_UN_FOLLOW: on_btn_un_follow,
           BTN_TYPE_INTIMACY: on_btn_intimacy,
           BTN_TYPE_HOMELAND: on_btn_homeland
           }

    def set_position(self, wpos, anchor_point=None):
        if anchor_point:
            self.panel.nd_tips.setAnchorPoint(anchor_point)
        template_utils.set_node_position_in_screen(self.panel.nd_tips, self.panel, wpos, BORDER_INDENT=24, right_cut=130)

    def on_click_add_btn(self, btn, touch):
        if self._cur_uid == self._my_uid:
            return
        if self._message_data.is_black_friend(self._cur_uid):
            global_data.game_mgr.show_tip(get_text_by_id(10021), True)
        elif self._message_data.is_friend(self._cur_uid):
            pass
        else:
            global_data.player.req_add_friend(self._cur_uid)
        self.close()

    def on_click_bth_home(self, btn, touch):
        if BTN_TYPE_HOMELAND in self.btns_map:
            self.btns_map[BTN_TYPE_HOMELAND]()

    def close_history_ui(self):
        if self.need_close_history_ui:
            if not global_data.video_player.is_in_init_state():
                global_data.video_player.stop_video()
            for ui_name in HISTORY_UI_LIST:
                global_data.ui_mgr.close_ui(ui_name)

    def on_click_chat_btn(self, btn, touch):
        if self._cur_uid == self._my_uid:
            return
        if self._message_data.is_black_friend(self._cur_uid):
            global_data.game_mgr.show_tip(get_text_by_id(10021), True)
        else:
            global_data.ui_mgr.close_ui('FriendSearchList')
            self.close_history_ui()
            ui = global_data.ui_mgr.show_ui('MainFriend', 'logic.comsys.message')
            if self.player_inf:
                role_id = self.player_inf.get(ROLE_ID, const.DEFAULT_ROLE_ID)
                dan_info = self.player_inf.get('dan_info', {})
                ui.open_new_chat_dialog(self._cur_uid, self.player_inf[C_NAME], self.player_inf[U_LV], role_id, dan_info)
        self.close()

    def on_detail_inf(self, *args):
        global_data.ui_mgr.close_ui('FriendSearchList')
        ui = global_data.ui_mgr.get_ui('PlayerInfoUI')
        if ui:
            ui.clear_show_count_dict()
            ui.hide_main_ui()
        else:
            ui = global_data.ui_mgr.show_ui('PlayerInfoUI', 'logic.comsys.role')
        from logic.comsys.role.PlayerInfoUI import TAB_PLAYER_INFO, TAB_HISTORY_INFO
        ui.refresh_by_uid(self._cur_uid)
        if self.need_close_history_ui:
            if not global_data.video_player.is_in_init_state():
                global_data.video_player.stop_video()
            for ui_name in HISTORY_UI_LIST:
                global_data.ui_mgr.close_ui(ui_name)

            ui.jump_to_tab(TAB_PLAYER_INFO, self._cur_uid)
            ui.init_show_tab()
        self.close()

    def set_chat_source(self, uid, channel, chat_text):
        self._chat_source = {}
        uid = str(uid)
        self._chat_source[uid] = {}
        if channel:
            self._chat_source[uid]['channel'] = channel
        self._chat_source[uid].update({'chat': chat_text})