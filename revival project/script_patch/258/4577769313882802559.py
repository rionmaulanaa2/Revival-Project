# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAttachableAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
from logic.gutils.skate_appearance_utils import SkateAppearanceAgent, record_skate_entity_id
import world
import math3d
import weakref
import game3d

class ComAttachableAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'G_YAW': '_get_yaw',
       'G_CHECK_ENTER_CONSOLOE_ZONE': '_check_enter_zone',
       'E_HITED': '_on_hited',
       'E_HIT_BLOOD_SFX': '_on_be_hited',
       'E_ATTACH_BROKEN': '_on_broken'
       })
    MODEL_PATH = 'model_new/vehicle/skate/6008/6008_skate.gim'

    def __init__(self):
        super(ComAttachableAppearance, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        from common.cfg import confmgr
        import math3d
        super(ComAttachableAppearance, self).init_from_dict(unit_obj, bdict)
        building_no = self.ev_g_attachable_id()
        building_conf = confmgr.get('c_building_res', str(building_no))
        ext_info = building_conf['ExtInfo']
        self._trigger_radius = ext_info['tri_radius'] * NEOX_UNIT_SCALE
        position = bdict.get('position', [0, 0, 0])
        self._position = math3d.vector(*position)
        self._fashion = bdict.get('fashion', {})
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        self._fashion_id = self._fashion.get(FASHION_POS_SUIT, None)
        self.skate_appearance_agent = SkateAppearanceAgent()
        record_skate_entity_id(self.unit_obj.id)
        return

    def _on_broken(self):
        self.skate_appearance_agent.on_skate_destroyed()

    def _on_hited(self, *args):
        if self.model:
            pos = self.model.world_position
            global_data.sound_mgr.play_sound_optimize('Play_bullet_hit', self.unit_obj, pos, ('bullet_hit_material',
                                                                                              'metal'))

    def _on_be_hited(self, begin_pos, end_pos, shot_type, **kwargs):
        if not self.model:
            return
        hit_sfx_path = 'effect/fx/weapon/bullet/jinshu.sfx'
        global_data.emgr.model_hitted_effect_event.emit(self.model, begin_pos, end_pos, hit_sfx_path)

    def _get_yaw(self):
        if self.model:
            return self.model.world_rotation_matrix.yaw
        return 0

    def _check_enter_zone(self, pos):
        if self.model:
            model_pos = self.model.world_position
            lpos = pos - model_pos
            lpos.y = 0
            length = lpos.length
            if length <= self._trigger_radius:
                return (True, length)
        return (False, None)

    def _on_pos_changed(self, pos):
        self._position = pos
        if self.model and pos:
            self.model.position = pos

    def _get_model_pos(self):
        return self._position

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rotation = bdict.get('rot', 0)
        data = {'pos': math3d.vector(*pos),'rotation': rotation}
        model_path = bdict.get('model_path', ComAttachableAppearance.MODEL_PATH)
        if self._fashion_id != None:
            from logic.gutils import dress_utils
            clothing_path = dress_utils.get_vehicle_res(self._fashion_id)
            if clothing_path != None:
                model_path = clothing_path
        return (model_path, None, data)

    def on_load_model_complete(self, model, userdata):
        self.skate_appearance_agent.on_skate_model_loaded(model)
        model.position = self._position
        global_data.emgr.scene_add_console.emit(self.unit_obj.id, self.unit_obj.get_owner())
        rot = userdata['rotation']
        mat = math3d.rotation_to_matrix(math3d.rotation(rot[0], rot[1], rot[2], rot[3]))
        model.rotation_matrix = mat

    def _on_attaching(self, unit_obj):
        pass

    def _on_detach(self, unit_obj):
        pass

    def destroy(self):
        if self.skate_appearance_agent:
            self.skate_appearance_agent.destroy()
            self.skate_appearance_agent = None
        global_data.emgr.scene_del_console.emit(self.unit_obj.id)
        super(ComAttachableAppearance, self).destroy()
        return