# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/NewSeasonUISea.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from .NewSeasonUI import NewSeasonUI
import common.const.uiconst as ui_const
import logic.gutils.season_utils as season_utils
from common.const import uiconst
import time

class NewSeasonUISea(NewSeasonUI):
    PANEL_CONFIG_NAME = 'season/season_s7_fg'
    VIDEO_PATH = 'video/season_7_logo.mp4'
    DLG_ZORDER = ui_const.NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_close.OnClick': 'try_close'
       }
    UI_OPEN_SOUND = 'season_logo'