# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/AddRecruit.py
from __future__ import absolute_import
from data.c_enlist_data import get_enlist_verify_gift
from common.cfg import confmgr
from logic.gutils import template_utils
from logic.gutils.share_utils import init_platform_list, is_share_enable
from logic.gutils.share_utils import web_share
from logic.client.const.share_const import DEEP_LINK_RECRUIT, TYPE_LINK
from logic.gutils import friend_utils

class AddRecruit(object):

    def __init__(self, main_panel):
        self.panel = main_panel
        self.init_panel()

    def init_panel(self):
        list_reward = self.panel.nd_main_reward.nd_content.list_reward
        list_reward.DeleteAllSubItem()
        reward_id = get_enlist_verify_gift()
        reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
        for item_no, num in reward_list:
            nd_item = list_reward.AddTemplateItem()
            template_utils.init_tempate_mall_i_item(nd_item, item_no, show_tips=True)

        self.panel.nd_main_reward.nd_desc.setString(get_text_by_id(10312))
        self.panel.nd_invite_tips.nd_desc.setString(get_text_by_id(10301))
        self.panel.nd_share.nd_desc.setString(get_text_by_id(10302))
        uid = global_data.player.uid
        self.panel.nd_invite_tips.nd_content.lab_invite_code.SetStringWithChildRefresh(get_text_by_id(10314).format(uid))
        btn_copy = self.panel.nd_invite_tips.nd_content.lab_invite_code.btn_copy

        @btn_copy.callback()
        def OnClick(*args):
            import game3d
            game3d.set_clipboard_text(str(global_data.player.uid))
            global_data.game_mgr.show_tip(get_text_by_id(10053))

        self.init_recruit_desc()
        if is_share_enable():

            def share_callback(info):
                if global_data.channel.is_guest():
                    global_data.channel.guest_bind()
                else:
                    platform_enum = info.get('platform_enum', None)
                    if platform_enum is None:
                        return
                    key_word = '%s=%s' % (DEEP_LINK_RECRUIT, str(global_data.player.uid))
                    web_share(key_word, platform_enum)
                    friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_SHARE_VIA_RECRUIT)
                return

            init_platform_list(self.panel.nd_share.nd_content.list_share, share_callback, share_type=TYPE_LINK)

    def init_recruit_desc(self):
        nd_step = self.panel.nd_invite_tips.nd_content.nd_step
        nd_step.nd_1.lab_title.setString(get_text_by_id(10315))
        nd_step.nd_1.lab_describe.setString(get_text_by_id(10316))
        nd_step.nd_2.lab_title.setString(get_text_by_id(10317))
        nd_step.nd_2.lab_describe.setString(get_text_by_id(10318))
        nd_step.nd_3.lab_title.setString(get_text_by_id(10319))
        nd_step.nd_3.lab_describe.setString(get_text_by_id(10320))

    def show_panel(self):
        self.panel.nd_main_reward.setVisible(True)
        self.panel.nd_invite_tips.setVisible(True)
        self.panel.nd_share.setVisible(True and is_share_enable())

    def hide_panel(self):
        self.panel.nd_main_reward.setVisible(False)
        self.panel.nd_invite_tips.setVisible(False)
        self.panel.nd_share.setVisible(False)

    def destroy(self):
        self.panel = None
        return