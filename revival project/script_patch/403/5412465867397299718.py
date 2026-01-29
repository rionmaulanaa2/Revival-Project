# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/TeachingStepsUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id

class TeachingStepsUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_community/i_activity_weixin_3'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_close.OnClick': 'on_click_nd_close'
       }

    def on_init_panel(self, *args, **kwargs):
        self.step_icon_list = [
         self.panel.img_1, self.panel.img_2, self.panel.img_3]
        self.step_text_list = [self.panel.lab_text1, self.panel.lab_text2, self.panel.lab_text3]
        content_dict = kwargs.get('content_dict', None)
        if content_dict:
            self.set_content(content_dict)
        self.panel.PlayAnimation('appear')
        return

    def on_click_nd_close(self, *args):
        self.close()

    def set_content(self, content_dict):
        title_icon_path = content_dict.get('title_icon_path', None)
        if title_icon_path:
            self.panel.img_title.SetDisplayFrameByPath('', title_icon_path)
        title_text_id = content_dict.get('title_text_id', None)
        if title_text_id:
            self.panel.img_title.setVisible(False)
            self.panel.lab_title.SetString(get_text_by_id(title_text_id))
        step_icon_path_list = content_dict.get('step_icon_path_list', [])
        for idx, icon_path in enumerate(step_icon_path_list):
            if idx >= len(self.step_icon_list):
                return
            self.step_icon_list[idx].SetDisplayFrameByPath('', icon_path)

        step_text_id_list = content_dict.get('step_text_id_list', [])
        for idx, text_id in enumerate(step_text_id_list):
            if idx >= len(self.step_text_list):
                return
            self.step_text_list[idx].SetString(get_text_by_id(text_id))

        extra_tip_text_id = content_dict.get('extra_tip_text_id', None)
        if extra_tip_text_id:
            self.panel.lab_tips.SetString(get_text_by_id(extra_tip_text_id))
        return