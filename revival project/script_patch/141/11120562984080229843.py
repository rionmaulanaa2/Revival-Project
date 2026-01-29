# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_human_effect/ComHumanEffectMgr.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
HUMAN_EFFECT_COM_DICT = {}

class ComHumanEffectMgr(UnitCom):

    def init_from_dict(self, unit_obj, bdict):
        super(ComHumanEffectMgr, self).init_from_dict(unit_obj, bdict)
        effect_list = [
         'ComHumanEffectCommon', 'ComHumanSkateEffect']
        for human_effect_com in effect_list:
            com = unit_obj.add_com(human_effect_com, 'client.com_human_effect')
            if com:
                com.init_from_dict(unit_obj, bdict)