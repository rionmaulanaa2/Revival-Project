# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapEggWidget.py
from __future__ import absolute_import
import six
import cc
from logic.comsys.map.map_widget.MapScaleInterface import CommonMapMark

class MapEggWidget(CommonMapMark):

    def __init__(self, parent_nd, mark_no, is_deep, state, parent=None, require_follow_model=False, **kwargs):
        super(MapEggWidget, self).__init__(parent_nd, mark_no, is_deep, state, parent, require_follow_model)
        self.egg_id = kwargs.get('egg_id', None)
        self._is_bind_event = False
        self.process_event(True)
        self.init_egg_appearance()
        return

    def init_egg_appearance(self):
        egg_holder = None
        if global_data.death_battle_data:
            for holder_id, npc_id in six.iteritems(global_data.death_battle_data.egg_picker_dict):
                if npc_id == self.egg_id:
                    egg_holder = holder_id
                    break

        if egg_holder:
            from mobile.common.EntityManager import EntityManager
            ent = EntityManager.getentity(egg_holder)
            if ent and ent.logic:
                picker_faction = ent.logic.ev_g_group_id()
                self._on_egg_pick_up(egg_holder, picker_faction, self.egg_id)
            else:
                self._nd.DelayCallWithTag(1.5, self.init_egg_appearance, tag=230423)
        else:
            self.switch_egg_active_ui(None, None)
        return

    def destroy(self):
        self._nd.stopAllActions()
        self.process_event(False)
        super(MapEggWidget, self).destroy()

    def process_event(self, is_bind):
        if self._is_bind_event == is_bind:
            return
        emgr = global_data.emgr
        econf = {'snatchegg_egg_drop': self._on_egg_recover,
           'snatchegg_egg_pick_up': self._on_egg_pick_up,
           'scene_observed_player_setted_event': self.on_enter_observed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)
        self._is_bind_event = is_bind

    def on_enter_observed(self, *args):
        self.init_egg_appearance()

    def _on_egg_recover(self, holder_id, holder_faction, reason, npc_id):
        if npc_id != self.egg_id:
            return
        else:
            from logic.gcommon.common_const.battle_const import THROW_EGG
            is_on_throw = reason == THROW_EGG
            self.switch_egg_active_ui(None, None, is_on_throw=is_on_throw)
            return

    def _on_egg_pick_up(self, picker_id, picker_faction, npc_id):
        if npc_id != self.egg_id:
            return
        self.switch_egg_active_ui(picker_id, picker_faction)

    def switch_egg_active_ui(self, picker_id=None, picker_faction=None, is_on_throw=False):
        if not global_data.cam_lplayer:
            return
        else:
            if is_on_throw:
                self._nd.icon_normal.setVisible(False)
                self._nd.icon_hold_blue.setVisible(False)
                self._nd.icon_hold_red.setVisible(False)
                self._nd.icon_drop.setVisible(True)
                return
            if picker_faction is None:
                self._nd.icon_normal.setVisible(True)
                self._nd.icon_hold_red.setVisible(False)
                self._nd.icon_hold_blue.setVisible(False)
                self._nd.icon_drop.setVisible(False)
            else:
                self._nd.icon_normal.setVisible(False)
                self._nd.icon_hold_red.setVisible(False)
                self._nd.icon_hold_blue.setVisible(False)
                self._nd.icon_drop.setVisible(False)
                if picker_id:
                    if picker_faction == global_data.cam_lplayer.ev_g_group_id():
                        self._nd.icon_hold_blue.setVisible(True)
                        self._nd.icon_hold_red.setVisible(False)
                    else:
                        self._nd.icon_hold_blue.setVisible(False)
                        self._nd.icon_hold_red.setVisible(True)
                else:
                    self._nd.icon_drop.setVisible(True)
            return