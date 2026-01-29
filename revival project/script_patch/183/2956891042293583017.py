# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/cinematic/datacommon.py
from __future__ import absolute_import
import uuid
import math3d
import world
RES_TYPE_BASE = 0
RES_TYPE_CAMERA_TRACK = 1
RES_TYPE_CHARACTER = 2
RES_TYPE_AUDIO = 3
RES_TYPE_SFX = 4
RES_TYPE_DIALOGUE = 5
RES_TYPE_SCREEN = 6
RES_TYPE_SUBTITLE = 7
RES_TYPE_DIRECTOR = 8
RES_TYPE_SCENE_CONFIG = 9
RES_TYPE_FLASHMOVIE = 10
RES_TYPE_SPEED_RATE = 11
RES_TYPE_ACTION = 12
EVENT_TYPE_BASE = 0
EVENT_TYPE_CAMERA_TRACK_NODE = 1
EVENT_TYPE_CHARACTER = 2
EVENT_TYPE_CHARACTER_ANIM = 3
EVENT_TYPE_AUDIO = 4
EVENT_TYPE_SFX = 5
EVENT_TYPE_DIALOGUE = 6
EVENT_TYPE_CHARACTER_WAYPOINT = 7
EVENT_TYPE_SCREEN_FILTER = 8
EVENT_TYPE_CAMERA_TRACK = 9
EVENT_TYPE_SUBTITLE = 10
EVENT_TYPE_SCENE_CHANGE = 11
EVENT_TYPE_CAMERA_FOCUS = 12
EVENT_TYPE_SFX_RATE = 13
EVENT_TYPE_FLASH_DIRECT = 14
EVENT_TYPE_SPEED_RATE = 15
EVENT_TYPE_FOG = 16
EVENT_TYPE_FLASH_FUNCTION = 17
EVENT_TYPE_BUILD_IN_ACTION = 18
EVENT_TYPE_SFX_WAYPOINT = 19
EXECUTE_TYPE_DIRECT = 1
EXECUTE_TYPE_INTERP = 2
SPLINE_TYPE_LINE = 1
SPLINE_TYPE_AUTO_BEZIER = 2
SPLINE_TYPE_BEZIER = 3
DEFAULT_TIME_LENGTH = 8000
RES_EVENT_DICT = {RES_TYPE_CAMERA_TRACK: (
                         EVENT_TYPE_CAMERA_TRACK_NODE,
                         EVENT_TYPE_CAMERA_FOCUS),
   RES_TYPE_CHARACTER: (
                      EVENT_TYPE_CHARACTER,
                      EVENT_TYPE_CHARACTER_ANIM,
                      EVENT_TYPE_CHARACTER_WAYPOINT),
   RES_TYPE_AUDIO: (
                  EVENT_TYPE_AUDIO,),
   RES_TYPE_SFX: (
                EVENT_TYPE_SFX,
                EVENT_TYPE_SFX_RATE),
   RES_TYPE_DIALOGUE: (
                     EVENT_TYPE_DIALOGUE,),
   RES_TYPE_SCREEN: (
                   EVENT_TYPE_SCREEN_FILTER,),
   RES_TYPE_SUBTITLE: (
                     EVENT_TYPE_SUBTITLE,),
   RES_TYPE_DIRECTOR: (
                     EVENT_TYPE_CAMERA_TRACK,),
   RES_TYPE_SCENE_CONFIG: (
                         EVENT_TYPE_SCENE_CHANGE,)
   }

def get_child_doc(node, node_name):
    child = node.FirstChild()
    while child:
        if child.Value == node_name:
            return child
        child = child.NextSibling()


def get_attribute(node, attri_name, default_value=None):
    attri = node.FirstAttribute()
    while attri:
        if attri.Name == attri_name:
            return attri.Value
        attri = attri.Next()

    return default_value


def get_uuid():
    return uuid.uuid1().get_hex()


MAX_VIEW_RANGE = 100000.0

def get_preset_camera_info--- This code section failed: ---

 123       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'tinyxml'
           9  STORE_FAST            1  'tinyxml'

 124      12  LOAD_CONST            1  ''
          15  LOAD_CONST            0  ''
          18  IMPORT_NAME           1  'C_file'
          21  STORE_FAST            2  'C_file'

 125      24  LOAD_CONST            1  ''
          27  LOAD_CONST            0  ''
          30  IMPORT_NAME           2  'math3d'
          33  STORE_FAST            3  'math3d'

 126      36  LOAD_FAST             3  'math3d'
          39  LOAD_ATTR             3  'vector'
          42  LOAD_CONST            1  ''
          45  LOAD_CONST            1  ''
          48  LOAD_CONST            1  ''
          51  CALL_FUNCTION_3       3 
          54  STORE_FAST            4  'pos'

 127      57  LOAD_FAST             3  'math3d'
          60  LOAD_ATTR             4  'matrix'
          63  CALL_FUNCTION_0       0 
          66  STORE_FAST            5  'rot'

 130      69  LOAD_FAST             1  'tinyxml'
          72  LOAD_ATTR             5  'TiXmlDocument'
          75  CALL_FUNCTION_0       0 
          78  STORE_FAST            6  'doc'

 131      81  LOAD_FAST             2  'C_file'
          84  LOAD_ATTR             6  'get_res_file'
          87  LOAD_ATTR             2  'math3d'
          90  CALL_FUNCTION_2       2 
          93  STORE_FAST            7  'buf'

 132      96  LOAD_FAST             6  'doc'
          99  LOAD_ATTR             7  'Parse'
         102  LOAD_FAST             7  'buf'
         105  CALL_FUNCTION_1       1 
         108  POP_TOP          

 134     109  LOAD_FAST             3  'math3d'
         112  LOAD_ATTR             3  'vector'
         115  LOAD_CONST            1  ''
         118  LOAD_CONST            1  ''
         121  LOAD_CONST            1  ''
         124  CALL_FUNCTION_3       3 
         127  STORE_FAST            4  'pos'

 135     130  LOAD_FAST             3  'math3d'
         133  LOAD_ATTR             4  'matrix'
         136  CALL_FUNCTION_0       0 
         139  STORE_FAST            5  'rot'

 136     142  LOAD_FAST             6  'doc'
         145  LOAD_ATTR             8  'RootElement'
         148  CALL_FUNCTION_0       0 
         151  STORE_FAST            8  'root'

 137     154  LOAD_FAST             8  'root'
         157  LOAD_ATTR             9  'FirstChild'
         160  LOAD_CONST            3  'info'
         163  CALL_FUNCTION_1       1 
         166  STORE_FAST            9  'node'

 138     169  LOAD_FAST             9  'node'
         172  POP_JUMP_IF_FALSE   370  'to 370'

 139     175  LOAD_FAST             9  'node'
         178  LOAD_ATTR             9  'FirstChild'
         181  LOAD_CONST            4  'Camera'
         184  CALL_FUNCTION_1       1 
         187  STORE_FAST            9  'node'

 140     190  LOAD_FAST             9  'node'
         193  POP_JUMP_IF_FALSE   370  'to 370'

 141     196  LOAD_FAST             9  'node'
         199  LOAD_ATTR            10  'FirstAttribute'
         202  CALL_FUNCTION_0       0 
         205  STORE_FAST           10  'attr'

 142     208  LOAD_FAST            10  'attr'
         211  POP_JUMP_IF_FALSE   281  'to 281'

 143     214  LOAD_GLOBAL          11  'tuple'
         217  BUILD_LIST_0          0 
         220  LOAD_FAST            10  'attr'
         223  LOAD_ATTR            12  'Value'
         226  LOAD_ATTR            13  'split'
         229  LOAD_CONST            5  ','
         232  CALL_FUNCTION_1       1 
         235  GET_ITER         
         236  FOR_ITER             18  'to 257'
         239  STORE_FAST           11  'v'
         242  LOAD_GLOBAL          14  'float'
         245  LOAD_FAST            11  'v'
         248  CALL_FUNCTION_1       1 
         251  LIST_APPEND           2  ''
         254  JUMP_BACK           236  'to 236'
         257  CALL_FUNCTION_1       1 
         260  STORE_FAST           12  't'

 144     263  LOAD_FAST             3  'math3d'
         266  LOAD_ATTR             3  'vector'
         269  LOAD_FAST            12  't'
         272  CALL_FUNCTION_VAR_0     0 
         275  STORE_FAST            4  'pos'
         278  JUMP_FORWARD          0  'to 281'
       281_0  COME_FROM                '278'

 145     281  LOAD_FAST            10  'attr'
         284  LOAD_ATTR            15  'Next'
         287  CALL_FUNCTION_0       0 
         290  STORE_FAST           10  'attr'

 146     293  LOAD_FAST            10  'attr'
         296  POP_JUMP_IF_FALSE   367  'to 367'

 147     299  LOAD_GLOBAL          11  'tuple'
         302  BUILD_LIST_0          0 
         305  LOAD_FAST            10  'attr'
         308  LOAD_ATTR            12  'Value'
         311  LOAD_ATTR            13  'split'
         314  LOAD_CONST            5  ','
         317  CALL_FUNCTION_1       1 
         320  GET_ITER         
         321  FOR_ITER             18  'to 342'
         324  STORE_FAST           11  'v'
         327  LOAD_GLOBAL          14  'float'
         330  LOAD_FAST            11  'v'
         333  CALL_FUNCTION_1       1 
         336  LIST_APPEND           2  ''
         339  JUMP_BACK           321  'to 321'
         342  CALL_FUNCTION_1       1 
         345  STORE_FAST           12  't'

 148     348  LOAD_FAST             5  'rot'
         351  LOAD_ATTR            16  'set_all'
         354  LOAD_FAST            12  't'
         357  CALL_FUNCTION_1       1 
         360  POP_TOP          
         361  JUMP_ABSOLUTE       367  'to 367'
         364  JUMP_ABSOLUTE       370  'to 370'
         367  JUMP_FORWARD          0  'to 370'
       370_0  COME_FROM                '367'

 149     370  LOAD_FAST             4  'pos'
         373  LOAD_FAST             5  'rot'
         376  BUILD_TUPLE_2         2 
         379  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 90


def load_scene_common--- This code section failed: ---

 152       0  LOAD_GLOBAL           0  'world'
           3  LOAD_ATTR             1  'scene'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            2  'scn'

 153      15  LOAD_FAST             2  'scn'
          18  LOAD_ATTR             3  'load'
          21  LOAD_FAST             0  'path'
          24  LOAD_CONST            0  ''
          27  LOAD_GLOBAL           4  'True'
          30  CALL_FUNCTION_3       3 
          33  POP_TOP          

 154      34  LOAD_FAST             2  'scn'
          37  LOAD_ATTR             5  'set_irradiance_map'
          40  LOAD_CONST            1  'shader/cube/far.cube'
          43  LOAD_CONST            2  'shader/cube/near.cube'
          46  CALL_FUNCTION_2       2 
          49  POP_TOP          

 156      50  LOAD_FAST             2  'scn'
          53  LOAD_ATTR             6  'create_camera'
          56  LOAD_GLOBAL           4  'True'
          59  CALL_FUNCTION_1       1 
          62  STORE_FAST            3  'camera'

 157      65  LOAD_GLOBAL           7  'get_preset_camera_info'
          68  LOAD_GLOBAL           3  'load'
          71  BINARY_ADD       
          72  CALL_FUNCTION_1       1 
          75  UNPACK_SEQUENCE_2     2 
          78  STORE_FAST            4  'pos'
          81  STORE_FAST            5  'rot'

 158      84  LOAD_FAST             4  'pos'
          87  LOAD_FAST             3  'camera'
          90  STORE_ATTR            8  'world_position'

 159      93  LOAD_FAST             5  'rot'
          96  LOAD_FAST             3  'camera'
          99  STORE_ATTR            9  'world_rotation_matrix'

 161     102  LOAD_FAST             2  'scn'
         105  LOAD_ATTR            10  'get_bounding'
         108  CALL_FUNCTION_0       0 
         111  UNPACK_SEQUENCE_2     2 
         114  STORE_FAST            6  'aabbmin'
         117  STORE_FAST            7  'aabbmax'

 162     120  LOAD_FAST             7  'aabbmax'
         123  LOAD_FAST             6  'aabbmin'
         126  BINARY_SUBTRACT  
         127  LOAD_ATTR            11  'length'
         130  STORE_FAST            8  'v_range'

 163     133  LOAD_FAST             8  'v_range'
         136  LOAD_GLOBAL          12  'MAX_VIEW_RANGE'
         139  COMPARE_OP            4  '>'
         142  POP_JUMP_IF_FALSE   172  'to 172'

 164     145  LOAD_GLOBAL          12  'MAX_VIEW_RANGE'
         148  STORE_FAST            8  'v_range'

 165     151  LOAD_FAST             4  'pos'
         154  LOAD_FAST             2  'scn'
         157  STORE_ATTR           13  'viewer_position'

 166     160  LOAD_FAST             8  'v_range'
         163  LOAD_FAST             2  'scn'
         166  STORE_ATTR           14  'view_range'
         169  JUMP_FORWARD         26  'to 198'

 168     172  LOAD_FAST             6  'aabbmin'
         175  LOAD_FAST             7  'aabbmax'
         178  BINARY_ADD       
         179  LOAD_CONST            4  0.5
         182  BINARY_MULTIPLY  
         183  LOAD_FAST             2  'scn'
         186  STORE_ATTR           13  'viewer_position'

 169     189  LOAD_FAST             8  'v_range'
         192  LOAD_FAST             2  'scn'
         195  STORE_ATTR           14  'view_range'
       198_0  COME_FROM                '169'

 170     198  LOAD_FAST             2  'scn'
         201  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_1' instruction at offset 72


def find_obj_idx_in_sorted_list_prev_time(l, time):
    n = len(l)
    if n < 20:
        for idx, t in enumerate(l):
            if t._time > time:
                return idx - 1

        return n - 1
    else:
        start = 0
        end = n - 1
        if l[start]._time > time:
            return -1
        while end - start > 1:
            mid = (start + end) / 2
            if l[mid]._time <= time:
                start = mid
            else:
                end = mid

        return start


def find_obj_idx_in_sorted_list_next_time(l, time):
    n = len(l)
    if n < 20:
        for idx, t in enumerate(l):
            if t._time >= time:
                return idx

        return -1
    else:
        start = 0
        end = n - 1
        if l[end]._time < time:
            return -1
        while end - start > 1:
            mid = (start + end) / 2
            if l[mid]._time >= time:
                end = mid
            else:
                start = mid

        return end