# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/programmatic_anim/ProgrammaticAnim.py
from __future__ import absolute_import
import six
from logic.comsys.programmatic_anim.InterpolateHelper import InterpolateHelper

class IProgrammaticAnim(object):

    def update(self, dt):
        raise NotImplementedError

    def is_finished(self):
        raise NotImplementedError

    def get_max_time(self):
        raise NotImplementedError


class StandardProgrammaticAnim(IProgrammaticAnim):

    def __init__(self):
        self._cur_time = 0.0
        self._vals = {}
        self._sequences = self._on_gen_sequences()
        self._max_time = self.get_max_time()
        self.update(0.0)

    def _on_gen_sequences(self):
        raise NotImplementedError

    def get_max_time(self):
        max_t = -1
        for seq_key, seq in six.iteritems(self._sequences):
            for frame in seq:
                t = frame[0]
                if t > max_t:
                    max_t = t

        return max_t

    def update(self, dt):
        self._cur_time += dt
        for seq_key, seq in six.iteritems(self._sequences):
            self._vals[seq_key] = InterpolateHelper.interpolate(self._cur_time, seq)

    def is_finished(self):
        return self._cur_time >= self._max_time

    def _get_animed_val(self, seq_key, default=None):
        return self._vals.get(seq_key, default)