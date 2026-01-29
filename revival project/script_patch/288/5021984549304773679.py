# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/FriendHelpShareUI.py
from __future__ import absolute_import
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from logic.client.const import share_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.gutils.share_utils import init_platform_list, share_url

class FriendHelpShareUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'activity/friend_help_platform_choose'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_plane'
    UI_ACTION_EVENT = {'temp_plane.btn_common.OnClick': 'on_click_save_btn'
       }

    def on_init_panel(self, *args, **kwargs):
        super(FriendHelpShareUI, self).on_init_panel()
        init_platform_list(self.panel.nd_share_list, share_callback=self.share_friendhelp, share_type=share_const.TYPE_LINK)

    def on_click_close_ui(self, *args):
        self.close()

    def share_friendhelp(self, share_args):
        platform = share_args.get('platform_enum', None)
        url = global_data.player.get_frd_share_url()
        if platform and url:
            share_url(url, platform)
        return