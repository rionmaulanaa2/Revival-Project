# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/MechaInfoShareCreator.py
from __future__ import absolute_import
from logic.gutils.end_statics_utils import init_end_person_statistics, init_end_teammate_statics
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper

class MechaInfoShareCreator(ShareTemplateBase):
    KIND = 'MECHA_INFO_SHARE'

    def set_mecha_type(self, mecha_type):
        from logic.gutils.share_utils import set_mecha_share_battle_stat
        set_mecha_share_battle_stat(self.panel.list_info, mecha_type)

    def set_show_record(self, is_show):
        self.panel.list_info.setVisible(is_show)