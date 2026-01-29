# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSignal.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_const import battle_const

class ComSignal(UnitCom):
    BIND_EVENT = {'G_SIGNAL': 'get_signal',
       'G_FULL_SIGNAL': 'is_full_signal',
       'G_MAX_SIGNAL': 'get_max_signal',
       'G_INIT_MAX_SIGNAL': 'get_init_max_signal',
       'G_SUB_SIGNAL': 'sub_signal',
       'E_RECOVER_SIGNAL': 'do_recover',
       'E_SET_MAX_SIGNAL': 'set_max_signal',
       'SET_SIGNAL': 'set_signal',
       'G_SIGNAL_PERCENT': 'get_signal_percent',
       'E_FULL_SIGNAL': 'full_signal',
       'G_SIGNAL_LEFT_TIME': 'get_signal_left_time',
       'E_SIGNAL_RATE_CHANGE': 'on_signal_rate_change',
       'G_SIGNAL_IN_POISON': 'is_in_poison',
       'E_IN_POISON': 'on_poison_change'
       }

    def __init__(self):
        super(ComSignal, self).__init__(need_update=False)
        self._max_signal = 0
        self.sd.ref_max_signal = 0
        self._cur_signal = 0
        self.sd.ref_cur_signal = 0
        self._init_max_signal = 0
        self._in_poison = False
        self._last_signal_reduce_rate = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComSignal, self).init_from_dict(unit_obj, bdict)
        self._max_signal = int(bdict.get('max_signal', 100))
        self.sd.ref_max_signal = self._max_signal
        self._cur_signal = int(bdict.get('signal', self._max_signal))
        self.sd.ref_cur_signal = self._cur_signal
        self._init_max_signal = int(bdict.get('init_max_signal', self._max_signal))
        self._in_poison = bdict.get('signal_in_poison', False)
        self._last_signal_reduce_rate = bdict.get('signal_reduce_rate', 0)
        unit_obj.send_event('E_SIGNAL_INIT', self._cur_signal, self._max_signal, self.get_signal_left_time())

    def destroy(self):
        super(ComSignal, self).destroy()

    def is_full_signal(self):
        return self._cur_signal >= self._max_signal

    def get_signal(self):
        return self._cur_signal

    def get_max_signal(self):
        return self._max_signal

    def get_init_max_signal(self):
        return self._init_max_hp

    def do_recover(self, delta):
        pre_signal = self._cur_signal
        self.add_signal(delta)
        recover_signal = self._cur_signal - pre_signal
        if recover_signal > 0:
            self.send_event('E_ON_RECOVER_SIGNAL', recover_signal)

    def add_signal(self, delta):
        if delta <= 0:
            return
        self.mod_signal(delta)

    def sub_signal(self, delta):
        if delta <= 0:
            return 0
        _pre = self._cur_signal
        self.mod_signal(-delta)
        return _pre - self._cur_signal

    def mod_signal(self, mod):
        self.set_signal(self._cur_signal + int(mod))

    def full_signal(self):
        self.set_signal(self._max_signal)

    def set_signal(self, signal):
        signal = min(max(0, signal), self._max_signal)
        if signal == self._cur_signal:
            return
        self._cur_signal = signal
        self.sd.ref_cur_signal = signal
        self.send_event('E_SIGNAL_CHANGE', self._cur_signal, self.get_signal_percent(), self.get_signal_left_time())
        if self._cur_signal <= 0:
            self.send_event('E_SIGNAL_EMPTY')
        if self._cur_signal == self._max_signal:
            self.send_event('E_GUIDE_FULL_SIGNAL')

    def get_signal_percent(self):
        return self._cur_signal * 1.0 / self._max_signal

    def on_signal_rate_change(self, in_poison, signal_reduce_rate):
        if global_data.player and self.unit_obj.id != global_data.player.id:
            self.on_poison_change(in_poison)
        self._last_signal_reduce_rate = signal_reduce_rate

    def get_signal_left_time(self):
        if self._last_signal_reduce_rate > 0:
            return int(self._cur_signal / self._last_signal_reduce_rate)
        else:
            return None

    def is_in_poison(self):
        return self._in_poison

    def on_poison_change(self, is_in_poison):
        if self._in_poison == is_in_poison:
            return
        self._in_poison = is_in_poison
        if not self.ev_g_is_cam_target():
            return
        inst = global_data.ui_mgr.get_ui('BattleSignalInfoUI')
        if inst:
            inst.on_poison_area_change(self.unit_obj.id, is_in_poison, self.get_signal_left_time())