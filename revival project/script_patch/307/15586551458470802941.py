# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfoUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER_1, UI_TYPE_MESSAGE
from common.utils.cocos_utils import ccp, CCSizeZero
from logic.comsys.battle import BattleMedCommonInfo
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_utils import battle_utils
from .BattleInfo.BattleTips import BattleTips, BattleTipsManager
from . import BattleInfoKill
from . import BattleInfoCoin
from . import BattleInfoCircle
from . import BattleInfoRank
from . import BattleInfoReport
from . import BattleInfoParadrop
from . import BattleInfoDoublePoint
from . import BattleInfoEnemyScan
from . import BattleHitFeedBack
from . import BattleMainCommonInfo
from . import BattleInfoPlayerNumber
from . import BattleInfoPoint
from . import KothCommonCountDownInfo
from . import CommonEndCountDownInfo
from . import KothRewardRateChangedInfo
from . import BattleMedRCommonInfo
from . import BattleInfoAreaInfo
from . import BattleInfoVoice
from . import BattleMainKillAchievement
from . import BattleInfoCandyShop
from . import BattleInfoParadropBall
from . import BattleInfoArmRaceUzi
from . import BattleInfoConcert
from . import BattleCommonRiko
from . import BattleGooseBearRiko
from .Magic.MagicHunterFieldRefresh import MagicHunterFieldRefresh
from logic.gcommon.common_const import battle_const as bconst
from .BattleInfo.MiddleBattleReportParser import MiddleBattleReportParser
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.gcommon.common_const import battle_const
from logic.gcommon import const
import world
import cc
import time
from logic.comsys.guide_ui.GuideUI import GuideUI, PCGuideUI
from logic.comsys.common_ui import CommonInfoUtils
from common.const import uiconst

class BattleInfoUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/feedback'
    DLG_ZORDER = DIALOG_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_MESSAGE
    UI_ACTION_EVENT = {}
    ENHANCE_NUMBER = 10
    MAIN_NODE_MESSAGE = {battle_const.MAIN_NODE_COMMON_INFO: BattleMainCommonInfo.BattleMainCommonInfo,
       battle_const.MAIN_NODE_RANK_AWARD: BattleInfoRank.BattleInfoRank,
       battle_const.MAIN_NODE_POINT: BattleInfoPoint.BattleInfoPoint,
       battle_const.MAIN_NODE_KILL_ACHIEVEMENT: BattleMainKillAchievement.BattleMainKillAchievement
       }
    UP_NODE_MESAAGE = {}
    MED_NODE_MESSAGE = {battle_const.MED_NODE_KILL_INFO: BattleInfoKill.BattleInfoKill,
       battle_const.MED_NODE_RECRUIT_COMMON_INFO: BattleMedCommonInfo.BattleMedCommonInfo
       }
    DOWN_NODE_MESSAGE = {}
    UP_NODE_MERGE_TYPE = ()
    MAIN_NODE_MULTIPLE_TYPE = (
     battle_const.MAIN_NODE_KILL_ACHIEVEMENT,)
    MED_R_NODE_MESSAGE = {battle_const.MED_R_NODE_COMMON_INFO: BattleMedRCommonInfo.BattleMedRCommonInfo
       }
    UP_LEFT_NODE_MERGE_TYPE = (
     battle_const.UP_NODE_PLAYER_NUMBER,)
    UP_LEFT_NODE_MESSAGE = {battle_const.UP_NODE_POISON_CIRCLE: BattleInfoCircle.BattleInfoCircle,
       battle_const.UP_NODE_PLAYER_NUMBER: BattleInfoPlayerNumber.BattleInfoPlayerNumber,
       battle_const.UP_NODE_PARADROP_BALL: BattleInfoParadropBall.BattleInfoParadropBall,
       battle_const.UP_NODE_PARADROP: BattleInfoParadrop.BattleInfoParadrop,
       battle_const.UP_NODE_CANDY_SHOP: BattleInfoCandyShop.BattleInfoCandyShop,
       battle_const.UP_NODE_AREA_INFO: BattleInfoAreaInfo.BattleInfoAreaInfo,
       battle_const.UP_NODE_ANCHOR_VOICE: BattleInfoVoice.BattleInfoVoice,
       battle_const.UP_NODE_ARMRACE_UZI: BattleInfoArmRaceUzi.BattleInfoArmRaceUzi,
       battle_const.UP_NODE_CONCERT_ANCHOR: BattleInfoConcert.BattleInfoConcert,
       battle_const.UP_NODE_COMMON_RIKO_TIPS: BattleCommonRiko.BattleCommonRiko,
       battle_const.UP_NODE_GOOSEBEAR_RIKO_TIPS: BattleGooseBearRiko.BattleGooseBearRiko
       }
    PRELOAD_GAME_MODE_SPECIFIED_MESSAGE = {battle_const.UP_NODE_POISON_CIRCLE: game_mode_const.GAME_MODE_SURVIVALS,
       battle_const.UP_NODE_PLAYER_NUMBER: game_mode_const.GAME_MODE_SURVIVALS,
       battle_const.UP_NODE_PARADROP_BALL: game_mode_const.GAME_MODE_SURVIVALS,
       battle_const.UP_NODE_CANDY_SHOP: game_mode_const.GAME_MODE_SURVIVALS,
       battle_const.UP_NODE_AREA_INFO: game_mode_const.GAME_MODE_SURVIVALS,
       battle_const.UP_NODE_ARMRACE_UZI: game_mode_const.GAME_MODE_ARMRACE,
       battle_const.UP_NODE_CONCERT_ANCHOR: game_mode_const.GAME_MODE_CONCERT
       }
    PRELOAD_ENVIRONMENT_SPECIFIED_MESSAGES = {battle_const.UP_NODE_CANDY_SHOP: battle_const.BATTLE_ENV_NEUTRAL_SHOP,
       battle_const.UP_NODE_PARADROP_BALL: battle_const.BATTLE_ENV_SUMMER
       }
    GLOBAL_EVENT = {'scene_player_setted_event': 'on_player_setted',
       'scene_camera_player_setted_event': '_on_scene_camera_player_setted_event',
       'battle_show_message_event': 'show_message',
       'update_alive_player_num_event': 'update_alive_player_num',
       'show_battle_report_event': 'show_battle_report',
       'scene_refresh_poison_circle_event': 'refresh_poison_circle',
       'battle_event_message': 'show_event_message',
       'battle_down_message': 'show_down_message',
       'agent_coin_get_event': 'show_get_coin',
       'on_throw_enent': 'on_throw_event',
       'player_make_damage_event': '_show_damage_ui_effect',
       'show_battle_main_message': 'show_main_message',
       'finish_battle_main_message': 'finish_main_message',
       'show_battle_med_message': 'show_med_message',
       'show_battle_med_r_message': 'show_med_r_message',
       'show_item_fly_to_bag_message_event': 'show_item_fly_to_bag_ani',
       'show_human_tips': 'show_human_tips',
       'block_battle_message_by_type': 'block_battle_message_by_type'
       }

    def on_init_panel(self):
        self.is_in_observe = False
        self.init_parameters()
        self.init_survive_panel_event()
        global_data.emgr.battle_info_ui_created.emit()
        if not global_data.is_32bit:
            self.preload_message_ui()

    def preload_message_ui(self):
        type_finish_func_tuple = [
         (
          self.MAIN_NODE_MESSAGE, self.finish_main_message_show),
         (
          self.UP_NODE_MESAAGE, self.finish_event_show),
         (
          self.MED_NODE_MESSAGE, self.finish_med_message_show),
         (
          self.DOWN_NODE_MESSAGE, self.finish_down_message_show),
         (
          self.MED_R_NODE_MESSAGE, self.finish_med_r_message_show),
         (
          self.UP_LEFT_NODE_MESSAGE, self.finish_up_left_message_show)]
        for queue_type, finish_func in type_finish_func_tuple:
            for message_type, node_cls in six.iteritems(queue_type):
                if not self.is_mode_show_tips(message_type):
                    continue
                node_cls(self.panel, finish_func)

        if global_data.battle and global_data.battle.battle_tid:
            CommonInfoUtils.preload_battle_ui(global_data.battle.battle_tid)

    def is_mode_show_tips(self, message_type):
        if message_type == battle_const.UP_NODE_AREA_INFO and global_data.game_mode.is_mode_type(game_mode_const.Hide_AreaInfo):
            return False
        if message_type in self.PRELOAD_GAME_MODE_SPECIFIED_MESSAGE:
            if not global_data.game_mode.is_mode_type(self.PRELOAD_GAME_MODE_SPECIFIED_MESSAGE[message_type]):
                return False
        if message_type in self.PRELOAD_ENVIRONMENT_SPECIFIED_MESSAGES:
            enviroment = global_data.game_mode.get_enviroment()
            if enviroment != self.PRELOAD_ENVIRONMENT_SPECIFIED_MESSAGES[message_type]:
                return False
        return True

    def on_finalize_panel(self):
        self._notice_message_queue.destroy()
        self.player = None
        global_data.ui_mgr.close_ui('BattleInfoParadrop')
        global_data.ui_mgr.close_ui('BattleInfoKill')
        global_data.ui_mgr.close_ui('BattleInfoCoin')
        global_data.ui_mgr.close_ui('BattleInfoCircle')
        global_data.ui_mgr.close_ui('BattleInfoRank')
        global_data.ui_mgr.close_ui('BattleInfoReport')
        global_data.ui_mgr.close_ui('BattleInfoDoublePoint')
        global_data.ui_mgr.close_ui('BattleInfoEnemyScan')
        global_data.ui_mgr.close_ui('BattleHitFeedBack')
        global_data.ui_mgr.close_ui('BattleInfoPlayerNumber')
        global_data.ui_mgr.close_ui('KothRewardRateChangedInfo')
        global_data.ui_mgr.close_ui('KothCommonCountDownInfo')
        global_data.ui_mgr.close_ui('CommonEndCountDownInfo')
        global_data.ui_mgr.close_ui('BattleInfoVoice')
        global_data.ui_mgr.close_ui('BattleInfoCandyShop')
        global_data.ui_mgr.close_ui('BattleInfoArmRaceUzi')
        global_data.ui_mgr.close_ui('MagicHunterFieldRefresh')
        return

    def init_parameters(self):
        self.player = None
        self.show_poison_time = None
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        self.panel.setVisible(False)
        self.is_player_not_first_setted = True
        self.cur_survive_num = 0
        self._event_message_queue = []
        self._is_showing_event_message = 0
        self._last_event_type = None
        self._need_break = False
        self.block_message_type_dict = {}
        self.block_message_type_set = set()
        self._down_message_queue = []
        self._can_show_down_message = True
        self._med_message_queue = []
        self._can_show_med_message = True
        self._main_message_queue = []
        self._can_show_main_message = True
        self._cur_processing_main_message = None
        self._med_r_message_queue = []
        self._can_show_med_r_message = True
        self._poison_circle_message_queue = []
        self._player_number_message_queue = []
        self._up_left_message_queue = []
        self._can_show_up_left_message = True
        self._last_up_left_type = None
        self._notice_message_queue = BattleTipsManager(self.panel.hint_2, BattleTips, max_msg_num=2, preload_tip_num=2)
        self.panel.RecordAnimationNodeState('armor_fix')
        if player:
            spec_target = player.ev_g_spectate_target()
            if spec_target:
                self.on_enter_observed(spec_target)
            else:
                self.on_player_setted(player)
        return

    def _on_scene_camera_player_setted_event(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.player = player
        if player:
            if self.is_player_not_first_setted:
                self.panel.setVisible(True)
                self.is_player_not_first_setted = False
            self.update_alive_player_num(self.player.get_battle().alive_player_num)
            self.update_all_kill_num(self.player.id, self.player.ev_g_groupmate())
            self._show_next_down_message()
            self._show_next_med_message()
            self._show_next_main_message()
            self._show_next_med_r_message()
            self._show_next_up_left_message()

    def show_message(self, msg, **kargs):
        self._notice_message_queue.add_tips(msg, ignore_check=kargs.get('ignore_check', False))

    def reset_num_nd(self, nd):
        nd.kill_num.stopAllActions()
        nd.new_kill_num.stopAllActions()
        nd.kill_num.SetPosition(nd.kill_num.getPosition().x, '50%')
        nd.kill_num.setOpacity(255)
        nd.new_kill_num.setOpacity(0)
        nd.new_kill_num.SetPosition(nd.new_kill_num.getPosition().x, '50%-29')

    def _show_num_ani(self, nd, old_num, new_num):
        move_action = cc.MoveBy.create(0.3, ccp(0, 29))
        nd.kill_num.runAction(cc.Spawn.create([
         move_action,
         cc.FadeOut.create(0.3)]))
        nd.new_kill_num.runAction(cc.Spawn.create([
         move_action,
         cc.FadeTo.create(0.3, 255)]))

    def update_alive_player_num(self, player_num):
        if player_num == self.cur_survive_num:
            return
        if player_num > self.ENHANCE_NUMBER:
            global_data.emgr.update_map_info_widget_event.emit(player_num)
        elif not global_data.game_mode.is_mode_type(game_mode_const.Hide_AlivePlayerNumTip) and player_num < self.cur_survive_num:
            self._player_number_message_queue.append(((self.cur_survive_num, player_num), battle_const.UP_NODE_PLAYER_NUMBER))
            self._show_next_up_left_message()
        else:
            global_data.emgr.update_map_info_widget_event.emit(player_num)
        self.cur_survive_num = player_num

    def show_human_tips(self, text_id, time_out, **kwargs):
        msg = (
         (
          text_id, time_out, kwargs), battle_const.UP_NODE_HUMAN_TIP)
        if self._last_up_left_type == battle_const.UP_NODE_HUMAN_TIP:
            self._show_next_up_left_message(msg)
        else:
            self._up_left_message_queue.append(msg)
            self._show_next_up_left_message()

    def block_battle_message_by_type(self, block, message_type_list, tag=None):
        if tag not in self.block_message_type_dict:
            self.block_message_type_dict[tag] = set()
        if block:
            self.block_message_type_dict[tag].update(message_type_list)
        else:
            self.block_message_type_dict[tag] = set()
        self.block_message_type_set = set()
        for mtype_set in six.itervalues(self.block_message_type_dict):
            self.block_message_type_set.update(mtype_set)

    def init_survive_panel_event(self):
        battle = global_data.player.get_joining_battle() or global_data.player.get_battle()
        player_statistics = {} if battle is None else battle.statistics.get(global_data.player.id, {})
        group_kill_statistics = 0 if battle is None else battle.group_kill_statistics
        self.my_kill_num = player_statistics.get('kill', 0)
        self.team_kill_num = group_kill_statistics
        return

    def get_text_with_checking(self, raw_msg_id):
        if raw_msg_id:
            return get_text_by_id(int(raw_msg_id))
        else:
            return ''

    def check_relate_kill(self, report_dict):
        if not self.player:
            return
        my_kill_num, team_kill_num = battle_utils.parse_battle_report_player_kill(self.player, report_dict)
        msg_dict = self.parse_self_battle_report(report_dict)
        if my_kill_num > 0:
            self.update_my_kill_num(self.my_kill_num + my_kill_num)
            global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', 'kill'))
        msg = msg_dict.get('msg')
        if msg:
            self.show_kill_info_message(msg_dict)
        self.update_team_kill_num(self.team_kill_num + team_kill_num)

    @execute_by_mode(False, (game_mode_const.GAME_MODE_KING,))
    def show_kill_info_message(self, msg_dict):
        self.show_med_message((msg_dict,), battle_const.MED_NODE_KILL_INFO)

    def parse_self_battle_report(self, report_dict):
        event_type = report_dict['event_type']
        player_id = self.player.id if self.player else None
        if event_type == bconst.FIGHT_EVENT_BLEED:
            msg, is_teammate, is_killer_in_team, is_assist = MiddleBattleReportParser().parse_self_bleed_battle_report(report_dict, player_id)
            msg_dict = {'is_knock_down': True} if is_killer_in_team else {'is_being_knock_down': True}
            msg_dict.update({'is_self': not is_teammate})
            msg_dict.update({'type_msg': get_text_by_id(18503)})
            msg_dict.update({'msg': msg})
            msg_dict.update({'kill_num': 0})
            msg_dict.update({'is_assist': is_assist})
        elif event_type in [bconst.FIGHT_EVENT_DEATH, bconst.FIGHT_EVENT_DEFEAT, bconst.FIGHT_EVENT_KILL_GROUP]:
            msg, is_teammate, is_killer_in_team, is_assist, is_critic, killer_id = MiddleBattleReportParser().parse_self_dead_battle_report(report_dict, player_id, self.cur_survive_num)
            if is_assist or is_killer_in_team:
                msg_dict = {'is_kill': True} if 1 else {'is_being_kill': True}
            else:
                msg_dict = {'is_assist': True}
            msg_dict.update({'is_self': not is_teammate})
            msg_dict.update({'type_msg': get_text_by_id(18509) if event_type in (bconst.FIGHT_EVENT_DEATH, bconst.FIGHT_EVENT_KILL_GROUP) else get_text_by_id(18514)})
            msg_dict.update({'msg': msg})
            from logic.gcommon.common_utils.battle_utils import get_player_kill_num
            kill_person_num, _ = get_player_kill_num(killer_id)
            msg_dict.update({'kill_num': kill_person_num})
            msg_dict['is_critic'] = is_critic
            msg_dict['points'] = report_dict.get('points')
        elif event_type == bconst.FIGHT_EVENT_MECHA_DEATH:
            msg, is_teammate, is_killer_in_team, is_critic, killer_id, is_assist, is_mecha_being_kill = MiddleBattleReportParser().parse_mecha_dead_battle_report(report_dict, player_id)
            msg_dict = {'is_kill_mecha': True} if is_killer_in_team else {'is_kill_mecha': False}
            msg_dict.update({'is_self': not is_teammate})
            msg_dict.update({'type_msg': get_text_by_id(18509)})
            msg_dict.update({'msg': msg})
            msg_dict.update({'is_assist': is_assist})
            from logic.gcommon.common_utils.battle_utils import get_player_kill_num
            _, kill_mecha_num = get_player_kill_num(killer_id)
            msg_dict.update({'kill_num': kill_mecha_num})
            msg_dict['is_critic'] = is_critic
            msg_dict['points'] = report_dict.get('points')
            msg_dict['is_mecha_being_kill'] = is_mecha_being_kill
        else:
            msg, is_teammate, is_killer_in_team = (None, None, None)
            msg_dict = {}
        if msg_dict:
            _, death_trigger_dict = report_dict.get('death_source') or (bconst.FIGHT_INJ_UNKNOWN, {})
            trigger_faction = death_trigger_dict.get('trigger_faction', None)
            msg_dict['trigger_faction'] = trigger_faction
        if global_data.game_mode.get_mode_type() == game_mode_const.GAME_MODE_EXERCISE and (msg_dict.get('is_assist', False) == True or msg_dict.get('is_self', True) == False):
            msg_dict['msg'] = None
        return msg_dict

    def check_need_get_specified_weapon_name(self, damage_type):
        from common.cfg import confmgr
        weapon_id = confmgr.get('death_notice_detail', str(damage_type), default={}).get('cNoticeWeapon', None)
        if not weapon_id:
            return False
        else:
            return True
            return

    def show_battle_report(self, report_dict):
        if not self.player:
            return
        self.check_relate_kill(report_dict)
        self.check_bleed(report_dict)
        self.recruit_mode_check_ai(report_dict)

    def _show_damage_ui_effect(self, *args, **kwargs):
        target = args[0]
        damage_info = args[1]
        if damage_info and isinstance(damage_info, dict):
            hit_part = const.HIT_PART_OTHER
            damage = 0
            for part in damage_info:
                if part == const.HIT_PART_HEAD:
                    hit_part = const.HIT_PART_HEAD
                info = damage_info[part]
                if isinstance(info, (tuple, list)) and len(info) == 2:
                    damage += damage_info[part][0] * damage_info[part][1]

        else:
            hit_part = const.HIT_PART_OTHER
            damage = 0 if 'shield_damage' not in kwargs else kwargs['shield_damage']
        ui = global_data.ui_mgr.get_ui('BattleHitFeedBack')
        if ui is None:
            ui = BattleHitFeedBack.BattleHitFeedBack(self.panel)
        ui.deal_message((bconst.FIGHT_EVENT_DAMAGE, target, damage, hit_part))
        return

    def recruit_mode_check_ai(self, report_dict):
        from logic.gcommon.common_const.battle_const import PLAY_TYPE_RECRUITMENT
        from logic.gcommon.common_utils.battle_utils import get_play_type_by_battle_id
        if not global_data.battle or get_play_type_by_battle_id(global_data.battle.get_battle_tid()) != PLAY_TYPE_RECRUITMENT:
            return
        else:
            if global_data.cam_lplayer and len(global_data.cam_lplayer.ev_g_groupmate()) == 3:
                return
            event_type = report_dict['event_type']
            from logic.gcommon.common_const import battle_const as bconst
            killer_id = None
            if event_type == bconst.FIGHT_EVENT_BLEED:
                bleed_damage_type, bleed_trigger_dict = report_dict.get('bleed_source') or (bconst.FIGHT_INJ_UNKNOWN, {})
                killer_id = bleed_trigger_dict.get('trigger_id')
            if killer_id and killer_id == global_data.player.id:
                injured_id = report_dict.get('injured_id', global_data.player.id)
                ent = global_data.battle.get_entity(injured_id)
                target_type = ent.logic.__class__.__name__
                if target_type != 'LPuppetRobot':
                    global_data.emgr.show_human_tips.emit(get_text_by_id(83169), 5)
            return

    @execute_by_mode(False, (game_mode_const.GAME_MODE_EXERCISE,))
    def check_bleed(self, report_dict):
        event_type = report_dict['event_type']
        from logic.gcommon.common_const import battle_const as bconst
        killer_id = None
        if event_type == bconst.FIGHT_EVENT_BLEED:
            bleed_damage_type, bleed_trigger_dict = report_dict.get('bleed_source') or (bconst.FIGHT_INJ_UNKNOWN, {})
            killer_id = bleed_trigger_dict.get('trigger_id')
        elif event_type in (bconst.FIGHT_EVENT_DEATH, bconst.FIGHT_EVENT_MECHA_DEATH, bconst.FIGHT_EVENT_MONSTER_DEATH, bconst.FIGHT_EVENT_KILL_GROUP):
            death_damage_type, death_trigger_dict = report_dict.get('death_source') or (bconst.FIGHT_INJ_UNKNOWN, {})
            killer_id = death_trigger_dict.get('trigger_id')
        elif event_type in (bconst.FIGHT_EVENT_DEFEAT,):
            death_damage_type, death_trigger_dict = report_dict.get('death_source') or (bconst.FIGHT_INJ_UNKNOWN, {})
            killer_id = death_trigger_dict.get('trigger_id')
        if killer_id and killer_id == global_data.player.id:
            ui = global_data.ui_mgr.get_ui('BattleHitFeedBack')
            if ui is None:
                ui = BattleHitFeedBack.BattleHitFeedBack(self.panel)
            ui.deal_message(event_type)
            global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', 'knock_down'))
        return

    def check_shoot_damage(self, report_dict):
        pass

    def update_my_kill_num(self, my_kill_num):
        self.my_kill_num = my_kill_num

    def update_team_kill_num(self, team_kill_num):
        self.team_kill_num = team_kill_num

    def refresh_poison_circle(self, state, refresh_time, last_time, level, poison_point, safe_point, reduce_type):
        if level == 0 or last_time == 0.0 or global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_GOOSE_BEAR):
            return
        else:

            def show_delay_poison_text(msg=None):
                from logic.gcommon.time_utility import time
                server_time = time()
                delay_time = refresh_time + last_time - server_time
                if delay_time < 0:
                    return
                else:

                    def _cc_show_event_message(msg=msg):
                        self._poison_circle_message_queue.append(((refresh_time, last_time, msg, reduce_type), battle_const.UP_NODE_POISON_CIRCLE))
                        self._show_next_up_left_message()

                    if delay_time > 0.5:
                        self.show_poison_time = self.panel.SetTimeOut(delay_time - 0.5, _cc_show_event_message)
                    else:
                        _cc_show_event_message(None)
                    return

            if self.show_poison_time:
                self.panel.stopAction(self.show_poison_time)
                self.dis_appear_anim = None
            show_delay_poison_text()
            return

    def show_bombing_area(self, *args):
        pass

    def show_event_message(self, message, bg_pic_path='', sign_pic_path='', message_type=None):
        if not self.is_mode_show_tips(message_type):
            return
        if message_type not in self.UP_NODE_MESAAGE:
            if message_type in self.UP_LEFT_NODE_MESSAGE:
                self.show_up_left_message(message, message_type)
            return
        if message_type in (battle_const.UP_NODE_TURN_WARN, battle_const.UP_NODE_TURN_COUNTDOWN):
            self._need_break = True
            self._event_message_queue.insert(0, (bg_pic_path, sign_pic_path, message, message_type))
        else:
            self._event_message_queue.append((bg_pic_path, sign_pic_path, message, message_type))
        self._show_next_event_message()

    def finish_event_show(self):
        self._is_showing_event_message = 0
        self.finish_event_msg_show()

    def _show_next_event_message(self):
        if len(self._event_message_queue) <= 0:
            return
        msg = self._event_message_queue[0]
        bg_pic_path, sign_pic_path, text, message_type = msg
        need_merge = message_type == self._last_event_type and message_type in self.UP_NODE_MERGE_TYPE
        if self._last_event_type == battle_const.UP_NODE_AREA_INFO:
            self._need_break = True
        cur_time = time.time()
        if self._is_showing_event_message and cur_time - self._is_showing_event_message < 20 and not need_merge and not self._need_break:
            return
        if self._need_break and self._last_event_type:
            self._need_break = False
            battle_info_message = self.UP_NODE_MESAAGE[self._last_event_type]
            ui = global_data.ui_mgr.get_ui(battle_info_message.__name__)
            if ui:
                ui.clear_message()
        self._is_showing_event_message = cur_time
        self._event_message_queue.pop(0)
        battle_info_message = self.UP_NODE_MESAAGE[message_type]
        ui = global_data.ui_mgr.get_ui(battle_info_message.__name__)
        if not ui:
            ui = battle_info_message(self.panel, self.finish_event_show)
        ui.add_message(text)
        self._last_event_type = message_type
        self._show_next_event_message()

    def finish_event_msg_show(self):
        self._show_next_event_message()

    def on_throw_event(self, time, finish_callback):
        from logic.comsys.control_ui.ThrowProgressUI import ThrowProgressUI
        ThrowProgressUI().show_progress(time, finish_callback)

    def show_get_coin(self, num, reason=None):
        if num <= 0 or reason is None:
            return
        else:
            from logic.gcommon import const
            if reason == const.KILL_ADD_EXTRA_COIN:
                msg = {'i_type': battle_const.MAIN_KILL_AWARD}
                self.show_main_message(msg, battle_const.MAIN_NODE_COMMON_INFO)
                global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                       'achievement_level4'))
            return

    def on_enter_observed(self, ltarget):
        self.is_in_observe = True
        self.on_player_setted(ltarget)

    def update_all_kill_num(self, player_id, teammate_ids):
        battle = global_data.player.get_joining_battle() or global_data.player.get_battle()
        battle_stat = {} if battle is None else battle.statistics
        player_statistics = battle_stat.get(player_id, {})
        self.my_kill_num = player_statistics.get('kill', 0)
        tmp_team_kill_num = 0
        for t_id in teammate_ids:
            tmp_team_kill_num += battle_stat.get(t_id, {}).get('kill', 0)

        self.update_team_kill_num(tmp_team_kill_num)
        return

    def show_down_message(self, message, message_type):
        if message_type not in self.DOWN_NODE_MESSAGE:
            return
        self._down_message_queue.append((message, message_type))
        self._show_next_down_message()

    def finish_down_message_show(self):
        self._can_show_down_message = True
        if not global_data.player:
            return
        self._show_next_down_message()

    def _show_next_down_message(self):
        if not self._can_show_down_message:
            return
        while True:
            if len(self._down_message_queue) <= 0:
                return
            msg = self._down_message_queue.pop(0)
            text, message_type = msg
            if message_type not in self.block_message_type_set:
                break

        self._can_show_down_message = False
        battle_info_message = self.DOWN_NODE_MESSAGE[message_type]
        ui = global_data.ui_mgr.get_ui(battle_info_message.__name__)
        if not ui:
            ui = battle_info_message(self.panel, self.finish_down_message_show)
        ui.add_message(*text)

    def show_med_message(self, message, message_type):
        if message_type not in self.MED_NODE_MESSAGE:
            return
        self._med_message_queue.append((message, message_type))
        self._show_next_med_message()

    def finish_med_message_show(self):
        self._can_show_med_message = True
        if not global_data.player:
            return
        self._show_next_med_message()

    def _show_next_med_message(self):
        if not self._can_show_med_message:
            return
        if len(self._med_message_queue) > 0:
            msg = self._med_message_queue.pop(0)
            text, message_type = msg
            self._can_show_med_message = False
            battle_info_message = self.MED_NODE_MESSAGE[message_type]
            ui = global_data.ui_mgr.get_ui(battle_info_message.__name__)
            if not ui:
                ui = battle_info_message(self.panel, self.finish_med_message_show)
            ui.add_message(*text)

    def show_main_message(self, message, message_type, push_to_head=False, multi_message=False):
        if not multi_message:
            message = [
             message]
            message_type = [message_type]
        for m_t in message_type:
            if m_t not in self.MAIN_NODE_MESSAGE:
                return

        if push_to_head:
            for i in range(len(message)):
                self._main_message_queue.insert(0, (message[i], message_type[i]))

        else:
            for i in range(len(message)):
                self._main_message_queue.append((message[i], message_type[i]))

        self._show_next_main_message()

    def finish_main_message(self, message, message_type, clear_all=False):
        if message_type not in self.MAIN_NODE_MESSAGE:
            return
        if clear_all:
            self._main_message_queue = [ message_pack for message_pack in self._main_message_queue if message_pack[0] != message or message_pack[1] != message_type ]
        battle_info_message = self.MAIN_NODE_MESSAGE[message_type]
        if self._cur_processing_main_message:
            if self._cur_processing_main_message == (message, message_type):
                ui = global_data.ui_mgr.get_ui(battle_info_message.__name__)
                if ui:
                    global_data.ui_mgr.close_ui(battle_info_message.__name__)
                    self.finish_main_message_show()

    def finish_main_message_show(self):
        self._can_show_main_message = True
        self._cur_processing_main_message = None
        if not global_data.player:
            return
        else:
            self._show_next_main_message()
            return

    def _show_next_main_message(self):
        if len(self._main_message_queue) <= 0:
            return
        if not self._can_show_main_message:
            need_merge = False
            if self._cur_processing_main_message:
                msg = self._cur_processing_main_message
                message, message_type = msg
                next_msg = self._main_message_queue[0]
                next_message, next_message_type = next_msg
                if message_type == next_message_type and message_type in self.MAIN_NODE_MULTIPLE_TYPE:
                    need_merge = True
            if not need_merge:
                return
        while True:
            if len(self._main_message_queue) <= 0:
                return
            msg = self._main_message_queue.pop(0)
            message, message_type = msg
            if message_type not in self.block_message_type_set:
                break

        self._cur_processing_main_message = msg
        self._can_show_main_message = False
        battle_info_message = self.MAIN_NODE_MESSAGE[message_type]
        ui = global_data.ui_mgr.get_ui(battle_info_message.__name__)
        if not ui:
            ui = battle_info_message(self.panel, self.finish_main_message_show)
        ui.add_message(message)
        to_be_remove_indexs = []
        for idx, next_msg in enumerate(list(self._main_message_queue)):
            next_message, next_message_type = next_msg
            if message_type == next_message_type and message_type in self.MAIN_NODE_MULTIPLE_TYPE:
                to_be_remove_indexs.append(idx)
                ui.add_message(next_message)

        for idx in reversed(to_be_remove_indexs):
            self._main_message_queue.pop(idx)

    def show_med_r_message(self, message, message_type):
        if message_type not in self.MED_R_NODE_MESSAGE:
            return
        self._med_r_message_queue.append((message, message_type))
        self._show_next_med_r_message()

    def finish_med_r_message_show(self):
        self._can_show_med_r_message = True
        if not global_data.player:
            return
        self._show_next_med_r_message()

    def _show_next_med_r_message(self):
        if not self._can_show_med_r_message:
            return
        while True:
            if len(self._med_r_message_queue) <= 0:
                return
            msg = self._med_r_message_queue.pop(0)
            message, message_type = msg
            if message_type not in self.block_message_type_set:
                break

        self._can_show_med_r_message = False
        battle_info_message = self.MED_R_NODE_MESSAGE[message_type]
        ui = global_data.ui_mgr.get_ui(battle_info_message.__name__)
        if not ui:
            ui = battle_info_message(self.panel, self.finish_med_r_message_show)
        ui.add_message(message)

    def show_up_left_message(self, message, message_type):
        if message_type not in self.UP_LEFT_NODE_MESSAGE:
            return
        self._up_left_message_queue.append((message, message_type))
        self._show_next_up_left_message()

    def finish_up_left_message_show(self):
        self._can_show_up_left_message = True
        if not global_data.player:
            return
        self._show_next_up_left_message()

    def _show_next_up_left_message(self, msg=None):
        while True:
            if msg is None:
                if not self._can_show_up_left_message:
                    return
                queue = self._up_left_message_queue
                if len(self._player_number_message_queue) > 0:
                    queue = self._player_number_message_queue
                if len(self._poison_circle_message_queue) > 0:
                    queue = self._poison_circle_message_queue
                if len(queue) <= 0:
                    return
                msg = queue.pop(0)
            message, message_type = msg
            if message_type in self.block_message_type_set:
                msg = None
            else:
                break

        self._can_show_up_left_message = False
        if message_type == battle_const.UP_NODE_HUMAN_TIP:
            text_id, time_out, kwargs = message
            cb = kwargs.get('cb', None)

            def callback(cb=cb):
                self.finish_up_left_message_show()
                if cb:
                    cb()

            if 'hot_key_func_code' in kwargs:
                self._guide_ui.do_show_human_tips_pc(text_id, time_out, hot_key_func_code=kwargs['hot_key_func_code'], cb=callback)
            else:
                self._guide_ui.do_show_human_tips(text_id, time_out, cb=callback)
        else:
            battle_info_message = self.UP_LEFT_NODE_MESSAGE[message_type]
            ui = global_data.ui_mgr.get_ui(battle_info_message.__name__)
            if not ui:
                ui = battle_info_message(self.panel, self.finish_up_left_message_show)
            ui.add_message(message)
        self._last_up_left_type = message_type
        return

    def test(self):
        from bson.objectid import ObjectId
        report = {'bleed_source': None,'death_source': [1,
                          {'maker_type': 1,'mecha_id': None,'trigger_parts': [
                                             2],
                             'trigger_id': global_data.cam_lplayer.id,
                             'die_pos': [
                                       10879.0, 207.0, -18103.0],
                             'item_id': 1002,
                             'trigger_name': u'\u91d1\u5de7\u5320\uff20\u5854\u5229\u5a05'
                             }],
           'injured_id': ObjectId('5b7a7b026dd5294bf384b9e3'),
           'injured_name': 'test_ai','event_type': 2
           }
        global_data.emgr.show_battle_report_event.emit(report)
        return

    def show_item_fly_to_bag_ani(self, item_list):
        for item_data in item_list:
            item_id = item_data.get('item_id', 0)
            self.show_item_fly_to_bag_ani_helper(item_id)

    def show_item_fly_to_bag_ani_helper(self, item_no):
        from logic.gcommon.common_const import battle_const
        from logic.gutils import template_utils, action_utils
        from logic.gutils import item_utils
        from common.cfg import confmgr
        i_type = battle_const.MED_R_EQUIPMENT_INFO

        def set_drug_ui_show_count(is_vis):
            pass

        def ani_func(node):
            ui_inst = global_data.ui_mgr.get_ui('DrugUI')
            if ui_inst:
                end_pos = ui_inst.panel.left.ConvertToWorldSpacePercentage(50, 10)
            else:
                return
            l_end_pos = node.icon.getParent().convertToNodeSpace(end_pos)
            l_start_pos = node.icon.getPosition()
            dis = l_start_pos.distance(l_end_pos)
            speed = global_data.ui_mgr.design_screen_size.width
            time = dis / speed
            act = action_utils.bezier_action_helper(time, l_start_pos, l_end_pos, normalized_p1=(0.04,
                                                                                                 0.38), normalized_p2=(0.52,
                                                                                                                       0.94))
            real_act = cc.Spawn.create([
             act,
             cc.Sequence.create([
              cc.FadeIn.create(0.06),
              cc.DelayTime.create(max(time - 0.06, 0.01)),
              cc.FadeOut.create(0.01),
              cc.CallFunc.create(lambda : set_drug_ui_show_count(True))])])
            if node.nd_lizi:
                node.nd_lizi.setVisible(True)
            node.icon.runAction(real_act)

        msg = {'i_type': i_type,
           'content_txt': get_text_by_id(81399, {'item_name': item_utils.get_item_name(item_no)}),
           'extra_disappear_time': 1,
           'extra_disappear_func': lambda node: ani_func(node),
           'item_id': item_no
           }
        set_drug_ui_show_count(False)
        global_data.emgr.show_battle_med_r_message.emit(msg, battle_const.MED_R_NODE_COMMON_INFO)

    @property
    def _guide_ui(self):
        if global_data.is_pc_mode:
            return PCGuideUI()
        else:
            return GuideUI()