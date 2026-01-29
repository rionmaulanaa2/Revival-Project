# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mode/ComReadyBox.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import collision_const
from logic.comsys.battle import BattleUtils
from common.utils import timer
import world
import math3d
import collision

class ComReadyBox(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': '_on_model_loaded',
       'E_ON_CAM_LCTARGET_SET': '_on_cam_lctarget_set'
       }

    def __init__(self):
        super(ComReadyBox, self).__init__()
        self.init_parameters()
        self.process_event(True)

    def init_from_dict(self, unit_obj, bdict):
        super(ComReadyBox, self).init_from_dict(unit_obj, bdict)

    def init_parameters(self):
        self.del_model_timer = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'battle_change_prepare_timestamp': self.change_prepare_timestamp,
           'battle_new_round': self._on_battle_new_round
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def clear_timer(self):
        self.del_model_timer and global_data.game_mgr.get_logic_timer().unregister(self.del_model_timer)
        self.del_model_timer = None
        return

    def _on_cam_lctarget_set(self):
        if global_data.cam_lplayer and global_data.player and global_data.cam_lplayer.id == global_data.player.id:
            return
        revive_time = BattleUtils.get_prepare_left_time()
        if revive_time > 0:
            self.set_see_throught()

    def set_see_throught(self):
        cam_lctarget = global_data.cam_lctarget
        if cam_lctarget and not cam_lctarget.ev_g_is_campmate(self.ev_g_camp_id()):
            self.send_event('E_ENABLE_SEE_THROUGHT', True)

    def change_prepare_timestamp(self):
        self.create_box()

    def _on_battle_new_round(self, *args, **kwargs):
        self.create_box()

    def _on_model_loaded(self, m):
        self.create_box()

    def create_box(self):
        revive_time = BattleUtils.get_prepare_left_time()
        is_show_range = revive_time > 0
        if is_show_range:
            self.set_see_throught()
            self.clear_timer()
            self.del_model_timer = global_data.game_mgr.get_logic_timer().register(func=self.destroy_model, mode=timer.CLOCK, interval=revive_time + 1, times=1)
        else:
            self.destroy_model()

    def destroy_model(self):
        self.send_event('E_ENABLE_SEE_THROUGHT', False)
        self.clear_timer()

    def destroy(self):
        self.destroy_model()
        self.process_event(False)
        super(ComReadyBox, self).destroy()