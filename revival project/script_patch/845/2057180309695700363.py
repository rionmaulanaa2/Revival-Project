# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/TrackImp/Dummy.py
from __future__ import absolute_import
from UniCineDriver.Movie.MovieObject import MovieGroupCls, MovieTrackCls
from .EntityBase import UEntityBase
from ..TrackImp.UniHelper import euler_angle_to_rotation_matrix
import math3d
import world
from .UniHelper import euler_angle_to_direction, get_active_scene
import MontageSDK

class VirtualObj(object):

    def __init__(self, v3Pos, v3Rot, create_model_callback=None):
        self.m_model = None
        self.m_v3Pos = v3Pos
        self.m_v3Rot = v3Rot
        self.m_v3OldPos = math3d.vector(v3Pos.x, v3Pos.y, v3Pos.z)
        self.m_v3OldRot = math3d.vector(v3Rot.x, v3Rot.y, v3Rot.z)
        self.callbackEx = create_model_callback
        world.create_model_async(self.m_szModelPath, self.create_model_callback)
        return

    def create_model_callback--- This code section failed: ---

  24       0  LOAD_FAST             1  'obj'
           3  LOAD_FAST             0  'self'
           6  STORE_ATTR            0  'm_model'

  25       9  LOAD_GLOBAL           1  'hasattr'
          12  LOAD_GLOBAL           1  'hasattr'
          15  CALL_FUNCTION_2       2 
          18  POP_JUMP_IF_FALSE    36  'to 36'

  26      21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             2  'name'
          27  LOAD_FAST             1  'obj'
          30  STORE_ATTR            2  'name'
          33  JUMP_FORWARD          0  'to 36'
        36_0  COME_FROM                '33'

  27      36  LOAD_FAST             0  'self'
          39  LOAD_ATTR             3  'm_v3Pos'
          42  LOAD_FAST             0  'self'
          45  LOAD_ATTR             0  'm_model'
          48  STORE_ATTR            4  'position'

  28      51  LOAD_FAST             0  'self'
          54  LOAD_ATTR             5  'adjust_scale'
          57  CALL_FUNCTION_0       0 
          60  POP_TOP          

  29      61  LOAD_GLOBAL           6  'euler_angle_to_direction'
          64  LOAD_FAST             0  'self'
          67  LOAD_ATTR             7  'm_v3Rot'
          70  CALL_FUNCTION_1       1 
          73  UNPACK_SEQUENCE_3     3 
          76  STORE_FAST            4  'v3Forward'
          79  STORE_FAST            5  '_'
          82  STORE_FAST            6  'v3Up'

  30      85  LOAD_FAST             0  'self'
          88  LOAD_ATTR             0  'm_model'
          91  POP_JUMP_IF_FALSE   175  'to 175'
          94  LOAD_FAST             0  'self'
          97  LOAD_ATTR             0  'm_model'
         100  LOAD_ATTR             8  'valid'
       103_0  COME_FROM                '91'
         103  POP_JUMP_IF_FALSE   175  'to 175'

  31     106  LOAD_FAST             0  'self'
         109  LOAD_ATTR             0  'm_model'
         112  LOAD_ATTR             9  'set_placement'
         115  LOAD_FAST             0  'self'
         118  LOAD_ATTR             3  'm_v3Pos'
         121  LOAD_FAST             4  'v3Forward'
         124  LOAD_FAST             6  'v3Up'
         127  CALL_FUNCTION_3       3 
         130  POP_TOP          

  32     131  LOAD_GLOBAL          10  'True'
         134  DUP_TOP          
         135  LOAD_FAST             0  'self'
         138  LOAD_ATTR             0  'm_model'
         141  STORE_ATTR           11  'visible'
         144  LOAD_FAST             0  'self'
         147  LOAD_ATTR             0  'm_model'
         150  STORE_ATTR           12  'pickable'

  33     153  LOAD_GLOBAL          13  'get_active_scene'
         156  CALL_FUNCTION_0       0 
         159  LOAD_ATTR            14  'add_object'
         162  LOAD_FAST             0  'self'
         165  LOAD_ATTR             0  'm_model'
         168  CALL_FUNCTION_1       1 
         171  POP_TOP          
         172  JUMP_FORWARD          0  'to 175'
       175_0  COME_FROM                '172'

  34     175  LOAD_GLOBAL          15  'callable'
         178  LOAD_FAST             0  'self'
         181  LOAD_ATTR            16  'callbackEx'
         184  CALL_FUNCTION_1       1 
         187  POP_JUMP_IF_FALSE   212  'to 212'

  35     190  LOAD_FAST             0  'self'
         193  LOAD_ATTR            16  'callbackEx'
         196  LOAD_FAST             1  'obj'
         199  LOAD_FAST             2  'userData'
         202  LOAD_FAST             3  'currentTask'
         205  CALL_FUNCTION_3       3 
         208  POP_TOP          
         209  JUMP_FORWARD          0  'to 212'
       212_0  COME_FROM                '209'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 15

    @property
    def model(self):
        return self.m_model

    @property
    def valid(self):
        return self.m_model and self.m_model.valid

    def clear_data(self):
        if self.m_model and self.m_model.valid:
            self.m_model.destroy()
            self.m_model = None
        return

    def adjust_scale(self):
        pass


class DummyObj(VirtualObj):

    def __init__(self, v3Pos, v3Rot, name, cb=None):
        self.m_szModelPath = 'model/monster/wu/wu.gim'
        super(DummyObj, self).__init__(v3Pos, v3Rot, cb)
        self.name = name

    def adjust_scale(self):
        self.m_model.scale = math3d.vector(0.05, 0.05, 0.05)
        self.m_model.world_scale = math3d.vector(0.05, 0.05, 0.05)


@MovieGroupCls('Dummy')
class UDummy(UEntityBase):

    def __init__(self, data, blackboard):
        super(UDummy, self).__init__(data, blackboard)
        self.m_bIsRemoved = False
        self._updatePending = False
        self.dummyObj = None
        return

    @property
    def model(self):
        if self.dummyObj is None or self.dummyObj.model is None or not self.dummyObj.model.valid:
            return
        else:
            return self.dummyObj.model

    @property
    def rot(self):
        from ..MontEditComponent import rotation_matrix_to_euler_angle
        mat = self.model.world_rotation_matrix
        rot = rotation_matrix_to_euler_angle(mat)
        return {'Roll': round(rot.z, 3),
           'Pitch': round(rot.x, 3),
           'Yaw': round(rot.y, 3)
           }

    def clear_data(self):
        ret = super(UDummy, self).clear_data()
        if ret:
            self.dummyObj = None
            return
        else:
            if self.dummyObj and self.dummyObj.model and self.dummyObj.model.valid:
                self.dummyObj.clear_data()
            return

    def afterinit(self):
        dummyObj = super(UDummy, self).afterinit()
        if dummyObj:
            self.dummyObj = dummyObj
            self.create_dummy_callback(dummyObj.model)
        else:
            self.dummyObj = DummyObj(math3d.vector(0, 0, 0), math3d.vector(0, 0, 0), str(self.properties['name']), cb=self.create_dummy_callback)

    def create_dummy_callback(self, obj, userData=None, currentTask=None):
        self.afterEditorInit()
        self.updateDummyTransform()

    def updateDummyTransform(self):
        if not self.dummyObj or not self.dummyObj.model or not self.dummyObj.model.valid:
            self._updatePending = True
            return
        if not self.transform:
            return
        self.dummyObj.model.position = math3d.vector(*self.transform.translate())
        self.dummyObj.model.scale = math3d.vector(*self.transform.scale())
        v3_rot = math3d.vector(self.transform.pitch(), self.transform.yaw(), self.transform.roll())
        m4_rotation = euler_angle_to_rotation_matrix(v3_rot)
        if self.dummyObj.model and self.dummyObj.model.valid:
            self.dummyObj.model.world_rotation_matrix = m4_rotation

    def goto(self, n_cur_time, n_interval_time):
        super(UDummy, self).goto(n_cur_time, n_interval_time)
        self.updateDummyTransform()

    def update(self, n_cur_time, n_interval_time, force=False):
        super(UDummy, self).update(n_cur_time, n_interval_time, force=force)
        if n_interval_time != 0:
            self.updateDummyTransform()