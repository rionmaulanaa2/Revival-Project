# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/rogue_gift_config.py
_reload_all = True
if G_IS_NA_PROJECT:
    from .na_rogue_gift_config import *
else:
    data = {'survivalGiftData': {1002: {'gift_id': 1002,
                                   'name_id': 17101,
                                   'icon_path': 'gui/ui_res_2/item/rogue/1002.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/1002_small.png',
                                   'desc_id': 17201,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 2,
                                   'target': 1,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '30%'],
                                   'gift_params': {'ON_ADD': {'mod_add_attr': {'item_sing_time_factor': -0.3}}}},
                            1003: {'gift_id': 1003,
                                   'name_id': 17102,
                                   'icon_path': 'gui/ui_res_2/item/rogue/1003.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/1003_small.png',
                                   'desc_id': 17202,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 3,
                                   'target': 1,
                                   'triggerState': 15,
                                   'gift_params': {'ON_ADD': {'set_self_attr': {'iDropMechaModuleOnDie': 0}}}},
                            1005: {'gift_id': 1005,
                                   'name_id': 17104,
                                   'icon_path': 'gui/ui_res_2/item/rogue/1005.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/1005_small.png',
                                   'desc_id': 17204,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 3,
                                   'target': 1,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '20%'],
                                   'gift_params': {'ON_ADD': {'mod_add_attr': {'eject_speed_factor': 0.2},'set_self_attr': {'iShowTailEffectOnMechaDie': 0}}}},
                            2001: {'gift_id': 2001,
                                   'name_id': 17105,
                                   'icon_path': 'gui/ui_res_2/item/rogue/2001.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/2001_small.png',
                                   'desc_id': 17205,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 1,
                                   'target': 1,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '20%'],
                                   'gift_params': {'ON_ADD': {'mod_add_attr': {'recall_mecha_time_factor': -0.2},'reduce_mecha_first_recall_cd': {'reduce_ratio': 0.2}}}},
                            2002: {'gift_id': 2002,
                                   'name_id': 17106,
                                   'icon_path': 'gui/ui_res_2/item/rogue/2002.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/2002_small.png',
                                   'desc_id': 17206,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 2,
                                   'target': 1,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '20%'],
                                   'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2011: {'yaw': 0.2,'pitch': 0.2,'dis': 0}}}}}},
                            2004: {'gift_id': 2004,
                                   'name_id': 17108,
                                   'icon_path': 'gui/ui_res_2/item/rogue/2004.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/2004_small.png',
                                   'desc_id': 17208,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 2,
                                   'target': 1,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '300', '10'],
                                   'gift_params': {'ON_OPEN_BOX': {'add_self_buff_on_open_box': {'box_item_no_list': [6004, 6005, 6022, 6023, 6039, 6040],'add_buffs': {2009: {'radius': 300,'detect_num': 10,'extra_duration': 10}}}}}},
                            2005: {'gift_id': 2005,
                                   'name_id': 17109,
                                   'icon_path': 'gui/ui_res_2/item/rogue/2005.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/2005_small.png',
                                   'desc_id': 17209,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 3,
                                   'target': 1,
                                   'triggerState': 1,
                                   'desc_param': [
                                                '4'],
                                   'gift_params': {'ON_MECHA_DIE': {'gen_explosive_robot': {'num': 4,'item_type': 10561}}}},
                            3001: {'gift_id': 3001,
                                   'name_id': 17110,
                                   'icon_path': 'gui/ui_res_2/item/rogue/3001.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/3001_small.png',
                                   'desc_id': 17210,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 1,
                                   'target': 1,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '40%'],
                                   'gift_params': {'ON_ADD': {'mod_add_attr': {'recall_mecha_on_leave_time_factor': -0.4}}}},
                            3002: {'gift_id': 3002,
                                   'name_id': 17111,
                                   'icon_path': 'gui/ui_res_2/item/rogue/3002.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/3002_small.png',
                                   'desc_id': 17211,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 2,
                                   'target': 7,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '12%'],
                                   'gift_params': {'ON_MANUAL_HUMAN_DAMAGE_CALC': {'add_damage_on_first_shoot': {'add_ratio': 0.12}},'ON_MANUAL_MECHA_DAMAGE_CALC': {'add_damage_on_first_shoot': {'add_ratio': 0.12}}}},
                            3003: {'gift_id': 3003,
                                   'name_id': 17112,
                                   'icon_path': 'gui/ui_res_2/item/rogue/3003.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/3003_small.png',
                                   'desc_id': 17212,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 3,
                                   'target': 2,
                                   'triggerState': 2,
                                   'desc_param': [
                                                '2', '12%'],
                                   'gift_params': {'ON_DO_TACTIC_SKILL': {'add_self_buff': {'add_buffs': {2001: {'fight_factor': 0.12,'extra_duration': 2}}}}}},
                            3004: {'gift_id': 3004,
                                   'name_id': 17113,
                                   'icon_path': 'gui/ui_res_2/item/rogue/3004.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/3004_small.png',
                                   'desc_id': 17213,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 2,
                                   'target': 7,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '0.8%', '7'],
                                   'gift_params': {'ON_MANUAL_HUMAN_DAMAGE_CALC': {'kill_player_add_fight_factor': {'add_ratio': 0.008,'max_layer_num': 7}},'ON_MANUAL_MECHA_DAMAGE_CALC': {'kill_player_add_fight_factor': {'add_ratio': 0.008,'max_layer_num': 7}}}},
                            3005: {'gift_id': 3005,
                                   'name_id': 17114,
                                   'icon_path': 'gui/ui_res_2/item/rogue/3005.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/3005_small.png',
                                   'desc_id': 17214,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 3,
                                   'target': 2,
                                   'triggerState': 2,
                                   'desc_param': [
                                                '0.8%', '1.5', '10'],
                                   'gift_params': {'ON_FIGHT': {'upgrade_main_weapon': {'add_buffs': {2013: {'rate': 0.8,'max_layer_num': 10,'extra_duration': 1.5}}}}}},
                            4001: {'gift_id': 4001,
                                   'name_id': 17115,
                                   'icon_path': 'gui/ui_res_2/item/rogue/4001.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/4001_small.png',
                                   'desc_id': 17215,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 1,
                                   'target': 2,
                                   'triggerState': 2,
                                   'desc_param': [
                                                '3%', '3%'],
                                   'gift_params': {'ACE_DOUBLE': {'ace_double_effect': {'normal_effect': {'speed_buff': {2004: {}},'skill_cd_params': {'buff_id': 2005,'reduce_factor': 0.03}},'double_effect': {'speed_buff': {2014: {}},'skill_cd_params': {'buff_id': 2005,'reduce_factor': 0.06}}}}}},
                            4002: {'gift_id': 4002,
                                   'name_id': 17116,
                                   'icon_path': 'gui/ui_res_2/item/rogue/4002.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/4002_small.png',
                                   'desc_id': 17216,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 2,
                                   'target': 2,
                                   'triggerState': 2,
                                   'desc_param': [
                                                '3.5%', '3'],
                                   'gift_params': {'ON_MECHA_STAY': {'add_self_buff': {'add_buffs': {2006: {'fight_factor': 0.035,'max_layer_num': 3}}}}}},
                            4003: {'gift_id': 4003,
                                   'name_id': 17117,
                                   'icon_path': 'gui/ui_res_2/item/rogue/4003.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/4003_small.png',
                                   'desc_id': 17217,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 3,
                                   'target': 10,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '3%', '3'],
                                   'gift_params': {'ON_OPEN_BOX': {'add_self_buff_on_open_box': {'box_item_no_list': [6004, 6005, 6022, 6023, 6039, 6040],'add_buffs': {2007: {'rate': 3,'max_layer_num': 3,'duration': 1.5}}}}}},
                            4004: {'gift_id': 4004,
                                   'name_id': 17118,
                                   'icon_path': 'gui/ui_res_2/item/rogue/4004.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/4004_small.png',
                                   'desc_id': 17218,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 2,
                                   'target': 7,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '10%', '5', '1'],
                                   'trigger_interval': 60,
                                   'gift_params': {'ON_HURT': {'add_attacker_buff_on_damage': {'add_buffs': {469: {'ratio': 0.1,'extra_duration': 5,'need_buff_creator': 1}}}}}},
                            4005: {'gift_id': 4005,
                                   'name_id': 17119,
                                   'icon_path': 'gui/ui_res_2/item/rogue/4005.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/4005_small.png',
                                   'desc_id': 17219,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 3,
                                   'target': 2,
                                   'triggerState': 2,
                                   'desc_param': [
                                                '40%', '10%'],
                                   'gift_params': {'ON_MANUAL_MECHA_DAMAGE_CALC': {'mecha_add_damage_on_shoot': {'add_ratio': 0.1,'only_main_weapon': 1,'bullet_less_than': 0.4}}}},
                            5001: {'gift_id': 5001,
                                   'name_id': 17120,
                                   'icon_path': 'gui/ui_res_2/item/rogue/5001.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/5001_small.png',
                                   'desc_id': 17220,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 1,
                                   'target': 10,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '2'],
                                   'gift_params': {'ON_PICK_ACE_STAR': {'add_mecha_hp_on_pick_ace_star': {'buff_id': 2008,'add_hp': 2}}}},
                            5002: {'gift_id': 5002,
                                   'name_id': 17121,
                                   'icon_path': 'gui/ui_res_2/item/rogue/5002.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/5002_small.png',
                                   'desc_id': 17221,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 2,
                                   'target': 10,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '50', '10%', '50', '5%'],
                                   'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2010: {'dis': 50,'reduce_ratio': 0.1,'add_ratio': 0.05}}}}}},
                            5003: {'gift_id': 5003,
                                   'name_id': 17122,
                                   'icon_path': 'gui/ui_res_2/item/rogue/5003.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/5003_small.png',
                                   'desc_id': 17222,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 3,
                                   'target': 2,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '10%'],
                                   'gift_params': {'ON_KILL_MECHA': {'recover_mecha_hp': {'ratio': 0.1}}}},
                            5004: {'gift_id': 5004,
                                   'name_id': 17123,
                                   'icon_path': 'gui/ui_res_2/item/rogue/5004.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/5004_small.png',
                                   'desc_id': 17223,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 2,
                                   'target': 2,
                                   'triggerState': 2,
                                   'desc_param': [
                                                '15%', '2'],
                                   'trigger_interval': 120,
                                   'gift_params': {'ON_HURT': {'full_mecha_shield': {'ratio': 0.15}}}},
                            5005: {'gift_id': 5005,
                                   'name_id': 17124,
                                   'icon_path': 'gui/ui_res_2/item/rogue/5005.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/5005_small.png',
                                   'desc_id': 17224,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 3,
                                   'target': 2,
                                   'triggerState': 2,
                                   'desc_param': [
                                                '40%'],
                                   'gift_params': {'ON_CURE': {'transform_to_shield_on_cure_mecha': {'max_ratio': 0.4,'buff_id': 2015}}}},
                            6001: {'gift_id': 6001,
                                   'name_id': 17140,
                                   'icon_path': 'gui/ui_res_2/item/rogue/6001.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/6001_small.png',
                                   'desc_id': 17440,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 2,
                                   'target': 1,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '40%'],
                                   'gift_params': {'ON_ADD': {'mod_add_attr': {'fAddToMechaDmg': {'val': 0.4,'weapon_ids': [1001, 1002, 1003, 1023, 1024]}}}}},
                            6002: {'gift_id': 6002,
                                   'name_id': 17141,
                                   'icon_path': 'gui/ui_res_2/item/rogue/6002.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/6002_small.png',
                                   'desc_id': 17441,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 2,
                                   'target': 1,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '10%'],
                                   'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {535: {'reinforced_ids': [1056, 1066, 1059],'add_mag_size': 1}}}}}},
                            6003: {'gift_id': 6003,
                                   'name_id': 17142,
                                   'icon_path': 'gui/ui_res_2/item/rogue/6003.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/6003_small.png',
                                   'desc_id': 17442,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 1,
                                   'target': 10,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '20%'],
                                   'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {538: {'power_ratio': 0.2}}}}}},
                            6004: {'gift_id': 6004,
                                   'name_id': 17143,
                                   'icon_path': 'gui/ui_res_2/item/rogue/6004.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/6004_small.png',
                                   'desc_id': 17443,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 1,
                                   'target': 10,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '10%'],
                                   'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {540: {'power_factor': 0.1}}}}}},
                            6005: {'gift_id': 6005,
                                   'name_id': 17144,
                                   'icon_path': 'gui/ui_res_2/item/rogue/6005.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/6005_small.png',
                                   'desc_id': 17444,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 3,
                                   'target': 10,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '5%'],
                                   'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {536: {'spd_type': 'base','spd_val': 0.05,'power_ratio': 0.05,'def_ratio': 0.05}}}}}},
                            6006: {'gift_id': 6006,
                                   'name_id': 17145,
                                   'icon_path': 'gui/ui_res_2/item/rogue/6006.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/6006_small.png',
                                   'desc_id': 17445,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 1,
                                   'target': 1,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '200'],
                                   'trigger_interval': 60,
                                   'gift_params': {'ON_JOIN_MECHA': {'add_self_buff': {'add_buffs': {2009: {'radius': 200,'detect_num': 5,'extra_duration': 6,'show_self': 1}}}}}},
                            6007: {'gift_id': 6007,
                                   'name_id': 17146,
                                   'icon_path': 'gui/ui_res_2/item/rogue/6007.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/6007_small.png',
                                   'desc_id': 17446,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 1,
                                   'target': 10,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '15%', '10%'],
                                   'gift_params': {'ON_ADD': {'mod_add_attr': {'attr_add_dmg_to_same_mecha': 0.15},'add_self_buff': {'add_buffs': {537: {'need_same_mecha': 1,'keep_on_defeated': 1,'ratio': 0.1}}}}}},
                            6008: {'gift_id': 6008,
                                   'name_id': 17147,
                                   'icon_path': 'gui/ui_res_2/item/rogue/6008.png',
                                   'small_icon_path': 'gui/ui_res_2/item/rogue/6008_small.png',
                                   'desc_id': 17447,
                                   'is_open': 1,
                                   'is_survival': True,
                                   'is_death': False,
                                   'is_exclusive': False,
                                   'brand': 3,
                                   'target': 10,
                                   'triggerState': 15,
                                   'desc_param': [
                                                '10%'],
                                   'gift_params': {'ON_ADD': {'mod_add_attr': {'fAddFullHealthDmg': 0.1}}}}
                            },
       'deathBattleCandidates': {1: {'candidates': [
                                                  104001, 100003, 101002, 105002, 100004, 103001, 100002, 104004, 105001, 101005, 103003, 103004, 103005, 104002, 104005, 105003, 105004, 106003, 106004, 106005, 106006, 103002, 107001, 107002, 107003, 107004, 107005, 107006, 107007, 107008, 107009, 107010],
                                     'exclusiveCandidates': [
                                                           208004, 208008, 208005, 208013, 208023, 208012, 208009, 208026, 208015, 200001, 200002, 200003, 200004, 200005, 200006, 200007, 200008, 200009, 200010, 200011, 200012, 200013, 200014, 200015, 200016, 200017, 208027, 208030, 208031, 208032, 208029]
                                     },
                                 2: {'candidates': [
                                                  104001, 100003, 101002, 105002, 100004, 103001, 100002, 104004, 105001, 101005, 103003, 103004, 103005, 104002, 104005, 105003, 105004, 106003, 106004, 106005, 106006, 103002, 107001, 107002, 107003, 107004, 107005, 107006],
                                     'exclusiveCandidates': [
                                                           208004, 208008, 208005, 208013, 208023, 208012, 208009, 208026, 208015, 200001, 200002, 200003, 200004, 200005, 200006, 200007, 200008, 200009, 200010, 200011, 200012, 200013, 200014, 200015, 200016, 200017, 208027, 208030, 208031, 208032, 208029]
                                     },
                                 3: {'candidates': [
                                                  104001, 100003, 101002, 105002, 100004, 103001, 100002, 104004, 105001, 101005, 103003, 103004, 103005, 104002, 104005, 105003, 105004, 106003, 106004, 106005, 106006, 103002, 107001, 107002, 107003, 107004, 107005, 107006],
                                     'exclusiveCandidates': [
                                                           208004, 208008, 208005, 208013, 208023, 208012, 208009, 208026, 208015, 200001, 200002, 200003, 200004, 200005, 200006, 200007, 200008, 200009, 200010, 200011, 200012, 200013, 200014, 200015, 200016, 200017, 208027, 208030, 208031, 208032, 208029]
                                     },
                                 4: {'candidates': [
                                                  104001, 100003, 105002, 100004, 103001, 100002, 104004, 103003, 103004, 103005, 104002, 104005, 105003, 105004, 106003, 106004, 103002, 107001, 107003, 107004, 107005, 107006],
                                     'exclusiveCandidates': []},
                                 5: {'candidates': [
                                                  104001, 100003, 101002, 105002, 100004, 103001, 100002, 104004, 105001, 101005, 103003, 103004, 103005, 104002, 104005, 105003, 105004, 106003, 106004, 106005, 106006, 103002, 107001, 107002, 107003, 107004, 107005, 107006, 107007, 107008, 107009, 107010],
                                     'exclusiveCandidates': [
                                                           208004, 208008, 208005, 208013, 208023, 208012, 208009, 208026, 208015, 200001, 200002, 200003, 200004, 200005, 200006, 200007, 200008, 200009, 200010, 200011, 200012, 200013, 200014, 200015, 200016, 200017, 208027, 208030, 208031, 208032, 208029]
                                     },
                                 6: {'candidates': [
                                                  104001, 100003, 101002, 105002, 100004, 103001, 100002, 104004, 105001, 101005, 103003, 103004, 103005, 104002, 104005, 105003, 105004, 106003, 106004, 106005, 106006, 103002, 107001, 107002, 107003, 107004, 107005, 107006],
                                     'exclusiveCandidates': [
                                                           208004, 208008, 208005, 208013, 208023, 208012, 208009, 208026, 208015, 200001, 200002, 200003, 200004, 200005, 200006, 200007, 200008, 200009, 200010, 200011, 200012, 200013, 200014, 200015, 200016, 200017, 208027, 208030, 208031, 208032, 208029]
                                     },
                                 7: {'candidates': [
                                                  104001, 100003, 101002, 105002, 100004, 103001, 100002, 104004, 105001, 101005, 103003, 103004, 103005, 104002, 104005, 105003, 105004, 106003, 106004, 106005, 106006, 103002, 107001, 107002, 107003, 107004, 107005, 107006, 107007, 107008, 107009, 107010],
                                     'exclusiveCandidates': [
                                                           208004, 208008, 208005, 208013, 208023, 208012, 208009, 208026, 208015, 200001, 200002, 200003, 200004, 200005, 200006, 200007, 200008, 200009, 200010, 200011, 200012, 200013, 200014, 200015, 200016, 200017, 208027, 208030, 208031, 208032, 208029]
                                     },
                                 8: {'candidates': [
                                                  104001, 100003, 101002, 105002, 100004, 103001, 100002, 104004, 105001, 101005, 103003, 103004, 103005, 104002, 104005, 105003, 105004, 106003, 106004, 106005, 106006, 103002, 107001, 107002, 107003, 107004, 107005, 107006],
                                     'exclusiveCandidates': [
                                                           208004, 208008, 208005, 208013, 208023, 208012, 208009, 208026, 208015, 200001, 200002, 200003, 200004, 200005, 200006, 200007, 200008, 200009, 200010, 200011, 200012, 200013, 200014, 200015, 200016, 200017, 208027, 208030, 208031, 208032, 208029]
                                     },
                                 9: {'candidates': [
                                                  104001, 100003, 101002, 105002, 100004, 103001, 100002, 104004, 105001, 101005, 103003, 103004, 103005, 104002, 104005, 105003, 105004, 106003, 106004, 106005, 106006, 103002, 107001, 107002, 107003, 107004, 107005, 107006],
                                     'exclusiveCandidates': [
                                                           208004, 208008, 208005, 208013, 208023, 208012, 208009, 208026, 208015, 200001, 200002, 200003, 200004, 200005, 200006, 200007, 200008, 200009, 200010, 200011, 200012, 200013, 200014, 200015, 200016, 200017, 208027, 208030, 208031, 208032, 208029]
                                     },
                                 10: {'candidates': [
                                                   104001, 100003, 101002, 105002, 100004, 103001, 100002, 104004, 105001, 101005, 103003, 103004, 103005, 104002, 104005, 105003, 105004, 106003, 106004, 106005, 106006, 103002, 107001, 107002, 107003, 107004, 107005, 107006],
                                      'exclusiveCandidates': [
                                                            208004, 208008, 208005, 208013, 208023, 208012, 208009, 208026, 208015, 200001, 200002, 200003, 200004, 200005, 200006, 200007, 200008, 200009, 200010, 200011, 200012, 200013, 200014, 200015, 200016, 200017, 208027, 208030, 208031, 208032, 208029]
                                      }
                                 },
       'giftWeight': {1: 7,
                      2: 5,
                      3: 4
                      },
       'exclusiveGiftData': {208004: {'gift_id': 208004,
                                      'name_id': 17631,
                                      'mecha_id': 8004,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208004.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208004_small.png',
                                      'desc_id': 17731,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 2,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '300'],
                                      'trigger_interval': 1,
                                      'gift_params': {'ON_FIGHT': {'dash_hit_shield': {'add_buffs': {2021: {'extra_duration': 3,'outer_shield_hp': 300}},'mecha_id': 8004}}}},
                             208008: {'gift_id': 208008,
                                      'name_id': 17625,
                                      'mecha_id': 8008,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208008.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208008_small.png',
                                      'desc_id': 17725,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '40%'],
                                      'gift_params': {'ON_ADD': {'mod_add_mecha_attr': {'speed_up_factor': 0.4,'mecha_id': 8008}}}},
                             208005: {'gift_id': 208005,
                                      'name_id': 17623,
                                      'mecha_id': 8005,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208005.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208005_small.png',
                                      'desc_id': 17723,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '80%', '3'],
                                      'gift_params': {'ON_KILL_MECHA': {'kill_recover_cd': {'valid_ids': [8205],'skill_id': 800552,'fuel': 30}},'ON_ADD': {'mod_add_mecha_attr': {'skill_4_fuel_cost_factor': 1,'mecha_id': 8005,'skill_4_dmg_factor': 0.8}}}},
                             208013: {'gift_id': 208013,
                                      'name_id': 17628,
                                      'mecha_id': 8013,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208013.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208013_small.png',
                                      'desc_id': 17728,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '12%'],
                                      'gift_params': {'ON_ADD': {'add_mecha_buff': {'mecha_id': 8013,'add_buffs': {2022: {'accumulate_gun_factor': 0.12}}}}}},
                             208023: {'gift_id': 208023,
                                      'name_id': 17630,
                                      'mecha_id': 8023,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208023.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208023_small.png',
                                      'desc_id': 17730,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '1'],
                                      'gift_params': {'ON_ADD': {'add_mecha_buff': {'mecha_id': 8023,'add_buffs': {2065: {'add_phantom_cnt': 1}}}}}},
                             208012: {'gift_id': 208012,
                                      'name_id': 17626,
                                      'mecha_id': 8012,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208012.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208012_small.png',
                                      'desc_id': 17726,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '10%', '2'],
                                      'gift_params': {'ON_ADD': {'add_mecha_buff': {'mecha_id': 8012,'add_buffs': {404: {'buff_id': 399,'update_params': {'damage_human': {'method': 'multi','val': 0.1},'damage_other': {'method': 'multi','val': 0.1},'extra_duration': {'method': 'add','val': 2}}}}}}}},
                             208009: {'gift_id': 208009,
                                      'name_id': 17629,
                                      'mecha_id': 8009,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208009.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208009_small.png',
                                      'desc_id': 17729,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '9%', '3'],
                                      'gift_params': {'ON_ADD': {'mod_skill_data': {'skill_id': 800951,'skill_data': {'improve_weapon1_attack_ratio': 0.09}}}}},
                             208026: {'gift_id': 208026,
                                      'name_id': 17624,
                                      'mecha_id': 8026,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208026.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208026_small.png',
                                      'desc_id': 17724,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'gift_params': {'ON_ADD': {'add_mecha_buff': {'mecha_id': 8026,'add_buffs': {2025: {'camera_sense': 7}}}}}},
                             208015: {'gift_id': 208015,
                                      'name_id': 17627,
                                      'mecha_id': 8015,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208015.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208015_small.png',
                                      'desc_id': 17727,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'gift_params': {'ON_ADD': {'mod_skill_data': {'skill_id': 801551,'skill_data': {'invincible_in_dash': True}}}}},
                             200001: {'gift_id': 200001,
                                      'name_id': 17632,
                                      'mecha_id': 8002,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208002.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208002_small.png',
                                      'desc_id': 17739,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '10%'],
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2027: {'power_factor': 0.1,'target_wp_ids': [800201]}}}}}},
                             200002: {'gift_id': 200002,
                                      'name_id': 17633,
                                      'mecha_id': 8003,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208003.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208003_small.png',
                                      'desc_id': 17740,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '130%'],
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2028: {'power_factor': 0.3,'target_wp_ids': [800301]}}}}}},
                             200003: {'gift_id': 200003,
                                      'name_id': 17634,
                                      'mecha_id': 8006,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208006.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208006_small.png',
                                      'desc_id': 17741,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '2'],
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2029: {'conv_duration_rate': 0.005,'max_add_duration': 2}}}}}},
                             200004: {'gift_id': 200004,
                                      'name_id': 17635,
                                      'mecha_id': 8001,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208001.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208001_small.png',
                                      'desc_id': 17742,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2030: {},2031: {},2032: {},2033: {}}}}}},
                             200005: {'gift_id': 200005,
                                      'name_id': 17636,
                                      'mecha_id': 8010,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208010.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208010_small.png',
                                      'desc_id': 17743,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2034: {'add_factor': 0.1},2035: {'reduce_factor': 0.5,'skill_ids': [801055, 801056]}}}}}},
                             200006: {'gift_id': 200006,
                                      'name_id': 17637,
                                      'mecha_id': 8014,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208014.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208014_small.png',
                                      'desc_id': 17744,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2036: {'near_dist': 20,'power_factor': 0.1,'wp_ids': [801401]}}}}}},
                             200007: {'gift_id': 200007,
                                      'name_id': 17638,
                                      'mecha_id': 8016,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208016.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208016_small.png',
                                      'desc_id': 17745,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2037: {'instant_kill_health': 0.1,'valid_wp_ids': [801651]}}}}}},
                             200008: {'gift_id': 200008,
                                      'name_id': 17642,
                                      'mecha_id': 8020,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208020.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208020_small.png',
                                      'desc_id': 17749,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '2', '200'],
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2039: {'valid_wp_ids': [802053],'damage': 200},575: {}}}}}},
                             200009: {'gift_id': 200009,
                                      'name_id': 17639,
                                      'mecha_id': 8011,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208011.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208011_small.png',
                                      'desc_id': 17746,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '30%'],
                                      'trigger_interval': 20,
                                      'gift_params': {'ON_HURT': {'add_skill_fuel': {'count': 1,'skill_id': 801155,'hp_percent': 0.3},'full_fill_weapon': {'wp_pos': 1,'hp_percent': 0.3}}}},
                             200010: {'gift_id': 200010,
                                      'name_id': 17640,
                                      'mecha_id': 8022,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208022.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208022_small.png',
                                      'desc_id': 17747,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '1.5', '10%'],
                                      'gift_params': {'ON_HURT': {'add_attacker_mark': {'mark_buff_id': 2040}},'ON_ADD': {'add_self_buff': {'add_buffs': {2041: {'power_factor': 0.1,'cd': 1,'valid_wp_ids': [802203]}}}}}},
                             200011: {'gift_id': 200011,
                                      'name_id': 17641,
                                      'mecha_id': 8007,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208007.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208007_small.png',
                                      'desc_id': 17748,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '25%', '3'],
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2042: {'hp_percent': 0.25,'valid_wp_ids': [800702, 800703, 800704, 800705, 800706]}}}}}},
                             200012: {'gift_id': 200012,
                                      'name_id': 17643,
                                      'mecha_id': 8024,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208024.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208024_small.png',
                                      'desc_id': 17750,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '3'],
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2045: {'add_buff_id': 2044,'add_buff_data': {'energy_clip': 100,'energy_add_range': [10, 40],'max_count': 3,'robot_no': 105631}}}}}}},
                             200013: {'gift_id': 200013,
                                      'name_id': 17644,
                                      'mecha_id': 8025,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208025.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208025_small.png',
                                      'desc_id': 17751,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '80%'],
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2048: {'heat_reduce_factor': 0.4,'decay_speed_buff_data': {'spd_val': 2,'spd_type': 'base','speed_decay': 0.4}}}}}}},
                             200014: {'gift_id': 200014,
                                      'name_id': 17648,
                                      'mecha_id': 8017,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208017.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208017_small.png',
                                      'desc_id': 17755,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '10%', '10%'],
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2051: {'shield_ratio': 0.1,'power_ratio': 0.1,'keep_on_defeat': 1}}}}}},
                             200015: {'gift_id': 200015,
                                      'name_id': 17649,
                                      'mecha_id': 8028,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208028.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208028_small.png',
                                      'desc_id': 17756,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '70%'],
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2052: {'reduce_factor': 0.3}}}}}},
                             200016: {'gift_id': 200016,
                                      'name_id': 17650,
                                      'mecha_id': 8021,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208021.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208021_small.png',
                                      'desc_id': 17757,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '5', '15%'],
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2054: {'ratio': 0.15},575: {'add_buffs': {2053: {'enable_ids': [802154, 802151]}}}}}}}},
                             200017: {'gift_id': 200017,
                                      'name_id': 17651,
                                      'mecha_id': 8019,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208019.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208019_small.png',
                                      'desc_id': 17758,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 10,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '5', '15%', '50'],
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2056: {'broken_buff': {2055: {'fight_factor': 0.15}},'shield_recover': 50}}}}}},
                             208027: {'gift_id': 208027,
                                      'name_id': 17659,
                                      'mecha_id': 8027,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208027.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208027_small.png',
                                      'desc_id': 17766,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 2,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '4%'],
                                      'gift_params': {'ON_FIGHT': {'wp_hit_power_factor': {'mecha_id': 8027,'add_buffs': {31802705: {'power_factor': 0.04,'target_wp_ids': [802702]}}}}}},
                             208029: {'gift_id': 208029,
                                      'name_id': 17660,
                                      'mecha_id': 8029,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208029.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208029_small.png',
                                      'desc_id': 17767,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 2,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '50', '50', '300'],
                                      'gift_params': {'ON_8029_PHANTOM_TELEPORT': {'add_8029_temporary_shield': {'add_buffs': {31802920: {'mecha_shield': 300,'mecha_shield_per_layer': 50,'min_add_mecha_shield': 50}}}}}},
                             208032: {'gift_id': 208032,
                                      'name_id': 17661,
                                      'mecha_id': 8032,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208032.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208032_small.png',
                                      'desc_id': 17768,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 2,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '8%'],
                                      'gift_params': {'ON_8032_ENTER_SPRINT': {'add_self_buff': {'add_buffs': {31803207: {'no_condition': 1,'ratio': 0.08}}}}}},
                             208031: {'gift_id': 208031,
                                      'name_id': 17662,
                                      'mecha_id': 8031,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208031.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208031_small.png',
                                      'desc_id': 17769,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 2,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '10%'],
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {31803106: {'acc_rate': 0.1,'max_dist': 150,'max_angle': 60}}}}}},
                             208030: {'gift_id': 208030,
                                      'name_id': 17663,
                                      'mecha_id': 8030,
                                      'icon_path': 'gui/ui_res_2/item/rogue/208030.png',
                                      'small_icon_path': 'gui/ui_res_2/item/rogue/208030_small.png',
                                      'desc_id': 17770,
                                      'is_open': 1,
                                      'quality': 2,
                                      'is_survival': False,
                                      'is_death': False,
                                      'is_exclusive': True,
                                      'brand': 2,
                                      'target': 2,
                                      'triggerState': 15,
                                      'desc_param': [
                                                   '20%'],
                                      'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {31803009: {'reduce_factor': 0.2,'skill_ids': [803051, 803052, 803053, 803054]}}}}}}
                             },
       'survivalBattleCandidates': {4: {'num': 10
                                        },
                                    5: {'num': 10
                                        },
                                    6: {'num': 10
                                        },
                                    10004: {'num': 8,
                                            'candidates': [
                                                         1002, 2002, 2005, 3002, 3004, 4001, 4005, 5003, 5005]
                                            },
                                    10005: {'num': 8,
                                            'candidates': [
                                                         1002, 2002, 2005, 3002, 3004, 4001, 4005, 5003, 5005]
                                            },
                                    10006: {'num': 8,
                                            'candidates': [
                                                         1002, 2002, 2005, 3002, 3004, 4001, 4005, 5003, 5005]
                                            },
                                    20004: {'num': 8,
                                            'candidates': [
                                                         1002, 2002, 2005, 3002, 3004, 4001, 4005, 5003, 5005]
                                            },
                                    20005: {'num': 8,
                                            'candidates': [
                                                         1002, 2002, 2005, 3002, 3004, 4001, 4005, 5003, 5005]
                                            },
                                    20006: {'num': 8,
                                            'candidates': [
                                                         1002, 2002, 2005, 3002, 3004, 4001, 4005, 5003, 5005]
                                            },
                                    30004: {'num': 8,
                                            'candidates': [
                                                         1002, 2002, 2005, 3002, 3004, 4001, 4005, 5003, 5005]
                                            },
                                    30006: {'num': 8,
                                            'candidates': [
                                                         1002, 2002, 2005, 3002, 3004, 4001, 4005, 5003, 5005]
                                            },
                                    64: {'num': 10
                                         },
                                    74: {'num': 10
                                         },
                                    75: {'num': 10
                                         },
                                    90005: {'num': 10
                                            },
                                    90006: {'num': 10
                                            },
                                    11: {'num': 10
                                         },
                                    12: {'num': 10
                                         },
                                    13: {'num': 10
                                         },
                                    61: {'num': 10
                                         },
                                    62: {'num': 10
                                         },
                                    63: {'num': 10
                                         },
                                    71: {'num': 10
                                         },
                                    72: {'num': 10
                                         },
                                    73: {'num': 10
                                         },
                                    76: {'num': 10
                                         },
                                    81: {'num': 10
                                         },
                                    82: {'num': 10
                                         },
                                    83: {'num': 10
                                         },
                                    91: {'num': 10
                                         },
                                    92: {'num': 10
                                         },
                                    93: {'num': 10
                                         },
                                    90002: {'num': 10
                                            },
                                    90003: {'num': 10
                                            },
                                    131: {'num': 10
                                          },
                                    103: {'num': 10
                                          },
                                    104: {'num': 10
                                          },
                                    105: {'num': 10
                                          },
                                    141: {'num': 10
                                          },
                                    142: {'num': 10
                                          },
                                    143: {'num': 10
                                          },
                                    146: {'num': 10
                                          },
                                    147: {'num': 10
                                          },
                                    148: {'num': 10
                                          },
                                    90034: {'num': 10
                                            },
                                    90035: {'num': 10
                                            },
                                    189: {'num': 10
                                          },
                                    190: {'num': 10
                                          },
                                    191: {'num': 10
                                          },
                                    90009: {'num': 10
                                            },
                                    90010: {'num': 10
                                            },
                                    90011: {'num': 10
                                            },
                                    90012: {'num': 10
                                            },
                                    90013: {'num': 10
                                            },
                                    90014: {'num': 10
                                            },
                                    90015: {'num': 10
                                            },
                                    90016: {'num': 10
                                            },
                                    90017: {'num': 10
                                            },
                                    90018: {'num': 10
                                            },
                                    90019: {'num': 10
                                            },
                                    90020: {'num': 10
                                            },
                                    90021: {'num': 10
                                            },
                                    90022: {'num': 10
                                            },
                                    90023: {'num': 10
                                            },
                                    90024: {'num': 10
                                            }
                                    },
       'boxRefreshData': {1: {'interval': 20,
                              'num': 40
                              },
                          2: {'interval': 220,
                              'num': 30
                              },
                          3: {'interval': 240,
                              'num': 30
                              },
                          4: {'interval': 240,
                              'num': 20
                              }
                          },
       'deathGiftData': {101005: {'gift_id': 101005,
                                  'name_id': 17600,
                                  'icon_path': 'gui/ui_res_2/item/rogue/1005.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/1005_small.png',
                                  'desc_id': 17700,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 1,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 1,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '20%'],
                                  'gift_params': {'ON_ADD': {'mod_add_attr': {'eject_speed_factor': 0.2},'set_self_attr': {'iShowTailEffectOnMechaDie': 0}}}},
                         103003: {'gift_id': 103003,
                                  'name_id': 17601,
                                  'icon_path': 'gui/ui_res_2/item/rogue/3003.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/3003_small.png',
                                  'desc_id': 17701,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 3,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 2,
                                  'triggerState': 2,
                                  'desc_param': [
                                               '2', '10%'],
                                  'gift_params': {'ON_DO_TACTIC_SKILL': {'add_self_buff': {'add_buffs': {2001: {'fight_factor': 0.1,'extra_duration': 2}}}}}},
                         103004: {'gift_id': 103004,
                                  'name_id': 17602,
                                  'icon_path': 'gui/ui_res_2/item/rogue/3004.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/3004_small.png',
                                  'desc_id': 17702,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 3,
                                  'is_exclusive': False,
                                  'brand': 2,
                                  'target': 7,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '0.8%', 8],
                                  'gift_params': {'ON_MANUAL_HUMAN_DAMAGE_CALC': {'kill_player_add_fight_factor': {'add_ratio': 0.008,'max_layer_num': 8}},'ON_MANUAL_MECHA_DAMAGE_CALC': {'kill_player_add_fight_factor': {'add_ratio': 0.008,'max_layer_num': 8}}},'sequence': [
                                             1]
                                  },
                         103005: {'gift_id': 103005,
                                  'name_id': 17603,
                                  'icon_path': 'gui/ui_res_2/item/rogue/3005.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/3005_small.png',
                                  'desc_id': 17703,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 2,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 2,
                                  'triggerState': 2,
                                  'desc_param': [
                                               '0.8%', '1.5', '10'],
                                  'gift_params': {'ON_FIGHT': {'upgrade_main_weapon': {'add_buffs': {2013: {'rate': 0.8,'max_layer_num': 10,'extra_duration': 1.5}}}}}},
                         104002: {'gift_id': 104002,
                                  'name_id': 17604,
                                  'icon_path': 'gui/ui_res_2/item/rogue/4002.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/4002_small.png',
                                  'desc_id': 17704,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 1,
                                  'is_exclusive': False,
                                  'brand': 2,
                                  'target': 2,
                                  'triggerState': 2,
                                  'desc_param': [
                                               '3%', 3],
                                  'gift_params': {'ON_MECHA_STAY': {'add_self_buff': {'add_buffs': {2006: {'fight_factor': 0.03,'max_layer_num': 3}}}}}},
                         104005: {'gift_id': 104005,
                                  'name_id': 17605,
                                  'icon_path': 'gui/ui_res_2/item/rogue/4005.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/4005_small.png',
                                  'desc_id': 17705,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 2,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 2,
                                  'triggerState': 2,
                                  'desc_param': [
                                               '50%', '10%'],
                                  'gift_params': {'ON_MANUAL_MECHA_DAMAGE_CALC': {'mecha_add_damage_on_shoot': {'add_ratio': 0.1,'only_main_weapon': 1,'bullet_less_than': 0.5}}}},
                         105003: {'gift_id': 105003,
                                  'name_id': 17606,
                                  'icon_path': 'gui/ui_res_2/item/rogue/5003.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/5003_small.png',
                                  'desc_id': 17706,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 3,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 2,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '10%'],
                                  'gift_params': {'ON_KILL_MECHA': {'recover_mecha_hp': {'ratio': 0.1}}}},
                         105004: {'gift_id': 105004,
                                  'name_id': 17607,
                                  'icon_path': 'gui/ui_res_2/item/rogue/5004.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/5004_small.png',
                                  'desc_id': 17707,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 2,
                                  'is_exclusive': False,
                                  'brand': 2,
                                  'target': 2,
                                  'triggerState': 2,
                                  'desc_param': [
                                               '15%', '2'],
                                  'trigger_interval': 120,
                                  'gift_params': {'ON_HURT': {'full_mecha_shield': {'ratio': 0.15}}}},
                         106003: {'gift_id': 106003,
                                  'name_id': 17608,
                                  'icon_path': 'gui/ui_res_2/item/rogue/6003.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/6003_small.png',
                                  'desc_id': 17708,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 2,
                                  'is_exclusive': False,
                                  'brand': 1,
                                  'target': 10,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '30', '20%'],
                                  'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {538: {'power_ratio': 0.2}}}}}},
                         106004: {'gift_id': 106004,
                                  'name_id': 17609,
                                  'icon_path': 'gui/ui_res_2/item/rogue/6004.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/6004_small.png',
                                  'desc_id': 17709,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 1,
                                  'is_exclusive': False,
                                  'brand': 1,
                                  'target': 10,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '0', '15%', '20%'],
                                  'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {540: {'power_factor': 0.2}}}}}},
                         106005: {'gift_id': 106005,
                                  'name_id': 17610,
                                  'icon_path': 'gui/ui_res_2/item/rogue/6005.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/6005_small.png',
                                  'desc_id': 17710,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 2,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 10,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '5%'],
                                  'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {536: {'spd_type': 'base','spd_val': 0.05,'power_ratio': 0.05,'def_ratio': 0.05}}}}},'sequence': [
                                             1]
                                  },
                         106006: {'gift_id': 106006,
                                  'name_id': 17611,
                                  'icon_path': 'gui/ui_res_2/item/rogue/6006.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/6006_small.png',
                                  'desc_id': 17711,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 1,
                                  'is_exclusive': False,
                                  'brand': 1,
                                  'target': 1,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '200'],
                                  'gift_params': {'ON_JOIN_MECHA': {'add_self_buff': {'add_buffs': {2009: {'radius': 200,'detect_num': 5,'extra_duration': 6,'show_self': 1}}}}}},
                         100003: {'gift_id': 100003,
                                  'name_id': 17612,
                                  'icon_path': 'gui/ui_res_2/item/rogue/0003.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/0003_small.png',
                                  'desc_id': 17712,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 2,
                                  'is_exclusive': False,
                                  'brand': 2,
                                  'target': 1,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '20%', '15%'],
                                  'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2016: {'blood_packet_cd_add': 0.15,'cure_factor': 0.2,'replicate_data': {'blood_packet_cd_add': 0.15,'cure_factor': 0.2}}}}}}},
                         104001: {'gift_id': 104001,
                                  'name_id': 17613,
                                  'icon_path': 'gui/ui_res_2/item/rogue/4001.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/4001_small.png',
                                  'desc_id': 17713,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 2,
                                  'is_exclusive': False,
                                  'brand': 2,
                                  'target': 1,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '7%', '7'],
                                  'gift_params': {'ACE_DOUBLE': {'add_acetime_buff': {'add_buffs': {2017: {'base_power_factor': 0.07,'skill_recover_factor': -0.07,'replicate_data': {'base_power_factor': 0.07,'skill_recover_factor': -0.07}}}}}},'sequence': [
                                             2]
                                  },
                         101002: {'gift_id': 101002,
                                  'name_id': 17614,
                                  'icon_path': 'gui/ui_res_2/item/rogue/1002.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/1002_small.png',
                                  'desc_id': 17714,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 1,
                                  'is_exclusive': False,
                                  'brand': 1,
                                  'target': 1,
                                  'triggerState': 15,
                                  'gift_params': {'ON_ADD': {'launch_items': {9940: 1}}},'sequence': [
                                             2]
                                  },
                         105002: {'gift_id': 105002,
                                  'name_id': 17615,
                                  'icon_path': 'gui/ui_res_2/item/rogue/5002.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/5002_small.png',
                                  'desc_id': 17715,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 3,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 10,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '15', '10'],
                                  'gift_params': {'ON_KILL': {'kill_mod_add_attr': {'max_hp_add': 15,'max_layer_num': 10}},'ON_ADD': {'kill_mod_add_attr': {'max_hp_add': 15,'max_layer_num': 10}}},'sequence': [
                                             1]
                                  },
                         100004: {'gift_id': 100004,
                                  'name_id': 17616,
                                  'icon_path': 'gui/ui_res_2/item/rogue/0004.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/0004_small.png',
                                  'desc_id': 17716,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 3,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 1,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '15%'],
                                  'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2018: {'super_jump_vspeed_add': 0.15,'replicate_data': {'super_jump_vspeed_add': 0.15}}}}}}},
                         103001: {'gift_id': 103001,
                                  'name_id': 17618,
                                  'icon_path': 'gui/ui_res_2/item/rogue/3001.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/3001_small.png',
                                  'desc_id': 17718,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 3,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 1,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '5', '5%'],
                                  'gift_params': {'ON_KILL': {'add_self_buff': {'add_buffs': {2019: {'base_power_factor': 0.05,'extra_duration': 5,'replicate_data': {'base_power_factor': 0.05}}}}}}},
                         100002: {'gift_id': 100002,
                                  'name_id': 17619,
                                  'icon_path': 'gui/ui_res_2/item/rogue/0002.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/0002_small.png',
                                  'desc_id': 17719,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 1,
                                  'is_exclusive': False,
                                  'brand': 1,
                                  'target': 10,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '10%'],
                                  'gift_params': {'ON_ADD': {'mod_add_attr': {'mecha_fuel_recover_factor': 0.1,'max_fuel_factor': 0.1}}}},
                         104004: {'gift_id': 104004,
                                  'name_id': 17620,
                                  'icon_path': 'gui/ui_res_2/item/rogue/4004.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/4004_small.png',
                                  'desc_id': 17720,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 2,
                                  'is_exclusive': False,
                                  'brand': 2,
                                  'target': 10,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '5%'],
                                  'gift_params': {'ON_ADD': {'mod_add_attr': {'vampire_factor_pos_1': 0.05}}}},
                         105001: {'gift_id': 105001,
                                  'name_id': 17621,
                                  'icon_path': 'gui/ui_res_2/item/rogue/5001.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/5001_small.png',
                                  'desc_id': 17721,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 1,
                                  'is_exclusive': False,
                                  'brand': 1,
                                  'target': 10,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '15', '300', '4'],
                                  'trigger_interval': 60,
                                  'gift_params': {'ON_JOIN_MECHA': {'add_shield_on_join_mecha': {'buff_id': 2020,'extra_duration': 4,'shield_per_enemy': 300,'radius': 15}}}},
                         103002: {'gift_id': 103002,
                                  'name_id': 17622,
                                  'icon_path': 'gui/ui_res_2/item/rogue/3002.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/3002_small.png',
                                  'desc_id': 17722,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 3,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 1,
                                  'triggerState': 1,
                                  'desc_param': [
                                               '12', '500', '60'],
                                  'gift_params': {'ON_MECHA_DIE': {'gen_explosion': {'radius': 12,'explosion_dmg': 500}}}},
                         107001: {'gift_id': 107001,
                                  'name_id': 17645,
                                  'icon_path': 'gui/ui_res_2/item/rogue/7002.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/7002_small.png',
                                  'desc_id': 17752,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 3,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 1,
                                  'triggerState': 15,
                                  'gift_params': {'ON_KILL_MECHA': {'modify_item_use_cd': {'alter_ids': {1613: 0}}},'ON_KILL_HUMAN': {'modify_item_use_cd': {'alter_ids': {1613: 0}}}}},
                         107002: {'gift_id': 107002,
                                  'name_id': 17646,
                                  'icon_path': 'gui/ui_res_2/item/rogue/7001.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/7001_small.png',
                                  'desc_id': 17753,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 3,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 1,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '30%'],
                                  'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2049: {'reduce_factor': 0.3}}}}}},
                         107003: {'gift_id': 107003,
                                  'name_id': 17647,
                                  'icon_path': 'gui/ui_res_2/item/rogue/7003.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/7003_small.png',
                                  'desc_id': 17754,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 1,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 10,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '5', '8%'],
                                  'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2050: {'ratio': 0.08,'activate_duration': 5}}}}}},
                         107004: {'gift_id': 107004,
                                  'name_id': 17652,
                                  'icon_path': 'gui/ui_res_2/item/rogue/7006.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/7006_small.png',
                                  'desc_id': 17759,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 3,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 2,
                                  'triggerState': 2,
                                  'desc_param': [
                                               '30%', '20%', '2'],
                                  'gift_params': {'ON_FIGHT': {'add_target_mecha_low_hp_buff': {'hp_threshold': 0.3,'add_buffs': {2057: {'spd_type': 'base','spd_val': 0.2}}}}}},
                         107005: {'gift_id': 107005,
                                  'name_id': 17653,
                                  'icon_path': 'gui/ui_res_2/item/rogue/7005.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/7005_small.png',
                                  'desc_id': 17760,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 2,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 2,
                                  'triggerState': 2,
                                  'desc_param': [
                                               '30', '100'],
                                  'gift_params': {'ON_KILL_MECHA': {'kill_mecha_heal': {'dist': 360,'shield': 100}}}},
                         107006: {'gift_id': 107006,
                                  'name_id': 17654,
                                  'icon_path': 'gui/ui_res_2/item/rogue/7004.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/7004_small.png',
                                  'desc_id': 17761,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 1,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 10,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '50%'],
                                  'gift_params': {'ON_ADD': {'add_self_buff': {'add_buffs': {2059: {'jump_bf_data': {'add_factor': 0.25}}}}}}},
                         107007: {'gift_id': 107007,
                                  'name_id': 17655,
                                  'icon_path': 'gui/ui_res_2/item/rogue/7010.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/7010_small.png',
                                  'desc_id': 17765,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 2,
                                  'is_exclusive': False,
                                  'brand': 3,
                                  'target': 1,
                                  'triggerState': 2,
                                  'desc_param': [
                                               '2'],
                                  'gift_params': {'ON_KILL_MECHA': {'kill_mecha_gen_detecter': {'duration': 2}}}},
                         107008: {'gift_id': 107008,
                                  'name_id': 17656,
                                  'icon_path': 'gui/ui_res_2/item/rogue/7007.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/7007_small.png',
                                  'desc_id': 17764,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 1,
                                  'is_exclusive': False,
                                  'brand': 1,
                                  'target': 10,
                                  'triggerState': 15,
                                  'desc_param': [
                                               '50%', '5'],
                                  'gift_params': {'ON_JOIN_MECHA': {'add_self_buff': {'add_buffs': {2061: {'spd_val': 1.5,'spd_type': 'base','speed_decay': 0.1}}}}}},
                         107009: {'gift_id': 107009,
                                  'name_id': 17657,
                                  'icon_path': 'gui/ui_res_2/item/rogue/7009.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/7009_small.png',
                                  'desc_id': 17763,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 3,
                                  'is_exclusive': False,
                                  'brand': 2,
                                  'target': 2,
                                  'triggerState': 2,
                                  'desc_param': [
                                               '15%', '25%', '3', '60'],
                                  'trigger_interval': 60,
                                  'gift_params': {'ON_HURT': {'low_hp_vampire': {'ratio': 0.15,'vampire_factor': 0.25,'duration': 3}}}},
                         107010: {'gift_id': 107010,
                                  'name_id': 17658,
                                  'icon_path': 'gui/ui_res_2/item/rogue/7008.png',
                                  'small_icon_path': 'gui/ui_res_2/item/rogue/7008_small.png',
                                  'desc_id': 17762,
                                  'is_open': 1,
                                  'is_survival': False,
                                  'is_death': True,
                                  'quality': 2,
                                  'is_exclusive': False,
                                  'brand': 2,
                                  'target': 2,
                                  'triggerState': 2,
                                  'desc_param': [
                                               '100', '8%', '3'],
                                  'gift_params': {'ON_FIGHT': {'far_dist_hit_buff': {'dist': 100,'buffs': {2064: {'fight_factor': 0.08,'duration': 3}}}}}}
                         }
       }
import six
from six.moves import range
ON_ADD = 'ON_ADD'
ON_DO_TACTIC_SKILL = 'ON_DO_TACTIC_SKILL'
ON_KILL_MECHA = 'ON_KILL_MECHA'
ON_OPEN_BOX = 'ON_OPEN_BOX'
ON_MECHA_DIE = 'ON_MECHA_DIE'
ON_FIRE = 'ON_FIRE'
ON_KILL_HUMAN = 'ON_KILL_HUMAN'
ON_FIGHT = 'ON_FIGHT'
ON_MECHA_STAY = 'ON_MECHA_STAY'
ON_HURT = 'ON_HURT'
ON_PICK_ITEM = 'ON_PICK_ITEM'
ON_CURE = 'ON_CURE'
ON_JOIN_MECHA = 'ON_JOIN_MECHA'
ON_MANUAL_HUMAN_DAMAGE_CALC = 'ON_MANUAL_HUMAN_DAMAGE_CALC'
ON_MANUAL_MECHA_DAMAGE_CALC = 'ON_MANUAL_MECHA_DAMAGE_CALC'
ACE_DOUBLE = 'ACE_DOUBLE'
ON_PICK_ACE_STAR = 'ON_PICK_ACE_STAR'
ON_KILL = 'ON_KILL'
NO_HANDLER_TRIGGER_TYPES = [ON_MECHA_STAY]
ROGUE_GIFT_TRIGGER_STATE_HUMAN = 1
ROGUE_GIFT_TRIGGER_STATE_MECHA = 2
ROGUE_GIFT_TRIGGER_STATE_VEHICLE_MECHA = 4
ROGUE_GIFT_TRIGGER_STATE_ALL = 15
ROGUE_GIFT_TARGET_HUMAN = 1
ROGUE_GIFT_TARGET_MECHA = 2
ROGUE_GIFT_TARGET_VEHICLE_MECHA = 4
ROGUE_GIFT_TARGET_CREATE_MECHA = 8
ROGUE_GIFT_TARGET_FRONT = 7
ROGUE_GIFT_TARGET_ALL = 15
BATTLE_INIT_GIFT_SET_SIZE = 15
ROGUE_BOX_CANDIDATE_GIFT_NUM = 3
ROGUE_BOX_RANDOM_TOP_GIFTS_CANDIDATE_NUM = 5
ROGUE_PLAYER_CAN_HOLD_MAX_GIFT_NUM = 3
ROGUE_GIFT_MECHA_STAY_STILL_ADD_FIGHT_FACTOR = 4002
ROGUE_GIFT_MECHA_STAY_STILL_ADD_BUFF_ID = 2006
ROGUE_BOX_MAX_HOLD_TIME = 180
ROGUE_GIFT_RANDOM_ONE_GIFT = 1004
ROGUE_BOX_REFRESH_TIP_ADVANCE_TIME = 5
ROGUE_GIFT_ADD_MECHA_HP_BY_ACE_STAR = 5001
import random
from collections import defaultdict
trigger_type_2_gift_ids = {}
wave_candidates = defaultdict(dict)
data['allGiftData'] = {}
data['allGiftData'].update(data['survivalGiftData'])
data['allGiftData'].update(data['deathGiftData'])
data['allGiftData'].update(data['exclusiveGiftData'])
data['allBattleCandidates'] = {}
data['allBattleCandidates'].update(data['survivalBattleCandidates'])
data['allBattleCandidates'].update(data['deathBattleCandidates'])

def get_gift_data():
    return data['allGiftData']


def get_exclusive_gift_data():
    return data['exclusiveGiftData']


def get_death_gift_data():
    return data['deathGiftData']


def get_survival_gift_data():
    return data['survivalGiftData']


def get_box_refresh_data():
    return data['boxRefreshData']


def get_all_battle_candidates_data():
    return data['allBattleCandidates']


def get_all_survival_battle_candidates_data():
    return data['survivalBattleCandidates']


def get_all_death_battle_candidates_data():
    return data['deathBattleCandidates']


def is_gift_opened(gift_id):
    open_status = get_gift_data().get(gift_id, {}).get('is_open', 0)
    return open_status > 0


def get_gift_exclusive_mecha_id(gift_id):
    gift_data = get_exclusive_gift_data().get(gift_id)
    if not gift_data:
        return None
    else:
        return gift_data.get('mecha_id', None)


def get_all_opened_gifts():
    return [ gift_id for gift_id, gift_conf in six.iteritems(get_gift_data()) if is_gift_opened(gift_id) ]


def get_survival_opened_gifts():
    return [ gift_id for gift_id, gift_conf in six.iteritems(get_survival_gift_data()) if is_gift_opened(gift_id) ]


def preprocess_all_gift():
    global trigger_type_2_gift_ids
    trigger_type_2_gift_ids = {}
    for gift_id, gift_conf in six.iteritems(get_gift_data()):
        for trigger_type, trigger_params in six.iteritems(gift_conf['gift_params']):
            trigger_type_2_gift_ids.setdefault(trigger_type, set())
            trigger_type_2_gift_ids[trigger_type].add(gift_id)


def get_rogue_gift_handler_name_set():
    handler_name_set = set()
    for gift_id, gift_data in six.iteritems(get_gift_data()):
        effect_params = gift_data.get('gift_params', {})
        for trigger_type, trigger_params in six.iteritems(effect_params):
            if trigger_type in NO_HANDLER_TRIGGER_TYPES:
                continue
            handler_name_set.update(six.iterkeys(trigger_params))

    return handler_name_set


def has_gift(gift_id):
    return gift_id in six.iterkeys(get_gift_data())


def get_gift_effect_params(gift_id, trigger_type):
    return get_gift_data().get(gift_id, {}).get('gift_params', {}).get(trigger_type, {})


def get_gift_trigger_interval(gift_id):
    return get_gift_data().get(gift_id, {}).get('trigger_interval', 0)


def get_gifts_of_trigger_type(trigger_type):
    return trigger_type_2_gift_ids.get(trigger_type, set())


def get_gift_trigger_types(gift_id):
    gift_params = get_gift_data().get(gift_id, {}).get('gift_params', {})
    return six.iterkeys(gift_params)


def get_battle_gift_candidates_data(battle_type):
    return get_all_battle_candidates_data().get(battle_type, {})


def get_survival_battle_gift_candidates_data(battle_type):
    return get_all_survival_battle_candidates_data().get(battle_type, {})


def get_waved_death_battle_gift_candidates_data(battle_type):
    total_candidates = get_all_death_battle_candidates_data().get(battle_type, {})
    if battle_type in wave_candidates:
        return {'candidates': wave_candidates[battle_type],'exclusiveCandidates': total_candidates.get('exclusiveCandidates', [])}
    else:
        wave_candidates[battle_type] = tmp_wave_candidates = defaultdict(list)
        normal_gifts = total_candidates.get('candidates', [])
        for gift_id in normal_gifts:
            sequence = get_gift_data().get(gift_id, {}).get('sequence', [])
            if not sequence:
                tmp_wave_candidates[-1].append(gift_id)
            else:
                for seq in sequence:
                    seq > 0 and tmp_wave_candidates[seq - 1].append(gift_id)

        return {'candidates': tmp_wave_candidates,'exclusiveCandidates': total_candidates.get('exclusiveCandidates', [])}


def get_death_battle_gift_candidates_data(battle_type):
    return get_all_death_battle_candidates_data().get(battle_type, {})


def gen_survival_battle_init_gift_id_set(battle_type):
    battle_data = get_survival_battle_gift_candidates_data(battle_type)
    if not battle_data:
        return set()
    candidates = battle_data.get('candidates', [])
    if not candidates:
        candidates = get_survival_opened_gifts()
    else:
        candidates = [ gift_id for gift_id in candidates if is_gift_opened(gift_id) ]
    select_num = battle_data.get('num', 0)
    if len(candidates) < ROGUE_PLAYER_CAN_HOLD_MAX_GIFT_NUM or select_num < ROGUE_PLAYER_CAN_HOLD_MAX_GIFT_NUM:
        log_error('gen_survival_battle_init_gift_id_set invalid battle_type=%s, select_num=%s, candidates=%s', battle_type, select_num, candidates)
        return set()
    max_num = select_num if len(candidates) >= select_num else len(candidates)
    return set(random.sample(candidates, max_num))


def gen_random_gift_list(gift_set):
    max_num = ROGUE_BOX_CANDIDATE_GIFT_NUM if len(gift_set) >= ROGUE_BOX_CANDIDATE_GIFT_NUM else len(gift_set)
    selected_gifts = random.sample(gift_set, max_num)
    if not selected_gifts or len(selected_gifts) < ROGUE_BOX_CANDIDATE_GIFT_NUM:
        log_error('gen_random_gift_list selected_gifts: %s not enough, gift_set:%s', selected_gifts, gift_set)
    return selected_gifts


def random_one_gift--- This code section failed: ---

2072       0  BUILD_LIST_0          0 
           3  LOAD_FAST             0  'candidates'
           6  GET_ITER         
           7  FOR_ITER             24  'to 34'
          10  STORE_FAST            2  'gift_id'
          13  LOAD_FAST             2  'gift_id'
          16  LOAD_FAST             1  'exclude_gifts'
          19  COMPARE_OP            7  'not-in'
          22  POP_JUMP_IF_FALSE     7  'to 7'
          25  LOAD_FAST             2  'gift_id'
          28  LIST_APPEND           2  ''
          31  JUMP_BACK             7  'to 7'
          34  STORE_FAST            0  'candidates'

2073      37  LOAD_FAST             0  'candidates'
          40  POP_JUMP_IF_TRUE     47  'to 47'

2074      43  LOAD_CONST            0  ''
          46  RETURN_END_IF    
        47_0  COME_FROM                '40'

2075      47  LOAD_GLOBAL           1  'random'
          50  LOAD_ATTR             2  'sample'
          53  LOAD_ATTR             1  'random'
          56  CALL_FUNCTION_2       2 
          59  STORE_FAST            3  'selected_gifts'

2076      62  LOAD_FAST             3  'selected_gifts'
          65  LOAD_CONST            2  ''
          68  BINARY_SUBSCR    
          69  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 56


def get_gift_quality(gift_id):
    return get_gift_data().get(gift_id).get('quality', 1)


def get_gift_name_text_id(gift_id):
    return get_gift_data().get(gift_id, {}).get('name_id', None)


def get_gift_desc_text_id(gift_id):
    return get_gift_data().get(gift_id, {}).get('desc_id', None)


def get_gift_desc_params(gift_id):
    return get_gift_data().get(gift_id, {}).get('desc_param', [])


def get_gift_trigger_state(gift_id):
    return get_gift_data().get(gift_id, {}).get('triggerState', 0)


def get_gift_effect_target(gift_id):
    return get_gift_data().get(gift_id, {}).get('target', 0)


def get_gift_brand(gift_id):
    return get_gift_data().get(gift_id, {}).get('brand', 0)


def get_gift_icon_path(gift_id, big=False):
    if big:
        return get_gift_data().get(gift_id, {}).get('icon_path', '')
    else:
        return get_gift_data().get(gift_id, {}).get('small_icon_path', '')


def get_mecha_stay_still_buff_max_lay_num():
    trigger_params = get_gift_effect_params(ROGUE_GIFT_MECHA_STAY_STILL_ADD_FIGHT_FACTOR, ON_MECHA_STAY)
    buff_params = trigger_params.get('add_self_buff', {})
    for buff_id, buff_data in six.iteritems(buff_params.get('add_buffs', {})):
        if buff_data.get('max_layer_num', 0) > 0:
            return buff_data.get('max_layer_num', 0)

    return 0


def check_survival_battle_candidates_config():
    for battle_type in get_all_survival_battle_candidates_data():
        gen_survival_battle_init_gift_id_set(battle_type)


def match_exclusive(gift_id, mecha_id):
    gift = get_exclusive_gift_data().get(gift_id, {})
    if not gift.get('is_exclusive'):
        return True
    if gift.get('mecha_id') == mecha_id:
        return True
    return False


def get_gift_weight(gift_id):
    quality = get_gift_quality(gift_id)
    return data['giftWeight'].get(quality, 1)


def cal_gift_weights(gifts):
    total_weight = 0
    for gift in gifts:
        total_weight += get_gift_weight(gift)

    return total_weight


def gen_death_gift_candidate(pre_candidates, total_death, total_exclusive, normal_len, exclusive_len, mix_len):
    total_pre = set()
    for key, candidates in six.iteritems(pre_candidates):
        total_pre.update(candidates)

    total_death_pure = []
    for death_gift in total_death:
        if death_gift not in total_pre:
            total_death_pure.append(death_gift)

    total_exclusive_pure = []
    for exclusive_gift in total_exclusive:
        if exclusive_gift not in total_pre:
            total_exclusive_pure.append(exclusive_gift)

    target_candidate = []
    target_candidate += sample_weight_gift(total_death_pure, normal_len)
    if len(target_candidate) != normal_len:
        log_error('gen_death_battle_death_gift_invalid pre_candidates=%s, total_death=%s, total_exclusive=%s', pre_candidates, total_death, total_exclusive)
    target_candidate += sample_weight_gift(total_exclusive_pure, exclusive_len)
    if len(target_candidate) != normal_len + exclusive_len:
        log_error('gen_death_battle_exclusive_gift_invalid: pre_candidates=%s, total_death=%s, total_exclusive=%s', pre_candidates, total_death, total_exclusive)
    total_pure = total_death_pure + total_exclusive_pure
    target_candidate += sample_weight_gift(total_pure, mix_len)
    if len(target_candidate) != normal_len + exclusive_len + mix_len:
        log_error('gen_death_battle_death_gift_invalid pre_candidates=%s, total_death=%s, total_exclusive=%s', pre_candidates, total_death, total_exclusive)
    return target_candidate


def sample_weight_gift(total_gifts, count):
    gift_len = len(total_gifts)
    if not total_gifts or gift_len < count:
        return []
    total_weight = cal_gift_weights(total_gifts)
    candidate = []
    for i in range(count):
        target_weight = random.randint(1, total_weight)
        weight_sum = 0
        t = 0
        while weight_sum < target_weight:
            weight_sum += get_gift_weight(total_gifts[t])
            t += 1

        if t > len(total_gifts):
            log_error('sample gift error: no gift left to choose')
        new_gift = total_gifts[t - 1]
        candidate.append(new_gift)
        total_gifts.remove(new_gift)
        total_weight -= get_gift_weight(new_gift)

    return candidate


def get_gift_quality_bg(gift_id):
    gift_quality = get_gift_quality(gift_id)
    return ROGUE_GIFT_BGS.get(gift_quality, DEFAULT_BG)


check_survival_battle_candidates_config()
ROGUE_GIFT_BGS = {1: 'gui/ui_res_2/battle_tdm/rogue/pnl_battle_tdm_rogue_item_blue.png',
   2: 'gui/ui_res_2/battle_tdm/rogue/pnl_battle_tdm_rogue_item_purple.png',
   3: 'gui/ui_res_2/battle_tdm/rogue/pnl_battle_tdm_rogue_item_yellow.png'
   }
DEFAULT_BG = 'gui/ui_res_2/battle_tdm/rogue/pnl_battle_tdm_rogue_item_blue.png'