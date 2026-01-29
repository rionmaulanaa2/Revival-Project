# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Hunting/EntityHeadMarkUI.py
from __future__ import absolute_import
import six_ex
import six
import weakref
import copy
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER
import cc
import math3d
from logic.gutils.team_utils import get_teammate_colors, get_teammate_num
from logic.comsys.battle.Hunting.EntityLocateUI import EntityLocateUI
from common.const import uiconst
from logic.entities.Battle import Battle
from logic.client.const import game_mode_const
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const.battle_const import MAP_COL_BLUE, MAP_COL_GREEN, MAP_COL_RED, MAP_COL_YELLOW

class EntityHeadMarkUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'on_player_inited_event': 'add_teammate',
       'on_teammate_global_add_emoji': 'on_teammate_show_emoji',
       'on_teammate_global_remove_emoji': 'on_teammate_remove_emoji'
       }

    def on_init_panel(self):
        self.player_map = {}
        self.teammate_ids = []
        self.panel.setLocalZOrder(1)
        scn = global_data.game_mgr.scene
        self.cam = weakref.ref(scn.active_camera)
        self.color_info = MAP_COL_RED
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self._update_pos),
         cc.DelayTime.create(0.1)])))

    def do_hide_panel(self):
        super(EntityHeadMarkUI, self).do_hide_panel()
        for k, v in six.iteritems(self.player_map):
            v.hide()

    def do_show_panel(self):
        super(EntityHeadMarkUI, self).do_show_panel()
        for k, v in six.iteritems(self.player_map):
            v.show()

    def on_finalize_panel(self):
        self.clear_all_players()

    def clear_all_players(self):
        for locate in six.itervalues(self.player_map):
            locate.destroy()

        self.player_map = {}
        self.teammate_ids = []

    def add_teammate(self, player, *args):
        if player.id not in self.teammate_ids:
            return
        self.add_player(player)

    def add_player(self, player):
        if player.id in self.player_map or not global_data.is_judge_ob and global_data.cam_lplayer and player.id == global_data.cam_lplayer.id:
            if player.id in self.player_map:
                locate_wrapper = self.player_map[player.id]
                locate_wrapper.set_teammate(player)
            return
        is_teammate = player.id in self.teammate_ids
        self._add_player(player.id, player, is_teammate)

    def _add_player(self, player_id, player, is_teammate=True):
        player_num = get_teammate_num(self.teammate_ids)[player_id]
        locate_wrapper = EntityLocateUI(self.color_info, player_num, self.panel)
        if player:
            locate_wrapper.set_teammate(player)
        self.player_map[player_id] = locate_wrapper

    def del_player(self, player):
        if player:
            self.del_player_by_id(player.id)

    def del_player_by_id(self, player_id):
        if player_id in self.player_map:
            self.player_map[player_id].destroy()
            del self.player_map[player_id]

    def on_teammate_show_emoji(self, pid):
        if pid in self.player_map:
            if pid in self.teammate_ids:
                locate_wrapper = self.player_map[pid]
                locate_wrapper.add_hide_reason_set('emoji')

    def on_teammate_remove_emoji(self, pid):
        if pid in self.player_map:
            if pid in self.teammate_ids:
                locate_wrapper = self.player_map[pid]
                locate_wrapper.remove_hide_reason_set('emoji')

    def update_entity_ids(self, pids):
        self.teammate_ids = pids
        for pid in pids:
            if pid not in self.player_map:
                ent = EntityManager.getentity(pid)
                if ent and ent.logic and not ent.logic.ev_g_death():
                    self.add_player(ent.logic)

        keys = six_ex.keys(self.player_map)
        for pid in keys:
            if pid not in pids:
                self.del_player_by_id(pid)

    def _update_pos(self):
        cam = self.cam()
        if not cam:
            return
        cam_lplayer = global_data.cam_lplayer
        if cam and cam_lplayer:
            del_ids = []
            lplayer_pos = self.get_target_pos(cam_lplayer)
            for pid, locate in six.iteritems(self.player_map):
                ret = locate.update_nd_pos(cam, cam_lplayer, lplayer_pos)

    def get_target_pos(self, ltarget):
        if ltarget:
            control_target = ltarget.sd.ref_ctrl_target
            if control_target and control_target.logic:
                pos = control_target.logic.ev_g_model_position()
                return pos
        return None

    def set_color_info(self, color):
        self.color_info = color