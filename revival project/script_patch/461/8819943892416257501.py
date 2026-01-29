# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/fly_out_animation.py
from __future__ import absolute_import
from logic.comsys.programmatic_anim.ProgrammaticAnim import StandardProgrammaticAnim
from logic.comsys.programmatic_anim.InterpolateHelper import InterpolateHelper

class FlyOutMotion(StandardProgrammaticAnim):

    def __init__(self, src_cocos_wpos, dst_cocos_wpos):
        self._src_cocos_wpos = src_cocos_wpos
        self._dst_cocos_wpos = dst_cocos_wpos
        self._fps = 30
        super(FlyOutMotion, self).__init__()

    def _on_gen_sequences(self):
        return {'pos': self._gen_pos_sequence()
           }

    def _gen_pos_sequence(self):
        return [
         (
          9.0 / self._fps,
          self._src_cocos_wpos,
          InterpolateHelper.EASE_IN_QUINT),
         (
          18.0 / self._fps,
          self._dst_cocos_wpos)]

    def get_pos(self):
        return self._get_animed_val('pos')