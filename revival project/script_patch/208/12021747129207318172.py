# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLocalEditorServer.py
from __future__ import absolute_import
from . import ScenePart
from logic.gcommon.common_const.mecha_const import MECHA_TYPE_NORMAL, RECALL_CD_TYPE_NORMAL
from logic.gcommon import time_utility
from common.utils.timer import CLOCK
RECALL_MECHA_CD = 7

class PartLocalEditorServer(ScenePart.ScenePart):
    INIT_EVENT = {'battle_logic_ready_event': 'battle_logic_ready_callback',
       'try_summon_mecha_in_local_editor': 'try_summon_mecha',
       'try_leave_mecha_in_local_editor': 'try_leave_mecha',
       'reset_local_editor': 'on_reset'
       }

    def __init__(self, scene, name):
        super(PartLocalEditorServer, self).__init__(scene, name)
        self.editor = global_data.game_mgr.local_editor

    def after_exit(self):
        self.editor = None
        return

    def _process_lavatar_event(self, flag):
        func = self.editor.avatar.logic.regist_event if flag else self.editor.avatar.logic.unregist_event
        func('E_END_PUT_ON_BULLET', self.on_avatar_reloading)

    def on_avatar_reloading(self):
        lavatar = self.editor.avatar.logic
        weapon_pos = lavatar.ev_g_wpbar_cur_weapon_pos()
        wp = lavatar.ev_g_wpbar_cur_weapon()
        lavatar.send_event('E_WEAPON_BULLET_CHG', weapon_pos, wp.get_bullet_cap())

    def battle_logic_ready_callback(self):
        global_data.ui_mgr.close_ui('BattleLoadingWidget')
        self.editor.add_avatar()
        self._process_lavatar_event(True)
        global_data.ui_mgr.close_ui('NetworkLagUI')
        global_data.no_cd = True

    def _process_lmecha_event(self, flag):
        if not self.editor.mecha:
            return
        func = self.editor.mecha.logic.regist_event if flag else self.editor.mecha.logic.unregist_event
        func('E_RELOADING', self.on_mecha_reloading)

    def on_mecha_reloading(self, duration, times, weapon_pos):
        lmecha = self.editor.mecha.logic
        wp = lmecha.sd.ref_wp_bar_mp_weapons.get(weapon_pos)
        global_data.game_mgr.register_logic_timer(lambda : lmecha.send_event('E_WEAPON_BULLET_CHG', weapon_pos, wp.get_bullet_cap()), interval=duration, times=1, mode=CLOCK)

    def try_summon_mecha(self, mecha_id, mecha_position_tuple, skin_info=None):
        if self.editor.mecha:
            return
        avatar = self.editor.avatar
        self.editor.add_mecha(mecha_id, mecha_position_tuple, avatar.logic.ev_g_yaw(), skin_info)
        self._process_lmecha_event(True)
        self.editor.mecha.logic.send_event('E_ENTER_LOCAL_EDITOR_MODE')
        avatar.logic.send_event('E_ON_JOIN_MECHA_START', global_data.local_battle_const.MECHA_EID, MECHA_TYPE_NORMAL, time_utility.time(), False, {}, 'seat_1')
        avatar.logic.send_event('E_RECALL_SUCESS', True)

    def try_leave_mecha(self):
        if not self.editor.mecha:
            return
        else:
            if global_data.is_reloading_mecha_model_in_editor:
                return
            avatar = self.editor.avatar
            avatar.logic.send_event('E_ON_LEAVE_MECHA_START', None, time_utility.time(), False, False)
            avatar.logic.send_event('E_STATE_CHANGE_CD', RECALL_CD_TYPE_NORMAL, RECALL_MECHA_CD, RECALL_MECHA_CD)
            global_data.game_mgr.register_logic_timer(self.editor.remove_mecha, interval=5, times=1, mode=CLOCK)
            self._process_lmecha_event(False)
            return

    def on_reset(self):
        if global_data.is_reloading_mecha_model_in_editor:
            return
        self._process_lavatar_event(False)
        self._process_lmecha_event(False)
        self.editor.reset()
        self._process_lavatar_event(True)