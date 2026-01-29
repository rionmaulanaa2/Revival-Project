# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/GameLimitDescUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst
import common.utilities
from common.cfg import confmgr
from logic.gutils.item_utils import init_limit_describe_tag

class GameLimitDescUI(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/limit_describe'
    DLG_ZORDER = common.const.uiconst.GUIDE_LAYER_ZORDER
    UI_VKB_TYPE = common.const.uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {}

    def on_init_panel(self, *args, **kargs):
        self.on_init_btn()

    def on_init_btn(self):

        @self.panel.callback()
        def OnClick(btn, touch):
            self.close()

    def set_show_limit_desc(self, item_no, limit_tag, kwargs):
        tag_conf = confmgr.get('skin_card_tag_conf', 'TagConf', 'Content', str(limit_tag), default={})
        init_limit_describe_tag(self.panel.nd_limit.temp_limit, item_no, limit_tag, kwargs)
        self.panel.nd_limit.lab_describe.SetString(tag_conf.get('tag_text', ''))

    def set_node_pos(self, wpos, anchor):
        import cc
        from logic.gutils import template_utils
        self.panel.nd_limit.setAnchorPoint(anchor)
        template_utils.set_node_position_in_screen(self.panel.nd_limit, self.panel, wpos)