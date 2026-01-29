# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/CommonFriendListWidget.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
import cc
from common.const.property_const import *
from common.const.uiconst import DIALOG_LAYER_ZORDER_1
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gcommon import const
from logic.gutils import role_head_utils
from logic.gutils.role_head_utils import PlayerInfoManager, set_gray, set_gray_by_online_state
STATE_WEIGHT_MAP = {const.STATE_INVISIBLE: 0,
   const.STATE_OFFLINE: 0,
   const.STATE_BATTLE: 1,
   const.STATE_BATTLE_FIGHT: 2,
   const.STATE_EXERCISE: 3,
   const.STATE_SPECTATING: 4,
   const.STATE_TEAM: 5,
   const.STATE_ROOM: 6,
   const.STATE_SINGLE: 10
   }

class CommonFriendListWidget(BaseUIWidget):

    def set_select_friend_cb(self, sel_cb):
        self._select_friend_cb = sel_cb

    def __init__(self, panel_cls, ui_panel):
        self.global_events = {}
        super(CommonFriendListWidget, self).__init__(panel_cls, ui_panel)
        self._select_friend_cb = None
        self._cur_show_index = -1
        self._is_check_scroll_view = False
        self._lst_nd = self.panel.nd_content.list_friend
        self._player_info_manager = PlayerInfoManager()
        self._friends_info = self._get_sorted_data()
        self._init_ui_event()
        self._lst_nd.addEventListener(self._scroll_callback)
        self._refresh_all()
        return

    def _scroll_callback(self, sender, eventType):
        if self._is_check_scroll_view == False:
            self._is_check_scroll_view = True
            self.panel.SetTimeOut(0.001, self._check_sview)

    def _check_sview(self):
        self._cur_show_index = self._lst_nd.AutoAddAndRemoveItem(self._cur_show_index, self._friends_info, len(self._friends_info), self._add_friend_item, 300, 400)
        self._is_check_scroll_view = False

    def _add_friend_item(self, data, is_back_item, index=-1):
        if is_back_item:
            item = self._lst_nd.AddTemplateItem(bRefresh=True)
        else:
            item = self._lst_nd.AddTemplateItem(0, bRefresh=True)
        self._refresh_friend_item(item, data)
        return item

    def _refresh_all(self):
        self._lst_nd.DeleteAllSubItem()
        data_count = len(self._friends_info)
        sview_height = self._lst_nd.getContentSize().height
        all_height = 0
        index = 0
        nd_empty_visible = True if data_count == 0 else False
        self.panel.nd_bar.nd_empty.setVisible(nd_empty_visible)
        self.panel.nd_bar.nd_empty.btn_empty.setVisible(False)
        self.panel.nd_content.setVisible(not nd_empty_visible)
        while all_height < sview_height + 200:
            if data_count - index <= 0:
                break
            data = self._friends_info[index]
            chat_pnl = self._add_friend_item(data, True)
            all_height += chat_pnl.getContentSize().height
            index += 1

        self._lst_nd.ScrollToTop()
        self._lst_nd._container._refreshItemPos()
        self._lst_nd._refreshItemPos()
        self._cur_show_index = index - 1

    def _refresh_friend_item(self, item, data):
        friend_id = data[U_ID]
        name = data.get(C_NAME, '')
        item.btn_item.lab_name.setString(name)
        self._player_info_manager.add_head_item_auto(item.btn_item.temp_head, friend_id, 0, data)
        role_head_utils.set_role_dan(item.temp_tier, data.get('dan_info', {}))
        self._set_online_state(item, friend_id)

        @item.btn_item.callback()
        def OnClick(btn, touch, f_data=data):
            if self._select_friend_cb and callable(self._select_friend_cb):
                self._select_friend_cb(f_data)

        @item.btn_item.temp_head.callback()
        def OnClick(*args):
            pos_x, pos_y = item.GetPosition()
            world_pos = item.ConvertToWorldSpace(pos_x, pos_y)
            size = item.getContentSize()
            show_pos_x = world_pos.x - size.width - 40
            lst_pos_x, lst_pos_y = self._lst_nd.GetPosition()
            lst_pos = self._lst_nd.ConvertToWorldSpace(lst_pos_x, lst_pos_y)
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            ui.refresh_by_uid(int(data[U_ID]))
            ui.set_position(cc.Vec2(show_pos_x, lst_pos.y))
            ui.set_template_zorder(DIALOG_LAYER_ZORDER_1)

    def _init_ui_event(self):

        @self.panel.nd_blokc.unique_callback()
        def OnClick(*args):
            self.hide()

    def _set_online_state(self, item, friend_id):
        from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
        import logic.gcommon.const as const
        friend_online_state = global_data.message_data.get_player_online_state()
        state = int(friend_online_state.get(int(friend_id), 0))
        text_id, color = ui_utils.get_online_inf(state)
        item.lab_status.setString(get_text_by_id(text_id))
        item.lab_status.SetColor(color)
        set_gray_by_online_state(item.btn_item.temp_head, state)

    def _get_sorted_data(self):
        friend_online_state = global_data.message_data.get_player_online_state()

        def cmp_func--- This code section failed: ---

 149       0  LOAD_GLOBAL           0  'int'
           3  LOAD_DEREF            0  'friend_online_state'
           6  LOAD_ATTR             1  'get'
           9  LOAD_GLOBAL           0  'int'
          12  LOAD_GLOBAL           1  'get'
          15  BINARY_SUBSCR    
          16  CALL_FUNCTION_1       1 
          19  LOAD_CONST            2  ''
          22  CALL_FUNCTION_2       2 
          25  CALL_FUNCTION_1       1 
          28  STORE_FAST            2  'a_state'

 150      31  LOAD_GLOBAL           0  'int'
          34  LOAD_DEREF            0  'friend_online_state'
          37  LOAD_ATTR             1  'get'
          40  LOAD_GLOBAL           0  'int'
          43  LOAD_FAST             1  'b'
          46  LOAD_CONST            1  'uid'
          49  BINARY_SUBSCR    
          50  CALL_FUNCTION_1       1 
          53  LOAD_CONST            2  ''
          56  CALL_FUNCTION_2       2 
          59  CALL_FUNCTION_1       1 
          62  STORE_FAST            3  'b_state'

 151      65  LOAD_FAST             2  'a_state'
          68  LOAD_FAST             3  'b_state'
          71  COMPARE_OP            3  '!='
          74  POP_JUMP_IF_FALSE   108  'to 108'

 152      77  LOAD_GLOBAL           2  'STATE_WEIGHT_MAP'
          80  LOAD_FAST             2  'a_state'
          83  BINARY_SUBSCR    
          84  LOAD_GLOBAL           2  'STATE_WEIGHT_MAP'
          87  LOAD_FAST             3  'b_state'
          90  BINARY_SUBSCR    
          91  COMPARE_OP            4  '>'
          94  POP_JUMP_IF_FALSE   101  'to 101'

 153      97  LOAD_CONST            3  1
         100  RETURN_END_IF    
       101_0  COME_FROM                '94'

 155     101  LOAD_CONST            4  -1
         104  RETURN_VALUE     
         105  JUMP_FORWARD          4  'to 112'

 157     108  LOAD_CONST            4  -1
         111  RETURN_VALUE     
       112_0  COME_FROM                '105'

Parse error at or near `CALL_FUNCTION_1' instruction at offset 25

        data_list = global_data.message_data.get_friends()
        sort_data_list = sorted(six_ex.values(data_list), key=cmp_to_key(cmp_func), reverse=True)
        return sort_data_list

    def destroy(self):
        self._select_friend_cb = None
        super(CommonFriendListWidget, self).destroy()
        return