# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/scene_const.py
from __future__ import absolute_import
from logic.gcommon.common_const import collision_const
_reload_all = True
MTL_DIRT = 0
MTL_METAL = 1
MTL_STONE = 2
MTL_SAND = 3
MTL_WOOD = 4
MTL_DEEP_WATER = 5
MTL_GRASS = 6
MTL_GLASS = 7
MTL_WATER = 10
MTL_HOUSE = 11
MTL_ICE = 12
COL_DIRT = collision_const.DIRT_GROUP
COL_GRASS = collision_const.GRASS_GROUP
COL_METAL = collision_const.METAL_GROUP
COL_SAND = collision_const.SAND_GROUP
COL_STONE = collision_const.STONE_GROUP
COL_WATER = collision_const.WATER_GROUP
COL_WOOD = collision_const.WOOD_GROUP
COL_GLASS = collision_const.GLASS_GROUP
COL_ROAD = collision_const.ROAD_GROUP
COL_SLOPE = collision_const.SLOPE_GROUP
COL_ICE = collision_const.ICE_GROUP
material_dic = {MTL_DIRT: 'dirt',
   MTL_GRASS: 'grass',
   MTL_METAL: 'metal',
   MTL_SAND: 'sand',
   MTL_STONE: 'stone',
   MTL_WATER: 'water',
   MTL_DEEP_WATER: 'water',
   MTL_WOOD: 'wood',
   MTL_GLASS: 'glass',
   MTL_ICE: 'ice'
   }
footstep_sfx_dic = {'dirt': 'effect/fx/renwu/tudi01.sfx',
   'grass': 'effect/fx/renwu/caodi01.sfx',
   'metal': 'effect/fx/renwu/yingdi01.sfx',
   'sand': 'effect/fx/renwu/tudi01.sfx',
   'stone': 'effect/fx/renwu/yingdi01.sfx',
   'road': 'effect/fx/renwu/yingdi01.sfx',
   'wood': 'effect/fx/renwu/yingdi01.sfx',
   'snow': 'effect/fx/renwu/snow_yanchen.sfx',
   'ice': 'effect/fx/renwu/snow_yanchen.sfx'
   }
material_sfx_map = {MTL_DIRT: ('effect/fx/weapon/bullet/shazi.sfx', 'effect/fx/weapon/bullet/shazi_dankong.sfx'),
   MTL_GRASS: ('effect/fx/weapon/bullet/caodi.sfx', 'effect/fx/weapon/bullet/caodi_dankong.sfx'),
   MTL_METAL: ('effect/fx/weapon/bullet/jinshu.sfx', 'effect/fx/weapon/bullet/jinshu_dankong.sfx'),
   MTL_SAND: ('effect/fx/weapon/bullet/shazi.sfx', 'effect/fx/weapon/bullet/shazi_dankong.sfx'),
   MTL_STONE: ('effect/fx/weapon/bullet/shitou.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx'),
   MTL_WATER: ('effect/fx/weapon/bullet/shui.sfx', ''),
   MTL_WOOD: ('effect/fx/weapon/bullet/mutou.sfx', 'effect/fx/weapon/bullet/mutou_dankong.sfx'),
   MTL_GLASS: ('effect/fx/weapon/bullet/mutou.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx'),
   MTL_ICE: ('effect/fx/weapon/bullet/ice_hit.sfx', 'effect/fx/weapon/shouji/snow_tiehua_01.sfx')
   }
snow_material_sfx_map = {MTL_DIRT: ('effect/fx/weapon/bullet/snow_hit.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx'),
   MTL_GRASS: ('effect/fx/weapon/bullet/snow_hit.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx'),
   MTL_METAL: ('effect/fx/weapon/bullet/jinshu.sfx', 'effect/fx/weapon/bullet/jinshu_dankong.sfx'),
   MTL_SAND: ('effect/fx/weapon/bullet/snow_hit.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx'),
   MTL_STONE: ('effect/fx/weapon/bullet/shitou.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx'),
   MTL_WATER: ('effect/fx/weapon/bullet/shui.sfx', ''),
   MTL_WOOD: ('effect/fx/weapon/bullet/mutou.sfx', 'effect/fx/weapon/bullet/mutou_dankong.sfx'),
   MTL_GLASS: ('effect/fx/weapon/bullet/mutou.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx'),
   MTL_ICE: ('effect/fx/weapon/bullet/ice_hit.sfx', 'effect/fx/weapon/shouji/snow_tiehua_01.sfx')
   }
collision_material_to_sound = {COL_DIRT: 'dirt',
   COL_GRASS: 'grass',
   COL_METAL: 'metal',
   COL_SAND: 'sand',
   COL_STONE: 'stone',
   COL_WATER: 'water',
   COL_WOOD: 'wood',
   COL_GLASS: 'glass',
   COL_ROAD: 'stone',
   COL_SLOPE: 'metal',
   COL_ICE: 'stone'
   }
collision_sfx_map = {COL_DIRT: ('effect/fx/weapon/bullet/shazi.sfx', 'effect/fx/weapon/bullet/shazi_dankong.sfx'),
   COL_GRASS: ('effect/fx/weapon/bullet/caodi.sfx', 'effect/fx/weapon/bullet/caodi_dankong.sfx'),
   COL_METAL: ('effect/fx/weapon/bullet/jinshu.sfx', 'effect/fx/weapon/bullet/jinshu_dankong.sfx'),
   COL_SLOPE: ('effect/fx/weapon/bullet/jinshu.sfx', 'effect/fx/weapon/bullet/jinshu_dankong.sfx'),
   COL_SAND: ('effect/fx/weapon/bullet/shazi.sfx', 'effect/fx/weapon/bullet/shazi_dankong.sfx'),
   COL_STONE: ('effect/fx/weapon/bullet/shitou.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx'),
   COL_WATER: ('effect/fx/weapon/bullet/shui.sfx', ''),
   COL_WOOD: ('effect/fx/weapon/bullet/mutou.sfx', 'effect/fx/weapon/bullet/mutou_dankong.sfx'),
   COL_GLASS: ('effect/fx/weapon/shouji/glass_ss.sfx', 'effect/fx/weapon/bullet/jinshu_dankong.sfx'),
   COL_ROAD: ('effect/fx/weapon/bullet/shitou.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx'),
   COL_ICE: ('effect/fx/weapon/bullet/ice_hit.sfx', 'effect/fx/weapon/shouji/snow_tiehua_01.sfx')
   }
snow_collision_sfx_map = {COL_DIRT: ('effect/fx/weapon/bullet/snow_hit.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx'),
   COL_GRASS: ('effect/fx/weapon/bullet/snow_hit.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx'),
   COL_METAL: ('effect/fx/weapon/bullet/jinshu.sfx', 'effect/fx/weapon/bullet/jinshu_dankong.sfx'),
   COL_SLOPE: ('effect/fx/weapon/bullet/jinshu.sfx', 'effect/fx/weapon/bullet/jinshu_dankong.sfx'),
   COL_SAND: ('effect/fx/weapon/bullet/snow_hit.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx'),
   COL_STONE: ('effect/fx/weapon/bullet/shitou.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx'),
   COL_WATER: ('effect/fx/weapon/bullet/shui.sfx', ''),
   COL_WOOD: ('effect/fx/weapon/bullet/mutou.sfx', 'effect/fx/weapon/bullet/mutou_dankong.sfx'),
   COL_GLASS: ('effect/fx/weapon/shouji/glass_ss.sfx', 'effect/fx/weapon/bullet/jinshu_dankong.sfx'),
   COL_ROAD: ('effect/fx/weapon/bullet/shitou.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx'),
   COL_ICE: ('effect/fx/weapon/bullet/ice_hit.sfx', 'effect/fx/weapon/shouji/snow_tiehua_01.sfx')
   }
collision_default_sfx = ('effect/fx/weapon/bullet/shitou.sfx', 'effect/fx/weapon/bullet/shitou_dankong.sfx')
ENV_TYPE_OUTSIDE = 0
ENV_TYPE_WATER = 1
ENV_TYPE_HOUSE = 2
PENETRATE_RENDER_STAGE = 64
MODEL_PLANE_PATH = 'model_new/airplane/601_airplane_base_lod2.gim'
FOG_SKY_HEIGHT = 4000
FOG_GROUND_HEIGHT = 700
HUMAN_VIS_TYPE = 0
MECHA_VIS_TYPE = 1
SCENE_MAIN = 'Main'
SCENE_TRANING = 'Traning'
SCENE_COMPETITION = 'Competition'
SCENE_PVE = 'PveEdit'
SCENE_PVE_LOBBY = 'PveLobby'
SCENE_LOBBY = 'Lobby'
SCENE_LOBBY_MIRROR = 'LobbyMirror'
SCENE_LIFT_LOADING = 'LiftLoading'
SCENE_NORMAL_SETTLE = 'NormalSettle'
SCENE_NIGHT_SETTLE = 'NightSettle'
SCENE_MECHA_CHUCHANG = 'MechaChuChang'
SCENE_MODEL_DISPLAY = 'ModelDisplay'
SCENE_LUCKY_HOUSE = 'LuckyHouse'
SCENE_LUCKY_HOUSE_FLASH = 'FlashLuckyHouse'
SCENE_LOTTERY = 'Lottery'
SCENE_AI_LOTTERY = 'AILottery'
SCENE_SAIJIKA = 'Saijika'
SCENE_ZHANSHI = 'Zhanshi'
SCENE_ZHANSHI_UI = 'Zhanshi_UI'
SCENE_SKIN_ZHANSHI = 'SkinZhanshi'
SCENE_ZHANSHI_MECHA = 'ZhanshiMecha'
SCENE_GET_MODEL_DISPLAY = 'GetModelDisplay'
SCENE_GET_MECHA_MODEL_DISPLAY = 'GetMechaModelDisplay'
SCENE_MALL = 'Mall'
SCENE_ITEM_BOOK = 'ItemBook'
SCENE_NEWBIE_PASS = 'NewbiePass'
SCENE_CLAN_RANK = 'ClanRank'
SCENE_MAIN_RANK = 'MainRank'
SCENE_GVG_PREPARE_CHOOSE_MECHA = 'GVGPrepareChooseMecha'
SCENE_GVG_CHOOSE_MECHA = 'GVGChooseMecha'
SCENE_MAIN_BOND = 'MainBond'
SCENE_CLONE_VOTE_MECHA = 'CloneVoteMecha'
SCENE_MECHA_RECONSTRUCT = 'MechaReconstruct'
SCENE_GET_DECORATION_DISPLAY = 'GetDecorationDisplay'
SCENE_FFA_PREPARE_CHOOSE_MECHA = 'FFAPrepareChooseMecha'
SCENE_FFA_CHOOSE_MECHA = 'FFAChooseMecha'
SCENE_MECHA_DEATH_PREPARE_CHOOSE_MECHA = 'MechaDeathPrepareChooseMecha'
SCENE_MECHA_DEATH_CHOOSE_MECHA = 'MechaDeathChooseMecha'
SCENE_SKIN_DEFINE = 'SkinDefine'
SCENE_ZOMBIEFFA_CHOOSE_MECHA = 'ZombieFFAChooseMecha'
SCENE_JIEMIAN_COMMON = 'JieMianCommon'
SCENE_GET_WEAPON_DISPLAY = 'GetWeaponDisplay'
SCENE_TOP_NATIVE = 'TopNativeRank'
SCENE_SMALL_BP = 'SmallBp'
SCENE_LUCKY_HOUSE_COMMON = 'LuckyHouseCommon'
SCENE_LUCKY_HOUSE_ART_COLLECTION = 'LuckyHouseArtCollection'
SCENE_TEAM_RECRUIT = 'TeamRecruit'
SCENE_AICONCERT = 'AiConcert'
SCENE_AR = 'AR'
SCENE_ACTIVITY_LEICHONG = 'ActivityLeichong'
SCENE_COMPETITION_SYNC = 'Competition_sync'
SCENE_PVE_MAIN_UI = 'PVEMainUI'
SCENE_PVE_BOOK_WIDGET_UI = 'PVEBookWidgetUI'
SCENE_PVE_END_UI = 'PVEEndUI'
SCENE_PVE_END_STATISTICS_UI = 'PVEEndStatisticsUI'
SCENE_PVE_EDIT = 'PVEEdit'
SCENE_PVE_RANK = 'PVERank'
SCENE_GLIDE_EFFECT = 'GlideEffectScene'
SCENE_ART_CHECK_DISPLAY = 'ArtCheckDisplay'
BATTLE_SCENE_TYPES = {
 SCENE_TRANING, SCENE_COMPETITION, SCENE_AICONCERT, SCENE_PVE}
LOBBY_EYE_ADAPT_FACTOR = 1.0
BLOOD_UNIT = 500
GVG_BLOOD_UNIT = BLOOD_UNIT * 100
DISPLAY_SCENES_LIST = (
 SCENE_ZHANSHI_MECHA, SCENE_SKIN_ZHANSHI, SCENE_ZHANSHI, SCENE_ZHANSHI_UI, SCENE_JIEMIAN_COMMON)