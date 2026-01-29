# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/client_unit_tag_utils.py
from __future__ import absolute_import
from logic.gcommon.common_utils.unit_tag_utils import unit_tag_mgr, preregistered_tags
NEED_TAG_UNIT_NAME_LIST = [
 'LAvatar',
 'LPuppet',
 'LPuppetRobot',
 'LMecha',
 'LMechaRobot',
 'LMechaTrans',
 'LMotorcycle',
 'LSeat',
 'LMonster',
 'LPhotonTower',
 'LLightShield',
 'LSkillWall',
 'LDeathDoor',
 'LExplosiveRobot',
 'LRatRobot',
 'LCrystal',
 'LIgniteGrenade',
 'LTriggerGrenade',
 'LParadropBall',
 'LHouse',
 'LField',
 'LHPBreakable',
 'LAttachable',
 'LExerciseTarget',
 'LParadrop',
 'LSnowman',
 'LBuilding',
 'LPveRandomBox',
 'LPvePuzzle',
 'LNeutralShop',
 'LMeowPostbox',
 'LConcertArena',
 'LSimplePortal',
 'LRocketGravitySwitch',
 'LArtTestMecha',
 'LFishHeadTarget',
 'LHittableBox',
 'LSphereShield',
 'LPvePortal',
 'LPveBox',
 'LPveShop',
 'LTrackMissile',
 'LPet']
UNIT_NAME_TO_MASK_MAP = {}
for index, unit_name in enumerate(NEED_TAG_UNIT_NAME_LIST):
    mask = 1 << index
    UNIT_NAME_TO_MASK_MAP[unit_name] = mask
    mod = __import__('logic.units', globals(), locals(), [unit_name])
    mod = getattr(mod, unit_name, None)
    unit_class = getattr(mod, unit_name, None)
    if unit_class:
        unit_class.MASK = mask

unit_tag_mgr.refresh_unit_name_to_mask_map(UNIT_NAME_TO_MASK_MAP)
register_unit_tag = unit_tag_mgr.register_unit_tag
preregistered_tags.HUMAN_TAG_VALUE = register_unit_tag(('LAvatar', 'LPuppet', 'LPuppetRobot'))
preregistered_tags.MECHA_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaRobot'))
preregistered_tags.VEHICLE_TAG_VALUE = register_unit_tag(('LMechaTrans', 'LMotorcycle'))
preregistered_tags.MECHA_VEHICLE_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaRobot',
                                                                'LMechaTrans', 'LMotorcycle'))
preregistered_tags.IGNORE_SOCKET_CHECK_TAG_VALUE = register_unit_tag(('LPhotonTower',
                                                                      'LLightShield',
                                                                      'LDeathDoor',
                                                                      'LExplosiveRobot',
                                                                      'LRatRobot',
                                                                      'LCrystal',
                                                                      'LSkillWall'))
preregistered_tags.TEAMMATE_SHOOT_UNIT_TAG_VALUE = register_unit_tag(('LSphereShield', ))
preregistered_tags.MONSTER_TAG_VALUE = register_unit_tag('LMonster')
preregistered_tags.PET_TAG_VALUE = register_unit_tag('LPet')