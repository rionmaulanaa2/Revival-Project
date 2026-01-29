# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLoadUEEnv.py
from __future__ import absolute_import
from . import ScenePart

class PartLoadUEEnv(ScenePart.ScenePart):

    def on_enter(self):
        if global_data.is_ue_model and global_data.feature_mgr.is_dynamic_ue_env_config():
            self.scene().load_env('default_nx2_mobile.xml')