# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/com_lobby_appearance/ComLobbyMoveAppr.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import lobby_ani_const

class ComLobbyMoveAppr(UnitCom):
    BIND_EVENT = {'E_ANIMATOR_LOADED': '_on_animator_loaded',
       'E_MOVE': 'on_move',
       'E_MOVE_STOP': 'on_move_stop',
       'E_ON_GROUND_FINISH': '_on_grounded',
       'E_ON_END_CLIMB': '_on_end_climb'
       }

    def __init__(self):
        super(ComLobbyMoveAppr, self).__init__()

    def _on_animator_loaded(self):
        self.replace_move_anim()
        is_moving = self.ev_g_is_move()
        self.on_move() if is_moving else self.on_move_stop()

    def on_move_stop(self, *args):
        self.on_move_state_changed()

    def on_move(self, *args):
        self.on_move_state_changed()

    def _on_grounded(self):
        self.on_move_state_changed()

    def _on_end_climb(self):
        self.on_move_state_changed()

    def on_move_state_changed(self):
        if self.ev_g_is_jump() or self.ev_g_is_climb():
            return
        if self.ev_g_is_camera_slerp():
            return
        self.send_event('E_SET_ANIMATOR_INT_STATE', 'state_idx', lobby_ani_const.STATE_MOVE)
        ctrl_dir = self.ev_g_ctrl_dir()
        if ctrl_dir and ctrl_dir.length > 0:
            if self.ev_g_is_free_camera():
                self.send_event('E_SET_ANIMATOR_FLOAT_STATE', 'dir_x', 0)
                self.send_event('E_SET_ANIMATOR_FLOAT_STATE', 'dir_z', 1)
            else:
                self.send_event('E_SET_ANIMATOR_FLOAT_STATE', 'dir_x', ctrl_dir.x)
                self.send_event('E_SET_ANIMATOR_FLOAT_STATE', 'dir_z', ctrl_dir.z)
        else:
            self.send_event('E_SET_ANIMATOR_FLOAT_STATE', 'dir_x', 0)
            self.send_event('E_SET_ANIMATOR_FLOAT_STATE', 'dir_z', 0)

    def replace_move_anim(self):
        model = self.ev_g_model()
        animator = self.ev_g_animator()
        if not animator:
            return
        animation_node = animator.find('blend_move')
        if not animation_node:
            return
        all_child_states = animation_node.GetChildStates()
        role_id = self.ev_g_role_id()
        for index, one_child_state in enumerate(all_child_states):
            one_source_node = one_child_state.childNode
            clip_name = one_source_node.clipName + '_' + str(role_id)
            if model.has_anim(clip_name):
                one_source_node.clipName = clip_name