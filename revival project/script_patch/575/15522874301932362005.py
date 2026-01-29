# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/CommonBgUnAdjustUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_BAN_ZORDER
from common.const import uiconst

class CommonBgUnAdjustUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/common_bg_unadjust'
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    ASYNC_LOAD_IMAGE = False