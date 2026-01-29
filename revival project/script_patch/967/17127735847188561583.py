# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/replay/ReplayDownloadProgressUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, DIALOG_LAYER_ZORDER
from common.const import uiconst

class ReplayDownloadProgressUI(BasePanel):
    PANEL_CONFIG_NAME = 'replay/replay_download_progress'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'replay_download_progress': 'update_download_progress'
       }

    def on_init_panel(self):
        self.panel.progress.SetPercent(0)

    def on_finalize_panel(self):
        pass

    def update_download_progress(self, record_name, percentage):
        self.panel.progress.SetPercent(percentage, 1.0)
        if percentage <= 5:
            self.panel.lab_record_name.SetString(record_name)
        tip_text = '\xe5\xb7\xb2\xe4\xb8\x8b\xe8\xbd\xbd#DG%d%%#,\xe8\xaf\xb7\xe7\xa8\x8d\xe5\x90\x8e.' % percentage
        self.panel.lab_progress.SetString(tip_text)