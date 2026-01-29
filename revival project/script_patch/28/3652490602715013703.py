# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/anticheat_utils.py
from __future__ import absolute_import
from common.framework import Singleton

class AnticheatUtils(Singleton):
    ALIAS_NAME = 'anticheat_utils'

    def init(self):
        self.is_init = False

    def force_stop_detact(self):
        pass

    def detect_human_bone(self, result_callback, interval=None, times=None):
        pass

    def detect_super_jump(self, result_callback, interval=None, times=None):
        pass

    def detect_recoil(self, result_callback, interval=None, times=None):
        pass

    def enable_check_scene_model_draw(self, result_callback, interval=None, times=None):
        pass

    def get_file_md5(self, file_path):
        pass

    def detect_all_materials(self, result_callback, interval=None, times=None):
        pass

    def detect_sound_visible_distance(self, result_callback, interval=None, times=None):
        pass

    def detect(self, detect_type, interval=None, times=None):
        pass

    def detect_timer(self, tag, ts):
        pass

    def detect_const(self):
        pass

    def detect_data(self, data):
        pass