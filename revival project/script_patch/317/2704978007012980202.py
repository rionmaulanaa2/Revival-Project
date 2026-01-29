# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/track_reader.py
from __future__ import absolute_import
import math3d
import math
track_test = [
 (
  0.0, (0, 0, 0)), (0.05, (0, 2.458, -0.704)), (0.1, (0, 5.982, 0.45)), (0.15, (0, 12.894, 2.908)), (0.2, (0, 16.043, 4.909)), (0.25, (0, 17.416, 6.556)), (0.3, (0, 18.282, 8.596))]

def precess_pos_2d(self, pos, is_rotate_fix_dir):
    if is_rotate_fix_dir:
        x = pos.x * self.cos - pos.z * self.sin
        z = pos.x * self.sin + pos.z * self.cos
        new_pos = math3d.vector(x, pos.y, z)
    else:
        new_pos = pos
    new_pos *= self.pos_scale
    new_pos += self.start_pos
    return new_pos


def precess_pos_3d(self, pos, is_rotate_fix_dir):
    return pos * self.rot_mat


class TrackReader(object):

    def __init__(self):
        self.start_pos = None
        self.pos_scale = None
        self.cos = None
        self.sin = None
        self.cur_index = 0
        self.track_all_time = 0
        return

    def create_by_track_data(self, track_data, direction, start_pos, end_pos):
        self.track_data = track_data
        self.track_all_time = self.track_data[-1][0]
        self.cur_index = 0
        self.start_pos = start_pos
        track_offset = self.track_data[-1][1] - self.track_data[0][1]
        vector_offset = end_pos - start_pos
        if isinstance(direction, math3d.vector):
            z_scale = vector_offset.length / track_offset.length
            scale_mat = math3d.matrix()
            scale_mat.scale = math3d.vector(1, 1, z_scale)
            pos_mat = math3d.matrix.make_translation(start_pos.x, start_pos.y, start_pos.z)
            vector_offset.normalize()
            rot_mat = math3d.matrix.make_rotation_between(math3d.vector(0.0, 0.0, 1.0), vector_offset)
            self.rot_mat = scale_mat * rot_mat * pos_mat
            self._precess_pos = precess_pos_3d
        else:
            self.cos = math.cos(direction)
            self.sin = math.sin(direction)
            self._precess_pos = precess_pos_2d
            track_offset = self.rotation_pos_2d(track_offset)
            if track_offset.x != 0:
                scale_x = vector_offset.x / track_offset.x
            else:
                scale_x = 1
            if track_offset.y != 0:
                scale_y = vector_offset.y / track_offset.y
            else:
                scale_y = 1
            if track_offset.z != 0:
                scale_z = vector_offset.z / track_offset.z
            else:
                scale_z = 1
            self.pos_scale = math3d.vector(scale_x, scale_y, scale_z)

    def read_track(self, track_name, direction, start_pos, end_pos, track_pos_list=[]):
        track_data = self.generate_track_data(track_pos_list)
        self.create_by_track_data(track_data, direction, start_pos, end_pos)

    def generate_track_data(self, track_pos_list=[]):
        if not track_pos_list:
            track_pos_list = track_test
        track_data = []
        for data in track_pos_list:
            if isinstance(data[1], tuple) or isinstance(data[1], list):
                track_data.append([data[0], math3d.vector(*data[1])])
            else:
                track_data.append([data[0], data[1]])

        return track_data

    def rotation_pos_2d(self, pos):
        x = pos.x * self.cos - pos.z * self.sin
        z = pos.x * self.sin + pos.z * self.cos
        return math3d.vector(x, pos.y, z)

    def precess_pos_2d(self, pos, is_rotate_fix_dir):
        if is_rotate_fix_dir:
            x = pos.x * self.cos - pos.z * self.sin
            z = pos.x * self.sin + pos.z * self.cos
            new_pos = math3d.vector(x, pos.y, z)
        else:
            new_pos = pos
        new_pos *= self.pos_scale
        new_pos += self.start_pos
        return new_pos

    def precess_pos_3d(self, pos, is_rotate_fix_dir):
        return pos * self.rot_mat

    def get_track_time(self):
        return self.track_all_time

    def get_cur_timeline_index(self):
        return self.cur_index

    def get_timeline_info(self, index):
        if index >= len(self.track_data):
            return
        return self.track_data[index]

    def get_cur_pos(self, time, is_rotate_fix_dir=True):
        if time > self.track_all_time:
            pos = math3d.vector(self.track_data[-1][1])
            is_end = True
        else:
            while time > self.track_data[self.cur_index + 1][0]:
                self.cur_index += 1

            rate = (time - self.track_data[self.cur_index][0]) / (self.track_data[self.cur_index + 1][0] - self.track_data[self.cur_index][0])
            pos_offset = self.track_data[self.cur_index + 1][1] - self.track_data[self.cur_index][1]
            pos = self.track_data[self.cur_index][1] + pos_offset * rate
            is_end = False
        pos = self._precess_pos(self, pos, is_rotate_fix_dir)
        return (
         pos, is_end)