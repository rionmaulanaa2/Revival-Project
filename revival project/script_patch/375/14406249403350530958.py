# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/home_message_board/MessageReplyUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gutils import role_head_utils
from logic.gutils import homeland_utils
from logic.comsys.lottery.LotterySmallSecondConfirmWidget import LotterySmallSecondConfirmWidget
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gcommon.common_const import homeland_const
from logic.gcommon.common_const.log_const import REPORT_FROM_TYPE_MESSAGE_BOARD, REPORT_CLASS_NORMAL
import time
import json

class MessageReplyUI(BasePanel):
    PANEL_CONFIG_NAME = 'home_system/open_home_system_reply'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'panel.btn_close.OnClick': 'on_click_btn_close',
       'panel.temp_btn_1.btn_common.OnClick': 'on_message_left_btn'
       }
    GLOBAL_EVENT = {'refresh_message_board_data': 'update_message_show_data',
       'message_on_player_simple_inf': 'on_player_simple_inf'
       }

    def on_init_panel(self):
        self.is_landlord = global_data.message_board_mgr.is_landlord()
        self.bid = None
        self._data = {}
        self.panel.temp_btn_1.setVisible(False)
        player = global_data.player
        if player:
            uid = player.get_visit_uid() or player.uid
            if self.is_landlord:
                self.panel.lab_title.SetString(get_text_by_id(611529).format(name=player.get_name()))
            else:
                role_data = global_data.message_data.get_player_inf(1, int(uid))
                if role_data:
                    char_name = role_data['char_name']
                    self.panel.lab_title.SetString(get_text_by_id(611529).format(name=char_name))
        return

    def on_click_btn_close(self, *args):
        self.close()

    def on_message_left_btn(self, *args):
        dlg = global_data.ui_mgr.show_ui('MessageLeftUI', 'logic.comsys.home_message_board')
        dlg.set_message_data(2, self.bid)

    def update_message_show_data(self, is_init=False, append_data=[]):
        if self.bid is None:
            self.close()
            return
        else:
            data = global_data.message_board_mgr.get_data_by_bid(self.bid)
            if data is None:
                self.close()
                return
            self.set_message_data(data[1])
            return

    def on_player_simple_inf(self, *args, **kargs):
        self.set_message_data(self._data)

    def set_message_data(self, data):
        self._data = data
        player = global_data.player
        if not player:
            return
        list_nd = self.panel.list_item
        self.bid = data[homeland_const.LEFT_MESSAGE].get('bid')
        left_nd = list_nd.GetItem(0)
        reply_nd = list_nd.GetItem(1)
        reply_nd.setVisible(False)
        has_reply = False
        for mid, msg in six.iteritems(data):
            msg_txt = msg.get('msg', '')
            sub_uid = msg.get('sub_uid')
            thumbs = msg.get('thumbs')
            send_time = msg.get('send_time')
            from logic.gcommon.time_utility import get_date_str
            time_txt = get_date_str('%Y:%m:%d', send_time).replace(':', '/')
            if mid == homeland_const.LEFT_MESSAGE:
                left_nd.lab_content.SetString(msg_txt)
                is_self = sub_uid == player.uid
                if is_self:
                    left_nd.lab_name.SetString(player.get_name())
                    role_head_utils.init_role_head(left_nd.temp_head, player.get_head_frame(), player.get_head_photo())
                else:
                    role_data = global_data.message_data.get_player_inf(1, int(sub_uid))
                    if role_data:
                        role_frame = role_data['head_frame']
                        role_photo = role_data['head_photo']
                        char_name = role_data['char_name']
                        left_nd.lab_name.SetString(char_name)
                        role_head_utils.init_role_head_auto(left_nd.temp_head, int(sub_uid), show_tips=True, head_frame=role_frame, head_photo=role_photo)
                total_thumbs = msg.get('thumb_cnt', 0)
                left_nd.lab_like.SetString(str(total_thumbs))
                list_nd = self.panel.list_item
                left_nd = list_nd.GetItem(0)
                left_del_nd = left_nd.list_icon.GetItem(0)
                uid = player.get_visit_uid() or player.uid
                left_del_nd.setVisible(player.uid == uid or player.uid == sub_uid)
                self.panel.temp_btn_1.setVisible(player.uid == uid and not has_reply)
                report_nd = left_nd.btn_report

                @report_nd.unique_callback()
                def OnClick(btn, touch):
                    if is_self:
                        user_info = {'uid': player.uid,'name': player.get_name(),
                           'intro': player.get_intro()
                           }
                    else:
                        role_data = global_data.message_data.get_player_inf(1, int(sub_uid))
                        if not role_data:
                            return
                        user_info = {'uid': role_data['uid'],'name': role_data['char_name'],
                           'intro': role_data.get('intro', '')
                           }
                    ui = global_data.ui_mgr.show_ui('UserReportUI', 'logic.comsys.report')
                    ui.report_users([user_info])
                    ui.set_report_class(REPORT_CLASS_NORMAL)
                    ui.set_hm_extra_report_info(msg_txt, REPORT_FROM_TYPE_MESSAGE_BOARD)

                @left_del_nd.btn_icon.callback()
                def OnClick(btn, touch):
                    self.del_message()

                left_like_nd = left_nd.list_icon.GetItem(1)
                left_like_nd.btn_icon.EnableCustomState(True)

                @global_unique_click(left_like_nd.btn_icon)
                def OnClick(btn, touch, mid=mid):
                    if btn.is_selected_like_btn is None:
                        btn.is_selected_like_btn = False
                    is_selected = btn.is_selected_like_btn
                    btn.SetSelect(not is_selected)
                    homeland_utils.give_like(self.bid, mid, is_selected)
                    player = global_data.player
                    if player:
                        if is_selected:
                            global_data.message_board_mgr.cancel_like(self.bid, mid, player.uid)
                        else:
                            global_data.message_board_mgr.give_like(self.bid, mid, player.uid)
                    btn.is_selected_like_btn = not is_selected
                    return

                uid = player.get_visit_uid() or player.uid
                left_nd.bar_praise.setVisible(uid in thumbs)
                is_selected = player.uid in thumbs
                left_like_nd.btn_icon.is_selected_like_btn = is_selected
                left_like_nd.btn_icon.SetSelect(is_selected)
                if send_time:
                    left_nd.lab_time.SetString(time_txt)
            else:
                reply_nd = list_nd.GetItem(1)
                reply_nd.setVisible(True)
                if msg:
                    self.panel.temp_btn_1.setVisible(False)
                    has_reply = True
                    reply_nd.lab_content.SetString(msg_txt)
                    uid = player.get_visit_uid() or player.uid
                    is_self = uid == player.uid
                    if is_self:
                        reply_nd.lab_name.SetString(player.get_name())
                        role_head_utils.init_role_head(reply_nd.temp_head, player.get_head_frame(), player.get_head_photo())
                    else:
                        role_data = global_data.message_data.get_player_inf(1, int(uid))
                        if role_data:
                            role_frame = role_data['head_frame']
                            role_photo = role_data['head_photo']
                            char_name = role_data['char_name']
                            reply_nd.lab_name.SetString(char_name)
                            role_head_utils.init_role_head_auto(reply_nd.temp_head, int(uid), head_frame=role_frame, head_photo=role_photo)
                    total_thumbs = msg.get('thumb_cnt', 0)
                    reply_nd.lab_like.SetString(str(total_thumbs))
                    reply_del_nd = reply_nd.list_icon.GetItem(0)
                    uid = player.get_visit_uid() or player.uid
                    reply_del_nd.setVisible(player.uid == uid)

                    @reply_del_nd.btn_icon.callback()
                    def OnClick(btn, touch):
                        self.del_reply()

                    reply_like_nd = reply_nd.list_icon.GetItem(1)
                    reply_like_nd.btn_icon.EnableCustomState(True)

                    @global_unique_click(reply_like_nd.btn_icon)
                    def OnClick(btn, touch, mid=mid):
                        if btn.is_selected_like_btn is None:
                            btn.is_selected_like_btn = False
                        is_selected = btn.is_selected_like_btn
                        btn.SetSelect(not is_selected)
                        homeland_utils.give_like(self.bid, mid, is_selected)
                        player = global_data.player
                        if player:
                            if is_selected:
                                global_data.message_board_mgr.cancel_like(self.bid, mid, player.uid)
                            else:
                                global_data.message_board_mgr.give_like(self.bid, mid, player.uid)
                        btn.is_selected_like_btn = not is_selected
                        return

                    is_selected = player.uid in thumbs
                    reply_like_nd.btn_icon.is_selected_like_btn = is_selected
                    reply_like_nd.btn_icon.SetSelect(is_selected)
                    if send_time:
                        reply_nd.lab_time.SetString(time_txt)

    def del_message(self):

        def _cb():
            homeland_utils.del_message(self.bid)
            global_data.message_board_mgr.del_message(self.bid)

        LotterySmallSecondConfirmWidget(title_text_id=611538, content_text_id=611535, confirm_callback=_cb)

    def del_reply(self):

        def _cb():
            homeland_utils.del_reply(self.bid, homeland_const.REPLY_MESSAGE)
            global_data.message_board_mgr.del_reply(self.bid, homeland_const.REPLY_MESSAGE)

        LotterySmallSecondConfirmWidget(title_text_id=611538, content_text_id=611535, confirm_callback=_cb)