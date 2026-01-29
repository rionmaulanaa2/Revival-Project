# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_hit_hint/ComHitHintHuman.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import logic.gcommon.common_const.animation_const as animation_const
from mobile.common.EntityManager import EntityManager

class ComHitHintHuman(UnitCom):
    BIND_EVENT = {'G_HIT_HINT_BONE': 'get_hit_hint_bone',
       'G_KILLER_INFO': 'get_killer_info',
       'E_UPDATE_KILLER': 'update_killer'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComHitHintHuman, self).init_from_dict(unit_obj, bdict)
        self._killer_id = bdict.get('killer', None)
        self._killer_pos = bdict.get('killer_pos', None)
        self._killer_camp_id = bdict.get('killer_faction', None)
        self.on_show_kill_mark(True)
        return

    def get_hit_hint_bone(self):
        return animation_const.BONE_SPINE2_NAME

    def on_show_kill_mark(self, show):
        if not self.ev_g_is_cam_player(self.unit_obj.id):
            return
        if self._killer_id:
            killer_obj = EntityManager.getentity(self._killer_id)
            if killer_obj and killer_obj.logic:
                killer_obj.logic.send_event('E_SHOW_KILL_MARK', show)
                mecha_id = killer_obj.logic.ev_g_ctrl_mecha()
                if mecha_id:
                    mecha = EntityManager.getentity(mecha_id)
                    if mecha and mecha.logic:
                        mecha.logic.send_event('E_SHOW_KILL_MARK', show)

    def update_killer(self, killer, pos, faction):
        if not killer:
            self.on_show_kill_mark(False)
        self._killer_id = killer
        self._killer_pos = pos
        self._killer_camp_id = faction
        if killer:
            self.on_show_kill_mark(True)

    def get_killer_info(self):
        return (
         self._killer_id, self._killer_pos, self._killer_camp_id)