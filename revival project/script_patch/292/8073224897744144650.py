# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/BattleFlagShareCreator.py
from __future__ import absolute_import
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper, async_disable_wrapper
from logic.gutils import battle_flag_utils

class BattleFlagShareCreator(ShareTemplateBase):
    KIND = 'BATTLE_FLAG'

    @async_disable_wrapper
    def create(self, parent=None, tmpl=None, is_role=False):
        super(BattleFlagShareCreator, self).create(parent)
        self.init_info(is_role)

    def init_info(self, is_role):
        battle_flag_utils.init_battle_flag_tempate_share(battle_flag_utils.get_battle_info_by_player(global_data.player), self.panel, is_role)