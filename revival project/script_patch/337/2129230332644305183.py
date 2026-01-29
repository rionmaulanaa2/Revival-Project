# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartCompetitionBattlePrepare.py
from __future__ import absolute_import
from logic.gcommon.common_utils import parachute_utils
from logic.client.const import game_mode_const
from logic.gcommon.common_const import collision_const
from mobile.common.EntityManager import EntityManager
from logic.vscene.parts.gamemode.CGameModeManager import CGameModeManager
from mobile.common.EntityFactory import EntityFactory
from mobile.common.IdManager import IdManager
from logic.comsys.battle import BattleUtils
from logic.gutils import scene_utils
from common.utils import timer
import world
import math3d
import collision
import math
from . import ScenePart
import logic.vscene.parts.battleprepare.BattlePrepare as BattlePrepare
from logic.vscene.parts.battleprepare.SurvivalBattlePrepare import SurvivalBattlePrepare
from logic.vscene.parts.battleprepare.PveBattlePrepare import PveEditBattlePrepare, PveBattlePrepare
KEY_TO_CLS = {game_mode_const.GAME_MODE_CONTROL: BattlePrepare.DeathBattlePrepare,
   game_mode_const.GAME_MODE_KING: BattlePrepare.KothBattlePrepare,
   game_mode_const.GAME_MODE_DEATH: BattlePrepare.DeathBattlePrepare,
   game_mode_const.GAME_MODE_EXERCISE: BattlePrepare.ExerciseBattlePrepare,
   game_mode_const.GAME_MODE_FFA: BattlePrepare.FFABattlePrepare,
   game_mode_const.GAME_MODE_GVG: BattlePrepare.GVGBattlePrepare,
   game_mode_const.GAME_MODE_SNIPE: BattlePrepare.DeathBattlePrepare,
   game_mode_const.GAME_MODE_CLONE: BattlePrepare.DeathBattlePrepare,
   game_mode_const.GAME_MODE_IMPROVISE: BattlePrepare.ImproviseBattlePrepare,
   game_mode_const.GAME_MODE_MECHA_DEATH: BattlePrepare.DeathBattlePrepare,
   game_mode_const.GAME_MODE_ZOMBIE_FFA: BattlePrepare.FFABattlePrepare,
   game_mode_const.GAME_MODE_NORMAL: SurvivalBattlePrepare,
   game_mode_const.GAME_MODE_HUMAN_SURVIVAL: SurvivalBattlePrepare,
   game_mode_const.GAME_MODE_FAST_SURVIVAL: SurvivalBattlePrepare,
   game_mode_const.GAME_MODE_NIGHT_SURVIVAL: SurvivalBattlePrepare,
   game_mode_const.GAME_MODE_SNOW_SURVIVAL: SurvivalBattlePrepare,
   game_mode_const.GAME_MODE_GRANBELM_SURVIVAL: SurvivalBattlePrepare,
   game_mode_const.GAME_MODE_HUMAN_DEATH: BattlePrepare.HumanDeathBattlePrepare,
   game_mode_const.GAME_MODE_GRANHACK_SURVIVAL: SurvivalBattlePrepare,
   game_mode_const.GAME_MODE_ARMRACE: BattlePrepare.ArmRaceBattlePrepare,
   game_mode_const.GAME_MODE_RANDOM_DEATH: BattlePrepare.DeathBattlePrepare,
   game_mode_const.GAME_MODE_CONCERT: BattlePrepare.ConcertBattlePrepare,
   game_mode_const.GAME_MODE_GRAVITY_SURVIVAL: SurvivalBattlePrepare,
   game_mode_const.GAME_MODE_FLAG: BattlePrepare.DeathBattlePrepare,
   game_mode_const.GAME_MODE_CROWN: BattlePrepare.DeathBattlePrepare,
   game_mode_const.GAME_MODE_CRYSTAL: BattlePrepare.DeathBattlePrepare,
   game_mode_const.GAME_MODE_BOUNTY_SURVIVAL: SurvivalBattlePrepare,
   game_mode_const.GAME_MODE_HUNTING: BattlePrepare.DeathBattlePrepare,
   game_mode_const.GAME_MODE_FIRE_SURVIVAL: SurvivalBattlePrepare,
   game_mode_const.GAME_MODE_MUTIOCCUPY: BattlePrepare.DeathBattlePrepare,
   game_mode_const.GAME_MODE_ADCRYSTAL: BattlePrepare.ADCrystalBattlePrepare,
   game_mode_const.GAME_MODE_TRAIN: BattlePrepare.DeathBattlePrepare,
   game_mode_const.GAME_MODE_SCAVENGE: BattlePrepare.HumanDeathBattlePrepare,
   game_mode_const.GAME_MODE_MAGIC_SURVIVAL: SurvivalBattlePrepare,
   game_mode_const.GAME_MODE_FLAG2: BattlePrepare.DeathBattlePrepare,
   game_mode_const.GAME_MODE_SNATCHEGG: BattlePrepare.SnatchEggBattlePrepare,
   game_mode_const.GAME_MODE_DUEL: BattlePrepare.GVGBattlePrepare,
   game_mode_const.GAME_MODE_GOOSE_BEAR: BattlePrepare.GooseBearBattlePrepare,
   game_mode_const.GAME_MODE_GULAG_SURVIVAL: SurvivalBattlePrepare,
   game_mode_const.GAME_MODE_PVE: PveBattlePrepare,
   game_mode_const.GAME_MODE_PVE_EDIT: PveEditBattlePrepare,
   game_mode_const.GAME_MODE_ASSAULT: BattlePrepare.AssaultBattlePrepare,
   game_mode_const.GAME_MODE_NBOMB_SURVIVAL: SurvivalBattlePrepare
   }

class PartCompetitionBattlePrepare(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartCompetitionBattlePrepare, self).__init__(scene, name, need_update=True)
        self.init_battle_prepare()

    def init_battle_prepare(self):
        mode_type = global_data.game_mode.get_mode_type()
        cls = KEY_TO_CLS.get(mode_type, BattlePrepare.BattlePrepareBase)
        self.battle_prepare = cls(self)

    def on_enter(self):
        if CGameModeManager().get_enviroment() == 'night':
            env_name = 'competition_bw_06_night.xml'
        elif CGameModeManager().get_enviroment() == 'granbelm':
            env_name = 'competition_bw_06_granbelm.xml'
        else:
            env_name = 'competition_bw_06.xml'
        world.get_active_scene().load_env(env_name)
        global_data.emgr.scene_tigger_auto_fog.emit(True)
        self.battle_prepare and self.battle_prepare.on_enter()

    def on_pre_load(self):
        self.battle_prepare.on_pre_load()

    def on_exit(self):
        global_data.emgr.camera_on_start_nearclip.emit()
        self.battle_prepare and self.battle_prepare.on_exit()

    def is_in_battle_boundary(self, px, py, pz, margin=0):
        if not self.battle_prepare or not hasattr(self.battle_prepare, 'is_in_battle_boundary'):
            return True
        return self.battle_prepare.is_in_battle_boundary(px, py, pz, margin=margin)