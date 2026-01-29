# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/audio/game_voice_mgr.py
from __future__ import absolute_import
import six
from common.framework import Singleton
import common.utils.timer as timer
from common.cfg import confmgr
from random import randint
from logic.gcommon.cdata import mecha_status_config
import time
import logic.gcommon.const as const
from mobile.common.EntityManager import EntityManager
import logic.gcommon.common_const.lang_data as lang
from logic.gcommon.common_const.voice_lang_data import voice_lang_data, VOICE_JA
import game3d
from common.utils.timer import CLOCK
_VOICE_TYPE_HUMAN = 'HumanVoice'
_VOICE_TYPE_MECHA = 'MechaVoice'
_VOICE_TYPE_TIPS = 'TipsVoice'
_VOICE_TYPE_ANCHOR = 'AnchorVoice'
VOICE_LEAVE_FIGHT = 0
VOICE_ENTER_FIGHT = 1
VOICE_LEAVE_FIGHT_DUL = 3000
VOICE_TICK_PEACE_TIMES = 20
VOICE_COUNT_PRE_PRO = 0.05
VOICE_HIT_DUL = 5

class GameVoiceMgr(Singleton):
    ALIAS_NAME = 'game_voice_mgr'

    def init(self):
        self._voice_enable = True
        self._delay_voice = {}
        self._next_play_time_dic = {}
        self._sp_next_play_time_dic = {}
        self._cur_voice_text_switch = None
        self.human_voice_trial_player_id = None
        self.uid_voice_player_id = None
        self.voide_item_id = None
        self.player = None
        self.mecha = None
        self.is_in_mecha = False
        self._game_voice_obj = global_data.sound_mgr.register_game_obj('virtual_anchor')
        self._loaded_bank_dic = {}
        self._role_voice_extern = {}
        self.vo_fight_state = VOICE_LEAVE_FIGHT
        self.atk_vo_dict = {}
        self.vo_fight_timer = None
        self.vo_peace_timer = None
        self.vo_time_count = 0
        self.hit_vo_dict = {}
        self.hit_vo_time = 0
        self._timer_id = global_data.game_mgr.register_logic_timer(self.timer_func, interval=0.1, times=-1, mode=timer.CLOCK)
        self.init_event()
        self.play_vo_tag = False
        return

    def on_finalize(self):
        if self.vo_fight_timer:
            game3d.cancel_delay_exec(self.vo_fight_timer)
            self.vo_fight_timer = None
        if self.vo_peace_timer:
            global_data.game_mgr.get_post_logic_timer().unregister(self.vo_peace_timer)
            self.vo_peace_timer = None
        return

    def timer_func(self):
        remove_triggers = set()
        for full_trigger_type, vo in six.iteritems(self._delay_voice):
            vo['delay_time'] -= 0.1
            if vo['delay_time'] <= 0:
                remove_triggers.add(full_trigger_type)
                self._start_play_voice(vo['voice_type'], vo['voice_data'], vo['entity_id'], vo['is_teamate'])

        for trigger in remove_triggers:
            self._delay_voice.pop(trigger)

    def clear(self):
        self.player_change(None)
        self.update_mecha()
        self.is_in_mecha = False
        self.player = None
        self.mecha = None
        self._delay_voice = {}
        self._next_play_time_dic = {}
        self._sp_next_play_time_dic = {}
        if self.vo_fight_timer:
            game3d.cancel_delay_exec(self.vo_fight_timer)
            self.vo_fight_timer = None
        if self.vo_peace_timer:
            global_data.game_mgr.get_post_logic_timer().unregister(self.vo_peace_timer)
            self.vo_peace_timer = None
        self.vo_time_count = 0
        self.atk_vo_dict = {}
        self.hit_vo_dict = {}
        self.hit_vo_time = 0
        return

    def init_event(self):
        emgr = global_data.emgr
        econf = {'switch_game_voice': self.switch_game_voice,
           'play_voice_by_uid': self.play_voice_by_uid,
           'play_human_voice_trial': self.play_human_voice_trial,
           'stop_human_voice_trial': self.stop_human_voice_trial,
           'play_game_voice': self.play_game_voice,
           'play_atk_voice': self.play_atk_voice,
           'play_hit_voice': self.play_hit_voice,
           'play_tips_voice': self.play_tips_voice,
           'play_anchor_voice': self.play_anchor_voice,
           'battle_group_voice': self.battle_group_voice,
           'net_login_reconnect_event': self.on_login_reconnect
           }
        emgr.bind_events(econf)

    def on_login_reconnect(self, *args):
        global_data.game_mgr.unregister_logic_timer(self._timer_id)
        self._timer_id = global_data.game_mgr.register_logic_timer(self.timer_func, interval=0.1, times=-1, mode=timer.CLOCK)
        if self.vo_peace_timer:
            global_data.game_mgr.get_post_logic_timer().unregister(self.vo_peace_timer)

    def switch_game_voice(self, is_open):
        self._voice_enable = is_open

    def init_battle_event(self):
        self.process_event(True)
        self.leave_fight_state()

    def exit_battle_event(self):
        self.process_event(False)
        self.clear()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_before_exit_event': self.exit_scene,
           'scene_player_setted_event': self.on_player_setted,
           'scene_observed_player_setted_event': self.on_enter_observe,
           'target_dead_event': self.on_camera_target_death,
           'target_defeated_event': self.on_camera_target_death
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_player_setted(self, lplayer):
        if global_data.game_mode and global_data.game_mode.is_pve():
            self._voice_enable = False
            return
        self._voice_enable = True
        self.player_change(lplayer)

    def on_enter_observe(self, lplayer):
        self._voice_enable = False

    def player_change(self, player):
        self.bind_player_event(self.player, is_bind=False)
        self.player = player
        if self.player:
            role_id = player.ev_g_role_id()
            voice_item_list = player.ev_g_role_voice()
            role_voice_cnf = confmgr.get('game_voice_conf', str(role_id), 'Content', default={})
            for item_no in voice_item_list:
                voice_item_cnf = role_voice_cnf.get(str(item_no))
                if voice_item_cnf is not None:
                    trigger_type = voice_item_cnf.get('trigger_type')
                    switch = voice_item_cnf.get('switch')
                    voice_type = voice_item_cnf.get('source')
                    if voice_type not in self._role_voice_extern:
                        self._role_voice_extern[voice_type] = {}
                    if trigger_type not in self._role_voice_extern[voice_type]:
                        self._role_voice_extern[voice_type][trigger_type] = []
                    self._role_voice_extern[voice_type][trigger_type].append(switch)

            self.bind_player_event(self.player, is_bind=True)
            self.update_mecha()
        else:
            self._role_voice_extern = {}
        return

    def bind_player_event(self, target, is_bind=True):
        if target and target.is_valid():
            if is_bind:
                ope_func = target.regist_event
            else:
                ope_func = target.unregist_event
            ope_func('E_ON_JOIN_MECHA', self.on_join_mecha)
            ope_func('E_ON_LEAVE_MECHA', self.on_leave_mecha)

    def update_mecha(self):
        self.bind_mecha_event(self.mecha, False)
        self.mecha = None
        if self.player and self.player.ev_g_in_mecha():
            control_target = self.player.ev_g_control_target()
            if control_target and control_target.logic:
                self.mecha = control_target.logic
                self.bind_mecha_event(self.mecha, True)
        return

    def bind_mecha_event(self, target, is_bind=True):
        if target and target.is_valid():
            if is_bind:
                ope_func = target.regist_event
            else:
                ope_func = target.unregist_event
            ope_func('E_ENTER_STATE', self.on_mecha_enter_state)
            ope_func('E_FIGHT_CAP_UPGRADE_SFX', self.on_mecha_level_up)
            ope_func('E_DEATH', self.on_mecha_die)

    def play_game_voice(self, trigger_type, mecha_id=None, teamate_id=None):
        if not self._voice_enable:
            return
        else:
            if not global_data.player or not global_data.player.logic or not self.player:
                return
            player = self.player
            is_teamate = False
            if teamate_id is not None:
                teamate_player = EntityManager.getentity(teamate_id)
                if teamate_player and teamate_player.logic:
                    player = teamate_player.logic
                    is_teamate = True
                else:
                    return
            role_id = player.ev_g_role_id()
            if mecha_id is None and player.ev_g_in_mecha():
                mecha_id = player.ev_g_get_bind_mecha_type()
            voice_type = None
            if mecha_id == None:
                voice_type = _VOICE_TYPE_HUMAN
                voice_cnf = confmgr.get('game_voice_conf', 'HumanVoice', 'Content', default={})
            else:
                voice_type = _VOICE_TYPE_MECHA
                voice_cnf = confmgr.get('game_voice_conf', 'MechaVoice', 'Content', default={})
            trigger_type = self.transfer_trigger(trigger_type, role_id, mecha_id)
            voice_data = None
            if mecha_id != None:
                full_trigger_type = '{0}_{1}_{2}'.format(role_id, mecha_id, trigger_type)
                voice_data = voice_cnf.get(full_trigger_type, None)
            if voice_data == None:
                full_trigger_type = '{0}_{1}'.format(role_id, trigger_type)
                voice_data = voice_cnf.get(full_trigger_type, None)
            self._parse_voice(voice_type, full_trigger_type, voice_data, teamate_id, is_teamate)
            return

    def play_atk_voice(self, trigger_type, wp_id):
        if not self._voice_enable or not global_data.player or not global_data.player.logic or not self.player:
            return
        else:
            self.reset_fight_state()
            result = self.check_atk_voice(wp_id)
            if not result:
                return
            player = self.player
            role_id = player.ev_g_role_id()
            mecha_id = None
            if player.ev_g_in_mecha():
                mecha_id = player.ev_g_get_bind_mecha_type()
            if mecha_id is None:
                voice_type = _VOICE_TYPE_HUMAN
                voice_cnf = confmgr.get('game_voice_conf', 'HumanVoice', 'Content', default={})
            else:
                voice_type = _VOICE_TYPE_MECHA
                voice_cnf = confmgr.get('game_voice_conf', 'MechaVoice', 'Content', default={})
            voice_data = None
            full_trigger_type = ''
            if mecha_id is not None:
                full_trigger_type = '{0}_{1}_{2}'.format(role_id, mecha_id, trigger_type)
                voice_data = voice_cnf.get(full_trigger_type, None)
            if voice_data is None:
                full_trigger_type = '{0}_{1}'.format(role_id, trigger_type)
                voice_data = voice_cnf.get(full_trigger_type, None)
            if voice_type in self._role_voice_extern and full_trigger_type in self._role_voice_extern[voice_type]:
                import copy
                voice_data = copy.deepcopy(voice_data)
                voice_data.setdefault('switch', [])
                voice_data['switch'].extend(self._role_voice_extern[voice_type][full_trigger_type])
            if voice_data is None:
                return
            voice_data = self._change_to_special_voice(voice_data, None, False)
            delay_time = voice_data.get('delay_time', 0)
            if delay_time != 0:
                self._delay_voice[full_trigger_type] = {'voice_type': voice_type,'delay_time': delay_time,'voice_data': voice_data,'entity_id': None,'is_teamate': False
                   }
            else:
                self._start_play_voice(voice_type, voice_data, None, False)
            return

    def play_hit_voice(self, trigger_type, wp_id, target):
        if not self._voice_enable:
            return
        else:
            if not global_data.player or not global_data.player.logic or not self.player:
                return
            self.reset_fight_state()
            result = self.check_hit_voice(wp_id, target)
            if not result:
                return
            player = self.player
            role_id = player.ev_g_role_id()
            if player.ev_g_in_mecha():
                mecha_id = player.ev_g_get_bind_mecha_type()
            else:
                mecha_id = None
            if mecha_id == None:
                voice_type = _VOICE_TYPE_HUMAN
                voice_cnf = confmgr.get('game_voice_conf', 'HumanVoice', 'Content', default={})
            else:
                voice_type = _VOICE_TYPE_MECHA
                voice_cnf = confmgr.get('game_voice_conf', 'MechaVoice', 'Content', default={})
            voice_data = None
            full_trigger_type = ''
            if mecha_id is not None:
                full_trigger_type = '{0}_{1}_{2}'.format(role_id, mecha_id, trigger_type)
                voice_data = voice_cnf.get(full_trigger_type, None)
            if voice_data is None:
                full_trigger_type = '{0}_{1}'.format(role_id, trigger_type)
                voice_data = voice_cnf.get(full_trigger_type, None)
            if voice_type in self._role_voice_extern:
                if full_trigger_type in self._role_voice_extern[voice_type]:
                    import copy
                    voice_data = copy.deepcopy(voice_data)
                    if 'switch' not in voice_data:
                        voice_data['switch'] = []
                    voice_data['switch'].extend(self._role_voice_extern[voice_type][full_trigger_type])
            voice_data = self._change_to_special_voice(voice_data, None, False)
            delay_time = voice_data.get('delay_time', 0)
            if delay_time != 0:
                self._delay_voice[full_trigger_type] = {'voice_type': voice_type,'delay_time': delay_time,'voice_data': voice_data,'entity_id': None,'is_teamate': False
                   }
            else:
                self._start_play_voice(voice_type, voice_data, None, False)
            return

    def enter_fight_state(self):
        if self.vo_peace_timer:
            global_data.game_mgr.get_post_logic_timer().unregister(self.vo_peace_timer)
            self.vo_peace_timer = None
        return

    def reset_fight_state(self):
        if self.vo_fight_state == VOICE_LEAVE_FIGHT:
            self.vo_fight_state = VOICE_ENTER_FIGHT
        self.enter_fight_state()
        if self.vo_fight_timer:
            game3d.cancel_delay_exec(self.vo_fight_timer)
        self.vo_fight_timer = game3d.delay_exec(VOICE_LEAVE_FIGHT_DUL, self.leave_fight_state)

    def leave_fight_state(self):
        self.vo_fight_timer = None
        if self.vo_fight_state == VOICE_ENTER_FIGHT:
            self.vo_fight_state = VOICE_LEAVE_FIGHT
        if self.vo_peace_timer:
            global_data.game_mgr.get_post_logic_timer().unregister(self.vo_peace_timer)
        self.vo_peace_timer = global_data.game_mgr.get_post_logic_timer().register(func=self.tick_vo_peace_count, interval=1, times=VOICE_TICK_PEACE_TIMES, mode=CLOCK)
        return

    def tick_vo_peace_count(self):
        self.vo_time_count += 1

    def play_tips_voice(self, trigger_type, **args):
        if not self._voice_enable:
            return
        else:
            if not global_data.player or not global_data.player.logic:
                return
            entity_id = args.get('entity_id')
            role_id = global_data.player.logic.ev_g_role_id()
            voice_cnf = confmgr.get('game_voice_conf', 'TipsVoice', 'Content', default={})
            full_trigger_type = '{0}_{1}'.format(role_id, trigger_type)
            voice_data = voice_cnf.get(full_trigger_type, None)
            self._parse_voice(_VOICE_TYPE_TIPS, full_trigger_type, voice_data, entity_id)
            return

    def play_anchor_voice(self, trigger_type):
        voice_cnf = confmgr.get('game_voice_conf', 'AnchorVoice', 'Content', default={})
        voice_data = voice_cnf.get(trigger_type, None)
        self._parse_voice(_VOICE_TYPE_ANCHOR, trigger_type, voice_data)
        return

    def play_human_voice_trial(self, role_id, item_id, success_callback, finish_callback=None):
        self.stop_human_voice_trial()
        human_voice_cnf = confmgr.get('game_voice_conf', str(role_id), 'Content', str(item_id))
        if human_voice_cnf is not None:
            switch = human_voice_cnf.get('switch')
            trigger_type = human_voice_cnf.get('trigger_type')
            source_type = human_voice_cnf.get('source')
            voice_data = confmgr.get('game_voice_conf', source_type, 'Content', str(trigger_type))
            event = voice_data.get('event')
            if isinstance(event, list):
                event = event[0]
            elif isinstance(event, str):
                pass
            self._init_voice_wwise(voice_data, switch)

            def end_callback(callback_type, infos, item_id=item_id):
                if self.voide_item_id == item_id:
                    self.human_voice_trial_player_id = None
                    if finish_callback:
                        finish_callback()
                return

            self.human_voice_trial_player_id = global_data.sound_mgr.post_event_2d(event, self._game_voice_obj, callback=end_callback)
            self.voide_item_id = item_id
            if self.human_voice_trial_player_id is not None and success_callback:
                success_callback()
        return

    def stop_human_voice_trial(self):
        if self.human_voice_trial_player_id is not None:
            global_data.sound_mgr.stop_playing_id(self.human_voice_trial_player_id)
            self.human_voice_trial_player_id = None
        return

    def play_voice_by_uid(self, source_type, trigger_type, cb=None):
        voice_cnf = confmgr.get('game_voice_conf', source_type, 'Content', trigger_type)
        if not voice_cnf:
            return False
        else:
            self.stop_voice_by_uid()
            event = voice_cnf.get('event')
            switch_list = voice_cnf.get('switch', None)
            if switch_list:
                switch = switch_list[randint(0, len(switch_list) - 1)]
                self._init_voice_wwise(voice_cnf, switch)
                if isinstance(event, list):
                    event = event[0]
                elif isinstance(event, str):
                    pass
            else:
                if event:
                    play_event = event[randint(0, len(event) - 1)]
                    self._init_voice_wwise(voice_cnf, None)
                    event = 'Play_{}'.format(play_event)

                def end_callback(callback_type, infos):
                    self.uid_voice_player_id = None
                    cb and cb()
                    return

                self.uid_voice_player_id = global_data.sound_mgr.post_event_2d(event, self._game_voice_obj, callback=end_callback)
                if self.uid_voice_player_id:
                    return True
            return False

    def stop_voice_by_uid(self):
        if self.uid_voice_player_id is not None:
            global_data.sound_mgr.stop_playing_id(self.uid_voice_player_id)
            self.uid_voice_player_id = None
        return

    def check_atk_voice(self, wp_id):
        wp_conf = confmgr.get('game_voice_conf', 'AttackVoice', 'Content', default={}).get(str(wp_id), None)
        if wp_conf is None:
            wp_conf = {'base_pro': 0.1,'atk_pro': 0.0,'min_dul': 15}
        base_pro = wp_conf.get('base_pro')
        if wp_id not in self.atk_vo_dict:
            self.atk_vo_dict[wp_id] = {'time': None,'count': 0,'ratio': 0}
        min_dul = wp_conf.get('min_dul')
        last_time = self.atk_vo_dict[wp_id].get('time', None)
        if last_time:
            if time.time() - last_time < min_dul:
                return False
        else:
            self.atk_vo_dict[wp_id]['time'] = time.time()
        atk_pre_pro = wp_conf.get('atk_pro')
        atk_count = self.atk_vo_dict[wp_id].get('count', None)
        if atk_count:
            self.atk_vo_dict[wp_id]['count'] += 1
        else:
            self.atk_vo_dict[wp_id]['count'] = 1
        atk_pro = atk_count * atk_pre_pro
        time_pre_pro = VOICE_COUNT_PRE_PRO
        time_pro = self.vo_time_count * time_pre_pro
        final_pro = base_pro + atk_pro + time_pro
        if self.atk_vo_dict[wp_id]['ratio'] == 0:
            self.atk_vo_dict[wp_id]['ratio'] = randint(1, 100)
        if final_pro * 100 >= self.atk_vo_dict[wp_id]['ratio']:
            self.atk_vo_dict[wp_id]['time'] = time.time()
            self.atk_vo_dict[wp_id]['count'] = 0
            self.vo_time_count = 0
            self.atk_vo_dict[wp_id]['ratio'] = 0
            return True
        else:
            return False
            return

    def check_hit_voice(self, wp_id, target):
        wp_conf = confmgr.get('game_voice_conf', 'HitVoice', 'Content', default={}).get(str(wp_id), None)
        if wp_conf is None:
            wp_conf = {'base_pro': 0.1}
        min_dul = VOICE_HIT_DUL
        if time.time() - self.hit_vo_time < min_dul:
            return False
        else:
            base_pro = wp_conf.get('base_pro')
            if wp_id not in self.hit_vo_dict:
                self.hit_vo_dict[wp_id] = {'ratio': 0}
            hp_ratio = 0
            hp_pro = 0
            if target and target.logic:
                ltarget = target.logic
                cur_hp = ltarget.ev_g_hp()
                max_hp = ltarget.ev_g_max_hp()
                hp_ratio = cur_hp * 1.0 / max_hp
                hp_pro = 3.6 * hp_ratio * (1 - hp_ratio)
            final_pro = base_pro + hp_pro
            if self.hit_vo_dict[wp_id]['ratio'] == 0:
                self.hit_vo_dict[wp_id]['ratio'] = randint(1, 100)
            if final_pro * 100 >= self.hit_vo_dict[wp_id]['ratio']:
                self.hit_vo_time = time.time()
                self.hit_vo_dict[wp_id]['ratio'] = 0
                return True
            return False
            return

    def _parse_voice(self, voice_type, full_trigger_type, voice_data, entity_id=None, is_teamate=False):
        if voice_data != None:
            probability = voice_data.get('probability', None)
            delay_time = voice_data.get('delay_time', 0)
            if randint(1, 100) <= probability or is_teamate:
                if not is_teamate:
                    if 'min_interval' in voice_data:
                        if full_trigger_type in self._next_play_time_dic:
                            if self._next_play_time_dic[full_trigger_type] > time.time():
                                return
                        self._next_play_time_dic[full_trigger_type] = time.time() + voice_data['min_interval']
                    sp_params = voice_data.get('sp_params', None)
                    if sp_params is not None:
                        same_src_interval = sp_params.get('same_src_interval', None)
                        if same_src_interval is not None and not self._check_same_src_interval(entity_id, full_trigger_type, same_src_interval):
                            return
                if voice_type in self._role_voice_extern:
                    if full_trigger_type in self._role_voice_extern[voice_type]:
                        import copy
                        voice_data = copy.deepcopy(voice_data)
                        if 'switch' not in voice_data:
                            voice_data['switch'] = []
                        voice_data['switch'].extend(self._role_voice_extern[voice_type][full_trigger_type])
                voice_data = self._change_to_special_voice(voice_data, entity_id, is_teamate)
                if delay_time != 0:
                    self._delay_voice[full_trigger_type] = {'voice_type': voice_type,'delay_time': delay_time,'voice_data': voice_data,'entity_id': entity_id,'is_teamate': is_teamate}
                else:
                    self._start_play_voice(voice_type, voice_data, entity_id, is_teamate)
        return

    def _change_to_special_voice(self, voice_data, entity_id, is_teammate):
        special_voice_id = voice_data.get('special')
        if not special_voice_id:
            return voice_data
        else:
            if isinstance(special_voice_id, int):
                special_voice_id = (
                 special_voice_id,)
            for voice_id in special_voice_id:
                special_voice_conf = confmgr.get('game_voice_conf', 'SpecialVoice', 'Content', str(voice_id))
                params = special_voice_conf.get('params')
                if not params:
                    continue
                func, kwargs = params['func'], params['kwargs']
                from logic.gutils import game_voice_utils
                if not hasattr(game_voice_utils, func):
                    continue
                if is_teammate:
                    player = EntityManager.getentity(entity_id) if 1 else global_data.player
                    func = getattr(game_voice_utils, func)
                    if func(player, **kwargs):
                        import copy
                        voice_data = copy.deepcopy(voice_data)
                        voice_data['switch'] = special_voice_conf.get('switch', None)
                        voice_data['text_only'] = special_voice_conf.get('text_only', False)
                        voice_data['bnk'] = special_voice_conf.get('bnk')
                        voice_data['event'] = special_voice_conf.get('event')
                        voice_data['switch_group'] = special_voice_conf.get('switch_group', None)
                        replace_photo_no = special_voice_conf.get('photo_no')
                        if replace_photo_no is not None:
                            voice_data['photo_no'] = replace_photo_no
                        return voice_data

            return voice_data

    def _start_play_voice(self, voice_type, voice_data, entity_id, is_teamate):
        if voice_type != _VOICE_TYPE_ANCHOR:
            if not global_data.player or not global_data.player.logic or not self.player:
                return
        if self.play_vo_tag:
            return
        else:
            sp_params = voice_data.get('sp_params', None)
            if sp_params is not None:
                distance = sp_params.get('distance', None)
                if not self._check_distance(entity_id, distance):
                    return
            priority = voice_data.get('priority', 0)
            event = voice_data.get('event')
            switch_list = voice_data.get('switch', None)
            if switch_list:
                switch = switch_list[randint(0, len(switch_list) - 1)]
                self._init_voice_wwise(voice_data, switch)
                cb_item = switch
                if isinstance(event, list):
                    event = event[0]
            elif event:
                play_event = event[randint(0, len(event) - 1)]
                self._init_voice_wwise(voice_data, None)
                cb_item = play_event
                event = 'Play_{}'.format(play_event)
            else:
                return

            def end_callback(callback_type, infos, voice_type=voice_type, switch=cb_item):
                if self._cur_voice_text_switch == switch or voice_type == _VOICE_TYPE_ANCHOR:
                    self._cur_voice_text_switch = None
                    global_data.game_mgr.next_exec(self._close_voice_text, voice_type, switch)
                self.play_vo_tag = False
                return

            text_only = voice_data.get('text_only', False)
            specific_photo_no = voice_data.get('photo_no')
            rtpc_value = 100 if self.is_in_mecha else 0
            global_data.sound_mgr.set_rtpc_ex('vo_on_mecha', rtpc_value)
            ret = global_data.sound_mgr.post_event_2d(event, self._game_voice_obj, callback=end_callback)
            show_text = text_only or ret
            if show_text:
                self._show_voice_text(voice_type, cb_item, entity_id, is_teamate, priority, specific_photo_no)
            if ret is not None:
                self.play_vo_tag = True
            return

    def _init_voice_wwise(self, voice_data, switch):
        bnk = voice_data.get('bnk', None)
        from logic.gcommon.common_utils.local_text import get_cur_voice_lang
        cur_voice_lang = get_cur_voice_lang()
        bnk_lang_list = confmgr.get('game_voice_conf', 'SpecialBnk', 'Content', bnk, 'lang_list', default=None)
        if bnk_lang_list and cur_voice_lang not in bnk_lang_list:
            cur_voice_lang = bnk_lang_list[0]
        bank_language = voice_lang_data.get(cur_voice_lang, {}).get('cVoiceDir', 'japanese')
        bnk = 'audio/{0}/{1}.bnk'.format(bank_language, bnk)
        if not global_data.player:
            return
        else:
            if bnk not in self._loaded_bank_dic:
                if not global_data.player.is_in_battle():
                    self.unload_bank()
                global_data.sound_mgr.load_bnk(bnk)
                self._loaded_bank_dic[bnk] = True
            if not switch:
                return
            switch_group = voice_data.get('switch_group', None)
            wwise_swtich = switch
            if wwise_swtich[:1].isdigit():
                wwise_swtich = 'a' + wwise_swtich
            global_data.sound_mgr.set_switch(switch_group, wwise_swtich, self._game_voice_obj)
            return

    def _show_voice_text(self, voice_type, switch, teamate_id=None, is_teamate=False, priority=0, photo_no=None):
        voice_cnf = confmgr.get('game_voice_conf', 'VoiceText', 'Content', default={})
        voice_text_id = voice_cnf.get(switch, {}).get('text_id', None)
        if voice_text_id is not None:
            from logic.gcommon.common_utils.local_text import get_text_by_id
            voice_text = get_text_by_id(voice_text_id)
            if voice_type == _VOICE_TYPE_ANCHOR:
                if global_data.battle and global_data.battle.is_settle:
                    return
                ui = global_data.ui_mgr.get_ui('AnchorVoiceTip')
                if not ui:
                    ui = global_data.ui_mgr.show_ui('AnchorVoiceTip', 'logic.comsys.prepare')
                if ui:
                    ui.start_voice_tip(voice_text, switch, priority)
            else:
                player = global_data.player
                if is_teamate:
                    teamate_player = EntityManager.getentity(teamate_id)
                    if teamate_player and teamate_player.logic:
                        player = teamate_player
                    else:
                        return
                if player and player.logic:
                    unit_id = player.id
                    unit_name = player.logic.ev_g_char_name()
                    msg = {'text': voice_text,
                       'head_frame': player.logic.ev_g_head_frame(),
                       'role_id': player.logic.ev_g_role_id()
                       }
                    if photo_no:
                        msg.update(photo_no=photo_no)
                    text_msg = {'msg': msg,'is_role_voice_msg': True}
                    global_data.emgr.add_battle_group_msg_event.emit(unit_id, unit_name, text_msg)
            self._cur_voice_text_switch = switch
        return

    def _close_voice_text(self, voice_type, switch):
        if voice_type == _VOICE_TYPE_ANCHOR:
            ui = global_data.ui_mgr.get_ui('AnchorVoiceTip')
            if ui:
                ui.stop_voice_tip(switch)
        else:
            global_data.emgr.battle_voice_tip_event.emit()

    def _check_distance(self, entity_id, distance):
        if distance is None or entity_id is None:
            return False
        else:
            battle = global_data.battle
            if not battle:
                return False
            entity = battle.get_entity(entity_id)
            if entity and entity.logic:
                player_pos = entity.logic.ev_g_cam_player_pos()
                if not player_pos:
                    return False
                unit_pos = entity.logic.ev_g_model_position()
                if not unit_pos:
                    return False
                vect = unit_pos - player_pos
                if vect.length_sqr < (distance * const.NEOX_UNIT_SCALE) ** 2:
                    return True
            return False

    def _check_same_src_interval(self, entity_id, full_trigger_type, interval):
        if entity_id is None:
            return True
        else:
            if entity_id not in self._sp_next_play_time_dic:
                self._sp_next_play_time_dic[entity_id] = {}
            entity_dic = self._sp_next_play_time_dic[entity_id]
            if full_trigger_type in entity_dic:
                if entity_dic[full_trigger_type] > time.time():
                    entity_dic[full_trigger_type] = time.time() + interval
                    return False
            entity_dic[full_trigger_type] = time.time() + interval
            return True

    def on_join_mecha(self, *args):
        if not self.is_in_mecha:
            self.is_in_mecha = True
            self.play_game_voice('summon')
            self.update_mecha()

    def on_leave_mecha(self):
        if self.is_in_mecha:
            self.is_in_mecha = False
            self.play_game_voice('leave', self.player.ev_g_get_bind_mecha_type())
            self.update_mecha()

    def on_camera_target_death(self, *args):
        self.play_anchor_voice('vo7')

    def on_mecha_enter_state(self, new_st):
        mecha_id = self.player.ev_g_get_bind_mecha_type() if self.player else None
        if new_st == mecha_status_config.MC_DASH and mecha_id and mecha_id not in (8007,
                                                                                   8013):
            self.play_game_voice('rush')
        return

    def on_mecha_level_up(self, *args):
        self.play_game_voice('upgrade')

    def on_mecha_die(self):
        self.play_game_voice('die')
        if self.is_in_mecha:
            self.is_in_mecha = False
            self.update_mecha()

    def exit_scene(self):
        self.clear()

    def battle_group_voice(self, teamate_id, voice_name):
        if not global_data.player or not global_data.player.logic:
            return
        else:
            if global_data.player.id == teamate_id:
                return
            from logic.client.const import game_mode_const
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
                self.play_game_voice(voice_name, None, teamate_id)
            return

    def unload_bank(self, unload_anchor=False):
        pop_bnk_list = []
        for bnk in self._loaded_bank_dic:
            if bnk.find('vo_anchor.bnk') == -1 or unload_anchor:
                global_data.sound_mgr.unload_bnk(bnk)
                pop_bnk_list.append(bnk)

        for pop_key in pop_bnk_list:
            self._loaded_bank_dic.pop(pop_key)

    def transfer_trigger(self, trigger_type, role_id, mecha_id):
        if trigger_type in ('hit', 'down', 'h_kill_mecha'):
            if role_id == 14 and mecha_id == 8004:
                from logic.gcommon.cdata import mecha_status_config
                mecha = self.player.ev_g_control_target().logic
                if mecha.ev_g_get_state(mecha_status_config.MC_HEAT):
                    trigger_type = 'rage_%s' % trigger_type
        return trigger_type