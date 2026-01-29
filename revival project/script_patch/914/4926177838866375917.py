# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/LobbyPuppet.py
from __future__ import absolute_import
from mobile.common.EntityManager import Dynamic
from logic.entities.LobbyNPC import LobbyNPC
import math3d

@Dynamic
class LobbyPuppet(LobbyNPC):

    def __init__(self, entityid=None):
        super(LobbyPuppet, self).__init__(entityid)
        self.uid = None
        return

    def init_from_dict(self, bdict):
        self.uid = bdict.get('uid')
        bdict['is_puppet'] = True
        super(LobbyPuppet, self).init_from_dict(bdict)

    def get_uid(self):
        return self.uid

    def on_spray(self, spray_id, lst_pos, lst_elr_rot, ex_data):
        from logic.gutils.interaction_utils import create_spray_sfx
        bdict = {'position': lst_pos,
           'euler_rotation': lst_elr_rot,
           'create_time': ex_data.get('create_time'),
           'spray_id': spray_id
           }
        create_spray_sfx(bdict)

    def on_gesture(self, role_id, gesture_id):
        if self.logic and self.logic.ev_g_role_id() == role_id:
            self.logic.send_event('E_LOBBY_CELEBRATE', gesture_id, True)

    def on_emoji(self, emoji_id, mecha_skin_no, mecha_skin_kill_cnt):
        if self.logic:
            self.logic.send_event('E_EMOJI', emoji_id, mecha_skin_no, mecha_skin_kill_cnt)

    def on_jump(self, jump_state, extra_args):
        if not self.logic or jump_state is None:
            return
        else:
            self.logic.send_event('E_SIMPLE_SYNC_JUMP', jump_state, *extra_args)
            return

    def on_climb(self, climb_type, lst_climb_pos, climb_rotation):
        if not self.logic:
            return
        if not climb_type or not lst_climb_pos or not climb_rotation:
            return
        climb_pos = math3d.vector(*lst_climb_pos)
        self.logic.send_event('E_SIMPLE_SYNC_CLIMB', climb_type, climb_pos, climb_rotation)