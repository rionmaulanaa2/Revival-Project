# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/home_message_board/MessageBoardManager.py
from __future__ import absolute_import
import six
from common.framework import Singleton
from logic.gcommon.common_const import homeland_const
from logic.gcommon.common_utils.text_utils import check_review_words_chat, CHECK_WORDS_PASS
from logic.gutils import homeland_utils
from common.utils import timer

class MessageBoardManager(Singleton):
    ALIAS_NAME = 'message_board_mgr'

    def init(self):
        self.new_timer = None
        self.new_dict = {}
        self.has_new = False
        self.init_new_message()
        self.init_parameters()
        self.process_event(True)
        return

    def init_parameters(self):
        self.message_data = []
        self.message_dict = {}
        self.message_show_data = []
        self.message_show_dict = {}
        self.message_count = 0
        self.intro_txt = ''
        self.heat = 0

    def destroy(self):
        self.clear_new_timer()
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'visit_place_change_event': self.on_visit_place_change,
           'on_login_enter_lobby': self.on_webtoken_init_succeed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_webtoken_init_succeed(self):
        homeland_utils.request_init_data()

    def on_visit_place_change(self):
        if not self.is_landlord():
            self.set_has_new(False)
        else:
            self.set_has_new(self.has_new)
        self.init_parameters()
        homeland_utils.request_init_data()
        self.save_new_message()

    def clear_new_timer(self):
        self.new_timer and global_data.game_mgr.get_logic_timer().unregister(self.new_timer)
        self.new_timer = None
        return

    def create_new_timer(self):
        self.clear_new_timer()

        def _cb():
            if not self.is_landlord():
                self.set_has_new(False)
                return
            ui = global_data.ui_mgr.get_ui('LobbyMessageBoardMainUI')
            if ui:
                return
            self.set_has_new(self.has_new)

        _cb()
        self.new_timer = global_data.game_mgr.get_logic_timer().register(func=_cb, mode=timer.CLOCK, interval=2)

    def set_has_new(self, has_new):
        for new in six.itervalues(self.new_dict):
            if new:
                has_new = True
                break

        if has_new == self.has_new:
            return
        self.has_new = has_new
        global_data.emgr.refresh_message_board_new.emit()

    def refresh_message_dict(self):
        self.bids = []
        self.init_new_message()
        is_all_read = not bool(self.new_dict)
        new_dict = {}
        for index, data in enumerate(self.message_data):
            bid = data.get('bid')
            if bid is None:
                continue
            if self.is_landlord():
                if is_all_read:
                    new_dict[str(bid)] = False
                elif str(bid) not in self.new_dict:
                    new_dict[str(bid)] = True
                else:
                    new_dict[str(bid)] = self.new_dict[str(bid)]
            self.bids.append(bid)
            self.message_dict[bid] = (index, data)

        self.new_dict = new_dict
        return

    def init_message_data(self, data):
        self.board_uid = data.get('uid', [])
        blocks = data.get('blocks', [])
        intro_txt = data.get('introduce', {}).get('intro') or ''
        _, flag, intro_txt = check_review_words_chat(intro_txt)
        self.heat = data.get('heat', 0)
        if flag != CHECK_WORDS_PASS:
            intro_txt = '******'
        self.intro_txt = intro_txt or (get_text_by_id(611540) if self.is_landlord() else '')
        self.message_count = len(blocks)
        self.message_data = blocks
        self.refresh_message_dict()
        self.message_show_data = []
        self.message_show_dict = {}
        self.set_has_new(self.has_new)
        self.create_new_timer()
        if self.message_count == 0:
            self.extend_message_data([])
        else:
            homeland_utils.request_more_data_max()

    def set_intro(self, intro_txt):
        self.intro_txt = intro_txt or (get_text_by_id(611540) if self.is_landlord() else '')
        global_data.emgr.refresh_message_board_data.emit()

    def give_like(self, bid, mid, sub_uid):
        if bid not in self.message_show_dict:
            return
        _, data = self.message_show_dict[bid]
        if mid not in data:
            return
        msg = data[mid]
        if sub_uid not in msg['thumbs']:
            msg['thumbs'].append(sub_uid)
        msg['thumb_cnt'] += 1
        global_data.emgr.refresh_message_board_data.emit()

    def cancel_like(self, bid, mid, sub_uid):
        if bid not in self.message_show_dict:
            return
        _, data = self.message_show_dict[bid]
        if mid not in data:
            return
        msg = data[mid]
        msg['thumbs'].remove(sub_uid)
        msg['thumb_cnt'] -= 1
        global_data.emgr.refresh_message_board_data.emit()

    def get_message_bid(self, data):
        for v in six.itervalues(data):
            return v.get('bid', 1)

    def refresh_message_show_dict(self):
        for index, msg_data in enumerate(self.message_show_data):
            bid = self.get_message_bid(msg_data)
            self.message_show_dict[bid] = (index, msg_data)

    def extend_message_data(self, data):
        is_init = not bool(self.message_show_data)
        cur_max_bid = self.get_max_bid()
        if data:
            one_data = data[0]
            bid = one_data.get('bid')
            mid = one_data.get('mid')
            send_time = one_data.get('send_time')
            for show_data in self.message_show_data:
                if mid in show_data:
                    if show_data[mid].get('bid') == bid and show_data[mid].get('send_time') == send_time:
                        return

            extend_max_bid = data[-1].get('bid', 0)
        else:
            extend_max_bid = 0
        if extend_max_bid > cur_max_bid:
            return
        msg_list_data = []
        msg_dict_data = {}
        uids = set()
        for msg in data:
            bid = msg.get('bid')
            mid = msg.get('mid')
            msg_txt = msg.get('msg', '')
            _, flag, msg_txt = check_review_words_chat(msg_txt)
            if flag != CHECK_WORDS_PASS:
                msg_txt = '******'
            msg['msg'] = msg_txt
            uids.add(msg.get('sub_uid'))
            if bid not in msg_dict_data:
                msg_dict_data[bid] = {}
                msg_list_data.append(msg_dict_data[bid])
            msg_dict_data[bid][mid] = msg

        if uids:
            global_data.message_data.get_multi_player_simple_inf(list(uids))
        append_data = msg_list_data[:]
        self.message_show_data.extend(msg_list_data)
        self.refresh_message_show_dict()
        global_data.emgr.refresh_message_board_data.emit(is_init=is_init, append_data=append_data)

    def get_message_show_data(self):
        return self.message_show_data[:]

    def get_max_bid(self):
        if self.message_show_data:
            return self.get_message_bid(self.message_show_data[-1])
        if self.message_data:
            return self.message_data[-1].get('bid', 0) + 1
        return 1

    def get_data_by_bid(self, bid):
        return self.message_show_dict.get(bid)

    def reply_message(self, bid, msg):
        msg_data = self.get_data_by_bid(bid)
        if not msg_data:
            return
        index, data = msg_data
        player = global_data.player
        if player:
            uid = player.get_visit_uid() or player.uid
            sub_uid = player.uid
            from logic.gcommon import time_utility
            now_time = time_utility.get_server_time()
            data[homeland_const.REPLY_MESSAGE] = {u'thumb_cnt': 0,u'uid': uid,
               u'bid': bid,
               u'mid': 2,
               u'thumbs': [],u'send_time': now_time,
               u'msg': msg,
               u'sub_uid': sub_uid
               }
            if bid in self.message_dict:
                index, data = self.message_dict[bid]
                data['messages'].append(homeland_const.REPLY_MESSAGE)
                data['mid'] = homeland_const.REPLY_MESSAGE
            global_data.emgr.refresh_message_board_data.emit()

    def del_message(self, bid):
        if bid in self.message_show_dict:
            index, _ = self.message_show_dict[bid]
            self.message_show_data.pop(index)
            del self.message_show_dict[bid]
            self.message_count = max(0, self.message_count - 1)
        if bid in self.message_dict:
            index, _ = self.message_dict[bid]
            self.message_data.pop(index)
            del self.message_dict[bid]
        self.del_new(bid)
        self.refresh_message_show_dict()
        self.refresh_message_dict()
        global_data.emgr.refresh_message_board_data.emit()

    def del_reply(self, bid, mid):
        if bid in self.message_show_dict:
            _, data = self.message_show_dict[bid]
            if mid in data:
                del data[mid]
        if bid in self.message_dict:
            _, data = self.message_dict[bid]
            data['messages'] = [homeland_const.LEFT_MESSAGE]
            data['mid'] = homeland_const.LEFT_MESSAGE
        global_data.emgr.refresh_message_board_data.emit()

    def init_new_message(self):
        message_board_arch = global_data.achi_mgr.get_archive_data('message_board_new')
        self.new_dict = message_board_arch.get_field(str(global_data.player.uid), {})

    def save_new_message(self):
        if not self.is_landlord():
            return
        message_board_arch = global_data.achi_mgr.get_archive_data('message_board_new')
        message_board_arch.set_field(str(global_data.player.uid), self.new_dict)

    def is_new_message(self, bid):
        return self.new_dict.get(str(bid), False)

    def is_landlord(self):
        player = global_data.player
        if not player:
            return False
        uid = player.get_visit_uid() or player.uid
        if uid and uid == player.uid:
            return True
        return False

    def del_new(self, bid=None):
        if not self.is_landlord():
            return
        else:
            if bid is None:
                for bid in six.iterkeys(self.new_dict):
                    self.new_dict[bid] = False

                self.set_has_new(False)
            elif str(bid) in self.new_dict:
                self.new_dict[str(bid)] = False
            global_data.emgr.refresh_message_board_data.emit()
            return

    def set_all_read(self):
        self.del_new()