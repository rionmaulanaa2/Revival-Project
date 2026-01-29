# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/TrackImp/UniGameInterface.py
from __future__ import absolute_import
import os
from math import cos, sin, acos, asin, atan2, sqrt, degrees, radians
import world
import math3d
from .UniHelper import euler_angle_to_direction, get_aspect_rate, get_active_scene
from UniCineDriver.UniGameInterfaceBase import UniGameInterfaceBase
from UniCineDriver.Utils.Matrix import MatrixBase

def get_active_camera():
    return get_active_scene().active_camera


def get_socket_matrix_by_name--- This code section failed: ---

  17       0  LOAD_FAST             1  'model'
           3  UNARY_NOT        
           4  POP_JUMP_IF_TRUE     17  'to 17'
           7  LOAD_FAST             1  'model'
          10  LOAD_ATTR             0  'valid'
          13  UNARY_NOT        
        14_0  COME_FROM                '4'
          14  POP_JUMP_IF_FALSE    21  'to 21'

  18      17  LOAD_CONST            0  ''
          20  RETURN_END_IF    
        21_0  COME_FROM                '14'

  19      21  LOAD_FAST             0  'name'
          24  UNARY_NOT        
          25  POP_JUMP_IF_TRUE     37  'to 37'
          28  POP_JUMP_IF_TRUE      1  'to 1'
          31  COMPARE_OP            2  '=='
        34_0  COME_FROM                '28'
        34_1  COME_FROM                '25'
          34  POP_JUMP_IF_FALSE    44  'to 44'

  20      37  LOAD_FAST             1  'model'
          40  LOAD_ATTR             2  'transformation'
          43  RETURN_END_IF    
        44_0  COME_FROM                '34'

  21      44  LOAD_FAST             1  'model'
          47  LOAD_ATTR             3  'get_socket_index'
          50  LOAD_FAST             0  'name'
          53  CALL_FUNCTION_1       1 
          56  STORE_FAST            2  'socket_index'

  22      59  LOAD_FAST             1  'model'
          62  LOAD_ATTR             4  'get_socket_matrix'
          65  LOAD_FAST             2  'socket_index'
          68  LOAD_CONST            2  1
          71  CALL_FUNCTION_2       2 
          74  RETURN_VALUE     

Parse error at or near `POP_JUMP_IF_TRUE' instruction at offset 28


def set_cur_camera_params(v3_pos=None, v3_rot=None, n_fov=None):
    cur_scn = get_active_scene()
    camera = get_active_camera()
    if v3_pos:
        camera.position = v3_pos
        cur_scn.viewer_position = v3_pos
    if v3_rot:
        v3_forward, v3_right, v3_up = euler_angle_to_direction(v3_rot)
        camera.set_placement(camera.position, v3_forward, v3_up)
    if n_fov is not None:
        camera.fov = n_fov / max(1.0, get_aspect_rate())
    return


def set_cur_camera_matrix(transform, n_fov=None):
    camera = get_active_camera()
    camera.set_placement(transform.translation, transform.forward, transform.up)
    if n_fov is not None:
        camera.fov = n_fov / max(1.0, get_aspect_rate())
    return


def recruitEntity--- This code section failed: ---

  58       0  LOAD_GLOBAL           0  'world'
           3  LOAD_ATTR             1  'create_model_async'
           6  LOAD_GLOBAL           2  'str'
           9  LOAD_GLOBAL           1  'create_model_async'
          12  BINARY_SUBSCR    
          13  CALL_FUNCTION_1       1 
          16  LOAD_FAST             1  'callback'
          19  CALL_FUNCTION_2       2 
          22  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 19


def recruitExistModel(name, callback):
    m = world.get_active_scene().get_model(str(name))
    if m:
        callback(m)
        return True
    return False


def recruitModelWithID(ID, callback):
    modelName = UniGameInterfaceBase.modelIDDict.get(ID, None)
    if modelName:
        m = world.get_active_scene().get_model(modelName)
        if m:
            callback(m)
            return True
    return False


def recruitFx--- This code section failed: ---

  81       0  LOAD_GLOBAL           0  'os'
           3  LOAD_ATTR             1  'path'
           6  LOAD_ATTR             2  'splitext'
           9  LOAD_ATTR             1  'path'
          12  BINARY_SUBSCR    
          13  CALL_FUNCTION_1       1 
          16  LOAD_CONST            2  -1
          19  BINARY_SUBSCR    
          20  LOAD_CONST            3  '.sfx'
          23  COMPARE_OP            2  '=='
          26  POP_JUMP_IF_FALSE    64  'to 64'

  82      29  LOAD_GLOBAL           3  'world'
          32  LOAD_ATTR             4  'create_sfx_async'
          35  LOAD_GLOBAL           5  'str'
          38  LOAD_GLOBAL           1  'path'
          41  BINARY_SUBSCR    
          42  CALL_FUNCTION_1       1 
          45  LOAD_ATTR             6  'replace'
          48  LOAD_CONST            4  '\\'
          51  LOAD_CONST            5  '/'
          54  CALL_FUNCTION_2       2 
          57  LOAD_FAST             1  'callback'
          60  CALL_FUNCTION_2       2 
          63  RETURN_END_IF    
        64_0  COME_FROM                '26'

  84      64  LOAD_GLOBAL           3  'world'
          67  LOAD_ATTR             7  'create_particle_system_async'
          70  LOAD_GLOBAL           5  'str'
          73  LOAD_GLOBAL           1  'path'
          76  BINARY_SUBSCR    
          77  CALL_FUNCTION_1       1 
          80  LOAD_ATTR             6  'replace'
          83  LOAD_CONST            4  '\\'
          86  LOAD_CONST            5  '/'
          89  CALL_FUNCTION_2       2 
          92  LOAD_FAST             1  'callback'
          95  CALL_FUNCTION_2       2 
          98  RETURN_VALUE     

Parse error at or near `BINARY_SUBSCR' instruction at offset 12


def recruitExistFx--- This code section failed: ---

  88       0  LOAD_GLOBAL           0  'get_active_scene'
           3  CALL_FUNCTION_0       0 
           6  STORE_FAST            2  'cur_scn'

  89       9  LOAD_FAST             2  'cur_scn'
          12  LOAD_ATTR             1  'get_sfx'
          15  LOAD_ATTR             1  'get_sfx'
          18  BINARY_SUBSCR    
          19  CALL_FUNCTION_1       1 
          22  STORE_FAST            3  'sfx'

  90      25  LOAD_FAST             3  'sfx'
          28  POP_JUMP_IF_FALSE    45  'to 45'

  91      31  LOAD_FAST             1  'callback'
          34  LOAD_FAST             3  'sfx'
          37  CALL_FUNCTION_1       1 
          40  POP_TOP          

  92      41  LOAD_GLOBAL           2  'True'
          44  RETURN_END_IF    
        45_0  COME_FROM                '28'

  93      45  LOAD_GLOBAL           3  'hasattr'
          48  LOAD_GLOBAL           4  'world'
          51  LOAD_CONST            2  'particlesystem'
          54  CALL_FUNCTION_2       2 
          57  POP_JUMP_IF_FALSE    99  'to 99'

  94      60  LOAD_FAST             2  'cur_scn'
          63  LOAD_ATTR             5  'get_particlesystem'
          66  LOAD_ATTR             1  'get_sfx'
          69  BINARY_SUBSCR    
          70  CALL_FUNCTION_1       1 
          73  STORE_FAST            4  'pse'

  95      76  LOAD_FAST             4  'pse'
          79  POP_JUMP_IF_FALSE    99  'to 99'

  96      82  LOAD_FAST             1  'callback'
          85  LOAD_FAST             4  'pse'
          88  CALL_FUNCTION_1       1 
          91  POP_TOP          

  97      92  LOAD_GLOBAL           2  'True'
          95  RETURN_END_IF    
        96_0  COME_FROM                '79'
          96  JUMP_FORWARD          0  'to 99'
        99_0  COME_FROM                '96'

  98      99  LOAD_GLOBAL           6  'False'
         102  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `BINARY_SUBSCR' instruction at offset 18


def getGameFPS():
    import game3d
    return game3d.get_frame_rate()


class NeoxMatrix(MatrixBase):

    def __init__(self):
        self.matrix_ = math3d.matrix()

    def mul(self, matrix_rhs):
        mulMat = NeoxMatrix()
        mulMat.matrix_ = self.matrix_ * matrix_rhs.matrix_
        return mulMat

    def createfromDegrees(self, roll_pitch_yaw):
        roll, pitch, yaw = [ radians(d) for d in roll_pitch_yaw ]
        self.createfromRadians([roll, pitch, yaw])

    def createfromRadians(self, roll_pitch_yaw):
        roll, pitch, yaw = roll_pitch_yaw
        self.matrix_.rotation = math3d.matrix_rotation_zxy(pitch, yaw, roll)

    def inverse(self):
        inverseMat = NeoxMatrix()
        inverseMat.matrix_ = math3d.matrix(self.matrix_).inverse()
        return inverseMat

    def rotation(self):
        return self.matrix_.rotation

    def translate(self):
        translation = self.matrix_.translation
        return [
         translation.x, translation.y, translation.z]

    def setTranslate(self, translate):
        translation = math3d.vector(translate[0], translate[1], translate[2])
        self.matrix_.translation = translation

    def scale(self):
        scale = self.matrix_.scale
        return [
         scale.x, scale.y, scale.z]

    def setScale(self, scale):
        self.matrix_.scale = math3d.vector(*scale)

    def roll(self):
        return degrees(self.matrix_.roll)

    def yaw(self):
        return degrees(self.matrix_.yaw)

    def pitch(self):
        return degrees(self.matrix_.pitch)

    def roll_radian(self):
        return self.matrix_.roll

    def yaw_radian(self):
        return self.matrix_.yaw

    def pitch_radian(self):
        return self.matrix_.pitch


class UniGameInterface(UniGameInterfaceBase):
    modelIDDict = dict()