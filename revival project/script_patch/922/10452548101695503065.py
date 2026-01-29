# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/SettleSystem.py
from __future__ import absolute_import
import six_ex
import six
import functools
from common.framework import Singleton
from logic.client.const import game_mode_const
from logic.comsys.battle.Settle import settle_system_utils
from common.cfg import confmgr
from logic.comsys.chart_ui.EndSettlementChartUI import EndSettlementChartUI
from logic.comsys.chart_ui.EndTDMSettlementChart import EndTDMSettlementChartUI
from logic.comsys.chart_ui.EndTDMSettlementChart2 import EndTDMSettlementChartUI2
from logic.gcommon.common_const.scene_const import SCENE_NORMAL_SETTLE, SCENE_NIGHT_SETTLE, SCENE_PVE_END_UI
from logic.vscene.parts.gamemode.CGameModeManager import CGameModeManager

class SettleSystem(Singleton):

    def init(self):
        self._all_dlgs = []
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)

    def on_finalize(self):
        self.close_all_dlg()
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_hide_count(self.__class__.__name__)

    def close_all_dlg(self):
        for dlg in self._all_dlgs:
            if dlg.is_valid():
                dlg.close()

        self._all_dlgs = []

    def show_end_death_replay(self, group_num, settle_dict):
        if global_data.game_mode.is_pve():
            return
        show_end_anim = False
        if global_data.player and global_data.player.logic:
            if global_data.player.logic.ev_g_all_groupmates_dead():
                show_end_anim = True
        if not show_end_anim:
            self.close_all_dlg()
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
                self.has_been_disable_stage = True
                self.show_end_death_replay_ui(settle_dict, group_num)

    def show_settle_teammate_alive(self, group_num, replay_data):
        self.close_all_dlg()
        from logic.comsys.battle.Settle.EndContinueUI import EndContinueUI
        self._all_dlgs.append(EndContinueUI(None, group_num))
        return

    def _ext_settle_use_org_skin(self, in_settle_dict, in_team_info):

        def modify_model_data--- This code section failed: ---

  60       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('FASHION_POS_SUIT',)
           6  IMPORT_NAME           0  'logic.gcommon.item.item_const'
           9  IMPORT_FROM           1  'FASHION_POS_SUIT'
          12  STORE_FAST            1  'FASHION_POS_SUIT'
          15  POP_TOP          

  61      16  LOAD_FAST             0  'in_data'
          19  LOAD_ATTR             2  'get'
          22  LOAD_CONST            3  'role'
          25  LOAD_FAST             0  'in_data'
          28  LOAD_ATTR             2  'get'
          31  LOAD_CONST            4  'role_id'
          34  LOAD_CONST            5  11
          37  CALL_FUNCTION_2       2 
          40  CALL_FUNCTION_2       2 
          43  STORE_FAST            2  'role_id'

  62      46  LOAD_FAST             0  'in_data'
          49  LOAD_ATTR             2  'get'
          52  LOAD_CONST            6  'fashion'
          55  BUILD_MAP_0           0 
          58  CALL_FUNCTION_2       2 
          61  STORE_FAST            3  'fashion_dict'

  63      64  LOAD_FAST             3  'fashion_dict'
          67  POP_JUMP_IF_FALSE   139  'to 139'
          70  LOAD_FAST             2  'role_id'
        73_0  COME_FROM                '67'
          73  POP_JUMP_IF_FALSE   139  'to 139'

  64      76  LOAD_GLOBAL           3  'confmgr'
          79  LOAD_ATTR             2  'get'
          82  LOAD_CONST            7  'role_info'
          85  LOAD_CONST            8  'RoleInfo'
          88  LOAD_CONST            9  'Content'
          91  LOAD_GLOBAL           4  'str'
          94  LOAD_FAST             2  'role_id'
          97  CALL_FUNCTION_1       1 
         100  LOAD_CONST           10  'default_skin'
         103  CALL_FUNCTION_5       5 
         106  STORE_FAST            4  'default_skin_lst'

  65     109  LOAD_FAST             4  'default_skin_lst'
         112  POP_JUMP_IF_FALSE   139  'to 139'

  66     115  BUILD_MAP_1           1 
         118  LOAD_FAST             4  'default_skin_lst'
         121  LOAD_CONST            1  ''
         124  BINARY_SUBSCR    
         125  LOAD_FAST             1  'FASHION_POS_SUIT'
         128  STORE_MAP        
         129  STORE_MAP        
         130  DELETE_SUBSCR    
         131  DELETE_SUBSCR    
         132  STORE_SUBSCR     
         133  JUMP_ABSOLUTE       139  'to 139'
         136  JUMP_FORWARD          0  'to 139'
       139_0  COME_FROM                '136'

  67     139  LOAD_FAST             0  'in_data'
         142  LOAD_ATTR             2  'get'
         145  LOAD_CONST           11  'mecha_fashion'
         148  BUILD_MAP_0           0 
         151  CALL_FUNCTION_2       2 
         154  STORE_FAST            5  'mecha_fashion'

  68     157  LOAD_FAST             5  'mecha_fashion'
         160  POP_JUMP_IF_FALSE   363  'to 363'

  69     163  LOAD_CONST            0  ''
         166  STORE_FAST            6  'mecha_item_id'

  70     169  LOAD_FAST             0  'in_data'
         172  LOAD_ATTR             2  'get'
         175  LOAD_CONST           12  'mecha_id'
         178  LOAD_CONST            0  ''
         181  CALL_FUNCTION_2       2 
         184  STORE_FAST            7  'mecha_id'

  71     187  LOAD_FAST             7  'mecha_id'
         190  LOAD_CONST            0  ''
         193  COMPARE_OP            8  'is'
         196  POP_JUMP_IF_FALSE   257  'to 257'

  72     199  LOAD_FAST             5  'mecha_fashion'
         202  LOAD_ATTR             2  'get'
         205  LOAD_FAST             1  'FASHION_POS_SUIT'
         208  LOAD_CONST            0  ''
         211  CALL_FUNCTION_2       2 
         214  STORE_FAST            8  'mecha_fashion_id'

  73     217  LOAD_FAST             8  'mecha_fashion_id'
         220  POP_JUMP_IF_FALSE   291  'to 291'

  74     223  LOAD_CONST            1  ''
         226  LOAD_CONST           13  ('get_lobby_item_belong_no',)
         229  IMPORT_NAME           6  'logic.gutils.item_utils'
         232  IMPORT_FROM           7  'get_lobby_item_belong_no'
         235  STORE_FAST            9  'get_lobby_item_belong_no'
         238  POP_TOP          

  75     239  LOAD_FAST             9  'get_lobby_item_belong_no'
         242  LOAD_FAST             8  'mecha_fashion_id'
         245  CALL_FUNCTION_1       1 
         248  STORE_FAST            6  'mecha_item_id'
         251  JUMP_ABSOLUTE       291  'to 291'
         254  JUMP_FORWARD         34  'to 291'

  77     257  LOAD_CONST            1  ''
         260  LOAD_CONST           14  ('battle_id_to_mecha_lobby_id',)
         263  IMPORT_NAME           8  'logic.gutils.dress_utils'
         266  IMPORT_FROM           9  'battle_id_to_mecha_lobby_id'
         269  STORE_FAST           10  'battle_id_to_mecha_lobby_id'
         272  POP_TOP          

  78     273  LOAD_FAST            10  'battle_id_to_mecha_lobby_id'
         276  LOAD_GLOBAL          10  'int'
         279  LOAD_FAST             7  'mecha_id'
         282  CALL_FUNCTION_1       1 
         285  CALL_FUNCTION_1       1 
         288  STORE_FAST            6  'mecha_item_id'
       291_0  COME_FROM                '254'

  79     291  LOAD_FAST             6  'mecha_item_id'
         294  POP_JUMP_IF_FALSE   363  'to 363'

  80     297  LOAD_GLOBAL           3  'confmgr'
         300  LOAD_ATTR             2  'get'
         303  LOAD_CONST           15  'mecha_conf'
         306  LOAD_CONST           16  'LobbyMechaConfig'
         309  LOAD_CONST            9  'Content'
         312  LOAD_GLOBAL           4  'str'
         315  LOAD_FAST             6  'mecha_item_id'
         318  CALL_FUNCTION_1       1 
         321  LOAD_CONST           17  'default_fashion'
         324  CALL_FUNCTION_5       5 
         327  STORE_FAST           11  'default_skin'

  81     330  LOAD_FAST            11  'default_skin'
         333  POP_JUMP_IF_FALSE   360  'to 360'

  82     336  BUILD_MAP_1           1 
         339  LOAD_FAST            11  'default_skin'
         342  LOAD_CONST            1  ''
         345  BINARY_SUBSCR    
         346  LOAD_FAST             1  'FASHION_POS_SUIT'
         349  STORE_MAP        
         350  STORE_MAP        
         351  STORE_MAP        
         352  STORE_MAP        
         353  STORE_SUBSCR     
         354  JUMP_ABSOLUTE       360  'to 360'
         357  JUMP_ABSOLUTE       363  'to 363'
         360  JUMP_FORWARD          0  'to 363'
       363_0  COME_FROM                '360'

  83     363  LOAD_CONST           18  'mecha_custom_skin'
         366  LOAD_FAST             0  'in_data'
         369  COMPARE_OP            6  'in'
         372  POP_JUMP_IF_FALSE   385  'to 385'

  84     375  BUILD_MAP_0           0 
         378  BUILD_MAP_18         18 
         381  STORE_SUBSCR     
         382  JUMP_FORWARD          0  'to 385'
       385_0  COME_FROM                '382'
         385  LOAD_CONST            0  ''
         388  RETURN_VALUE     

Parse error at or near `STORE_MAP' instruction at offset 129

        modify_model_data(in_settle_dict)
        history_mate = in_settle_dict.get('history_mate', [])
        if history_mate:
            history_mate_info = history_mate[0]
            if history_mate_info:
                for object_id in history_mate_info:
                    modify_model_data(history_mate_info[object_id])

        for object_id in in_team_info:
            modify_model_data(in_team_info[object_id])

    def show_settle_final(self, group_num, settle_dict, reward, teammate_num, teaminfo, enemy_dict, achievement, total_fighter_num):
        from ext_package.ext_decorator import has_skin_ext
        if not has_skin_ext():
            self._ext_settle_use_org_skin(settle_dict, teaminfo)
        mode_type = global_data.game_mode.get_mode_type()
        if mode_type == game_mode_const.GAME_MODE_KING:
            self._show_koth_settle_final(group_num, settle_dict, reward, teammate_num, teaminfo, achievement)
        elif mode_type in game_mode_const.GAME_MODE_DEATHS:
            self._show_death_settle_final(group_num, settle_dict, reward, teammate_num, teaminfo, enemy_dict, achievement)
        elif mode_type == game_mode_const.GAME_MODE_FFA:
            self._show_ffa_settle_final(group_num, settle_dict, reward, teammate_num, teaminfo, total_fighter_num)
        elif mode_type in (game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_DUEL):
            self._show_gvg_settle_final(group_num, settle_dict, reward, teaminfo, achievement)
        elif mode_type == game_mode_const.GAME_MODE_IMPROVISE:
            self._show_improvise_settle_final(group_num, settle_dict, reward, teaminfo, achievement)
        elif mode_type == game_mode_const.GAME_MODE_ZOMBIE_FFA:
            self._show_zombieffa_settle_final(group_num, settle_dict, reward, teaminfo, total_fighter_num)
        elif mode_type == game_mode_const.GAME_MODE_ARMRACE:
            self._show_armrace_settle_final(group_num, settle_dict, reward, teammate_num, teaminfo, total_fighter_num)
        elif mode_type == game_mode_const.GAME_MODE_SNATCHEGG:
            self._show_snatchegg_settle_final(group_num, settle_dict, reward, teammate_num, teaminfo, enemy_dict, achievement)
        elif mode_type == game_mode_const.GAME_MODE_GOOSE_BEAR:
            self._show_death_settle_final(group_num, settle_dict, reward, teammate_num, teaminfo, enemy_dict, achievement)
        elif mode_type in game_mode_const.GAME_MODE_PVES:
            self._show_pve_settle_final(group_num, settle_dict, reward, teammate_num, teaminfo, total_fighter_num)
        else:
            if mode_type in game_mode_const.GAME_MODE_NBOMB_SURVIVAL:
                end_anim_ui = global_data.ui_mgr.get_ui('EndAnimUI')
                end_scene_ui = global_data.ui_mgr.get_ui('EndSceneUI')
                end_transition_ui = global_data.ui_mgr.get_ui('EndTransitionUI')
                end_statistics_ui = global_data.ui_mgr.get_ui('EndStatisticsUI')
                end_settlement_chart_ui = global_data.ui_mgr.get_ui('EndSettlementChartUI')
                end_settlement_chart_ui2 = global_data.ui_mgr.get_ui('EndTDMSettlementChartUI2')
                end_exp_ui = global_data.ui_mgr.get_ui(settle_system_utils.get_end_exp_ui_cls().__name__)
                quit_from_spectate = settle_dict.get('quit_from_spectate', False)
                if quit_from_spectate:
                    if end_anim_ui:
                        global_data.ui_mgr.close_ui('EndAnimUI')
                        end_anim_ui = None
                    self.close_all_dlg()
                if end_anim_ui or end_scene_ui or end_statistics_ui or end_exp_ui or end_transition_ui or end_settlement_chart_ui or end_settlement_chart_ui2:
                    return
                is_in_spec = False
                if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_is_in_spectate():
                    is_in_spec = True
            cmode = global_data.game_mode.mode
            if cmode:
                is_explosed = cmode.is_nomb_exploded() if 1 else False
                if is_explosed and not is_in_spec:
                    self._show_nbomb_settle_final(group_num, settle_dict, reward, teammate_num, teaminfo, achievement, total_fighter_num)
                    return
                self._show_settle_final(group_num, settle_dict, reward, teammate_num, teaminfo, achievement, total_fighter_num)
            else:
                self._show_settle_final(group_num, settle_dict, reward, teammate_num, teaminfo, achievement, total_fighter_num)
        if mode_type in game_mode_const.GAME_MODE_DEATHS:
            from logic.comsys.common_ui.EndLikeNoticeUI import EndLikeNoticeUI
            end_like_ui = EndLikeNoticeUI()
            self._all_dlgs.append(end_like_ui)
        self._play_settle_bgm(settle_dict)
        return

    def show_judge_ob_settle(self):
        from logic.gutils.judge_utils import is_ob
        if not is_ob():
            return
        else:
            global_data.ui_mgr.close_ui('BattleWinnersUI')
            import wwise
            wwise.SoundEngine.SetRTPCValue('game_settlement', 100)
            battle = global_data.player.get_battle()
            if battle and battle.ob_settle_info:
                from logic.comsys.observe_ui.JudgeObSettleUI import JudgeObSettleUI
                from logic.comsys.battle.Settle.EndTransitionUI import EndTransitionUI
                self._all_dlgs.append(EndTransitionUI(None, lambda : self._all_dlgs.append(JudgeObSettleUI(None, battle.ob_settle_info)), need_close_self=True, animation_played_callback=None))
            return

    def _play_settle_bgm(self, settle_dict):
        is_draw = settle_dict.get('is_draw', None)
        rank = settle_dict.get('rank', None)
        if not rank and not is_draw:
            return
        else:
            if is_draw:
                global_data.sound_mgr.play_music('normalplace')
                return
            if rank <= 1:
                global_data.sound_mgr.play_music('firstplace')
            else:
                global_data.sound_mgr.play_music('normalplace')
            return

    def _show_death_settle_final(self, group_num, settle_dict, reward, teammate_num, teaminfo, enemy_dict, achievement):
        self.close_all_dlg()
        import wwise
        wwise.SoundEngine.SetRTPCValue('game_settlement', 100)
        global_data.ui_mgr.close_all_ui(exceptions=('WizardTrace', 'ProfileGraphUI',
                                                    'DanmuLinesUI', 'CreditReportResultFail',
                                                    'CreditCompensateUI', 'CreditReportResultSuccess',
                                                    'LobbyConfirmUI2', 'FreeRecordUI',
                                                    'EndHighlightUI', 'VideoManualCtrlUI'))
        from logic.comsys.battle.Death.DeathEndStatisticsUI import DeathStatisticsUI
        from logic.comsys.battle.Clone.CloneEndStatisticsUI import CloneStatisticsUI
        from logic.comsys.battle.MechaDeath.MechaDeathEndStatisticsUI import MechaDeathStatisticsUI
        from logic.comsys.battle.Flag.FlagEndStatisticsUI import FlagStatisticsUI
        from logic.comsys.battle.Occupy.OccupyEndStatisticsUI import OccupyStatisticsUI
        from logic.comsys.battle.Crown.CrownEndStatisticsUI import CrownStatisticsUI
        from logic.comsys.battle.Hunting.HuntingEndStatisticsUI import HuntingStatisticsUI
        from logic.comsys.battle.Crystal.CrystalEndStatisticsUI import CrystalEndStatisticsUI
        from logic.comsys.battle.MutiOccupy.MutiOccupyEndStatisticsUI import MutiOccupyStatisticsUI
        from logic.comsys.battle.ADCrystal.ADCrystalEndStatisticsUI import ADCrystalEndStatisticsUI
        from logic.comsys.battle.Train.TrainEndStatisticsUI import TrainEndStatisticsUI
        from logic.comsys.battle.MechaDeath.GooseBearEndStatisticsUI import GooseBearEndStatisticsUI
        from logic.comsys.battle.Assault.AssaultEndStatisticsUI import AssaultEndStatisticsUI
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CLONE):
            ui_cls = CloneStatisticsUI
        elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_MECHA_DEATH,)):
            ui_cls = MechaDeathStatisticsUI
        elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_FLAG, game_mode_const.GAME_MODE_FLAG2)):
            ui_cls = FlagStatisticsUI
        elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CONTROL):
            ui_cls = OccupyStatisticsUI
        elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CROWN):
            ui_cls = CrownStatisticsUI
        elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_HUNTING):
            ui_cls = HuntingStatisticsUI
        elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CRYSTAL):
            ui_cls = CrystalEndStatisticsUI
        elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_MUTIOCCUPY):
            ui_cls = MutiOccupyStatisticsUI
        elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_ADCRYSTAL):
            ui_cls = ADCrystalEndStatisticsUI
        elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_TRAIN):
            ui_cls = TrainEndStatisticsUI
        elif global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_GOOSE_BEAR,)):
            ui_cls = GooseBearEndStatisticsUI
        elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_ASSAULT):
            ui_cls = AssaultEndStatisticsUI
        else:
            ui_cls = DeathStatisticsUI
        ui = ui_cls(None, group_num, settle_dict, reward, teammate_num, teaminfo, enemy_dict, achievement)
        self._all_dlgs.append(ui)
        scene_type = self._get_settle_scene_type()
        scene_conf = confmgr.get('scenes', scene_type)

        def callback():
            from logic.comsys.battle.Settle.EndTransitionUI import EndTransitionUI
            self._all_dlgs.append(EndTransitionUI(None, lambda : ui.begin_show(), True, lambda : global_data.ex_scene_mgr_agent.add_extra_scene(scene_type)))
            return

        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CRYSTAL):
            from logic.comsys.battle.Crystal.CrystalEndUI import CrystalEndUI
            self._all_dlgs.append(CrystalEndUI(None, settle_dict, callback))
        elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_ADCRYSTAL):
            from logic.comsys.battle.ADCrystal.ADCrystalEndUI import ADCrystalEndUI
            self._all_dlgs.append(ADCrystalEndUI(None, settle_dict, callback))
        elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_TRAIN):
            from logic.comsys.battle.Train.TrainEndUI import TrainEndUI
            self._all_dlgs.append(TrainEndUI(None, settle_dict, callback))
        elif global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_ASSAULT):
            from logic.comsys.battle.Assault.AssaultEndUI import AssaultEndUI
            self._all_dlgs.append(AssaultEndUI(None, settle_dict, callback))
        else:
            from logic.comsys.battle.Death.DeathEndUI import DeathEndUI
            self._all_dlgs.append(DeathEndUI(None, settle_dict, callback))
        global_data.ex_scene_mgr_agent.load_extra_scene_background(scene_type, scene_conf)
        return

    def _show_snatchegg_settle_final(self, group_num, settle_dict, reward, teammate_num, teaminfo, enemy_dict, achievement):
        self.close_all_dlg()
        import wwise
        wwise.SoundEngine.SetRTPCValue('game_settlement', 100)
        from logic.comsys.battle.SnatchEgg.SnatchEggEndUI import SnatchEggEndUI

        def wrapper_callback(directly=False):
            global_data.ui_mgr.close_all_ui(exceptions=('WizardTrace', 'ProfileGraphUI',
                                                        'DanmuLinesUI', 'CreditReportResultFail',
                                                        'CreditCompensateUI', 'CreditReportResultSuccess',
                                                        'LobbyConfirmUI2', 'FreeRecordUI',
                                                        'EndHighlightUI', 'VideoManualCtrlUI',
                                                        'SnatchEggEndUI', 'SnatchEggEndStatisticsUI'))
            from logic.comsys.battle.SnatchEgg.SnatchEggEndStatisticsUI import SnatchEggEndStatisticsUI
            ui = SnatchEggEndStatisticsUI(None, group_num, settle_dict, reward, teammate_num, teaminfo, enemy_dict, achievement)
            self._all_dlgs.append(ui)
            scene_type = self._get_settle_scene_type()
            scene_conf = confmgr.get('scenes', scene_type)

            def callback():
                from logic.comsys.battle.Settle.EndTransitionUI import EndTransitionUI
                self._all_dlgs.append(EndTransitionUI(None, lambda : ui.begin_show(), True, lambda : global_data.ex_scene_mgr_agent.add_extra_scene(scene_type)))
                return

            if not directly:
                global_data.ex_scene_mgr_agent.load_extra_scene_background(scene_type, scene_conf)
                global_data.game_mgr.next_exec(callback)
            else:
                global_data.ex_scene_mgr_agent.load_extra_scene_background(scene_type, scene_conf)
                callback()
            return

        is_in_spec = False
        if global_data.player and global_data.player.logic:
            if global_data.player.logic.ev_g_is_in_spectate():
                is_in_spec = True
        if not is_in_spec:
            self._all_dlgs.append(SnatchEggEndUI(None, settle_dict, wrapper_callback))
        else:
            wrapper_callback(True)
        return

    def _show_koth_settle_final(self, group_num, settle_dict, reward, teammate_num, teaminfo, achievement):
        self.close_all_dlg()
        rank = settle_dict.get('rank')
        statistics_finished_cb = functools.partial(self._show_koth_camp_settle_statistics, settle_dict)
        finished_cb = functools.partial(self._show_koth_settle_statistics, group_num, settle_dict, reward, teammate_num, teaminfo, achievement, statistics_finished_cb)
        if rank <= 3:
            from logic.comsys.battle.Settle.KothEndWinUI import KothEndWinUI
            self._all_dlgs.append(KothEndWinUI(None, settle_dict, finished_cb))
        else:
            self._show_koth_settle_statistics(group_num, settle_dict, reward, teammate_num, teaminfo, achievement, finished_cb)
        return

    def _show_koth_settle_statistics(self, group_num, settle_dict, reward, teammate_num, teaminfo, achievement, finished_cb):
        self.close_all_dlg()
        from logic.comsys.battle.Settle.KothEndStatisticsUI import KothEndStatisticsUI
        dlg = KothEndStatisticsUI(None, group_num, settle_dict, reward, teammate_num, teaminfo, achievement, finished_cb)
        self._all_dlgs.append(dlg)
        return

    def _show_koth_camp_settle_statistics(self, settle_dict):
        self.close_all_dlg()
        from logic.comsys.battle.Settle.KothEndCampStatisticsUI import KothEndCampStatisticsUI
        dlg = KothEndCampStatisticsUI(None, settle_dict)
        self._all_dlgs.append(dlg)
        return

    def _show_ffa_settle_final(self, group_num, settle_dict, reward, teammate_num, teaminfo, total_fighter_num):
        self.close_all_dlg()
        import wwise
        wwise.SoundEngine.SetRTPCValue('game_settlement', 100)
        global_data.ui_mgr.close_all_ui(exceptions=('WizardTrace', 'ProfileGraphUI',
                                                    'DanmuLinesUI', 'FreeRecordUI',
                                                    'EndHighlightUI', 'VideoManualCtrlUI'))
        rank = settle_dict.get('rank')
        from logic.comsys.battle.Settle.FFAEndSceneUI import FFAEndSceneUI
        self._all_dlgs.append(FFAEndSceneUI(None, settle_dict, reward, teammate_num, teaminfo, total_fighter_num))

        def on_rank_anim_end_callback():
            global_data.ui_mgr.close_ui('EndAnimUI')
            global_data.ex_scene_mgr_agent.add_extra_scene(scene_type)
            global_data.emgr.start_settle_scene_camera.emit()

        from logic.comsys.battle.Settle.EndAnimUI import EndAnimUI
        self._all_dlgs.append(EndAnimUI(None, rank, on_rank_anim_end_callback))
        scene_type = self._get_settle_scene_type()
        scene_conf = confmgr.get('scenes', scene_type)
        global_data.ex_scene_mgr_agent.load_extra_scene_background(scene_type, scene_conf)
        return

    def _show_armrace_settle_final(self, group_num, settle_dict, reward, teammate_num, teaminfo, total_fighter_num):
        self.close_all_dlg()
        import wwise
        wwise.SoundEngine.SetRTPCValue('game_settlement', 100)
        global_data.ui_mgr.close_all_ui(exceptions=('WizardTrace', 'ProfileGraphUI',
                                                    'DanmuLinesUI', 'FreeRecordUI',
                                                    'EndHighlightUI', 'VideoManualCtrlUI'))
        rank = settle_dict.get('rank')
        from logic.comsys.battle.Settle.ArmRaceEndSceneUI import ArmRaceEndSceneUI
        self._all_dlgs.append(ArmRaceEndSceneUI(None, settle_dict, reward, teammate_num, teaminfo, total_fighter_num))

        def on_rank_anim_end_callback():
            global_data.ui_mgr.close_ui('EndAnimUI')
            global_data.ex_scene_mgr_agent.add_extra_scene(scene_type)
            global_data.emgr.start_settle_scene_camera.emit()

        from logic.comsys.battle.Settle.EndAnimUI import EndAnimUI
        self._all_dlgs.append(EndAnimUI(None, rank, on_rank_anim_end_callback))
        scene_type = self._get_settle_scene_type()
        scene_conf = confmgr.get('scenes', scene_type)
        global_data.ex_scene_mgr_agent.load_extra_scene_background(scene_type, scene_conf)
        return

    def _show_gvg_settle_final(self, group_num, settle_dict, reward, teaminfo, achievement):
        self.close_all_dlg()
        import wwise
        wwise.SoundEngine.SetRTPCValue('game_settlement', 100)
        global_data.ui_mgr.close_all_ui(exceptions=('WizardTrace', 'DanmuLinesUI',
                                                    'CreditReportResultFail', 'CreditCompensateUI',
                                                    'CreditReportResultSuccess',
                                                    'LobbyConfirmUI2', 'FreeRecordUI',
                                                    'EndHighlightUI', 'VideoManualCtrlUI'))
        from logic.comsys.battle.Settle.GVGEndSceneUI import GVGEndSceneUI
        from logic.comsys.battle.Settle.DuelEndSceneUI import DuelEndSceneUI
        mode_type = global_data.game_mode.get_mode_type()
        end_cls = DuelEndSceneUI if mode_type == game_mode_const.GAME_MODE_DUEL else GVGEndSceneUI
        if not global_data.is_judge_ob or mode_type == game_mode_const.GAME_MODE_DUEL:
            ui = end_cls(None, group_num, settle_dict, reward, teaminfo, achievement)
            self._all_dlgs.append(ui)
            scene_type = self._get_settle_scene_type()
            scene_conf = confmgr.get('scenes', scene_type)
            if mode_type == game_mode_const.GAME_MODE_DUEL and global_data.is_judge_ob:

                def ui_callback():
                    ui.begin_judge_show()

            else:

                def ui_callback():
                    ui.begin_show()

            def callback():
                from logic.comsys.battle.Settle.EndTransitionUI import EndTransitionUI
                self._all_dlgs.append(EndTransitionUI(None, lambda : ui_callback(), True, lambda : global_data.ex_scene_mgr_agent.add_extra_scene(scene_type)))
                return

            from logic.comsys.battle.Settle.GVGEndUI import GVGEndUI
            self._all_dlgs.append(GVGEndUI(None, settle_dict, callback))
            global_data.ex_scene_mgr_agent.load_extra_scene_background(scene_type, scene_conf)
        else:

            def show_judge_panel():
                ob_end_data_list = self.prepare_gvg_judge_ob_data(settle_dict, teaminfo)
                from logic.comsys.observe_ui.JudgeObSettleUI import JudgeObSettleUI
                self._all_dlgs.append(JudgeObSettleUI(None, ob_end_data_list))
                return

            ret_callback = None
            if mode_type == game_mode_const.GAME_MODE_DUEL:
                ui2 = None
                ret_callback = show_judge_panel
            else:
                from logic.comsys.battle.gvg.GVGJudgeResultUI import GVGJudgeResultUI
                ui2 = GVGJudgeResultUI(None, group_num, settle_dict, reward, teaminfo, achievement)
                self._all_dlgs.append(ui2)
                ui2.set_end_callback(show_judge_panel)

            def callback():
                from logic.comsys.battle.Settle.EndTransitionUI import EndTransitionUI
                self._all_dlgs.append(EndTransitionUI(None, lambda : (ui2 and ui2.is_valid() and ui2.set_settle_dict(settle_dict), ui2 and ui2.is_valid() and ui2.begin_result_show(),
                 ret_callback and ret_callback()), False, lambda : None))
                return

            from logic.comsys.battle.Settle.GVGEndUI import GVGEndUI
            self._all_dlgs.append(GVGEndUI(None, settle_dict, callback))
        return

    def _show_improvise_settle_final(self, group_num, settle_dict, reward, teaminfo, achievement):
        self.close_all_dlg()
        import wwise
        wwise.SoundEngine.SetRTPCValue('game_settlement', 100)
        global_data.ui_mgr.close_all_ui(exceptions=('WizardTrace', 'DanmuLinesUI',
                                                    'CreditReportResultFail', 'CreditCompensateUI',
                                                    'CreditReportResultSuccess',
                                                    'LobbyConfirmUI2', 'FreeRecordUI',
                                                    'EndHighlightUI', 'VideoManualCtrlUI'))
        cur_round = settle_dict.get('cur_round', 0)
        is_draw = settle_dict.get('is_draw', False)
        self_group_id = settle_dict.get('group_id', None)
        group_points_dict = settle_dict.get('group_points_dict', {})
        group_points_dict_int_key = {}
        for key in six_ex.keys(group_points_dict):
            if not isinstance(key, six.string_types):
                continue
            try:
                int_key = int(key)
            except Exception as e:
                log_error(e)
            else:
                group_points_dict_int_key[int_key] = group_points_dict[key]

        from logic.comsys.battle.Settle.ImproviseEndSceneUI import ImproviseEndSceneUI
        ui = ImproviseEndSceneUI(None, group_num, settle_dict, reward, teaminfo, achievement)
        self._all_dlgs.append(ui)
        scene_type = self._get_settle_scene_type()
        scene_conf = confmgr.get('scenes', scene_type)

        def cb():
            from logic.comsys.battle.Settle.EndTransitionUI import EndTransitionUI
            self._all_dlgs.append(EndTransitionUI(None, lambda : ui.begin_show(), True, lambda : global_data.ex_scene_mgr_agent.add_extra_scene(scene_type)))
            return

        from logic.comsys.battle.Improvise.ImproviseRoundSettleUI import SETTLE_WIN, SETTLE_DRAW, SETTLE_LOSE
        if is_draw:
            settle_result = SETTLE_DRAW
        else:
            rank = settle_dict.get('rank', 2)
            if rank == 1:
                settle_result = SETTLE_WIN
            else:
                settle_result = SETTLE_LOSE
        from logic.comsys.battle.Improvise.ImproviseRoundSettleUI import ImproviseRoundSettleUI
        pre_end_ui = ImproviseRoundSettleUI(None, settle_result, group_points_dict_int_key, self_group_id, click_close_cb=cb)
        self._all_dlgs.append(pre_end_ui)
        global_data.ex_scene_mgr_agent.load_extra_scene_background(scene_type, scene_conf)
        return

    def _show_zombieffa_settle_final(self, group_num, settle_dict, reward, teaminfo, total_fighter_num):
        import wwise
        from logic.comsys.battle.Settle.EndTransitionUI import EndTransitionUI
        self.close_all_dlg()
        wwise.SoundEngine.SetRTPCValue('game_settlement', 100)
        global_data.ui_mgr.close_all_ui(exceptions=('WizardTrace', 'ProfileGraphUI',
                                                    'DanmuLinesUI', 'FreeRecordUI',
                                                    'EndHighlightUI', 'VideoManualCtrlUI'))
        from logic.comsys.battle.Settle.ZombieFFASceneUI import ZombieFFASceneUI
        scene_ui = ZombieFFASceneUI(None, group_num, settle_dict, reward, teaminfo, total_fighter_num)
        self._all_dlgs.append(scene_ui)
        scene_type = self._get_settle_scene_type()
        scene_conf = confmgr.get('scenes', scene_type)

        def callback():
            self._all_dlgs.append(EndTransitionUI(None, lambda : global_data.ex_scene_mgr_agent.add_extra_scene(scene_type), True, lambda : global_data.emgr.start_settle_scene_camera.emit()))
            return

        from logic.comsys.battle.ZombieFFA.ZombieFFAEndUI import ZombieFFAEndUI
        self._all_dlgs.append(ZombieFFAEndUI(None, settle_dict, callback))
        global_data.ex_scene_mgr_agent.load_extra_scene_background(scene_type, scene_conf)
        return

    def _show_pve_settle_final(self, group_num, settle_dict, reward, teammate_num, teaminfo, total_fighter_num):
        import wwise
        from logic.comsys.battle.Settle.PVEEndTransitionUI import PVEEndTransitionUI
        from logic.comsys.battle.pve.PVEEndUI import PVEEndUI
        from logic.comsys.battle.pve.PVEEndVxUI import PVEEndVxUI
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        from bson.objectid import ObjectId
        self.close_all_dlg()
        wwise.SoundEngine.SetRTPCValue('game_settlement', 100)
        global_data.ui_mgr.close_all_ui(exceptions=('WizardTrace', 'ProfileGraphUI',
                                                    'DanmuLinesUI', 'FreeRecordUI',
                                                    'EndHighlightUI', 'VideoManualCtrlUI'))
        for info in six_ex.values(teaminfo):
            statistics = info.get('statistics', {})
            info['role_name'] = info.get('char_name', '')
            info['chossed_breakthrough'] = statistics.get('pve_choosed_breakthrough', {})
            info['choosed_blesses'] = statistics.get('pve_choosed_blesses', {})
            pve_sell_blesses = statistics.get('pve_sell_blesses', {})
            pve_donate_blesses = statistics.get('pve_donate_blesses', {})
            removed_blesses = {}
            removed_blesses.update(pve_sell_blesses)
            removed_blesses.update(pve_donate_blesses)
            info['removed_blesses'] = removed_blesses
            statistics['total_damage'] = int(statistics.get('damage_to_monster', 0))

        if global_data.player:
            player_info = {}
            player_info['head_photo'] = global_data.player.get_head_photo()
            player_info['head_frame'] = global_data.player.get_head_frame()
            player_info['role_name'] = global_data.player.get_name()
            statistics = settle_dict.get('statistics', {})
            player_info['mecha_id'] = int(settle_dict.get('mecha_id', 8001))
            player_info['chossed_breakthrough'] = settle_dict.get('chossed_breakthrough', {})
            player_info['choosed_blesses'] = settle_dict.get('choosed_blesses', {})
            pve_sell_blesses = statistics.get('pve_sell_blesses', {})
            pve_donate_blesses = statistics.get('pve_donate_blesses', {})
            removed_blesses = {}
            removed_blesses.update(pve_sell_blesses)
            removed_blesses.update(pve_donate_blesses)
            player_info['removed_blesses'] = removed_blesses
            if removed_blesses:
                settle_dict['removed_blesses'] = removed_blesses
            player_info['pve_mecha_base_info'] = {}
            player_info['pve_mecha_base_info']['pve_mecha_atk'] = global_data.mecha.logic.ev_g_base_atk_power() if global_data.mecha and global_data.mecha.logic else 0
            player_info['pve_mecha_base_info']['pve_mecha_shield'] = global_data.mecha.logic.ev_g_max_shield() if global_data.mecha and global_data.mecha.logic else 0
            player_info['pve_mecha_base_info']['pve_mecha_hp'] = global_data.mecha.logic.ev_g_max_hp() if global_data.mecha and global_data.mecha.logic else 0
            player_info['statistics'] = {}
            player_info['statistics']['survival'] = float(statistics.get('survival', 0))
            player_info['statistics']['kill_monster'] = int(statistics.get('kill_monster', 0))
            player_info['statistics']['total_damage'] = statistics.get('total_damage', 0)
            eid = ObjectId(global_data.player.id)
            teaminfo[eid] = player_info
        self._all_dlgs.append(PVEEndUI(settle_dict=settle_dict, reward=reward, teammate_settle_dict=teaminfo))
        scene_type = SCENE_PVE_END_UI
        scene_conf = confmgr.get('scenes', scene_type)
        scene_data = {}
        extra_detail = settle_dict.get('extra_detail', {})
        scene_data['chapter'] = extra_detail.get('chapter', 1)
        scene_data['difficulty'] = extra_detail.get('difficulty', 1)

        def callback():
            self._all_dlgs.append(PVEEndTransitionUI(None, lambda : global_data.ex_scene_mgr_agent.add_extra_scene(scene_type, scene_data), True, lambda ui=global_data.ui_mgr.get_ui('PVEEndUI'): ui and ui.show()))
            return

        self._all_dlgs.append(PVEEndVxUI(None, settle_dict, callback))
        global_data.ex_scene_mgr_agent.load_extra_scene_background(scene_type, scene_conf)
        return

    def _show_nbomb_settle_final(self, group_num, settle_dict, reward, teammate_num, teaminfo, achievement, total_fighter_num):
        from common.cinematic.VideoPlayer import VideoPlayer
        video_path = 'video/pvp_nbomb.mp4'

        def _on_stop_cb():
            global_data.emgr.nbomb_clear_war.emit()
            self._show_settle_statistics_helper(group_num, settle_dict, reward, teammate_num, teaminfo, achievement, total_fighter_num)

        import os
        VideoPlayer().play_video(video_path, _on_stop_cb, repeat_time=1, can_jump=False)

    def _show_settle_final(self, group_num, settle_dict, reward, teammate_num, teaminfo, achievement, total_fighter_num):
        end_anim_ui = global_data.ui_mgr.get_ui('EndAnimUI')
        end_scene_ui = global_data.ui_mgr.get_ui('EndSceneUI')
        end_transition_ui = global_data.ui_mgr.get_ui('EndTransitionUI')
        end_statistics_ui = global_data.ui_mgr.get_ui('EndStatisticsUI')
        end_settlement_chart_ui = global_data.ui_mgr.get_ui('EndSettlementChartUI')
        end_settlement_chart_ui2 = global_data.ui_mgr.get_ui('EndTDMSettlementChartUI2')
        end_exp_ui = global_data.ui_mgr.get_ui(settle_system_utils.get_end_exp_ui_cls().__name__)
        quit_from_spectate = settle_dict.get('quit_from_spectate', False)
        if quit_from_spectate:
            if end_anim_ui:
                global_data.ui_mgr.close_ui('EndAnimUI')
                end_anim_ui = None
            self.close_all_dlg()
        if end_anim_ui or end_scene_ui or end_statistics_ui or end_exp_ui or end_transition_ui or end_settlement_chart_ui or end_settlement_chart_ui2:
            return
        else:
            rank = settle_dict.get('rank')
            quit_battle = settle_dict.get('quit_battle', False)
            dead_reason = settle_dict.get('dead_reason', 0)
            show_func = functools.partial(self._show_settle_statistics_helper, group_num, settle_dict, reward, teammate_num, teaminfo, achievement, total_fighter_num)
            exit_callback = show_func
            if settle_dict.get('escape_battle', False):
                self.close_all_dlg()
                exit_callback()
                return
            from logic.comsys.battle.Settle.EndAnimUI import EndAnimUI
            if rank >= 3:
                self.close_all_dlg()
                player = global_data.player
                if not quit_battle and player and player.logic and player.logic.ev_g_all_groupmates_dead():
                    replay_data = settle_dict.get('reply_data', {})
                    if not getattr(self, 'has_been_disable_stage', False):
                        end_anim_ui_cb = lambda sd=replay_data, gn=group_num, cb=exit_callback: self.show_end_death_replay_ui(sd, gn, cb)
                    else:
                        end_anim_ui_cb = lambda gn=group_num, rd=replay_data, cb=exit_callback: self.show_end_continue_ui(gn, rd, cb)
                    self._all_dlgs.append(EndAnimUI(None, rank, end_anim_ui_cb, dead_reason))
                else:
                    exit_callback()
            else:
                if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_SURVIVALS,)) and rank == 1:

                    def celebrate_func():
                        from logic.comsys.battle.Settle.EndCelebrateUI import EndCelebrateUI
                        global_data.ui_mgr.close_ui('EndAnimUI')
                        if global_data.player:
                            global_data.player.celebrate_win()
                        global_data.emgr.celebrate_win_stage_event.emit()
                        EndCelebrateUI()
                        ui = global_data.ui_mgr.get_ui('EndCelebrateUI')
                        if ui:
                            ui.set_close_callback(show_func)

                    exit_callback = celebrate_func
                else:
                    self.close_all_dlg()
                self._all_dlgs.append(EndAnimUI(None, rank, exit_callback, dead_reason))
            return

    def show_end_death_replay_ui(self, replay_dict, group_num, exit_callback=None):
        self.show_end_continue_ui(group_num, replay_dict, exit_callback, next_step_cb=lambda rd=replay_dict: self._show_end_death_replay_ui(rd))

    def _show_end_death_replay_ui(self, replay_dict):
        from logic.comsys.battle.Settle.EndDeathReplayUI import EndDeathReplayUI
        self._all_dlgs.append(EndDeathReplayUI(None, replay_dict))
        end_anim_ui = global_data.ui_mgr.get_ui('EndAnimUI')
        if end_anim_ui:
            end_anim_ui.add_hide_count('EndDeathReplayUI')
        return

    def show_end_continue_ui(self, group_num, replay_dict, exit_callback=None, next_step_cb=None):
        from logic.comsys.battle.Settle.EndContinueUI import EndContinueUI
        ui = EndContinueUI()
        ui.show()
        ui.on_show_imp(group_num, replay_dict, exit_callback, next_step_cb=next_step_cb)
        if ui not in self._all_dlgs:
            self._all_dlgs.append(ui)

    def show_settle_exp(self, settle_dict, reward):
        battle = global_data.battle
        if battle:
            if battle.get_is_round_competition() or battle.need_skip_end_exp_ui():
                global_data.player and global_data.player.quit_battle(True)
                return
        from logic.gcommon.ctypes.BattleReward import BattleReward
        battle_reward = BattleReward()
        battle_reward.init_from_dict(settle_dict.get('reward', {}))
        exp_dict = {'old_lv': settle_dict.get('lv', 0),
           'old_exp': settle_dict.get('exp', 0),
           'add_exp': battle_reward.exp
           }
        cls = settle_system_utils.get_end_exp_ui_cls()
        self._all_dlgs.append(cls(None, settle_dict, battle_reward, exp_dict, lambda : None))
        return

    def show_settlement_chart_ui(self, settle_dict, teammate_info, reward, achievement_list):
        self._all_dlgs.append(EndSettlementChartUI(None, settle_dict, teammate_info, reward, achievement_list))
        return

    def show_settlement_tdm_chart_ui(self, settle_dict, all_info, reward):
        self._all_dlgs.append(EndTDMSettlementChartUI(None, settle_dict, all_info, reward))
        return

    def show_settlement_tdm_chart2_ui(self, settle_dict, all_info, reward):
        self._all_dlgs.append(EndTDMSettlementChartUI2(None, settle_dict, all_info, reward))
        return

    def _get_settle_scene_type(self):
        if CGameModeManager().get_enviroment() in ('night', 'granbelm', 'bounty'):
            return SCENE_NIGHT_SETTLE
        else:
            return SCENE_NORMAL_SETTLE

    def _show_settle_statistics_helper(self, group_num, settle_dict, reward, teammate_num, teaminfo, achievement, total_fighter_num):
        rank = settle_dict.get('rank')
        is_done = True
        if rank >= 3:
            is_done = False
        import wwise
        wwise.SoundEngine.SetRTPCValue('game_settlement', 100)
        self.close_all_dlg()
        global_data.emgr.stop_player_damage_event.emit()
        global_data.ui_mgr.close_all_ui(exceptions=('WizardTrace', 'ProfileGraphUI',
                                                    'DanmuLinesUI', 'FreeRecordUI',
                                                    'CreditReportResultFail', 'CreditCompensateUI',
                                                    'CreditReportResultSuccess',
                                                    'LobbyConfirmUI2', 'EndHighlightUI',
                                                    'VideoManualCtrlUI'))
        from logic.comsys.battle.Settle.EndSceneUI import EndSceneUI
        self._all_dlgs.append(EndSceneUI(None, settle_dict, reward, teammate_num, teaminfo, achievement, is_done, total_fighter_num))
        scene_type = self._get_settle_scene_type()
        scene_conf = confmgr.get('scenes', scene_type)

        def after_trans():
            ui = global_data.ui_mgr.get_ui('EndSceneUI')
            if ui:
                ui.begin_show()

        def load_settle_scene_callback():
            from logic.comsys.battle.Settle.EndTransitionUI import EndTransitionUI
            self._all_dlgs.append(EndTransitionUI(None, lambda : after_trans(), True, lambda : global_data.ex_scene_mgr_agent.add_extra_scene(scene_type)))
            return

        global_data.ex_scene_mgr_agent.load_extra_scene_background(scene_type, scene_conf, load_settle_scene_callback)
        return

    def get_test_args(self):
        settle_dict = {'statistics': {'survival': 387,
                          'move_dist': 258
                          },
           'damage': 20,
           'move_dist': 100,
           'pick_item': 1,
           'exp': 50,
           'rank': 2,
           'lv': 4,
           'gold': 200,
           'score': {'combat_score_increment': 0,
                     'overall_score_increment': 10,
                     'survival_score_increment': 15
                     },
           'is_survival': False,
           'match_score_diff': 0,
           'reward': {'1': {'gold': 486,
                            'exp': 900
                            }
                      },
           'poison_level': 2
           }
        from logic.gcommon.ctypes.BattleReward import BattleReward
        battle_reward = BattleReward()
        battle_reward.init_from_dict(settle_dict.get('reward', {}))
        return (
         settle_dict, battle_reward)

    def prepare_gvg_judge_ob_data(self, settle_dict, teammate_info):
        if global_data.is_judge_ob:
            my_group_id = str(settle_dict.get('group_id', 1))
            enemy_group_id = str(3 - int(my_group_id))
            win_ending = settle_dict.get('rank', 2) == 1
            draw_ending = settle_dict.get('is_draw', False)
            from bson.objectid import ObjectId
            my_group_data = settle_dict['settle_detail'][my_group_id]
            enemy_group_data = settle_dict['settle_detail'][enemy_group_id]
            end_list = []

            def append_group_data(group_data, rank):
                member_info = {}
                member_settle_dict = {}
                for mid, mdata in six.iteritems(group_data):
                    member_info[mid] = {'char_name': mdata[1]}
                    member_settle_dict[mid] = {'statistics': {}}
                    member_settle_dict[mid]['statistics'] = teammate_info.get(ObjectId(mid), {}).get('statistics', {})

                end_list.append({'member_settle_dict': member_settle_dict,'member_info': member_info,'rank': rank})

            if not draw_ending:
                if win_ending:
                    append_group_data(my_group_data, 1)
                    append_group_data(enemy_group_data, 2)
                else:
                    append_group_data(enemy_group_data, 1)
                    append_group_data(my_group_data, 2)
            else:
                append_group_data(my_group_data, 1)
                append_group_data(enemy_group_data, 1)
            return end_list
        else:
            return []