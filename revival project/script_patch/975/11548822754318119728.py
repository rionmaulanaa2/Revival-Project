# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/home_message_board/LobbyVisitMainUI.py
from __future__ import absolute_import
import six_ex
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CUSTOM
from common.const.property_const import C_NAME, U_ID
from logic.gutils.role_head_utils import PlayerInfoManager
from logic.comsys.lottery.LotterySmallSecondConfirmWidget import LotterySmallSecondConfirmWidget
from logic.gutils import homeland_utils
from logic.gutils import role_head_utils
from logic.gutils.lobby_click_interval_utils import global_unique_click
from logic.gcommon.common_const import homeland_const
import json

class LobbyVisitMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'home_system/visitor_invite'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'panel.OnClick': 'on_click_close_btn'
       }
    GLOBAL_EVENT = {'refresh_visit_player_info_event': 'refresh_visit_player_info'
       }

    def on_init_panel(self):
        self.init_parameters()
        self.refresh_visit_player_info()
        self.panel.PlayAnimation('show')

    def on_finalize_panel(self):
        self.player_info_manager and self.player_info_manager.destroy()

    def on_click_close_btn(self, *args):
        self.ui_vkb_custom_func()

    def hide(self):
        animation_time = self.panel.GetAnimationMaxRunTime('hide')
        self.panel.PlayAnimation('hide')
        self.panel.SetTimeOut(animation_time, self.close)

    def init_parameters(self):
        self.player_info_manager = PlayerInfoManager()

    def ui_vkb_custom_func(self):
        if not self.panel.IsPlayingAnimation('hide'):
            self.hide()
        return True

    def refresh_visit_player_info(self):
        player = global_data.player
        if not player:
            return
        visitors = player.get_all_puppet_info(False)
        if not visitors:
            self.panel.list_visitor.SetInitCount(0)
            return
        visitor_ids = six_ex.keys(visitors)
        visitor_ids.sort()
        self.panel.list_visitor.SetInitCount(len(visitor_ids))
        for index, node in enumerate(self.panel.list_visitor.GetAllItem()):
            data = visitors[visitor_ids[index]]
            friend_id = data[U_ID]
            name = data.get(C_NAME, '')
            node.lab_name.setString(name)
            if global_data.player:
                remark = global_data.player._frds_remark.get(int(friend_id), '') if 1 else ''
                if node.lab_name2:
                    node.lab_name2.setVisible(bool(remark))
                    if remark:
                        node.lab_name2.SetString('(%s)' % remark)
                self.player_info_manager.add_head_item_auto(node.temp_head, friend_id, 0, data, show_tips=True)
                self.player_info_manager.add_dan_info_item(node.temp_tier, friend_id)
                role_head_utils.init_dan_info(node.temp_tier, friend_id, txt_nd=node.lab_status)
                priv_data = global_data.message_data.get_player_simple_inf(friend_id)
                if not priv_data:
                    priv_data = {}
                role_head_utils.init_privilege_name_color_and_badge(node.lab_name, node.temp_head, priv_data, 0)

                @node.btn_del.callback()
                def OnClick(btn, touch, friend_id=friend_id, name=name):

                    def _cb(friend_id=friend_id, name=name):
                        player = global_data.player
                        if not player:
                            return
                        player.request_kick_visitor(friend_id)

                    LotterySmallSecondConfirmWidget(title_text_id=611560, content_text_id=get_text_by_id(611536).format(name=name), confirm_callback=_cb)