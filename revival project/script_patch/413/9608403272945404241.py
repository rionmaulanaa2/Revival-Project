# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/CareerIconOutMotion.py
from __future__ import absolute_import
from logic.comsys.programmatic_anim.ProgrammaticAnim import StandardProgrammaticAnim
import cc

class CareerIconOutMotion(StandardProgrammaticAnim):

    def __init__(self, src_cocos_wpos, dst_cocos_wpos):
        self._src_cocos_wpos = src_cocos_wpos
        self._dst_cocos_wpos = dst_cocos_wpos
        self._fps = 30
        super(CareerIconOutMotion, self).__init__()

    def _on_gen_sequences(self):
        return {'pos': self._gen_pos_sequence(),
           'alpha': self._gen_alpha_sequence(),
           'scale': self._gen_scale_sequence()
           }

    def _gen_pos_sequence(self):
        return [
         (
          12.0 / self._fps,
          self._src_cocos_wpos),
         (
          22.0 / self._fps,
          self._dst_cocos_wpos)]

    def _gen_alpha_sequence(self):
        return [
         (
          0.0 / self._fps,
          255.0),
         (
          22.0 / self._fps,
          255.0),
         (
          25.0 / self._fps,
          0.0)]

    def _gen_scale_sequence(self):
        return [
         (
          12.0 / self._fps,
          cc.Vec2(1.0, 1.0)),
         (
          22.0 / self._fps,
          cc.Vec2(0.36, 0.36))]

    def get_pos(self):
        return self._get_animed_val('pos')

    def get_alpha(self):
        return self._get_animed_val('alpha')

    def get_scale(self):
        return self._get_animed_val('scale')