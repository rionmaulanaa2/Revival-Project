# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/hdr_tool/hdr_lumens_analysis.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from functools import cmp_to_key
from hdr_tool.hdr_lumens_const import LUMENS_DIR, CHUNK_SIZE, PADDING
import struct
import os

def calc_variance_by_chunk_index(x, z):
    chunk_length = CHUNK_SIZE / PADDING
    chunk_lights = load_chunk_light_by_index(x, z)
    lights = []
    if chunk_lights:
        for i in range(chunk_length):
            for j in range(chunk_length):
                same_y_height_lights = chunk_lights[i, j]
                for y_lights in six.itervalues(same_y_height_lights):
                    lights.extend(y_lights)

        sorted(lights, key=cmp_to_key(lambda x, y: x > y))
        for light in lights:
            print(light)

    else:
        return None
    return None


def load_chunk_light_by_index(x, z):
    file_path = '%s/%d_%d.lumen' % (LUMENS_DIR, x, z)
    if not os.path.exists(file_path):
        return
    f = open(file_path, 'rb')
    data = f.read()
    xlength, ylength = struct.unpack('<2b', data[:2])
    data = data[2:]
    wb_chunk_lights = {}
    for i in range(xlength):
        for j in range(ylength):
            wb_chunk_lights[i, j] = {}
            same_xz_length = struct.unpack('<b', data[:1])[0]
            data = data[1:]
            for k in range(same_xz_length):
                yheight = struct.unpack('<f', data[:4])[0]
                data = data[4:]
                lights = struct.unpack('<10B', data[:10])
                data = data[10:]
                wb_chunk_lights[i, j][yheight] = lights

    return wb_chunk_lights