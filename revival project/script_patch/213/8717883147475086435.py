# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/MainFriend.py
from __future__ import absolute_import
import six
import render
import cc
import game3d
from .FriendList import FriendList
from .IntimacyList import IntimacyList
from .BlackList import BlackList
from .AddFriend import AddFriend
from .MainFollow import MainFollow
from logic.gutils.share_utils import is_share_enable
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.comsys.common_ui.WindowBigBase import WindowBigBase
from logic.gcommon.const import HAS_CLICK_FRIEND_CHAT_HINT_KEY
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import mouse_scroll_utils
from logic.gcommon.common_const import ui_operation_const as uoc
FRIEND_TAB_RELATIONSHIP = 0
FRIEND_TAB_INTIMACY = 1
FRIEND_TAB_ADDFRIEND = 2
FRIEND_TAB_RECRUIT = 3
FRIEND_TAB_FOLLOW = 4
FRIEND_TAB_BLACK = 5
FRIEND_TAB_COUNT = 6
TAB_MAP = {FRIEND_TAB_RELATIONSHIP: {'tab_name': 80180,'ui_class': FriendList,'redpoint_id': '1'},FRIEND_TAB_INTIMACY: {'tab_name': 3214,'ui_class': IntimacyList,'redpoint_id': '12'},FRIEND_TAB_ADDFRIEND: {'tab_name': 10262,'ui_class': AddFriend,'redpoint_id': '4'},FRIEND_TAB_FOLLOW: {'tab_name': 10330,'ui_class': MainFollow},FRIEND_TAB_BLACK: {'tab_name': 10260,'ui_class': BlackList}}

class MainFriend(WindowBigBase):
    PANEL_CONFIG_NAME = 'friend/main_friend'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    HOT_KEY_NEED_SCROLL_SUPPORT = True

    def on_init_panel(self, *args, **kargs):
        super(MainFriend, self).on_init_panel(*args, **kargs)
        self._message_data = global_data.message_data
        self._friends = global_data.message_data.get_friends()
        self._black_friends = global_data.message_data.get_black_friends()
        self._init_finish_cb = dict()
        self._init_tab_index = kargs.get('init_tab_index', FRIEND_TAB_RELATIONSHIP)
        self._init_sub_tab_index = kargs.get('init_sub_tab_index', None)
        self._need_show_highlight = bool(kargs.get('need_show_highlight', False))
        self._cur_tab_index = None
        self._sub_panel_uis = {}
        self._tab_panels = {}
        self.init_tab_map()
        self.init_tab()
        self.query_player_role_head_info()
        self.hide_main_ui()
        self.panel.temp_bg.btn_close.SetSwallowTouch(False)
        self.init_scroll()
        return

    def on_login_reconnect(self, *args):
        self.close()

    def init_tab_map(self):
        if is_share_enable() and G_IS_NA_USER:
            self._tab_map = TAB_MAP
        else:
            self._tab_map = dict(TAB_MAP)
            if FRIEND_TAB_RECRUIT in self._tab_map:
                del self._tab_map[FRIEND_TAB_RECRUIT]

    def init_tab(self):
        FRAME_INTERVAL = 0.03
        frame_actions = [
         cc.CallFunc.create(lambda : self.create_tab(self._init_tab_index)),
         cc.CallFunc.create(lambda : self.touch_tab_by_index(self._init_tab_index))]
        for n, key in enumerate(six.iterkeys(self._tab_map)):
            if key == self._init_tab_index:
                continue
            frame_actions.extend([
             cc.DelayTime.create(FRAME_INTERVAL),
             cc.CallFunc.create(lambda idx=key: self.create_tab(idx))])

        self.panel.runAction(cc.Sequence.create(frame_actions))

    def create_tab(self, tab_idx):
        panel = self.panel.temp_bg.list_tab.AddTemplateItem()
        panel.btn_window_tab.SetText(get_text_by_id(self._tab_map[tab_idx]['tab_name']), color1='#DD', color2='#SW', color3='#SW')
        panel.btn_window_tab.SetSelect(False)
        self.add_touch_tab(panel, tab_idx)
        redpoint_id = TAB_MAP[tab_idx].get('redpoint_id')
        if redpoint_id:
            global_data.redpoint_mgr.register_redpoint(panel.img_hint, redpoint_id)
        self._ui_init_finish(tab_idx)

    def set_ui_init_finish_cb(self, tab_idx, cb):
        self._init_finish_cb[tab_idx] = cb

    def _ui_init_finish(self, tab_idx):
        cb = self._init_finish_cb.get(tab_idx, None)
        if callable(cb):
            cb()
        return

    def query_player_role_head_info(self):
        global_data.message_data.request_role_head_info(['friend', 'recent_team', 'recent_chat'])

    def add_touch_tab(self, panel, index):
        panel.btn_window_tab.EnableCustomState(True)
        panel.btn_window_tab.BindMethod('OnClick', lambda *args: self.touch_tab_by_index(index))
        self._tab_panels[index] = panel

    def touch_tab_by_index(self, index):
        if not global_data.player:
            self.close()
        if not self.panel or self.panel.IsDestroyed():
            return
        else:
            if index not in self._tab_panels:
                self.set_ui_init_finish_cb(index, lambda i=index: self.touch_tab_by_index(i))
                return
            if self._cur_tab_index != None:
                sub_panel = self._sub_panel_uis.get(self._cur_tab_index)
                sub_panel.set_visible(False)
                tab_panel = self._tab_panels.get(self._cur_tab_index)
                tab_panel.btn_window_tab.SetSelect(False)
                tab_panel.StopAnimation('continue')
                tab_panel.RecoverAnimationNodeState('continue')
            sub_panel = self._sub_panel_uis.get(index)
            if not sub_panel:
                sub_panel = TAB_MAP[index]['ui_class'](self, tab_index=self._init_sub_tab_index)
                self._init_sub_tab_index = None
                self._sub_panel_uis[index] = sub_panel
            sub_panel.set_visible(True)
            has_click_friend_chat_hint = global_data.achi_mgr.get_general_archive_data().get_field(HAS_CLICK_FRIEND_CHAT_HINT_KEY, 0)
            if self._need_show_highlight and not has_click_friend_chat_hint:
                if hasattr(sub_panel, 'set_coin_animation'):
                    sub_panel.set_coin_animation()
            tab_panel = self._tab_panels.get(index)
            tab_panel.btn_window_tab.SetSelect(True)
            tab_panel.PlayAnimation('click')
            tab_panel.RecordAnimationNodeState('continue')
            tab_panel.PlayAnimation('continue')
            self._cur_tab_index = index
            return sub_panel

    def on_finalize_panel(self):
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)
        global_data.message_data.remove_all_intimacy_event_data()
        for panel_ui in six.itervalues(self._sub_panel_uis):
            if panel_ui and getattr(panel_ui, 'isValid', lambda : True)():
                panel_ui.destroy()

        self._sub_panel_uis = {}
        self.show_main_ui()

    def open_new_chat_dialog(self, uid, cname, lv, role_id, dan_info):

        def _action():
            data = self._message_data.add_new_record(uid, cname=cname, role_id=role_id, lv=lv, dan_info=dan_info)
            self.touch_tab_by_index(FRIEND_TAB_RELATIONSHIP)
            sub_panel = self._sub_panel_uis.get(FRIEND_TAB_RELATIONSHIP)
            sub_panel.refresh_friend_chat(data)
            sub_panel.refresh_choose_panel(uid)

        if FRIEND_TAB_RELATIONSHIP not in self._tab_panels:
            self._init_finish_cb[FRIEND_TAB_RELATIONSHIP] = _action
            return
        _action()

    def do_show_panel(self):
        super(MainFriend, self).do_show_panel()
        global_data.display_agent.set_post_effect_active('gaussian_blur', True)

    def do_hide_panel(self):
        super(MainFriend, self).do_hide_panel()
        for i in six.iterkeys(self._tab_map):
            sub_panel = self._sub_panel_uis.get(i)
            if sub_panel and getattr(sub_panel, 'hide_inputbox', None):
                sub_panel.hide_inputbox()

        global_data.display_agent.set_post_effect_active('gaussian_blur', False)
        return

    def init_scroll(self):
        if global_data.is_pc_mode:
            self.register_mouse_scroll_event()

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        sub_panel = self._sub_panel_uis.get(self._cur_tab_index)
        if not sub_panel:
            return
        else:
            get_friend_list = getattr(sub_panel, 'get_friend_list', None)
            if not callable(get_friend_list):
                return
            friend_list = get_friend_list()
            if not friend_list:
                return
            if friend_list.GetItemCount() == 0:
                return
            if self._cur_tab_index == FRIEND_TAB_RELATIONSHIP:
                mouse_scroll_utils.sview_scroll_by_mouse_wheel_dynamic(sub_panel, friend_list, delta, uoc.SST_TASK_MAIN_MOUSE_WHEEL)
            elif self._cur_tab_index == FRIEND_TAB_FOLLOW:
                mouse_scroll_utils.sview_scroll_by_mouse_wheel_dynamic(sub_panel.get_cur_tab(), friend_list, delta, uoc.SST_TASK_MAIN_MOUSE_WHEEL)
            elif self._cur_tab_index == FRIEND_TAB_ADDFRIEND:
                mouse_scroll_utils.sview_scroll_by_mouse_wheel(friend_list, delta, uoc.SST_TASK_MAIN_MOUSE_WHEEL)
            return

    def check_can_mouse_scroll(self):
        if global_data.is_pc_mode and self.HOT_KEY_NEED_SCROLL_SUPPORT and global_data.player:
            return True
        return False