# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/MechaTips.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER
from common.utils.cocos_utils import getScreenSize, neox_pos_to_cocos
from logic.gcommon.const import NEOX_UNIT_SCALE
import math
import math3d
from logic.gutils.team_utils import limit_pos_in_screen
import cc

class MechaTips(object):
    DISTANCE_APPEAR_LENGTH = 20 * NEOX_UNIT_SCALE
    screen_size = getScreenSize()
    screen_angle_limit = math.atan(getScreenSize().height / 2.0 / (getScreenSize().width / 2.0)) * 180 / math.pi

    def __init__(self, locate_nd, panel, height, pos):
        self._nd = locate_nd
        self.panel = panel
        self._pos = math3d.vector(pos.x, pos.y + height, pos.z)
        self._is_playing = False

    def calc_nd_pos(self, camera):
        x, y = camera.world_to_screen(self._pos)
        new_x, new_y = limit_pos_in_screen(x, y)
        is_in_screen = new_x == x and new_y == y
        if is_in_screen:
            new_x, new_y = neox_pos_to_cocos(new_x, new_y)
            pos = self._nd.getParent().convertToNodeSpace(cc.Vec2(new_x, new_y))
            self._nd.setPosition(pos)
            if self._is_playing is False:
                self._nd.PlayAnimation('hint')
                self._is_playing = True
            self._nd.setVisible(True)
        else:
            if self._is_playing is True:
                self._nd.StopAnimation('hint')
                self._is_playing = False
            self._nd.setVisible(False)

    def destroy(self):
        self._nd.setVisible(False)
        self._nd.Destroy()
        self._nd = None
        return


from common.const import uiconst

class MechaTipsUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self._mecha_tips = {}
        self._timer = None
        return

    def on_finalize_panel(self):
        for _, tips in six.iteritems(self._mecha_tips):
            tips.destroy()

        self._mecha_tips.clear()
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
            self._timer = None
        return

    def update_mecha_tips(self, mecha_id, height, show, pos):
        if show:
            self._add_tips(mecha_id, height, pos)
        else:
            tips = self._mecha_tips.get(mecha_id, None)
            if tips:
                tips.destroy()
                del self._mecha_tips[mecha_id]
        if self._timer is None and self._mecha_tips:
            self._timer = global_data.game_mgr.register_logic_timer(lambda : self.tips_tick(), interval=1)
        if self._timer and not self._mecha_tips:
            global_data.game_mgr.unregister_logic_timer(self._timer)
            self._timer = None
        return

    def _add_tips(self, mecha_id, height, pos):
        if mecha_id in self._mecha_tips:
            return
        nd = global_data.uisystem.load_template_create('battle_tips/koth_tips/koth_mech_in')
        self.panel.AddChild('', nd)
        tips = MechaTips(nd, self.panel, height, pos)
        self._mecha_tips[mecha_id] = tips

    def tips_tick(self):
        camera = global_data.game_mgr.scene.active_camera
        for _, tips in six.iteritems(self._mecha_tips):
            tips.calc_nd_pos(camera)