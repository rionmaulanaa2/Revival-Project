# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/Meta/Generated.py
from __future__ import absolute_import
from . import TrackMeta, TCustomCue
from . import OrderedProperties, PBool, PFloat, PInt, PStr, PVector2, PEnum
from sunshine.SunshineSDK.Meta.EnumMeta import DefEnum

@TrackMeta
class TXMLCustomCue(TCustomCue):

    def Serialize(self, model):
        p = model.properties
        datastr = ''
        for key, item in self.FRAME_PROPERTIES.items():
            if isinstance(item, PBool):
                datastr += '1' if p[key] else '0'
            elif isinstance(item, PFloat):
                datastr += str(p[key])
            elif isinstance(item, PInt):
                datastr += str(p[key])
            elif isinstance(item, PStr):
                datastr += p[key]
            elif isinstance(item, PVector2):
                datastr += '%d:%d' % (p[key][0], p[key][1])
            elif isinstance(item, PEnum):
                datastr += str(p[key])
            else:
                continue
            datastr += ':'

        if len(datastr) == 0:
            return '1'
        return datastr[:-1]


DefEnum('custom3Type_1', {0: 'COMBO_START',1: 'COMBO_END',2: 'COMBO_FAILED',3: 'SKILL_POST',4: 'SKILL_MOVEPOST'})
DefEnum('custom9Type_0', {0: 'LeftHandWeapon',1: 'RightHandWeapon'})
DefEnum('custom11Type_1', {0: 'root',
   1: 'originPos',
   2: 'camera',
   3: 'HP_hit',
   4: 'HP_hit_back',
   5: 'HP_spell1',
   6: 'HP_spell2',
   7: 'HP_spell8',
   8: 'HP_state1',
   9: 'HP_state2',
   10: 'HP_blade1',
   11: 'HP_blade2',
   12: 'HP_blade3',
   13: 'HP_blade4',
   14: 'HP_blade5',
   15: 'HP_blade6',
   16: 'HP_hand_left',
   17: 'HP_hand_left_inv',
   18: 'HP_hand_left1',
   19: 'HP_hand_right',
   20: 'HP_hand_right_inv',
   21: 'HP_hand_right1',
   22: 'HP_neck',
   23: 'HP_ride',
   24: 'HP_waist_left',
   25: 'HP_waist_right',
   26: 'Bone01',
   27: 'Target_root',
   28: 'Weapon_HP_effect1',
   29: 'Weapon_HP_effect2',
   30: 'Weapon_HP_effect3',
   31: 'Weapon_HP_blade1',
   32: 'Weapon_HP_blade2',
   33: 'Armor_HP_effect1',
   34: 'Armor_HP_effect2',
   35: 'Armor_HP_effect3',
   36: 'Armor_HP_blade1',
   37: 'Armor_HP_blade2',
   38: 'HP_back_up1',
   39: 'HP_back_up2',
   40: 'HP_clavicle_left',
   41: 'HP_clavicle_right',
   42: 'HP_crus_left',
   43: 'HP_crus_right',
   44: 'HP_forearm_left',
   45: 'HP_forearm_right',
   46: 'HP_break1',
   47: 'HP_back_down',
   48: 'Weapon_Bone01',
   49: 'Weapon_Bone02',
   50: 'Weapon_Bone03',
   51: 'Weapon_Bone04',
   52: 'Weapon_Bone05',
   53: 'Weapon_Bone06',
   54: 'Weapon_Bone07',
   55: 'Weapon_Bone08',
   56: 'Weapon_Bone09',
   57: 'Weapon_Bone10',
   58: 'Weapon_Bone11',
   59: 'Weapon_Bone12',
   60: 'Weapon_Bone13',
   61: 'Weapon_Bone14',
   62: 'Weapon_Bone15',
   63: 'Weapon_Bone16',
   64: 'HP_armor1',
   65: 'HP_wing',
   66: 'HP_head',
   67: 'HP_piao1',
   68: 'HP_piao2',
   69: 'cs_bone37',
   70: 'HP_state06',
   71: 'HP_state08',
   72: 'HP_state10',
   73: 'HP_state12',
   74: 'HP_cos_hat',
   75: 'HP_cos_forehead',
   76: 'HP_cos_furryear_right',
   77: 'HP_cos_furryear_left',
   78: 'HP_cos_glasses',
   79: 'HP_cos_respirator',
   80: 'HP_cos_eardrop_right',
   81: 'HP_cos_eardrop_left'
   })
DefEnum('custom11Type_2', {0: 'root',
   1: 'originPos',
   2: 'camera',
   3: 'HP_hit',
   4: 'HP_hit_back',
   5: 'HP_spell1',
   6: 'HP_spell2',
   7: 'HP_spell8',
   8: 'HP_state1',
   9: 'HP_state2',
   10: 'HP_blade1',
   11: 'HP_blade2',
   12: 'HP_blade3',
   13: 'HP_blade4',
   14: 'HP_blade5',
   15: 'HP_blade6',
   16: 'HP_hand_left',
   17: 'HP_hand_left_inv',
   18: 'HP_hand_left1',
   19: 'HP_hand_right',
   20: 'HP_hand_right_inv',
   21: 'HP_hand_right1',
   22: 'HP_neck',
   23: 'HP_ride',
   24: 'HP_waist_left',
   25: 'HP_waist_right',
   26: 'Bone01',
   27: 'Target_root',
   28: 'Weapon_HP_effect1',
   29: 'Weapon_HP_effect2',
   30: 'Weapon_HP_effect3',
   31: 'Weapon_HP_blade1',
   32: 'Weapon_HP_blade2',
   33: 'Armor_HP_effect1',
   34: 'Armor_HP_effect2',
   35: 'Armor_HP_effect3',
   36: 'Armor_HP_blade1',
   37: 'Armor_HP_blade2',
   38: 'HP_back_up1',
   39: 'HP_back_up2',
   40: 'HP_clavicle_left',
   41: 'HP_clavicle_right',
   42: 'HP_crus_left',
   43: 'HP_crus_right',
   44: 'HP_forearm_left',
   45: 'HP_forearm_right',
   46: 'HP_break1',
   47: 'HP_back_down',
   48: 'Weapon_Bone01',
   49: 'Weapon_Bone02',
   50: 'Weapon_Bone03',
   51: 'Weapon_Bone04',
   52: 'Weapon_Bone05',
   53: 'Weapon_Bone06',
   54: 'Weapon_Bone07',
   55: 'Weapon_Bone08',
   56: 'Weapon_Bone09',
   57: 'Weapon_Bone10',
   58: 'Weapon_Bone11',
   59: 'Weapon_Bone12',
   60: 'Weapon_Bone13',
   61: 'Weapon_Bone14',
   62: 'Weapon_Bone15',
   63: 'Weapon_Bone16',
   64: 'HP_armor1',
   65: 'HP_wing',
   66: 'HP_head',
   67: 'HP_piao1',
   68: 'HP_piao2',
   69: 'cs_bone37',
   70: 'HP_state06',
   71: 'HP_state08',
   72: 'HP_state10',
   73: 'HP_state12',
   74: 'HP_cos_hat',
   75: 'HP_cos_forehead',
   76: 'HP_cos_furryear_right',
   77: 'HP_cos_furryear_left',
   78: 'HP_cos_glasses',
   79: 'HP_cos_respirator',
   80: 'HP_cos_eardrop_right',
   81: 'HP_cos_eardrop_left'
   })
DefEnum('custom22Type_0', {0: 'Begin',1: 'End'})
DefEnum('custom43Type_0', {0: 'Linear',1: 'Parabola',2: 'Decay'})
DefEnum('custom44Type_0', {0: 'Linear',1: 'Parabola',2: 'Ladder'})
DefEnum('custom32762Type_0', {0: 'OpenInputDialog',
   1: 'UpdateInputDialog',
   2: 'CloseInputDialog',
   3: 'SyncStart',
   4: 'SelectTarget',
   5: 'PrePlayResult',
   6: 'ExitQTE',
   7: 'OnJumpNewState',
   8: 'MoveToCliff',
   9: 'MoveToSafeLand',
   10: 'SetDestSafeLand',
   11: 'SuicideToPos',
   12: 'SetDestByParam',
   13: 'UseCinemaOrbit',
   14: 'CancelCinemaOrbit'
   })

@TrackMeta
class Tcustom1(TXMLCustomCue):
    CUEID = 1
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PStr(text='Media \xe8\xb7\xaf\xe5\xbe\x84:'))])


@TrackMeta
class Tcustom2(TXMLCustomCue):
    CUEID = 2
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PStr(text='\xe6\x8c\x82\xe6\x8e\xa5\xe7\x89\xb9\xe6\x95\x88'))])


@TrackMeta
class Tcustom3(TXMLCustomCue):
    CUEID = 3
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PInt(text='\xe6\x8a\x80\xe8\x83\xbd\xe7\xbc\x96\xe5\x8f\xb7:', default=0, min=0, max=200000)),
     (
      'param1', PEnum(text='\xe4\xba\x8b\xe4\xbb\xb6\xe6\xa0\x87\xe8\xaf\x86:', default=0, enumType='custom3Type_1'))])


@TrackMeta
class Tcustom4(TXMLCustomCue):
    CUEID = 4
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PInt(text='\xe6\x8a\x80\xe8\x83\xbd\xe7\xbc\x96\xe5\x8f\xb7:', default=0, min=0, max=200000)),
     (
      'param1', PFloat(text='\xe4\xbc\xa4\xe5\xae\xb3\xe6\x9d\x83\xe9\x87\x8d:', default=1.0, min=0, max=1)),
     (
      'param2', PFloat(text='\xe6\x8f\x92\xe5\xb8\xa7\xe9\x80\x9f\xe7\x8e\x87:', default=1.0, min=0, max=1)),
     (
      'param3', PFloat(text='\xe6\x8f\x92\xe5\xb8\xa7\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4:', default=0.0, min=0, max=10000)),
     (
      'param4', PFloat(text='\xe6\xb7\xa1\xe5\x85\xa5\xe6\x97\xb6\xe9\x97\xb4:', default=0.0, min=0, max=10000)),
     (
      'param5', PFloat(text='\xe6\xb7\xa1\xe5\x87\xba\xe6\x97\xb6\xe9\x97\xb4:', default=0.0, min=0, max=10000)),
     (
      'param6', PInt(text='\xe6\x8c\xaf\xe5\x8a\xa8\xe7\xb1\xbb\xe5\x9e\x8b:', default=0, min=0, max=10)),
     (
      'param7', PFloat(text='\xe6\x8c\xaf\xe5\xb9\x85:', default=1, min=0.001, max=100000)),
     (
      'param8', PFloat(text='\xe6\x8c\xaf\xe5\x8a\xa8\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4:', default=1, min=0.001, max=100000)),
     (
      'param9', PFloat(text='\xe6\x8c\xaf\xe5\xb9\x85\xe8\xa1\xb0\xe5\x87\x8f\xe7\xb3\xbb\xe6\x95\xb0:', default=0.2, min=0.001, max=1)),
     (
      'param10', PFloat(text='\xe6\x8c\xaf\xe5\x8a\xa8\xe5\xbe\xaa\xe7\x8e\xaf\xe6\xac\xa1\xe6\x95\xb0:', default=1, min=1, max=100000)),
     (
      'param11', PFloat(text='\xe5\x8f\x97\xe5\x87\xbb\xe6\x96\xb9\xe6\x8f\x92\xe5\xb8\xa7\xe9\x80\x9f\xe7\x8e\x87:', default=1.0, min=0, max=1)),
     (
      'param12', PFloat(text='\xe5\x8f\x97\xe5\x87\xbb\xe6\x96\xb9\xe6\x8f\x92\xe5\xb8\xa7\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4:', default=0.0, min=0, max=10000)),
     (
      'param13', PFloat(text='\xe5\x8f\x97\xe5\x87\xbb\xe6\x96\xb9\xe6\xb7\xa1\xe5\x85\xa5\xe6\x97\xb6\xe9\x97\xb4:', default=0.0, min=0, max=10000)),
     (
      'param14', PFloat(text='\xe5\x8f\x97\xe5\x87\xbb\xe6\x96\xb9\xe6\xb7\xa1\xe5\x87\xba\xe6\x97\xb6\xe9\x97\xb4:', default=0.0, min=0, max=10000))])


@TrackMeta
class Tcustom6(TXMLCustomCue):
    CUEID = 6
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PInt(text='\xe6\x8a\x80\xe8\x83\xbd\xe7\xbc\x96\xe5\x8f\xb7:', default=0, min=0, max=200000))])


@TrackMeta
class Tcustom7(TXMLCustomCue):
    CUEID = 7
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PInt(text='\xe6\x8a\x80\xe8\x83\xbd\xe7\xbc\x96\xe5\x8f\xb7:', default=0, min=0, max=200000))])


@TrackMeta
class Tcustom8(TXMLCustomCue):
    CUEID = 8
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PStr(text='\xe6\x8c\x82\xe6\x8e\xa5\xe9\x9f\xb3\xe6\x95\x88:'))])


@TrackMeta
class Tcustom28(TXMLCustomCue):
    CUEID = 28
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PStr(text='Bnk\xe5\x90\x8d\xe7\xa7\xb0:')),
     (
      'param1', PStr(text='\xe5\xa3\xb0\xe9\x9f\xb3\xe4\xba\x8b\xe4\xbb\xb6\xe5\x90\x8d\xe7\xa7\xb0:')),
     (
      'param2', PStr(text='Switch Group:'))])


@TrackMeta
class Tcustom9(TXMLCustomCue):
    CUEID = 9
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PEnum(text='\xe7\xbb\x84\xe4\xbb\xb6\xe5\x90\x8d\xe7\xa7\xb0', default=0, enumType='custom9Type_0')),
     (
      'param1', PFloat(text='\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4(\xe7\xa7\x92):', default=-1, min=-1, max=10000))])


@TrackMeta
class Tcustom11(TXMLCustomCue):
    CUEID = 11
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PStr(text='\xe7\x89\xb9\xe6\x95\x88\xe5\x90\x8d\xe7\xa7\xb0:', default='1001/ParticleSystem0')),
     (
      'param1', PEnum(text='\xe7\x89\xb9\xe6\x95\x88\xe6\x8c\x82\xe6\x8e\xa5\xe4\xbd\x8d\xe7\xbd\xae:', default=0, enumType='custom11Type_1')),
     (
      'param2', PEnum(text='\xe5\xaf\xb9\xe6\x96\xb9\xe7\x89\xb9\xe6\x95\x88\xe6\x8c\x82\xe6\x8e\xa5\xe4\xbd\x8d\xe7\xbd\xae:', default=0, enumType='custom11Type_2')),
     (
      'param3', PFloat(text='\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4(\xe7\xa7\x92):', default=-1, min=-1, max=10000))])


@TrackMeta
class Tcustom12(TXMLCustomCue):
    CUEID = 12
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PInt(text='\xe7\xb1\xbb\xe5\x9e\x8b:', default=0, min=0, max=10)),
     (
      'param1', PFloat(text='\xe6\x8c\xaf\xe5\xb9\x85:', default=1, min=0.001, max=100000)),
     (
      'param2', PFloat(text='\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4:', default=1, min=0.001, max=100000)),
     (
      'param3', PFloat(text='\xe6\x8c\xaf\xe5\xb9\x85\xe8\xa1\xb0\xe5\x87\x8f\xe7\xb3\xbb\xe6\x95\xb0:', default=0.2, min=0.001, max=1)),
     (
      'param4', PFloat(text='\xe5\xbe\xaa\xe7\x8e\xaf\xe6\xac\xa1\xe6\x95\xb0:', default=1, min=1, max=100000)),
     (
      'param5', PBool(text='\xe5\xbc\xba\xe5\x88\xb6\xe9\x9c\x87\xe5\x8a\xa8:', default=False))])


@TrackMeta
class Tcustom13(TXMLCustomCue):
    CUEID = 13
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PFloat(text='\xe6\x8f\x92\xe5\xb8\xa7\xe9\x80\x9f\xe7\x8e\x87:', default=1.0, min=0, max=1)),
     (
      'param1', PFloat(text='\xe6\x8f\x92\xe5\xb8\xa7\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4:', default=0.0, min=0, max=10000)),
     (
      'param2', PFloat(text='\xe6\xb7\xa1\xe5\x85\xa5\xe6\x97\xb6\xe9\x97\xb4:', default=0.0, min=0, max=10000)),
     (
      'param3', PFloat(text='\xe6\xb7\xa1\xe5\x87\xba\xe6\x97\xb6\xe9\x97\xb4:', default=0.0, min=0, max=10000))])


@TrackMeta
class Tcustom14(TXMLCustomCue):
    CUEID = 14
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PInt(text='\xe9\x98\xb6\xe6\xae\xb5:', default=0, min=0, max=1)),
     (
      'param1', PFloat(text='\xe8\xb7\x9f\xe9\x9a\x8f\xe9\x80\x9f\xe7\x8e\x87:', default=10.0, min=0.2, max=100))])


@TrackMeta
class Tcustom15(TXMLCustomCue):
    CUEID = 15
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PInt(text='\xe5\x8f\xaf\xe8\xa7\x81\xe6\xa0\x87\xe5\xbf\x97\xe4\xbd\x8d', default=0, min=0, max=1))])


@TrackMeta
class Tcustom16(TXMLCustomCue):
    CUEID = 16
    FRAME_PROPERTIES = OrderedProperties([])


@TrackMeta
class Tcustom17(TXMLCustomCue):
    CUEID = 17
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PStr(text='\xe7\x89\xb9\xe6\x95\x88id:', default='EffectMonster/boss01_sc04_fei')),
     (
      'param1', PStr(text='\xe5\xad\x90\xe5\xbc\xb9\xe7\x9a\x84Graph\xe8\xb7\xaf\xe5\xbe\x84:'))])


@TrackMeta
class Tcustom18(TXMLCustomCue):
    CUEID = 18
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PFloat(text='\xe6\x95\x88\xe6\x9e\x9c\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4', default=1.0, min=0, max=9999)),
     (
      'param1', PFloat(text='\xe6\xb7\xa1\xe5\x87\xba\xe6\x97\xb6\xe9\x97\xb4', default=1.0, min=0, max=9999)),
     (
      'param2', PStr(text='UI\xe8\xb5\x84\xe6\xba\x90\xe7\x9a\x84\xe6\x96\x87\xe4\xbb\xb6\xe5\x90\x8d\xef\xbc\x8c\xe8\xa6\x81\xe6\xb1\x82\xe5\x86\x99UIScript\xe7\x9b\xae\xe5\xbd\x95\xe4\xb8\x8b\xe7\x9a\x84\xe6\x96\x87\xe4\xbb\xb6\xe5\x90\x8d', default='Screenbroken.csb'))])


@TrackMeta
class Tcustom19(TXMLCustomCue):
    CUEID = 19
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PStr(text='Motor\xe7\xb1\xbb\xe5\x9e\x8b', default='default'))])


@TrackMeta
class Tcustom20(TXMLCustomCue):
    CUEID = 20
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PFloat(text='\xe6\xa8\xa1\xe7\xb3\x8a\xe7\xa8\x8b\xe5\xba\xa6', default=1.0, min=0, max=1)),
     (
      'param1', PFloat(text='\xe5\xa4\x9a\xe5\xb0\x91\xe7\xa7\x92\xe5\x86\x85\xe6\xa8\xa1\xe7\xb3\x8a\xe5\x88\xb0\xe6\x8c\x87\xe5\xae\x9a\xe7\xa8\x8b\xe5\xba\xa6', default=0, min=0, max=9999)),
     (
      'param2', PFloat(text='\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4', default=1.0, min=0, max=9999)),
     (
      'param3', PFloat(text='\xe6\xa8\xa1\xe7\xb3\x8a\xe6\xb6\x88\xe5\xa4\xb1\xe7\x9a\x84\xe6\xb8\x90\xe5\x8f\x98\xe6\x97\xb6\xe9\x97\xb4', default=0, min=0, max=9999)),
     (
      'param4', PBool(text='\xe6\x98\xaf\xe5\x90\xa6\xe5\xbc\xba\xe5\x88\xb6\xe4\xbd\xbf\xe7\x94\xa8', default=False))])


@TrackMeta
class Tcustom21(TXMLCustomCue):
    CUEID = 21
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PFloat(text='\xe7\xba\xa2\xef\xbc\x88R\xef\xbc\x89', default=0, min=0, max=1)),
     (
      'param1', PFloat(text='\xe7\xbb\xbf\xef\xbc\x88G\xef\xbc\x89', default=0, min=0, max=1)),
     (
      'param2', PFloat(text='\xe8\x93\x9d\xef\xbc\x88B\xef\xbc\x89', default=0, min=0, max=1)),
     (
      'param3', PFloat(text='\xe6\x9f\x93\xe8\x89\xb2\xe6\xaf\x94\xe4\xbe\x8b\xef\xbc\x8c0\xe4\xb8\xba\xe4\xb8\x8d\xe6\x9f\x93\xe8\x89\xb2\xef\xbc\x8c1\xe4\xb8\xba\xe5\xae\x8c\xe5\x85\xa8\xe6\x9f\x93\xe8\x89\xb2', default=0, min=0, max=1)),
     (
      'param4', PFloat(text='\xe6\x9f\x93\xe8\x89\xb2\xe7\x9a\x84\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4', default=1, min=0, max=9999)),
     (
      'param5', PBool(text='\xe6\x98\xaf\xe5\x90\xa6\xe5\xbc\xba\xe5\x88\xb6\xe4\xbd\xbf\xe7\x94\xa8', default=False))])


@TrackMeta
class Tcustom22(TXMLCustomCue):
    CUEID = 22
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PEnum(text='\xe5\x8a\xa8\xe4\xbd\x9c\xe5\xbc\x80\xe5\xa7\x8b\xe6\x88\x96\xe7\xbb\x93\xe6\x9d\x9f', default=0, enumType='custom22Type_0'))])


@TrackMeta
class Tcustom23(TXMLCustomCue):
    CUEID = 23
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PStr(text='\xe5\xbd\x93\xe5\x89\x8d\xe8\x8a\x82\xe7\x82\xb9\xe5\x90\x8d\xe5\xad\x97'))])


@TrackMeta
class Tcustom24(TXMLCustomCue):
    CUEID = 24
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PBool(text='\xe6\x98\xaf\xe5\x90\xa6\xe7\xab\x8b\xe5\x8d\xb3\xe6\x8b\x89\xe5\x9b\x9e', default=True)),
     (
      'param1', PFloat(text='\xe5\xa4\x9a\xe5\xb0\x91\xe6\x97\xb6\xe9\x97\xb4\xe7\xa6\x81\xe6\xad\xa2\xe7\x8e\xa9\xe5\xae\xb6\xe8\xb0\x83\xe6\x95\xb4\xe8\xa7\x86\xe8\xa7\x92', default=1, min=0.5, max=9999))])


@TrackMeta
class Tcustom43(TXMLCustomCue):
    CUEID = 43
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PEnum(text='\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87\xe8\xbf\x87\xe6\xb8\xa1\xe6\xa8\xa1\xe5\xbc\x8f', default=0, enumType='custom43Type_0')),
     (
      'param1', PFloat(text='\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87\xe7\x9b\xae\xe6\xa0\x87\xe5\x80\xbc', default=0, min=-100, max=100)),
     (
      'param2', PFloat(text='\xe8\xbf\x87\xe6\xb8\xa1\xe6\x97\xb6\xe9\x97\xb4', default=0.2, min=0, max=100))])


@TrackMeta
class Tcustom44(TXMLCustomCue):
    CUEID = 44
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PEnum(text='\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87\xe7\xaa\x81\xe5\x8f\x98\xe8\xbf\x87\xe6\xb8\xa1\xe6\xa8\xa1\xe5\xbc\x8f', default=0, enumType='custom44Type_0')),
     (
      'param1', PFloat(text='\xe6\x92\xad\xe6\x94\xbe\xe9\x80\x9f\xe7\x8e\x87\xe7\xaa\x81\xe5\x8f\x98\xe7\x9b\xae\xe6\xa0\x87\xe5\x80\xbc', default=0, min=-100, max=100)),
     (
      'param2', PFloat(text='\xe5\x88\x9d\xe5\xa7\x8b\xe7\x8a\xb6\xe6\x80\x81\xe8\x87\xb3\xe7\xaa\x81\xe5\x8f\x98\xe5\x80\xbc\xe8\xbf\x87\xe6\xb8\xa1\xe6\x97\xb6\xe9\x97\xb4', default=0.2, min=0, max=100)),
     (
      'param3', PFloat(text='\xe7\xaa\x81\xe5\x8f\x98\xe7\x8a\xb6\xe6\x80\x81\xe6\x81\xa2\xe5\xa4\x8d\xe6\x97\xb6\xe9\x97\xb4', default=0.2, min=0, max=100))])


@TrackMeta
class Tcustom50(TXMLCustomCue):
    CUEID = 50
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PStr(text='TargetSlot', default='main')),
     (
      'param1', PStr(text='Skeleton\xe8\xb7\xaf\xe5\xbe\x84')),
     (
      'param2', PStr(text='Model\xe8\xb7\xaf\xe5\xbe\x84')),
     (
      'param3', PStr(text='Graph\xe8\xb7\xaf\xe5\xbe\x84'))])


@TrackMeta
class Tcustom51(TXMLCustomCue):
    CUEID = 51
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PStr(text='TargetSlot'))])


@TrackMeta
class Tcustom52(TXMLCustomCue):
    CUEID = 52
    FRAME_PROPERTIES = OrderedProperties([])


@TrackMeta
class Tcustom60(TXMLCustomCue):
    CUEID = 60
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PInt(text='\xe7\x88\xac\xe5\xa2\x99\xe7\x8a\xb6\xe6\x80\x81', default=0, min=0, max=100))])


@TrackMeta
class Tcustom32762(TXMLCustomCue):
    CUEID = 32762
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PEnum(text='QTE\xe4\xba\x8b\xe4\xbb\xb6\xe7\xb1\xbb\xe5\x9e\x8b', default=0, enumType='custom32762Type_0')),
     (
      'param1', PStr(text='\xe5\x8f\x82\xe6\x95\xb0'))])


@TrackMeta
class Tcustom32763(TXMLCustomCue):
    CUEID = 32763
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PStr(text='\xe4\xba\x8b\xe4\xbb\xb6\xe5\x90\x8d\xe5\xad\x97')),
     (
      'param1', PStr(text='\xe5\x8f\x82\xe6\x95\xb0'))])


@TrackMeta
class Tcustom32761(TXMLCustomCue):
    CUEID = 32761
    FRAME_PROPERTIES = OrderedProperties([
     (
      'param0', PStr(text='\xe4\xba\x8b\xe4\xbb\xb6\xe5\x90\x8d\xe5\xad\x97'))])


GenCustomEntityTracks = [
 ('\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe5\x88\x9b\xe7\x94\x9f\xe6\xb3\x95\xe6\x9c\xaf\xe5\x9c\xba',
 'Tcustom6'),
 ('\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe8\xaf\xb7\xe6\xb1\x82\xe6\x9c\x8d\xe5\x8a\xa1\xe7\xab\xaf\xe5\x88\x9b\xe7\x94\x9f\xe6\xb3\x95\xe6\x9c\xaf\xe5\x9c\xba',
 'Tcustom7'),
 ('\xe5\x8f\x91\xe5\xb0\x84\xe5\xad\x90\xe5\xbc\xb9\xe7\x89\xb9\xe6\x95\x88', 'Tcustom17')]
GenCustomSceneTracks = [
 ('\xe6\x8c\x82\xe6\x8e\xa5\xe9\x9f\xb3\xe6\x95\x88\xe4\xba\x8b\xe4\xbb\xb6', 'Tcustom1'),
 ('\xe6\x8c\x82\xe6\x8e\xa5\xe7\x89\xb9\xe6\x95\x88', 'Tcustom2'),
 ('\xe6\x8a\x80\xe8\x83\xbd\xe8\xa7\xa6\xe5\x8f\x91\xe4\xba\x8b\xe4\xbb\xb6', 'Tcustom3'),
 ('\xe6\x8a\x80\xe8\x83\xbd\xe5\x87\xbb\xe4\xb8\xad\xe4\xba\x8b\xe4\xbb\xb6', 'Tcustom4'),
 ('\xe6\x8c\x82\xe6\x8e\xa5\xe9\x9f\xb3\xe6\x95\x88', 'Tcustom8'),
 ('\xe6\x8c\x82\xe6\x8e\xa5\xe5\xb8\xa6Switch\xe7\x9a\x84\xe9\x9f\xb3\xe6\x95\x88\xe4\xba\x8b\xe4\xbb\xb6',
 'Tcustom28'),
 ('\xe9\x9a\x90\xe8\x97\x8f\xe6\xa8\xa1\xe5\x9e\x8b\xe7\xbb\x84\xe4\xbb\xb6', 'Tcustom9'),
 ('\xe6\x8c\x82\xe6\x8e\xa5\xe8\xbf\x9e\xe6\x8e\xa5\xe7\x89\xb9\xe6\x95\x88', 'Tcustom11'),
 ('\xe9\x95\x9c\xe5\xa4\xb4\xe9\x9c\x87\xe5\x8a\xa8', 'Tcustom12'),
 ('\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x8f\x92\xe5\xb8\xa7', 'Tcustom13'),
 ('\xe9\x95\x9c\xe5\xa4\xb4\xe8\xb7\x9f\xe9\x9a\x8f', 'Tcustom14'),
 ('\xe8\xae\xbe\xe7\xbd\xae\xe6\xa8\xa1\xe5\x9e\x8b\xe5\x8f\xaf\xe8\xa7\x81\xe6\x80\xa7',
 'Tcustom15'),
 ('\xe5\xbc\xb9\xe5\x87\xba\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x9b\xbe', 'Tcustom16'),
 ('\xe5\xb1\x8f\xe5\xb9\x95\xe7\xa0\xb4\xe7\xa2\x8e\xe6\x95\x88\xe6\x9e\x9c', 'Tcustom18'),
 ('\xe9\x95\x9c\xe5\xa4\xb4Motor', 'Tcustom19'),
 ('\xe9\x95\x9c\xe5\xa4\xb4\xe6\xa8\xa1\xe7\xb3\x8a', 'Tcustom20'),
 ('\xe5\xb1\x8f\xe5\xb9\x95\xe6\x9f\x93\xe8\x89\xb2', 'Tcustom21'),
 ('\xe5\xbc\x80\xe5\x9c\xba\xe5\x8a\xa8\xe4\xbd\x9c', 'Tcustom22'),
 ('\xe7\x9b\xb8\xe6\x9c\xba\xe4\xbf\x9d\xe6\x8c\x81\xe7\x8e\xa9\xe5\xae\xb6\xe8\xba\xab\xe5\x90\x8e',
 'Tcustom23'),
 ('\xe7\x9b\xb8\xe6\x9c\xba\xe6\x8b\x89\xe5\x9b\x9e\xe6\xad\xa3\xe5\xb8\xb8\xe8\xa7\x86\xe8\xa7\x92',
 'Tcustom24'),
 ('Action\xe9\x80\x9f\xe7\x8e\x87\xe6\x94\xb9\xe5\x8f\x98', 'Tcustom43'),
 ('Action\xe9\x80\x9f\xe7\x8e\x87\xe7\xaa\x81\xe5\x8f\x98', 'Tcustom44'),
 ('\xe5\x88\x9b\xe5\xbb\xbaTarget Entity', 'Tcustom50'),
 ('\xe5\x88\xa0\xe9\x99\xa4Target Entity', 'Tcustom51'),
 ('\xe5\x88\xa0\xe9\x99\xa4\xe6\x89\x80\xe6\x9c\x89Target Entity', 'Tcustom52'),
 ('\xe7\x88\xac\xe5\xa2\x99\xe7\x8a\xb6\xe6\x80\x81\xe5\x8f\x98\xe5\x8c\x96', 'Tcustom60'),
 ('QTE\xe4\xba\x8b\xe4\xbb\xb6', 'Tcustom32762'),
 ('\xe9\x95\x9c\xe5\xa4\xb4\xe4\xba\x8b\xe4\xbb\xb6\xe4\xbf\xa1\xe5\x8f\xb7', 'Tcustom32763'),
 ('\xe4\xba\x8b\xe4\xbb\xb6\xe4\xbf\xa1\xe5\x8f\xb7', 'Tcustom32761')]