# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPhotonTowerShield.py
from __future__ import absolute_import
from __future__ import print_function
import world
import math3d
import collision
import render
import game3d
from common.cfg import confmgr
from mobile.common.EntityManager import EntityManager
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import scene_const
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const.collision_const import BUILDING_GROUP, GROUP_GRENADE, GROUP_SHOOTUNIT, GROUP_SHIELD, GROUP_AUTO_AIM
from .ComBaseModelAppearance import ComBaseModelAppearance
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
from logic.gutils.effect_utils import check_need_ignore_effect_behind_camera
_HASH_SKEY_Y = game3d.calc_string_hash('Vertex_skew_y')

class ComPhotonTowerShield(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_BUILDING_CHANGE_HP': '_on_hp_change',
       'E_HIT_BLOOD_SFX': '_on_be_hited',
       'G_CHECK_SHOOT_INFO': '_check_shoot_info'
       })

    def __init__(self):
        super(ComPhotonTowerShield, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComPhotonTowerShield, self).init_from_dict(unit_obj, bdict)
        self._info = bdict
        self._building_no = bdict.get('building_no', 6020)
        self._owner_ids = bdict.get('adjacent_towers', [None, None])
        self._towers_pos = bdict.get('towers_pos')
        building_conf = confmgr.get('c_building_res', str(self._building_no))
        ext_conf = building_conf.get('ExtInfo')
        scale = ext_conf.get('scale', 1)
        self._tower_height = ext_conf.get('height', 46) * scale
        self.col = None
        self.idle_sound_player_id = None
        return

    def _on_hp_change(self, hp):
        self.send_event('E_HEALTH_HP_CHANGE', hp)
        if hp <= 0:
            if self._model and self._model.valid:
                global_data.sound_mgr.play_event('m_8008_shield_break_3p', self._model.world_position)

    def _check_shoot_info(self, begin, pdir, hit_pos=None):
        return 0

    def _on_be_hited(self, begin_pos, end_pos, shot_type, **kwargs):
        global_data.sound_mgr.play_sound_optimize('m_8008_shield_hit_3p', self.unit_obj, end_pos, ('m_8008_shield_hit_3p',
                                                                                                   'nf'))
        if check_need_ignore_effect_behind_camera(shot_type, end_pos):
            return
        else:
            if shot_type:
                sfx_path = confmgr.get('firearm_res_config', str(shot_type), 'cSfxHit')
                if sfx_path:
                    global_data.sfx_mgr.create_sfx_in_scene(sfx_path, end_pos, duration=0.5, int_check_type=CREATE_SRC_SIMPLE)
                    return
            col_type = kwargs.get('col_type', None)
            hit_sfx_path = ('effect/fx/weapon/bullet/jinshu.sfx', 'effect/fx/weapon/bullet/jinshu_dankong.sfx')
            if col_type:
                hit_sfx_path = scene_const.collision_sfx_map.get(col_type, hit_sfx_path)
            global_data.sfx_mgr.create_sfx_in_scene(hit_sfx_path[0], end_pos, int_check_type=CREATE_SRC_SIMPLE)
            return

    def on_load_model_complete(self, model, user_data):
        if not self._owner_ids or not len(self._owner_ids) == 2:
            return
        else:
            owner_1 = EntityManager.getentity(self._owner_ids[0])
            owner_2 = EntityManager.getentity(self._owner_ids[1])
            if not (owner_1 and owner_1.logic and owner_2 and owner_2.logic):
                return
            owner_1.logic.send_event('E_PHOTON_SHIELD_STATE', True)
            owner_2.logic.send_event('E_PHOTON_SHIELD_STATE', True)
            pos_1, top_pos_1 = owner_1.logic.ev_g_shield_pos()
            pos_2, top_pos_2 = owner_2.logic.ev_g_shield_pos()
            if top_pos_2 is None or top_pos_1 is None:
                top_pos_1 = pos_1 + math3d.vector(0, self._tower_height, 0)
                top_pos_2 = pos_2 + math3d.vector(0, self._tower_height, 0)
            center = (pos_1 + top_pos_2) * 0.5
            center = math3d.vector(center.x, center.y - (pos_1.y - pos_2.y) / 2, center.z)
            xz_pos1 = math3d.vector(pos_1.x, 0, pos_1.z)
            xz_pos2 = math3d.vector(pos_2.x, 0, pos_2.z)
            mask = GROUP_GRENADE | GROUP_SHOOTUNIT | GROUP_AUTO_AIM
            group = BUILDING_GROUP | GROUP_SHOOTUNIT | GROUP_SHIELD | GROUP_AUTO_AIM
            col_obj = collision.col_object(collision.VERTS, [[pos_1 - center, top_pos_1 - center, pos_2 - center, top_pos_2 - center],
             [
              0, 1, 2, 1, 3, 2, 1, 0, 2, 1, 2, 3]], mask, group)
            global_data.game_mgr.scene.scene_col.add_object(col_obj)
            col_obj.position = center
            self.col = col_obj
            global_data.emgr.scene_add_common_shoot_obj.emit(self.col.cid, self.unit_obj)
            self._model.all_materials.set_var(_HASH_SKEY_Y, 'Vertex_skew_y', (pos_1.y - pos_2.y, 0.0))
            self._model.all_materials.rebuild_tech()
            self._model.world_position = center
            scale_x = (xz_pos2 - xz_pos1).length / self._model.bounding_box.x
            scale_y = (top_pos_1.y - pos_1.y) / self._model.bounding_box.y
            dir1 = xz_pos1 - xz_pos2
            forward = dir1.cross(math3d.vector(0, 1, 0))
            rot = math3d.matrix.make_orient(forward, math3d.vector(0, 1, 0))
            self._model.scale = math3d.vector(scale_x * 0.5, scale_y * 0.5, 1)
            self._model.rotation_matrix = rot
            box = self._model.bounding_box
            box.y = box.y / 2.0
            self.send_event('E_MODEL_LOADED', self._model, box)
            return

    def get_model_info(self, unit_obj, bdict):
        from common.cfg import confmgr
        building_no = bdict.get('building_no', 6020)
        building_conf = confmgr.get('c_building_res', str(building_no))
        model_path = building_conf['ResPath']
        return (
         model_path, None, None)

    def _load_callback(self, model, user_data, use_idx):
        if not self.is_enable(use_idx):
            try:
                model.destroy()
            except Exception as e:
                print('[_load_callback] model has been remove form sceen %s' % self.__class__.__name__, '--error = ', str(e))
                import traceback
                traceback.print_stack()

            return
        self._model = model
        if model:
            scene = self.scene
            if scene:
                scene.add_object(model)
            self._bind_event(self.BIND_LOAD_FINISH_EVENT)
            if self._is_unbind_model_event:
                self._unbind_event(self._save_unbind_model_event)
                self._save_unbind_model_event = []
                self._is_unbind_model_event = False
            self.on_load_model_complete(model, user_data)
            if self.is_zhujue:
                self.do_set_zhujue(model)
                if hasattr(model, 'cast_shadow'):
                    model.cast_shadow = True
            if hasattr(model, 'decal_recievable'):
                model.decal_recievable = False

    def _destroy_self(self):
        pass

    def _remove_col(self):
        if self.col:
            global_data.emgr.scene_remove_common_shoot_obj.emit(self.col.cid)
            global_data.game_mgr.scene.scene_col.remove_object(self.col)
            self.col = None
        return

    def destroy(self):
        self._remove_col()
        owner_1 = EntityManager.getentity(self._owner_ids[0])
        owner_2 = EntityManager.getentity(self._owner_ids[1])
        if owner_1 and owner_1.logic:
            owner_1.logic.send_event('E_PHOTON_SHIELD_STATE', False)
        if owner_2 and owner_2.logic:
            owner_2.logic.send_event('E_PHOTON_SHIELD_STATE', False)
        if self.idle_sound_player_id:
            global_data.sound_mgr.stop_playing_id(self.idle_sound_player_id)
            self.idle_sound_player_id = None
        super(ComPhotonTowerShield, self).destroy()
        return