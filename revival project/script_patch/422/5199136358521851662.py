# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComOuterShield.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_const import buff_const as bconst

class ComOuterShield(UnitCom):
    BIND_EVENT = {'E_OUTER_SHIELD_HP_CHANGED': '_on_outer_shield_changed',
       'E_MODEL_LOADED': '_on_model_loaded',
       'G_OUTER_SHIELD': 'get_outer_shield'
       }
    SFX_START_PATH = {8001: ('fx_hudun', 'effect/fx/mecha/8001/8001_hudun_start.sfx'),
       8012: ('shield', 'effect/fx/mecha/8012/8012_hudun_start.sfx')
       }
    SFX_END_PATH = {8001: ('fx_hudun', 'effect/fx/mecha/8001/8001_hudun_end.sfx'),
       8012: ('shield', 'effect/fx/mecha/8012/8012_hudun_end.sfx')
       }
    DELAY_CREATE = {8001: 0.0,
       8012: 0.7
       }

    def __init__(self):
        super(ComOuterShield, self).__init__()
        self.mecha_id = 8001
        self._sfx_start_info = None
        self._sfx_end_info = None
        self._outer_shield_hp = 0
        self._sfx_start = None
        self._sfx_end = None
        self._delay_create_time = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComOuterShield, self).init_from_dict(unit_obj, bdict)
        mecha_id = bdict.get('mecha_id', 8001)
        mecha_id = mecha_id if mecha_id in self.SFX_START_PATH else 8001
        self.mecha_id = mecha_id
        if mecha_id == 8012:
            mecha_id = 8001
        self._sfx_start_info = self.SFX_START_PATH[mecha_id]
        self._sfx_end_info = self.SFX_END_PATH[mecha_id]
        self._delay_create_time = self.DELAY_CREATE[mecha_id] if mecha_id in self.DELAY_CREATE else 0
        self._on_outer_shield_changed(bdict.get('outer_shield_hp', 0))

    def on_add_mecha_buff(self, buff_id, *args):
        if buff_id == bconst.BUFF_ID_OUTER_SHIELD and self.mecha_id == 8012:
            self._sfx_start_info = self.SFX_START_PATH[8012]
            self._sfx_end_info = self.SFX_END_PATH[8012]
            self._delay_create_time = self.DELAY_CREATE[8012]
            sfx_start, sfx_end = self._sfx_start, self._sfx_end
            self._clear_sfx()
            if sfx_start:
                if self._delay_create_time > 0:
                    global_data.game_mgr.delay_exec(self._delay_create_time, lambda : self._show_sfx())
                else:
                    self._show_sfx()
            elif sfx_end:
                self._hide_sfx()

    def on_del_mecha_buff(self, buff_id, *args):
        if buff_id == bconst.BUFF_ID_OUTER_SHIELD and self.mecha_id == 8012:
            self._sfx_start_info = self.SFX_START_PATH[8001]
            self._sfx_end_info = (
             self.SFX_END_PATH[8001][0], self.SFX_END_PATH[8012][1])
            self._delay_create_time = self.DELAY_CREATE[8001]
            sfx_start, sfx_end = self._sfx_start, self._sfx_end
            self._clear_sfx()
            if sfx_start:
                if self._delay_create_time > 0:
                    global_data.game_mgr.delay_exec(self._delay_create_time, lambda : self._show_sfx())
                else:
                    self._show_sfx()
            elif sfx_end:
                self._hide_sfx()

    def _on_outer_shield_changed(self, outer_shield_hp):
        diff = self._outer_shield_hp - outer_shield_hp
        self._outer_shield_hp = outer_shield_hp

    def get_outer_shield(self):
        return self._outer_shield_hp

    def _on_model_loaded(self, *args):
        self._on_outer_shield_changed(self._outer_shield_hp)

    def _show_sfx(self):
        if not self or not self.is_valid():
            return
        if self._outer_shield_hp <= 0:
            return
        if self._sfx_start:
            return
        self._clear_sfx()
        model = self.ev_g_model()
        if not model:
            return
        socket, path = self._sfx_start_info
        self._sfx_start = global_data.sfx_mgr.create_sfx_on_model(path, model, socket, on_create_func=lambda sfx: self._on_create_sfx(sfx))

    def _hide_sfx(self):
        self._clear_sfx()
        model = self.ev_g_model()
        if not model:
            return
        socket, path = self._sfx_end_info
        self._sfx_end = global_data.sfx_mgr.create_sfx_on_model(path, model, socket, on_create_func=lambda sfx: self._on_create_sfx(sfx))

    def _on_create_sfx(self, sfx):
        import math3d
        sfx.position = math3d.vector(0, -26, 0)

    def _clear_sfx(self):
        if self._sfx_start:
            global_data.sfx_mgr.remove_sfx_by_id(self._sfx_start)
            self._sfx_start = None
        if self._sfx_end:
            global_data.sfx_mgr.remove_sfx_by_id(self._sfx_end)
            self._sfx_end = None
        return

    def destroy(self):
        self._clear_sfx()
        super(ComOuterShield, self).destroy()