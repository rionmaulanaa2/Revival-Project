# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/clan/ClanHomePage.py
from __future__ import absolute_import
from common import utilities
from logic.gutils import clan_utils
from logic.gutils import template_utils
from common.const.property_const import *
from logic.gcommon.common_const import chat_const
from logic.comsys.clan.ClanPageBase import ClanPageBase

class ClanHomePage(ClanPageBase):

    def __init__(self, dlg):
        self.global_events = {'clan_mod_name': self.update_name,
           'clan_mod_intro': self.update_intr,
           'chat_add_channel_msg': self.on_add_msg,
           'chat_close_end': self.on_close_chat,
           'clan_change_badge_suc': self._update_badge
           }
        super(ClanHomePage, self).__init__(dlg)

    def on_init_panel(self):
        super(ClanHomePage, self).on_init_panel()
        self._share_content = None
        self.init_widget(None)
        self.panel.PlayAnimation('show')
        return

    def on_finalize_panel(self):
        self.destroy_widget('_share_content')
        super(ClanHomePage, self).on_finalize_panel()

    def refresh_panel(self):
        super(ClanHomePage, self).refresh_panel()

    def update_name(self):
        self.panel.lab_name.SetString(global_data.player.get_clan_name())

    def update_intr(self):
        info = global_data.player.get_clan_info()
        self.panel.list_content.SetInitCount(1)
        text_item = self.panel.list_content.GetItem(0)
        text_item.lab_describe.SetString(info['intro'])
        text_item.lab_describe.formatText()
        sz = text_item.lab_describe.getTextContentSize()
        sz.height += 20
        text_item.setContentSize(sz)
        text_item.RecursionReConfPosition()
        self.panel.list_content.SetInnerContentSize(sz.width, sz.height)
        self.panel.list_content.GetContainer()._refreshItemPos()
        self.panel.list_content._refreshItemPos()

    def init_widget(self, _):
        info = global_data.player.get_clan_info()
        if not info:
            return

        @self.panel.btn_describe.unique_callback()
        def OnClick(btn, touch):
            ui = global_data.ui_mgr.show_ui('AnnouncementUI', 'logic.comsys.announcement')
            if ui:
                ui.show_content(800001, get_text_by_id(800052))

        @self.panel.bth_setting.unique_callback()
        def OnClick(btn, touch):
            global_data.ui_mgr.show_ui('ClanSettingUI', 'logic.comsys.clan')

        clan_utils.set_permission('setup_permission_titles', self.panel.bth_setting, set_visible=True)

        @self.panel.btn_copy.unique_callback()
        def OnClick(btn, touch):
            import game3d
            clan_id = global_data.player.get_clan_id()
            game3d.set_clipboard_text(str(clan_id))
            global_data.game_mgr.show_tip(get_text_by_id(800095).format(clan_id))

        @self.panel.bth_share.unique_callback()
        def OnClick(*args):
            if not global_data.player or not global_data.player.is_in_clan():
                return
            else:
                clan_id = global_data.player.get_clan_id()
                from logic.comsys.share.ShareUI import ShareUI
                share_ui = ShareUI(parent=self.panel)

                def get_chat_data():
                    if not self._share_content:
                        return None
                    else:
                        clan_info, clan_commander_info = self._share_content.get_share_info()
                        if not clan_info or not clan_commander_info:
                            return None
                        extra_data = {'type': chat_const.MSG_TYPE_CLAN_CARD,'clan_id': clan_info.get('clan_id', -1),
                           'clan_lv': clan_info.get('lv', 1),
                           'clan_member_num': clan_info.get('member_num', 0),
                           'clan_name': clan_info.get('clan_name', ''),
                           'badge': clan_info.get('badge', 0)
                           }
                        return extra_data

                def on_click_chat_btn(*args):
                    extra_data = get_chat_data()
                    if extra_data is None:
                        return
                    else:
                        share_ui.close()
                        self.show_main_chat(True, chat_const.CHAT_WORLD)
                        global_data.player.send_msg(chat_const.CHAT_WORLD, '', extra=extra_data)
                        return

                def on_click_friend(f_data):
                    from logic.comsys.message.MainFriend import FRIEND_TAB_RELATIONSHIP
                    extra_data = get_chat_data()
                    if extra_data is None:
                        return
                    else:
                        share_ui.close()

                        def ui_init_finish_cb():
                            sub_panel = ui.touch_tab_by_index(0)
                            sub_panel.click_uid_button(f_data[U_ID])
                            global_data.message_data.recv_to_friend_msg(f_data[U_ID], f_data[C_NAME], '', f_data[U_LV], extra=extra_data)
                            global_data.player.req_friend_msg(f_data[U_ID], f_data[U_LV], f_data.get(CLAN_ID, -1), '', extra=extra_data)

                        ui = global_data.ui_mgr.get_ui('MainFriend')
                        if ui:
                            ui_init_finish_cb()
                            return
                        ui = global_data.ui_mgr.show_ui('MainFriend', 'logic.comsys.message')
                        ui.set_ui_init_finish_cb(FRIEND_TAB_RELATIONSHIP, ui_init_finish_cb)
                        return

                def on_click_friend_btn(*args):
                    share_ui.on_click_friend_btn(on_click_friend)

                btn_infos = [{'template_name': 'common/i_common_button_2','click_cb': on_click_friend_btn,'btn_name': 'btn_common','btn_text': 10259}, {'template_name': 'common/i_common_button_2','click_cb': on_click_chat_btn,'btn_name': 'btn_common','btn_text': 800150}]

                def init_cb():
                    if share_ui and share_ui.is_valid():
                        share_ui.add_custom_button(btn_infos, is_head=True)
                        share_ui.set_share_content_raw(self._share_content.get_show_render_texture(), 'pnl_share_crew', True, share_content=self._share_content)
                        share_ui.set_save_content(self._share_content.get_save_render_texture())

                if not self._share_content:
                    from logic.comsys.share.ClanShareCreator import ClanShareCreator
                    share_creator = ClanShareCreator()
                    share_creator.create(clan_id, init_cb=init_cb, parent=None)
                    self._share_content = share_creator
                else:
                    init_cb()
                return

        @self.panel.btn_report.unique_callback()
        def OnClick(*args):
            self.on_click_report_btn()

        @self.panel.btn_rename.unique_callback()
        def OnClick(btn, touch):
            from logic.gcommon.item.item_const import ITEM_NO_CLAN_CHANGE_NAME
            if not global_data.player:
                return
            clan_ticket_num = global_data.player.get_item_money(ITEM_NO_CLAN_CHANGE_NAME)
            if clan_ticket_num <= 0:
                from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
                from logic.client.const.mall_const import CLAN_CHANGE_NAME_GOODS_ID

                def call_back():
                    groceries_buy_confirmUI(CLAN_CHANGE_NAME_GOODS_ID)

                SecondConfirmDlg2().confirm(content=800132, confirm_callback=call_back)
            else:
                from logic.gutils import jump_to_ui_utils
                jump_to_ui_utils.jump_to_clan_change_name()

        clan_utils.set_permission('name_permission_titles', self.panel.btn_rename, set_visible=True)

        @self.panel.btn_notice_edit.unique_callback()
        def OnClick(btn, touch):
            global_data.ui_mgr.show_ui('ClanAnnounceUI', 'logic.comsys.clan')

        self.update_intr()
        clan_utils.set_permission('setup_permission_titles', self.panel.btn_notice_edit, set_visible=True)
        self.panel.lab_name.SetString(global_data.player.get_clan_name())
        self.panel.lab_id.SetString('ID: {}'.format(global_data.player.get_clan_id()))
        lv = global_data.player.get_clan_lv()
        self.panel.lab_level.SetString('Lv{}'.format(lv))
        self._update_badge()
        cur_exp = info['history_point']
        total_exp = clan_utils.get_clan_lv_exp(lv)
        self.panel.progress_exp.SetPercent(utilities.safe_percent(cur_exp, total_exp))
        if total_exp <= 0:
            self.panel.lab_task_progress.SetString(get_text_by_id(800096))
        else:
            self.panel.lab_task_progress.SetString('{0}/{1}'.format(cur_exp, total_exp))
        cur_count = len(global_data.player.get_clan_member_list())
        total_count = clan_utils.get_clan_person_limit(lv)
        self.panel.number.SetString(get_text_by_id(19313, (cur_count, total_count)))
        self.panel.lab_rank_one.SetString('{}'.format(info['week_point']))
        self.panel.lab_rank_two.SetString('{}'.format(clan_utils.get_my_clan_info_by_field('week_point')))
        self.panel.lab_rank_three.SetString('{}'.format(info['season_point']))
        self.panel.lab_rank_four.SetString('{}'.format(clan_utils.get_my_clan_info_by_field('season_point')))
        self.show_chat()

    def on_close_chat(self):
        ui = global_data.ui_mgr.get_ui('MainChat')
        if ui:
            ui.do_hide_panel()

    def show_main_chat(self, flag=None, channel=chat_const.CHAT_CLAN):
        ui = global_data.ui_mgr.get_ui('MainChat')
        if not ui:
            return
        else:
            is_chat_open = ui.is_chat_open()
            if flag == is_chat_open:
                return
            if flag == None:
                flag = not is_chat_open
            if flag:
                ui.do_show_panel()
                ui.chat_open()
                ui.touch_channel_btn(channel)
            else:
                ui.chat_close()
            return

    def show_chat(self):
        chat_tmpl = self.panel.chat_frames.GetItem(0)
        msg_list = global_data.message_data.get_channel_msg(chat_const.CHAT_CLAN)

        @chat_tmpl.unique_callback()
        def OnClick(btn, event):
            self.show_main_chat()

        @self.panel.centrre.unique_callback()
        def OnClick(btn, event):
            self.show_main_chat(flag=False)

        count = len(msg_list)
        if count > 0:
            data = msg_list[count - 1]
            self.on_add_msg(False, chat_const.CHAT_CLAN, data)
        else:
            chat_tmpl.lab_msg.SetString(800055)

    def on_add_msg(self, is_msg_move, channel, data):
        from logic.comsys.message import message_data
        from logic.gcommon.common_utils.local_text import get_server_text
        if channel != chat_const.CHAT_CLAN or not self.panel:
            return
        chat_tmpl = self.panel.chat_frames.GetItem(0)
        msg_color = message_data.CHANNEL_COLOR[data['chnl']]
        channel_name = message_data.get_channel_name_by_chid(data['chnl'])
        if 'sender_info' in data and data['sender_info'] and 'notify_type' not in data['sender_info']:
            name = data['sender_info'][C_NAME]
        else:
            name = ''
        htmltext = '<color=%s>[%s]%s:%s</color>' % (msg_color, channel_name, name, get_server_text(data['msg']))
        chat_tmpl.lab_msg.SetString(htmltext)

    def _update_badge(self, *args):
        info = global_data.player.get_clan_info()
        template_utils.update_badge_node(info.get('badge', 0), self.panel.temp_crew_logo)

    def on_click_report_btn(self, *args):
        from logic.gutils import jump_to_ui_utils
        clan_info = global_data.player.get_clan_info()
        if not clan_info:
            return
        jump_to_ui_utils.jump_to_clan_report({'clan_id': clan_info.get('clan_id', -1),
           'clan_name': clan_info.get('clan_name', ''),
           'clan_intro': clan_info.get('intro', '')
           })