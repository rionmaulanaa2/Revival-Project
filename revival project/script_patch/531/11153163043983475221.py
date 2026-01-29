# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/FriendSearchList.py
from __future__ import absolute_import
from six.moves import filter
from common.uisys.basepanel import BasePanel
import time
import common.utils.timer as timer
import common.uisys.richtext
from cocosui import cc, ccui, ccs
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.const.property_const import *
import common.utilities
import logic.gcommon.const as const
from common.utils.cocos_utils import ccc3FromHex, ccp, CCRect, CCSizeZero, ccc4FromHex, ccc4aFromHex
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.comsys.common_ui.InputBox as InputBox
from logic.gutils.role_head_utils import PlayerInfoManager
from logic.gutils import role_head_utils
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

class FriendSearchList(WindowMediumBase):
    PANEL_CONFIG_NAME = 'friend/add_friend_search_result'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_window'
    UI_ACTION_EVENT = {}

    def on_init_panel(self, *args, **kargs):
        super(FriendSearchList, self).on_init_panel()
        self.tag_idnex = 0
        self.role_head_manager = PlayerInfoManager()
        self._message_data = global_data.message_data
        self.refresh_search_friends()
        self.hide_main_ui()
        self.panel.PlayAnimation('show')

    def on_login_reconnect(self, *args):
        self.close()

    def _search_result_filter(self, data):
        if not data:
            return True
        name = data[C_NAME]
        if not name:
            return True
        from logic.gcommon.common_utils import text_utils
        return text_utils.check_review_name(name)

    def refresh_search_friends(self):
        friends = self._message_data.get_search_friends()
        friends = list(filter(self._search_result_filter, friends))
        self.panel.list_apply.DeleteAllSubItem()
        if friends:
            for data in friends:
                self.add_friend_elem(data)

        self.panel.nd_empty.setVisible(not friends)

    def add_friend_elem(self, data):
        lv_friend = self.panel.list_apply
        panel = lv_friend.AddTemplateItem()
        panel.lab_name.setString(data[C_NAME])
        uid = data[U_ID]
        self.role_head_manager.add_head_item_auto(panel.temp_head, uid, 0, data)
        role_head_utils.set_role_dan(panel.temp_tier, data.get('dan_info'))
        tag = self.tag_idnex
        panel.setTag(tag)
        self.tag_idnex += 1

        @panel.btn_add.callback()
        def OnClick(*args):
            global_data.player.req_add_friend(data[U_ID])
            global_data.message_data.del_recommend_friend(data[U_ID])
            lv_friend.DeleteItemByTag(tag)

        @panel.temp_head.callback()
        def OnClick(*args):
            pos_x, pos_y = panel.temp_head.GetPosition()
            world_pos = panel.temp_head.ConvertToWorldSpace(pos_x, pos_y)
            size = panel.temp_head.getContentSize()
            world_pos = cc.Vec2(world_pos.x + size.width, world_pos.y + size.height)
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            ui.refresh_by_uid(int(data[U_ID]))
            ui.set_position(world_pos, cc.Vec2(0.0, 0.5))

    def on_finalize_panel(self):
        self.show_main_ui()