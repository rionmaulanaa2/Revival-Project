# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/teammate/TeammateManager.py
from __future__ import absolute_import
import six
import weakref

class TeammateManager(object):
    TEAMMATE_COMS = [
     ('ComTeammateGlobalSender', 'client.com_global_sync')]

    def __init__(self):
        self._player = None
        self._teammate_map = {}
        self.process_event(True)
        return

    def destroy(self):
        self.process_event(False)
        self.clear_all_teammates()
        self._player = None
        return

    def process_event(self, is_bind):
        if is_bind:
            global_data.emgr.on_player_inited_event += self.on_entity_init
            global_data.emgr.scene_on_teammate_change += self.on_teammate_change
        else:
            global_data.emgr.on_player_inited_event -= self.on_entity_init
            global_data.emgr.scene_on_teammate_change -= self.on_teammate_change

    def set_player(self, lplayer):
        cur_lplayer = self._player() if self._player else None
        if cur_lplayer and lplayer and cur_lplayer.id == lplayer.id:
            return
        else:
            if cur_lplayer:
                self.clear_all_teammates()
                self._player = None
            if lplayer:
                self.update_teammate(lplayer)
                self._player = weakref.ref(lplayer)
            return

    def del_teammate(self, tid):
        if tid in self._teammate_map:
            teammate_ref = self._teammate_map[tid]
            if teammate_ref:
                lteammate = teammate_ref()
                self._del_coms(lteammate, self.TEAMMATE_COMS)

    def add_teammate(self, tid):
        from mobile.common.EntityManager import EntityManager
        target = EntityManager.getentity(tid)
        if target and target.logic:
            self._add_coms(target.logic, self.TEAMMATE_COMS)
            self._teammate_map[tid] = weakref.ref(target.logic)
        else:
            self._teammate_map[tid] = None
        return

    def _del_coms(self, lteammate, coms):
        if lteammate and lteammate.is_valid():
            for cname, path in coms:
                com = lteammate.get_com(cname)
                if com is not None:
                    lteammate.del_com(cname)

        return

    def _add_coms(self, lteammate, coms):
        if not lteammate or not lteammate.is_valid():
            return
        else:
            lst_complete = []
            for cname, path in coms:
                com = lteammate.get_com(cname)
                if com is None:
                    com = lteammate.add_com(cname, path)
                    com.init_from_dict(lteammate, {})
                    lst_complete.append(com)

            for com in lst_complete:
                com.on_init_complete()

            return

    def clear_all_teammates(self):
        for t_id, t_ref in six.iteritems(self._teammate_map):
            self.del_teammate(t_id)

        self._teammate_map = {}

    def on_teammate_change(self, player_id):
        if self._player:
            lplayer = self._player()
            if lplayer and lplayer.id == player_id:
                self.update_teammate(lplayer)

    def update_teammate(self, lplayer):
        if not lplayer:
            return
        teammate_ids = lplayer.ev_g_groupmate()
        for t_id in teammate_ids:
            self.add_teammate(t_id)

    def on_entity_init(self, lentity):
        if lentity:
            if lentity.id in self._teammate_map:
                self.add_teammate(lentity.id)