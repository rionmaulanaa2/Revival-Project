# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComInfinityLightBall8017.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import PART_WEAPON_POS_MAIN6

class ComInfinityLightBall8017(UnitCom):
    BIND_EVENT = {'E_ENABLE_8017_INFINITY_LIGHT_BALL': 'enable_infinity_light_ball',
       'E_GRENADE_SELF_INTRO': 'on_grenade_self_intro',
       'E_MODEL_LOADED': 'on_model_loaded'
       }

    def __init__(self):
        super(ComInfinityLightBall8017, self).__init__()
        self._infinity_light_ball_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComInfinityLightBall8017, self).init_from_dict(unit_obj, bdict)
        self._infinity_light_ball_active = bdict.get('_infinity_light_ball_active', False)

    def on_model_loaded(self, *args):
        if self._infinity_light_ball_active:
            self.enable_infinity_light_ball(True)

    def on_grenade_self_intro(self, _infinity_light_ball_id):
        if self._infinity_light_ball_id:
            grenade = global_data.battle.get_entity(self._infinity_light_ball_id)
            if grenade and grenade.logic:
                grenade.logic.send_event('E_FORCE_EXPLODE')
        self._infinity_light_ball_id = _infinity_light_ball_id

    def enable_infinity_light_ball(self, enable):
        self._infinity_light_ball_active = enable
        if enable:
            if not self.ev_g_try_weapon_attack_begin(PART_WEAPON_POS_MAIN6):
                return
            self.send_event('E_DO_SKILL', 801755)
            self.ev_g_try_weapon_attack_end(PART_WEAPON_POS_MAIN6)
            self.send_event('E_ACC_SKILL_END')
        elif self._infinity_light_ball_id:
            grenade = global_data.battle.get_entity(self._infinity_light_ball_id)
            if grenade and grenade.logic:
                grenade.logic.send_event('E_FORCE_EXPLODE')
            self._infinity_light_ball_id = None
        return