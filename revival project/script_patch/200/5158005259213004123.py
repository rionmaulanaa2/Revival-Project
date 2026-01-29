# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/SoundDrive.py
from __future__ import absolute_import
import six
import time
import common.utils.timer as timer
import copy
import game3d
import logic.gcommon.common_utils.bcast_utils as bcast
from mobile.common.IdManager import IdManager
import logic.gcommon.const as const
from logic.gcommon.utility import dummy_cb
CONTROL_TYPE_PLAY = 1
CONTROL_TYPE_STOP = 0
CONTROL_TYPE_STOP_FADEOUT = 2
END_TIEM = -1
SOUND_VISIBLE_STOP = 0
SOUND_VISIBLE_ONE = 1
SOUND_VISIBLE_LOOP = 2
RUN_STATE = 'run_state'
TOUCH_STATE = 'touch_state'
CUSTOM_STATE = 'custom_state'

class SoundState(object):

    def __init__(self, sound_drive, command_data):
        self.command_data = command_data
        self.enable = False
        self.cur_index = 0
        self.start_time = 0
        self.cur_command_data = None
        self.tick_timer = None
        self.sound_drive = sound_drive
        self.is_run = False
        return

    def start(self):
        if self.is_run:
            return
        self.is_run = True
        self.enable = True if self.command_data else False
        self.cur_index = 0
        if self.enable:
            self.start_time = time.time()
            self.cur_command_data = self.command_data[self.cur_index]
            self.clean_timer()
            self.tick_timer = global_data.game_mgr.register_logic_timer(self.tick, interval=1, times=-1, mode=timer.LOGIC)
            self.tick()

    def clean_timer(self):
        if self.tick_timer:
            global_data.game_mgr.unregister_logic_timer(self.tick_timer)
            self.tick_timer = None
        return

    def tick(self):
        elapsed_time = time.time() - self.start_time
        while True:
            if self.cur_command_data['time'] == END_TIEM:
                self.clean_timer()
                break
            elif elapsed_time >= self.cur_command_data['time']:
                self.sound_drive.execute(self.cur_command_data)
                self.cur_index += 1
                if self.cur_index < len(self.command_data):
                    self.cur_command_data = self.command_data[self.cur_index]
                else:
                    self.enable = False
                    self.clean_timer()
                    break
            else:
                break

    def end(self):
        if not self.is_run:
            return
        self.is_run = False
        self.clean_timer()
        if not self.enable:
            return
        while self.cur_index < len(self.command_data):
            command_data = self.command_data[self.cur_index]
            if command_data['time'] == END_TIEM:
                self.sound_drive.execute(command_data)
            self.cur_index += 1

        self.enable = True

    def cancel(self):
        self.is_run = False
        self.clean_timer()

    def destroy(self):
        self.clean_timer()
        self.sound_drive = None
        return


class SoundDrive(object):

    def __init__(self, unit_obj, command_data, skin_id=None):
        self.sound_states = {}
        if isinstance(command_data, dict):
            if 'common' in command_data:
                if str(skin_id) in command_data:
                    command_data = command_data[str(skin_id)]
                else:
                    command_data = command_data['common']
            for key, value in six.iteritems(command_data):
                self.sound_states[key] = SoundState(self, value)

        else:
            self.sound_states[RUN_STATE] = SoundState(self, command_data)
        self.sound_param = command_data
        self.unit_obj = unit_obj
        self.send_event = self.unit_obj.send_event
        self.get_value = self.unit_obj.get_value
        self.delay_index = 0
        self.delay_callback = {}
        self.loop_sound_name = set()

    def touch_start(self):
        TOUCH_STATE in self.sound_states and self.sound_states[TOUCH_STATE].start()

    def touch_end(self):
        TOUCH_STATE in self.sound_states and self.sound_states[TOUCH_STATE].end()

    def touch_cancel(self):
        TOUCH_STATE in self.sound_states and self.sound_states[TOUCH_STATE].cancel()

    def run_start(self):
        RUN_STATE in self.sound_states and self.sound_states[RUN_STATE].start()

    def run_end(self):
        RUN_STATE in self.sound_states and self.sound_states[RUN_STATE].end()
        self.force_clean_loop_sound()

    def custom_start(self):
        CUSTOM_STATE in self.sound_states and self.sound_states[CUSTOM_STATE].start()

    def custom_end(self):
        CUSTOM_STATE in self.sound_states and self.sound_states[CUSTOM_STATE].end()

    def start_custom_sound(self, key):
        key in self.sound_states and self.sound_states[key].start()

    def end_custom_sound(self, key):
        key in self.sound_states and self.sound_states[key].end()

    def end_all_sound(self):
        for sound_state in six.itervalues(self.sound_states):
            sound_state.end()

    def get_running_state_keys(self):
        key_list = []
        for key, sound_state in six.iteritems(self.sound_states):
            if sound_state.is_run:
                key_list.append(key)

        return key_list

    def execute(self, command_data):
        delay_time = command_data.get('delay', 0.0)
        if delay_time > 0:
            command_data_ex = copy.deepcopy(command_data)
            command_data_ex['delay'] = 0.0
            delay_index = self.delay_index
            self.delay_index += 1

            def delay_callback():
                self.execute(command_data_ex)
                if delay_index in self.delay_callback:
                    del self.delay_callback[delay_index]

            self.delay_callback[delay_index] = global_data.game_mgr.register_logic_timer(delay_callback, interval=delay_time, times=1, mode=timer.CLOCK)
        else:
            condition = command_data.get('condition', None)
            if condition:
                if condition == 'air' and self.get_value('G_ON_GROUND'):
                    return
                if condition == 'land' and not self.get_value('G_ON_GROUND'):
                    return
            sound_name = command_data['sound_name']
            command_type = command_data.get('command_type', CONTROL_TYPE_PLAY)
            pos_yoffset = command_data.get('pos_yoffset', 0.0)
            is_loop = command_data.get('is_loop', False)
            force_record = command_data.get('force_record', False)
            sound_visible = command_data.get('sound_visible', None)
            visible_type = command_data.get('visible_type', const.SOUND_TYPE_MECHA_FOOTSTEP)
            if not self.unit_obj or not self.unit_obj.is_valid():
                return
            self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', command_type, sound_name, pos_yoffset, is_loop, sound_visible, visible_type, force_record)
            if is_loop or sound_visible == SOUND_VISIBLE_LOOP:
                self.loop_sound_name.add(sound_name)
            if is_loop:
                spell_id = IdManager.genid()
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND,
                 (
                  command_type, sound_name, pos_yoffset, is_loop, sound_visible, visible_type, force_record),
                 None, True, spell_id, 'E_STOP_ALL_MECHA_ACTION_SOUND'], True)
            else:
                if isinstance(sound_name, tuple):
                    if sound_name[0].endswith('_on') or sound_name[0].endswith('_off'):
                        return
                self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND,
                 (
                  command_type, sound_name, pos_yoffset, is_loop, sound_visible, visible_type, force_record)], True)
        return

    def force_clean_loop_sound(self):
        if self.loop_sound_name:
            self.send_event('E_MECHA_FORCE_CLEAN_LOOP_SOUND', self.loop_sound_name)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_MECHA_FORCE_CLEAN_LOOP_SOUND, (list(self.loop_sound_name),)], True)

    def destroy(self):
        for sound_state in six.itervalues(self.sound_states):
            sound_state.destroy()

        self.sound_states = {}
        for callback_id in six.itervalues(self.delay_callback):
            global_data.game_mgr.unregister_logic_timer(callback_id)

        self.delay_callback = {}
        self.unit_obj = None
        self.send_event = dummy_cb
        self.get_value = dummy_cb
        return