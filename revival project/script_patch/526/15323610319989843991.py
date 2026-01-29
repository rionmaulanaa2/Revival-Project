# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAvatarSound.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import common.utils.timer as timer
import math3d
import world
import logic.gcommon.const as const
import game3d
from logic.gcommon.common_const.scene_const import *
from logic.gcommon.common_const import animation_const
from . import ComSound

class ComAvatarSound(ComSound.ComSound):

    def __init__(self):
        super(ComAvatarSound, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComAvatarSound, self).init_from_dict(unit_obj, bdict)

    def _play_footstep_sound(self, *args):
        super(ComAvatarSound, self)._play_footstep_sound(args)
        if self._env_type != self.sound_mgr.get_listener_env_type():
            self.sound_mgr.set_listener_env_type(self._env_type)

    def destroy(self):
        super(ComAvatarSound, self).destroy()