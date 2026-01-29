# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/decal_utils.py
from __future__ import absolute_import
import six
from logic.gcommon.const import NEOX_UNIT_SCALE
import math
MAX_DECAL_NUM = 4
FAR_MAX_SCL = 0.68
FAR_MIN_SCL = 0.2
NER_MAX_SCL = 1.5
NER_MIN_SCL = 0.5
MIN_RADIUS = 2.5 * NEOX_UNIT_SCALE
MAX_RADIUS = 5.5 * NEOX_UNIT_SCALE
format_degree = --- This code section failed: ---

  18       0  LOAD_GLOBAL           0  'int'
           3  LOAD_FAST             0  'x'
           6  LOAD_GLOBAL           1  'math'
           9  LOAD_ATTR             2  'floor'
          12  LOAD_ATTR             1  'math'
          15  BINARY_DIVIDE    
          16  CALL_FUNCTION_1       1 
          19  LOAD_CONST            2  360
          22  BINARY_MULTIPLY  
          23  BINARY_SUBTRACT  
          24  CALL_FUNCTION_1       1 
          27  RETURN_VALUE_LAMBDA
          -1  LAMBDA_MARKER    

Parse error at or near `BINARY_SUBTRACT' instruction at offset 23
CAM_RADIUS_OFFSET = 1000000
CAM_THETA_OFFSET = 1000
DECAL_POS_SCALE = 10000
DECAL_POS_OFFSET = 100000
DECAL_SCALE_SCALE = 100
DECAL_SCALE_OFFSET = 1000
MODEL_SCALE_SCALE = 100

def encode(item_id, radius, theta, phi, pos_x, pos_y, rot, decal_scale, model_scale):
    cam_p1 = int(radius) * CAM_RADIUS_OFFSET + format_degree(theta) * CAM_THETA_OFFSET + format_degree(phi)
    decal_p1 = int(pos_y * DECAL_POS_SCALE) * DECAL_POS_OFFSET + int(pos_x * DECAL_POS_SCALE)
    decal_p2 = int(decal_scale * DECAL_SCALE_SCALE) * DECAL_SCALE_OFFSET + format_degree(rot)
    model_p1 = int(model_scale * MODEL_SCALE_SCALE)
    return (
     item_id, cam_p1, decal_p1, decal_p2, model_p1)


def decode(item_id, cam_p1, decal_p1, decal_p2, model_p1):
    radius = cam_p1 / CAM_RADIUS_OFFSET
    theta = cam_p1 % CAM_RADIUS_OFFSET / CAM_THETA_OFFSET
    phi = cam_p1 % CAM_THETA_OFFSET
    pos_x = float(decal_p1 % DECAL_POS_OFFSET) / DECAL_POS_SCALE
    pos_y = float(decal_p1 / DECAL_POS_OFFSET) / DECAL_POS_SCALE
    rot = decal_p2 % DECAL_SCALE_OFFSET
    decal_scale = float(decal_p2 / DECAL_SCALE_OFFSET) / DECAL_SCALE_SCALE
    model_scale = float(model_p1) / MODEL_SCALE_SCALE
    return (
     item_id, radius, theta, phi, pos_x, pos_y, rot, decal_scale, model_scale)


def check_range(item_id, radius, theta, phi, pos_x, pos_y, rot, decal_scale, model_scale):
    if not MIN_RADIUS - 1 < radius < MAX_RADIUS + 1:
        return False
    if not 0 < pos_y < 1:
        return False
    per = (radius - MIN_RADIUS) * 1.0 / (MAX_RADIUS - MIN_RADIUS)
    MAX_SCL = NER_MAX_SCL - (NER_MAX_SCL - FAR_MAX_SCL) * per
    MIN_SCL = (FAR_MIN_SCL - NER_MIN_SCL) * per + NER_MIN_SCL
    if not MIN_SCL - 0.1 < decal_scale < MAX_SCL + 0.1:
        return False
    if not 0.2 < model_scale < 0.35:
        return False
    return True


def encode_decal_list(decal_list):
    return [ encode(*decal) for decal in decal_list ]


def decode_decal_list(decal_list):
    return [ decode(*decal) for decal in decal_list ]


def decode_decal_dict(decal_dict):
    return {skin_id:[ decode(*one_decal) for one_decal in decal_list ] for skin_id, decal_list in six.iteritems(decal_dict)}


def check_decal_data(decal_list):
    if len(decal_list) <= 0:
        return False
    for one_decal in decal_list:
        for value in one_decal:
            if not (isinstance(value, int) and value > 0):
                return False

        raw_data = decode(*one_decal)
        if not check_range(*raw_data):
            return False

    return True


COLOR_CHANNEL_MAX = 255
COLOR_PART_SCALE = 1000

def encode_color(color_dict, need_sort=False):
    return {str(part):value for part, value in six.iteritems(color_dict)}


def decode_color(color_dict):
    return {int(part):value for part, value in six.iteritems(color_dict)}


def decode_color_dict(color_dict):
    return {skin_id:decode_color(color_list) for skin_id, color_list in six.iteritems(color_dict)}


def cal_diff_color(ori_color, new_color):
    return {part:value for part, value in six.iteritems(new_color) if value != ori_color.get(part, -1)}