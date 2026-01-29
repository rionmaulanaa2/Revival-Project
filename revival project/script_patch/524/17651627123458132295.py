# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/ADCrystalBattle.py
from __future__ import absolute_import
import six
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from logic.entities.DeathBattle import DeathBattle
from logic.gcommon import time_utility as t_util
from logic.gcommon.common_const import battle_const as bconst
import math
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_utils import battle_utils
INTERVAL_HIDE_UI_LIST = [
 'MechaUI',
 'FireRockerUI',
 'PostureControlUI',
 'MoveRockerUI',
 'MoveRockerTouchUI',
 'BulletReloadUI',
 'FightLeftShotUI',
 'HpInfoUI']

class ADCrystalBattle(DeathBattle):

    def init_from_dict(self, bdict, is_change_weapon=True):
        super(ADCrystalBattle, self).init_from_dict(bdict, is_change_weapon)
        self._round_settle_timestamp = bdict.get('round_settle_timestamp', 0)
        self._atk_group_id = bdict.get('atk_group_id')
        self._def_group_id = bdict.get('def_group_id')
        self._old_atk_group_id = bdict.get('old_atk_group_id')
        self._old_def_group_id = bdict.get('old_def_group_id')
        self._group_crystal_hp_percent = bdict.get('group_crystal_hp_percent')
        self._group_left_die_count = bdict.get('group_left_die_count')
        self._crystal_round = bdict.get('cur_round')
        self._group_crystal_points_dict = bdict.get('group_crystal_points_dict', {})
        self._my_group_id = bdict.get('my_group_id', None)
        self._low_die_cnt_buff = bdict.get('low_die_cnt_buff', [])
        self._low_die_cnt_buff_id = bdict.get('low_die_cnt_buff_id', None)
        self._round_prepare_timestamp = bdict.get('round_prepare_timestamp')
        self._group_left_time_dict = bdict.get('group_left_time_dict', {})
        self._group_crystal_player_cnt = bdict.get('group_crystal_player_cnt', {})
        self._round_status = bdict.get('round_status')
        self._last_showed_crystal_hp = 999
        self._close_transition_timer = None
        return

    def destroy(self, clear_cache=True):
        self.stop_close_transitionui_timer()
        super(ADCrystalBattle, self).destroy(clear_cache)

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'), List('born_point_list'), Dict('group_born_dict'), Dict('group_points_dict'), Dict('selected_combat_weapons'), Dict('extra_data')))
    def update_battle_data(self, settle_timestamp, born_point_list, group_born_dict, group_points_dict, selected_combat_weapons, extra_data):
        self._update_battle_data(settle_timestamp, born_point_list, group_born_dict, group_points_dict, selected_combat_weapons)
        self._round_settle_timestamp = extra_data.get('round_settle_timestamp')
        self._group_crystal_hp_percent = extra_data.get('group_crystal_hp_percent')
        self._group_left_die_count = extra_data.get('group_left_die_count')
        self._atk_group_id = extra_data.get('atk_group_id')
        self._def_group_id = extra_data.get('def_group_id')
        self._old_atk_group_id = extra_data.get('old_atk_group_id')
        self._old_def_group_id = extra_data.get('old_def_group_id')
        self._crystal_round = extra_data.get('cur_round')
        self._group_crystal_player_cnt = extra_data.get('group_crystal_player_cnt', {})
        global_data.emgr.crystal_round_settle_timestamp_event.emit(self._round_settle_timestamp)
        self.try_show_crystal_locate_ui(extra_data.get('crystal_position'))
        global_data.emgr.do_update_crystal_hp.emit(self._def_group_id, self.get_def_crystal_hp_percent())
        global_data.emgr.update_group_left_die_count_event.emit(self._atk_group_id, self.get_atk_left_die_count())
        global_data.emgr.player_around_crystal_change_event.emit(self._def_group_id, self._group_crystal_player_cnt.get(self._def_group_id, 0))
        global_data.emgr.show_last_round_info_event.emit()

    @rpc_method(CLIENT_STUB, (Dict('group_crystal_hp_percent'), Dict('add_buff_ret')))
    def update_group_crystal_hp_percent(self, group_crystal_hp_percent, add_buff_ret):
        for group_id, percent in six.iteritems(group_crystal_hp_percent):
            self._group_crystal_hp_percent[group_id] = percent
            global_data.emgr.do_update_crystal_hp.emit(group_id, percent)

        if add_buff_ret:
            self.check_show_low_crystal_hp_tip(add_buff_ret)

    @rpc_method(CLIENT_STUB, (Bool('enable_out_base_rogue'),))
    def clear_rogue(self, enable_out_base_rogue):
        from collections import defaultdict
        battle_data = global_data.death_battle_data
        battle_data.rogue_gift_candidates = {}
        battle_data.selected_rogue_gifts = defaultdict(dict)
        battle_data.enable_out_base_rogue = enable_out_base_rogue
        battle_data.rogue_refresh_times = defaultdict(int)
        global_data.ui_mgr.close_ui('DeathRogueChooseUI')
        ui = global_data.ui_mgr.get_ui('ADCrystalRogueChooseBtnUI')
        if ui:
            ui.hide()
            ui._first_in_base = True

    @rpc_method(CLIENT_STUB, (Dict('group_left_die_count'),))
    def update_group_left_die_count(self, group_left_die_count):
        for group_id in six.iterkeys(group_left_die_count):
            old_cnt = self._group_left_die_count.get(group_id, 0)
            new_cnt = group_left_die_count[group_id]
            self._group_left_die_count[group_id] = new_cnt
            global_data.emgr.update_group_left_die_count_event.emit(group_id, self._group_left_die_count[group_id])
            if group_id == self._atk_group_id:
                self.check_show_low_die_cnt_tip(old_cnt, new_cnt)

    @rpc_method(CLIENT_STUB, (Int('group_id'), Int('player_cnt')))
    def update_player_cnt_around_crystal(self, group_id, player_cnt):
        global_data.emgr.player_around_crystal_change_event.emit(group_id, player_cnt)

    @rpc_method(CLIENT_STUB, (Dict('round_interval_data'),))
    def crystal_round_interval(self, round_interval_data):
        self._atk_group_id = round_interval_data.get('atk_group_id')
        self._def_group_id = round_interval_data.get('def_group_id')
        self._group_crystal_hp_percent = round_interval_data.get('group_crystal_hp_percent')
        self._group_crystal_points_dict = round_interval_data.get('group_crystal_points_dict')
        self._group_left_time_dict = round_interval_data.get('group_left_time_dict', {})
        self._crystal_round = round_interval_data.get('cur_round')
        self._round_prepare_timestamp = round_interval_data.get('round_prepare_timestamp')
        self._round_status = round_interval_data.get('round_status')
        self.enter_interval_view()
        global_data.ui_mgr.close_ui('ADCrystalLocateUI')
        global_data.ui_mgr.close_ui('DeathChooseWeaponUI')
        global_data.ui_mgr.close_ui('MechaSummonUI')
        global_data.ui_mgr.close_ui('MechaSummonAndChooseSkinUI')
        if global_data.ui_mgr.get_ui('StateChangeUI'):
            global_data.ui_mgr.close_ui('StateChangeUI')

    @rpc_method(CLIENT_STUB, (Dict('round_end_data'),))
    def crystal_round_begin(self, round_begin_data):
        self._round_settle_timestamp = round_begin_data.get('round_settle_timestamp')
        self._crystal_round = round_begin_data.get('cur_round')
        self._round_status = round_begin_data.get('round_status')
        global_data.emgr.crystal_round_settle_timestamp_event.emit(self._round_settle_timestamp)
        self.show_round_begin_tip()
        global_data.emgr.show_last_round_info_event.emit()
        global_data.ui_mgr.close_ui('ADCrystalTransitionUI')

    @rpc_method(CLIENT_STUB, (Dict('stage_data'),))
    def crystal_stage_change(self, stage_data):
        crystal_position = stage_data.get('crystal_position')
        self.try_show_crystal_locate_ui(crystal_position)
        self.show_second_stage_tip()

    @rpc_method(CLIENT_STUB, (Float('round_end_data'),))
    def update_round_settle_timestamp(self, settle_timestamp):
        self._round_settle_timestamp = settle_timestamp
        global_data.emgr.crystal_round_settle_timestamp_event.emit(self._round_settle_timestamp)

    @rpc_method(CLIENT_STUB, (Dict('group_crystal_damage_dict'),))
    def update_group_crystal_points(self, group_crystal_damage_dict):
        pass

    @rpc_method(CLIENT_STUB, ())
    def start_set_out_all_soul(self):
        self.do_set_out_all_soul()

    @rpc_method(CLIENT_STUB, (Float('settle_timestamp'),))
    def update_settle_timestamp(self, settle_timestamp):
        self.settle_timestamp = settle_timestamp
        global_data.death_battle_data.set_settle_timestamp(settle_timestamp)
        global_data.emgr.crystal_round_settle_timestamp_event.emit(self._round_settle_timestamp)

    @rpc_method(CLIENT_STUB, (Dict('clean_up_data'),))
    def start_clean_up_all_soul(self, clean_up_data):
        from logic.comsys.battle.ADCrystal.ADCrystalTransitionUI import ADCrystalTransitionUI
        ADCrystalTransitionUI()
        crystal_position = clean_up_data.get('crystal_position')
        self.try_show_crystal_locate_ui(crystal_position)
        self.exit_interval_view()

    @rpc_method(CLIENT_STUB, ())
    def crystal_hit_hint(self):
        global_data.emgr.show_crystal_hit_hint_event.emit()

    @rpc_method(CLIENT_STUB, (Int('crystal_group_id'),))
    def crystal_destroy_hint(self, crystal_group_id):
        self.show_crystal_destroy_tip()

    @rpc_method(CLIENT_STUB, (Int('crystal_group_id'), Int('crystal_round')))
    def crystal_die_hint(self, crystal_group_id, crystal_round):
        pass

    def get_round_left_time(self):
        return int(math.ceil(self._round_settle_timestamp - t_util.time()))

    def check_show_low_die_cnt_tip(self, old_cnt, new_cnt):
        if self._round_status == bconst.ROUND_STATUS_INTERVAL:
            return
        for low_cnt, power_up in self._low_die_cnt_buff:
            if new_cnt < low_cnt <= old_cnt:
                power_up_str = '{}%'.format(int(power_up * 100))
                if self._my_group_id == self._atk_group_id:
                    tip_type = bconst.ADCRYSTAL_TIP_LOW_DIE_CNT_BUFF_ATK
                    text = get_text_by_id(17500).format(power_up_str)
                else:
                    text = get_text_by_id(17501).format(power_up_str)
                    tip_type = bconst.ADCRYSTAL_TIP_LOW_DIE_CNT_BUFF_DEF
                set_attr_dict = {'node_name': 'lab_tips','func_name': 'SetString',
                   'args': (
                          get_text_by_id(17499).format(low_cnt),)
                   }
                message = {'i_type': tip_type,'content_txt': text,'set_attr_dict': set_attr_dict}
                global_data.emgr.show_battle_main_message.emit(message, bconst.MAIN_NODE_COMMON_INFO)
                break

    def check_show_low_crystal_hp_tip(self, add_buff_ret):
        if self._round_status == bconst.ROUND_STATUS_INTERVAL:
            return
        low_hp = add_buff_ret.get('low_hp', 0)
        low_hp_str = '{}%'.format(int(low_hp * 100))
        power_up = add_buff_ret.get('fight_factor', 0)
        atk_group_id = self._atk_group_id
        power_up_str = '{}%'.format(int(power_up * 100))
        if self._my_group_id == atk_group_id:
            tip_type = bconst.ADCRYSTAL_TIP_LOW_HP_BUFF_ATK
            tip_text = get_text_by_id(17501).format(power_up_str)
        else:
            tip_type = bconst.ADCRYSTAL_TIP_LOW_HP_BUFF_DEF
            tip_text = get_text_by_id(17500).format(power_up_str)
        set_attr_dict = {'node_name': 'lab_tips',
           'func_name': 'SetString',
           'args': (
                  get_text_by_id(17498).format(low_hp_str),)
           }
        message = {'i_type': tip_type,'content_txt': tip_text,'set_attr_dict': set_attr_dict}
        message_type = bconst.MAIN_NODE_COMMON_INFO
        global_data.emgr.show_battle_main_message.emit(message, message_type)

    def show_round_begin_tip(self):
        if self._crystal_round is None:
            return
        else:
            round_no = self._crystal_round + 1
            if self._my_group_id == self._atk_group_id:
                tip_type = bconst.ADCRYSTAL_TIP_ATK_START
                text = get_text_by_id(17471).format(round_no)
            else:
                text = get_text_by_id(17470).format(round_no)
                tip_type = bconst.ADCRYSTAL_TIP_DEF_START
            message = {'i_type': tip_type,'content_txt': text,'in_anim': 'break','out_anim': 'break_out'}
            global_data.emgr.show_battle_med_message.emit((message,), bconst.MED_NODE_RECRUIT_COMMON_INFO)
            return

    def show_crystal_destroy_tip(self):
        if self._my_group_id == self._atk_group_id:
            tip_type = bconst.ADCRYSTAL_TIP_PRE_CRYSTAL_DESTROY_ATK
            text = get_text_by_id(17481)
        else:
            text = get_text_by_id(17480)
            tip_type = bconst.ADCRYSTAL_TIP_PRE_CRYSTAL_DESTROY_DEF
        message = {'i_type': tip_type,'content_txt': text}
        global_data.emgr.show_battle_main_message.emit(message, bconst.MAIN_NODE_COMMON_INFO)

    def try_show_crystal_locate_ui(self, position):
        global_data.ui_mgr.close_ui('ADCrystalLocateUI')
        if not isinstance(position, (tuple, list)):
            return
        from logic.gutils.judge_utils import get_player_group_id
        if get_player_group_id() == self._atk_group_id:
            mark_type = bconst.CRYSTAL_BATTLE_CRYSTAL_MARK_RED
        else:
            mark_type = bconst.CRYSTAL_BATTLE_CRYSTAL_MARK_BLUE
        ui = global_data.ui_mgr.show_ui('ADCrystalLocateUI', 'logic.comsys.battle.ADCrystal')
        ui and ui.add_locate_widget(mark_type, position)
        ui and global_data.emgr.do_update_crystal_hp.emit(self._def_group_id, self.get_def_crystal_hp_percent())

    def show_second_stage_tip(self):
        from logic.gutils.judge_utils import get_player_group_id
        if get_player_group_id() == self._def_group_id:
            tip_type_1 = bconst.ADCRYSTAL_TIP_SEC_STAGE_DEF
            tip_type_2 = bconst.ADCRYSTAL_TIP_POS_CHANGE_DEF
        else:
            tip_type_1 = bconst.ADCRYSTAL_TIP_SEC_STAGE_ATK
            tip_type_2 = bconst.ADCRYSTAL_TIP_POS_CHANGE_ATK
        tip_text_1 = get_text_by_id(17478)
        tip_text_2 = get_text_by_id(17479)
        message = [{'i_type': tip_type_1,'content_txt': tip_text_1}, {'i_type': tip_type_2,'content_txt': tip_text_2}]
        message_type = [
         bconst.MAIN_NODE_COMMON_INFO, bconst.MAIN_NODE_COMMON_INFO]
        global_data.emgr.show_battle_main_message.emit(message, message_type, False, True)

    def show_interval_count_down(self):
        if self._round_status != bconst.ROUND_STATUS_INTERVAL:
            return
        else:
            ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')
            revive_time = self._round_prepare_timestamp - t_util.time()
            ui.on_delay_close(revive_time, None)
            return

    def update_low_die_cnt_buff_show(self, old_cnt, new_cnt):
        for idx, buff_data in enumerate(self._low_die_cnt_buff):
            low_cnt, power_up = buff_data
            if idx == len(self._low_die_cnt_buff) - 1:
                break
            if new_cnt < low_cnt <= old_cnt:
                show_val = self.get_low_die_cnt_power_up(new_cnt)
                show_val and global_data.emgr.battle_update_buff_show_val.emit(self._low_die_cnt_buff_id, {'fight_factor': show_val})
            elif old_cnt < low_cnt <= new_cnt:
                show_val = self.get_low_die_cnt_power_up(new_cnt)
                show_val and global_data.emgr.battle_update_buff_show_val.emit(self._low_die_cnt_buff_id, {'fight_factor': show_val})

    def get_low_die_cnt_power_up(self, left_cnt):
        for low_cnt, power_up in self._low_die_cnt_buff:
            if left_cnt < low_cnt:
                return power_up

        return 0

    def on_receive_report_dict(self, report_dict):
        cam_lplayer = global_data.cam_lplayer
        if not cam_lplayer:
            return
        killer_id, injured_id, _ = battle_utils.parse_battle_report_death(report_dict)
        if killer_id and cam_lplayer.id == killer_id:
            from logic.gutils.judge_utils import get_player_group_id
            set_attr_dict = {'node_name': 'lab_operator','func_name': 'SetString'
               }
            if get_player_group_id() == self._atk_group_id:
                text = get_text_by_id(17506)
                show_num = 1
                set_attr_dict['args'] = ('+', )
            else:
                text = get_text_by_id(17508)
                show_num = 2
                set_attr_dict['args'] = ('-', )
            msg = {'i_type': bconst.MAIN_KOTH_KILL_POINT,'icon_path': 'gui/ui_res_2/battle/notice/icon_msg_kill.png',
               'content_txt': text,
               'show_num': show_num,
               'set_attr_dict': set_attr_dict
               }
            cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, bconst.MAIN_NODE_POINT)
        mecha_killer_id, mecha_injured_id = battle_utils.parse_battle_report_mecha_death(report_dict)
        if mecha_killer_id and cam_lplayer.id == mecha_killer_id:
            from logic.gutils.judge_utils import get_player_group_id
            set_attr_dict = {'node_name': 'lab_operator','func_name': 'SetString'
               }
            if get_player_group_id() == self._atk_group_id:
                text = get_text_by_id(17505)
                show_num = 1
                set_attr_dict['args'] = ('+', )
            else:
                text = get_text_by_id(17507)
                show_num = 2
                set_attr_dict['args'] = ('-', )
            msg = {'i_type': bconst.MAIN_KOTH_KILL_MECHA_POINT,'content_txt': text,
               'show_num': show_num,
               'set_attr_dict': set_attr_dict
               }
            cam_lplayer.send_event('E_SHOW_MAIN_BATTLE_MESSAGE', msg, bconst.MAIN_NODE_POINT)

    def on_update_group_points(self, old_group_points_dict, group_points_dict):
        pass

    def enter_interval_view(self):
        if global_data.mecha and global_data.mecha.logic:
            global_data.mecha.logic.send_event('E_PLAY_VICTORY_CAMERA')
        if global_data.player and global_data.player.logic:
            global_data.player.logic.send_event('E_PLAY_VICTORY_CAMERA')
        global_data.ui_mgr.hide_all_ui_by_key('adcrystalbattle', INTERVAL_HIDE_UI_LIST)

    def exit_interval_view(self):
        if global_data.cam_lplayer:
            global_data.cam_lplayer.send_event('E_EXIT_FOCUS_CAMERA')
            if global_data.mecha and global_data.mecha.logic:
                global_data.mecha.logic.send_event('E_EXIT_FOCUS_CAMERA')
        global_data.ui_mgr.revert_hide_all_ui_by_key_action('adcrystalbattle', INTERVAL_HIDE_UI_LIST)

    def delay_close_transitionui(self):
        self._close_transition_timer = global_data.game_mgr.register_logic_timer(lambda : global_data.ui_mgr.close_ui('ADCrystalTransitionUI'), interval=4, times=1)

    def stop_close_transitionui_timer(self):
        if self._close_transition_timer:
            global_data.game_mgr.unregister_logic_timer(self._close_transition_timer)
            self._close_transition_timer = None
        return

    def do_set_out_all_soul(self):
        global_data.emgr.force_check_player_forward_event.emit()
        global_data.cam_lplayer and global_data.cam_lplayer.send_event('E_TO_THIRD_PERSON_CAMERA')
        self.show_interval_count_down()
        self.clear_limit_height_tip()

    @rpc_method(CLIENT_STUB, (Float('suicide_timestamp'),))
    def start_suicide_result(self, suicide_timestamp):
        self.suicide_timestamp = suicide_timestamp
        global_data.emgr.update_death_come_home_time.emit()

    def clear_limit_height_tip(self):
        try:
            BattlePrepare = global_data.game_mgr.scene.get_com('PartCompetitionBattlePrepare')
            if not (BattlePrepare and BattlePrepare.battle_prepare):
                return
            if not hasattr(BattlePrepare.battle_prepare, 'range_mgr'):
                return
            range_mgr = BattlePrepare.battle_prepare.range_mgr
            if not range_mgr:
                return
            range_mgr.clear_timer()
        except:
            pass

    def get_group_crystal_hp_percent(self, group_id):
        return self._group_crystal_hp_percent.get(group_id)

    def get_def_crystal_hp_percent(self):
        return self._group_crystal_hp_percent.get(self._def_group_id, 1.0)

    def get_atk_left_die_count(self):
        return self._group_left_die_count.get(self._atk_group_id, 50)

    def get_atk_group_id(self):
        return self._atk_group_id

    def get_def_group_id(self):
        return self._def_group_id

    def get_old_atk_group_id(self):
        return self._old_atk_group_id

    def get_old_def_group_id(self):
        return self._old_def_group_id

    def get_group_left_time(self, group_id):
        return self._group_left_time_dict.get(group_id, 0)

    def get_group_left_time_dict(self):
        return self._group_left_time_dict

    def get_group_crystal_points(self, group_id):
        return self._group_crystal_points_dict.get(group_id, 0)

    def get_prepare_left_time(self):
        return self._round_prepare_timestamp

    def get_crystal_round(self):
        return self._crystal_round

    def get_round_status(self):
        return self._round_status

    def get_last_showed_crystal_hp(self):
        return self._last_showed_crystal_hp

    def set_last_showed_crystal_hp(self, low_hp):
        self._last_showed_crystal_hp = low_hp