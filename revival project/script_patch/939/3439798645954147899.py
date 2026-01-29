# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/KizunaHitCallHelper.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
from common.const.uiconst import BASE_LAYER_ZORDER_1, UI_VKB_NO_EFFECT
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import activity_const
from logic.client.const.camera_const import POSTURE_STAND, POSTURE_SQUAT, POSTURE_GROUND, POSTURE_JUMP
import cc
from logic.gcommon import time_utility as tutil
import time
import game
import world
from logic.client.const import pc_const
from logic.gutils import pc_utils
from logic.gcommon.common_const.skill_const import SKILL_ROLL, SKILL_AIR_JUMP
SINGLE_BEAT = 1
MULTIPLE_BEAT = 2
LONG_BEAT = 3

class KizunaHitCallGenerator(object):

    def __init__(self):
        self.quick_key_map = {game.VK_1: SINGLE_BEAT,
           game.VK_2: MULTIPLE_BEAT,
           game.VK_3: LONG_BEAT,
           game.VK_4: None
           }
        self._registered_keyboard = False
        self.keynote_record = []
        self.battle_record = {}
        self.result_record = []
        self._song_start_time = 0
        self._song_no = 0
        return

    def destroy(self):
        if self._registered_keyboard:
            self.recover_keyboard_ctrl()

    def init_record(self):
        self.keynote_record = []
        self._song_start_time = 0
        self._song_no = 0
        bat = global_data.battle
        if bat:
            self._song_no = bat.song_idx
            if bat.song_idx == -1 and bat.song_idx != None:
                global_data.game_mgr.show_tip('\xe6\x9c\xaa\xe5\x9c\xa8\xe6\x92\xad\xe6\x94\xbe\xe6\xad\x8c\xe6\x9b\xb2\xef\xbc\x8c\xe4\xb8\x8d\xe8\x83\xbd\xe8\xbf\x9b\xe5\x85\xa5\xe7\x94\x9f\xe6\x88\x90\xe6\xa8\xa1\xe5\xbc\x8f,\xe5\x9c\xa8\xe6\xad\x8c\xe6\x9b\xb2\xe5\xbc\x80\xe5\xa7\x8b\xe5\x90\x8e\xe5\x86\x8d\xe6\xac\xa1\xe8\xb0\x83\xe7\x94\xa8\xe6\x8c\x87\xe4\xbb\xa4')
                return
            self._song_start_time = tutil.get_server_time()
        return

    def init_keyboard_ctrl(self):
        partctrl = global_data.game_mgr.scene.get_com('PartCtrl')
        if not partctrl:
            return
        else:
            partctrl.unregister_keys()
            import logic.vscene.parts.ctrl.GamePyHook as game_hook
            game_hook.add_key_handler(None, six_ex.keys(self.quick_key_map), self.on_quick_key)
            self._registered_keyboard = True
            return

    def recover_keyboard_ctrl(self):
        if not self._registered_keyboard:
            return
        else:
            partctrl = global_data.game_mgr.scene.get_com('PartCtrl')
            if not partctrl:
                return
            import logic.vscene.parts.ctrl.GamePyHook as game_hook
            game_hook.remove_key_handler(None, six_ex.keys(self.quick_key_map), self.on_quick_key)
            partctrl.register_keys()
            self._registered_keyboard = False
            return

    def on_quick_key(self, msg, keycode):
        if keycode == game.VK_4:
            self.init_record()
        else:
            self.keynote_record.append((time.time(), tutil.get_server_time(), msg, keycode))
            global_data.game_mgr.show_tip('\xe6\x8c\x89\xe4\xb8\x8b\xe6\x8c\x89\xe9\x94\xae %s' % str(keycode))

    def process_key_note(self):
        processing_type = -1
        processing_beat_time = [0, 0]
        last_finished_time = -1
        self.result_record = []
        result_record = []
        len_keynotes = len(self.keynote_record)
        for idx, keynote in enumerate(self.keynote_record):
            _, server_t, msg, keycode = keynote
            current_type = self.quick_key_map[keycode]
            if msg == game.MSG_KEY_DOWN:
                if processing_type != -1:
                    log_error('keynote appears when last one is not finish! Will be postponed!', keynote)
                else:
                    processing_type = current_type
                    if idx + 1 >= len_keynotes:
                        return
                    for jdx in range(idx + 1, len_keynotes):
                        _, j_server_t, j_msg, j_keycode = self.keynote_record[jdx]
                        if j_msg == game.MSG_KEY_UP and processing_type == self.quick_key_map[j_keycode]:
                            middle_time = (j_server_t - server_t) / 2.0 + server_t
                            if j_server_t - server_t < MIN_BEAT_TIME_LENGTH:
                                processing_beat_time = [
                                 middle_time - MIN_BEAT_TIME_LENGTH / 2.0, middle_time + MIN_BEAT_TIME_LENGTH / 2.0]
                            else:
                                processing_beat_time = [
                                 server_t, j_server_t]
                            if processing_beat_time[0] < last_finished_time:
                                processing_beat_time[0] = last_finished_time + 0.1
                            last_finished_time = processing_beat_time[-1]
                            processing_beat_time = [ round(t - self._song_start_time, 2) for t in processing_beat_time ]
                            result_record.append({'type': processing_type,'time_range': processing_beat_time})
                            processing_type = -1
                            break
                        else:
                            log_error('unmatched keynote appears! Will be discard!', jdx, keynote)

        merging_multiple_beat = {}
        for info in result_record:
            if info['type'] != MULTIPLE_BEAT:
                if merging_multiple_beat:
                    self.result_record.append(merging_multiple_beat)
                    merging_multiple_beat = {}
                self.result_record.append(info)
            elif not merging_multiple_beat:
                merging_multiple_beat = {'type': MULTIPLE_BEAT,'time_ranges': [info['time_range']]}
            elif merging_multiple_beat['time_ranges'][-1][-1] - info['time_range'][0] < 3:
                merging_multiple_beat['time_ranges'].append(info['time_range'])
            else:
                self.result_record.append(merging_multiple_beat)
                merging_multiple_beat = {'type': MULTIPLE_BEAT,'time_ranges': [info['time_range']]}

        for info in self.result_record:
            if info['type'] == MULTIPLE_BEAT:
                info['time_range'] = [
                 info['time_ranges'][0][0], info['time_ranges'][-1][-1]]

        for index, ret in enumerate(self.result_record):
            print('ret %04d' % index, ret)