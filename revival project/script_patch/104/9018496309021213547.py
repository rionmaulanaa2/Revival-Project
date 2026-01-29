# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHidingAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
import world
import math3d
import weakref
import game3d
from common.cfg import confmgr

class ComHidingAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'G_YAW': '_get_yaw',
       'G_CHECK_ENTER_CONSOLOE_ZONE': '_check_enter_zone',
       'E_HEALTH_HP_EMPTY': '_on_explode',
       'E_HIDING_ADD_SOUL': '_add_soul',
       'E_HIDING_DEL_SOUL': '_del_soul',
       'E_HIT_BLOOD_SFX': '_on_be_hited'
       })

    def __init__(self):
        super(ComHidingAppearance, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComHidingAppearance, self).init_from_dict(unit_obj, bdict)
        self._trigger_radius = 30.0
        self._trigger_height = 20.0
        self._hiding_id = bdict['hiding_id']

    def _get_yaw(self):
        if self.model:
            return self.model.world_rotation_matrix.yaw
        return 0

    def _check_enter_zone(self, pos):
        if self.model:
            model_pos = self.model.world_position
            lpos = pos - model_pos
            height = lpos.y
            lpos.y = 0
            radius = lpos.length
            if radius <= self._trigger_radius and abs(height) < self._trigger_height:
                return (True, radius)
        return (
         False, None)

    def _on_explode(self, *args):
        sfx_path = 'effect/fx/weapon/gaobaozhayao/heavy_weapons_bomb.sfx'
        if sfx_path and self.model:
            global_data.sfx_mgr.create_sfx_in_scene(sfx_path, self.model.world_position, duration=1)

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rotation = bdict.get('yaw', 0)
        data = {'pos': math3d.vector(*pos),'rotation': rotation}
        model_path = confmgr.get('hiding_data', str(bdict['hiding_id']))['cModel']
        return (
         model_path, None, data)

    def on_load_model_complete(self, model, userdata):
        from mobile.common.EntityManager import EntityManager
        import math3d
        model.position = userdata['pos']
        m = math3d.matrix.make_rotation_y(userdata['rotation'])
        model.rotation_matrix = m
        global_data.emgr.scene_add_console.emit(self.unit_obj.id, self.unit_obj.get_owner())
        soul_id = self.unit_obj.ev_g_hiding_soul()
        if soul_id:
            target = EntityManager.getentity(soul_id)
            if target and target.logic and target.logic.is_enable():
                target.logic.send_event('E_ENTER_HIDING', self.unit_obj.id)

    def _add_soul(self, *args):
        if self.model:
            self.model.play_animation('open')

    def _del_soul(self, *args):
        if self.model:
            self.model.play_animation('open')

    def destroy(self):
        super(ComHidingAppearance, self).destroy()