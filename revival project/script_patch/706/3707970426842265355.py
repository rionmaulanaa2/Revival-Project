# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impPlace.py
from __future__ import absolute_import
import six

class impPlace(object):

    def _init_place_from_dict(self, bdict):
        self.destroy_place_func_map = {'battle': self.destroy_battle,
           'lobby': self.destroy_lobby,
           'town': self.destroy_town
           }
        self.player_place_type = None
        return

    def destroy_battle(self):
        battle = self.get_battle() or self.get_joining_battle()
        if battle:
            battle.destroy()
            battle = None
        if self.is_in_global_spectate():
            self.destroy_global_spectate()
        return

    def get_place(self):
        return self.player_place_type

    def enter_place(self, place_type):
        self.player_place_type = place_type
        for k, v in six.iteritems(self.destroy_place_func_map):
            if k != place_type:
                v()

    def destroy_lobby(self):
        lobby = self.get_lobby()
        if lobby:
            lobby.destroy()
            lobby = None
        return

    def destroy_town(self):
        town = self.get_town()
        if town:
            town.destory()
            town = None
        self.quit_town()
        return