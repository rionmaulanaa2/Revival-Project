# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaTailEffect.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gcommon.cdata.mecha_status_config import *
from common.utils.timer import CLOCK
from common.cfg import confmgr
TAIL_SFX = {'effect/fx/mecha/tuowei/mecha_tuowei_01.sfx': ('part_point1', )}
TAIL_END_SFX = {'effect/fx/mecha/tuowei/mecha_tuowei_end.sfx': ('part_point1', )}
RAINBOW_TAIL_SFX = {'effect/fx/mecha/tuowei/mecha_tuowei_caihong.sfx': ('part_point1', )
   }

class ComMechaTailEffect(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaTailEffect, self).init_from_dict(unit_obj, bdict)
        self.tail_sfx_event_registered = False
        self.tail_sfx_ids = []
        self.tail_sfx_timer = None
        self.tail_disappear_sfx_timer = None
        self.add_tail_sfx_states = set()
        self.tail_sfx_max_duration = 10.0
        self.delay_remove_time = 0.5
        self.is_avatar = False
        self.tail_sfx_path = {'tail_sfx': TAIL_SFX,
           'tail_end_sfx': TAIL_END_SFX
           }
        return

    def destroy(self):
        if self.tail_sfx_event_registered:
            self.unregist_event('E_SHOW_TAIL_SFX', self.show_tail_sfx)
            self.unregist_event('E_ENTER_STATE', self.on_enter_state)
            self.unregist_event('E_LEAVE_STATE', self.on_leave_state)
            self.tail_sfx_event_registered = False
            self._remove_tail_sfx()
            self._unregister_tail_sfx_remove_timer()
            self._unregister_tail_disappear_sfx_timer()
        super(ComMechaTailEffect, self).destroy()

    def on_model_loaded(self, model):
        if global_data.is_inner_server and not self.tail_sfx_event_registered:
            self.regist_event('E_SHOW_TAIL_SFX', self.show_tail_sfx)
            self.regist_event('E_ENTER_STATE', self.on_enter_state)
            self.regist_event('E_LEAVE_STATE', self.on_leave_state)
            self.tail_sfx_event_registered = True
            self._unregister_tail_sfx_remove_timer()
            conf = confmgr.get('mecha_tail_sfx_config', str(self.sd.ref_mecha_id), default={})
            state_list = conf.get('tail_sfx_state_list', [])
            self.add_tail_sfx_states.clear()
            for state in state_list:
                self.add_tail_sfx_states.add(desc_2_num[state])

            skin_sfx_path_dict = conf.get('skin_sfx_path_dict', None)
            if skin_sfx_path_dict:
                skin_id, shiny_weapon_id = self.ev_g_mecha_skin_and_shiny_weapon_id()
                skin_id = str(skin_id)
                shiny_weapon_id = str(shiny_weapon_id)
                if skin_id in skin_sfx_path_dict:
                    if shiny_weapon_id in skin_sfx_path_dict[skin_id]:
                        self.tail_sfx_path = skin_sfx_path_dict[skin_id][shiny_weapon_id]
                    elif 'common' in skin_sfx_path_dict[skin_id]:
                        self.tail_sfx_path = skin_sfx_path_dict[skin_id]['common']
            self.tail_sfx_max_duration = conf.get('max_duration', self.tail_sfx_max_duration)
            self.delay_remove_time = conf.get('delay_remove_time', self.delay_remove_time)
            self.is_avatar = self.ev_g_is_avatar()
        return

    def _remove_tail_sfx(self):
        for sfx_id in self.tail_sfx_ids:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.tail_sfx_ids = []

    def show_tail_sfx(self, flag):
        if flag:
            if self.tail_sfx_ids:
                return
            model = self.ev_g_model()
            if not model or not model.valid:
                return
            tail_sfx_info = self.tail_sfx_path['tail_sfx']
            for path, sockets in six.iteritems(tail_sfx_info):
                for socket in sockets:
                    self.tail_sfx_ids.append(global_data.sfx_mgr.create_sfx_on_model(path, model, socket))

        else:
            self._remove_tail_sfx()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_TAIL_SFX, (flag,)], True)

    def _remove_tail_sfx_callback(self):
        self.show_tail_sfx(False)
        self.tail_sfx_timer = None
        return

    def _register_tail_sfx_remove_timer(self, interval=10.0):
        self._unregister_tail_sfx_remove_timer()
        self.tail_sfx_timer = global_data.game_mgr.register_logic_timer(self._remove_tail_sfx_callback, interval=interval, times=1, mode=CLOCK)

    def _unregister_tail_sfx_remove_timer(self):
        if self.tail_sfx_timer:
            global_data.game_mgr.unregister_logic_timer(self.tail_sfx_timer)
            self.tail_sfx_timer = None
        return

    def on_enter_state(self, enter_state):
        if enter_state in self.add_tail_sfx_states:
            self.show_tail_sfx(True)
            self._register_tail_sfx_remove_timer()

    def _unregister_tail_disappear_sfx_timer(self):
        if self.tail_disappear_sfx_timer:
            global_data.game_mgr.unregister_logic_timer(self.tail_disappear_sfx_timer)
            self.tail_disappear_sfx_timer = None
        return

    def _remove_tail_sfx_in_advance(self):
        self.tail_disappear_sfx_timer = None
        self._remove_tail_sfx()
        return

    def _show_disappear_tail_sfx(self):
        model = self.ev_g_model()
        self._unregister_tail_disappear_sfx_timer()
        self.tail_disappear_sfx_timer = global_data.game_mgr.register_logic_timer(self._remove_tail_sfx_in_advance, interval=0.18, times=1, mode=CLOCK)
        sfx_dict = self.tail_sfx_path['tail_end_sfx']
        for path, sockets in six.iteritems(sfx_dict):
            for socket in sockets:
                self.tail_sfx_ids.append(global_data.sfx_mgr.create_sfx_on_model(path, model, socket))

    def on_leave_state(self, leave_state, new_state=None):
        cur_state = self.ev_g_cur_state()
        if cur_state is None:
            cur_state = set()
        and_state = self.add_tail_sfx_states & cur_state
        if len(and_state) == 1 and leave_state in self.add_tail_sfx_states and new_state not in self.add_tail_sfx_states:
            self.is_avatar and self._show_disappear_tail_sfx()
            self._register_tail_sfx_remove_timer(self.delay_remove_time)
        return