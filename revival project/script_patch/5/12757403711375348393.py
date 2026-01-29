# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDataAnimator.py
from ..share.ComDataBase import ComDataBase

class ComDataAnimator(ComDataBase):
    BIND_EVENT = {'E_ANIMATOR_LOADED': 'on_load_animator_complete',
       'E_SET_YAW_MIRRORED': 'set_yaw_mirrored'
       }

    def __init__(self):
        super(ComDataAnimator, self).__init__(False)
        self.yaw_head_local = 0
        self.yaw_head_offset = 0
        self.pitch_head_local = 0
        self.left_max_yaw_angle = -90
        self.right_max_yaw_angle = 50
        self.y_twist_node = None
        self.yaw_mirrored = False
        return

    def get_share_data_name(self):
        return 'ref_animator_data'

    def on_load_animator_complete(self, *args):
        animator = self.ev_g_animator()
        if not animator:
            return
        _y_twist_node = animator.find('turn_y_up_body')
        if _y_twist_node:
            self.y_twist_node = _y_twist_node
            self.activate_ecs()

    def set_yaw_mirrored(self, mirror):
        self.yaw_mirrored = mirror

    def _do_cache(self):
        self.y_twist_node = None
        return

    def _do_destroy(self):
        self.y_twist_node = None
        return