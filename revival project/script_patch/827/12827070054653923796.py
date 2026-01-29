# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComObjCollision.py
from __future__ import absolute_import
from __future__ import print_function
from ..UnitCom import UnitCom
import weakref

def ignore_lod_collisions(cobj):
    if not cobj:
        return
    model_name_list = cobj.model_col_name.split('_')
    if len(model_name_list) == 3 and model_name_list[2] == 'c':
        if model_name_list[0].isdigit() and model_name_list[1].isdigit():
            return True
    return False


class ComObjCollision(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_load_complete',
       'E_CHARACTER_ATTR': '_change_character_attr'
       }

    def __init__(self):
        super(ComObjCollision, self).__init__()
        self._model = None
        self._model_cache = None
        self._col_obj = None
        return

    def _change_character_attr--- This code section failed: ---

  36       0  LOAD_FAST             1  'name'
           3  LOAD_CONST            1  'dump_character'
           6  COMPARE_OP            2  '=='
           9  POP_JUMP_IF_FALSE   132  'to 132'

  37      12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             0  '_col_obj'
          18  POP_JUMP_IF_TRUE     25  'to 25'

  38      21  LOAD_CONST            0  ''
          24  RETURN_END_IF    
        25_0  COME_FROM                '18'

  40      25  LOAD_GLOBAL           1  'print'
          28  LOAD_CONST            2  'test--ComObjCollision.dump_character--cid ='
          31  LOAD_FAST             0  'self'
          34  LOAD_ATTR             0  '_col_obj'
          37  LOAD_ATTR             2  'cid'
          40  LOAD_CONST            3  '--is_character ='
          43  LOAD_FAST             0  'self'
          46  LOAD_ATTR             0  '_col_obj'
          49  LOAD_ATTR             3  'is_character'
          52  LOAD_CONST            4  '--group ='
          55  LOAD_FAST             0  'self'
          58  LOAD_ATTR             0  '_col_obj'
          61  LOAD_ATTR             4  'group'
          64  LOAD_CONST            5  '--mask ='
          67  LOAD_FAST             0  'self'
          70  LOAD_ATTR             0  '_col_obj'
          73  LOAD_ATTR             5  'mask'
          76  LOAD_CONST            6  '--self ='
          79  LOAD_CONST            7  '--unit_obj ='
          82  LOAD_FAST             0  'self'
          85  LOAD_ATTR             6  'unit_obj'
          88  BUILD_TUPLE_12       12 
          91  CALL_FUNCTION_1       1 
          94  POP_TOP          

  41      95  LOAD_GLOBAL           7  'hasattr'
          98  LOAD_FAST             0  'self'
         101  LOAD_ATTR             0  '_col_obj'
         104  LOAD_CONST            8  'dump_info'
         107  CALL_FUNCTION_2       2 
         110  POP_JUMP_IF_FALSE   132  'to 132'

  42     113  LOAD_FAST             0  'self'
         116  LOAD_ATTR             0  '_col_obj'
         119  LOAD_ATTR             8  'dump_info'
         122  CALL_FUNCTION_0       0 
         125  POP_TOP          
         126  JUMP_ABSOLUTE       132  'to 132'
         129  JUMP_FORWARD          0  'to 132'
       132_0  COME_FROM                '129'

Parse error at or near `CALL_FUNCTION_1' instruction at offset 91

    def cache(self):
        self.on_model_destroy()
        self.destroy_col()
        self._model = None
        super(ComObjCollision, self).cache()
        return

    @property
    def position(self):
        if self._col_obj:
            return self._col_obj.position
        else:
            return None

    @position.setter
    def position(self, val):
        if self._col_obj:
            self._col_obj.position = val
            m = self._model() if self._model else None
            if m:
                m.position = val
        return

    def init_from_dict(self, unit, bdict):
        super(ComObjCollision, self).init_from_dict(unit, bdict)
        if self._model is None:
            m = self.unit_obj.ev_g_model()
            if m:
                self.on_model_load_complete(m)
        return

    def on_model_load_complete(self, model):
        if not self.is_enable():
            return
        else:
            if self._model is not None:
                return
            self._model = weakref.ref(model)
            self._model_cache = model
            self._create_col_obj()
            return

    def get_collision_info(self):
        return {}

    @property
    def model(self):
        t_model = self._model()
        if t_model and t_model.valid:
            return t_model

    def _create_col_obj(self):
        self.destroy_col()
        if not self.is_enable():
            return
        else:
            import collision
            from logic.gcommon.common_const.collision_const import GROUP_CHARACTER_EXCLUDE
            if self._model:
                m = self._model() if 1 else None
                return m and m.valid or None
            collision_info_dict = self.get_collision_info()
            func = getattr(self.unit_obj, 'get_collision_info', None)
            if callable(func):
                collision_info_dict = self.unit_obj.get_collision_info()
            collision_type = collision_info_dict.get('collision_type', collision.BOX)
            bounding_box = collision_info_dict.get('bounding_box', m.bounding_box)
            mask = collision_info_dict.get('mask', GROUP_CHARACTER_EXCLUDE)
            group = collision_info_dict.get('group', GROUP_CHARACTER_EXCLUDE)
            position = collision_info_dict.get('position', m.center_w)
            mass = collision_info_dict.get('mass', 1)
            is_character = collision_info_dict.get('is_character', False)
            scn = self.scene
            self._col_obj = collision.col_object(collision_type, bounding_box, mask, group, mass)
            self._col_obj.position = position
            self._col_obj.rotation_matrix = m.rotation_matrix
            if hasattr(self._col_obj, 'is_character'):
                self._col_obj.is_character = is_character
            scn.scene_col.add_object(self._col_obj)
            return

    def on_model_destroy(self):
        pass

    def destroy_col(self):
        if self._col_obj:
            self.scene.scene_col.remove_object(self._col_obj)
        self._col_obj = None
        return

    def destroy(self):
        self.on_model_destroy()
        self.destroy_col()
        self._model = None
        self._model_cache = None
        super(ComObjCollision, self).destroy()
        return