# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ShareTipsWidget.py
from __future__ import absolute_import
import six
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from common.cfg import confmgr
import logic.gcommon.time_utility as tutil
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gutils.share_utils import check_share_tips_wrapper, hide_share_tips, check_share_tips

class ShareTipsWidget(BaseUIWidget):

    def __init__(self, parent_ui, panel, share_btn, tips_text_id=3154, pos=None, mount_node=None, custom_check_func=None, json_path=None):
        if not custom_check_func:
            self.global_events = {'player_first_success_share_event': self.on_success_share}
        super(ShareTipsWidget, self).__init__(parent_ui, panel)
        from logic.gutils.share_utils import is_share_enable
        self._share_btn = None
        self._mount_node = None
        if not is_share_enable():
            if not global_data.is_share_show:
                if type(share_btn) in (str, six.text_type):
                    ctrl = self.panel
                    share_btn = ShareTipsWidget.parse_ctrl_list(ctrl, share_btn)
                share_btn.setVisible(False)
            return
        else:
            if type(share_btn) in (str, six.text_type):
                ctrl = self.panel
                share_btn = ShareTipsWidget.parse_ctrl_list(ctrl, share_btn)
            if type(mount_node) in (str, six.text_type):
                ctrl = self.panel
                mount_node = ShareTipsWidget.parse_ctrl_list(ctrl, mount_node)
            self._share_btn = share_btn
            self._mount_node = mount_node or share_btn
            check_share_tips(self._mount_node, tips_text_id, pos=pos, custom_check_func=custom_check_func, json_path=json_path)
            return

    def destroy(self):
        self._share_btn = None
        self._mount_node = None
        super(ShareTipsWidget, self).destroy()
        return

    def on_success_share(self):
        if self._mount_node:
            hide_share_tips(self._mount_node)

    @staticmethod
    def parse_ctrl_list(ctrl, ctrl_path):
        ctrlnamelist = ctrl_path.split('.')
        for name in ctrlnamelist:
            ctrl = getattr(ctrl, name)

        return ctrl