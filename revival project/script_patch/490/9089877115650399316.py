# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanJoinPageUI.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
from common.cfg import confmgr
from common.const.property_const import C_NAME, HEAD_FRAME, HEAD_PHOTO
from logic.comsys.clan.ClanPageBase import ClanPageBase
from logic.comsys.common_ui.InputBox import InputBox
from logic.gcommon.cdata import dan_data
from logic.gcommon.common_const.lang_data import code_2_showname
from logic.gcommon.common_utils.func_utils import check_is_int
from logic.gcommon.common_utils.local_text import get_cur_text_lang, LANG_CN
from logic.gcommon.const import CLICK_INTERVAL_TIME
from logic.gutils import template_utils
from logic.gutils.role_head_utils import set_role_head_frame, set_role_head_photo
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const import clan_const
from logic.gutils import clan_utils

class ClanJoinPageUI(ClanPageBase):

    def __init__(self, dlg):
        self.global_events = {'update_clan_recommend_lst': self._update_clan_info,
           'message_on_player_simple_inf': self._update_clan_commander
           }
        super(ClanJoinPageUI, self).__init__(dlg)

    def on_init_panel(self):
        super(ClanJoinPageUI, self).on_init_panel()
        self._init_params()
        self._init_ui_event()
        self._init_na_project()
        self._init_widget()
        self.panel.btn_change.OnClick(None)
        self.panel.nd_crew_details_show.setVisible(False)
        self._search_input = InputBox(self.panel.input_box, placeholder=800053, clear_btn_cb=self._clear_search_callback)
        self._search_input.set_rise_widget(self.panel)
        self.panel.PlayAnimation('show')
        return

    def _init_params(self):
        self._browsed_num = 0
        self._clan_info_lst = []
        self._refreshing = False
        self._last_select_item = None
        self._clan_commander_uid = None
        self._displaying_clan_id = None
        self._displaying_clan_name = ''
        self._displaying_clan_intro = ''
        self._clan_to_fid = {}
        if G_IS_NA_USER:
            self._lang_limit = get_cur_text_lang()
        else:
            self._lang_limit = LANG_CN
        return

    def _init_na_project(self):
        if not G_IS_NA_USER:
            level_pos_x, level_pos_y = self.panel.lab_limited_level.GetPosition()
            tier_pos_x, tier_pos_y = self.panel.lab_limited_tier.GetPosition()
            notice_pos_x, notice_pos_y = self.panel.nd_notice.GetPosition()
            self.panel.lab_limited_level.SetPosition(level_pos_x, level_pos_y + 41)
            self.panel.lab_limited_tier.setPosition(tier_pos_x, tier_pos_y + 41)
            self.panel.nd_notice.setPosition(notice_pos_x, notice_pos_y + 41)
            self.panel.lab_language.setVisible(False)

    def _init_widget(self):
        if G_IS_NA_USER:
            from .ClanLangSettingWidget import ClanLangSettingWidget
            self._lang_widget = ClanLangSettingWidget(self, self.panel.btn_language, get_cur_text_lang(), select_cb=self._select_lang_cb, reverse=True)
        else:
            self.panel.btn_language.setVisible(False)

    def _update_clan_info(self, clan_info_lst):
        self._refreshing = False
        if not clan_info_lst:
            self._browsed_num = 0
        self._clan_to_fid = global_data.message_data or {} if 1 else global_data.message_data.get_clan_friends_info()
        self._reset_details_display()
        self._clan_info_lst = sorted(clan_info_lst, key=cmp_to_key(--- This code section failed: ---

  90       0  LOAD_GLOBAL           0  'six_ex'
           3  LOAD_ATTR             1  'compare'
           6  LOAD_DEREF            0  'self'
           9  LOAD_ATTR             2  '_get_friend_num'
          12  LOAD_ATTR             1  'compare'
          15  BINARY_SUBSCR    
          16  CALL_FUNCTION_1       1 
          19  LOAD_DEREF            0  'self'
          22  LOAD_ATTR             2  '_get_friend_num'
          25  LOAD_FAST             1  'b'
          28  LOAD_CONST            1  'clan_id'
          31  BINARY_SUBSCR    
          32  CALL_FUNCTION_1       1 
          35  CALL_FUNCTION_2       2 
          38  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `CALL_FUNCTION_1' instruction at offset 16
), reverse=True)
        clan_len = len(self._clan_info_lst)
        self.panel.rank_list.SetInitCount(clan_len)
        if clan_len == 0:
            show = False if 1 else True
            self.panel.rank_list.setVisible(show)
            self.panel.lab_empty.setVisible(not show)
            self.panel.nd_crew_details_show.setVisible(show)
            return show or None
        else:
            day_no = tutil.get_rela_day_no()
            for idx, clan_info in enumerate(self._clan_info_lst):
                clan_name = clan_info['clan_name']
                clan_lv = clan_info['lv']
                clan_id = clan_info['clan_id']
                clan_member_num = clan_info['member_num']
                item = self.panel.rank_list.GetItem(idx)
                template_utils.update_badge_node(clan_info.get('badge', 0), item.temp_crew_logo)
                item.lab_name.setString(str(clan_name))
                item.lab_id.setString(str(clan_id))
                item.lab_rank.setString(str(clan_lv))
                item.img_tag_active.setVisible(clan_utils.is_active_clan(clan_info, day_no))
                max_member_num = confmgr.get('clan_lv_data', str(clan_lv), 'iMember')
                item.lab_total.setString('{0}/{1}'.format(clan_member_num, max_member_num))
                item.lab_friend_num.setString(str(self._get_friend_num(clan_id)))

                @item.callback()
                def OnClick(btn, touch, click_item=item, info=clan_info):
                    self._clan_commander_uid = info['commander_uid']
                    self._displaying_clan_id = info['clan_id']
                    self._displaying_clan_name = info['clan_name']
                    self._displaying_clan_intro = info['intro']
                    self._update_sel_state(click_item)
                    template_utils.update_badge_node(info.get('badge', 0), self.panel.temp_crew_logo)
                    self.panel.lab_id.setString('ID:{}'.format(info['clan_id']))
                    self.panel.lab_crew_name.setString(str(info['clan_name']))
                    player_inf = global_data.message_data.get_player_simple_inf(self._clan_commander_uid)
                    if player_inf:
                        commander_name = player_inf['char_name']
                        self.panel.lab_captian.setString(get_text_by_id(800027) + ':' + commander_name)
                    lang_limit = info.get('lang', -1)
                    dan_limit = info.get('apply_dan_limit', -1)
                    level_limit = info.get('apply_lv_limit', 0)
                    intro = info['intro']
                    if G_IS_NA_USER:
                        lang_name = code_2_showname.get(lang_limit, get_text_by_id(860016))
                        lang_font = confmgr.get('lang_conf', str(lang_limit), default={}).get('bShowFont', 'gui/fonts/fzdys.ttf')
                        text = get_text_by_id(800147) + '<fontname="%s">%s</fontname>' % (lang_font, lang_name)
                        self.panel.lab_language.SetStringWithAdapt(str(text))
                    text = get_text_by_id(800145)
                    my_level = global_data.player.get_lv()
                    color = '#SW'
                    if level_limit > 0:
                        text += 'Lv {}'.format(level_limit)
                        if my_level < level_limit:
                            color = '#SR'
                    else:
                        text += '#SW' + get_text_by_id(800065) + '#n'
                    text = color + text + '#n'
                    self.panel.lab_limited_level.SetStringWithAdapt(str(text))
                    color = '#SW'
                    text = get_text_by_id(800146)
                    my_dan = global_data.player.get_dan(dan_data.DAN_SURVIVAL)
                    dan_limit_name = dan_data.data.get(dan_limit, {}).get('name', 800065)
                    if dan_limit in dan_data.data and my_dan < dan_limit:
                        color = '#SR'
                    text = color + text + get_text_by_id(dan_limit_name) + '#n'
                    self.panel.lab_limited_tier.SetStringWithAdapt(str(text))
                    friend_lst = self._clan_to_fid.get(info['clan_id'], [])
                    self.panel.nd_notice.container.DeleteAllSubItem()
                    if intro or friend_lst:
                        self.panel.nd_notice.setVisible(True)
                        panel = global_data.uisystem.load_template_create('crew/i_crew_notice')
                        lab_notice_str = ''
                        if intro:
                            lab_notice_str = get_text_by_id(800023) + ':\n' + str(intro)
                        if friend_lst:
                            lab_notice_str += '\n' + get_text_by_id(800028)
                        panel.lab_notice.SetStringWithAdapt(lab_notice_str)
                        panel.Resize(panel.lab_notice.GetTextContentSize().width, panel.lab_notice.GetTextContentSize().height + 34)
                        self.panel.nd_notice.container.AddControl(panel, bRefresh=True)
                        for f_id in friend_lst:
                            my_friends = global_data.message_data.get_friends()
                            if f_id in my_friends:
                                f_item = self.panel.nd_notice.container.AddTemplateItem()
                                name = my_friends[f_id][C_NAME]
                                frame_no = my_friends[f_id][HEAD_FRAME]
                                photo_no = my_friends[f_id][HEAD_PHOTO]
                                f_item.lab_name.setString(name)
                                set_role_head_frame(f_item.temp_head, frame_no)
                                set_role_head_photo(f_item.temp_head, photo_no)

                    else:
                        self.panel.nd_notice.setVisible(False)
                    self._update_btn_apply_state(info['clan_id'])

            self.panel.rank_list.GetItem(0).OnClick(None)
            return

    def _get_friend_num(self, clan_id):
        if clan_id in self._clan_to_fid:
            return len(self._clan_to_fid)
        else:
            return 0

    def _update_sel_state(self, now_item):
        if self._last_select_item:
            self._last_select_item.img_bg_sel.setVisible(False)
        now_item.img_bg_sel.setVisible(True)
        self._last_select_item = now_item

    def _update_clan_commander(self, info):
        if info['uid'] == self._clan_commander_uid:
            commander_name = info['char_name']
            self.panel.lab_captian.setString(get_text_by_id(800027) + ':' + commander_name)

    def refresh_panel(self):
        super(ClanJoinPageUI, self).refresh_panel()

    def _reset_details_display(self):
        self._last_select_item = None
        self._clan_commander_uid = None
        self._displaying_clan_id = None
        self._displaying_clan_name = ''
        self._displaying_clan_intro = ''
        self.panel.rank_list.DeleteAllSubItem()
        return

    def _init_ui_event(self):

        @self.panel.btn_change.callback()
        def OnClick(*args):
            if self._refreshing:
                global_data.game_mgr.show_tip(get_text_by_id(15815), True)
                return
            self._refreshing = True
            self._browsed_num += len(self._clan_info_lst)
            self._search_clan(self._browsed_num)

        @self.panel.btn_apply_all.callback()
        def OnClick(*args):
            clan_id_lst = []
            for info in self._clan_info_lst:
                clan_id_lst.append(info['clan_id'])

            apply_window = global_data.ui_mgr.show_ui('ClanApplyJoinUI', 'logic.comsys.clan')
            apply_window.set_clan_id_list(clan_id_lst)

        self._search_time = 0

        @self.panel.btn_search.callback()
        def OnClick(*args):
            clan_name = self._search_input.get_text()
            if not clan_name:
                return
            import time
            now = time.time()
            interval = now - self._search_time
            if interval < CLICK_INTERVAL_TIME:
                notify_text = get_text_by_id(10039, {'time': int(CLICK_INTERVAL_TIME - interval) + 1})
                global_data.player.notify_client_message((notify_text,))
            self._search_time = now
            if check_is_int(clan_name):
                global_data.player and global_data.player.search_clan_by_cid(int(clan_name))
            else:
                global_data.player and global_data.player.search_clan_by_name(str(clan_name))

        @self.panel.btn_need_no_check.btn.callback()
        def OnClick(*args):
            need_approval = self.panel.btn_need_no_check.choose.IsVisible()
            self.panel.btn_need_no_check.choose.setVisible(not need_approval)
            self._reset_and_search()

        @self.panel.btn_meet_conditions.btn.callback()
        def OnClick(*args):
            need_condition = self.panel.btn_meet_conditions.choose.IsVisible()
            self.panel.btn_meet_conditions.choose.setVisible(not need_condition)
            self._reset_and_search()

        @self.panel.btn_apply.btn_common.callback()
        def OnClick(*args):
            if self._displaying_clan_id and global_data.player:
                apply_window = global_data.ui_mgr.show_ui('ClanApplyJoinUI', 'logic.comsys.clan')
                apply_window.set_clan_id_list([self._displaying_clan_id])
                apply_window.set_apply_cb(lambda : self.request_join_cb())

        @self.panel.btn_report.unique_callback()
        def OnClick(*args):
            self.on_click_btn_report()

    def _select_lang_cb(self):
        lang_limit = self._lang_widget.get_value()
        if lang_limit != self._lang_limit:
            self._lang_limit = lang_limit
            self._reset_and_search()

    def _reset_and_search(self):
        self._reset_details_display()
        self._browsed_num = 0
        self._search_clan(self._browsed_num)

    def request_join_cb(self):
        if not self.panel or not self.panel.isValid():
            return
        self._update_btn_apply_state(self._displaying_clan_id)

    def _update_btn_apply_state(self, clan_id):
        if global_data.player and global_data.player.has_requested_join(clan_id):
            apply_state = False
            text_id = 800033
        else:
            apply_state = True
            text_id = 800034
        if not self.panel or not self.panel.isValid():
            return
        self.panel.btn_apply.btn_common.SetShowEnable(apply_state)
        self.panel.btn_apply.btn_common.SetEnable(apply_state)
        self.panel.btn_apply.btn_common.SetText(get_text_by_id(text_id))

    def _clear_search_callback(self):
        self._browsed_num = 0
        self._search_clan(self._browsed_num)

    def _search_clan(self, skip):
        need_approval = self.panel.btn_need_no_check.choose.IsVisible()
        need_condition = self.panel.btn_meet_conditions.choose.IsVisible()
        apply_approval_limit = 0 if need_approval else 1
        my_dan_info = global_data.player or {} if 1 else global_data.player.get_dan_info_by_type('survival_dan')
        my_dan = my_dan_info.get('dan', dan_data.BROZE)
        apply_dan_limit = 99999 if not need_condition or global_data.player is None else my_dan
        apply_lv_limit = 99999 if not need_condition or global_data.player is None else global_data.player.get_lv()
        apply_active_limit = clan_utils.get_apply_active_limit()
        if global_data.player:
            global_data.player.search_clan_by_limit(apply_approval_limit, apply_dan_limit, apply_lv_limit, skip, lang_limit=self._lang_limit, active_limit=apply_active_limit)
        return

    def on_click_btn_report(self):
        from logic.gutils import jump_to_ui_utils
        clan_info = {'clan_id': self._displaying_clan_id,
           'clan_name': self._displaying_clan_name,
           'clan_intro': self._displaying_clan_intro
           }
        jump_to_ui_utils.jump_to_clan_report(clan_info)

    def on_finalize_panel(self):
        self.destroy_widget('_lang_widget')
        self._last_select_item = None
        super(ClanJoinPageUI, self).on_finalize_panel()
        return