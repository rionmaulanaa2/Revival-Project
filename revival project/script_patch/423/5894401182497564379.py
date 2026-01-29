# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/FocusKillerUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import world
import cc
from common.const.uiconst import AIM_ZORDER, UI_TYPE_EFFECT
from common.utils.cocos_utils import ccc4, ccp
from common.utils.cocos_utils import getScreenSize
from common.utils.cocos_utils import neox_pos_to_cocos
from common.const import uiconst

class FocusKillerUI(BasePanel):
    PANEL_CONFIG_NAME = 'observe/i_model_killer'
    DLG_ZORDER = AIM_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_EFFECT

    def on_init_panel(self, focus_id):
        self.focus_id = focus_id
        self.screen_height = getScreenSize().height
        self.hide()
        self.player_pos = None
        self.init_parameters()
        self.init_ui()
        return

    def init_parameters(self):
        self.player = None
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        spectate_target = None
        if global_data.player and global_data.player.logic:
            spectate_target = global_data.player.logic.ev_g_spectate_target()
        if spectate_target and spectate_target.logic:
            self.on_player_setted(spectate_target.logic)
        elif player:
            self.on_player_setted(player)
        else:
            emgr.scene_player_setted_event += self.on_player_setted
            emgr.scene_observed_player_setted_event += self.on_player_setted
        econf = {}
        emgr.bind_events(econf)
        return

    def on_finalize_panel(self):
        pass

    def init_ui(self):
        if self.focus_id:
            self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
             cc.CallFunc.create(self.focus_entity),
             cc.DelayTime.create(0.033)])))

    def focus_entity(self):
        if not self.player_pos:
            self.hide()
            return
        import math3d
        from logic.gcommon.const import NEOX_UNIT_SCALE
        camera = global_data.game_mgr.scene.active_camera
        from mobile.common.EntityManager import EntityManager
        if self.focus_id:
            focus_entity = EntityManager.getentity(self.focus_id)
            if focus_entity and focus_entity.logic:
                con_target = focus_entity.logic.ev_g_control_target()
                if con_target and con_target.logic:
                    wpos = con_target.logic.ev_g_position()
                else:
                    wpos = focus_entity.logic.ev_g_position()
                if not wpos:
                    return
                wpos = math3d.vector(wpos)
                wpos.y += 18
                if wpos and camera:
                    pos_in_screen = camera.world_to_screen(wpos)
                    x, y = neox_pos_to_cocos(pos_in_screen[0], pos_in_screen[1])
                    lpos = self.panel.getParent().convertToNodeSpace(ccp(x, y))
                    self.panel.SetPosition(lpos.x, lpos.y)
                    length = (wpos - self.player_pos).length
                    if length > 100000000.0:
                        log_error('FocusKillerUI got an unexpected length, The pos:%s', str(wpos))
                        return
                    self.panel.lab_distance.setString(str(int(length / NEOX_UNIT_SCALE)) + 'm')
                    self.show()

    def on_player_setted(self, player):
        if player:
            self.player_pos = player.ev_g_position()