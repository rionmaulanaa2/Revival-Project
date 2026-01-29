# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/BattleSoundAiMgr.py
from __future__ import absolute_import
import six
from six.moves import range
import math3d
import world
import logic.gcommon.const as const
import render
import game3d
from logic.gcommon import time_utility
import logic.gcommon.common_const.scene_const as scene_const
import common.utilities
import math
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import poison_circle_const
from logic.gcommon.common_utils import battle_utils
import random
from common.cfg import confmgr
from logic.gcommon import time_utility as tutil
import common.utils.timer as timer
import time
import logic.gcommon.const as const
AI_INDEX_A = 0
AI_INDEX_B = 1
AI_COUNT = 2
CAMMAND_TYPE_DELAY = 0
CAMMAND_TYPE_FIRE = 1
PLAYER_TYPE_HUMAN = 1
PLAYER_TYPE_MECHA = 2

class DummyAiEntity(object):

    def __init__(self):
        self.id = None
        return

    def ev_g_camp_id(self):
        return None


class SoundAi(object):

    def __init__(self, random):
        self.sound_mgr = global_data.sound_mgr
        self.random = random
        self._timer = None
        self.sound_type = None
        self.pos = None
        self.cammand_list = []
        self.entity = DummyAiEntity()
        self.sound_id = self.sound_mgr.register_game_obj('battle_ai_sound')
        self.main_weapon_id = None
        self.sub_weapon_id = None
        self.main_weapon_sound_name = ''
        self.main_weapon_sound_nf = False
        self.sub_weapon_sound_name = ''
        self.sub_weapon_sound_nf = False
        self.main_weapon_auto_player_id = None
        self.cur_cammand_index = 0
        self.is_main_weapon_continue_sound = False
        return

    def set_sound_type(self, sound_type):
        self.sound_type = sound_type
        sound_type_data = confmgr.get('ai_data', 'Sound_Sim_Type', 'Content', str(sound_type))
        self.player_type = sound_type_data.get('PlayerType')
        self.main_weapon_id = sound_type_data.get('MainWeapon')
        self.main_weapon_sound_name = confmgr.get('firearm_config', str(self.main_weapon_id), 'cSoundName')
        self.is_main_weapon_continue_sound = confmgr.get('firearm_config', str(self.main_weapon_id), 'iIsContinueSound')
        self.sub_weapon_id = sound_type_data.get('SideWeapon')
        self.sub_weapon_sound_name = confmgr.get('firearm_config', str(self.sub_weapon_id), 'cSoundName')
        if isinstance(self.main_weapon_sound_name, list):
            if self.main_weapon_sound_name[1] == 'nf':
                self.main_weapon_sound_nf = True
        elif isinstance(self.main_weapon_sound_name, str):
            self.main_weapon_sound_nf = False
        if isinstance(self.sub_weapon_sound_name, list):
            if self.sub_weapon_sound_name[1] == 'nf':
                self.sub_weapon_sound_nf = True
        elif isinstance(self.sub_weapon_sound_name, str):
            self.sub_weapon_sound_nf = False

    def set_cammand_list(self, cammand_list):
        self.cammand_list = cammand_list
        self.cur_cammand_index = 0

    def run(self):
        self._start_time = time.time()
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
            self._timer = None
        self._timer = global_data.game_mgr.register_logic_timer(self.tick, 1, times=-1, mode=timer.LOGIC)
        return

    def tick(self):
        now = time.time()
        relative_time = now - self._start_time
        cur_cammand = self.cammand_list[self.cur_cammand_index]
        if relative_time > cur_cammand[0]:
            self.excule(cur_cammand)
            self.cur_cammand_index += 1
            if self.cur_cammand_index >= len(self.cammand_list):
                self.end()

    def excule(self, cammand):
        cammand_type = cammand[1]
        extra_data = cammand[2]
        if cammand_type == CAMMAND_TYPE_DELAY:
            if self.main_weapon_auto_player_id:
                sound_name = self.main_weapon_sound_name
                if not self.main_weapon_sound_nf:
                    self.sound_mgr.set_switch('gun', sound_name, self.sound_id)
                    self.sound_mgr.set_switch('gun_option', 'end', self.sound_id)
                    self.sound_mgr.post_event('Play_weapon_fire', self.sound_id, self.pos)
                elif len(sound_name) > 2 and sound_name[2] == 'ai_fix':
                    self.sound_mgr.set_switch('gun_tails', 'caliber_small', self.sound_id)
                    self.sound_mgr.post_event('{}_{}'.format(sound_name[0], 'start_3p'), self.sound_id, self.pos)
                else:
                    self.sound_mgr.post_event('{}_{}'.format(sound_name[0], '3p'), self.sound_id, self.pos)
                if len(sound_name) > 2 and sound_name[2] == 'ai_fix':
                    self.sound_mgr.post_event_non_optimization('{}_{}'.format(sound_name[0], 'stop_3p'), self.sound_id, self.pos)
                else:
                    self.sound_mgr.stop_playing_id(self.main_weapon_auto_player_id)
                self.main_weapon_auto_player_id = None
            return
        else:
            if cammand_type == CAMMAND_TYPE_FIRE:
                if self.player_type == PLAYER_TYPE_HUMAN:
                    sound_visible_type = const.SOUND_TYPE_FIRE
                else:
                    sound_visible_type = const.SOUND_TYPE_MECHA_FIRE
                global_data.emgr.sound_visible_add.emit(self.entity, self.pos, sound_visible_type, self.get_to_cam_target_length_sqr(self.pos))
                is_main_weapon = extra_data.get('is_main_weapon')
                if is_main_weapon and self.is_main_weapon_continue_sound:
                    if self.main_weapon_auto_player_id:
                        return
                    sound_name = self.main_weapon_sound_name
                    if not self.main_weapon_sound_nf:
                        self.sound_mgr.set_switch('gun', sound_name, self.sound_id)
                        self.sound_mgr.set_switch('gun_option', 'continuous', self.sound_id)
                        self.main_weapon_auto_player_id = self.sound_mgr.post_event('Play_weapon_fire', self.sound_id, self.pos)
                    elif len(sound_name) > 2 and sound_name[2] == 'ai_fix':
                        self.sound_mgr.set_switch('gun_tails', 'caliber_small', self.sound_id)
                        self.main_weapon_auto_player_id = self.sound_mgr.post_event('{}_{}'.format(sound_name[0], 'start_3p'), self.sound_id, self.pos)
                    else:
                        self.main_weapon_auto_player_id = self.sound_mgr.post_event('{}_{}'.format(sound_name[0], '3p'), self.sound_id, self.pos)
                elif is_main_weapon:
                    sound_name = self.main_weapon_sound_name
                    if not self.main_weapon_sound_nf:
                        self.sound_mgr.set_switch('gun', sound_name, self.sound_id)
                        self.sound_mgr.set_switch('gun_option', 'single', self.sound_id)
                        self.sound_mgr.post_event('Play_weapon_fire', self.sound_id, self.pos)
                    elif len(sound_name) > 2 and sound_name[2] == 'ai_fix':
                        self.sound_mgr.set_switch('gun_tails', 'caliber_small', self.sound_id)
                        self.sound_mgr.post_event('{}_{}'.format(sound_name[0], 'start_3p'), self.sound_id, self.pos)
                    else:
                        self.sound_mgr.post_event('{}_{}'.format(sound_name[0], '3p'), self.sound_id, self.pos)
                else:
                    sound_name = self.sub_weapon_sound_name
                    if not self.sub_weapon_sound_nf:
                        self.sound_mgr.set_switch('gun', sound_name, self.sound_id)
                        self.sound_mgr.set_switch('gun_option', 'single', self.sound_id)
                        self.sound_mgr.post_event('Play_weapon_fire', self.sound_id, self.pos)
                    elif len(sound_name) > 2 and sound_name[2] == 'ai_fix':
                        self.sound_mgr.set_switch('gun_tails', 'caliber_small', self.sound_id)
                        self.sound_mgr.post_event('{}_{}'.format(sound_name[0], 'start_3p'), self.sound_id, self.pos)
                    else:
                        self.sound_mgr.post_event('{}_{}'.format(sound_name[0], '3p'), self.sound_id, self.pos)
            return

    def get_to_cam_target_length_sqr(self, pos):
        target_pos = None
        if global_data.cam_lctarget:
            target_pos = global_data.cam_lctarget.ev_g_model_position()
        if not target_pos:
            target_pos = self.sound_mgr.get_listener_pos()
        return (pos - target_pos).length_sqr

    def end(self):
        if self._timer:
            global_data.game_mgr.unregister_logic_timer(self._timer)
            self._timer = None
        if self.main_weapon_auto_player_id:
            sound_name = self.main_weapon_sound_name
            if len(sound_name) > 2 and sound_name[2] == 'ai_fix':
                self.sound_mgr.post_event_non_optimization('{}_{}'.format(sound_name[0], 'stop_3p'), self.sound_id, self.pos)
            else:
                self.sound_mgr.stop_playing_id(self.main_weapon_auto_player_id)
            self.main_weapon_auto_player_id = None
        return

    def destroy(self):
        self.end()
        if self.sound_id:
            self.sound_mgr.unregister_game_obj(self.sound_id)
            self.sound_id = None
        return


class BattleSoundAiMgr(object):

    def __init__(self):
        self.random = random.WichmannHill()
        self._sound_ai_a = SoundAi(self.random)
        self._sound_ai_b = SoundAi(self.random)
        self._sound_ai = SoundAi(self.random)
        self._open_log = False
        self.init_event()

    def init_event(self):
        global_data.emgr.play_ai_sound += self.start
        global_data.emgr.play_ai_sound_type += self.start_sound
        global_data.emgr.force_stop_ai_sound += self.force_stop
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect

    def start(self, a_pos, b_pos, battle_type, a_sound_type=None, b_sound_type=None, kill_point_time=0, random_seed=None):
        if random_seed:
            self.random.seed(random_seed)
        a_ai = self._sound_ai_a
        a_ai.pos = a_pos
        sound_type = a_sound_type if a_sound_type is not None else self.generate_battle_sound_type()
        a_ai.set_sound_type(sound_type)
        b_ai = self._sound_ai_b
        b_ai.pos = b_pos
        sound_type = b_sound_type if b_sound_type is not None else self.generate_battle_sound_type()
        b_ai.set_sound_type(sound_type)
        if battle_type == const.AI_BATTLE_TYPE_NO_RESULT:
            a_last_time = kill_point_time
            b_last_time = a_last_time + self.random.uniform(2, 4)
        elif battle_type == const.AI_BATTLE_TYPE_KILL:
            a_last_time = kill_point_time
            b_last_time = a_last_time + self.random.uniform(0.5, 2)
        else:
            a_last_time = kill_point_time
            b_last_time = a_last_time + self.random.uniform(1.5, 3)
        if self.random.random() < 0.5:
            a_delay = 0.0
            b_delay = 3.0
        else:
            a_delay = 3.0
            b_delay = 0.0
        cammand_list = self.generate_cammand(a_ai.sound_type, a_delay, a_last_time)
        a_ai.set_cammand_list(cammand_list)
        cammand_list = self.generate_cammand(b_ai.sound_type, b_delay, b_last_time)
        b_ai.set_cammand_list(cammand_list)
        a_ai.run()
        b_ai.run()
        return

    def start_sound(self, pos, sound_type, random_seed=None):
        if random_seed:
            self.random.seed(random_seed)
        ai = self._sound_ai
        ai.pos = pos
        sound_type = sound_type if sound_type else self.generate_battle_sound_type()
        ai.set_sound_type(sound_type)
        cammand_list = self.generate_cammand(ai.sound_type, 0.0, 1)
        ai.set_cammand_list(cammand_list)
        ai.run()

    def generate_cammand(self, sound_type, delay_time, last_time):
        if self._open_log:
            pass
        sound_type_data = confmgr.get('ai_data', 'Sound_Sim_Type', 'Content', str(sound_type))
        main_weapon_id = sound_type_data.get('MainWeapon')
        main_weapon_data = confmgr.get('ai_data', 'Sound_Sim_Weapon', 'Content', str(main_weapon_id))
        main_weapon_fire_interval = self.get_fire_interval(main_weapon_data['Interval'])
        main_weapon_clip_capacity = main_weapon_data.get('ClipCapacity', 999999)
        main_weapon_cur_bullet_num = main_weapon_clip_capacity
        sub_weapon_id = sound_type_data.get('SideWeapon')
        sub_weapon_fire_last_time = 0
        if sub_weapon_id:
            sub_weapon_data = confmgr.get('ai_data', 'Sound_Sim_Weapon', 'Content', str(sub_weapon_id))
            sub_weapon_fire_last_time += self.random.uniform(0, self.get_fire_interval(sub_weapon_data['CDTime']))
        cammand_list = []
        cur_time = 0
        if delay_time:
            cammand_list.append((cur_time, CAMMAND_TYPE_DELAY, {}))
            cur_time += delay_time
        count = 0
        while cur_time < last_time:
            count += 1
            if count > 100:
                break
            if sub_weapon_id and cur_time > sub_weapon_fire_last_time:
                sub_weapon_fire_last_time = cur_time + self.get_fire_interval(sub_weapon_data['CDTime'])
                cur_time += sub_weapon_data['PreTime']
                fire_times = self.get_fire_times(sub_weapon_data['ShootCnt'])
                if self._open_log:
                    pass
                for index in range(fire_times):
                    cammand = (cur_time,
                     CAMMAND_TYPE_FIRE, {'player_type': sound_type_data.get('PlayerType'),'is_maine_weapon': False})
                    cammand_list.append(cammand)
                    cur_time += sub_weapon_data['ShootInterval']

                cur_time += sub_weapon_data['PostTime']
                continue
            if main_weapon_cur_bullet_num <= 0:
                if self._open_log:
                    pass
                main_weapon_cur_bullet_num = main_weapon_clip_capacity
                cammand_list.append((cur_time, CAMMAND_TYPE_DELAY, {}))
                cur_time += main_weapon_data['ReloadingTime']
                continue
            fire_times = self.get_fire_times(main_weapon_data['ShootCnt'])
            if fire_times > main_weapon_cur_bullet_num:
                fire_times = main_weapon_cur_bullet_num
            if self._open_log:
                pass
            for index in range(fire_times):
                cammand = (cur_time,
                 CAMMAND_TYPE_FIRE, {'player_type': sound_type_data.get('PlayerType'),'is_main_weapon': True})
                cammand_list.append(cammand)
                main_weapon_cur_bullet_num -= 1
                cur_time += main_weapon_data['ShootInterval']

            if main_weapon_cur_bullet_num != 0:
                if self._open_log:
                    pass
                cammand_list.append((cur_time, CAMMAND_TYPE_DELAY, {}))
                cur_time += self.get_fire_interval(main_weapon_data['Interval'])

        return cammand_list

    def get_fire_times(self, shoot_cnt_data):
        all_weight = 0
        area_list = []
        for weight, area in six.iteritems(shoot_cnt_data):
            all_weight += int(weight)
            area_list.append((int(weight), area))

        random_weight = self.random.randint(0, all_weight)
        for weight, area in area_list:
            if random_weight < weight:
                return self.random.randint(area[0], area[1])
        else:
            return self.random.randint(area_list[0][1][0], area_list[0][1][1])

    def get_fire_interval(self, interval_data):
        return self.random.uniform(interval_data[0], interval_data[1])

    def generate_battle_sound_type(self):
        battle = global_data.player.get_battle()
        cur_time = tutil.get_server_time() - battle.init_timestamp
        sound_type_datas = confmgr.get('ai_data', 'Sound_Sim_Type', 'Content')
        all_weight = 0
        sound_type_map = {}
        for sound_type, data in six.iteritems(sound_type_datas):
            weight = int(data['PickWeight'][0] + data['PickWeight'][1] * cur_time)
            sound_type_map[sound_type] = weight
            all_weight += weight

        random_weight = self.random.randint(0, all_weight)
        for sound_type, weight in six.iteritems(sound_type_map):
            if random_weight < weight:
                return sound_type
            random_weight -= weight
        else:
            return 2001

    def force_stop(self):
        self._sound_ai_a.end()
        self._sound_ai_b.end()

    def destroy(self):
        global_data.emgr.play_ai_sound -= self.start
        global_data.emgr.play_ai_sound_type -= self.start_sound
        global_data.emgr.force_stop_ai_sound -= self.force_stop
        global_data.emgr.net_login_reconnect_event -= self.on_login_reconnect
        self._sound_ai_a.destroy()
        self._sound_ai_b.destroy()

    def on_login_reconnect(self, *args):
        self._sound_ai_a.end()
        self._sound_ai_b.end()