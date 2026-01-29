# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Scavenge/ScavengeWelcomeUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.comsys.guide_ui.GuideUI import GuideUI, PCGuideUI
from logic.gcommon.common_utils.local_text import get_text_by_id

class ScavengeWelcomeUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle/empty'
    GLOBAL_EVENT = {'show_carry_bullet_empty': 'show_carry_bullet_empty_guide'
       }

    def on_init_panel(self):
        self.show_scavenge_guide()

    def on_finalize_panel(self):
        pass

    def show_scavenge_guide(self):
        if global_data.player:
            show_scavenge_guide_name = 'ScavengeGuideUI' + str(global_data.player.uid)
            show_guide_ui = global_data.achi_mgr.get_cur_user_archive_data(show_scavenge_guide_name, False)
            if not show_guide_ui:
                text = get_text_by_id(83221)
                self._guide_ui.do_show_human_tips(text, 3.0, None)
                show_scavenge_guide_name = 'ScavengeGuideUI' + str(global_data.player.uid)
                global_data.achi_mgr.set_cur_user_archive_data(show_scavenge_guide_name, True)
        return

    def show_carry_bullet_empty_guide(self):
        if global_data.player:
            show_scavenge_guide_name = 'ScavengeCBEGuideUI' + str(global_data.player.uid)
            guide_showed = global_data.achi_mgr.get_cur_user_archive_data(show_scavenge_guide_name, False)
            if not guide_showed:
                text = get_text_by_id(83225)
                self._guide_ui.do_show_human_tips(text, 3.0, None)
                show_scavenge_guide_name = 'ScavengeCBEGuideUI' + str(global_data.player.uid)
                global_data.achi_mgr.set_cur_user_archive_data(show_scavenge_guide_name, True)
        return

    @property
    def _guide_ui(self):
        if global_data.is_pc_mode:
            return PCGuideUI()
        else:
            return GuideUI()