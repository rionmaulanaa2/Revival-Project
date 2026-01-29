# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/ConcertBattle.py
from __future__ import absolute_import
from __future__ import print_function
import six
from logic.entities.Battle import Battle
from logic.gcommon.common_utils import parachute_utils
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Uuid, List, Str, Dict, Int, Float, Bool, Tuple
from mobile.common.EntityManager import EntityManager
from logic.gutils.EntityPool import EntityPool
from mobile.common.IdManager import IdManager
from logic.gcommon.common_const import battle_const
from mobile.common.EntityFactory import EntityFactory
from common.utils import timer
import math3d
from ext_package.ext_decorator import ext_get_nb_mecha_info, ext_get_nb_role_info

class ConcertBattle(Battle):
    ui_to_hide = ('BattleInfoPlayerNumber', )

    def init_from_dict(self, bdict):
        super(ConcertBattle, self).init_from_dict(bdict)
        self.area_id = '1'
        self._king = None
        self._defier = None
        self._duel_queue = []
        self._mvp_entity_id = []
        self.best_role_skin_show = None
        self._max_duel_queue_cnt = global_data.game_mode.get_cfg_data('play_data').get('max_duel_queue_cnt', 2)
        self._king_info = [0, 0, 0]
        self.concert_stage = -1
        self.duel_stage = -1
        self.is_duel_waiting = False
        self.show_outline_player_id = None
        self.concert_start_ts = 0
        self.concert_idx = 1
        self.concert_end_ts = 0
        self.song_idx = -1
        self.song_end_ts = 0
        self.random_weapon = None
        self.duel_start_time = 0
        self.duel_end_time = 0
        self.last_king = None
        self.duel_waiting_timer = None
        self.question_round = -1
        self.question_ids = []
        self.question_end_ts = 0
        self._exit_timestamp = bdict.get('exit_timestamp', 0)
        self._top_nb_role_info = bdict.get('top_nb_role_info', [])
        self._top_nb_mecha_info = bdict.get('top_nb_mecha_info', [])
        self._next_island_refresh_ts = bdict.get('next_island_refresh_ts', 0)
        return

    @rpc_method(CLIENT_STUB, (Int('concert_stage'), Dict('concert_data')))
    def update_battle_data(self, concert_stage, concert_data):
        change_stage = concert_stage != self.concert_stage
        self.concert_stage = concert_stage
        self.concert_start_ts = concert_data.get('concert_start_ts', 0)
        self.concert_idx = concert_data.get('concert_idx', 0)
        self.concert_end_ts = concert_data.get('concert_end_ts', 0)
        duel_info = concert_data.get('duel_data', {}).get('duel_info', {})
        duel_stage = concert_data.get('duel_data', {}).get('duel_stage', -1)
        change_stage = change_stage or self.duel_stage != duel_stage
        self.duel_stage = duel_stage
        self.random_weapon = duel_info.get('random_weapon')
        self.duel_start_time = duel_info.get('duel_start_time', 0)
        self.duel_end_time = duel_info.get('duel_end_time', 0)
        self.check_best_skin_show()
        self._king = duel_info.get('king', None)
        self._king_info = duel_info.get('king_info', [0, 0, 0])
        self._defier = duel_info.get('defier', None)
        self._duel_queue = duel_info.get('duel_queue', [])
        self.refresh_mvp_tv()
        global_data.emgr.update_battle_data.emit()
        cur_time = global_data.game_time_server
        if cur_time >= self.concert_start_ts:
            if not (self.is_king_or_defier_player() and self.duel_stage == battle_const.CONCERT_FIGHT_STAGE):
                global_data.sound_mgr.set_sfx_volume_scale(0.5)
            else:
                global_data.sound_mgr.set_sfx_volume_scale(1.0)
        if self.is_duel_stage():
            from logic.gcommon.const import REGION_TAG_CHINA
            region_id = global_data.channel.get_region_id()
            if region_id != REGION_TAG_CHINA and cur_time < self.concert_start_ts:
                global_data.sound_mgr.play_music('M02_hall_Final')
            if change_stage:
                global_data.emgr.camera_cancel_all_trk.emit()
                if self.duel_stage == battle_const.CONCERT_FIGHT_STAGE:
                    self.start_duel()
        if self.is_sing_stage():
            global_data.sound_mgr.delay_stop_music()
            self.song_idx = concert_data.get('song_idx')
            self.song_end_ts = concert_data.get('song_end_ts')
            global_data.emgr.change_concert_song_data_event.emit(self.concert_stage, self.song_idx, self.song_end_ts)
        elif concert_stage == battle_const.CONCERT_STOP_SING_PRE_SETTLE:
            from logic.comsys.concert.KizunaLiveEndUI import KizunaLiveEndUI
            KizunaLiveEndUI()
        global_data.emgr.update_concert_data_info_event.emit()
        if change_stage:
            global_data.emgr.update_battle_stage.emit()
        return

    def get_battle_stage(self):
        return self.concert_stage

    def is_duel_stage(self):
        return self.duel_stage in [battle_const.CONCERT_WAIT_STAGE, battle_const.CONCERT_CONFIRM_STAGE, battle_const.CONCERT_FIGHT_STAGE]

    def is_sing_stage(self):
        return battle_const.CONCERT_WAIT_STAGE < self.concert_stage < battle_const.CONCERT_STOP_SING_PRE_SETTLE

    def is_wait_duel_stage(self):
        return self.duel_stage in [battle_const.CONCERT_WAIT_STAGE, battle_const.CONCERT_CONFIRM_STAGE]

    def get_battle_data(self):
        return (
         self._king, self._defier, self._duel_queue, self._king_info)

    def stop_self_fire_and_movement(self):
        from logic.comsys.battle.BattleUtils import stop_self_fire_and_movement
        stop_self_fire_and_movement()

    def is_in_queue(self):
        if not global_data.player:
            return False
        player_id = global_data.player.id
        if not player_id:
            return False
        if player_id in (self._king, self._defier) or player_id in self._duel_queue:
            return True
        return False

    def is_duel_player(self, id):
        return id is not None and id in (self._king, self._defier)

    def get_other_duel_player(self):
        if not global_data.player:
            return
        player_id = global_data.player.id
        if not player_id:
            return
        if player_id in (self._king, self._defier):
            if player_id == self._king:
                return self._defier
            return self._king

    def is_king(self):
        if not self._king:
            return False
        if not global_data.player:
            return False
        return global_data.player.id == self._king

    def is_defier(self):
        if not self._defier:
            return False
        if not global_data.player:
            return False
        return global_data.player.id == self._defier

    def is_wait_player(self):
        if not (self._king or self._defier):
            return True
        if not global_data.player:
            return False
        return global_data.player.id not in (self._king, self._defier)

    def is_king_or_defier_player(self):
        if not (self._king or self._defier):
            return False
        if not global_data.player:
            return False
        return global_data.player.id in (self._king, self._defier)

    def is_full_queue(self):
        return len(self._duel_queue) >= self._max_duel_queue_cnt

    def req_duel(self):
        if len(self._duel_queue) >= self._max_duel_queue_cnt:
            return
        self.call_soul_method('req_duel', ())

    def cancel_duel(self):
        self.call_soul_method('cancel_duel', ())

    @rpc_method(CLIENT_STUB, (Int('stop_time'),))
    def pre_stop_duel(self, stop_time):
        from logic.gcommon.common_const.battle_const import UP_NODE_CONCERT_ANCHOR
        global_data.emgr.battle_event_message.emit(get_text_by_id(609913), message_type=UP_NODE_CONCERT_ANCHOR)

    @rpc_method(CLIENT_STUB, (Float('timeout_ts'), Int('confirm_idx')))
    def on_confirm_duel(self, timeout_ts, confirm_idx):
        ui = global_data.ui_mgr.show_ui('ArenaConfirmUI', 'logic.comsys.concert')
        ui.set_timeout_ts(confirm_idx, timeout_ts)

    def confirm_duel(self, confirm_idx, is_confirm):
        self.call_soul_method('confirm_duel', (confirm_idx, is_confirm))

    def clear_outline(self):
        if self.show_outline_player_id:
            show_outline_player = EntityManager.getentity(self.show_outline_player_id)
            if show_outline_player and show_outline_player.logic:
                show_outline_player.logic.send_event('E_ENABLE_MODEL_OUTLINE_ONLY', False)
                self.show_outline_player_id = None
        return

    def get_show_outline_player_id(self):
        return self.show_outline_player_id

    def refresh_outline(self):
        if global_data.player:
            if not self.is_wait_player():
                self.clear_outline()
            return
        if global_data.player and global_data.player.id in (self._king, self._defier):
            self.clear_outline()
            show_outline_player_id, view_outline_player_id = (self._defier, self._king) if self.is_king() else (self._king, self._defier)
            if show_outline_player_id and global_data.player and global_data.player.id == view_outline_player_id:
                show_outline_player = EntityManager.getentity(show_outline_player_id)
                if show_outline_player and show_outline_player.logic:
                    show_outline_player.logic.send_event('E_ENABLE_MODEL_OUTLINE_ONLY', True)
                    self.show_outline_player_id = show_outline_player_id

    def start_duel(self):
        if global_data.player and global_data.player.id in (self._king, self._defier):
            self.stop_self_fire_and_movement()
            self.refresh_outline()
            import math
            from logic.gcommon import time_utility
            from logic.comsys.concert.ArenaRandomWeaponUI import UI_ANIM_TIME
            start_left_time = 0
            if self.duel_start_time:
                start_left_time = int(math.ceil(self.duel_start_time - time_utility.time()))
            need_time = UI_ANIM_TIME
            if start_left_time <= need_time:
                if start_left_time > 0:
                    ui = global_data.ui_mgr.show_ui('FFABeginCountDown', 'logic.comsys.battle.ffa')
                    ui.on_delay_close(start_left_time)
                global_data.ui_mgr.show_ui('ArenaTopUI', 'logic.comsys.concert')
            else:
                global_data.ui_mgr.show_ui('ArenaRandomWeaponUI', 'logic.comsys.concert')
            global_data.ui_mgr.close_ui('ArenaApplyUI')
            global_data.ui_mgr.close_ui('ArenaEndUI')
            global_data.ui_mgr.close_ui('KizunaConcertViewUI')
            if start_left_time > 0:
                self.is_duel_waiting = True

                def _end_waiting():
                    self.is_duel_waiting = False

                if self.duel_waiting_timer:
                    global_data.game_mgr.get_logic_timer().unregister(self.duel_waiting_timer)
                self.duel_waiting_timer = global_data.game_mgr.get_logic_timer().register(func=_end_waiting, mode=timer.CLOCK, interval=start_left_time, times=1)

    def get_duel_info(self):
        return (
         self.random_weapon, self.duel_start_time, self.duel_end_time)

    def can_move(self):
        return not self.is_duel_waiting

    def can_fire(self):
        return not self.is_duel_waiting

    def can_roll(self):
        return not self.is_duel_waiting

    def can_lens_aim(self):
        return not self.is_duel_waiting

    @rpc_method(CLIENT_STUB, (Uuid('winner'), Int('reward_cnt')))
    def on_duel_finish(self, winner, reward_cnt):
        self.stop_self_fire_and_movement()
        self.clear_outline()
        if not global_data.player:
            return
        player_id = global_data.player.id
        is_king = self.is_king()
        is_winner = player_id == winner
        ui = global_data.ui_mgr.show_ui('ArenaEndUI', 'logic.comsys.concert')
        ui.set_winner(winner, is_king, is_winner, reward_cnt)
        global_data.ui_mgr.close_ui('ArenaApplyUI')
        global_data.ui_mgr.close_ui('ArenaTopUI')
        global_data.ui_mgr.close_ui('ArenaRandomWeaponUI')
        global_data.ui_mgr.close_ui('FFABeginCountDown')

    def refresh_mvp_tv(self):
        if not self._king:
            return
        show_ani = False
        if self.last_king != self._king:
            self.last_king = self._king
            show_ani = True
        player = EntityManager.getentity(self._king)
        if player and player.logic:
            num, _, _ = self._king_info
            char_name = player.logic.ev_g_char_name()
            dressed_clothing_id = player.logic.ev_g_dressed_clothing_id()
            info = {'name': char_name,'dressed_clothing_id': dressed_clothing_id,'mvp': num,'show_ani': show_ani}
            if not self._mvp_entity_id:
                for tv_id in (30002, ):
                    entity_id = IdManager.genid()
                    entity_obj = EntityFactory.instance().create_entity('Television', entity_id)
                    info['show_ani'] = False
                    entity_obj.init_from_dict({'tv_id': tv_id,'is_client': True,'is_show': True,'show_info': info})
                    entity_obj.on_add_to_battle(self.id)
                    self._mvp_entity_id.append(entity_id)

            else:
                for entity_id in self._mvp_entity_id:
                    entity_obj = EntityManager.getentity(entity_id)
                    if entity_obj and entity_obj.logic:
                        entity_obj.logic.send_event('E_UPDATE_TV_INFO', {'is_show': True,'show_info': info})

    def clear_mvp_tv(self):
        for entity_id in self._mvp_entity_id:
            entity_obj = EntityManager.getentity(entity_id)
            if entity_obj:
                entity_obj.on_remove_from_battle()
                entity_obj.destroy()

    def init_top_nb_info(self, stage_dict):
        self._next_island_refresh_ts = stage_dict.get('next_island_refresh_ts', 0)
        self._top_nb_role_info = stage_dict.get('top_nb_role_info', [])
        self._top_nb_mecha_info = stage_dict.get('top_nb_mecha_info', [])

    @ext_get_nb_role_info
    def get_top_nb_role_info(self):
        return self._top_nb_role_info

    @ext_get_nb_mecha_info
    def get_top_nb_mecha_info(self):
        return self._top_nb_mecha_info

    def get_next_island_refresh_ts(self):
        return self._next_island_refresh_ts

    @rpc_method(CLIENT_STUB, (List('top_nb_mecha_info'), List('top_nb_role_info'), Float('next_refresh_time')))
    def on_island_nb_fasion_update(self, top_nb_mecha_info, top_nb_role_info, next_refresh_time):
        self._top_nb_mecha_info = top_nb_mecha_info
        self._top_nb_role_info = top_nb_role_info
        self._next_island_refresh_ts = next_refresh_time
        global_data.emgr.island_top_skin_change.emit()
        if self.best_role_skin_show:
            self.best_role_skin_show.refresh()

    def check_best_skin_show(self):
        from logic.vscene.parts.battleprepare.BestSkinShow import ConcertBestSkinShowWithModel, SKIN_TYPE_ROLE, ConcertBestSkinShow
        if global_data.enable_island_chushengtai:
            if not self.best_role_skin_show:
                self.best_role_skin_show = ConcertBestSkinShow(self, SKIN_TYPE_ROLE)
            else:
                self.best_role_skin_show.refresh()

    def clear_best_skin_show(self):
        if self.best_role_skin_show:
            self.best_role_skin_show.destroy()
            self.best_role_skin_show = None
        return

    def get_concert_start_ts(self):
        return self.concert_start_ts

    @rpc_method(CLIENT_STUB, (Int('song_idx'), Int('end_ts')))
    def start_sing_song(self, song_idx, end_ts):
        self.concert_stage = battle_const.CONCERT_SING_STAGE
        self.song_idx = song_idx
        self.song_end_ts = end_ts
        self.on_start_sing_song(self.concert_stage, self.song_idx, self.song_end_ts)

    def on_start_sing_song(self, concert_stage, song_idx, song_end_ts):
        global_data.emgr.change_concert_song_data_event.emit(concert_stage, song_idx, song_end_ts)

    @rpc_method(CLIENT_STUB, (Int('song_idx'),))
    def stop_sing_song(self, song_idx):
        self.concert_stage = battle_const.CONCERT_STOP_SING_STAGE
        global_data.emgr.change_concert_song_data_event.emit(self.concert_stage, self.song_idx, self.song_end_ts)

    def do_dance_call(self, song_idx, hit_idx):
        self.call_soul_method('do_dance_call', (song_idx, hit_idx))

    @rpc_method(CLIENT_STUB, (Int('song_idx'), Int('hit_rate'), Dict('reward_dict')))
    def offer_do_call_reward(self, song_idx, hit_rate, reward_dict):
        self.on_offer_do_call_reward(song_idx, hit_rate, reward_dict)

    def on_offer_do_call_reward(self, song_idx, hit_rate, reward_dict):
        global_data.emgr.concert_offer_do_call_reward.emit(song_idx, hit_rate, reward_dict)

    @rpc_method(CLIENT_STUB, (Int('song_idx'), Int('combo_cnt')))
    def concert_combo_call(self, song_idx, combo_cnt):
        pass

    def play_fireworks(self, item_id):
        self.call_soul_method('play_fireworks', (item_id,))

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Int('item_id')))
    def play_fireworks_succ(self, soul_id, item_id):
        pass

    def get_cur_song_start_ts(self):
        if self.song_idx is not None and self.song_idx != -1:
            sing_time_conf = global_data.game_mode.get_cfg_data('play_data').get('sing_time_conf', [])
            if self.song_idx < len(sing_time_conf):
                start_ts, song_len = sing_time_conf[self.song_idx]
                return self.song_end_ts - song_len
        return -1

    def load_finish(self):
        ui_mgr = global_data.ui_mgr
        for ui in self.ui_to_hide:
            ui_mgr.hide_ui(ui)

        super(ConcertBattle, self).load_finish()

    @rpc_method(CLIENT_STUB, (Int('round_idx'), List('question_idx'), Int('question_end_ts')))
    def on_question_start(self, round_idx, question_ids, question_end_ts):
        self.question_round = round_idx
        self.question_ids = question_ids
        self.question_end_ts = question_end_ts
        self.on_question_start_ui_imp()

    def on_question_start_ui_imp(self):
        from logic.gcommon.time_utility import get_server_time
        from logic.comsys.activity.Activity202201.AnnivesaryASMainUI import AnnivesaryASMainUI
        if self.question_round >= 0 and self.question_ids:
            ui = AnnivesaryASMainUI()
            ui.refresh_data(self.question_ids[0], self.question_end_ts)

    def answer_question(self, question_id, answer):
        self.call_soul_method('commit_answer', (self.question_round, question_id, answer))

    @rpc_method(CLIENT_STUB, (Int('round_idx'), List('reward_souls')))
    def question_lottery_ret(self, round_idx, reward_souls):
        self.question_lottery_ret_imp(round_idx, reward_souls)

    def question_lottery_ret_imp(self, round_idx, reward_souls):
        if global_data.player.id in reward_souls:
            live_answer_rewards = global_data.game_mode.get_cfg_data('play_data').get('live_answer_rewards', [])
            from logic.gutils import template_utils
            if live_answer_rewards and round_idx < len(live_answer_rewards):
                item_no, cnt = live_answer_rewards[round_idx]
                from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
                from logic.gutils.item_utils import get_lobby_item_name
                reward_str = get_lobby_item_name(item_no) + '*' + str(cnt)
                NormalConfirmUI2(content=get_text_by_id(610571, {'rewards': reward_str}))

    def destroy(self, clear_cache=True):
        super(ConcertBattle, self).destroy(clear_cache)
        if global_data.sound_mgr:
            global_data.sound_mgr.set_sfx_volume_scale(1.0)
        self.clear_mvp_tv()
        self.clear_best_skin_show()

    def get_concert_passed_time(self):
        from logic.gcommon import time_utility
        from logic.gutils.concert_utils import get_song_len, get_song_start_ts
        cur_time = time_utility.get_server_time()
        passed_time = cur_time - self.concert_start_ts
        if self.get_battle_stage() in [battle_const.CONCERT_SING_STAGE, battle_const.CONCERT_STOP_SING_STAGE]:
            song_end_ts = self.song_end_ts
            song_start_ts = self.get_cur_song_start_ts()
            song_passed_time = cur_time - song_start_ts
            song_idx = self.song_idx
            if song_end_ts > 0 and song_start_ts > 0 and song_passed_time > 0:
                passed_time = get_song_start_ts(song_idx) + song_passed_time
        return passed_time

    def move_to_born_pos(self):
        self.call_soul_method('move_to_born_pos')

    @rpc_method(CLIENT_STUB, (Str('lottery_id'), Dict('lottery_ret'), Dict('user_dict')))
    def notify_global_lottery_ret(self, lottery_id, lottery_ret, user_dict):
        print('test-qintao on_notify_global_lottery_reward', lottery_id, lottery_ret, user_dict)
        self.on_notify_global_lottery_ret(lottery_id, lottery_ret, user_dict)

    def test_notify_global_lottery_ret(self):
        from bson.objectid import ObjectId
        self.on_notify_global_lottery_ret('anniversary2_cn_1', {u'12301902': [],u'12301901': [500909]}, {500909: {'_id': ObjectId('6342886cfeaab2e1f6af73d2'),'uid': 500908,'char_name': 'ZeroPhantom'}})

    def on_notify_global_lottery_ret(self, lottery_id, lottery_ret, user_dict):
        from common.cfg import confmgr
        from logic.gutils.concert_utils import get_concert_region_lottery_id_list
        region_id = global_data.channel.get_region_id()
        concert_idx = global_data.battle.concert_idx
        region_lottery_id_list = get_concert_region_lottery_id_list()
        if lottery_id not in region_lottery_id_list:
            log_error('lottery_id not found', region_id, concert_idx, lottery_id)
            return None
        else:
            round_index = region_lottery_id_list.index(lottery_id)
            from logic.gcommon.cdata.global_lottery_config import get_global_lottery_conf
            lottery_conf = get_global_lottery_conf(lottery_id)
            lottery_rewards = lottery_conf.get('lottery_reward', [(None, 0)])
            first_reward_id = lottery_rewards[0][0]
            if global_data.player:
                for reward_id, rewarded_players in six.iteritems(lottery_ret):
                    if global_data.player.uid in rewarded_players:
                        self.on_concert_player_received_reward(global_data.player.uid, global_data.player.get_name(), round_index, [reward_id])

            for reward_id, rewarded_players in six.iteritems(lottery_ret):
                if str(first_reward_id) == reward_id:
                    for rplayer_uid in rewarded_players:
                        if global_data.player and global_data.player.uid == rplayer_uid:
                            continue
                        user_name = user_dict.get(rplayer_uid, {}).get('char_name', '')
                        self.on_concert_player_received_reward(rplayer_uid, user_name, round_index, [reward_id])

            return None

    def on_concert_player_received_reward(self, player_id, player_name, round, reward_souls):
        from common.cfg import confmgr
        from logic.gutils import item_utils
        reward_text = ''
        reward_text_list = []
        item_png = ''
        for reward_id in reward_souls:
            r_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            for item_info in r_list:
                item_no, item_count = item_info
                reward_text_list.append(item_utils.get_lobby_item_name(item_no))
                item_png = item_utils.get_lobby_item_pic_by_item_no(item_no)

        reward_text = ', '.join(reward_text_list)
        if global_data.player and player_id == global_data.player.uid:
            set_attr_dict = [
             {'node_name': 'icon_big','func_name': 'SetDisplayFrameByPath','args': (
                       '', item_png)
                }]
            text = get_text_by_id(633938).format(reward=reward_text)
            message = [{'i_type': battle_const.CONCERT_RECEIVED_REWARD,'content_txt': text,'set_attr_dict': set_attr_dict}]
            message_type = [battle_const.MAIN_NODE_COMMON_INFO]
            global_data.emgr.show_battle_main_message.emit(message, message_type, True, True)
        else:
            if round == 2:
                i_type = battle_const.CONCERT_PLAYER_FINAL_ROUND_REWARD
            else:
                i_type = battle_const.CONCERT_PLAYER_NORMAL_ROUND_REWARD
            text = get_text_by_id(633937).format(name=player_name, reward=reward_text)
            set_attr_dict = [
             {'node_name': 'icon_big','func_name': 'SetDisplayFrameByPath',
                'args': (
                       '', item_png)
                }]
            message = [{'i_type': i_type,'content_txt': text,'set_attr_dict': set_attr_dict}]
            message_type = [
             battle_const.MAIN_NODE_COMMON_INFO]
            global_data.emgr.show_battle_main_message.emit(message, message_type, True, True)