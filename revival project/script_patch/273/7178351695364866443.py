# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLiftManager.py
from __future__ import absolute_import
from . import ScenePart
from common.cfg import confmgr
import math3d
from mobile.common.EntityManager import EntityManager

class PartLiftManager(ScenePart.ScenePart):
    INIT_EVENT = {'scene_add_lift_user_event': 'add_lift_user',
       'scene_remove_lift_user_event': 'remove_lift_user',
       'scene_find_lift_user_event': 'find_lift_user'
       }

    def __init__(self, scene, name):
        super(PartLiftManager, self).__init__(scene, name)
        self.lift_users = {}

    def add_lift_user(self, cid, uid):
        self.lift_users[cid] = uid

    def remove_lift_user(self, cid):
        if cid in self.lift_users:
            del self.lift_users[cid]

    def find_lift_user(self, cid):
        if cid in self.lift_users:
            uid = self.lift_users[cid]
            entity = EntityManager.getentity(uid)
            if entity and entity.logic and entity.logic.is_valid():
                return entity.logic
        return None

    def on_enter(self):
        pass

    def on_exit(self):
        self.lift_users = {}