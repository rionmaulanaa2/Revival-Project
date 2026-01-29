# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8027.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
from common.utils import timer
import world
import math3d
import game3d
import render
import logic.gcommon.const as g_const
RUSH_HIT_EFFECT_ID = '8'

class ComMechaEffect8027(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_MODEL_LOADED': 'on_model_loaded',
       'E_CHRACTER_INITED': 'on_character_init',
       'E_DO_OXRUSH_8027': '_on_rush',
       'E_RUSH_HIT_TARGET_SFX': 'on_rush_hit_target_sfx'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8027, self).init_from_dict(unit_obj, bdict)
        self.check_timer = None
        self.mask = None
        return

    def destroy(self):
        self.clear_check_timer()
        super(ComMechaEffect8027, self).destroy()

    def on_model_loaded(self, model):
        super(ComMechaEffect8027, self).on_model_loaded(model)

    def on_character_init(self, character):
        self.mask = character.filter
        self.check_col()

    def _check_dask(self):
        if not self.mask:
            return
        is_hit = self.ev_g_static_test(mask=self.mask)
        if not is_hit:
            self.send_event('E_SET_CHAR_MASK', self.mask)
            self.clear_check_timer()

    def _on_rush(self, is_rush):
        if is_rush:
            self.send_event('E_SET_CHAR_MASK', ~self.mask)
        else:
            self.start_check_dask()

    def start_check_dask(self):
        self.clear_check_timer()
        self.check_timer = global_data.game_mgr.get_logic_timer().register(func=self._check_dask, mode=timer.CLOCK, interval=0.5)

    def clear_check_timer(self):
        self.check_timer and global_data.game_mgr.get_logic_timer().unregister(self.check_timer)
        self.check_timer = None
        return

    def check_col(self):
        if not self.mask:
            return
        is_hit = self.ev_g_static_test(mask=self.mask)
        if is_hit:
            self.send_event('E_SET_CHAR_MASK', ~self.mask)
            self.start_check_dask()

    def on_rush_hit_target_sfx(self, pos, rot=None):
        self.on_trigger_disposable_effect(RUSH_HIT_EFFECT_ID, pos, rot, need_sync=True)