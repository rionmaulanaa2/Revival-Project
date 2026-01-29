# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/fight_proto.py
from __future__ import absolute_import
import six_ex
from logic.gcommon.common_utils.math3d_utils import v3d_to_tp, tp_to_v3d
from logic.gcommon.const import HIT_PART_HEAD, HIT_PART_BODY, HIT_PART_ARM, HIT_PART_OTHER
if G_IS_CLIENT:
    from logic.gutils.mecha_utils import check_mecha_hit, check_mecha_hit_shield
    from logic.gutils.monster_utils import check_monster_hit
    from logic.gutils.salog import SALog
    from logic.gutils.sound_utils import play_hit_sound_2d
from logic.gcommon.const import WEAKNESS_ATTACK_TAG, EXECUTE_HIT_HINT
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const.battle_const import FIGHT_INJ_SHOOT, FIGHT_INJ_BOMB, FIGHT_INJ_FALLING, FIGHT_INJ_CRASH, FIGHT_INJ_SKILL
import logic.gcommon.common_const.log_const as log_const
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.cdata import status_config

def change_at_aim_args(synchronizer, f_aim_x, f_aim_y, f_aim_r):
    synchronizer.send_event('E_SET_AT_AIM_ARGS', f_aim_x, f_aim_y, f_aim_r)


def set_atk_target(synchronizer, atk_target_id):
    if atk_target_id is not None:
        from mobile.common.EntityManager import EntityManager
        atk_target = EntityManager.getentity(atk_target_id)
        if atk_target and atk_target.logic:
            synchronizer.send_event('E_ATK_TARGET', atk_target.logic)
            return
    synchronizer.send_event('E_ATK_TARGET', None)
    return


def set_follow_target(synchronizer, target_id):
    synchronizer.send_event('E_FOLLOW_TARGET', target_id)


def check_attacker_visible(trigger, id_trigger, target, from_pos=None):
    if not target or not target.unit_obj:
        return
    else:
        if not global_data.player:
            return
        my_player = global_data.player.logic
        if not my_player:
            return
        if my_player.id != target.unit_obj.id:
            return
        target_id = str(target.unit_obj.id)
        if not global_data.player.can_send_general_log(target_id, log_const.LOG_KEY_INVISIBLE_PLAYER):
            return
        info = {}
        if trigger and trigger.logic:
            trigger_model = trigger.logic.ev_g_model()
            if trigger_model and trigger_model.visible:
                return
        if trigger and trigger.logic:
            trigger_class_name = trigger.logic.__class__.__name__
            if trigger_class_name == 'LAvatar':
                if trigger.logic.ev_g_get_state(status_config.ST_AIM):
                    return
                control_target = trigger.logic.ev_g_control_target()
                if control_target and control_target.logic and control_target.logic.__class__.__name__ in ('LMecha',
                                                                                                           'LMechaTrans'):
                    if control_target.logic.sd.ref_in_open_aim:
                        return
                    mecha_model = control_target.logic.ev_g_model()
                    if mecha_model and mecha_model.visible:
                        return
            elif trigger_class_name == 'LPuppet':
                control_target = trigger.logic.ev_g_control_target()
                if control_target and control_target.logic and control_target.logic.__class__.__name__ in ('LMecha',
                                                                                                           'LMechaTrans'):
                    mecha_model = control_target.logic.ev_g_model()
                    if mecha_model and mecha_model.visible:
                        return
            elif trigger_class_name == 'LPuppetRobot':
                mecha = trigger.logic.ev_g_bind_mecha_entity()
                if mecha and mecha.logic and not mecha.logic.ev_g_death():
                    model = mecha.logic.ev_g_model()
                    if model and model.visible:
                        return
                else:
                    model = trigger.logic.ev_g_model()
                    if model and model.visible:
                        return
        info['target_id'] = target_id
        target_pos = target.ev_g_position()
        target_pos = [target_pos.x, target_pos.y, target_pos.z]
        info['target_pos'] = target_pos
        info['attacker_id'] = str(id_trigger)
        attacker_pos = None
        if trigger and trigger.logic:
            attacker_pos = trigger.logic.ev_g_position()
            info['target_valid'] = True
            mecha = trigger.logic.ev_g_bind_mecha_entity()
            info['has_bind_mecha'] = True if mecha and mecha.logic and not mecha.logic.ev_g_death() else False
            info['is_death'] = True if trigger.logic.ev_g_death() else False
        elif from_pos:
            attacker_pos = from_pos
            info['target_valid'] = False
        if attacker_pos:
            attacker_pos = [
             attacker_pos.x, attacker_pos.y, attacker_pos.z]
            info['attacker_pos'] = attacker_pos
        global_data.player.upload_general_log(target_id, log_const.LOG_KEY_INVISIBLE_PLAYER, info)
        return


def show_hurt_dir(trigger, target, damage=0, parts=(), from_pos=None, id_trigger=None):
    if not trigger or not trigger.logic:
        check_attacker_visible(trigger, id_trigger, target, from_pos=from_pos)
        return
    else:
        if from_pos is None:
            from_pos = trigger.logic.ev_g_position()
        if not from_pos:
            return
        is_mecha = True if trigger.logic.ev_g_in_mecha() else False
        is_monster = True if trigger.logic.is_monster() else False
        check_attacker_visible(trigger, id_trigger, target, from_pos=from_pos)
        target.send_event('E_HITED_SHOW_HURT_DIR', trigger, from_pos, damage=damage, is_mecha=is_mecha or is_monster)
        return


def check_enter_battle_state(trigger, target):
    if trigger and trigger.logic and (target.is_unit_obj_type('LMecha') or target.is_unit_obj_type('LMechaTrans') or target.unit_obj.ev_g_in_mecha()):
        global_data.emgr.scene_check_enter_battle_state.emit(trigger)
    if trigger and trigger.logic:
        if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_campmate(trigger.logic.ev_g_camp_id()):
            target.send_event('E_SHOW_HIT_MARK')
            global_data.emgr.campmate_make_damage_event.emit(target)
        if trigger.logic.ev_g_is_cam_target():
            if global_data.cam_lplayer:
                global_data.cam_lplayer.send_event('E_ON_HIT_OTHER')


def on_hit_miss(synchronizer, weapon_type, id_trigger, text_id=17019):
    if id_trigger == global_data.player.id or global_data.cam_lplayer and global_data.cam_lplayer.id == id_trigger:
        global_data.emgr.target_invincible_event.emit(synchronizer.unit_obj, weapon_type, text_id)


def on_hit_pve_reaction(synchronizer, id_trigger, reaction_key):
    global_data.emgr.pve_element_reaction_event.emit(synchronizer.unit_obj, reaction_key)


def on_hit_judge(synchronizer, id_trigger, damage):
    if not id_trigger:
        return
    triger = EntityManager.getentity(id_trigger)
    if not triger or not triger.logic:
        return
    triger_is_mecha = True if triger.logic.ev_g_in_mecha() else False
    if triger_is_mecha:
        control_target = triger.logic.ev_g_control_target()
        if control_target and control_target.logic:
            control_target.logic.send_event('E_HIT_OTHER', synchronizer.unit_obj, damage)
    else:
        triger.logic.send_event('E_HIT_OTHER', synchronizer.unit_obj, damage)


def on_hit_shoot--- This code section failed: ---

 192       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('HIT_PART_HEAD',)
           6  IMPORT_NAME           0  'logic.gcommon.const'
           9  IMPORT_FROM           1  'HIT_PART_HEAD'
          12  STORE_FAST            8  'HIT_PART_HEAD'
          15  POP_TOP          

 193      16  LOAD_CONST            1  ''
          19  LOAD_CONST            3  ('EntityManager',)
          22  IMPORT_NAME           2  'mobile.common.EntityManager'
          25  IMPORT_FROM           3  'EntityManager'
          28  STORE_FAST            9  'EntityManager'
          31  POP_TOP          

 194      32  LOAD_CONST            1  ''
          35  LOAD_CONST            4  ('LPuppet',)
          38  IMPORT_NAME           4  'logic.units.LPuppet'
          41  IMPORT_FROM           5  'LPuppet'
          44  STORE_FAST           10  'LPuppet'
          47  POP_TOP          

 195      48  LOAD_CONST            1  ''
          51  LOAD_CONST            5  ('LPuppetRobot',)
          54  IMPORT_NAME           6  'logic.units.LPuppetRobot'
          57  IMPORT_FROM           7  'LPuppetRobot'
          60  STORE_FAST           11  'LPuppetRobot'
          63  POP_TOP          

 197      64  LOAD_GLOBAL           8  'tp_to_v3d'
          67  LOAD_FAST             4  'lst_target'
          70  CALL_FUNCTION_1       1 
          73  STORE_FAST           12  'target_pos'

 198      76  LOAD_GLOBAL           8  'tp_to_v3d'
          79  LOAD_FAST             5  'lst_from'
          82  CALL_FUNCTION_1       1 
          85  STORE_FAST           13  'from_pos'

 200      88  LOAD_GLOBAL           9  'False'
          91  STORE_FAST           14  'is_robot'

 201      94  LOAD_CONST            0  ''
          97  STORE_FAST           15  'triger'

 202     100  LOAD_GLOBAL           9  'False'
         103  STORE_FAST           16  'triger_is_mecha'

 203     106  LOAD_CONST            1  ''
         109  STORE_FAST           17  'hit_sfx_code'

 204     112  LOAD_FAST             7  'ext_dict'
         115  POP_JUMP_IF_FALSE   139  'to 139'

 205     118  LOAD_FAST             7  'ext_dict'
         121  LOAD_ATTR            11  'get'
         124  LOAD_CONST            6  'hit_sfx_code'
         127  LOAD_CONST            1  ''
         130  CALL_FUNCTION_2       2 
         133  STORE_FAST           17  'hit_sfx_code'
         136  JUMP_FORWARD          0  'to 139'
       139_0  COME_FROM                '136'

 207     139  LOAD_FAST             6  'id_trigger'
         142  POP_JUMP_IF_FALSE   238  'to 238'

 208     145  LOAD_FAST             9  'EntityManager'
         148  LOAD_ATTR            12  'getentity'
         151  LOAD_FAST             6  'id_trigger'
         154  CALL_FUNCTION_1       1 
         157  STORE_FAST           15  'triger'

 209     160  LOAD_FAST            15  'triger'
         163  POP_JUMP_IF_FALSE   229  'to 229'
         166  LOAD_FAST            15  'triger'
         169  LOAD_ATTR            13  'logic'
       172_0  COME_FROM                '163'
         172  POP_JUMP_IF_FALSE   229  'to 229'

 210     175  LOAD_FAST            15  'triger'
         178  LOAD_ATTR            13  'logic'
         181  LOAD_ATTR            14  'ev_g_in_mecha'
         184  CALL_FUNCTION_0       0 
         187  POP_JUMP_IF_FALSE   196  'to 196'
         190  LOAD_GLOBAL          15  'True'
         193  JUMP_FORWARD          3  'to 199'
         196  LOAD_GLOBAL           9  'False'
       199_0  COME_FROM                '193'
         199  STORE_FAST           16  'triger_is_mecha'

 211     202  LOAD_FAST            16  'triger_is_mecha'
         205  POP_JUMP_IF_FALSE   211  'to 211'

 212     208  JUMP_ABSOLUTE       235  'to 235'

 215     211  LOAD_FAST            15  'triger'
         214  LOAD_ATTR            13  'logic'
         217  LOAD_ATTR            16  'sd'
         220  LOAD_ATTR            17  'ref_is_robot'
         223  STORE_FAST           14  'is_robot'
         226  JUMP_ABSOLUTE       238  'to 238'

 217     229  LOAD_CONST            0  ''
         232  STORE_FAST           15  'triger'
         235  JUMP_FORWARD          0  'to 238'
       238_0  COME_FROM                '235'

 219     238  LOAD_GLOBAL          18  'check_enter_battle_state'
         241  LOAD_FAST            15  'triger'
         244  LOAD_FAST             0  'synchronizer'
         247  CALL_FUNCTION_2       2 
         250  POP_TOP          

 220     251  LOAD_FAST             2  'dmg_parts'
         254  POP_JUMP_IF_TRUE    263  'to 263'
         257  LOAD_FAST             3  'shield_damage'
         260  JUMP_FORWARD         20  'to 283'
         263  LOAD_GLOBAL          19  'six_ex'
         266  LOAD_ATTR            20  'values'
         269  LOAD_FAST             2  'dmg_parts'
         272  CALL_FUNCTION_1       1 
         275  LOAD_CONST            1  ''
         278  BINARY_SUBSCR    
         279  LOAD_CONST            7  1
         282  BINARY_SUBSCR    
       283_0  COME_FROM                '260'
         283  STORE_FAST           18  'damage'

 222     286  LOAD_GLOBAL          21  'show_hurt_dir'
         289  LOAD_FAST            15  'triger'
         292  LOAD_FAST             8  'HIT_PART_HEAD'
         295  LOAD_FAST            18  'damage'
         298  LOAD_CONST            9  'from_pos'
         301  LOAD_FAST            13  'from_pos'
         304  LOAD_CONST           10  'id_trigger'
         307  LOAD_FAST             6  'id_trigger'
         310  CALL_FUNCTION_770   770 
         313  POP_TOP          

 224     314  LOAD_FAST             0  'synchronizer'
         317  LOAD_ATTR            22  'send_event'
         320  LOAD_CONST           11  'E_HITED_SHOW_HURT_FIREARMS_SCREEN_TRK'
         323  LOAD_FAST            13  'from_pos'
         326  LOAD_GLOBAL          19  'six_ex'
         329  LOAD_ATTR            23  'keys'
         332  LOAD_FAST             2  'dmg_parts'
         335  CALL_FUNCTION_1       1 
         338  LOAD_FAST             1  'shot_type'
         341  LOAD_FAST            16  'triger_is_mecha'
         344  CALL_FUNCTION_5       5 
         347  POP_TOP          

 225     348  LOAD_FAST             0  'synchronizer'
         351  LOAD_ATTR            24  '_is_avatar'
         354  POP_JUMP_IF_TRUE    373  'to 373'

 226     357  LOAD_FAST             0  'synchronizer'
         360  LOAD_ATTR            22  'send_event'
         363  LOAD_CONST           12  'E_HITED'
         366  CALL_FUNCTION_1       1 
         369  POP_TOP          
         370  JUMP_FORWARD          0  'to 373'
       373_0  COME_FROM                '370'

 228     373  LOAD_FAST             0  'synchronizer'
         376  LOAD_ATTR            22  'send_event'
         379  LOAD_CONST           13  'E_SHOW_SCREEN_HURT_SFX'
         382  LOAD_GLOBAL          25  'FIGHT_INJ_SHOOT'
         385  LOAD_FAST            18  'damage'
         388  LOAD_FAST            13  'from_pos'
         391  LOAD_FAST             1  'shot_type'
         394  LOAD_FAST             2  'dmg_parts'
         397  LOAD_FAST            16  'triger_is_mecha'
         400  CALL_FUNCTION_7       7 
         403  POP_TOP          

 229     404  LOAD_FAST             0  'synchronizer'
         407  LOAD_ATTR            22  'send_event'
         410  LOAD_CONST           14  'E_RECORD_ON_HIT_INFO'
         413  LOAD_FAST             6  'id_trigger'
         416  LOAD_FAST             1  'shot_type'
         419  LOAD_CONST            0  ''
         422  CALL_FUNCTION_4       4 
         425  POP_TOP          

 231     426  LOAD_GLOBAL          26  'global_data'
         429  LOAD_ATTR            27  'player'
         432  POP_JUMP_IF_FALSE   453  'to 453'
         435  LOAD_FAST             6  'id_trigger'
         438  LOAD_GLOBAL          26  'global_data'
         441  LOAD_ATTR            27  'player'
         444  LOAD_ATTR            28  'id'
         447  COMPARE_OP            2  '=='
       450_0  COME_FROM                '432'
         450  POP_JUMP_IF_TRUE    480  'to 480'
         453  LOAD_GLOBAL          26  'global_data'
         456  LOAD_ATTR            29  'cam_lplayer'
         459  POP_JUMP_IF_FALSE   888  'to 888'
         462  LOAD_GLOBAL          26  'global_data'
         465  LOAD_ATTR            29  'cam_lplayer'
         468  LOAD_ATTR            28  'id'
         471  LOAD_FAST             6  'id_trigger'
         474  COMPARE_OP            2  '=='
       477_0  COME_FROM                '459'
       477_1  COME_FROM                '450'
         477  POP_JUMP_IF_FALSE   888  'to 888'

 233     480  LOAD_GLOBAL          30  'isinstance'
         483  LOAD_FAST             7  'ext_dict'
         486  LOAD_GLOBAL          31  'dict'
         489  CALL_FUNCTION_2       2 
         492  POP_JUMP_IF_FALSE   513  'to 513'
         495  LOAD_FAST             7  'ext_dict'
         498  LOAD_ATTR            11  'get'
         501  LOAD_CONST           15  'hit_carry_shield'
         504  LOAD_GLOBAL           9  'False'
         507  CALL_FUNCTION_2       2 
         510  JUMP_FORWARD          3  'to 516'
         513  LOAD_GLOBAL           9  'False'
       516_0  COME_FROM                '510'
         516  STORE_FAST           19  'hit_carry_shield'

 234     519  LOAD_FAST             7  'ext_dict'
         522  POP_JUMP_IF_FALSE   543  'to 543'
         525  LOAD_FAST             7  'ext_dict'
         528  LOAD_ATTR            11  'get'
         531  LOAD_GLOBAL          32  'WEAKNESS_ATTACK_TAG'
         534  LOAD_CONST            1  ''
         537  CALL_FUNCTION_2       2 
         540  JUMP_FORWARD          3  'to 546'
         543  LOAD_CONST            1  ''
       546_0  COME_FROM                '540'
         546  STORE_FAST           20  '_weakness_tag'

 235     549  LOAD_GLOBAL          26  'global_data'
         552  LOAD_ATTR            33  'emgr'
         555  LOAD_ATTR            34  'player_make_damage_event'
         558  LOAD_ATTR            35  'emit'

 236     561  LOAD_FAST             0  'synchronizer'
         564  LOAD_ATTR            36  'unit_obj'
         567  LOAD_FAST             2  'dmg_parts'
         570  LOAD_FAST             3  'shield_damage'
         573  LOAD_FAST             1  'shot_type'

 237     576  BUILD_MAP_3           3 
         579  LOAD_FAST            12  'target_pos'
         582  LOAD_CONST           16  'target_pos'
         585  STORE_MAP        
         586  LOAD_FAST            19  'hit_carry_shield'
         589  LOAD_CONST           15  'hit_carry_shield'
         592  STORE_MAP        
         593  LOAD_FAST            20  '_weakness_tag'
         596  LOAD_GLOBAL          32  'WEAKNESS_ATTACK_TAG'
         599  STORE_MAP        
         600  CALL_FUNCTION_5       5 
         603  POP_TOP          

 239     604  LOAD_FAST             0  'synchronizer'
         607  LOAD_ATTR            22  'send_event'
         610  LOAD_CONST           17  'E_SHOW_HP_OVER_HEAD'
         613  CALL_FUNCTION_1       1 
         616  POP_TOP          

 240     617  LOAD_GLOBAL          26  'global_data'
         620  LOAD_ATTR            37  'cam_lctarget'
         623  POP_JUMP_IF_FALSE   648  'to 648'

 241     626  LOAD_GLOBAL          26  'global_data'
         629  LOAD_ATTR            37  'cam_lctarget'
         632  LOAD_ATTR            22  'send_event'
         635  LOAD_CONST           18  'E_HIT_TARGET'
         638  LOAD_FAST             2  'dmg_parts'
         641  CALL_FUNCTION_2       2 
         644  POP_TOP          
         645  JUMP_FORWARD          0  'to 648'
       648_0  COME_FROM                '645'

 243     648  LOAD_FAST             0  'synchronizer'
         651  LOAD_ATTR            36  'unit_obj'
         654  LOAD_ATTR            16  'sd'
         657  LOAD_ATTR            38  'ref_is_mecha'
         660  STORE_FAST           21  'is_mecha'

 244     663  LOAD_FAST             8  'HIT_PART_HEAD'
         666  LOAD_FAST             2  'dmg_parts'
         669  COMPARE_OP            6  'in'
         672  STORE_FAST           22  'is_head'

 245     675  LOAD_FAST            22  'is_head'
         678  POP_JUMP_IF_FALSE   776  'to 776'

 246     681  LOAD_GLOBAL          30  'isinstance'
         684  LOAD_FAST             0  'synchronizer'
         687  LOAD_ATTR            36  'unit_obj'
         690  LOAD_FAST            10  'LPuppet'
         693  CALL_FUNCTION_2       2 
         696  POP_JUMP_IF_TRUE    717  'to 717'
         699  LOAD_GLOBAL          30  'isinstance'
         702  LOAD_FAST             0  'synchronizer'
         705  LOAD_ATTR            36  'unit_obj'
         708  LOAD_FAST            11  'LPuppetRobot'
         711  CALL_FUNCTION_2       2 
       714_0  COME_FROM                '696'
         714  POP_JUMP_IF_FALSE   742  'to 742'

 248     717  LOAD_GLOBAL          26  'global_data'
         720  LOAD_ATTR            33  'emgr'
         723  LOAD_ATTR            39  'play_atk_voice'
         726  LOAD_ATTR            35  'emit'
         729  LOAD_CONST           19  'hit_head'
         732  LOAD_FAST             1  'shot_type'
         735  CALL_FUNCTION_2       2 
         738  POP_TOP          
         739  JUMP_ABSOLUTE       868  'to 868'

 249     742  LOAD_FAST            21  'is_mecha'
         745  POP_JUMP_IF_FALSE   868  'to 868'

 250     748  LOAD_GLOBAL          26  'global_data'
         751  LOAD_ATTR            33  'emgr'
         754  LOAD_ATTR            39  'play_atk_voice'
         757  LOAD_ATTR            35  'emit'
         760  LOAD_CONST           20  'hit_mecha_head'
         763  LOAD_FAST             1  'shot_type'
         766  CALL_FUNCTION_2       2 
         769  POP_TOP          
         770  JUMP_ABSOLUTE       868  'to 868'
         773  JUMP_FORWARD         92  'to 868'

 252     776  LOAD_GLOBAL          30  'isinstance'
         779  LOAD_FAST             0  'synchronizer'
         782  LOAD_ATTR            36  'unit_obj'
         785  LOAD_FAST            10  'LPuppet'
         788  CALL_FUNCTION_2       2 
         791  POP_JUMP_IF_TRUE    812  'to 812'
         794  LOAD_GLOBAL          30  'isinstance'
         797  LOAD_FAST             0  'synchronizer'
         800  LOAD_ATTR            36  'unit_obj'
         803  LOAD_FAST            11  'LPuppetRobot'
         806  CALL_FUNCTION_2       2 
       809_0  COME_FROM                '791'
         809  POP_JUMP_IF_FALSE   837  'to 837'

 253     812  LOAD_GLOBAL          26  'global_data'
         815  LOAD_ATTR            33  'emgr'
         818  LOAD_ATTR            39  'play_atk_voice'
         821  LOAD_ATTR            35  'emit'
         824  LOAD_CONST           21  'hit_body'
         827  LOAD_FAST             1  'shot_type'
         830  CALL_FUNCTION_2       2 
         833  POP_TOP          
         834  JUMP_FORWARD         31  'to 868'

 254     837  LOAD_FAST            21  'is_mecha'
         840  POP_JUMP_IF_FALSE   868  'to 868'

 255     843  LOAD_GLOBAL          26  'global_data'
         846  LOAD_ATTR            33  'emgr'
         849  LOAD_ATTR            39  'play_atk_voice'
         852  LOAD_ATTR            35  'emit'
         855  LOAD_CONST           22  'hit_mecha_body'
         858  LOAD_FAST             1  'shot_type'
         861  CALL_FUNCTION_2       2 
         864  POP_TOP          
         865  JUMP_FORWARD          0  'to 868'
       868_0  COME_FROM                '865'
       868_1  COME_FROM                '834'
       868_2  COME_FROM                '773'

 256     868  LOAD_GLOBAL          40  'play_hit_sound_2d'
         871  LOAD_FAST             1  'shot_type'
         874  LOAD_FAST            21  'is_mecha'
         877  UNARY_NOT        
         878  LOAD_FAST            22  'is_head'
         881  CALL_FUNCTION_3       3 
         884  POP_TOP          
         885  JUMP_FORWARD        277  'to 1165'

 258     888  LOAD_FAST            14  'is_robot'
         891  POP_JUMP_IF_FALSE   998  'to 998'
         894  LOAD_FAST            15  'triger'
       897_0  COME_FROM                '891'
         897  POP_JUMP_IF_FALSE   998  'to 998'

 259     900  LOAD_FAST             0  'synchronizer'
         903  LOAD_ATTR            41  'ev_g_ai_can_atk_type'
         906  CALL_FUNCTION_0       0 
         909  STORE_FAST           23  'can_atk_type'

 260     912  LOAD_FAST            23  'can_atk_type'
         915  LOAD_CONST            0  ''
         918  COMPARE_OP            9  'is-not'
         921  POP_JUMP_IF_FALSE   970  'to 970'
         924  LOAD_FAST            23  'can_atk_type'
         927  LOAD_CONST            1  ''
         930  COMPARE_OP            4  '>'
       933_0  COME_FROM                '921'
         933  POP_JUMP_IF_FALSE   970  'to 970'

 261     936  LOAD_FAST            15  'triger'
         939  LOAD_ATTR            13  'logic'
         942  LOAD_ATTR            22  'send_event'
         945  LOAD_CONST           23  'E_CHECK_ATK_POS_CROSS'
         948  LOAD_FAST            13  'from_pos'
         951  LOAD_FAST            12  'target_pos'
         954  LOAD_FAST             0  'synchronizer'
         957  LOAD_ATTR            36  'unit_obj'
         960  LOAD_ATTR            28  'id'
         963  CALL_FUNCTION_4       4 
         966  POP_TOP          
         967  JUMP_ABSOLUTE      1165  'to 1165'

 263     970  LOAD_FAST            15  'triger'
         973  LOAD_ATTR            13  'logic'
         976  LOAD_ATTR            22  'send_event'
         979  LOAD_CONST           24  'E_CHECK_ATK_POS'
         982  LOAD_FAST            13  'from_pos'
         985  LOAD_GLOBAL          15  'True'
         988  LOAD_FAST             2  'dmg_parts'
         991  CALL_FUNCTION_4       4 
         994  POP_TOP          
         995  JUMP_FORWARD        167  'to 1165'

 265     998  BUILD_MAP_0           0 
        1001  STORE_FAST           24  'kwargs'

 267    1004  BUILD_MAP_1           1 
        1007  LOAD_FAST            17  'hit_sfx_code'
        1010  LOAD_CONST            6  'hit_sfx_code'
        1013  STORE_MAP        
        1014  LOAD_FAST            24  'kwargs'
        1017  LOAD_CONST           25  'ext_dict'
        1020  STORE_SUBSCR     

 268    1021  LOAD_FAST            15  'triger'
        1024  POP_JUMP_IF_FALSE  1053  'to 1053'

 269    1027  LOAD_FAST            15  'triger'
        1030  LOAD_ATTR            13  'logic'
        1033  LOAD_ATTR            42  'ev_g_camp_id'
        1036  CALL_FUNCTION_0       0 
        1039  LOAD_FAST            24  'kwargs'
        1042  LOAD_CONST           25  'ext_dict'
        1045  BINARY_SUBSCR    
        1046  LOAD_CONST           26  'trigger_camp_id'
        1049  STORE_SUBSCR     
        1050  JUMP_FORWARD          0  'to 1053'
      1053_0  COME_FROM                '1050'

 272    1053  LOAD_FAST             0  'synchronizer'
        1056  LOAD_ATTR            22  'send_event'
        1059  LOAD_CONST           27  'E_HIT_BLOOD_SFX'
        1062  LOAD_FAST            13  'from_pos'
        1065  LOAD_FAST            12  'target_pos'
        1068  LOAD_FAST             1  'shot_type'
        1071  LOAD_CONST           28  'is_self'
        1074  LOAD_FAST             0  'synchronizer'
        1077  LOAD_ATTR            24  '_is_avatar'
        1080  LOAD_CONST           29  'dmg_parts'
        1083  LOAD_FAST             2  'dmg_parts'
        1086  LOAD_CONST           30  'triger_is_mecha'

 273    1089  LOAD_FAST            16  'triger_is_mecha'
        1092  LOAD_FAST            24  'kwargs'
        1095  CALL_FUNCTION_KW_772   772 
        1098  POP_TOP          

 275    1099  LOAD_FAST             0  'synchronizer'
        1102  LOAD_ATTR            22  'send_event'
        1105  LOAD_CONST           31  'E_HIT_SHIELD_SFX'
        1108  LOAD_FAST            13  'from_pos'
        1111  LOAD_FAST            12  'target_pos'
        1114  LOAD_FAST             1  'shot_type'
        1117  CALL_FUNCTION_4       4 
        1120  POP_TOP          

 276    1121  LOAD_FAST             0  'synchronizer'
        1124  LOAD_ATTR            22  'send_event'
        1127  LOAD_CONST           32  'E_HIT_FIELD_SHIELD'
        1130  LOAD_FAST            13  'from_pos'
        1133  LOAD_FAST            12  'target_pos'
        1136  CALL_FUNCTION_3       3 
        1139  POP_TOP          

 277    1140  LOAD_FAST             0  'synchronizer'
        1143  LOAD_ATTR            22  'send_event'
        1146  LOAD_CONST           33  'E_SHOW_PART_HIGHLIGHT'
        1149  LOAD_GLOBAL          19  'six_ex'
        1152  LOAD_ATTR            23  'keys'
        1155  LOAD_FAST             2  'dmg_parts'
        1158  CALL_FUNCTION_1       1 
        1161  CALL_FUNCTION_2       2 
        1164  POP_TOP          
      1165_0  COME_FROM                '995'
      1165_1  COME_FROM                '885'

 279    1165  LOAD_FAST             3  'shield_damage'
        1168  STORE_FAST           25  'total_damage'

 280    1171  LOAD_FAST             2  'dmg_parts'
        1174  POP_JUMP_IF_FALSE  1207  'to 1207'

 281    1177  LOAD_FAST            25  'total_damage'
        1180  LOAD_GLOBAL          19  'six_ex'
        1183  LOAD_ATTR            20  'values'
        1186  LOAD_FAST             2  'dmg_parts'
        1189  CALL_FUNCTION_1       1 
        1192  LOAD_CONST            1  ''
        1195  BINARY_SUBSCR    
        1196  LOAD_CONST            7  1
        1199  BINARY_SUBSCR    
        1200  INPLACE_ADD      
        1201  STORE_FAST           25  'total_damage'
        1204  JUMP_FORWARD          0  'to 1207'
      1207_0  COME_FROM                '1204'

 282    1207  LOAD_GLOBAL          43  'on_hit_judge'
        1210  LOAD_FAST             0  'synchronizer'
        1213  LOAD_FAST             6  'id_trigger'
        1216  LOAD_FAST            25  'total_damage'
        1219  CALL_FUNCTION_3       3 
        1222  POP_TOP          

 283    1223  LOAD_FAST             0  'synchronizer'
        1226  LOAD_ATTR            22  'send_event'
        1229  LOAD_CONST           34  'E_ON_HIT'
        1232  CALL_FUNCTION_1       1 
        1235  POP_TOP          

 284    1236  LOAD_FAST             0  'synchronizer'
        1239  LOAD_ATTR            22  'send_event'
        1242  LOAD_CONST           35  'E_ON_HIT_POINT_INFO'
        1245  LOAD_FAST            13  'from_pos'
        1248  LOAD_FAST            12  'target_pos'
        1251  LOAD_FAST            18  'damage'
        1254  CALL_FUNCTION_4       4 
        1257  POP_TOP          

 286    1258  LOAD_GLOBAL          44  'check_monster_hit'
        1261  LOAD_FAST             0  'synchronizer'
        1264  LOAD_ATTR            36  'unit_obj'
        1267  LOAD_ATTR            28  'id'
        1270  LOAD_FAST             6  'id_trigger'
        1273  CALL_FUNCTION_2       2 
        1276  POP_TOP          
        1277  LOAD_CONST            0  ''
        1280  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_770' instruction at offset 310


def on_hit_poison(synchronizer, damage):
    synchronizer.send_event('E_FIGHT_POISON_HURT', damage)


def on_hit_buff(synchronizer, buff_id, damage, shield_damage, id_trigger, extra_dict=None):
    trigger_is_self = False
    if extra_dict is None:
        extra_dict = {}
    if id_trigger == global_data.player.id or global_data.cam_lplayer and global_data.cam_lplayer.id == id_trigger:
        trigger_is_self = True
        hit_part = HIT_PART_HEAD if extra_dict.get(EXECUTE_HIT_HINT) else -1
        global_data.emgr.player_make_damage_event.emit(synchronizer.unit_obj, {hit_part: [1, damage]}, shield_damage, buff_id, extra_dict)
        synchronizer.send_event('E_SHOW_HP_OVER_HEAD')
    else:
        synchronizer.send_event('E_ON_HIT')
    synchronizer.send_event('E_HIT_BUFF_SOUND', buff_id, trigger_is_self)
    synchronizer.send_event('E_BUFF_HIT_SFX', buff_id)
    check_monster_hit(synchronizer.unit_obj.id, id_trigger)
    total_damage = shield_damage + damage
    on_hit_judge(synchronizer, id_trigger, total_damage)
    return


def on_hit_bomb--- This code section failed: ---

 322       0  LOAD_FAST             0  'synchronizer'
           3  LOAD_ATTR             0  'is_valid'
           6  CALL_FUNCTION_0       0 
           9  POP_JUMP_IF_TRUE     16  'to 16'

 323      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 325      16  LOAD_CONST            1  ''
          19  LOAD_CONST            0  ''
          22  IMPORT_NAME           1  'math3d'
          25  STORE_FAST            8  'math3d'

 326      28  LOAD_FAST             0  'synchronizer'
          31  LOAD_ATTR             2  'send_event'
          34  LOAD_CONST            2  'E_HITED'
          37  CALL_FUNCTION_1       1 
          40  POP_TOP          

 328      41  LOAD_GLOBAL           3  'global_data'
          44  LOAD_ATTR             4  'player'
          47  POP_JUMP_IF_TRUE     54  'to 54'

 329      50  LOAD_CONST            0  ''
          53  RETURN_END_IF    
        54_0  COME_FROM                '47'

 330      54  LOAD_FAST             4  'id_trigger'
          57  LOAD_GLOBAL           3  'global_data'
          60  LOAD_ATTR             4  'player'
          63  LOAD_ATTR             5  'id'
          66  COMPARE_OP            2  '=='
          69  POP_JUMP_IF_TRUE     99  'to 99'
          72  LOAD_GLOBAL           3  'global_data'
          75  LOAD_ATTR             6  'cam_lplayer'
          78  POP_JUMP_IF_FALSE   577  'to 577'
          81  LOAD_GLOBAL           3  'global_data'
          84  LOAD_ATTR             6  'cam_lplayer'
          87  LOAD_ATTR             5  'id'
          90  LOAD_FAST             4  'id_trigger'
          93  COMPARE_OP            2  '=='
        96_0  COME_FROM                '78'
        96_1  COME_FROM                '69'
          96  POP_JUMP_IF_FALSE   577  'to 577'

 331      99  LOAD_CONST            3  -1
         102  STORE_FAST            9  'part'

 332     105  LOAD_FAST             6  'parts'
         108  POP_JUMP_IF_FALSE   133  'to 133'

 333     111  LOAD_GLOBAL           7  'six_ex'
         114  LOAD_ATTR             8  'keys'
         117  LOAD_FAST             6  'parts'
         120  CALL_FUNCTION_1       1 
         123  LOAD_CONST            1  ''
         126  BINARY_SUBSCR    
         127  STORE_FAST            9  'part'
         130  JUMP_FORWARD          0  'to 133'
       133_0  COME_FROM                '130'

 335     133  LOAD_FAST             8  'math3d'
         136  LOAD_ATTR             9  'vector'
         139  LOAD_FAST             5  'tp3_pos'
         142  CALL_FUNCTION_VAR_0     0 
         145  STORE_FAST           10  'target_pos'

 336     148  LOAD_FAST             7  'extra_dict'
         151  JUMP_IF_TRUE_OR_POP   157  'to 157'
         154  BUILD_MAP_0           0 
       157_0  COME_FROM                '151'
         157  STORE_FAST            7  'extra_dict'

 337     160  LOAD_FAST            10  'target_pos'
         163  LOAD_FAST             7  'extra_dict'
         166  LOAD_CONST            4  'target_pos'
         169  STORE_SUBSCR     

 338     170  LOAD_FAST             7  'extra_dict'
         173  LOAD_ATTR            10  'get'
         176  LOAD_GLOBAL          11  'EXECUTE_HIT_HINT'
         179  CALL_FUNCTION_1       1 
         182  POP_JUMP_IF_FALSE   191  'to 191'
         185  LOAD_GLOBAL          12  'HIT_PART_HEAD'
         188  JUMP_FORWARD          3  'to 194'
         191  LOAD_FAST             9  'part'
       194_0  COME_FROM                '188'
         194  STORE_FAST            9  'part'

 339     197  LOAD_GLOBAL           3  'global_data'
         200  LOAD_ATTR            13  'emgr'
         203  LOAD_ATTR            14  'player_make_damage_event'
         206  LOAD_ATTR            15  'emit'
         209  LOAD_FAST             0  'synchronizer'
         212  LOAD_ATTR            16  'unit_obj'
         215  BUILD_MAP_1           1 
         218  LOAD_CONST            5  1
         221  LOAD_FAST             2  'damage'
         224  BUILD_LIST_2          2 
         227  LOAD_FAST             9  'part'
         230  STORE_MAP        
         231  LOAD_FAST             3  'shield_damage'
         234  LOAD_FAST             1  'bomb_id'
         237  LOAD_FAST             7  'extra_dict'
         240  CALL_FUNCTION_5       5 
         243  POP_TOP          

 340     244  LOAD_FAST             0  'synchronizer'
         247  LOAD_ATTR             2  'send_event'
         250  LOAD_CONST            6  'E_SHOW_HP_OVER_HEAD'
         253  CALL_FUNCTION_1       1 
         256  POP_TOP          

 341     257  LOAD_GLOBAL           3  'global_data'
         260  LOAD_ATTR            17  'cam_lctarget'
         263  POP_JUMP_IF_FALSE   300  'to 300'

 342     266  LOAD_GLOBAL           3  'global_data'
         269  LOAD_ATTR            17  'cam_lctarget'
         272  LOAD_ATTR             2  'send_event'
         275  LOAD_CONST            7  'E_HIT_TARGET'
         278  LOAD_FAST             6  'parts'
         281  POP_JUMP_IF_FALSE   290  'to 290'
         284  LOAD_FAST             6  'parts'
         287  JUMP_FORWARD          3  'to 293'
         290  BUILD_MAP_0           0 
       293_0  COME_FROM                '287'
         293  CALL_FUNCTION_2       2 
         296  POP_TOP          
         297  JUMP_FORWARD          0  'to 300'
       300_0  COME_FROM                '297'

 343     300  LOAD_FAST             0  'synchronizer'
         303  LOAD_ATTR             2  'send_event'
         306  LOAD_CONST            8  'E_HIT_BOMB_SOUND'
         309  LOAD_FAST            10  'target_pos'
         312  LOAD_FAST             1  'bomb_id'
         315  LOAD_GLOBAL          18  'True'
         318  LOAD_FAST             6  'parts'
         321  CALL_FUNCTION_5       5 
         324  POP_TOP          

 346     325  LOAD_CONST            1  ''
         328  LOAD_CONST            9  ('LPuppet',)
         331  IMPORT_NAME          19  'logic.units.LPuppet'
         334  IMPORT_FROM          20  'LPuppet'
         337  STORE_FAST           11  'LPuppet'
         340  POP_TOP          

 347     341  LOAD_CONST            1  ''
         344  LOAD_CONST           10  ('LPuppetRobot',)
         347  IMPORT_NAME          21  'logic.units.LPuppetRobot'
         350  IMPORT_FROM          22  'LPuppetRobot'
         353  STORE_FAST           12  'LPuppetRobot'
         356  POP_TOP          

 348     357  LOAD_FAST             9  'part'
         360  LOAD_GLOBAL          12  'HIT_PART_HEAD'
         363  COMPARE_OP            2  '=='
         366  POP_JUMP_IF_FALSE   473  'to 473'

 349     369  LOAD_GLOBAL          23  'isinstance'
         372  LOAD_FAST             0  'synchronizer'
         375  LOAD_ATTR            16  'unit_obj'
         378  LOAD_FAST            11  'LPuppet'
         381  CALL_FUNCTION_2       2 
         384  POP_JUMP_IF_TRUE    405  'to 405'
         387  LOAD_GLOBAL          23  'isinstance'
         390  LOAD_FAST             0  'synchronizer'
         393  LOAD_ATTR            16  'unit_obj'
         396  LOAD_FAST            12  'LPuppetRobot'
         399  CALL_FUNCTION_2       2 
       402_0  COME_FROM                '384'
         402  POP_JUMP_IF_FALSE   430  'to 430'

 350     405  LOAD_GLOBAL           3  'global_data'
         408  LOAD_ATTR            13  'emgr'
         411  LOAD_ATTR            24  'play_atk_voice'
         414  LOAD_ATTR            15  'emit'
         417  LOAD_CONST           11  'hit_head'
         420  LOAD_FAST             1  'bomb_id'
         423  CALL_FUNCTION_2       2 
         426  POP_TOP          
         427  JUMP_ABSOLUTE       574  'to 574'

 351     430  LOAD_FAST             0  'synchronizer'
         433  LOAD_ATTR            16  'unit_obj'
         436  LOAD_ATTR            25  'sd'
         439  LOAD_ATTR            26  'ref_is_mecha'
         442  POP_JUMP_IF_FALSE   574  'to 574'

 352     445  LOAD_GLOBAL           3  'global_data'
         448  LOAD_ATTR            13  'emgr'
         451  LOAD_ATTR            24  'play_atk_voice'
         454  LOAD_ATTR            15  'emit'
         457  LOAD_CONST           12  'hit_mecha_head'
         460  LOAD_FAST             1  'bomb_id'
         463  CALL_FUNCTION_2       2 
         466  POP_TOP          
         467  JUMP_ABSOLUTE       574  'to 574'
         470  JUMP_ABSOLUTE       617  'to 617'

 354     473  LOAD_GLOBAL          23  'isinstance'
         476  LOAD_FAST             0  'synchronizer'
         479  LOAD_ATTR            16  'unit_obj'
         482  LOAD_FAST            11  'LPuppet'
         485  CALL_FUNCTION_2       2 
         488  POP_JUMP_IF_TRUE    509  'to 509'
         491  LOAD_GLOBAL          23  'isinstance'
         494  LOAD_FAST             0  'synchronizer'
         497  LOAD_ATTR            16  'unit_obj'
         500  LOAD_FAST            12  'LPuppetRobot'
         503  CALL_FUNCTION_2       2 
       506_0  COME_FROM                '488'
         506  POP_JUMP_IF_FALSE   534  'to 534'

 355     509  LOAD_GLOBAL           3  'global_data'
         512  LOAD_ATTR            13  'emgr'
         515  LOAD_ATTR            24  'play_atk_voice'
         518  LOAD_ATTR            15  'emit'
         521  LOAD_CONST           13  'hit_body'
         524  LOAD_FAST             1  'bomb_id'
         527  CALL_FUNCTION_2       2 
         530  POP_TOP          
         531  JUMP_ABSOLUTE       617  'to 617'

 356     534  LOAD_FAST             0  'synchronizer'
         537  LOAD_ATTR            16  'unit_obj'
         540  LOAD_ATTR            25  'sd'
         543  LOAD_ATTR            26  'ref_is_mecha'
         546  POP_JUMP_IF_FALSE   617  'to 617'

 357     549  LOAD_GLOBAL           3  'global_data'
         552  LOAD_ATTR            13  'emgr'
         555  LOAD_ATTR            24  'play_atk_voice'
         558  LOAD_ATTR            15  'emit'
         561  LOAD_CONST           14  'hit_mecha_body'
         564  LOAD_FAST             1  'bomb_id'
         567  CALL_FUNCTION_2       2 
         570  POP_TOP          
         571  JUMP_ABSOLUTE       617  'to 617'
         574  JUMP_FORWARD         40  'to 617'

 360     577  LOAD_FAST             8  'math3d'
         580  LOAD_ATTR             9  'vector'
         583  LOAD_FAST             5  'tp3_pos'
         586  CALL_FUNCTION_VAR_0     0 
         589  STORE_FAST           10  'target_pos'

 361     592  LOAD_FAST             0  'synchronizer'
         595  LOAD_ATTR             2  'send_event'
         598  LOAD_CONST            8  'E_HIT_BOMB_SOUND'
         601  LOAD_FAST            10  'target_pos'
         604  LOAD_FAST             1  'bomb_id'
         607  LOAD_GLOBAL          27  'False'
         610  LOAD_FAST             6  'parts'
         613  CALL_FUNCTION_5       5 
         616  POP_TOP          
       617_0  COME_FROM                '574'

 363     617  LOAD_GLOBAL          28  'EntityManager'
         620  LOAD_ATTR            29  'getentity'
         623  LOAD_FAST             4  'id_trigger'
         626  CALL_FUNCTION_1       1 
         629  STORE_FAST           13  'triger'

 364     632  LOAD_GLOBAL          30  'check_enter_battle_state'
         635  LOAD_FAST            13  'triger'
         638  LOAD_FAST             0  'synchronizer'
         641  CALL_FUNCTION_2       2 
         644  POP_TOP          

 366     645  LOAD_GLOBAL          27  'False'
         648  STORE_FAST           14  'triger_is_mecha'

 367     651  LOAD_FAST            13  'triger'
         654  POP_JUMP_IF_FALSE   696  'to 696'
         657  LOAD_FAST            13  'triger'
         660  LOAD_ATTR            31  'logic'
       663_0  COME_FROM                '654'
         663  POP_JUMP_IF_FALSE   696  'to 696'

 368     666  LOAD_FAST            13  'triger'
         669  LOAD_ATTR            31  'logic'
         672  LOAD_ATTR            32  'ev_g_in_mecha'
         675  CALL_FUNCTION_0       0 
         678  POP_JUMP_IF_FALSE   687  'to 687'
         681  LOAD_GLOBAL          18  'True'
         684  JUMP_FORWARD          3  'to 690'
         687  LOAD_GLOBAL          27  'False'
       690_0  COME_FROM                '684'
         690  STORE_FAST           14  'triger_is_mecha'
         693  JUMP_FORWARD          0  'to 696'
       696_0  COME_FROM                '693'

 370     696  LOAD_FAST             2  'damage'
         699  LOAD_FAST             3  'shield_damage'
         702  BINARY_ADD       
         703  STORE_FAST           15  'total_damage'

 372     706  LOAD_GLOBAL          33  'on_hit_judge'
         709  LOAD_FAST             0  'synchronizer'
         712  LOAD_FAST             4  'id_trigger'
         715  LOAD_FAST            15  'total_damage'
         718  CALL_FUNCTION_3       3 
         721  POP_TOP          

 373     722  LOAD_FAST             2  'damage'
         725  POP_JUMP_IF_TRUE    734  'to 734'
         728  LOAD_FAST             3  'shield_damage'
         731  JUMP_FORWARD          3  'to 737'
         734  LOAD_FAST             2  'damage'
       737_0  COME_FROM                '731'
         737  STORE_FAST            2  'damage'

 374     740  LOAD_GLOBAL          34  'show_hurt_dir'
         743  LOAD_FAST            13  'triger'
         746  LOAD_FAST            15  'total_damage'
         749  LOAD_FAST             2  'damage'
         752  LOAD_CONST           16  'id_trigger'
         755  LOAD_FAST             4  'id_trigger'
         758  CALL_FUNCTION_514   514 
         761  POP_TOP          

 376     762  LOAD_FAST             0  'synchronizer'
         765  LOAD_ATTR             2  'send_event'
         768  LOAD_CONST           17  'E_SHOW_SCREEN_HURT_SFX'
         771  LOAD_GLOBAL          35  'FIGHT_INJ_BOMB'
         774  LOAD_FAST             2  'damage'
         777  LOAD_FAST             8  'math3d'
         780  LOAD_ATTR             9  'vector'
         783  LOAD_FAST             5  'tp3_pos'
         786  CALL_FUNCTION_VAR_0     0 
         789  LOAD_FAST             1  'bomb_id'
         792  LOAD_FAST            14  'triger_is_mecha'
         795  CALL_FUNCTION_6       6 
         798  POP_TOP          

 377     799  LOAD_FAST             0  'synchronizer'
         802  LOAD_ATTR             2  'send_event'
         805  LOAD_CONST           18  'E_HIT_SHIELD_SFX'
         808  LOAD_CONST           19  'end'
         811  LOAD_FAST             8  'math3d'
         814  LOAD_ATTR             9  'vector'
         817  LOAD_FAST             5  'tp3_pos'
         820  CALL_FUNCTION_VAR_0     0 
         823  LOAD_CONST           20  'itype'
         826  LOAD_FAST             1  'bomb_id'
         829  CALL_FUNCTION_513   513 
         832  POP_TOP          

 378     833  LOAD_FAST             0  'synchronizer'
         836  LOAD_ATTR             2  'send_event'
         839  LOAD_CONST           21  'E_HIT_FIELD_SHIELD'
         842  LOAD_CONST           19  'end'
         845  LOAD_FAST             8  'math3d'
         848  LOAD_ATTR             9  'vector'
         851  LOAD_FAST             5  'tp3_pos'
         854  CALL_FUNCTION_VAR_0     0 
         857  CALL_FUNCTION_257   257 
         860  POP_TOP          

 379     861  LOAD_CONST            0  ''
         864  STORE_FAST           16  'sfx_path'

 380     867  LOAD_GLOBAL          27  'False'
         870  STORE_FAST           17  'ignore_shield'

 388     873  LOAD_FAST            13  'triger'
         876  POP_JUMP_IF_FALSE   915  'to 915'
         879  LOAD_FAST            13  'triger'
         882  LOAD_ATTR            31  'logic'
         885  LOAD_ATTR            37  'ev_g_is_avatar'
         888  CALL_FUNCTION_0       0 
         891  POP_JUMP_IF_FALSE   915  'to 915'
         894  LOAD_FAST             1  'bomb_id'
         897  LOAD_CONST           22  800602
         900  COMPARE_OP            2  '=='
       903_0  COME_FROM                '891'
       903_1  COME_FROM                '876'
         903  POP_JUMP_IF_FALSE   915  'to 915'

 389     906  LOAD_CONST           23  'effect/fx/mecha/8006/8006_s02_shouji_fresnel.sfx'
         909  STORE_FAST           16  'sfx_path'
         912  JUMP_FORWARD          0  'to 915'
       915_0  COME_FROM                '912'

 390     915  LOAD_FAST             0  'synchronizer'
         918  LOAD_ATTR             2  'send_event'
         921  LOAD_CONST           24  'E_SHOW_PART_HIGHLIGHT'
         924  LOAD_CONST            0  ''
         927  LOAD_FAST            16  'sfx_path'
         930  LOAD_FAST            17  'ignore_shield'
         933  CALL_FUNCTION_4       4 
         936  POP_TOP          

 392     937  LOAD_FAST             0  'synchronizer'
         940  LOAD_ATTR             2  'send_event'
         943  LOAD_CONST           25  'E_RECORD_ON_HIT_INFO'
         946  LOAD_FAST             4  'id_trigger'
         949  LOAD_FAST             1  'bomb_id'
         952  LOAD_FAST             8  'math3d'
         955  LOAD_ATTR             9  'vector'
         958  LOAD_FAST             5  'tp3_pos'
         961  CALL_FUNCTION_VAR_0     0 
         964  CALL_FUNCTION_4       4 
         967  POP_TOP          

 394     968  LOAD_FAST             0  'synchronizer'
         971  LOAD_ATTR             2  'send_event'
         974  LOAD_CONST           26  'E_ON_HIT'
         977  CALL_FUNCTION_1       1 
         980  POP_TOP          

 395     981  LOAD_FAST             0  'synchronizer'
         984  LOAD_ATTR             2  'send_event'
         987  LOAD_CONST           27  'E_ON_HIT_BOMB_INFO'
         990  LOAD_FAST             8  'math3d'
         993  LOAD_ATTR             9  'vector'
         996  LOAD_FAST             5  'tp3_pos'
         999  CALL_FUNCTION_VAR_0     0 
        1002  LOAD_FAST             2  'damage'
        1005  CALL_FUNCTION_3       3 
        1008  POP_TOP          

 396    1009  LOAD_FAST             0  'synchronizer'
        1012  LOAD_ATTR             2  'send_event'
        1015  LOAD_CONST           28  'E_BOMB_HIT_SFX'
        1018  LOAD_FAST             1  'bomb_id'
        1021  CALL_FUNCTION_2       2 
        1024  POP_TOP          

 398    1025  LOAD_GLOBAL          38  'check_monster_hit'
        1028  LOAD_FAST             0  'synchronizer'
        1031  LOAD_ATTR            16  'unit_obj'
        1034  LOAD_ATTR             5  'id'
        1037  LOAD_FAST             4  'id_trigger'
        1040  CALL_FUNCTION_2       2 
        1043  POP_TOP          

 399    1044  LOAD_FAST             5  'tp3_pos'
        1047  POP_JUMP_IF_FALSE  1084  'to 1084'

 400    1050  LOAD_FAST             0  'synchronizer'
        1053  LOAD_ATTR             2  'send_event'
        1056  LOAD_CONST           29  'E_HITED_SHOW_HURT_THROW_SCREEN_TRK'
        1059  LOAD_FAST             8  'math3d'
        1062  LOAD_ATTR             9  'vector'
        1065  LOAD_FAST             5  'tp3_pos'
        1068  CALL_FUNCTION_VAR_0     0 
        1071  LOAD_FAST             1  'bomb_id'
        1074  LOAD_FAST            14  'triger_is_mecha'
        1077  CALL_FUNCTION_4       4 
        1080  POP_TOP          
        1081  JUMP_FORWARD          0  'to 1084'
      1084_0  COME_FROM                '1081'
        1084  LOAD_CONST            0  ''
        1087  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_514' instruction at offset 758


def on_hit_crash(synchronizer, crash_type, id_trigger, damage, tp3_pos, item_id=0):
    import math3d
    from logic.gcommon.common_const import crash_const
    import random
    if damage and (id_trigger == global_data.player.id or global_data.cam_lplayer and global_data.cam_lplayer.id == id_trigger):
        global_data.emgr.player_make_damage_event.emit(synchronizer.unit_obj, {-1: [1, damage]}, 0, item_id)
    on_hit_judge(synchronizer, id_trigger, damage)
    check_mecha_hit_shield(synchronizer, id_trigger)
    if global_data.player.id == synchronizer.unit_obj.id and global_data.player.logic:
        if id_trigger is None or crash_type == crash_const.CRASH_TYPE_INSIDE:
            pos = global_data.player.logic.ev_g_position()
            if pos:
                dir_pos = pos + math3d.vector(random.randint(1, 10), 0, random.randint(1, 10))
                synchronizer.send_event('E_HITED_SHOW_HURT_DIR', id_trigger, dir_pos, damage=damage, is_mecha=False)
    if tp3_pos:
        synchronizer.send_event('E_HITED_SHOW_HURT_OTHER_SCREEN_TRK', math3d.vector(*tp3_pos), damage)
        fight_inj_type = FIGHT_INJ_CRASH if id_trigger else FIGHT_INJ_FALLING
        synchronizer.send_event('E_SHOW_SCREEN_HURT_SFX', fight_inj_type, damage, math3d.vector(*tp3_pos))
    synchronizer.send_event('E_ON_HIT')
    return


def on_hit_skill--- This code section failed: ---

 428       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('SHOOT_MASK_AT_AIM',)
           6  IMPORT_NAME           0  'logic.gcommon.common_const.battle_const'
           9  IMPORT_FROM           1  'SHOOT_MASK_AT_AIM'
          12  STORE_FAST            9  'SHOOT_MASK_AT_AIM'
          15  POP_TOP          

 429      16  LOAD_FAST             0  'synchronizer'
          19  LOAD_ATTR             2  '_is_avatar'
          22  POP_JUMP_IF_TRUE     41  'to 41'

 430      25  LOAD_FAST             0  'synchronizer'
          28  LOAD_ATTR             3  'send_event'
          31  LOAD_CONST            3  'E_HITED'
          34  CALL_FUNCTION_1       1 
          37  POP_TOP          
          38  JUMP_FORWARD          0  'to 41'
        41_0  COME_FROM                '38'

 432      41  LOAD_GLOBAL           4  'False'
          44  STORE_FAST           10  'trigger_is_self'

 433      47  LOAD_FAST             6  'id_trigger'
          50  LOAD_GLOBAL           5  'global_data'
          53  LOAD_ATTR             6  'player'
          56  LOAD_ATTR             7  'id'
          59  COMPARE_OP            2  '=='
          62  POP_JUMP_IF_TRUE     92  'to 92'
          65  LOAD_GLOBAL           5  'global_data'
          68  LOAD_ATTR             8  'cam_lplayer'
          71  POP_JUMP_IF_FALSE   219  'to 219'
          74  LOAD_GLOBAL           5  'global_data'
          77  LOAD_ATTR             8  'cam_lplayer'
          80  LOAD_ATTR             7  'id'
          83  LOAD_FAST             6  'id_trigger'
          86  COMPARE_OP            2  '=='
        89_0  COME_FROM                '71'
        89_1  COME_FROM                '62'
          89  POP_JUMP_IF_FALSE   219  'to 219'

 434      92  LOAD_GLOBAL           9  'True'
          95  STORE_FAST           10  'trigger_is_self'

 435      98  LOAD_FAST             8  'extra_dict'
         101  LOAD_ATTR            10  'get'
         104  LOAD_GLOBAL          11  'EXECUTE_HIT_HINT'
         107  CALL_FUNCTION_1       1 
         110  POP_JUMP_IF_FALSE   119  'to 119'
         113  LOAD_GLOBAL          12  'HIT_PART_HEAD'
         116  JUMP_FORWARD          3  'to 122'
         119  LOAD_GLOBAL          13  'HIT_PART_BODY'
       122_0  COME_FROM                '116'
         122  STORE_FAST           11  'hit_part'

 436     125  LOAD_GLOBAL           5  'global_data'
         128  LOAD_ATTR            14  'emgr'
         131  LOAD_ATTR            15  'player_make_damage_event'
         134  LOAD_ATTR            16  'emit'
         137  LOAD_FAST             0  'synchronizer'
         140  LOAD_ATTR            17  'unit_obj'
         143  BUILD_MAP_1           1 
         146  LOAD_CONST            4  1
         149  LOAD_FAST             4  'damage'
         152  BUILD_LIST_2          2 
         155  LOAD_FAST            11  'hit_part'
         158  STORE_MAP        
         159  LOAD_FAST             5  'shield_damage'
         162  LOAD_FAST             1  'skill_id'
         165  LOAD_FAST             8  'extra_dict'
         168  CALL_FUNCTION_5       5 
         171  POP_TOP          

 437     172  LOAD_FAST             0  'synchronizer'
         175  LOAD_ATTR             3  'send_event'
         178  LOAD_CONST            5  'E_SHOW_HP_OVER_HEAD'
         181  CALL_FUNCTION_1       1 
         184  POP_TOP          

 438     185  LOAD_GLOBAL           5  'global_data'
         188  LOAD_ATTR            18  'cam_lctarget'
         191  POP_JUMP_IF_FALSE   219  'to 219'

 439     194  LOAD_GLOBAL           5  'global_data'
         197  LOAD_ATTR            18  'cam_lctarget'
         200  LOAD_ATTR             3  'send_event'
         203  LOAD_CONST            6  'E_HIT_TARGET'
         206  BUILD_MAP_0           0 
         209  CALL_FUNCTION_2       2 
         212  POP_TOP          
         213  JUMP_ABSOLUTE       219  'to 219'
         216  JUMP_FORWARD          0  'to 219'
       219_0  COME_FROM                '216'

 442     219  LOAD_GLOBAL          19  'check_monster_hit'
         222  LOAD_FAST             0  'synchronizer'
         225  LOAD_ATTR            17  'unit_obj'
         228  LOAD_ATTR             7  'id'
         231  LOAD_FAST             6  'id_trigger'
         234  CALL_FUNCTION_2       2 
         237  POP_TOP          

 443     238  LOAD_GLOBAL          20  'check_mecha_hit_shield'
         241  LOAD_FAST             0  'synchronizer'
         244  LOAD_FAST             6  'id_trigger'
         247  CALL_FUNCTION_2       2 
         250  POP_TOP          

 445     251  LOAD_FAST             4  'damage'
         254  POP_JUMP_IF_TRUE    263  'to 263'
         257  LOAD_FAST             5  'shield_damage'
         260  JUMP_FORWARD          3  'to 266'
         263  LOAD_FAST             4  'damage'
       266_0  COME_FROM                '260'
         266  STORE_FAST            4  'damage'

 447     269  LOAD_FAST             5  'shield_damage'
         272  LOAD_FAST             4  'damage'
         275  BINARY_ADD       
         276  STORE_FAST           12  'total_damage'

 448     279  LOAD_GLOBAL          21  'on_hit_judge'
         282  LOAD_FAST             0  'synchronizer'
         285  LOAD_FAST             6  'id_trigger'
         288  LOAD_FAST            12  'total_damage'
         291  CALL_FUNCTION_3       3 
         294  POP_TOP          

 450     295  LOAD_GLOBAL          22  'EntityManager'
         298  LOAD_ATTR            23  'getentity'
         301  LOAD_FAST             6  'id_trigger'
         304  CALL_FUNCTION_1       1 
         307  STORE_FAST           13  'trigger_ent'

 451     310  LOAD_FAST            13  'trigger_ent'
         313  POP_JUMP_IF_FALSE   384  'to 384'
         316  LOAD_FAST            13  'trigger_ent'
         319  LOAD_ATTR            24  'logic'
       322_0  COME_FROM                '313'
         322  POP_JUMP_IF_FALSE   384  'to 384'

 452     325  LOAD_FAST            13  'trigger_ent'
         328  LOAD_ATTR            24  'logic'
         331  LOAD_ATTR            25  'ev_g_position'
         334  CALL_FUNCTION_0       0 
         337  STORE_FAST           14  'pos'

 453     340  LOAD_FAST             0  'synchronizer'
         343  LOAD_ATTR             3  'send_event'
         346  LOAD_CONST            7  'E_HITED_SHOW_HURT_OTHER_SCREEN_TRK'
         349  LOAD_FAST            14  'pos'
         352  LOAD_FAST             4  'damage'
         355  CALL_FUNCTION_3       3 
         358  POP_TOP          

 454     359  LOAD_FAST             0  'synchronizer'
         362  LOAD_ATTR             3  'send_event'
         365  LOAD_CONST            8  'E_SHOW_SCREEN_HURT_SFX'
         368  LOAD_GLOBAL          26  'FIGHT_INJ_SKILL'
         371  LOAD_FAST             4  'damage'
         374  LOAD_FAST            14  'pos'
         377  CALL_FUNCTION_4       4 
         380  POP_TOP          
         381  JUMP_FORWARD          0  'to 384'
       384_0  COME_FROM                '381'

 456     384  LOAD_GLOBAL          22  'EntityManager'
         387  LOAD_ATTR            23  'getentity'
         390  LOAD_FAST             6  'id_trigger'
         393  CALL_FUNCTION_1       1 
         396  STORE_FAST           15  'triger'

 457     399  LOAD_GLOBAL          27  'check_enter_battle_state'
         402  LOAD_FAST            15  'triger'
         405  LOAD_FAST             0  'synchronizer'
         408  CALL_FUNCTION_2       2 
         411  POP_TOP          

 458     412  LOAD_GLOBAL          28  'show_hurt_dir'
         415  LOAD_FAST            15  'triger'
         418  LOAD_FAST             9  'SHOOT_MASK_AT_AIM'
         421  LOAD_FAST             4  'damage'
         424  LOAD_CONST           10  'id_trigger'
         427  LOAD_FAST             6  'id_trigger'
         430  CALL_FUNCTION_514   514 
         433  POP_TOP          

 459     434  LOAD_FAST             0  'synchronizer'
         437  LOAD_ATTR             3  'send_event'
         440  LOAD_CONST           11  'E_ON_HIT'
         443  CALL_FUNCTION_1       1 
         446  POP_TOP          

 461     447  LOAD_FAST             0  'synchronizer'
         450  LOAD_ATTR             3  'send_event'
         453  LOAD_CONST           12  'E_PALY_SKILL_HIT_SOUND'
         456  LOAD_FAST             1  'skill_id'
         459  LOAD_FAST            10  'trigger_is_self'
         462  CALL_FUNCTION_3       3 
         465  POP_TOP          

Parse error at or near `CALL_FUNCTION_514' instruction at offset 430


def reloaded(synchronizer, reload_num, wp_pos=None):
    synchronizer.send_event('E_RELOADED', reload_num, wp_pos)


def do_break(synchronizer):
    synchronizer.send_event('E_BREAK')


def air_shoot(synchronizer, start, end, scene_pellet, id_trigger, shoot_mask, ext_dict=None):
    start_pos = tp_to_v3d(start)
    end_pos = tp_to_v3d(end)
    global_data.emgr.teammate_on_fire.emit(id_trigger)
    if global_data.player and global_data.player.id != id_trigger:
        if synchronizer.sd.ref_is_robot:
            synchronizer.send_event('E_CHECK_ATK_POS', start_pos, False, None)
        else:
            synchronizer.send_event('E_AIR_SHOOT', start_pos, end_pos, scene_pellet, shoot_mask, ext_dict)
    return


def set_aim_target(synchronizer, target_id):
    if target_id is None:
        synchronizer.send_event('E_AIM_TARGET', None)
    else:
        from mobile.common.EntityManager import EntityManager
        ent = EntityManager.getentity(target_id)
        if ent and ent.logic:
            synchronizer.send_event('E_AIM_TARGET', ent.logic)
    return


def try_gen_robot_nearby(synchronizer, players):
    synchronizer.send_event('E_ROBOT_TRY_GEN_NEARBY', players)


def query_robot_dead_pos(synchronizer, rid):
    synchronizer.send_event('E_ROBOT_DEAD_POS', rid)


def set_shield(synchronizer, shield, add_from_dmg):
    synchronizer.send_event('E_SET_SHIELD', shield, add_from_dmg)


def enable_shield_overfull(synchronizer, flag):
    synchronizer.send_event('E_ENABLE_SHIELD_OVERFULL', flag)


def set_temporary_shield(synchronizer, temporary_shield_map):
    synchronizer.send_event('E_SET_TEMPORARY_SHIELD', temporary_shield_map)


def set_shield_max(synchronizer, max_hp, hp, change_hp=True):
    Event = synchronizer.send_event
    Event('E_SET_SHIELD_MAX', max_hp)
    if change_hp:
        Event('E_SET_SHIELD', hp)


def on_outer_shield_changed(synchronizer, outer_shield_hp):
    synchronizer.send_event('E_OUTER_SHIELD_HP_CHANGED', outer_shield_hp)


def set_fuel_max(synchronizer, max_fuel, cur_fuel):
    Event = synchronizer.send_event
    Event('E_SET_MAX_FUEL', max_fuel)
    Event('E_SET_CUR_FUEL', cur_fuel)


def set_skill_fuel_max(synchronizer, skill_id, max_fuel, cur_fuel):
    Event = synchronizer.send_event
    Event('E_SET_SKILL_MAX_FUEL', skill_id, max_fuel)
    Event('E_SET_SKILL_CUR_FUEL', skill_id, cur_fuel)


def add_fuel(synchronizer, delta):
    synchronizer.send_event('E_ADD_FUEL', delta)


def fresh_dummy_info(synchronizer, ret):
    from logic.comsys.debug.DummyTestUI import DummyTestUI
    DummyTestUI().update_data(ret)


def query_explosive_robot_pos(synchronizer, rid):
    from mobile.common.EntityManager import EntityManager
    robot = EntityManager.getentity(rid)
    if robot:
        pos = robot.logic.ev_g_position()
        robot.logic.send_event('E_CALL_SYNC_METHOD', 'explosive_robot_explode', ((pos.x, pos.y, pos.z),), True)


def heartbeat_request(synchronizer, idx):
    synchronizer.send_event('E_CALL_SYNC_METHOD', 'heartbeat_reply', (idx,), True)


def update_killer(synchronizer, killer, pos, faction):
    synchronizer.send_event('E_UPDATE_KILLER', killer, pos, faction)


def on_kill_prompt(synchronizer, prompt_id_list, short_kill_info):
    from logic.gcommon.common_const import battle_const
    from logic.gcommon.item.item_const import FASHION_POS_SUIT
    from logic.gutils import mecha_skin_utils
    from common.cfg import confmgr

    def get_mecha_default_fashion(mecha_id):
        if mecha_id:
            original_skin_lst = mecha_skin_utils.get_original_skin_lst(mecha_id)
            if original_skin_lst:
                return original_skin_lst[0]
        return None

    killer_mecha_id = short_kill_info.get('killer_mecha_id')
    dead_mecha_id = short_kill_info.get('mecha_id')
    killer_mecha_fashion = short_kill_info.get('killer_mecha_fashion', {}).get(FASHION_POS_SUIT) or get_mecha_default_fashion(killer_mecha_id)
    dead_mecha_fashion = short_kill_info.get('mecha_fasion', {}).get(FASHION_POS_SUIT) or get_mecha_default_fashion(dead_mecha_id)
    mecha_eid = short_kill_info.get('mecha_eid')
    mecha_entity = EntityManager.getentity(mecha_eid)
    for prompt_id in prompt_id_list:
        kill_conf = confmgr.get('kill_prompt', 'KillPrompt', 'Content') or {}
        kill_prompt_conf = kill_conf.get(str(prompt_id), {})
        tip_type = kill_prompt_conf.get('tip_type')
        if tip_type and tip_type in (battle_const.GVG_KILL_TIPS, battle_const.GVG_MULTI_KILL_TIPS):
            if synchronizer and mecha_entity and mecha_entity.logic:
                if synchronizer.ev_g_is_campmate(mecha_entity.logic.ev_g_camp_id()):
                    frd_mecha_id = dead_mecha_fashion
                    eny_mecha_id = killer_mecha_fashion
                    frd_is_killer = False
                else:
                    frd_mecha_id = killer_mecha_fashion
                    eny_mecha_id = dead_mecha_fashion
                    frd_is_killer = True
                if frd_mecha_id and eny_mecha_id:
                    msg = battle_utils.get_kill_prompt_msg(prompt_id, frd_mecha_id, eny_mecha_id, frd_is_killer, '')
                    synchronizer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, battle_const.MAIN_NODE_COMMON_INFO)
                    global_data.sound_mgr.play_ui_sound('get_small_achievements')
        else:
            msg = {'i_type': battle_const.TDM_KILL_TIPS,'content_txt': get_text_by_id(kill_prompt_conf.get('desc_id')),'bar_path': kill_prompt_conf.get('icon_path')}
            if global_data.game_mode.is_pve():
                if msg.get('i_type') == battle_const.TDM_KILL_TIPS:
                    msg.update({'voice_dict': {'tag': 'Play_ui_pve_achievement'}})
            synchronizer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, battle_const.MAIN_NODE_KILL_ACHIEVEMENT)
            if not global_data.game_mode.is_pve():
                global_data.sound_mgr.play_ui_sound('get_small_achievements')


def on_away_from_keyboard(synchronizer):
    if synchronizer.unit_obj and global_data.player and synchronizer.unit_obj.get_owner().id == global_data.player.id:
        global_data.emgr.show_hang_up_event.emit()


def fight_user_info(synchronizer):
    synchronizer.send_event('E_FIGHT_USER_INFO')


def update_exercise_dps_info(synchronizer, ret):
    pass


def on_hit_thunder(synchronizer, id_trigger, damage, shield_damage, item_id):
    total_damage = damage + shield_damage
    if total_damage and (id_trigger == global_data.player.id or global_data.cam_lplayer and global_data.cam_lplayer.id == id_trigger):
        global_data.emgr.player_make_damage_event.emit(synchronizer.unit_obj, {-1: [1, damage]}, shield_damage, item_id)
        synchronizer.send_event('E_SHOW_HP_OVER_HEAD')
        if global_data.cam_lctarget:
            global_data.cam_lctarget.send_event('E_HIT_TARGET', {})
    on_hit_judge(synchronizer, id_trigger, total_damage)
    synchronizer.send_event('E_ON_HIT')
    from common.cfg import confmgr
    sfx_path = confmgr.get('script_gim_ref')['thunder_hit_role_sfx']
    if synchronizer.unit_obj.sd.ref_is_mecha:
        sfx_path = confmgr.get('script_gim_ref')['thunder_hit_mecha_sfx']
    synchronizer.send_event('E_SHOW_SFX_ON_MODEL', sfx_path)
    need_shake = False
    if synchronizer.unit_obj.sd.ref_is_mecha:
        ctrl_target = global_data.player.logic.ev_g_control_target()
        if ctrl_target and synchronizer.unit_obj.id == ctrl_target.id:
            need_shake = True
        elif global_data.cam_lplayer:
            ctrl_target = global_data.cam_lplayer.ev_g_control_target()
            if ctrl_target and synchronizer.unit_obj.id == ctrl_target.id:
                need_shake = True
    elif synchronizer.unit_obj.id == global_data.player.id or global_data.cam_lplayer and global_data.cam_lplayer.id == synchronizer.unit_obj.id:
        need_shake = True
    if need_shake:
        sfx_path = confmgr.get('script_gim_ref')['thunder_shake_sfx']
        synchronizer.send_event('E_SHOW_SFX_ON_MODEL', sfx_path)
    synchronizer.send_event('E_HIT_LIGHTING_21')


def on_stun_change(synchronizer, stun):
    synchronizer.send_event('S_STUN', stun)


def steal_fuel(synchronizer, delta):
    synchronizer.send_event('E_STEAL_FUEL', delta)


def sync_forbid_recover_fuel(synchronizer, flag):
    synchronizer.send_event('E_FORBID_RECOVER_FUEL', flag)


def enable_8017_infinity_light_ball(synchronizer, enable):
    synchronizer.send_event('E_ENABLE_8017_INFINITY_LIGHT_BALL', enable)