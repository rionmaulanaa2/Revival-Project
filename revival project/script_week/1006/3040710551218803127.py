# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/basepanel.py
from __future__ import absolute_import
from __future__ import print_function
import six
import time
from cocosui import cc, ccui
import world
from common.uisys.uielment.CCNode import CCNode
from common.uisys.uielment.CCUIWidget import CCUIWidget
from common.utils.ui_utils import is_ui_object
from common.uisys.ui_proxy import trans2ProxyObj
from common.framework import Singleton
from common.algorithm.traversal import traversal_dict
from common.const import uiconst
from logic.vscene import scene_type
from common.cfg import confmgr
import game
import game3d
from logic.client.const import pc_const
from copy import deepcopy
MAIN_UI_LIST = {
 'LobbyUI', 'MainChat', 'MainFriend', 'FriendChat', 'MallMainUI', 'LotteryMainUI', 'ItemsBookMainUI', 'RoomListUI', 'RoomUI', 'AirshipDriveUI', 'MainRank', 'MechaTopRank', 'LobbyConversationUI', 'LiveMainUI',
 'SecondConfirmDlg2', 'LoginReconnectConfirmDlg', 'ShareUI', 'ShareScreenCaptureUI', 'LanguageSettingUI', 'LobbyRockerUI', 'MechaDisplay', 'MechaDetails',
 'SeasonPassUI', 'NewbiePassUI', 'FriendApplyList', 'RoleInfoUI', 'RoleDIY', 'RoleChooseUI', 'LobbyBagUI', 'MainEmail', 'SeasonPassRetrospectChooseUI', 'RetroSpectMainUI', 'SeasonPassActiveGiftUI', 'SeasonPassActiveBuyLevelUI',
 'ActivityCenterMainUI', 'ActivityAnnivMainUI', 'TaskMainUI', 'MainHouseUI', 'ChargeUI', 'ChargeUINew', 'ChangeHeadUI', 'PlayerInfoUI', 'ModelArrowUI',
 'RoleAndSkinBuyConfirmUI', 'RoleAndSkinTogetherBuyConfirmUI', 'RecommendGiftBuyConfirmUI', 'GroceriesBuyConfirmUI', 'ItemSkinBuyConfirmUI', 'ClanCardUI', 'ClanJoinMainUI', 'PreviewReward', 'ClanApplyJoinUI',
 'MatchMode', 'SeasonMainUI', 'TierRewardUI', 'ClanMainUI', 'CardBuyCheck', 'LobbyRecruimentEndAddFriend',
 'LobbySceneCaptureListenerUI', 'MechaProficiencyDetailsUI', 'KothEndFullScreenBg', 'SkinImproveWidgetUI', 'RoomListUINew', 'RoomUINew', 'RoleSkinDefineUI',
 'CommonBuyListUI', 'SkinDefineUI', 'SkinDefineBuyUI', 'SkinDefineGuideColorUI', 'SkinDefineGuideDecalUI',
 'BuySeasonCardUITestA', 'BuySeasonCardUI', 'RoleSkinBuyShowUI', 'LotteryExchangeMallUI', 'LotteryActivityChooseUI', 'RoleSkinDecorationStoreUI',
 'CareerMainUI', 'CareerBadgeWallConfigUI', 'CareerBadgeWallConfigUI', 'GiftBoxSkinUI', 'GiftBoxItemUI', 'InscriptionMainUI', 'AlphaPlanMainUI', 'CertificateMainUI', 'CertificateMainUIBg',
 'RoleBondTipsUI', 'MultiRewardUI', 'MultiRewardPreview', 'MultiChosenRewardUI', 'LobbyItemPreviewUI', 'BondSkillLevelUp',
 'FightEndUI', 'FightEndFullScreenBg', 'GuideAppComment', 'FaceCertificationUI', 'NewChatPigeon', 'TeamHallUI',
 'LobbySkinPreViewUI', 'GlMainRank', 'SummerGameRewardUI', 'ArmRaceStatisticsShareUI', 'JudgeChooseFactionUI',
 'LobbyASMainUI', 'PrivilegeSettingUI', 'PrivilegeSettingTips', 'ClanReportUI', 'RoomReportUI', 'LobbyMusicUI', 'PetMainUI',
 'IntimacyRemoveList', 'NormalAttendSignUI', 'AlphaPlanNewBieAttendUI', 'Newbie2ndMechaUI', 'LotteryTicketBuyConfirmUI', 'LobbyMessageBoardMainUI', 'MessageReplyUI', 'MessageLeftUI', 'LobbyVisitMainUI', 'WinningStreakUI',
 'FightSightUI', 'BattleInfoUI', 'DrugUI', 'DrugUIPC', 'FightSightUI', 'HpInfoUI', 'HpInfoUIPC', 'MobileInfoUI', 'PickUI', 'TeammateUI', 'WeaponBarSelectUI',
 'AimLensUI', 'BagUI', 'DriveUI', 'FireRockerUI', 'MoveRockerUI', 'PostureControlUI', 'ThrowRockerUI', 'ThrowRockerUIPC',
 'ParachuteInfoUI', 'ParachutePlaneUI', 'BattleSettingUI', 'CamaraSettingUI', 'SensitySettingUI', 'BigMapUI', 'SmallMapUI', 'SmallMapUIPC', 'MidMapUI',
 'FrontSightUI', 'SurviveInfoUI', 'ObserveUI', 'ObserveUIPC', 'FightChatUI', 'FightChatUIPC', 'BegChatUI', 'SOSUI', 'SceneInteractionUI', 'SceneInteractionUIPC', 'FightLeftShotUI', 'JudgeBigMapUI',
 'ObserveInfoUI', 'TeamBloodUI', 'TeamBloodUIPC', 'JudgeTeamBloodUI', 'JudgeObserveUINew', 'JudgeObserveUINewPC', 'JudgeLoadingUI', 'BattleBuffUI', 'BattleBuffUIPC', 'ScalePlateUI', 'ScalePlateUIPC', 'BulletReloadUI',
 'MechaSummonUI', 'MechaControlMain', 'MechaControlMainPC', 'MechaFuelUI', 'MechaHpInfoUI', 'MechaHpInfoUIPC', 'MechaBulletReloadUI', 'StateChangeUI', 'StateChangeUIPC', 'ShareUI',
 'BulletReloadProgressUI', 'FightReadyTipsUI', 'BattleRightTopUI', 'BattleRightTopUIPC', 'BattleLeftBottomUI', 'Mecha8004HeatUI', 'Mecha8007SubUI', 'Mecha8007SubUI2', 'Mecha8006RushUI', 'Mecha8011DragonUI', 'Mecha8014LockedUI', 'Mecha8018SubUI',
 'MechaTransUI', 'BattleInfoMessageVisibleUI', 'MechaTestSightUI', 'MechaUI', 'MechaUIPC', 'MainSettingUI', 'BattleFightCapacity', 'BattleFightCapacityPC', 'BattleFightMeow', 'BattleFightMeowPC', 'Mecha8023SubUI', 'Mecha8024RushUI', 'Mecha8025SecondAimUI', 'Mecha8035LockedUIEndAnimUI',
 'EndWithGoldUI', 'EndWithSliverUI', 'EndStatisticsUI', 'MechaChargeUI', 'BriefRankUI', 'RankBeginUI', 'MechaCancelUI', 'HumanCancelUI', 'FightLocateUI', 'Mecha8029RushUI',
 'MechaModuleSpSelectUI', 'FightStateUI', 'FightStateUIPC', 'MechaCockpitUI', 'GuideUI', 'PCGuideUI', 'LeaveGuideUI', 'KingBattleUI', 'FightBagUI',
 'KothCampShopEntryUI', 'KothCampShopUI', 'QuickMarkBtn', 'QuickMarkBtnPC', 'QuickMarkBtnMecha', 'PVEQuickMarkBtn', 'BeaconTowerOccupyUI', 'MapGuideUI', 'MechaTipsUI', 'GameVoiceTextUI', 'UserReportUI',
 'DeathWeaponChooseBtn', 'DeathBeginCountDown', 'FFAScoreUI', 'FFABeginCountDown', 'FFAFinishCountDown', 'FFAScoreDetailsUI', 'GVGTopScoreUI', 'GVGScoreDetailsUI', 'GVGScoreMsgUI',
 'ExerciseCommandUI', 'ExerciseMechaModuleUI', 'ExerciseDPSInfoUI', 'ExerciseWeaponConfUI', 'ExerciseEquipmentUI', 'ExerciseWeaponListUI', 'ExerciseTimerUI', 'ExerciseDistanceUI', 'BattleAceCoinUI', 'BattleAceCoinUIPC',
 'GranbelmRuneConfUI', 'GranbelmRuneConfUIPC', 'GranbelmRuneListUI', 'MagicRuneConfUI', 'MagicRuneConfUIPC', 'MagicRuneListUI', 'FightKillNumberUI', 'BattleControlUIPC',
 'ImproviseTopScoreUI', 'ImproviseRoundPrompUI', 'GulagInfoUI',
 'MechaModuleEffectiveUI', 'MechaModuleEffectiveUIPC', 'BattleSignalInfoUI', 'NewbieMechaTipsUI', 'NewbieStageSideTipUI',
 'RogueGiftTopRightUI', 'RogueGiftTopRightUIPC', 'RogueGiftPickUI', 'EndCelebrateUI', 'BattleSceneOnlyUI', 'GVGTopScoreJudgeUI',
 'ArmRaceScoreUI', 'ArmRaceScoreDetailsUI', 'ArmRaceBeginCountDown', 'ArmRaceFinishCountDown', 'ArmRaceStartUI',
 'ArenaWaitUI', 'ArenaApplyUI', 'ArenaConfirmUI', 'ArenaTopUI', 'ArenaEndUI', 'KizunaLiveBattleMainUI', 'KizunaHitCallUI', 'KizunaSongbarUI', 'KizunaLotteryWidgetUI',
 'KizunaShowtimeIntroUI', 'KizunaConcertViewUI', 'KizunaLiveEndUI', 'KizunaDrugUI', 'OccupyProgressUI', 'OccupyScoreDetailsUI', 'FlagScoreDetailsUI', 'FlagTopScoreUI', 'FlagEndStatisticsUI,', 'CrownTopScoreUI', 'CrownScoreDetailsUI', 'CrownEndStatisticsUI',
 'CrownTopCounterUI', 'CrownGuideUI', 'GVGChooseMecha', 'GVGReadyUI', 'FireSurvivalBattleTopCounterUI', 'LotteryExclusiveGiftUI', 'MutiOccupyScoreDetailsUI', 'MutiOccupySkillUI', 'MutiOccupyBattleUI', 'MutiOccupySkillUIPC', 'DeathRogueGiftTopRightUI',
 'TrainMarkUI', 'TrainSkillUI', 'TrainSkillSelectUI', 'TrainTopProgUI', 'BattleGiveUpUI', 'ADCrystalTopScoreUI', 'Mecha8033CarUI', 'NBombCoreCollectUI',
 'PVEBlessConfUI', 'PVETipsUI', 'PVERadarMapUI', 'PVERadarMapUIPC', 'PVEBagUI', 'PVELobbyUI', 'PVEEndUI', 'PVEKeyBuyUI',
 'PVEMainUI', 'PVELevelWidgetUI', 'PVEMechaWidgetUI', 'PVETalentWidgetUI', 'PVEStoryWidgetUI', 'PVEEquipWidgetUI', 'PVEBookWidgetUI', 'PVEDebrisWidgetUI', 'PVEPetWidgetUI',
 'PVEBreakConfUI', 'PVEInfoUI', 'PVEShopUI', 'PVEMechaUpgradePanel', 'PVEResUI', 'PVESuggestUI', 'PVEEndStatisticsUI', 'PVETeamBloodUI',
 'PVESellUI', 'PVETopTipsUI', 'PVEShopMechaUI', 'PVEPetBuffUI', 'PVEMonsterAttributesUI', 'PVECareerWidgetUI', 'PVECareerProgressUI', 'PVEElementUI',
 'TVMissileLauncherUI', 'TVMissileLauncherAimUI', 'TVMissileAimUI'}
PVE_MAIN_UI_LIST = [
 'PVEKeyBuyUI', 'PVEMainUI', 'PVELevelWidgetUI', 'PVEMechaWidgetUI', 'PVETalentWidgetUI', 'PVEStoryWidgetUI',
 'PVEEquipWidgetUI', 'PVEBookWidgetUI', 'PVEDebrisWidgetUI', 'PVEPetWidgetUI', 'PVEPetBuffUI', 'PVEMonsterAttributesUI',
 'PVECareerWidgetUI', 'PVECareerProgressUI']
MECHA_AIM_UI_LSIT = [
 'MechaKnightAimUI', 'MechaNingNingAimUI', 'Mecha8003AimUI', 'Mecha8004AimUI', 'Mecha8005AimUI', 'Mecha8006AimUI',
 'Mecha8007AimUI', 'Mecha8007AimUI2', 'Mecha8008AimUI', 'Mecha8009AimUI', 'Mecha8010AimUI', 'Mecha8011AimUI',
 'Mecha8013AimUI', 'Mecha8014AimUI', 'Mecha8015AimUI', 'Mecha8016AimUI', 'Mecha8017AimUI', 'Mecha8018AimUI',
 'Mecha8019AimUI', 'Mecha8020AimUI', 'Mecha8021AimUI', 'Mecha8022AimUI', 'Mecha8023AimUI', 'Mecha8024AimUI',
 'Mecha8025AimUI', 'Mecha8026AimUI', 'Mecha8027AimUI', 'Mecha8028AimUI', 'Mecha8029AimUI', 'Mecha8030AimUI',
 'Mecha8501AimUI', 'MotorcycleAimUI', 'TVMissileLauncherAimUI', 'Mecha8032AimUI', 'Mecha8033AimUI', 'Mecha8034AimUI',
 'Mecha8035AimUI', 'Mecha8036AimUI', 'Mecha8037AimUI']
MAIN_UI_LIST.update(MECHA_AIM_UI_LSIT)

class BasePanel(Singleton):
    PANEL_CONFIG_NAME = 'not_exit'
    UI_ACTION_EVENT = {}
    DLG_ZORDER = uiconst.BASE_LAYER_ZORDER
    UI_TYPE = uiconst.UI_TYPE_NORMAL
    UI_VKB_TYPE = None
    IS_FULLSCREEN = False
    IS_PLAY_OPEN_SOUND = True
    OPEN_SOUND_NAME = ''
    RECREATE_WHEN_RESOLUTION_CHANGE = False
    UI_EFFECT_LIST = []
    CONTENT_NODES = ()
    DELAY_TIME = 0
    UI_CLICK_SALOG_DIC = {}
    GLOBAL_EVENT = {}
    MOUSE_CURSOR_TRIGGER_SHOW = False
    HOT_KEY_FUNC_MAP = {}
    HOT_KEY_FUNC_MAP_SHOW = {}
    HOT_KEY_FUNC_MAP_SHOW_CONDITIONAL = {}
    ENABLE_HOT_KEY_SUPPORT = False
    HOT_KEY_CHECK_VISIBLE = True
    HOT_KEY_NEED_SCROLL_SUPPORT = False
    NEED_SCROLL_ALWAYS = False
    PLAY_THE_IN_ANIM_ON_INIT = True
    BG_CONFIG_NAME = ''
    BG_DLG_ZORDER = 0
    ASSOCIATE_PANEL_PATHS = []
    SHARE_TIPS_INFO = ()
    EXCEPTION_IGNORE_ZORDER = False

    def regist_main_ui(self):
        global MAIN_UI_LIST
        MAIN_UI_LIST.add(self.__class__.__name__)

    def unregist_main_ui(self):
        MAIN_UI_LIST.discard(self.__class__.__name__)

    def init(self, parent=None, *arg, **kwargs):
        self.recreate_args = {}
        self.recreate_tuple_args = ()
        if self.RECREATE_WHEN_RESOLUTION_CHANGE:
            self.recreate_args = kwargs
            self.recreate_tuple_args = arg
        self._panelName = self.__class__.__name__
        self.panel = None
        if isinstance(parent, (CCNode, CCUIWidget)):
            self._parent = parent
        else:
            if parent is None:
                parent = global_data.cocos_scene
            if isinstance(parent, cc.Node):
                parent = trans2ProxyObj(parent)
            elif isinstance(parent, ccui.Widget):
                parent = trans2ProxyObj(parent)
            self._parent = parent
        self._base_init()
        import time
        import six
        if six.PY3:
            t1 = time.process_time()
        else:
            t1 = time.clock()
        if 'zorder' in kwargs:
            self.DLG_ZORDER = kwargs['zorder']
            del kwargs['zorder']
        self.on_custom_template_create(*arg, **kwargs)
        self.panel = self.create_template()
        if six.PY3:
            t2 = time.process_time()
        else:
            t2 = time.clock()
        self._effect = None
        if self._parent is not None and getattr(self.panel, 'pnl_blur'):
            from logic.comsys.effect.ui_effect import GaussianEffect
            self._effect = GaussianEffect(self._parent, self.panel.pnl_blur)
            self._effect.start()
        ui_events = self.UI_ACTION_EVENT
        sa_log_dic = dict(self.UI_CLICK_SALOG_DIC)
        if ui_events:
            format_events = traversal_dict(ui_events)
            for ctrl_path, func_name in six.iteritems(format_events):
                ctrlnamelist = ctrl_path.split('.')
                handler = getattr(self, func_name, None)
                if not callable(handler):
                    continue
                event_name = ctrlnamelist[-1]
                com_path = ctrlnamelist[:-1]
                ctrl = self
                for name in com_path:
                    ctrl = getattr(ctrl, name)

                if is_ui_object(ctrl):
                    if ctrl_path in sa_log_dic:
                        from logic.gutils.ui_salog_utils import ui_operaion_salog_wrapper
                        handler = ui_operaion_salog_wrapper(handler, sa_log_dic[ctrl_path])
                        del sa_log_dic[ctrl_path]

                    def _func(c, *args):
                        handler(*args)

                    ctrl.BindMethod(event_name, handler)

        if len(sa_log_dic) > 0:
            log_error('UnFounded salogs', sa_log_dic)
        self._base_bg_panel = None
        self._sub_page_dict = {}
        if self.BG_CONFIG_NAME:
            self._base_bg_panel = global_data.ui_mgr.create_simple_dialog(self.BG_CONFIG_NAME, self.BG_DLG_ZORDER or self.DLG_ZORDER, UI_VKB_TYPE=uiconst.UI_VKB_NO_EFFECT)
            self.add_associate_vis_ui(self._base_bg_panel.__class__.__name__)
        self.process_global_event(True)
        if global_data.ui_mgr.enable_profile_init_panel:
            import cProfile
            import sys
            import pstats
            import six_ex.moves.StringIO
            import time
            p = cProfile.Profile()
            p.enable()
            start_time = time.time()
            self.on_init_panel(*arg, **kwargs)
            p.disable()
            s = six_ex.moves.StringIO.StringIO()
            ps = pstats.Stats(p, stream=s)
            ps.sort_stats('cumulative', 'calls')
            ps.print_stats(20)
            ps.sort_stats('time', 'calls')
            ps.print_stats(20)
            print(s.getvalue())
        else:
            self.on_init_panel(*arg, **kwargs)
        self.init_hot_key_event()
        if self.DELAY_TIME > 0:
            self.show_content(False)

            def _cc_show_content():
                self.show_content(True)

            def _cc_on_delay_init_panel():
                self.on_delay_init_panel(*arg, **kwargs)

            self.panel.runAction(cc.Sequence.create([
             cc.DelayTime.create(self.DELAY_TIME),
             cc.CallFunc.create(_cc_show_content),
             cc.CallFunc.create(_cc_on_delay_init_panel)]))
        if len(self.UI_EFFECT_LIST) > 0:
            self.on_init_anim()
        self._init_reused_ani_info()
        self._check_play_reused_anim_on_init()
        self.register_func_key_mapping()
        self._check_show_count_dict()
        if (self.ENABLE_HOT_KEY_SUPPORT or self.HOT_KEY_FUNC_MAP or self.HOT_KEY_FUNC_MAP_SHOW or self.HOT_KEY_NEED_SCROLL_SUPPORT) and global_data.pc_ctrl_mgr:
            if global_data.pc_ctrl_mgr.is_pc_control_enable():
                self.on_hot_key_opened_state()
            else:
                self.on_hot_key_closed_state()
        if self.HOT_KEY_NEED_SCROLL_SUPPORT and self.NEED_SCROLL_ALWAYS and global_data.pc_ctrl_mgr:
            self.register_mouse_scroll_event()
        if global_data.redpoint_mgr:
            global_data.redpoint_mgr.register_by_project_name_auto(self.panel, self.PANEL_CONFIG_NAME)
        self.check_share_btn_tips()
        global_data.emgr.ui_open_event.emit(self.__class__.__name__)
        if global_data.is_inner_server:
            if self.UI_VKB_TYPE is None:
                msg = '\xe5\x86\x85\xe6\x9c\x8d\xe6\x8f\x90\xe7\xa4\xba\xef\xbc\x9a\xe6\x9c\xac\xe7\x95\x8c\xe9\x9d\xa2%s\xe6\xb2\xa1\xe6\x9c\x89\xe6\x8c\x87\xe6\x98\x8e\xe5\xae\x89\xe5\x8d\x93\xe4\xb8\x8a\xe5\x90\x8e\xe9\x80\x80\xe9\x94\xae\xe6\x8c\x89\xe4\xb8\x8b\xe6\x97\xb6\xe6\x9c\xac\xe7\x95\x8c\xe9\x9d\xa2\xe5\xba\x94\xe6\x9c\x89\xe7\x9a\x84\xe5\x93\x8d\xe5\xba\x94\xef\xbc\x8c\xe8\xaf\xb7\xe8\xae\xbe\xe7\xbd\xaeUI_VKB_TYPE\xe5\xb1\x9e\xe6\x80\xa7, \xe7\x95\x8c\xe9\x9d\xa2\xe6\xa8\xa1\xe6\x9d\xbf\xe4\xb8\xba%s' % (self.__class__.__name__, self.PANEL_CONFIG_NAME)
                global_data.game_mgr.show_tip(msg)
                log_error(msg)
                import exception_hook
                exception_hook.post_error(msg)
        elif self.UI_VKB_TYPE is None:
            self.UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
        if self.ASSOCIATE_PANEL_PATHS:
            for ass_cond_func, ass_name, ass_dpath, ass_args, ass_kwargs in self.ASSOCIATE_PANEL_PATHS:
                if ass_cond_func():
                    ass_ui = global_data.ui_mgr.show_ui_with_args(ass_name, ass_dpath, *ass_args, **ass_kwargs)
                    if ass_ui:
                        self.add_associate_vis_ui(ass_ui)

        return

    def set_effect(self, effect):
        self._effect = effect

    def _base_init(self):
        self._show_count_dict = {}
        self._show_count = 0
        self._enable_show_count = False
        self._hide_name_list = []
        self._touch_effect_cache = []
        self._touch_idx = 0
        self._hide_set = set([])
        self._blocking_set = set()
        self.associate_vis_ui_list = set()
        self._registered_hot_key_funcs = []
        self._hotkey_should_show_set = set()
        self._reused_anim_info = {}
        self._is_register_mouse_scroll = False
        from logic.gutils.hot_key_utils import get_ui_mouse_scroll_sensitivity
        self.ui_scroll_sensitivity = get_ui_mouse_scroll_sensitivity(self.__class__.__name__)
        self._base_bg_panel = None
        return

    def __getattr__--- This code section failed: ---

 376       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'getattr'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    64  'to 64'

 377      12  LOAD_GLOBAL           1  'getattr'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             2  'panel'
          21  LOAD_FAST             1  'aname'
          24  CALL_FUNCTION_2       2 
          27  STORE_FAST            2  'attr'

 378      30  LOAD_FAST             2  'attr'
          33  LOAD_CONST            0  ''
          36  COMPARE_OP            8  'is'
          39  POP_JUMP_IF_FALSE    57  'to 57'

 379      42  LOAD_GLOBAL           4  'AttributeError'
          45  LOAD_FAST             1  'aname'
          48  CALL_FUNCTION_1       1 
          51  RAISE_VARARGS_1       1 
          54  JUMP_ABSOLUTE        76  'to 76'

 381      57  LOAD_FAST             2  'attr'
          60  RETURN_VALUE     
          61  JUMP_FORWARD         12  'to 76'

 383      64  LOAD_GLOBAL           4  'AttributeError'
          67  LOAD_FAST             1  'aname'
          70  CALL_FUNCTION_1       1 
          73  RAISE_VARARGS_1       1 
        76_0  COME_FROM                '61'
          76  LOAD_CONST            0  ''
          79  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def on_custom_template_create(self, *arg, **kwargs):
        self._custom_template_info = None
        return

    def on_get_template_zorder(self):
        return self.DLG_ZORDER

    ccbfiles_that_trigger_anim_reuse = ('common/i_common_window_big', 'common/i_window_common',
                                        'common/i_window_common_medium', 'common/i_window_common_small')
    common_window_reused_ani_map = {'common/i_window_common': ('in', 'friend/main_friend'),
       'common/i_common_window_big': ('in', 'friend/main_friend'),
       'common/i_window_common_medium': ('in', 'mech_display/mech_proficiency'),
       'common/i_window_common_small': ('in', 'common/change_name')
       }

    def _init_reused_ani_info(self):
        if not self.panel:
            return
        else:
            for template_contained, reused_anim_info in six.iteritems(self.common_window_reused_ani_map):
                reused_anim_name = reused_anim_info[0]
                temp_path_got_anim_reused = reused_anim_info[1]
                has, trigger_node = self.panel.IsCCBFileContained(template_contained)
                if has:
                    anim_name_on_root = None
                    if self.panel.GetTemplatePath() == temp_path_got_anim_reused:
                        anim_name_on_root = reused_anim_name
                    elif not self.panel.IsCSBNode():
                        anim_name_on_root = self.copy_ani_from_template_to_root_node(temp_path_got_anim_reused, reused_anim_name)
                    else:
                        anim_name_on_root = self.copy_ani_from_template_to_root_node_csb(temp_path_got_anim_reused, reused_anim_name)
                    self._reused_anim_info[reused_anim_name] = (
                     trigger_node, anim_name_on_root)
                    break

            return

    def copy_ani_from_template_to_root_node(self, temp_path_got_anim_reused, reused_anim_name):
        anim_name_on_root = None
        temp_got_anim_reused = None
        try:
            temp_got_anim_reused = global_data.uisystem.load_template(temp_path_got_anim_reused)
        except Exception as e:
            log_error(str(e))

        if temp_got_anim_reused:
            ani_name_prefix = '{0}->'.format(temp_path_got_anim_reused)
            ani_conf, ani_times = global_data.uisystem.create_ani_info_for_single_node(self.panel, temp_got_anim_reused, [
             reused_anim_name], ani_name_prefix)
            if ani_conf:
                self.panel.UpdateAnimConfWhenKeyNotExist(ani_conf)
                anim_name_on_root = ani_name_prefix + reused_anim_name
                if ani_times:
                    self.panel.UpdateAnimPlayTimesWhenKeyNotExist(ani_times)
        return anim_name_on_root

    def copy_ani_from_template_to_root_node_csb(self, temp_path_got_anim_reused, reused_anim_name):
        temp_got_anim_reused = None
        import ccs
        path = global_data.uisystem.get_fixed_template_path(temp_path_got_anim_reused, '.csb')
        actiontimeline = ccs.ActionTimelineCache.getInstance().createActionWithFlatBuffersFile(path)
        if actiontimeline:
            ani_action_map = actiontimeline.splitByAnimation()
            if reused_anim_name in ani_action_map:
                target_sub_action_timeline = ani_action_map[reused_anim_name]
                target_sub_action_timeline.pause()
                target_sub_action_timeline.retain()
                tags = target_sub_action_timeline.getTimelineTags()
                minTag = min([ t for t in tags if t > 0 ])
                target_sub_action_timeline.changeTimelineTag(minTag, self.panel.getActionTag())
                self.panel.addTimelineAnimation(reused_anim_name, target_sub_action_timeline)
        return reused_anim_name

    def _check_play_reused_anim_on_init(self):
        if not global_data.mute_auto_in_anim and self.PLAY_THE_IN_ANIM_ON_INIT:
            self.play_the_in_anim()

    def play_the_in_anim(self, adjust_to_time=-1, force_resume=False, scale=1.0):
        ani_name = 'in'
        if self._reused_anim_info is None or ani_name not in self._reused_anim_info:
            return
        else:
            trigger_node, actual_ani_name_on_root = self._reused_anim_info[ani_name]
            if not self.panel:
                return
            self.panel.PlayAnimation(actual_ani_name_on_root, adjust_to_time=adjust_to_time, force_resume=force_resume, scale=scale)
            trigger_node.PlayAnimation(ani_name, adjust_to_time=adjust_to_time, force_resume=force_resume, scale=scale)
            return

    def set_template_zorder(self, zorder):
        global_data.ui_mgr.set_dialog_zorder(self.panel, zorder, is_full_screen=self.IS_FULLSCREEN)

    def get_name(self):
        return self._panelName

    def create_template(self):
        if self.PANEL_CONFIG_NAME.startswith('bg_') or self.PANEL_CONFIG_NAME.find('/bg_') > 0 or self.PANEL_CONFIG_NAME.find('\\bg_') > 0:
            self.IS_FULLSCREEN = True
        inst = global_data.ui_mgr.create_dialog(self, self.PANEL_CONFIG_NAME, self.on_get_template_zorder(), is_full_screen=self.IS_FULLSCREEN, template_info=self._custom_template_info, exception_ignore_zorder=self.EXCEPTION_IGNORE_ZORDER)
        if self.IS_FULLSCREEN:
            inst.SeFullBgMode()
        return inst

    def on_init_panel(self, *args, **kwargs):
        pass

    def on_delay_init_panel(self, *args, **kwargs):
        pass

    def on_finalize(self):
        if global_data.redpoint_mgr:
            global_data.redpoint_mgr.unregister_by_project_name(self.PANEL_CONFIG_NAME)
        self._reused_anim_info = None
        self.unregister_func_key_mapping()
        self.remove_blocking_ui_list()
        self.process_global_event(False)
        self.unregist_hot_key_event()
        if self.HOT_KEY_NEED_SCROLL_SUPPORT:
            self.unregister_mouse_scroll_event()
        self._hotkey_should_show_set.clear()
        if self._effect:
            self._effect.destroy()
        self.on_finalize_panel()
        if self.MOUSE_CURSOR_TRIGGER_SHOW:
            if global_data.mouse_mgr:
                global_data.mouse_mgr.add_cursor_hide_count(self.__class__.__name__)
        if self._base_bg_panel:
            self._base_bg_panel.close()
            self._base_bg_panel = None
        if self.ASSOCIATE_PANEL_PATHS:
            for ass_cond_func, ass_name, ass_dpath, ass_args, ass_kwargs in self.ASSOCIATE_PANEL_PATHS:
                global_data.ui_mgr.close_ui(ass_name)

        self.clear_sub_pages()
        if self.SHARE_TIPS_INFO:
            self.destroy_widget('_share_tips_widget')
        if self.panel and self.panel.isValid():
            self.panel.Destroy()
        self.panel = None
        self._panelName = None
        self._parent = None
        return

    def on_finalize_panel(self):
        pass

    def enter_screen(self):
        self.add_show_count('__screen__')

    def leave_screen(self):
        self.add_hide_count('__screen__')

    def get_widget(self):
        return self.panel

    def is_valid(self):
        return self.panel is not None and self.panel.isValid()

    def close(self, *args):
        global_data.ui_mgr.close_ui(self.get_name())

    @property
    def scene(self):
        return world.get_active_scene()

    def hide(self):
        self.add_hide_count(self.__class__.__name__)

    def show(self):
        self.add_show_count(self.__class__.__name__)

    def isPanelVisible(self):
        if self.panel and self.panel.isValid():
            return self.panel.isVisible()
        return False

    def do_hide_panel(self):
        if self.panel and self.panel.isValid():
            if self._effect:
                self.effect.stop()
            self.panel.setVisible(False)
            self.update_associate_vis_ui_visible()
            if self.MOUSE_CURSOR_TRIGGER_SHOW:
                if global_data.mouse_mgr:
                    global_data.mouse_mgr.add_cursor_hide_count(self.__class__.__name__)
            if not self._will_cause_panel_hide(pc_const.PANEL_HIDE_REASON_DUE_TO_PC_HOTKEY_HINT_DISPLAY_OPTION):
                self.unregister_func_key_mapping()

    def do_show_panel(self):
        if self.panel and self.panel.isValid():
            self.panel.setVisible(True)
            if self._effect:
                self.effect.start()
            self.update_associate_vis_ui_visible()
            if self.MOUSE_CURSOR_TRIGGER_SHOW:
                if global_data.mouse_mgr:
                    global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)
            self.register_func_key_mapping()

    def add_hide_count_before(self, key):
        return key in self._show_count_dict

    def add_show_count(self, key='_default', count=1, is_check=True):
        if key in self._show_count_dict:
            if self._show_count_dict[key] < 0:
                self._show_count_dict[key] += count
        if is_check:
            self._check_show_count_dict()

    def add_hide_count(self, key='_default', count=1, no_same_key=True, is_check=True):
        if key in self._show_count_dict:
            if not no_same_key:
                self._show_count_dict[key] -= count
            elif self._show_count_dict[key] >= 0:
                self._show_count_dict[key] -= count
        else:
            self._show_count_dict[key] = -count
        if is_check:
            self._check_show_count_dict()

    def remove_count_key(self, key):
        if key in self._show_count_dict:
            del self._show_count_dict[key]
        self._check_show_count_dict()

    def check_can_hide_count(self, key):
        return self._show_count_dict.get(key, 0) >= 0

    def get_show_count(self, key):
        return self._show_count_dict.get(key, 0)

    def check_show_count_dict(self):
        self._check_show_count_dict()

    def _check_show_count_dict(self):
        if not self.panel:
            return
        for key, val in six.iteritems(self._show_count_dict):
            if self._will_cause_panel_hide(key):
                self.do_hide_panel()
                break
        else:
            self.do_show_panel()

    def get_show(self):
        if not self.panel:
            return False
        for key, val in six.iteritems(self._show_count_dict):
            if self._will_cause_panel_hide(key):
                return False

        return True

    def _will_cause_panel_hide(self, show_count_dict_key):
        return show_count_dict_key in self._show_count_dict and self._show_count_dict[show_count_dict_key] < 0

    def has_hide_reason(self, show_count_dict_key):
        return self._will_cause_panel_hide(show_count_dict_key)

    def clear_show_count_dict(self):
        self._show_count_dict = {}
        self._check_show_count_dict()

    def clear_hide_set(self):
        self._hide_set.clear()

    def hide_main_ui(self, ui_list=None, exceptions=(), exception_types=()):
        from logic.gutils.pc_ui_utils import MOBILE_2_PC_UI_DICT, PC_2_MOBILE_UI_DICT
        need_check_ui = []
        self._hide_set.clear()
        ui_list = MAIN_UI_LIST if ui_list is None else ui_list
        for ui_name in ui_list:
            if ui_name in exceptions:
                continue
            if global_data.is_pc_mode and MOBILE_2_PC_UI_DICT.get(ui_name) in exceptions:
                continue
            if ui_name != self._panelName:
                ui = global_data.ui_mgr.get_ui(ui_name)
                if ui and ui.UI_TYPE in exception_types:
                    continue
                if ui:
                    ui.add_hide_count(self.__class__.__name__, is_check=False)
                    need_check_ui.append(ui)
                    self._hide_set.add(ui_name)

        for ui in need_check_ui:
            if not ui.isPanelVisible():
                continue
            ui._check_show_count_dict()

        return

    def show_main_ui(self):
        need_check_ui = []
        for ui_name in self._hide_set:
            ui = global_data.ui_mgr.get_ui(ui_name)
            if ui:
                ui.add_show_count(self.__class__.__name__, is_check=False)
                need_check_ui.append(ui)

        for ui in need_check_ui:
            if ui.isPanelVisible():
                continue
            ui._check_show_count_dict()

        self._hide_set.clear()

    def show_main_ui_by_type(self, key):
        if key in self._hide_set:
            ui = global_data.ui_mgr.get_ui(key)
            if ui:
                ui.add_show_count(self.__class__.__name__)
            self._hide_set.remove(key)

    def hide_all_ui_by_type(self, key, types=(uiconst.UI_TYPE_NORMAL,), exceptions=()):
        total_exceptions = [
         self.__class__.__name__]
        total_exceptions.extend(exceptions)
        self._hide_name_list = global_data.ui_mgr.hide_all_ui_by_type(key, types, total_exceptions)

    def revert_hide_all_ui_by_type_action(self, key):
        for name in self._hide_name_list:
            ui_inst = global_data.ui_mgr.get_ui(name)
            if ui_inst:
                ui_inst.add_show_count(key)

        self._hide_name_list = []

    def on_init_anim--- This code section failed: ---

 745       0  BUILD_LIST_0          0 
           3  STORE_FAST            2  'action_list'

 746       6  LOAD_CONST            0  ''
           9  STORE_FAST            3  'tab_list'

 747      12  LOAD_CONST            0  ''
          15  STORE_FAST            4  'tab_time'

 748      18  LOAD_GLOBAL           1  'hasattr'
          21  LOAD_GLOBAL           1  'hasattr'
          24  CALL_FUNCTION_2       2 
          27  POP_JUMP_IF_FALSE    42  'to 42'

 749      30  LOAD_FAST             0  'self'
          33  LOAD_ATTR             2  'tab_list'
          36  STORE_FAST            3  'tab_list'
          39  JUMP_FORWARD          0  'to 42'
        42_0  COME_FROM                '39'

 750      42  SETUP_LOOP          203  'to 248'
          45  LOAD_FAST             0  'self'
          48  LOAD_ATTR             3  'UI_EFFECT_LIST'
          51  GET_ITER         
          52  FOR_ITER            192  'to 247'
          55  STORE_FAST            5  'info'

 751      58  LOAD_GLOBAL           4  'getattr'
          61  LOAD_FAST             0  'self'
          64  LOAD_ATTR             5  'panel'
          67  LOAD_FAST             5  'info'
          70  LOAD_CONST            2  'node'
          73  BINARY_SUBSCR    
          74  CALL_FUNCTION_2       2 
          77  STORE_FAST            6  'node'

 752      80  LOAD_FAST             5  'info'
          83  LOAD_CONST            3  'anim'
          86  BINARY_SUBSCR    
          87  STORE_FAST            7  'anim_name'

 753      90  LOAD_FAST             5  'info'
          93  LOAD_CONST            4  'time'
          96  BINARY_SUBSCR    
          97  STORE_FAST            8  'trigger_time'

 754     100  LOAD_FAST             6  'node'
         103  LOAD_ATTR             6  'setVisible'
         106  LOAD_GLOBAL           7  'False'
         109  CALL_FUNCTION_1       1 
         112  POP_TOP          

 755     113  LOAD_FAST             3  'tab_list'
         116  POP_JUMP_IF_FALSE   149  'to 149'
         119  LOAD_FAST             6  'node'
         122  LOAD_FAST             3  'tab_list'
         125  COMPARE_OP            2  '=='
       128_0  COME_FROM                '116'
         128  POP_JUMP_IF_FALSE   149  'to 149'

 756     131  LOAD_FAST             6  'node'
         134  LOAD_ATTR             8  'GetAnimationMaxRunTime'
         137  LOAD_FAST             7  'anim_name'
         140  CALL_FUNCTION_1       1 
         143  STORE_FAST            4  'tab_time'
         146  JUMP_FORWARD          0  'to 149'
       149_0  COME_FROM                '146'

 757     149  LOAD_FAST             8  'trigger_time'
         152  LOAD_CONST            5  ''
         155  COMPARE_OP            4  '>'
         158  POP_JUMP_IF_FALSE   189  'to 189'

 758     161  LOAD_FAST             2  'action_list'
         164  LOAD_ATTR             9  'append'
         167  LOAD_GLOBAL          10  'cc'
         170  LOAD_ATTR            11  'DelayTime'
         173  LOAD_ATTR            12  'create'
         176  LOAD_FAST             8  'trigger_time'
         179  CALL_FUNCTION_1       1 
         182  CALL_FUNCTION_1       1 
         185  POP_TOP          
         186  JUMP_FORWARD          0  'to 189'
       189_0  COME_FROM                '186'

 759     189  LOAD_CONST               '<code_object cb>'
         192  MAKE_FUNCTION_0       0 
         195  STORE_DEREF           0  'cb'

 762     198  LOAD_FAST             6  'node'
         201  LOAD_FAST             7  'anim_name'
         204  LOAD_CLOSURE          0  'cb'
         210  LOAD_CONST               '<code_object _cc_init_aim_help>'
         213  MAKE_CLOSURE_2        2 
         216  STORE_FAST            9  '_cc_init_aim_help'

 764     219  LOAD_FAST             2  'action_list'
         222  LOAD_ATTR             9  'append'
         225  LOAD_GLOBAL          10  'cc'
         228  LOAD_ATTR            13  'CallFunc'
         231  LOAD_ATTR            12  'create'
         234  LOAD_FAST             9  '_cc_init_aim_help'
         237  CALL_FUNCTION_1       1 
         240  CALL_FUNCTION_1       1 
         243  POP_TOP          
         244  JUMP_BACK            52  'to 52'
         247  POP_BLOCK        
       248_0  COME_FROM                '42'

 766     248  LOAD_FAST             3  'tab_list'
         251  POP_JUMP_IF_FALSE   329  'to 329'

 767     254  LOAD_FAST             0  'self'
         257  LOAD_ATTR            14  'pre_tab_anim'
         260  CALL_FUNCTION_0       0 
         263  POP_TOP          

 768     264  LOAD_FAST             4  'tab_time'
         267  POP_JUMP_IF_FALSE   298  'to 298'

 769     270  LOAD_FAST             2  'action_list'
         273  LOAD_ATTR             9  'append'
         276  LOAD_GLOBAL          10  'cc'
         279  LOAD_ATTR            11  'DelayTime'
         282  LOAD_ATTR            12  'create'
         285  LOAD_FAST             4  'tab_time'
         288  CALL_FUNCTION_1       1 
         291  CALL_FUNCTION_1       1 
         294  POP_TOP          
         295  JUMP_FORWARD          0  'to 298'
       298_0  COME_FROM                '295'

 770     298  LOAD_FAST             2  'action_list'
         301  LOAD_ATTR             9  'append'
         304  LOAD_GLOBAL          10  'cc'
         307  LOAD_ATTR            13  'CallFunc'
         310  LOAD_ATTR            12  'create'
         313  LOAD_FAST             0  'self'
         316  LOAD_ATTR            15  'on_tab_anim'
         319  CALL_FUNCTION_1       1 
         322  CALL_FUNCTION_1       1 
         325  POP_TOP          
         326  JUMP_FORWARD          0  'to 329'
       329_0  COME_FROM                '326'

 771     329  LOAD_FAST             1  'init_cb'
         332  POP_JUMP_IF_FALSE   363  'to 363'

 772     335  LOAD_FAST             2  'action_list'
         338  LOAD_ATTR             9  'append'
         341  LOAD_GLOBAL          10  'cc'
         344  LOAD_ATTR            13  'CallFunc'
         347  LOAD_ATTR            12  'create'
         350  LOAD_FAST             1  'init_cb'
         353  CALL_FUNCTION_1       1 
         356  CALL_FUNCTION_1       1 
         359  POP_TOP          
         360  JUMP_FORWARD          0  'to 363'
       363_0  COME_FROM                '360'

 773     363  LOAD_FAST             0  'self'
         366  LOAD_ATTR             5  'panel'
         369  LOAD_ATTR            16  'runAction'
         372  LOAD_GLOBAL          10  'cc'
         375  LOAD_ATTR            17  'Sequence'
         378  LOAD_ATTR            12  'create'
         381  LOAD_FAST             2  'action_list'
         384  CALL_FUNCTION_1       1 
         387  CALL_FUNCTION_1       1 
         390  POP_TOP          
         391  LOAD_CONST            0  ''
         394  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 24

    def pre_tab_anim--- This code section failed: ---

 776       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'tab_panels'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    33  'to 33'
          12  LOAD_FAST             0  'self'
          15  LOAD_ATTR             1  'tab_panels'
        18_0  COME_FROM                '9'
          18  POP_JUMP_IF_FALSE    33  'to 33'
          21  LOAD_GLOBAL           2  'getattr'
          24  LOAD_GLOBAL           1  'tab_panels'
          27  CALL_FUNCTION_2       2 
          30  JUMP_FORWARD          3  'to 36'
          33  LOAD_CONST            0  ''
        36_0  COME_FROM                '30'
          36  STORE_FAST            1  'tab_panels'

 777      39  LOAD_FAST             1  'tab_panels'
          42  POP_JUMP_IF_TRUE     49  'to 49'

 778      45  LOAD_CONST            0  ''
          48  RETURN_END_IF    
        49_0  COME_FROM                '42'

 779      49  SETUP_LOOP           27  'to 79'
          52  LOAD_FAST             1  'tab_panels'
          55  GET_ITER         
          56  FOR_ITER             19  'to 78'
          59  STORE_FAST            2  'tab'

 780      62  LOAD_FAST             2  'tab'
          65  LOAD_ATTR             4  'setVisible'
          68  LOAD_GLOBAL           5  'False'
          71  CALL_FUNCTION_1       1 
          74  POP_TOP          
          75  JUMP_BACK            56  'to 56'
          78  POP_BLOCK        
        79_0  COME_FROM                '49'
          79  LOAD_CONST            0  ''
          82  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def on_tab_anim--- This code section failed: ---

 783       0  BUILD_LIST_0          0 
           3  STORE_FAST            1  'action_list'

 784       6  LOAD_GLOBAL           0  'hasattr'
           9  LOAD_GLOBAL           1  'tab_panels'
          12  CALL_FUNCTION_2       2 
          15  POP_JUMP_IF_FALSE    39  'to 39'
          18  LOAD_FAST             0  'self'
          21  LOAD_ATTR             1  'tab_panels'
        24_0  COME_FROM                '15'
          24  POP_JUMP_IF_FALSE    39  'to 39'
          27  LOAD_GLOBAL           2  'getattr'
          30  LOAD_GLOBAL           1  'tab_panels'
          33  CALL_FUNCTION_2       2 
          36  JUMP_FORWARD          3  'to 42'
          39  LOAD_CONST            0  ''
        42_0  COME_FROM                '36'
          42  STORE_FAST            2  'tab_panels'

 785      45  LOAD_FAST             2  'tab_panels'
          48  POP_JUMP_IF_TRUE     55  'to 55'

 786      51  LOAD_CONST            0  ''
          54  RETURN_END_IF    
        55_0  COME_FROM                '48'

 787      55  SETUP_LOOP          143  'to 201'
          58  LOAD_FAST             2  'tab_panels'
          61  GET_ITER         
          62  FOR_ITER            135  'to 200'
          65  STORE_FAST            3  'tab'

 788      68  LOAD_FAST             3  'tab'
          71  LOAD_ATTR             4  'btn_window_tab'
          74  STORE_FAST            4  'btn'

 789      77  LOAD_FAST             4  'btn'
          80  LOAD_ATTR             5  'GetContentSize'
          83  CALL_FUNCTION_0       0 
          86  UNPACK_SEQUENCE_2     2 
          89  STORE_DEREF           0  'width'
          92  STORE_DEREF           1  'height'

 790      95  LOAD_FAST             4  'btn'
          98  LOAD_ATTR             6  'setPositionX'
         101  LOAD_CONST            2  ''
         104  CALL_FUNCTION_1       1 
         107  POP_TOP          

 791     108  LOAD_CLOSURE          0  'width'
         111  LOAD_CLOSURE          1  'height'
         117  LOAD_CONST               '<code_object cb>'
         120  MAKE_CLOSURE_0        0 
         123  STORE_DEREF           2  'cb'

 794     126  LOAD_FAST             4  'btn'
         129  LOAD_FAST             3  'tab'
         132  LOAD_CLOSURE          2  'cb'
         138  LOAD_CONST               '<code_object _cc_tab_ani_help>'
         141  MAKE_CLOSURE_2        2 
         144  STORE_FAST            5  '_cc_tab_ani_help'

 796     147  LOAD_FAST             1  'action_list'
         150  LOAD_ATTR             7  'append'
         153  LOAD_GLOBAL           8  'cc'
         156  LOAD_ATTR             9  'CallFunc'
         159  LOAD_ATTR            10  'create'
         162  LOAD_FAST             5  '_cc_tab_ani_help'
         165  CALL_FUNCTION_1       1 
         168  CALL_FUNCTION_1       1 
         171  POP_TOP          

 797     172  LOAD_FAST             1  'action_list'
         175  LOAD_ATTR             7  'append'
         178  LOAD_GLOBAL           8  'cc'
         181  LOAD_ATTR            11  'DelayTime'
         184  LOAD_ATTR            10  'create'
         187  LOAD_CONST            5  0.05
         190  CALL_FUNCTION_1       1 
         193  CALL_FUNCTION_1       1 
         196  POP_TOP          
         197  JUMP_BACK            62  'to 62'
         200  POP_BLOCK        
       201_0  COME_FROM                '55'

 799     201  LOAD_GLOBAL           0  'hasattr'
         204  LOAD_GLOBAL           6  'setPositionX'
         207  CALL_FUNCTION_2       2 
         210  POP_JUMP_IF_FALSE   234  'to 234'
         213  LOAD_FAST             0  'self'
         216  LOAD_ATTR            12  'tab_list'
       219_0  COME_FROM                '210'
         219  POP_JUMP_IF_FALSE   234  'to 234'
         222  LOAD_GLOBAL           2  'getattr'
         225  LOAD_GLOBAL           6  'setPositionX'
         228  CALL_FUNCTION_2       2 
         231  JUMP_FORWARD          3  'to 237'
         234  LOAD_CONST            0  ''
       237_0  COME_FROM                '231'
         237  STORE_FAST            6  'tab_list'

 800     240  LOAD_FAST             6  'tab_list'
         243  POP_JUMP_IF_FALSE   277  'to 277'

 801     246  LOAD_FAST             0  'self'
         249  LOAD_ATTR            12  'tab_list'
         252  LOAD_ATTR            13  'runAction'
         255  LOAD_GLOBAL           8  'cc'
         258  LOAD_ATTR            14  'Sequence'
         261  LOAD_ATTR            10  'create'
         264  LOAD_FAST             1  'action_list'
         267  CALL_FUNCTION_1       1 
         270  CALL_FUNCTION_1       1 
         273  POP_TOP          
         274  JUMP_FORWARD          0  'to 277'
       277_0  COME_FROM                '274'
         277  LOAD_CONST            0  ''
         280  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 12

    def show_content(self, visible):
        for node_name in self.CONTENT_NODES:
            node = getattr(self.panel, node_name)
            node.setVisible(visible)

    def destroy_widget(self, widget_name):
        widget = getattr(self, widget_name, None)
        if widget:
            widget.destroy()
            setattr(self, widget_name, None)
        return

    def play_touch_effect(self, anim_nam, click_name, pos, scale=None):
        if anim_nam:
            self.panel.PlayAnimation(anim_nam)
        if not global_data.is_key_mocking_ui_event:
            if len(self._touch_effect_cache) >= 3:
                self._touch_idx = (self._touch_idx + 1) % 3
                circle = self._touch_effect_cache[self._touch_idx]
                circle.setPosition(pos)
                if scale is not None:
                    circle.setScale(scale)
                circle.stopAllActions()
                circle.PlayAnimation(click_name)
            else:
                circle = global_data.uisystem.load_template_create('battle/i_fight_button')
                circle.setPosition(pos)
                if scale is not None:
                    circle.setScale(scale)
                circle.PlayAnimation(click_name)
                self.panel.AddChild('', circle)
                self._touch_effect_cache.append(circle)
                self._touch_idx = len(self._touch_effect_cache) - 1
        return

    def process_global_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        for event, func_names in six.iteritems(self.GLOBAL_EVENT):
            if isinstance(func_names, str):
                func_names = (
                 func_names,)
            for func_name in func_names:
                func = getattr(self, func_name)
                if func and callable(func):
                    func_list = econf.setdefault(event, [])
                    func_list.append(func)

        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def add_blocking_ui_list(self, ui_name_list):
        ui_name_list = ui_name_list if isinstance(ui_name_list, set) else set(ui_name_list)
        self._blocking_set = self._blocking_set | ui_name_list
        global_data.ui_mgr.add_blocking_tag(self._blocking_set, self.__class__.__name__)
        for ui_name in ui_name_list:
            if ui_name != self._panelName:
                ui = global_data.ui_mgr.get_ui(ui_name)
                if ui and ui.check_can_hide_count(self.__class__.__name__):
                    ui.add_hide_count(self.__class__.__name__)

    def remove_blocking_ui_list(self):
        for ui_name in self._blocking_set:
            if ui_name != self._panelName:
                ui = global_data.ui_mgr.get_ui(ui_name)
                if ui:
                    ui.add_show_count(self.__class__.__name__)

        global_data.ui_mgr.remove_blocking_tag(self._blocking_set, self.__class__.__name__)
        self._blocking_set = set()

    def add_associate_vis_ui(self, child_ui_name):
        if child_ui_name not in self.associate_vis_ui_list:
            self.associate_vis_ui_list.add(child_ui_name)
            self.update_associate_vis_ui_visible()

    def remove_associate_vis_ui(self, child_ui_name):
        if child_ui_name in self.associate_vis_ui_list:
            self.associate_vis_ui_list.remove(child_ui_name)
            ui = global_data.ui_mgr.get_ui(child_ui_name)
            if ui:
                ui.remove_count_key(self.__class__.__name__)
            global_data.ui_mgr.remove_blocking_tag([child_ui_name], self.__class__.__name__)

    def update_associate_vis_ui_visible(self):
        if not self.associate_vis_ui_list:
            return
        if not self.panel.isVisible():
            global_data.ui_mgr.add_blocking_tag(self.associate_vis_ui_list, self.__class__.__name__)
            for ui_name in self.associate_vis_ui_list:
                if ui_name != self._panelName:
                    ui = global_data.ui_mgr.get_ui(ui_name)
                    if ui and ui.check_can_hide_count(self.__class__.__name__):
                        ui.add_hide_count(self.__class__.__name__)

        else:
            for ui_name in self.associate_vis_ui_list:
                if ui_name != self._panelName:
                    ui = global_data.ui_mgr.get_ui(ui_name)
                    if ui:
                        ui.add_show_count(self.__class__.__name__)

            global_data.ui_mgr.remove_blocking_tag(self.associate_vis_ui_list, self.__class__.__name__)

    def init_hot_key_event(self):
        from logic.gutils.pc_utils import check_can_enable_pc_mode
        if not check_can_enable_pc_mode():
            return
        if self.HOT_KEY_FUNC_MAP or self.ENABLE_HOT_KEY_SUPPORT or self.HOT_KEY_FUNC_MAP_SHOW or self.MOUSE_CURSOR_TRIGGER_SHOW or self.HOT_KEY_NEED_SCROLL_SUPPORT:
            try:
                global_data.emgr.hot_key_swtich_on_event += self.on_switch_on_hot_key
                global_data.emgr.hot_key_conf_refresh_event += self.on_refresh_hot_key
                global_data.emgr.hot_key_swtich_off_event += self.on_switch_off_hot_key
            except:
                pass

    def unregist_hot_key_event(self):
        from logic.gutils.pc_utils import check_can_enable_pc_mode
        if not check_can_enable_pc_mode():
            return
        if self.HOT_KEY_FUNC_MAP or self.ENABLE_HOT_KEY_SUPPORT or self.HOT_KEY_FUNC_MAP_SHOW or self.MOUSE_CURSOR_TRIGGER_SHOW or self.HOT_KEY_NEED_SCROLL_SUPPORT:
            try:
                global_data.emgr.hot_key_swtich_on_event -= self.on_switch_on_hot_key
                global_data.emgr.hot_key_conf_refresh_event -= self.on_refresh_hot_key
                global_data.emgr.hot_key_swtich_off_event -= self.on_switch_off_hot_key
            except:
                pass

    def register_func_key_mapping(self):
        self.unregister_func_key_mapping()
        self._registered_hot_key_funcs = []
        if not global_data.pc_ctrl_mgr:
            return
        else:
            from logic.gutils.hot_key_utils import hot_key_func_to_hot_key
            from common.framework import Functor
            if self.HOT_KEY_FUNC_MAP:
                registed_hot_key_func_name = set()
                for hot_key_func_def, func_spec in six.iteritems(self.HOT_KEY_FUNC_MAP):
                    event_name = 'DOWN'
                    if '.' in hot_key_func_def:
                        hot_key_func_name, event_name = hot_key_func_def.split('.')
                    else:
                        hot_key_func_name = hot_key_func_def
                    if type(func_spec) is tuple:
                        func_name, func_args = func_spec
                        func = getattr(self, func_name)
                        final_func = Functor(func, func_args)
                    else:
                        final_func = getattr(self, func_spec)
                    if event_name == 'CANCEL':
                        global_data.pc_ctrl_mgr.register_cancel_func(hot_key_func_name, final_func)
                        continue

                    def final_func_wrapper(msg, keycode, final_func=final_func):
                        if not self.panel:
                            return False
                        if self.HOT_KEY_CHECK_VISIBLE and not self.panel.IsVisible():
                            if not self._will_cause_panel_hide(pc_const.PANEL_HIDE_REASON_DUE_TO_PC_HOTKEY_HINT_DISPLAY_OPTION):
                                return False
                        from logic.vscene.parts.ctrl.KeyboardMouseOperations import can_respond_to_key
                        if not can_respond_to_key(keycode, msg):
                            return False
                        if final_func:
                            global_data.is_key_mocking_ui_event = True
                            res = final_func(msg, keycode)
                            global_data.is_key_mocking_ui_event = False
                            return res

                    hot_key, msg_func_dict = global_data.pc_ctrl_mgr.prepare_key_callback(hot_key_func_name, event_name, final_func_wrapper)
                    if hot_key is None or msg_func_dict is None:
                        continue
                    if not (event_name and hot_key and final_func):
                        log_error('register_func_key_mapping have errors', event_name, hot_key_func_name, hot_key, msg_func_dict)
                        continue
                    if hot_key_func_name in registed_hot_key_func_name:
                        log_error('register_func_key_mapping have multiple definition!', event_name, hot_key_func_name, final_func)
                        continue
                    registed_hot_key_func_name.add(hot_key_func_name)
                    for msg, func in six.iteritems(msg_func_dict):
                        global_data.pc_ctrl_mgr.register_key_callback(hot_key, msg, func, hot_key_func_name)
                        self._registered_hot_key_funcs.append((hot_key, msg, func))

            return

    def unregister_func_key_mapping(self):
        if not global_data.pc_ctrl_mgr:
            return
        if self._registered_hot_key_funcs:
            for item in self._registered_hot_key_funcs:
                hot_key, event_name, func = item
                global_data.pc_ctrl_mgr.unregister_key_callback(hot_key, event_name, func)

            self._registered_hot_key_funcs = []
        for hot_key_func_def, func_spec in six.iteritems(self.HOT_KEY_FUNC_MAP):
            if '.' in hot_key_func_def:
                hot_key_func_name, event_name = hot_key_func_def.split('.')
                if event_name == 'CANCEL':
                    global_data.pc_ctrl_mgr.unregister_cancel_func(hot_key_func_name)

    def on_switch_on_hot_key(self):
        if self.isPanelVisible():
            if self.MOUSE_CURSOR_TRIGGER_SHOW:
                if global_data.mouse_mgr:
                    global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)
        self.unregister_func_key_mapping()
        if self.isPanelVisible():
            self.register_func_key_mapping()
        self.on_hot_key_opened_state()

    def on_refresh_hot_key(self):
        self._registered_hot_key_funcs = []
        if self.isPanelVisible():
            self.register_func_key_mapping()
        if global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.is_pc_control_enable():
            self.on_hot_key_opened_state()
        self.on_refresh_hot_key_imp()

    def on_refresh_hot_key_imp(self):
        pass

    def on_switch_off_hot_key(self):
        if self.HOT_KEY_NEED_SCROLL_SUPPORT and not self.NEED_SCROLL_ALWAYS:
            self.unregister_mouse_scroll_event()
        self.on_hot_key_closed_state()

    def on_hot_key_closed_state(self):
        for hot_key_func_name in six.iterkeys(self.HOT_KEY_FUNC_MAP_SHOW):
            if hot_key_func_name in self._hotkey_should_show_set:
                self._hotkey_should_show_set.remove(hot_key_func_name)
            self.check_hotkey_show(hot_key_func_name)

        self.on_hot_key_state_closed()

    def on_hot_key_state_closed(self):
        pass

    def on_hot_key_opened_state(self):
        for hot_key_func_name in six.iterkeys(self.HOT_KEY_FUNC_MAP_SHOW):
            self._hotkey_should_show_set.add(hot_key_func_name)
            self.check_hotkey_show(hot_key_func_name)

        if self.HOT_KEY_NEED_SCROLL_SUPPORT and not self.NEED_SCROLL_ALWAYS:
            self.register_mouse_scroll_event()
        self.on_hot_key_state_opened()

    def on_hot_key_state_opened(self):
        pass

    def register_mouse_scroll_event(self):
        key = self.__class__.__name__
        scroll_priority = confmgr.get('c_hot_key_parameter', 'scroll_priority_dict', key, default=0)
        mouse_mgr = global_data.mouse_mgr
        if mouse_mgr:
            mouse_mgr.register_wheel_event(scroll_priority, self.__class__.__name__, self._inner_on_hot_key_mouse_scroll)
            self._is_register_mouse_scroll = True

    def unregister_mouse_scroll_event(self):
        if self._is_register_mouse_scroll:
            key = self.__class__.__name__
            scroll_priority = confmgr.get('c_hot_key_parameter', 'scroll_priority_dict', key, default=0)
            mouse_mgr = global_data.mouse_mgr
            if mouse_mgr:
                mouse_mgr.unregister_wheel_event(scroll_priority, self.__class__.__name__)
                self._is_register_mouse_scroll = False

    def _inner_on_hot_key_mouse_scroll(self, msg, delta, key_state):
        if not self.panel:
            return False
        if self.HOT_KEY_CHECK_VISIBLE and not self.panel.IsVisible():
            return False
        if not self.check_can_mouse_scroll():
            return False
        self.on_hot_key_mouse_scroll(msg, delta, key_state)
        return True

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        pass

    def check_can_mouse_scroll(self):
        raise NotImplementedError('need override check_can_mouse_scroll')

    def on_resolution_changed(self):
        pass

    def get_hotkey_show_condition(self, hot_key_func_name):
        func_name = self.HOT_KEY_FUNC_MAP_SHOW_CONDITIONAL.get(hot_key_func_name, None)
        if not func_name:
            return
        else:
            return getattr(self, func_name, None)

    def check_hotkey_show(self, hot_key_func_name):
        common_show = hot_key_func_name in self._hotkey_should_show_set
        cond = self.get_hotkey_show_condition(hot_key_func_name)
        if not cond:
            show = common_show
        else:
            show = cond(common_show)
        self.switch_hot_key_node(hot_key_func_name, show)

    def switch_hot_key_node(self, hot_key_func_name, enable):
        from logic.gutils.hot_key_utils import get_hot_key_short_display_name_ex, set_hot_key_common_tip
        conf = self.HOT_KEY_FUNC_MAP_SHOW.get(hot_key_func_name, {})
        node_paths = conf.get('node', '')
        text_path = conf.get('text', '')

        def switch_node_path(node_path):
            top_node = None
            ctrl = self
            ctrlnamelist = node_path.split('.')
            for name in ctrlnamelist:
                ctrl = getattr(ctrl, name)
                if not ctrl:
                    log_error('error when show pc hot key!', hot_key_func_name, conf)
                    return

            if ctrl:
                ctrl.setVisible(enable)
                top_node = ctrl
            return top_node

        if text_path:
            ctrl = self
            ctrlnamelist = text_path.split('.')
            for name in ctrlnamelist:
                ctrl = getattr(ctrl, name)
                if not ctrl:
                    log_error('error when show pc hot key!', hot_key_func_name, conf)
                    return

            text_node = ctrl
            if text_node:
                text_node.setVisible(enable)
                if enable:
                    text_node.SetString(get_hot_key_short_display_name_ex(hot_key_func_name))
        elif node_paths:
            if type(node_paths) in (tuple, list):
                for node_path in node_paths:
                    res = switch_node_path(node_path)
                    if not res:
                        continue
                    res.setVisible(enable)
                    if enable:
                        set_hot_key_common_tip(res, hot_key_func_name)

            else:
                node_path = node_paths
                res = switch_node_path(node_path)
                if not res:
                    return
                res.setVisible(enable)
                if enable:
                    set_hot_key_common_tip(res, hot_key_func_name)

    def get_invisible_reason(self):
        if self.panel and self.panel.isValid():
            for key, val in six.iteritems(self._show_count_dict):
                if val < 0:
                    log_error('hide because of key:', key, self._show_count_dict)
                    return

            self.panel.GetInvisibleReason()
        else:
            log_error('get_invisible_reason: invalid panel')

    def get_show_count_dict(self):
        return dict(self._show_count_dict)

    def set_show_count_dict(self, show_count):
        self._show_count_dict = show_count
        self._check_show_count_dict()

    def get_bg_panel(self):
        return self._base_bg_panel

    def add_sub_page(self, sub_page):
        print('add_sub_page', sub_page)
        self._sub_page_dict[sub_page.__class__.__name__] = sub_page

    def remove_sub_page(self, sub_page_or_sub_page_name):
        if not sub_page_or_sub_page_name:
            return
        if type(sub_page_or_sub_page_name) in (str, six.text_type):
            if sub_page_or_sub_page_name in self._sub_page_dict:
                self._sub_page_dict.pop(sub_page_or_sub_page_name)
        elif sub_page_or_sub_page_name.__class__.__name__ in self._sub_page_dict:
            self._sub_page_dict.pop(sub_page_or_sub_page_name.__class__.__name__)

    def get_sub_page(self, sub_page_name):
        return self._sub_page_dict.get(sub_page_name)

    def clear_sub_pages(self):
        self._sub_page_dict = {}

    def check_share_btn_tips(self):
        from logic.gutils.share_utils import is_share_enable
        from logic.comsys.share.ShareTipsWidget import ShareTipsWidget
        if not is_share_enable():
            if not global_data.is_share_show:
                if self.SHARE_TIPS_INFO:
                    share_btn = self.SHARE_TIPS_INFO[0]
                    if type(share_btn) in (str, six.text_type):
                        ctrl = self.panel
                        share_btn = ShareTipsWidget.parse_ctrl_list(ctrl, share_btn)
                    if share_btn:
                        share_btn.setVisible(False)
            return
        if self.SHARE_TIPS_INFO:
            self._share_tips_widget = ShareTipsWidget(self, self.panel, *self.SHARE_TIPS_INFO)