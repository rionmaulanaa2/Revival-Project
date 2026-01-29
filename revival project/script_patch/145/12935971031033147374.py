# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_field/ComFieldAppearance.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.component.UnitCom import UnitCom
import math3d
from common.cfg import confmgr
from mobile.common.EntityManager import EntityManager
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
from logic.gcommon.const import NEOX_UNIT_SCALE

class ComFieldAppearance(UnitCom):
    BIND_EVENT = {'E_POS_CHANGED': '_on_field_move',
       'E_FIELD_LOCK_TARGET': '_on_field_lock_target',
       'E_INIT_FIELD_SOUND': 'init_sound'
       }

    def __init__(self):
        super(ComFieldAppearance, self).__init__()
        self._mask_col = None
        self._filed_sfx = None
        self._filed_sfx_id = None
        self.sound_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComFieldAppearance, self).init_from_dict(unit_obj, bdict)
        self._faction_id = bdict.get('faction_id', None)
        self._range = bdict.get('range', 0)
        sfx_path = bdict.get('sfx_path', '')
        self.add_sfx(bdict['npc_id'], math3d.vector(*bdict['position']), sfx_path)
        return

    def _on_field_lock_target(self, lock_target_id, pos, sfx_path=None, create_id=None):
        if not sfx_path:
            return
        else:
            entity = EntityManager.getentity(lock_target_id)
            if not (entity and entity.logic):
                return
            mecha_model = None
            if create_id:
                create_entity = EntityManager.getentity(create_id)
                if create_entity and create_entity.logic:
                    if create_entity.logic.sd.ref_is_mecha:
                        mecha_model = create_entity.logic.ev_g_model()
                    else:
                        control_target = create_entity.logic.ev_g_control_target()
                        if control_target and control_target.logic:
                            mecha_model = control_target.logic.ev_g_model()

            def create_cb(sfx):
                if entity.logic and entity.logic.is_enable():
                    model = entity.logic.ev_g_model() if 1 else None
                    return model or None
                else:
                    if model and model.valid:
                        sfx.endpos_attach(model, 'fx_buff', True)
                    return

            if mecha_model:
                global_data.sfx_mgr.create_sfx_on_model(sfx_path, mecha_model, 'fx_buff', on_create_func=create_cb)
            else:
                global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos, on_create_func=create_cb, int_check_type=CREATE_SRC_SIMPLE)
            return

    def _on_field_move(self, pos):
        if pos:
            if self._filed_sfx and self._filed_sfx.valid:
                self._filed_sfx.position = pos
            if self._mask_col:
                self._mask_col.position = pos

    def add_sfx(self, npc_id, pos, sfx_path):
        field_inf = confmgr.get('field_data', str(npc_id), default={})
        if sfx_path:
            sfx_path = sfx_path if 1 else field_inf.get('cSfx')
            return sfx_path or None
        else:
            if field_inf:
                ex_data = {}
                sfx_diff = field_inf.get('cCustomParam', {}).get('camp_diff', 0)
                if sfx_diff and global_data.cam_lplayer:
                    if self._faction_id is not None and self._faction_id != global_data.cam_lplayer.ev_g_camp_id():
                        if type(sfx_diff) != int:
                            sfx_path = sfx_diff
                        else:
                            ex_data['need_diff_process'] = True
                func = lambda sfx, npc_id=npc_id: self._sfx_field_sfx_create_cb(sfx, npc_id)
                self._filed_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos, on_create_func=func, ex_data=ex_data, int_check_type=CREATE_SRC_SIMPLE)
                event = field_inf.get('cCustomParam', {}).get('sound_event', '')
                event and self.init_sound(event, pos)
            if 'iAimShieldRange' not in field_inf or field_inf['iAimShieldRange'] <= 0 or self._mask_col:
                return
            import collision
            from logic.gcommon.common_const.collision_const import GROUP_AUTO_AIM
            radius = field_inf['iAimShieldRange'] * NEOX_UNIT_SCALE
            self._mask_col = collision.col_object(collision.SPHERE, math3d.vector(radius, radius, radius), GROUP_AUTO_AIM, GROUP_AUTO_AIM, 0)
            self._mask_col.position = pos
            self._mask_col.car_undrivable = True
            self.scene.scene_col.add_object(self._mask_col)
            return

    def _sfx_field_sfx_create_cb(self, sfx, npc_id):
        field_inf = confmgr.get('field_data', str(npc_id), default={})
        self._filed_sfx = sfx
        field_range = self._range or field_inf.get('fRange', 0) * NEOX_UNIT_SCALE
        custom_param = field_inf.get('cCustomParam', {})
        if 'sfx_origin_range' in custom_param and field_range:
            scl = field_range * 1.0 / (custom_param['sfx_origin_range'] * NEOX_UNIT_SCALE)
            sfx.scale = math3d.vector(scl, scl, scl)
        if custom_param.get('use_ground_normal', False):
            from logic.gcommon.common_const.collision_const import GROUP_DEFAULT_VISIBLE
            import collision
            pos = sfx.world_position
            ret = self.scene.scene_col.hit_by_ray(pos + math3d.vector(0, 5, 0), pos - math3d.vector(0, 5, 0), 0, GROUP_DEFAULT_VISIBLE, GROUP_DEFAULT_VISIBLE, collision.INCLUDE_FILTER, False)
            if ret and ret[0]:
                forward = math3d.vector(0, 0, 1)
                up = ret[2]
                right = forward.cross(up)
                forward = up.cross(right)
                sfx.rotation_matrix = math3d.matrix.make_orient(forward, up)

    def init_sound(self, event, pos):
        self.remove_sound()
        self.sound_id = global_data.sound_mgr.play_event(event, pos)

    def remove_sound(self):
        if self.sound_id:
            global_data.sound_mgr.stop_playing_id(self.sound_id)
            self.sound_id = None
        return

    def destroy--- This code section failed: ---

 140       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'None'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_3       3 
          12  POP_JUMP_IF_FALSE    49  'to 49'

 141      15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             2  'scene'
          21  LOAD_ATTR             3  'scene_col'
          24  LOAD_ATTR             4  'remove_object'
          27  LOAD_FAST             0  'self'
          30  LOAD_ATTR             5  '_mask_col'
          33  CALL_FUNCTION_1       1 
          36  POP_TOP          

 142      37  LOAD_CONST            0  ''
          40  LOAD_FAST             0  'self'
          43  STORE_ATTR            5  '_mask_col'
          46  JUMP_FORWARD          0  'to 49'
        49_0  COME_FROM                '46'

 143      49  LOAD_FAST             0  'self'
          52  LOAD_ATTR             6  '_filed_sfx_id'
          55  POP_JUMP_IF_FALSE    98  'to 98'

 144      58  LOAD_GLOBAL           7  'global_data'
          61  LOAD_ATTR             8  'sfx_mgr'
          64  LOAD_ATTR             9  'shutdown_sfx_by_id'
          67  LOAD_FAST             0  'self'
          70  LOAD_ATTR             6  '_filed_sfx_id'
          73  CALL_FUNCTION_1       1 
          76  POP_TOP          

 145      77  LOAD_CONST            0  ''
          80  LOAD_FAST             0  'self'
          83  STORE_ATTR            6  '_filed_sfx_id'

 146      86  LOAD_CONST            0  ''
          89  LOAD_FAST             0  'self'
          92  STORE_ATTR           10  '_filed_sfx'
          95  JUMP_FORWARD          0  'to 98'
        98_0  COME_FROM                '95'

 147      98  LOAD_FAST             0  'self'
         101  LOAD_ATTR            11  'remove_sound'
         104  CALL_FUNCTION_0       0 
         107  POP_TOP          

 148     108  LOAD_GLOBAL          12  'super'
         111  LOAD_GLOBAL          13  'ComFieldAppearance'
         114  LOAD_FAST             0  'self'
         117  CALL_FUNCTION_2       2 
         120  LOAD_ATTR            14  'destroy'
         123  CALL_FUNCTION_0       0 
         126  POP_TOP          
         127  LOAD_CONST            0  ''
         130  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9