# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/ItemTipsUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.cfg import confmgr
from logic.gutils import item_utils
from common.const import uiconst

class ItemTipsUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'message/i_item_tips_2'
    IS_PLAY_OPEN_SOUND = False

    def on_init_panel(self, **kwargs):

        @self.panel.callback()
        def OnClick(*args):
            self.close()

    def show_tips(self, item_id, item_data={}, anchor=None, pos=None):
        self.panel.lab_name.setString(item_utils.get_item_name(item_id))
        self.panel.lab_desc.setString(item_utils.get_item_desc(item_id))
        self.panel.img_item.SetDisplayFrameByPath('', item_utils.get_item_pic_by_item_no(item_id))
        if pos and anchor:
            size = self.panel.node.getContentSize()
            print(('--------', size, anchor))
            x = pos.x + size.width * anchor.x
            y = pos.y + size.height * anchor.y
            print(('---ccc-----', x, y))
            self.panel.node.SetPosition(x, y)