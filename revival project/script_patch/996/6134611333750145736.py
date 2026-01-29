# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ShareScreenCaptureUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
import social
from logic.client.const import share_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const import uiconst

class ShareScreenCaptureUI(BasePanel):
    PANEL_CONFIG_NAME = 'share/share_screenshot'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn',
       'bg_layer.OnClick': 'on_click_bg_layer'
       }

    def on_init_panel(self, *arg, **kwargs):
        self._file_ready = False
        self._priority_image_path = ''
        self._share_link = kwargs.get('share_link', '')
        self._share_title = kwargs.get('share_title', None)
        self._share_message = kwargs.get('share_message', None)
        self._share_cb = kwargs.get('share_cb', None)
        show_text = kwargs.get('text', None)
        if show_text != None:
            self.panel.lab_tips.SetString(show_text)
        self.panel.PlayAnimation('appear')
        self.init_platform_list()
        return

    def get_exclude_platforms(self):
        return []

    def on_click_close_btn(self, *args):
        self.close()

    def init_platform_list(self):
        share_type = share_const.TYPE_LINK if self._share_link else share_const.TYPE_IMAGE
        from logic.comsys.share.ShareManager import ShareManager
        exclude_list = self.get_exclude_platforms()
        platform_list = ShareManager().get_support_platform(share_type)
        platform_list = [ pt for pt in platform_list if pt.get('share_args', {}).get('platform_enum', 0) not in exclude_list ]
        self.panel.nd_share_btn.SetInitCount(len(platform_list))
        for idx, pf_info in enumerate(platform_list):
            ui_item = self.panel.nd_share_btn.GetItem(idx)
            if not ui_item:
                continue
            self._init_platform_btn(ui_item, pf_info)

    def _init_platform_btn(self, nd, data):
        pic = data.get('pic', '')
        share_args = data.get('share_args', ())
        nd.btn_share.SetFrames('', [pic, pic, pic], False, None)

        @nd.btn_share.unique_callback()
        def OnClick(btn, touch):
            if self._share_link:
                global_data.share_mgr.share(share_args, share_const.TYPE_LINK, '', link=self._share_link, title=self._share_title, message=self._share_message, share_cb=self._share_cb)
            elif self._file_ready:
                from logic.comsys.share.ShareManager import ShareManager
                ShareManager().share_screen_capture(share_args)
                self.close()
            else:
                global_data.game_mgr.show_tip(get_text_by_id(2182))

        return

    def on_file_ready(self):
        self._file_ready = True

    def on_click_bg_layer(self, layer, touch):
        self.close()

    def set_priority_image_path(self, image_path):
        self._priority_image_path = image_path