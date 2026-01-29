# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComLightShieldAppearance.py
from __future__ import absolute_import
import six
import world
import math3d
from mobile.common.EntityManager import EntityManager
from .ComBaseModelAppearance import ComBaseModelAppearance
from logic.gcommon.common_const import scene_const
from logic.gcommon.common_const import building_const
from logic.gcommon import time_utility as tutil
from common.cfg import confmgr

class ComLightShieldAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_BUILDING_CHANGE_HP': '_on_hp_change',
       'E_BUILDING_DONE': '_on_building_done',
       'E_HITED': '_on_hited',
       'E_ADD_THROW_OBJ': '_on_add_throw_obj',
       'E_DEL_THROW_OBJ': '_on_del_throw_obj',
       'G_HP_POSITION': '_on_get_hp_pos',
       'G_BUILDING_NO': '_on_get_building_no',
       'G_BUILD_TIME': '_on_get_birthtime',
       'G_REMAIN_TIME': '_on_get_remaintime',
       'G_IS_CAMPMATE': '_on_get_is_teammate'
       })

    def __init__(self):
        super(ComLightShieldAppearance, self).__init__()
        self._thow_objs = {}

    def init_from_dict(self, unit_obj, bdict):
        self._building_no = bdict.get('building_no', None)
        self._build_done = bdict.get('status', building_const.BUILDIND_ST_DONE) == building_const.BUILDIND_ST_DONE
        self._birth_time = bdict.get('birthtime', None)
        self._faction_id = bdict.get('faction_id', None)
        self._owner_id = bdict['owner_id']
        self.conf = confmgr.get('c_building_res', str(self._building_no))
        self.model_path = self.conf['ResPath']
        self.life_time = self.conf['LifeTime']
        super(ComLightShieldAppearance, self).init_from_dict(unit_obj, bdict)
        return

    def reuse(self, share_data):
        super(ComLightShieldAppearance, self).reuse(share_data)
        self._thow_objs = {}

    def cache(self):
        super(ComLightShieldAppearance, self).cache()

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rot = bdict.get('rot', [0, 0, 0, 1])
        rot = [0, 0, 0, 1] if rot is None else rot
        return (
         self.model_path, None, (pos, rot, bdict))

    def on_load_model_complete(self, model, userdata):
        import math3d
        import collision
        import render
        import game3d
        pos, rot = userdata[0], userdata[1]
        pos = math3d.vector(pos[0], pos[1], pos[2])
        mat = math3d.rotation_to_matrix(math3d.rotation(rot[0], rot[1], rot[2], rot[3]))
        model.world_position = pos
        model.rotation_matrix = mat

    def _on_building_done(self):
        self._build_done = True
        target = EntityManager.getentity(self._owner_id)
        if target and target.logic:
            target.logic.send_event('E_BUILDING_DONE')

    def _on_hp_change(self, hp):
        if not self.model or not self.model.valid:
            return
        self.send_event('E_HEALTH_HP_CHANGE', hp)

    def _on_hited(self):
        if self.model and self.model.valid:
            pos = self.model.world_position
            global_data.sound_mgr.play_sound_optimize('m_8008_shield_hit_3p', self.unit_obj, pos, ('m_8008_shield_hit_3p',
                                                                                                   'nf'))

    def on_model_destroy(self):
        if not self._build_done:
            target = EntityManager.getentity(self._owner_id)
            if target and target.logic:
                target.logic.send_event('E_BUILDING_DONE')
        self.notify_thow_obj()

    def _on_get_building_no(self):
        return self._building_no

    def _on_get_birthtime(self):
        return self._birth_time

    def _on_get_remaintime(self):
        return self._birth_time + self.life_time - tutil.time() + 1

    def _on_get_hp_pos(self):
        return self.model.position

    def _on_add_throw_obj(self, eid):
        self._thow_objs[eid] = True

    def _on_del_throw_obj(self, eid):
        if eid in self._thow_objs:
            del self._thow_objs[eid]

    def notify_thow_obj(self):
        for eid in six.iterkeys(self._thow_objs):
            obj = EntityManager.getentity(eid)
            if obj and obj.logic:
                obj.logic.send_event('E_RESET_POSITION')

        self._thow_objs.clear()

    def _on_get_is_teammate(self, other_faction_id):
        return self._faction_id == other_faction_id

    def _on_get_is_camplate(self, other_faction_id):
        return self._faction_id == other_faction_id