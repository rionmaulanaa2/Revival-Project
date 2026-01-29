# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/PlatformAPI/Platforms/Messiah/Globals.py
import MConfig
PLATFORM = (
 MConfig.Platform, MConfig.IsBit64, MConfig.Architecture)
RES_TYPE_NONE = 0
RES_TYPE_DATA = 1
RES_TYPE_SHADER = 2
RES_TYPE_MESH = 3
RES_TYPE_SKIN = 4
RES_TYPE_TEXTURE = 5
RES_TYPE_ANIMATION = 6
RES_TYPE_SOUND = 7
RES_TYPE_MATERIAL = 8
RES_TYPE_SKELETON = 9
RES_TYPE_MODEL = 10
RES_TYPE_CHARACTER = 11
RES_TYPE_PARTICLE = 12
RES_TYPE_TERRAIN = 13
RES_TYPE_NAVIGATE_MAP = 14
RES_TYPE_COLLISION_SHAPE = 15
RES_TYPE_POINT_CLOUD = 16
RES_TYPE_LEVEL = 17
RES_TYPE_WORLD = 18
RES_TYPE_STRING_TABLE = {RES_TYPE_NONE: 'None',
   RES_TYPE_DATA: 'Data',
   RES_TYPE_SHADER: 'Shader',
   RES_TYPE_MESH: 'Mesh',
   RES_TYPE_SKIN: 'Skin',
   RES_TYPE_TEXTURE: 'Texture',
   RES_TYPE_ANIMATION: 'Animation',
   RES_TYPE_SOUND: 'Sound',
   RES_TYPE_MATERIAL: 'Material',
   RES_TYPE_SKELETON: 'Skeleton',
   RES_TYPE_MODEL: 'Model',
   RES_TYPE_CHARACTER: 'Character',
   RES_TYPE_PARTICLE: 'ParticleSystem',
   RES_TYPE_TERRAIN: 'Terrain',
   RES_TYPE_NAVIGATE_MAP: 'NavigateMap',
   RES_TYPE_COLLISION_SHAPE: 'CollisionShape',
   RES_TYPE_POINT_CLOUD: 'PointCloud',
   RES_TYPE_LEVEL: 'Level',
   RES_TYPE_WORLD: 'World'
   }
VISUAL_DEBUG_POS_TYPE_WORLD = 0
VISUAL_DEBUG_POS_TYPE_RELATIVE = 1

class PhysicsData(object):
    NOTHING = 0
    GHOST = 1
    COMMON_OBSTACLE = 2
    GLASSWALL = 3
    OBSTACLE_QUERY = 4
    VISIBLE_OBSTACLE_QUERY = 5
    SOUND = 21
    WATER = 22
    WATER_QUERY = 23
    STRANGER = 25
    FILTER_COMBATANT = 26
    FILTER_CREATURE = 27
    NPC = 28
    MONSTER_GHOST = 29
    MONSTER_ELITE = 30
    AVATAR = 31