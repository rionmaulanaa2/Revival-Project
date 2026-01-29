# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartPVEStoryManager.py
from __future__ import absolute_import
from __future__ import print_function
import six
from . import ScenePart
from common.cfg import confmgr
from mobile.common.EntityManager import EntityManager
from logic.comsys.battle.pve.PVEStoryUI import PVEStoryUI
import six_ex
from logic.gcommon.item.item_const import ITEM_NO_PVE_STORY_DEBRIS

class PartPVEStoryManager(ScenePart.ScenePart):
    INIT_EVENT = {'pve_start_read_dialog_event': 'on_pve_start_read_dialog',
       'pve_stop_read_dialog_event': 'on_pve_stop_read_dialog'
       }

    def __init__(self, scene, name):
        super(PartPVEStoryManager, self).__init__(scene, name, True)
        self.lplayer = None
        return

    def on_pve_start_read_dialog(self, lplayer, story_data):
        ui = global_data.ui_mgr.get_ui('PVEStoryUI')
        if not ui:
            PVEStoryUI(lplayer=lplayer, story_data=story_data)
            from logic.comsys.battle.BattleUtils import stop_self_fire_and_movement
            stop_self_fire_and_movement()
            self.set_block_control(True)

    def on_pve_stop_read_dialog(self, lplayer):
        ui = global_data.ui_mgr.get_ui('PVEStoryUI')
        if ui:
            ui.play_disappear_anim()
        self.set_block_control(False)

    def set_block_control(self, is_block):
        if not global_data.pc_ctrl_mgr:
            return
        from data import hot_key_def
        for hotkey_name in hot_key_def.ALL_HOTKEY_SET:
            if is_block:
                global_data.pc_ctrl_mgr.block_hotkey(hotkey_name, 'SHOWING_PVE_DIALOG')
            else:
                global_data.pc_ctrl_mgr.unblock_hotkey(hotkey_name, 'SHOWING_PVE_DIALOG')