# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/intimacy/IntimacyManage.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE

class IntimacyManage(BasePanel):
    PANEL_CONFIG_NAME = 'friend/i_intimacy_my_manage'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_bg.OnClick': 'close',
       'btn_edit.OnClick': 'on_click_edit',
       'btn_remove.OnClick': 'on_click_remove'
       }

    def on_init_panel(self, *args, **kwargs):
        self.edit_callback = kwargs.get('edit_cb', None)
        self.remove_callback = kwargs.get('remove_cb', None)
        self.close_on_click = kwargs.get('close_on_click', True)
        nd_manage_pos = kwargs.get('nd_manage_pos', None)
        if nd_manage_pos:
            self.panel.nd_manage.SetPosition(nd_manage_pos.x, nd_manage_pos.y)
        return

    def on_click_edit(self, *args):
        callable(self.edit_callback) and self.edit_callback()
        if self.close_on_click:
            self.close()

    def on_click_remove(self, *args):
        callable(self.remove_callback) and self.remove_callback()
        if self.close_on_click:
            self.close()