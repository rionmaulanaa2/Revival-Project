# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_death/ComMechaModuleInstallEffect.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.component.UnitCom import UnitCom
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from common.cfg import confmgr
from logic.gcommon import time_utility as tutil
import math3d

class ComMechaModuleInstallEffect(UnitCom):
    BIND_EVENT = {'E_MECHA_MOUNT_COMPLETE': ('_on_join_mecha_finish', 10)
       }

    def __init__(self):
        super(ComMechaModuleInstallEffect, self).__init__(need_update=False)
        self._cur_recall_time = 0
        self._sfx_timer_id = None
        return

    def on_post_init_complete(self, bdict):
        self._cur_recall_time = self.ev_g_mecha_recall_times()

    def destroy(self):
        super(ComMechaModuleInstallEffect, self).destroy()
        if self._sfx_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._sfx_timer_id)
        self._sfx_timer_id = 0

    @execute_by_mode(True, game_mode_const.TDM_MechaModuleCallSfx)
    def _on_join_mecha_finish(self):
        if self.check_is_first_call_mecha():
            battle_duration = global_data.game_mode.get_cfg_data('play_data').get('battle_duration', 0)
            mecha_module_call_sfx = global_data.game_mode.get_cfg_data('play_data').get('mecha_module_call_sfx', [])
            battle_start_time = global_data.death_battle_data.settle_timestamp - battle_duration
            pass_time = tutil.get_server_time() - battle_start_time
            call_sfx_count = len(mecha_module_call_sfx)
            is_found = False
            play_sfx = ''
            for i in range(0, call_sfx_count - 1):
                cur_sfx_info = mecha_module_call_sfx[i]
                next_sfx_info = mecha_module_call_sfx[i + 1]
                if pass_time >= cur_sfx_info[0] and pass_time < next_sfx_info[0]:
                    play_sfx = cur_sfx_info[1]
                    is_found = True
                    break

            if not is_found and call_sfx_count >= 1:
                final_sfx_info = mecha_module_call_sfx[call_sfx_count - 1]
                if pass_time >= final_sfx_info[0]:
                    play_sfx = final_sfx_info[1]
            if play_sfx:
                from common.utils.timer import CLOCK
                self._sfx_timer_id = global_data.game_mgr.register_logic_timer(lambda : self.show_sfx(play_sfx), 0.8, times=1, mode=CLOCK)

    def show_sfx(self, play_sfx):
        if play_sfx:
            size = global_data.really_sfx_window_size
            scale = math3d.vector(size[0] / 1334.0, size[1] / 768.0, 1.0)

            def create_cb(sfx):
                sfx.scale = scale

            global_data.sfx_mgr.create_sfx_in_scene(play_sfx, on_create_func=create_cb)
        self._sfx_timer_id = None
        return

    def check_is_first_call_mecha(self):
        if self.ev_g_mecha_recall_times() == 1:
            return True
        else:
            return False

    def test(self):
        import math3d
        play_sfx = 'effect/fx/pingmu/acetime_pm_blue.sfx'
        size = global_data.really_sfx_window_size
        scale = math3d.vector(size[0] / 1334.0, size[1] / 768.0, 1.0)

        def create_cb(sfx):
            sfx.scale = scale

        global_data.sfx_mgr.create_sfx_in_scene(play_sfx, on_create_func=create_cb)