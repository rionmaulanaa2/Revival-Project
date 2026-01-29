# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/pve/ComPveGainEffectShow.py
from logic.gcommon.component.UnitCom import UnitCom

class ComPveGainEffectShow(UnitCom):
    BIND_EVENT = {'E_SHOW_EFFECT_ENTRY': 'on_show_effect_entry',
       'E_CLEAR_EFFECT_ENTRY': 'on_clear_effect_entry',
       'G_PVE_EFFECT_DATA': 'get_effect_show_data'
       }

    def __init__(self):
        super(ComPveGainEffectShow, self).__init__()
        self._effect_show_data = {}

    def init_from_dict(self, unit_obj, bdict):
        super(ComPveGainEffectShow, self).init_from_dict(unit_obj, bdict)
        self._effect_show_data = bdict.get('effect_show_data', {})

    def on_show_effect_entry(self, effect_type, effect_id, start_time, end_time):
        self._effect_show_data.setdefault(effect_type, {})[effect_id] = [
         start_time, end_time]

    def on_clear_effect_entry(self, effect_type, effect_id):
        if effect_type in self._effect_show_data:
            self._effect_show_data[effect_type].pop(effect_id, None)
        return

    def get_effect_show_data(self):
        return self._effect_show_data