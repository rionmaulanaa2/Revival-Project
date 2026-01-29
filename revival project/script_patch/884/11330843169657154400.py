# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/ent_visibility_utils.py
from __future__ import absolute_import
import six

class EntSimpleVisibilityMgr(object):

    def __init__(self):
        self._cur_visibility_target = False
        self._enable = False
        self._need_check_eids = []
        self.concern_types = ['Puppet', 'Avatar', 'Pet', 'Mecha']
        self.process_event(True)
        self._timer = None
        return

    def destroy(self):
        self.process_event(False)
        self.unregister_timer()

    def set_concern_types(self, types):
        self.concern_types = types

    def show_all_ent(self):
        self.set_all_ent_visibility(True)

    def hide_all_ent(self, except_list=()):
        self.set_all_ent_visibility(False, except_list=except_list)

    def set_independent_ent_list_vis(self, ent_id_list, vis):
        from mobile.common.EntityManager import EntityManager
        for eid in ent_id_list:
            v = EntityManager.getentity(eid)
            if not v.logic:
                continue
            self.set_ent_visibility(v.logic, vis)

    def set_is_enable_control(self, val):
        self._enable = val

    def set_all_ent_visibility(self, val, ent_list=(), except_list=()):
        self._cur_visibility_target = val
        if self._enable:
            self.apply_to_all_ent(ent_list, except_list)

    def apply_to_all_ent(self, ent_list=(), except_list=()):
        if not self._enable:
            return
        from mobile.common.EntityManager import EntityManager
        concern_types = self.concern_types
        for ty in concern_types:
            if not ent_list:
                all_ents = EntityManager.get_entities_by_type(ty)
            else:
                all_ents = {}
                for eid in ent_list:
                    all_ents[eid] = EntityManager.getentity(eid)

            for k, v in six.iteritems(all_ents):
                if k in except_list:
                    continue
                if not v.logic:
                    continue
                self.set_ent_visibility(v.logic, self._cur_visibility_target)

    def set_ent_visibility(self, lent, vis):
        from logic.gutils.client_unit_tag_utils import preregistered_tags
        if lent.MASK & preregistered_tags.PET_TAG_VALUE:
            lent.send_event('E_FORCE_INVIS', not vis)
            return
        else:
            event = vis or 'E_HIDE_MODEL' if 1 else 'E_SHOW_MODEL'
            lent.send_event(event)
            if lent.MASK & preregistered_tags.HUMAN_TAG_VALUE:
                con_target = lent.ev_g_control_target()
                if con_target and con_target.logic:
                    con_target.logic.send_event(event)
            elif lent.MASK & preregistered_tags.MECHA_TAG_VALUE:
                player_id = lent.ev_g_driver()
                target = global_data.battle.get_entity(player_id)
                ltarget = target.logic if target else None
                if ltarget:
                    ltarget.send_event(event)
            return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_player_animator_inited_event': self.add_ent,
           'mecha_init_event': self.add_mecha,
           'mecha_boarded_event': self.add_mecha,
           'mecha_leaved_event': self.leave_mecha
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def add_ent(self, lplayer, *args):
        if self._enable:
            if not self._cur_visibility_target:
                self.set_ent_visibility(lplayer, self._cur_visibility_target)

    def add_mecha(self, lmecha, *args):
        if self._enable:
            if not self._cur_visibility_target:
                self.set_ent_visibility(lmecha, self._cur_visibility_target)

    def leave_mecha(self, lmecha, ldriver):
        if self._enable:
            if not self._cur_visibility_target:
                self.set_ent_visibility(lmecha, self._cur_visibility_target)
                self.set_ent_visibility(ldriver, self._cur_visibility_target)
                if ldriver:
                    self._need_check_eids.append(ldriver.id)
                self.register_timer()

    def enforce_visibility(self):
        for eid in self._need_check_eids:
            target = global_data.battle.get_entity(eid)
            if target and target.logic:
                if self._enable:
                    if not self._cur_visibility_target:
                        self.set_ent_visibility(target.logic, self._cur_visibility_target)

        self._need_check_eids = []

    def unregister_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = None
        return

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.enforce_visibility, interval=1, times=1, mode=CLOCK)