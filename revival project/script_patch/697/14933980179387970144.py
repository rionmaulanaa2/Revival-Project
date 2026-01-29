# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffectMgr.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
MECHA_EFFECT_COM_DICT = {8001: [
        'ComMechaEffect8001'],
   8002: [
        'ComMechaEffect8002'],
   8003: [
        'ComMechaEffect8003'],
   8004: [
        'ComMechaEffect8004'],
   8005: [
        'ComMechaEffect8005'],
   8006: [
        'ComMechaEffect8006'],
   8007: [
        'ComMechaEffect8007'],
   8008: [
        'ComMechaEffect8008'],
   8009: [
        'ComMechaEffect8009'],
   8010: [
        'ComMechaEffect8010'],
   8011: [
        'ComMechaEffect8011'],
   8012: [
        'ComMechaEffect8012'],
   8013: [
        'ComMechaEffect8013'],
   8014: [
        'ComMechaEffect8014'],
   8015: [
        'ComMechaEffect8015'],
   8016: [
        'ComMechaEffect8016'],
   8017: [
        'ComMechaEffect8017'],
   8018: [
        'ComMechaEffect8018'],
   8019: [
        'ComMechaEffect8019'],
   8020: [
        'ComMechaEffect8020'],
   8021: [
        'ComMechaEffect8021'],
   8022: [
        'ComMechaEffect8022'],
   8023: [
        'ComMechaEffect8023'],
   8024: [
        'ComMechaEffect8024'],
   8025: [
        'ComMechaEffect8025'],
   8026: [
        'ComMechaEffect8026'],
   8027: [
        'ComMechaEffect8027'],
   8028: [
        'ComMechaEffect8028'],
   8029: [
        'ComMechaEffect8029'],
   8030: [
        'ComMechaEffect8030'],
   8031: [
        'ComMechaEffect8031'],
   8032: [
        'ComMechaEffect8032'],
   8033: [
        'ComMechaEffect8033'],
   8034: [
        'ComMechaEffect8034'],
   8035: [
        'ComMechaEffect8035'],
   8036: [
        'ComMechaEffect8036'],
   8037: [
        'ComMechaEffect8037'],
   8501: [
        'ComMechaEffect8501'],
   8502: [
        'ComMechaEffect8501'],
   8503: [
        'ComMechaEffect8501'],
   8504: [
        'ComMechaEffect8501'],
   4108: [
        'ComMechaEffect4108']
   }
GENERIC_MECHA_EFFECT_COMPONENTS = ('ComMechaEffectCommon', 'ComMechaBuffShieldEffect',
                                   'ComMechaTailEffect')

class ComMechaEffectMgr(UnitCom):

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffectMgr, self).init_from_dict(unit_obj, bdict)
        for mecha_effect_com in GENERIC_MECHA_EFFECT_COMPONENTS:
            com = unit_obj.add_com(mecha_effect_com, 'client.com_mecha_effect')
            if com:
                com.init_from_dict(unit_obj, bdict)

        mecha_id = bdict.get('mecha_id', None)
        if mecha_id in MECHA_EFFECT_COM_DICT:
            append_list = MECHA_EFFECT_COM_DICT.get(mecha_id, [])
            for mecha_effect_com in append_list:
                com = unit_obj.add_com(mecha_effect_com, 'client.com_mecha_effect')
                if com:
                    com.init_from_dict(unit_obj, bdict)

        return