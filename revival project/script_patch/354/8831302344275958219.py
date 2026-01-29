# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/home_message_board/LobbyMessageBoardMainUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.comsys.lottery.LotterySmallSecondConfirmWidget import LotterySmallSecondConfirmWidget
from logic.gutils import homeland_utils
from logic.gutils import role_head_utils
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gcommon.common_const import homeland_const
import json

class LobbyMessageBoardMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'home_system/bg_home_system'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'panel.btn_close.OnClick': 'on_click_btn',
       'panel.temp_btn_1.btn_common.OnClick': 'on_message_left_btn',
       'panel.btn_write.OnClick': 'on_click_write_btn',
       'panel.btn_tips.OnClick': 'on_click_tips_btn'
       }
    GLOBAL_EVENT = {'refresh_message_board_data': 'update_message_show_data',
       'visit_place_change_event': 'on_visit_place_change',
       'message_on_players_detail_inf': 'on_message_on_players_inf'
       }

    def on_init_panel(self):
        self.is_landlord = global_data.message_board_mgr.is_landlord()
        self.panel.btn_write.setVisible(False)
        self.panel.temp_btn_1.setVisible(False)
        player = global_data.player
        if player:
            uid = player.get_visit_uid() or player.uid
            if self.is_landlord:
                role_head_utils.init_role_head(self.panel.temp_head, player.get_head_frame(), player.get_head_photo())
                self.panel.lab_name.SetString(get_text_by_id(611529).format(name=player.get_name()))
                self.panel.temp_btn_1.btn_common.SetText(80915)
            else:
                role_data = global_data.message_data.get_player_inf(1, int(uid))
                if role_data:
                    role_frame = role_data['head_frame']
                    role_photo = role_data['head_photo']
                    char_name = role_data['char_name']
                    self.panel.lab_name.SetString(get_text_by_id(611529).format(name=char_name))
                    role_head_utils.init_role_head_auto(self.panel.temp_head, int(uid), head_frame=role_frame, head_photo=role_photo)
                self.panel.temp_btn_1.btn_common.SetText(611527)
            self.panel.btn_write.setVisible(self.is_landlord)
            if not self.is_landlord:
                self.panel.temp_btn_1.setVisible(True)
        self.update_message_info()
        self.init_scroll_view()
        self.request_init_data()

    def update_message_info(self):
        self.panel.lab_welcome.SetString(global_data.message_board_mgr.intro_txt)
        self.panel.lab_value.SetString(str(global_data.message_board_mgr.heat))
        self.panel.lab_limit.SetString(get_text_by_id(611528).format(global_data.message_board_mgr.message_count, max(global_data.message_board_mgr.message_count, homeland_const.HOMELAND_MAX_BLOCK_COUNT)))

    def on_visit_place_change(self):
        self.close()

    def on_finalize_panel(self):
        global_data.message_board_mgr.save_new_message()
        global_data.message_board_mgr.set_has_new(False)

    def request_init_data(self):
        homeland_utils.request_init_data()

    def init_scroll_view(self):
        self.message_show_list = []
        self._cur_message_page = -1
        self._page_sizes = {}
        from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget

        def require_data_callback():
            homeland_utils.request_more_data_max()

        def refresh_callback():
            self.request_init_data()

        self._sview = InfiniteScrollWidget(self.panel.list_item, self.panel.bg, up_limit=600, down_limit=600)
        self._sview.set_is_only_add(True)
        self._sview.set_refresh_callback(refresh_callback)
        self._sview.set_template_init_callback(self.init_one_message_template)
        self._sview.enable_item_auto_pool(True)

        @self.panel.list_item.unique_callback()
        def OnScrollBounceBottom(sv):
            require_data_callback()

        self.update_message_show_data(is_init=True)

    def init_one_message_template(self, node, data):
        player = global_data.player
        if not player:
            return
        node.lab_reply.SetString('')
        for mid, msg in six.iteritems(data):
            bid = msg.get('bid')
            msg_txt = msg.get('msg', '')
            sub_uid = msg.get('sub_uid')
            thumbs = msg.get('thumbs')
            if mid == homeland_const.LEFT_MESSAGE:
                node.lab_content.SetString(msg_txt)
                if sub_uid:
                    is_self = sub_uid == player.uid
                    if is_self:
                        node.lab_name.SetString(player.get_name())
                        role_head_utils.init_role_head(node.temp_head, player.get_head_frame(), player.get_head_photo())
                    elif global_data.message_data.has_player_inf(int(sub_uid)):
                        role_data = global_data.message_data.get_player_inf(1, int(sub_uid))
                        if role_data:
                            role_frame = role_data['head_frame']
                            role_photo = role_data['head_photo']
                            char_name = role_data['char_name']
                            node.lab_name.SetString(char_name)
                            role_head_utils.init_role_head_auto(node.temp_head, int(sub_uid), show_tips=True, head_frame=role_frame, head_photo=role_photo)
                send_time = msg.get('send_time')
                if send_time:
                    from logic.gcommon.time_utility import get_date_str
                    node.lab_time.SetString(get_date_str('%Y:%m:%d', send_time).replace(':', '/'))
                total_thumbs = msg.get('thumb_cnt', 0)
                node.lab_like.SetString(str(total_thumbs))
                del_nd = node.list_icon.GetItem(0)
                uid = player.get_visit_uid() or player.uid
                del_nd.setVisible(player.uid == uid or player.uid == sub_uid)

                @del_nd.btn_icon.callback()
                def OnClick(btn, touch, bid=bid):
                    self.del_message(bid)

                is_new = self.is_landlord and global_data.message_board_mgr.is_new_message(bid)
                node.img_new_tag.setVisible(is_new)

                @node.callback()
                def OnClick(btn, touch, bid=bid, data=data):
                    dlg = global_data.ui_mgr.show_ui('MessageReplyUI', 'logic.comsys.home_message_board')
                    dlg.set_message_data(data)
                    if self.is_landlord:
                        global_data.message_board_mgr.del_new(bid)

                like_nd = node.list_icon.GetItem(1)
                like_nd.btn_icon.EnableCustomState(True)

                @global_unique_click(like_nd.btn_icon)
                def OnClick(btn, touch, bid=bid, mid=mid):
                    if btn.is_selected_like_btn is None:
                        btn.is_selected_like_btn = False
                    is_selected = btn.is_selected_like_btn
                    btn.SetSelect(not is_selected)
                    homeland_utils.give_like(bid, mid, is_selected)
                    player = global_data.player
                    if player:
                        if is_selected:
                            global_data.message_board_mgr.cancel_like(bid, mid, player.uid)
                        else:
                            global_data.message_board_mgr.give_like(bid, mid, player.uid)
                    btn.is_selected_like_btn = not is_selected
                    return

                uid = player.get_visit_uid() or player.uid
                node.bar_praise.setVisible(uid in thumbs)
                is_selected = player.uid in thumbs
                like_nd.btn_icon.is_selected_like_btn = is_selected
                like_nd.btn_icon.SetSelect(is_selected)
            else:
                from logic.gutils.live_utils import format_one_line_text
                formated_txt = format_one_line_text(node.lab_reply, msg_txt, 299)
                node.lab_reply.SetString(get_text_by_id(611537).format(content=formated_txt))

    def clear_scroll_view(self):
        if self._sview:
            self._sview.destroy()
            self._sview = None
        return

    def on_message_on_players_inf(self, *args, **kargs):
        self.update_message_show_data()

    def update_message_show_data(self, is_init=False, append_data=[]):
        self.update_message_info()
        if is_init:
            self.message_show_list = global_data.message_board_mgr.get_message_show_data()
            self._sview.update_data_list(self.message_show_list)
            self._sview.refresh_showed_item()
            self._sview.update_scroll_view()
            self.panel.list_item.ScrollToTop()
        elif append_data:
            self._sview.on_receive_data(append_data)
        else:
            offset = self.panel.list_item.GetContentOffset()
            old_h = self.panel.list_item.GetInnerContentSize().height
            self.message_show_list = global_data.message_board_mgr.get_message_show_data()
            self._sview.update_data_list(self.message_show_list)
            self._sview.refresh_showed_item(has_diff_size=True)
            self._sview.update_scroll_view()
            new_h = self.panel.list_item.GetInnerContentSize().height
            _, content_h = self.panel.list_item.GetContentSize()
            if content_h >= new_h:
                self.panel.list_item.ScrollToTop()
            else:
                offset.y += old_h - new_h
                self.panel.list_item.SetContentOffset(offset)
        if self.is_landlord:
            self.panel.temp_btn_1.setVisible(global_data.message_board_mgr.has_new)
        self.panel.nd_empty.setVisible(not self.message_show_list)

    def del_message(self, bid):

        def _cb(bid=bid):
            homeland_utils.del_message(bid)
            global_data.message_board_mgr.del_message(bid)

        LotterySmallSecondConfirmWidget(title_text_id=611538, content_text_id=611549 if self.is_landlord else 611535, confirm_callback=_cb)

    def on_click_btn(self, *args):
        self.close()

    def on_message_left_btn(self, *args):
        if self.is_landlord:
            global_data.message_board_mgr.set_all_read()
            self.panel.temp_btn_1.setVisible(False)
        else:
            player = global_data.player
            if player:
                left_message_count = global_data.message_data.get_seting_inf('message_board_left_count') or {}
                uid = player.get_visit_uid() or player.uid
                count, day = left_message_count.get(int(uid), [0, 0])
                from logic.gcommon import time_utility as tutil
                cur_day = tutil.get_rela_day_no()
                if cur_day != day:
                    count = 0
                    left_message_count[int(uid)] = [count, cur_day]
                    global_data.message_data.set_seting_inf('message_board_left_count', left_message_count)
                player_lv = player.get_lv()
                if player_lv < 10:
                    global_data.game_mgr.show_tip(get_text_by_id(603007).format('10'))
                elif count >= 5:
                    global_data.game_mgr.show_tip(get_text_by_id(611523))
                else:
                    dlg = global_data.ui_mgr.show_ui('MessageLeftUI', 'logic.comsys.home_message_board')
                    dlg.set_message_data(1)

    def on_click_write_btn(self, *args):
        dlg = global_data.ui_mgr.show_ui('MessageLeftUI', 'logic.comsys.home_message_board')
        dlg.set_message_data(3)

    def on_click_tips_btn(self, btn, touch):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        import cc
        dlg = GameRuleDescUI()
        dlg.set_show_rule(602039, 611648)
        dlg.set_node_pos(touch.getLocation(), cc.Vec2(0, 1))