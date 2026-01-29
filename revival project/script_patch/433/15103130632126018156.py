# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/SysAimPoisonWarning.py
from __future__ import absolute_import
from logic.vscene.part_sys.ScenePartSysBase import ScenePartSysBase
from logic.gutils.client_unit_tag_utils import preregistered_tags

class SysAimPoisonWarning(ScenePartSysBase):
    GLOBAL_EVENTS = {'on_observer_poison_status_changed': '_poison_status_changed',
       'camera_switch_to_state_event': 'on_switch_to_camera_state'
       }

    def __init__(self):
        super(SysAimPoisonWarning, self).__init__()
        self._is_in_poison = False
        self.process_global_event(True)

    def destroy(self):
        self.process_global_event(False)

    def _poison_status_changed(self, is_in_poison):
        self._is_in_poison = is_in_poison
        self.check_show_warning()

    def check_show_warning(self):
        if self._is_in_poison and self.get_is_in_aim():
            self.on_show_warning_tips()
        else:
            self.close_aim_show_warning()

    @staticmethod
    def get_is_in_aim():
        is_in_aim = False
        if global_data.cam_lctarget:
            unit = global_data.cam_lctarget
            if unit.MASK & preregistered_tags.HUMAN_TAG_VALUE:
                is_in_aim = global_data.cam_lctarget.sd.ref_in_aim
            elif unit.__class__.__name__ == 'LMecha':
                is_in_aim = global_data.cam_lctarget.sd.ref_in_open_aim
        return is_in_aim

    def on_switch_to_camera_state(self, state, old_state, is_finish):
        from logic.client.const.camera_const import AIM_MODE
        if state == AIM_MODE and is_finish:
            self.check_show_warning()
        if state != AIM_MODE and is_finish:
            self.close_aim_show_warning()

    def on_show_warning_tips(self):
        if global_data.cam_lplayer:
            from logic.gcommon.common_const import battle_const
            msg = {'i_type': battle_const.COMMON_AIM_POISON_TIPS
               }
            global_data.cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, battle_const.MAIN_NODE_COMMON_INFO)

    def close_aim_show_warning(self):
        from logic.gcommon.common_const import battle_const
        msg = {'i_type': battle_const.COMMON_AIM_POISON_TIPS
           }
        global_data.emgr.finish_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)