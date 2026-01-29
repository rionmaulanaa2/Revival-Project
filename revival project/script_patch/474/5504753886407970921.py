# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CGameModeManager.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.client.const import game_mode_const
from common.framework import Singleton
from logic.gcommon.common_const.battle_const import BATTLE_SCENE_NORMAL
import world
from logic.gcommon.common_const import battle_const
from logic.vscene.parts.gamemode.CNormalMode import CNormalMode
from logic.vscene.parts.gamemode.CScoreMode import CScoreMode
from logic.vscene.parts.gamemode.COccupyMode import COccupyMode
from logic.vscene.parts.gamemode.CKingMode import CKingMode
from logic.vscene.parts.gamemode.CDeathMode import CDeathMode
from logic.vscene.parts.gamemode.CFFAMode import CFFAMode
from logic.vscene.parts.gamemode.CGVGMode import CGVGMode
from logic.vscene.parts.gamemode.CSnipeMode import CSnipeMode
from logic.vscene.parts.gamemode.CGranbelmSurMode import CGranbelmSurMode
from logic.vscene.parts.gamemode.CCloneMode import CCloneMode
from logic.vscene.parts.gamemode.CImproviseMode import CImproviseMode
from logic.vscene.parts.gamemode.CMechaDeathMode import CMechaDeathMode
from logic.vscene.parts.gamemode.CZombieFFAMode import CZombieFFAMode
from logic.vscene.parts.gamemode.CNewbieStageMode import CNewbieStageMode
from logic.vscene.parts.gamemode.CHumanDeathMode import CHumanDeathMode
from logic.vscene.parts.gamemode.CGranhackSurMode import CGranhackSurMode
from logic.vscene.parts.gamemode.CArmRaceMode import CArmRaceMode
from logic.vscene.parts.gamemode.CRandomDeathMode import CRandomDeathMode
from logic.vscene.parts.gamemode.CConcertMode import CConcertMode
from logic.vscene.parts.gamemode.CFlagMode import CFlagMode
from logic.vscene.parts.gamemode.CCrownMode import CCrownMode
from logic.vscene.parts.gamemode.CGravitySurMode import CGravitySurMode
from logic.vscene.parts.gamemode.CBountySurMode import CBountySurMode
from logic.vscene.parts.gamemode.CExerciseMode import CExerciseMode
from logic.vscene.parts.gamemode.CRecruitmentSurMode import CRecruitmentSurMode
from logic.vscene.parts.gamemode.CHuntingMode import CHuntingMode
from logic.vscene.parts.gamemode.CFireSurMode import CFireSurMode
from logic.vscene.parts.gamemode.CCrystalMode import CCrystalMode
from logic.vscene.parts.gamemode.CMutiOccupyMode import CMutiOccupyMode
from logic.vscene.parts.gamemode.CADCrystalMode import CADCrystalMode
from logic.vscene.parts.gamemode.CScavengeMode import CScavengeMode
from logic.vscene.parts.gamemode.CTrainMode import CTrainMode
from logic.vscene.parts.gamemode.CMagicSurMode import CMagicSurMode
from logic.vscene.parts.gamemode.CFlag2Mode import CFlag2Mode
from logic.vscene.parts.gamemode.CSnatchEggMode import CSnatchEggMode
from logic.vscene.parts.gamemode.CGooseBearMode import CGooseBearMode
from logic.vscene.parts.gamemode.CGulagSurMode import CGulagSurMode
from logic.vscene.parts.gamemode.CPveMode import CPveMode
from logic.vscene.parts.gamemode.CPveEditMode import CPveEditMode
from logic.vscene.parts.gamemode.CAssaultMode import CAssaultMode
from logic.vscene.parts.gamemode.CNBombMode import CNBombMode
KEY_TO_CLS = {game_mode_const.GAME_MODE_NORMAL: CNormalMode,
   game_mode_const.GAME_MODE_SCORE: CScoreMode,
   game_mode_const.GAME_MODE_CONTROL: COccupyMode,
   game_mode_const.GAME_MODE_KING: CKingMode,
   game_mode_const.GAME_MODE_DEATH: CDeathMode,
   game_mode_const.GAME_MODE_FFA: CFFAMode,
   game_mode_const.GAME_MODE_GVG: CGVGMode,
   game_mode_const.GAME_MODE_SNIPE: CSnipeMode,
   game_mode_const.GAME_MODE_GRANBELM_SURVIVAL: CGranbelmSurMode,
   game_mode_const.GAME_MODE_CLONE: CCloneMode,
   game_mode_const.GAME_MODE_IMPROVISE: CImproviseMode,
   game_mode_const.GAME_MODE_MECHA_DEATH: CMechaDeathMode,
   game_mode_const.GAME_MODE_ZOMBIE_FFA: CZombieFFAMode,
   game_mode_const.GAME_MODE_NEWBIE_STAGE: CNewbieStageMode,
   game_mode_const.GAME_MODE_HUMAN_DEATH: CHumanDeathMode,
   game_mode_const.GAME_MODE_GRANHACK_SURVIVAL: CGranhackSurMode,
   game_mode_const.GAME_MODE_ARMRACE: CArmRaceMode,
   game_mode_const.GAME_MODE_RANDOM_DEATH: CRandomDeathMode,
   game_mode_const.GAME_MODE_CONCERT: CConcertMode,
   game_mode_const.GAME_MODE_GRAVITY_SURVIVAL: CGravitySurMode,
   game_mode_const.GAME_MODE_FLAG: CFlagMode,
   game_mode_const.GAME_MODE_CROWN: CCrownMode,
   game_mode_const.GAME_MODE_BOUNTY_SURVIVAL: CBountySurMode,
   game_mode_const.GAME_MODE_EXERCISE: CExerciseMode,
   game_mode_const.GAME_MODE_RECRUITMENT_SURVIVAL: CRecruitmentSurMode,
   game_mode_const.GAME_MODE_HUNTING: CHuntingMode,
   game_mode_const.GAME_MODE_FIRE_SURVIVAL: CFireSurMode,
   game_mode_const.GAME_MODE_CRYSTAL: CCrystalMode,
   game_mode_const.GAME_MODE_MUTIOCCUPY: CMutiOccupyMode,
   game_mode_const.GAME_MODE_ADCRYSTAL: CADCrystalMode,
   game_mode_const.GAME_MODE_SCAVENGE: CScavengeMode,
   game_mode_const.GAME_MODE_TRAIN: CTrainMode,
   game_mode_const.GAME_MODE_MAGIC_SURVIVAL: CMagicSurMode,
   game_mode_const.GAME_MODE_FLAG2: CFlag2Mode,
   game_mode_const.GAME_MODE_SNATCHEGG: CSnatchEggMode,
   game_mode_const.GAME_MODE_DUEL: CGVGMode,
   game_mode_const.GAME_MODE_GOOSE_BEAR: CGooseBearMode,
   game_mode_const.GAME_MODE_GULAG_SURVIVAL: CGulagSurMode,
   game_mode_const.GAME_MODE_PVE: CPveMode,
   game_mode_const.GAME_MODE_PVE_EDIT: CPveEditMode,
   game_mode_const.GAME_MODE_ASSAULT: CAssaultMode,
   game_mode_const.GAME_MODE_NBOMB_SURVIVAL: CNBombMode
   }

class CGameModeManager(Singleton):
    ALIAS_NAME = 'game_mode'

    def init(self):
        self.map_id = 4
        self.mode = None
        self.mode_Type = game_mode_const.GAME_MODE_NORMAL
        self.enviroment = None
        self.mode_scale = 1.0
        self.born_path = None
        self.is_replace_model = False
        self.scene_name = BATTLE_SCENE_NORMAL
        return

    def on_finalize(self):
        self.mode and self.mode.on_finalize()
        self.mode = None
        self.enviroment = None
        self.born_path = None
        self.is_replace_model and world.reset_res_object_filemap()
        self.is_replace_model = False
        return

    def get_mode_type(self):
        return self.mode_Type

    def get_map_id(self):
        return self.map_id

    def is_mode_type(self, i_type):
        if type(i_type) is set or type(i_type) is tuple:
            for item in i_type:
                if type(item) is set or type(item) is tuple:
                    if self.mode_Type in item:
                        return True
                elif self.mode_Type == item:
                    return True

            return False
        else:
            return self.mode_Type == i_type

    def ignore_sdmap_hidelayer(self):
        is_not_ignore = self.is_mode_type(game_mode_const.Show_AirWall)
        if global_data.feature_mgr.is_support_scene_ignore_group_names():
            hide_group_names = [] if is_not_ignore else ['sdmap_hidelayer']
            world.set_scene_ignore_group_names(hide_group_names)
        else:
            hide_group_name = '' if is_not_ignore else 'sdmap_hidelayer'
            world.set_scene_ignore_group_name(hide_group_name)

    def replace_model_by_mode(self):
        if self.is_kongdao_scene() and self.mode_Type in game_mode_const.GAME_MODE_DEATHS:
            kongdao_dc = confmgr.get('script_gim_ref')['kongdao_dc']
            old_gim_lst = kongdao_dc['old']
            new_gim_lst = kongdao_dc['new']
            for i, path in enumerate(old_gim_lst):
                world.set_res_object_filemap(path.replace('/', '\\'), new_gim_lst[i].replace('/', '\\'))

            self.is_replace_model = True
        if self.mode_Type in (game_mode_const.GAME_MODE_PVE, game_mode_const.GAME_MODE_PVE_EDIT):
            global_data.battle.replace_scene_model()
            self.is_replace_model = True

    def set_map(self, map_id, battle_type):
        self.map_id = map_id
        self.mode and self.mode.on_finalize()
        self.mode = None
        map_config = confmgr.get('map_config')
        self.mode_Type = map_config.get(str(self.map_id), {}).get('cCMode', game_mode_const.GAME_MODE_NORMAL)
        self.scene_name = map_config.get(str(self.map_id), {}).get('cSceneConfig', BATTLE_SCENE_NORMAL)
        self.ignore_sdmap_hidelayer()
        mode_cls = KEY_TO_CLS.get(self.mode_Type, CNormalMode)
        battle_config = confmgr.get('battle_config', str(battle_type), default={})
        self.mode_scale = battle_config.get('fBattleScale', 1.0)
        if mode_cls:
            self.mode = mode_cls(map_id)
            global_data.emgr.game_mode_init_complete.emit()
        return

    def get_born_data(self, *args, **kwargs):
        map_config = confmgr.get('map_config', str(self.map_id), default={})
        map_name = map_config.get('cName', '')
        map_path = self.get_cfg_name(self.map_id)
        if map_name == 'map_kongdao':
            self.born_path = '/'.join([map_path, map_name, 'born_data'])
        else:
            self.born_path = '/'.join([map_path, 'born_data'])
        return confmgr.get(self.born_path, *args, **kwargs)

    def get_map_name(self):
        map_config = confmgr.get('map_config', str(self.map_id), default={})
        map_name = map_config.get('cName', '')
        return map_name

    def get_cfg_name(self, map_id):
        map_config = confmgr.get('map_config', str(map_id), default={})
        map_path = map_config['cCModeCfgName'] if 'cCModeCfgName' in map_config else map_config.get('cCMode', game_mode_const.GAME_MODE_NORMAL)
        return '/'.join(['game_mode', map_path])

    def get_cfg_data(self, cfg_file, *args, **kwargs):
        cfg_name = '/'.join([self.get_cfg_name(self.map_id), cfg_file])
        return confmgr.get(cfg_name, *args, **kwargs)

    def get_cfg_data_by_map_id(self, map_id, cfg_file):
        cfg_name = '/'.join([self.get_cfg_name(map_id), cfg_file])
        return confmgr.get(cfg_name)

    def set_enviroment(self, ev_type):
        self.enviroment = ev_type

    def get_enviroment(self):
        return self.enviroment

    def is_map_name(self, map_name):
        if map_name == self.get_map_name():
            return True
        return False

    def is_snow_weather(self):
        return self.enviroment == battle_const.BATTLE_ENV_SNOW

    def is_snow_night_weather(self):
        return self.enviroment == battle_const.BATTLE_ENV_SNOW_NIGHT

    def is_snow_res(self):
        return self.enviroment in (battle_const.BATTLE_ENV_SNOW, battle_const.BATTLE_ENV_SNOW_NIGHT)

    def is_night_weather(self):
        return self.enviroment == battle_const.BATTLE_ENV_NIGHT

    def is_neutral_shop_env(self):
        return self.enviroment == battle_const.BATTLE_ENV_NEUTRAL_SHOP

    def is_granbelm_env(self):
        return self.enviroment == battle_const.BATTLE_ENV_GRANBELM

    def is_summer_environment(self):
        return self.enviroment == battle_const.BATTLE_ENV_SUMMER

    def is_kongdao_scene(self):
        from logic.gcommon.common_const.battle_const import BATTLE_SCENE_KONGDAO
        return self.scene_name == BATTLE_SCENE_KONGDAO

    def is_bounty_environment(self):
        return self.enviroment == battle_const.BATTLE_ENV_BOUNTY

    def is_pve(self):
        return self.is_mode_type(game_mode_const.GAME_MODE_PVES)

    def get_mode_scale(self):
        return self.mode_scale

    def is_ace_coin_enable(self):
        return self.is_neutral_shop_env()

    def get_shader_env_type(self):
        return battle_const.SHADER_ENV_MAP.get(self.enviroment, battle_const.SHADER_EVN_NORMAL)