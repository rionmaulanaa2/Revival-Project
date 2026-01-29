# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/programmatic_anim/InterpolateHelper.py
from __future__ import absolute_import
import cc

class InterpolateHelper(object):
    EASE_IN_SINE = 1
    EASE_OUT_SINE = 2
    EASE_IN_QUINT = 3
    EASE_OUT_QUINT = 4

    @classmethod
    def interpolate(cls, cur_time, seq):
        left, right = cls._get_frame_idx(cur_time, seq)
        if left == -1:
            return
        ratio = cls._get_factor(cur_time, left, right, seq)
        if len(seq[left]) >= 3:
            ease_type = seq[left][2]
            ratio = cls._apply_ease(ratio, ease_type)
        left_val = seq[left][1]
        right_val = seq[right][1]
        return cls._interpolate_helper(left_val, right_val, ratio)

    @classmethod
    def _apply_ease(cls, ratio, ease_type):
        import math
        if ease_type == cls.EASE_IN_SINE:
            return 1.0 - math.cos(ratio * math.pi / 2.0)
        else:
            if ease_type == cls.EASE_OUT_SINE:
                return math.sin(ratio * math.pi / 2.0)
            if ease_type == cls.EASE_IN_QUINT:
                return ratio * ratio * ratio * ratio * ratio
            if ease_type == cls.EASE_OUT_QUINT:
                return 1.0 - math.pow(1.0 - ratio, 5)
            return ratio

    @classmethod
    def _get_frame_idx(cls, cur_time, sequence):
        leng = len(sequence)
        left_frame_idx = -1
        for idx, frame in enumerate(sequence):
            if idx + 1 == leng:
                left_frame_idx = idx
                break
            else:
                next_frame = sequence[idx + 1]
                next_frame_time = next_frame[0]
                if cur_time < next_frame_time:
                    left_frame_idx = idx
                    break

        if left_frame_idx == -1:
            return (-1, -1)
        if left_frame_idx + 1 >= leng:
            right_frame_idx = left_frame_idx
        else:
            right_frame_idx = left_frame_idx + 1
        return (
         left_frame_idx, right_frame_idx)

    @classmethod
    def _interpolate_helper(cls, left_val, right_val, ratio):
        if isinstance(left_val, cc.Vec2):
            lhs = cc.Vec2(left_val.x, left_val.y)
            lhs.scale(1.0 - ratio)
            rhs = cc.Vec2(right_val.x, right_val.y)
            rhs.scale(ratio)
            lhs.add(rhs)
            return lhs
        else:
            return left_val * (1.0 - ratio) + right_val * ratio

    @classmethod
    def _get_factor(cls, t, left_idx, right_idx, sequence):
        if left_idx == right_idx:
            return 0.0
        else:
            left_frame = sequence[left_idx]
            right_frame = sequence[right_idx]
            left_t = left_frame[0]
            right_t = right_frame[0]
            if left_t == right_t:
                return 0.0
            offset = t - left_t
            delta = right_t - left_t
            ratio = float(offset) / delta
            ratio = min(1.0, max(0.0, ratio))
            return ratio