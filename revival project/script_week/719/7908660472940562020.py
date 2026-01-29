# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/__init__.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
import time
FRAME_DUR = 0.02

def register_entities(finish_cb=None):
    from mobile.client.ClientEntity import ClientEntity
    from mobile.common.EntityScanner import _get_class_list
    from mobile.common.EntityFactory import EntityFactory
    from mobile.common.RpcIndex import RpcIndexer, CLIENT_SALT
    reg_entity = ('Avatar', 'CharacterSelect', 'ClientAccount', 'Lobby', 'BaseClientAvatar',
                  'Battle', 'PointsBattle', 'ControlBattle', 'OccupyBattle', 'SurvivalBattle',
                  'BlankBattle', 'NightSurvivalBattle', 'SnowSurvivalBattle', 'NeutralShopSurvivalBattle',
                  'HumanSurvivalBattle', 'FastSurvivalBattle', 'MagicSurvivalBattle',
                  'KingBattle', 'DeathBattle', 'HumanDeathBattle', 'FFABattle', 'GvgBattle',
                  'LocalBattle', 'ExerciseBattle', 'SnipeBattle', 'GranbelmSurvivalBattle',
                  'GranhackSurvivalBattle', 'CloneBattle', 'ImproviseBattle', 'MechaDeathBattle',
                  'ZombieFFABattle', 'ArmRaceBattle', 'RandomDeathBattle', 'QTELocalBattleServer',
                  'QTELocalBattle', 'NewbieThirdLocalBattleServer', 'NewbieThirdLocalBattle',
                  'NewbieFourLocalBattleServer', 'NewbieFourLocalBattle', 'ConcertBattle',
                  'GravitySurvivalBattle', 'HuntingBattle', 'FireSurvivalBattle',
                  'Puppet', 'Breakable', 'BreakableAggregation', 'NPC', 'Plane',
                  'Item', 'House', 'Grenade', 'Barrage', 'TrackMissile', 'ShockWave',
                  'SwordLight', 'NavigateSwordLight', 'TowerBullet', 'PhotonTowerShield',
                  'MulitPartGrenade', 'ClusterGrenade', 'RainGrenade', 'Building',
                  'BattleReplay', 'Drone', 'Console', 'Paradrop', 'NightmareBox',
                  'ParadropPlane', 'Airship', 'Field', 'FogField', 'Hiding', 'Attachable',
                  'Mecha', 'TrackBullet', 'NavigateBullet', 'TrackNavigateBullet',
                  'RadialGrenade', 'AttachableRadialGrenade', 'InfiniteRadialGrenade',
                  'CommonRadialGrenade', 'ShiranuiFanGrenade', 'FlyingAttachGrenade',
                  'NavigateExtraTriggerExplodeGrenade', 'TrackNavigateExtraTriggerExplodeGrenade',
                  'ExtraTriggerExplodeGrenade', 'ClawGrenade', 'MechaBody', 'MechaTrans',
                  'DynamicBox', 'ExplosiveRobot', 'RatRobot', 'HPBreakable', 'Charger',
                  'Monster', 'ControlPoint', 'KingPoint', 'ConvoluteBird', 'Shop',
                  'NeutralShop', 'BeaconTower', 'PhotonTower', 'LightShield', 'Lift',
                  'LobbyNPC', 'LobbyPuppet', 'OilBottle', 'OilBottleBullet', 'DeathDoor',
                  'Fire', 'SceneSpray', 'Television', 'Icewall', 'SkillWall', 'Snowman',
                  'ExerciseTarget', 'GranbelmPortal', 'SummerSurvivalBattle', 'ParadropBall',
                  'RogueBox', 'Billboard', 'GodCamera', 'MeowPostbox', 'Motorcycle',
                  'Seat', 'ConcertArena', 'DebugNPC', 'FlagBattle', 'CrownBattle',
                  'SimplePortal', 'Train', 'TrainCarriage', 'BountySurvivalBattle',
                  'FlagBuilding', 'FlagBaseBuilding', 'RecruitmentSurvivalBattle',
                  'TrainStation', 'TriggerGrenade', 'TriggerMine', 'IgniteGrenade',
                  'CrystalBattle', 'Crystal', 'CrystalCover', 'CrystalBuff', 'ScavengeBattle',
                  'MPLobby', 'ADCrystalBattle', 'TrainBattle', 'Phantom', 'FishHeadTarget',
                  'HittableBox', 'Flag2Battle', 'Flag2Building', 'Flag2BaseBuilding',
                  'SnatchEggBattle', 'Goldenegg', 'TVMissile', 'TVMissileLauncher',
                  'DuelBattle', 'Beacon8031', 'GooseBearBattle', 'Pet', 'SphereShield',
                  'ShockField', 'ShockWarning', 'GulagSurvivalBattle', 'TrainBattle',
                  'PveEditBattle', 'PveRandomBox', 'PvePuzzle', 'SpotSfxPlayer',
                  'SpotSoundPlayer', 'PvePortal', 'PveDynamicDoor', 'PveBox', 'PveShop',
                  'AssaultBattle', 'PveShop', 'NBombDevice', 'NBombCore', 'NBombSurvivalBattle',
                  'RocketGravitySwitch', 'SkillWallField')
    class_dict = {'ClientEntity': ClientEntity}

    def reg_callback():
        entity_factory = EntityFactory.instance()
        for e_type, cla_z in six.iteritems(class_dict):
            entity_factory.register_entity(e_type, cla_z)

        not RpcIndexer.is_recv_indexed() and RpcIndexer.set_recv_rpc_salt(CLIENT_SALT)
        if finish_cb and callable(finish_cb):
            finish_cb()

    b_time = time.time()
    for idx in range(len(reg_entity)):
        member_name = reg_entity[idx]
        mod = __import__('logic.entities.' + member_name, globals(), locals(), fromlist=[''])
        cls = _get_class_list(mod, ClientEntity)
        if hasattr(mod, 'post_meta_class_generator'):
            for gen_ret in mod.post_meta_class_generator():
                yield False
                b_time = time.time()

        for cla_z in cls:
            class_dict[cla_z.__name__] = cla_z

        if time.time() - b_time > FRAME_DUR:
            yield False
            b_time = time.time()

    reg_callback()
    print('entity register finished')
    yield True