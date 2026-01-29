# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/com_lobby_appearance/ComLobbyCelebrate.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import lobby_ani_const
from common.cfg import confmgr

class ComLobbyCelebrate(UnitCom):
    BIND_EVENT = {'E_LOBBY_CELEBRATE': 'on_celebrate',
       'E_LOBBY_CELEBRATE_BREAK': 'on_celebrate_end',
       'E_ENTER_SCREENSHOT': 'on_enter_screenshot',
       'E_LEAVE_SCREENSHOT': 'on_leave_screenshot',
       'E_CAMERA_SLERP_END': 'on_camera_slerp_end',
       'E_ANIMATOR_LOADED': 'on_animator_loaded',
       'G_IS_CELEBRATE': 'is_celebrate',
       'G_IS_CAMERA_SLERP': 'is_camera_slerp'
       }

    def __init__(self):
        super(ComLobbyCelebrate, self).__init__()
        self._is_celebrate = False
        self._is_camera_slerp = False

    def destroy(self):
        super(ComLobbyCelebrate, self).destroy()

    def on_animator_loaded(self):
        self.register_animator_event()

    def register_animator_event(self):
        animator = self.ev_g_animator()

    def on_celebrate(self, item_no, is_puppet):
        animator = self.ev_g_animator()
        gesture_name = None
        if animator:
            ctrl_dir = self.ev_g_ctrl_dir()
            if animator.GetInt('state_idx') == lobby_ani_const.STATE_MOVE and ctrl_dir and ctrl_dir.length > 0:
                return
            gesture_items_conf = confmgr.get('gesture_conf', 'GestureConfig', 'Content')
            gesture_data = gesture_items_conf[str(item_no)]
            gesture_name = gesture_data['action_name']
            belong_to_role = gesture_data.get('belong_to_role', None)
            if belong_to_role and self.ev_g_role_id() not in belong_to_role:
                return
            model = self.ev_g_model()
            if not model or not model.valid or not model.has_anim(gesture_name):
                return
            if not is_puppet:
                self._is_celebrate = True
                if not self.ev_g_is_free_camera():
                    global_data.emgr.enable_lobby_player_free_cam.emit(True)
                animator.add_trigger_clip(gesture_name, 'end', self.on_celebrate_end)
            animator.replace_clip_name(lobby_ani_const.INTERACTION_NODE_NAME, gesture_name, force=True)
            if self.sd.ref_animator_mirror:
                self.sd.ref_animator_mirror.replace_clip_name(lobby_ani_const.INTERACTION_NODE_NAME, gesture_name, force=True)
        self.send_event('E_SET_ANIMATOR_INT_STATE', 'state_idx', lobby_ani_const.STATE_INTERACTION)
        if gesture_name:
            self.send_event('E_UPDATE_INTERACTION_NAME', gesture_name)
        return

    def on_celebrate_end(self, *args):
        if self._is_celebrate:
            self._is_celebrate = False
            is_screenshot = global_data.ui_mgr.get_ui('LobbySceneOnlyUI')
            if not is_screenshot:
                self._is_camera_slerp = True
                global_data.emgr.enable_lobby_player_free_cam.emit(False)
            self.send_event('E_SET_ANIMATOR_INT_STATE', 'state_idx', lobby_ani_const.STATE_IDLE)

    def is_celebrate(self):
        return self._is_celebrate

    def is_camera_slerp(self):
        return self._is_camera_slerp

    def is_screen_shot(self):
        return self._is_screenshot

    def on_camera_slerp_end(self):
        self._is_camera_slerp = False