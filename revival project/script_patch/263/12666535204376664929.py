# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/LetterOpenUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from common.cfg import confmgr
from common.const import uiconst

class LetterOpenUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202201/anniversary_letters/anniversary_letters_open'
    DLG_ZORDER = uiconst.TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def __init__(self, *arg, **kwargs):
        super(LetterOpenUI, self).__init__(*arg, **kwargs)