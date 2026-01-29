# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/MainEmail.py
from __future__ import absolute_import
import six_ex
import six
from functools import cmp_to_key
from common.uisys.basepanel import BasePanel
import time
import common.uisys.richtext
from cocosui import cc, ccui, ccs
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.const.property_const import *
import common.utilities
from logic.gcommon import const
from common.uisys.color_table import get_color_val
from common.uisys.uielment.CCRichText import CCRichText
from logic.gcommon.common_const import mail_const
from logic.gcommon.common_utils.local_text import get_text_by_id, get_server_text
from common.utils.cocos_utils import ccc4FromHex, ccp, CCRect, CCSizeZero, CCSize
from logic.gutils.item_utils import init_lobby_bag_item, get_item_pic_by_item_no, get_lobby_item_pic_by_item_no
from logic.comsys.chat import chat_link
from logic.comsys.common_ui.WindowBigBase import WindowBigBase
from logic.gutils.version_utils import get_integer_script_version, get_integer_engine_version
from logic.gcommon.cdata.privilege_data import COLOR_NAME
from logic.gutils.lobby_click_interval_utils import check_click_interval
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
email_read_pic_path = 'gui/ui_res_2/message/mail_icon_2.png'
TAB_LIST = [
 mail_const.MAIL_TAG_SYS, mail_const.MAIL_TAG_CREDIT, mail_const.MAIL_TAG_FRIEND]
TAB_MAP = {mail_const.MAIL_TAG_SYS: {'tab_name': 3202,'redpoint_id': '6'},mail_const.MAIL_TAG_CREDIT: {'tab_name': 3201,'redpoint_id': '6'},mail_const.MAIL_TAG_FRIEND: {'tab_name': 3203,'redpoint_id': '6'}}

class MainEmail(WindowBigBase):
    PANEL_CONFIG_NAME = 'mail/mail_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'temp_content.temp_get_all_reward.btn_common.OnClick': 'on_all_reward_btn',
       'temp_content.temp_all_del.btn_common.OnClick': 'on_all_del_btn',
       'temp_content.temp_all_read.btn_common.OnClick': 'on_all_read_btn',
       'temp_content.temp_get_reward.btn_common.OnClick': 'on_reward_btn',
       'temp_content.temp_delete.btn_common.OnClick': 'on_delete_btn'
       }

    def on_init_panel(self, *args, **kargs):
        super(MainEmail, self).on_init_panel(*args, **kargs)
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)
        self._message_data = global_data.message_data
        if not self._message_data:
            return
        else:
            self._email_datas = []
            self._cur_email_id = None
            self._cur_tab_index = None
            self._tab_panels = {}
            self._del_email_time = {}
            temp_content = self.panel.nd_content.temp_content
            self._msg_width = temp_content.list_content.getContentSize().width
            self._lv_email = temp_content.nd_mail.nd_list.list_mail
            self._lv_email.DeleteAllSubItem()
            self.script_ver = get_integer_script_version()
            self.engine_ver = get_integer_engine_version()
            self.process_event(True)
            self.init_handle()
            self.init_tab()
            self.hide_main_ui()
            return

    def on_finalize_panel(self):
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'message_refresh_email_list': self.refresh_sys_email,
           'message_get_reward': self.on_get_reward,
           'message_del_email': self.on_del_email,
           'message_read_email': self.on_email_read,
           'message_on_friend_gold_gift': self.refresh_email_list,
           'message_recv_friend_gold_gift': self.refresh_sys_email
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_tab(self):
        list_tab = self.panel.temp_bg.nd_window.nd_left_tab.list_tab
        list_tab.DeleteAllSubItem()
        self._sview_data_index = -1
        for i, key in enumerate(TAB_LIST):
            tab_info = TAB_MAP[key]
            panel = list_tab.AddTemplateItem()
            panel.btn_window_tab.SetText(get_text_by_id(tab_info['tab_name']), color1='#DD', color2='#SW', color3='#SW')
            panel.btn_window_tab.SetSelect(False)
            self.add_touch_tab(panel, key)
            redpoint_id = tab_info.get('redpoint_id', 0)
            if redpoint_id:
                global_data.redpoint_mgr.register_redpoint(panel.img_hint, redpoint_id, tag=key)

        self.touch_tab_by_index(mail_const.MAIL_TAG_SYS)
        self._is_check_sview = False

        def scroll_callback(sender, eventType):
            if self._is_check_sview == False:
                self._is_check_sview = True
                self.SetTimeOut(0.021, self.check_sview)

        self._lv_email.addEventListener(scroll_callback)
        self.refresh_sys_email()

    def __get_can_del_mail_ids(self, limit=mail_const.MAIL_MAX_CNT):
        email_ids = []
        for email_data in self._email_datas:
            mail_id = email_data[mail_const.MAIL_ID]
            if type(mail_id) == str and mail_id.startswith('gold_'):
                continue
            state = email_data[mail_const.MAIL_STATE]
            if email_data.get(mail_const.MAIL_ATTACHMENT, None):
                if state == mail_const.MAIL_STATE_REWARD_GET:
                    email_ids.append(mail_id)
            elif state == mail_const.MAIL_STATE_READ:
                email_ids.append(mail_id)
            if len(email_ids) >= limit:
                break

        return email_ids

    def __del_all_mails(self):
        if not global_data.player:
            return
        email_ids = self.__get_can_del_mail_ids(mail_const.MAIL_ALL_DEL_MAX_CNT)
        if email_ids:
            global_data.player.req_del_more_mail(email_ids)

    @check_click_interval()
    def on_all_del_btn(self, *args):
        sec_confirm_dlg = SecondConfirmDlg2()
        sec_confirm_dlg.confirm(content=611631, confirm_callback=self.__del_all_mails)

    @check_click_interval()
    def on_all_reward_btn(self, *args):
        if not global_data.player:
            return
        script_ver = self.script_ver
        engine_ver = self.engine_ver
        player_lv = global_data.player.get_lv()
        email_ids = []
        for email_data in self._email_datas:
            state = email_data[mail_const.MAIL_STATE]
            if state != mail_const.MAIL_STATE_REWARD_GET and email_data.get(mail_const.MAIL_ATTACHMENT, []) and email_data.get(mail_const.MAIL_RECEIVE_LV, 0) <= player_lv and email_data.get(mail_const.MAIL_RECEIVE_LVER, 0) <= script_ver and email_data.get(mail_const.MAIL_RECEIVE_EVER, 0) <= engine_ver:
                email_ids.append(email_data[mail_const.MAIL_ID])

        if email_ids:
            global_data.player.req_get_reward(email_ids)
        if self._cur_tab_index == mail_const.MAIL_TAG_FRIEND:
            global_data.player.request_receive_all_friend_gold_gift()

    @check_click_interval()
    def on_all_read_btn(self, *args):
        email_ids = []
        for email_data in self._email_datas:
            state = email_data[mail_const.MAIL_STATE]
            if state == mail_const.MAIL_STATE_UNREAD:
                email_ids.append(email_data[mail_const.MAIL_ID])

        if email_ids:
            self._message_data.set_email_read(email_ids)
            global_data.player.notify_client_message((get_text_by_id(11054),))

    @check_click_interval()
    def on_reward_btn(self, *args):
        if self._cur_email_id:
            if type(self._cur_email_id) == str and self._cur_email_id.startswith('gold_'):
                uid = int(self._cur_email_id.replace('gold_', ''))
                global_data.player.request_receive_friend_gold_gift(uid)
            else:
                global_data.player.req_get_reward([self._cur_email_id])

    @check_click_interval()
    def on_delete_btn(self, *args):
        if self._cur_email_id:
            if type(self._cur_email_id) == str and self._cur_email_id.startswith('gold_'):
                return
            last_del_time = self._del_email_time.get(self._cur_email_id, None)
            if last_del_time == None or time.time() - last_del_time > 3.0:
                self._del_email_time[self._cur_email_id] = time.time()
                global_data.player.req_del_email(self._cur_email_id)
        return

    def init_handle(self):
        self.handle_dict = {mail_const.MAIL_TAG_SYS: self.set_system_email_state,mail_const.MAIL_TAG_CREDIT: self.set_credit_email_state,
           mail_const.MAIL_TAG_FRIEND: self.set_friend_email_state
           }

    def refresh_quick_btn(self):
        if self._message_data.is_unget_reward_email(tag=self._cur_tab_index):
            self.panel.temp_content.temp_get_all_reward.setVisible(True)
            self.panel.temp_content.temp_all_read.setVisible(False)
            self.panel.temp_content.temp_all_del.setVisible(False)
        else:
            self.panel.temp_content.temp_get_all_reward.setVisible(False)
            unread_count, _ = self._message_data.get_email_count_inf(tag=self._cur_tab_index)
            if bool(unread_count):
                self.panel.temp_content.temp_all_del.setVisible(False)
                self.panel.temp_content.temp_all_read.setVisible(True)
            else:
                self.panel.temp_content.temp_all_read.setVisible(False)
                mail_ids = self.__get_can_del_mail_ids(mail_const.MAIL_ALL_DEL_MIN_CNT)
                if len(mail_ids) >= mail_const.MAIL_ALL_DEL_MIN_CNT:
                    self.panel.temp_content.temp_all_del.setVisible(True)
                else:
                    self.panel.temp_content.temp_all_del.setVisible(False)

    def refresh_right(self):
        temp_content = self.panel.nd_content.temp_content
        temp_content.nd_mail.nd_content.setVisible(False)
        temp_content.nd_mail.nd_empty.setVisible(True)

    def on_del_email(self, email_id):
        if self._email_datas:
            for email_data in self._email_datas:
                cur_mail_id = email_data[mail_const.MAIL_ID]
                if isinstance(cur_mail_id, six.string_types) or isinstance(cur_mail_id, int) and isinstance(email_id, int) and cur_mail_id > email_id:
                    next_open_email_id = email_data[mail_const.MAIL_ID]
                    break
            else:
                next_open_email_id = self._email_datas[0][mail_const.MAIL_ID]

            self.refresh_email_inf(next_open_email_id)
            self.refresh_email_choose()
        else:
            self.panel.temp_content.nd_content.setVisible(False)
        self.refresh_quick_btn()

    def on_get_reward(self, email_ids):
        if self._cur_email_id in email_ids:
            self.refresh_email_inf(self._cur_email_id, True)
        for email_item in self._lv_email.GetAllItem():
            if email_item.email_id in email_ids:
                email_item.img_mail.SetDisplayFrameByPath('', email_read_pic_path)
                email_item.nd_reward.setVisible(False)
                data = self._message_data.get_email_by_id(email_item.email_id)
                if self.is_item_red_point(data):
                    email_item.red_dot_1.setVisible(True)
                else:
                    email_item.red_dot_1.setVisible(False)
                    if email_item.email_id != self._cur_email_id:
                        email_item.btn_item.SetShowEnable(False)

        self.refresh_quick_btn()

    def add_touch_tab(self, panel, index):
        self._tab_panels[index] = panel
        panel.btn_window_tab.EnableCustomState(True)

        @panel.btn_window_tab.callback()
        def OnClick(*args):
            self.touch_tab_by_index(index)

        unread_count, _ = self._message_data.get_email_count_inf(tag=index)
        panel.img_hint.setVisible(bool(unread_count))

    def touch_tab_by_index(self, index):
        if self._cur_tab_index == index:
            return
        else:
            if self._cur_tab_index != None:
                tab_panel = self._tab_panels.get(self._cur_tab_index)
                tab_panel.btn_window_tab.SetSelect(False)
                tab_panel.StopAnimation('continue')
                tab_panel.RecoverAnimationNodeState('continue')
            tab_panel = self._tab_panels.get(index)
            tab_panel.btn_window_tab.SetSelect(True)
            tab_panel.RecordAnimationNodeState('continue')
            tab_panel.PlayAnimation('continue')
            if index != self._cur_tab_index:
                self._cur_tab_index = index
                tab_panel.PlayAnimation('click')
            self.refresh_sys_email()
            return

    def refresh_email_list(self):
        self._lv_email.DeleteAllSubItem()

        def sort_mail(x, y):
            x_st = x[mail_const.MAIL_STATE]
            if x_st > 0:
                x_st = 1
            x_sendtime = x[mail_const.MAIL_SENDTIME]
            y_st = y[mail_const.MAIL_STATE]
            if y_st > 0:
                y_st = 1
            y_sendtime = y[mail_const.MAIL_SENDTIME]
            if x_st < y_st:
                return -1
            else:
                if x_st > y_st:
                    return 1
                if x_sendtime < y_sendtime:
                    return 1
                return -1

        self._email_datas = sorted(six_ex.values(global_data.message_data.get_sys_email_by_tag(tag=self._cur_tab_index)), key=cmp_to_key(sort_mail))
        data_count = len(self._email_datas)
        sview_height = self._lv_email.getContentSize().height
        self._sview_data_index = 0
        all_height = 0
        index = 0
        while all_height < sview_height - 10 and index < data_count:
            data = self._email_datas[index]
            chat_pnl = self.add_email_elem(data, True)
            all_height += chat_pnl.getContentSize().height
            index += 1

        self._sview_data_index = index - 1
        self._lv_email.ScrollToTop()
        temp_content = self.panel.nd_content.temp_content
        nd_empty = temp_content.nd_mail.nd_empty
        nd_empty.setVisible(not temp_content.nd_mail.nd_content.isVisible())
        self.panel.nd_content.temp_content.nd_mail.nd_list.list_empty.setVisible(not bool(self._email_datas))
        if data_count > 0:
            nd_empty.lab_empty.SetString(11038)
        else:
            nd_empty.lab_empty.SetString(80091)
        self.refresh_quick_btn()

    def refresh_sys_email(self):
        self._cur_email_id = None
        self.refresh_right()
        self.refresh_email_list()
        return

    def on_email_read(self, email_ids):
        for email_item in self._lv_email.GetAllItem():
            if email_item.email_id in email_ids:
                email_item.img_mail.SetDisplayFrameByPath('', email_read_pic_path)
                data = self._message_data.get_email_by_id(email_item.email_id)
                if self.is_item_red_point(data):
                    email_item.red_dot_1.setVisible(True)
                    email_item.lab_read.setVisible(False)
                    email_item.btn_item.SetSelect(False)
                else:
                    email_item.red_dot_1.setVisible(False)
                    email_item.lab_read.setVisible(False)
                    email_item.btn_item.SetShowEnable(False)
                if email_item.email_id == self._cur_email_id:
                    email_item.btn_item.SetSelect(True)

        self.refresh_quick_btn()

    def add_email_elem(self, data, is_back_item=True, index=-1):
        if is_back_item:
            email_item = self._lv_email.AddTemplateItem(bRefresh=True)
        else:
            email_item = self._lv_email.AddTemplateItem(0, bRefresh=True)
        email_item.btn_item.SetEnableCascadeOpacityRecursion(True)
        email_item.email_id = data[mail_const.MAIL_ID]
        if data[mail_const.MAIL_STATE] != mail_const.MAIL_STATE_UNREAD:
            email_item.img_mail.SetDisplayFrameByPath('', email_read_pic_path)
        if self.is_item_red_point(data):
            email_item.red_dot_1.setVisible(True)
            email_item.lab_read.setVisible(False)
            email_item.btn_item.SetSelect(False)
        else:
            email_item.red_dot_1.setVisible(False)
            email_item.lab_read.setVisible(False)
            email_item.btn_item.SetShowEnable(False)
        email_item.nd_reward.setVisible(self.is_unget_reward(data))
        title = get_server_text(data.get(mail_const.MAIL_TITLE, None))
        if title:
            title = common.utilities.cut_string_by_len(title, 12, '...')
            email_item.lab_name.setString(title)
        send_time = data.get(mail_const.MAIL_SENDTIME, None)
        if send_time:
            t = time.localtime(send_time)
            t_str = '%02d-%02d %02d:%02d' % (t[1], t[2], t[3], t[4])
            email_item.lab_time.setString(t_str)
        tab_index = TAB_LIST[self._cur_tab_index]
        self.handle_dict[tab_index](email_item, data)
        return email_item

    def refresh_content_scroll(self, list_content):
        is_bottom = [
         True]
        img_arrow = self.panel.nd_content.temp_content.img_arrow
        out_height = list_content.getContentSize().height
        inner_height = list_content.getInnerContainerSize().height

        def OnScrolling():
            if inner_height <= out_height:
                img_arrow.setVisible(False)
                return
            if is_bottom[0]:
                img_arrow.setVisible(True)
                is_bottom[0] = False

        def OnScrollToBottom():
            if inner_height <= out_height:
                img_arrow.setVisible(False)
                return
            if not is_bottom[0]:
                img_arrow.setVisible(False)
                is_bottom[0] = True

        list_content.OnScrollToBottom = OnScrollToBottom
        list_content.OnScrolling = OnScrolling
        OnScrolling()
        posx = list_content.getPositionX()
        posy = list_content.getPositionY()
        img_arrow.SetPosition(posx, posy - 0.5 * out_height + 5)

    def _get_mail_content(self, data):
        if type(data) is dict and 'mail_type' in data:
            if data['mail_type'] == 'credit':
                print (
                 '###### ', data)
                content = ''
                if global_data.player.uid == data['credit_uid']:
                    content += get_text_by_id(900035, data)
                    content += '\n'
                    if data.get('forbidden_match', 0) > 0:
                        content += get_text_by_id(900041, data)
                    else:
                        content += get_text_by_id(900040, data)
                else:
                    content += get_text_by_id(900034, data)
                    content += '\n'
                    report_list = data.get('be_report_list', [])
                    if global_data.player.uid in report_list:
                        if data.get('forbidden_match', 0) > 0:
                            content += get_text_by_id(900039, data)
                        else:
                            content += get_text_by_id(900038, data)
                    elif data.get('forbidden_match', 0) > 0:
                        content += get_text_by_id(900037, data)
                    else:
                        content += get_text_by_id(900036, data)
                    forbid_text = ''
                    if data.get('forbid_battle_type', 0):
                        forbid_text += '\n'
                        forbid_text += '    ' + get_text_by_id(data['forbid_battle_type'])
                    if data.get('forbid_credit_reward', False):
                        forbid_text += '\n'
                        forbid_text += '    ' + get_text_by_id(900046)
                    if data.get('forbid_compensation', False):
                        forbid_text += '\n'
                        forbid_text += '    ' + get_text_by_id(900047)
                    if data.get('reduce_exp', False):
                        forbid_text += '\n'
                        forbid_text += '    ' + get_text_by_id(900048)
                    if forbid_text:
                        content += '\n'
                        content += get_text_by_id(900042)
                        content += forbid_text
                    content += '\n'
                    if global_data.player.uid in report_list:
                        content += get_text_by_id(900050)
                    else:
                        content += get_text_by_id(900049)
                    content += '\n'
                    content += get_text_by_id(900051)
                return content
        else:
            return get_server_text(data)

    def refresh_email_inf(self, email_id, refresh_force=False):
        self._message_data.set_email_read([email_id])
        if self._cur_email_id == email_id and refresh_force == False:
            return
        self._cur_email_id = email_id
        temp_content = self.panel.temp_content
        temp_content.nd_content.setVisible(True)
        temp_content.nd_empty.setVisible(False)
        data = self._message_data.get_email_by_id(email_id)
        title = get_server_text(data.get(mail_const.MAIL_TITLE, ''))
        temp_content.lab_mail_name.setString(title)
        send_time = data.get(mail_const.MAIL_SENDTIME, '')
        t = time.localtime(send_time)
        t_str = get_text_by_id(2147) + ':%04d-%02d-%02d %02d:%02d' % (t[0], t[1], t[2], t[3], t[4])
        temp_content.lab_mail_time.setString(t_str)
        if type(self._cur_email_id) == str and self._cur_email_id.startswith('gold_'):
            temp_content.lab_mail_sender.SetString(title)
            temp_content.temp_get_reward.btn_common.SetText(3211)
        else:
            temp_content.lab_mail_sender.SetString(11040)
            temp_content.temp_get_reward.btn_common.SetText(80248)
        attachment_list = data.get(mail_const.MAIL_ATTACHMENT, [])
        if attachment_list:
            list_content = self.panel.nd_content.temp_content.list_content
            self.panel.nd_content.temp_content.list_content_no_reward.setVisible(False)
        else:
            list_content = self.panel.nd_content.temp_content.list_content_no_reward
            self.panel.nd_content.temp_content.list_content.setVisible(False)
        list_content.setVisible(True)
        list_content.DeleteAllSubItem()
        content = self._get_mail_content(data.get(mail_const.MAIL_CONTENT, ''))
        content = chat_link.linkstr_to_richtext(content)
        content = content.replace('<br/>', '\n')
        panel = list_content.AddTemplateItem()
        color4b = ccc4FromHex(get_color_val('#BC'))

        def touch_callback(msg, element, touch, eventTouch):
            import ccui
            if type(element) not in [ccui.RichElementCustomNode]:
                chat_link.link_touch_callback(msg)
            else:
                from logic.gutils.rich_text_utils import on_custom_chat_link
                on_custom_chat_link(msg, element, touch, eventTouch)

        rt_msg = CCRichText.Create(content, 20, cc.Size(self._msg_width - 15, 0), color4b=color4b, callback=touch_callback)
        rt_msg.setAnchorPoint(cc.Vec2(0.0, 1.0))
        rt_msg.setHorizontalAlign(0)
        rt_msg.formatText()
        size = rt_msg.getVirtualRendererSize()
        rt_msg.setPosition(cc.Vec2(0, size.height))
        panel.setContentSize(cc.Size(self._msg_width, size.height))
        panel.AddChild('msg', rt_msg)
        list_content._container._refreshItemPos()
        list_content._refreshItemPos()
        if attachment_list:
            temp_content.nd_reward.setVisible(True)
            is_get = data[mail_const.MAIL_STATE] == mail_const.MAIL_STATE_REWARD_GET
            temp_content.lv_award.DeleteAllSubItem()
            for item_data in attachment_list:
                item_panel = temp_content.lv_award.AddTemplateItem(bRefresh=True)
                item_data['item_no'] = item_data.get('item_no', item_data['type'])
                item_data['quantity'] = item_data.get('quantity', item_data['cnt'])
                item_data['is_get'] = is_get
                item_data['touch_show_desc'] = True
                init_lobby_bag_item(item_panel, item_data)

        else:
            temp_content.nd_reward.setVisible(False)
        script_ver = self.script_ver
        engine_ver = self.engine_ver
        if attachment_list and data[mail_const.MAIL_STATE] != mail_const.MAIL_STATE_REWARD_GET:
            temp_content.temp_delete.setVisible(False)
            rec_lv = data.get(mail_const.MAIL_RECEIVE_LV, 0)
            email_script_ver = data.get(mail_const.MAIL_RECEIVE_LVER, 0)
            email_engine_ver = data.get(mail_const.MAIL_RECEIVE_EVER, 0)
            if rec_lv <= global_data.player.get_lv() and email_script_ver <= script_ver and email_engine_ver <= engine_ver:
                temp_content.temp_get_reward.setVisible(True)
                temp_content.lab_limit.setVisible(False)
            else:
                temp_content.temp_get_reward.setVisible(False)
                if rec_lv > global_data.player.get_lv():
                    temp_content.lab_limit.SetString(get_text_by_id(11104, (rec_lv,)))
                elif email_script_ver > script_ver:
                    temp_content.lab_limit.SetString(get_text_by_id(609151))
                else:
                    temp_content.lab_limit.SetString(get_text_by_id(609141))
                temp_content.lab_limit.setVisible(True)
        else:
            temp_content.temp_get_reward.setVisible(False)
            temp_content.temp_delete.setVisible(True)
            temp_content.lab_limit.setVisible(False)
        self.refresh_content_scroll(list_content)

    def refresh_email_choose(self):
        for email_item in self._lv_email.GetAllItem():
            if email_item.email_id == self._cur_email_id:
                email_item.btn_item.SetSelect(True)
                email_item.lab_name.SetColor('#SW')
                email_item.lab_time.SetColor('#SW')
                email_item.lab_read.SetColor('#SW')
            else:
                if email_item.red_dot_1.isVisible():
                    email_item.btn_item.SetSelect(False)
                else:
                    email_item.btn_item.SetShowEnable(False)
                email_item.lab_name.SetColor('#BC')
                email_item.lab_time.SetColor('#BC')
                email_item.lab_read.SetColor('#BC')

    def refresh_friend_choose(self):
        for email_item in self._lv_email.GetAllItem():
            if email_item.email_id == self._cur_email_id:
                email_item.btn_item.SetSelect(True)
                email_item.lab_name.SetColor('#SW')
                email_item.lab_time.SetColor('#SW')
                email_item.lab_read.SetColor('#SW')
            else:
                if email_item.red_dot_1.isVisible():
                    email_item.btn_item.SetSelect(False)
                else:
                    email_item.btn_item.SetShowEnable(False)
                if isinstance(email_item.email_id, str) and email_item.email_id.startswith('gold_'):
                    uid = int(email_item.email_id.replace('gold_', ''))
                    friend_info = global_data.message_data.get_player_detail_inf(uid)
                else:
                    friend_info = None
                if friend_info:
                    priv_settings = friend_info.get('priv_settings', {})
                    priv_purple_id = friend_info.get('priv_purple_id', False)
                    if priv_purple_id and priv_settings.get(const.PRIV_SHOW_PURPLE_ID, False):
                        email_item.lab_name.SetColor(COLOR_NAME)
                    else:
                        email_item.lab_name.SetColor('#BC')
                else:
                    email_item.lab_name.SetColor('#BC')

        return

    def is_item_red_point(self, data):
        state = data[mail_const.MAIL_STATE]
        player_lv = global_data.player.get_lv() if global_data.player else 0
        is_recv_friend_gold_gift_limit = global_data.player.is_recv_friend_gold_gift_limit() if global_data.player else False
        script_ver = self.script_ver
        engine_ver = self.engine_ver
        mail_id = data.get(mail_const.MAIL_ID, '')
        if type(mail_id) == str and mail_id.startswith('gold_') and is_recv_friend_gold_gift_limit:
            return False
        can_get_attachment = state != mail_const.MAIL_STATE_REWARD_GET and data.get(mail_const.MAIL_ATTACHMENT, []) and data.get(mail_const.MAIL_RECEIVE_LV, 0) <= player_lv and data.get(mail_const.MAIL_RECEIVE_LVER, 0) <= script_ver and data.get(mail_const.MAIL_RECEIVE_EVER, 0) <= engine_ver
        if data[mail_const.MAIL_STATE] == mail_const.MAIL_STATE_UNREAD or can_get_attachment:
            return True
        return False

    def is_unget_reward(self, data):
        if data[mail_const.MAIL_STATE] != mail_const.MAIL_STATE_REWARD_GET and data.get(mail_const.MAIL_ATTACHMENT, []):
            return True
        return False

    def check_sview(self):
        msg_count = len(self._email_datas)
        self._sview_data_index = self._lv_email.AutoAddAndRemoveItem(self._sview_data_index, self._email_datas, msg_count, self.add_email_elem, 300, 300)
        self._is_check_sview = False

    def set_visible(self, visible):
        self.panel.setVisible(visible)

    def on_finalize_panel(self):
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)
        self.show_main_ui()

    def do_show_panel(self):
        super(MainEmail, self).do_show_panel()
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)

    def do_hide_panel(self):
        super(MainEmail, self).do_hide_panel()
        import render
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)

    def set_email_state(self, email_item, data):
        email_item.img_item.SetDisplayFrameByPath('', get_item_pic_by_item_no(6001))
        email_item.img_item.setScale(0.5)
        if email_item.email_id == self._cur_email_id:
            email_item.btn_item.SetSelect(True)
            email_item.lab_name.SetColor('#SW')
            email_item.lab_time.SetColor('#SW')
            email_item.lab_read.SetColor('#SW')
        else:
            email_item.lab_name.SetColor('#BC')
            email_item.lab_time.SetColor('#BC')
            email_item.lab_read.SetColor('#BC')

        @email_item.btn_item.callback()
        def OnClick(*args):
            self.refresh_email_inf(data[mail_const.MAIL_ID])
            self.refresh_email_choose()

    def set_friend_email_state(self, email_item, data, *args):
        email_item.img_item.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(50101003))
        email_item.img_item.setScale(0.2)
        if email_item.email_id == self._cur_email_id:
            email_item.btn_item.SetSelect(True)
            email_item.lab_name.SetColor('#SW')
            email_item.lab_time.SetColor('#SW')
            email_item.lab_read.SetColor('#SW')
        else:
            if isinstance(email_item.email_id, str) and email_item.email_id.startswith('gold_'):
                uid = int(email_item.email_id.replace('gold_', ''))
                friend_info = global_data.message_data.get_player_detail_inf(uid)
            else:
                friend_info = None
            if friend_info:
                priv_settings = friend_info.get('priv_settings', {})
                priv_purple_id = friend_info.get('priv_purple_id', False)
                if priv_purple_id and priv_settings.get(const.PRIV_SHOW_PURPLE_ID, False):
                    email_item.lab_name.SetColor(COLOR_NAME)
                else:
                    email_item.lab_name.SetColor('#BC')
            else:
                email_item.lab_name.SetColor('#BC')

        @email_item.btn_item.callback()
        def OnClick(*args):
            self.refresh_email_inf(data[mail_const.MAIL_ID])
            self.refresh_friend_choose()

        return

    def set_system_email_state(self, email_item, data, *args):
        self.set_email_state(email_item, data)

    def set_credit_email_state(self, email_item, data, *args):
        self.set_email_state(email_item, data)