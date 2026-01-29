# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/GMHelperUIFactory.py
from __future__ import absolute_import
from .GMHelperUI import GMHelperUI
from .GMHelperUIPC import GMHelperUIPC

class GMHelperUIFactory(object):

    @staticmethod
    def create_gm_helper_ui(*args, **kwargs):
        if global_data.cam_lplayer and global_data.cam_lplayer.sd.ref_kongdao_falling:
            return
        else:
            if not global_data.game_mode:
                return
            if global_data.game_mode.is_pve():
                return
            if global_data.is_pc_mode:
                return GMHelperUIPC(*args, **kwargs)
            return GMHelperUI(*args, **kwargs)

    @staticmethod
    def close_gm_helper_ui(*args, **kwargs):
        if global_data.is_pc_mode:
            global_data.ui_mgr.close_ui('GMHelperUIPC')
        else:
            global_data.ui_mgr.close_ui('GMHelperUI')

    @staticmethod
    def get_gm_helper_ui_name(*args, **kwargs):
        if global_data.is_pc_mode:
            return 'GMHelperUIPC'
        else:
            return 'GMHelperUI'