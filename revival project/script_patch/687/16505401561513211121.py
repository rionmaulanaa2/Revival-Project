# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/trk/TrkManager.py
from __future__ import absolute_import
from six.moves import range
import math3d
import json
import pickle

class TrkManager(object):

    def __init__(self):
        self._trk_data = None
        self._trk_length = None
        self._trk_duration = None
        self._is_left_hand = False
        return

    def load_trk(self, file_name, rail_length, is_left_hand=False):
        self._trk_data = global_data.track_cache.create_track(file_name)
        self._trk_length = rail_length
        self._trk_duration = self._trk_data.duration
        self._is_left_hand = is_left_hand

    def reencode_pos(self, save_path, sample_count=0):
        if not self._trk_data:
            return
        sample_count = sample_count or int(self._trk_duration + 1)
        pos_list = []
        sample_delta = self._trk_duration / (sample_count - 1)
        for i in range(sample_count):
            tmp_time = i * sample_delta
            pos = self._trk_data.get_transform(tmp_time).translation
            pos_list.append([pos.x, pos.y, pos.z])

        with open(save_path, 'w') as f:
            pickle.dump(pos_list, f)

    @property
    def trk_length(self):
        return self._trk_length

    def trk_dis_2_time(self, dis):
        dis = self.get_circular_dis(dis)
        return dis * self._trk_duration / self._trk_length

    def get_circular_dis(self, dis):
        return dis % self._trk_length

    def get_transform(self, tmp_dis):
        if not self._trk_data:
            return None
        else:
            tmp_trk_time = self.trk_dis_2_time(tmp_dis)
            trans = self._trk_data.get_transform(tmp_trk_time)
            if not self._is_left_hand:
                trans = self._conv_right_to_left_hand(trans)
            return trans
            return None

    def get_pos_and_rot(self, tmp_dis):
        tmp_trans = self.get_transform(tmp_dis)
        tmp_pos = tmp_trans.translation
        tmp_rot = tmp_trans.rotation
        return (
         tmp_pos, tmp_rot)

    def get_pos(self, tmp_dis):
        tmp_trans = self.get_transform(tmp_dis)
        tmp_pos = tmp_trans.translation
        return tmp_pos

    def get_rot(self, tmp_dis):
        tmp_trans = self.get_transform(tmp_dis)
        tmp_rot = tmp_trans.rotation
        return tmp_rot

    def _conv_right_to_left_hand(self, trans):
        pos = trans.translation
        rot = trans.rotation
        forward = rot.forward
        forward = forward.cross(-rot.right)
        trans = math3d.matrix.make_orient(forward, rot.forward)
        trans.do_translate(pos)
        return trans