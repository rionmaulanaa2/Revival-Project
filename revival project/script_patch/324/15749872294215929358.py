# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummer/VeteranRecallSubUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.gutils import share_utils
from logic.client.const.share_const import TYPE_LINK, APP_SHARE_MOBILE_QQ, APP_SHARE_WEIXIN

class VeteranRecallSubUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'activity/activity_202107/veterans_recall_send'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {}

    def on_init_panel(self, *args, **kwargs):
        super(VeteranRecallSubUI, self).on_init_panel()
        self.init_params()

    def init_params(self):
        self.role_data = {}

    def set_role_data(self, role_data):
        self.role_data = role_data
        self.init_ui_events()

    def init_ui_events(self):
        if not share_utils.is_share_enable():
            global_data.game_mgr.show_tip(get_text_by_id(609778))
        support_platform = share_utils.get_team_up_url_support_platform_enum()
        platform_info_list = global_data.share_mgr.get_support_platforms_from_enum(support_platform)
        nd_1 = self.panel.list_social.GetItem(0)

        @nd_1.btn_send.btn_common.unique_callback()
        def OnClick(_btn, _touch, *args):
            if platform_info_list and APP_SHARE_WEIXIN in support_platform:
                pass
            else:
                global_data.game_mgr.show_tip(get_text_by_id(633703))
                return
            nd_1.btn_send.btn_common.SetEnable(False)
            nd_1.btn_send.btn_common.SetText(609731)
            uid = self.role_data['uid']
            username = self.role_data['username']
            global_data.player.send_qqorwc_to_lost_role(uid, username, 'wc')
            if platform_info_list:
                share_url, s_title, s_message = share_utils.get_mainland_invite_team_url()
                share_args = global_data.share_mgr.get_share_app_share_args(APP_SHARE_WEIXIN)
                share_inform_cb = lambda *args: True
                global_data.share_mgr.share(share_args, TYPE_LINK, '', link=share_url, title=s_title, message=s_message, share_inform_cb=share_inform_cb)

        nd_2 = self.panel.list_social.GetItem(1)

        @nd_2.btn_send.btn_common.unique_callback()
        def OnClick(_btn, _touch, *args):
            if platform_info_list and APP_SHARE_MOBILE_QQ in support_platform:
                pass
            else:
                global_data.game_mgr.show_tip(get_text_by_id(633703))
                return
            nd_2.btn_send.btn_common.SetEnable(False)
            nd_2.btn_send.btn_common.SetText(609731)
            uid = self.role_data['uid']
            username = self.role_data['username']
            global_data.player.send_qqorwc_to_lost_role(uid, username, 'qq')
            if platform_info_list:
                share_url, s_title, s_message = share_utils.get_mainland_invite_team_url()
                share_args = global_data.share_mgr.get_share_app_share_args(APP_SHARE_MOBILE_QQ)
                share_inform_cb = lambda *args: True
                global_data.share_mgr.share(share_args, TYPE_LINK, '', link=share_url, title=s_title, message=s_message, share_inform_cb=share_inform_cb)

        nd_3 = self.panel.list_social.GetItem(2)
        has_phone = self.role_data.get('has_phone', False)
        if not has_phone:
            nd_3.setVisible(False)
            return
        nd_3.setVisible(True)
        uid = self.role_data['uid']
        self.send_mgs_uids = global_data.player.send_msg_uids
        if uid in self.send_mgs_uids.get('msg', []):
            nd_3.btn_send.btn_common.SetEnable(False)
            nd_3.btn_send.btn_common.SetText(609731)
            return

        @nd_3.btn_send.btn_common.unique_callback()
        def OnClick(_btn, _touch, *args):
            nd_3.btn_send.btn_common.SetEnable(False)
            nd_3.btn_send.btn_common.SetText(609731)
            username = self.role_data['username']
            global_data.player.send_msg_to_lost_role(uid, username)
            global_data.game_mgr.show_tip(get_text_by_id(609785))

    def on_finalize_panel(self):
        self.init_params()
        super(VeteranRecallSubUI, self).on_finalize_panel()