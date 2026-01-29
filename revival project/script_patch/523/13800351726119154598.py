# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/battlemembers/impPveAmbSound.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Dict, Int
from logic.gcommon.common_const.pve_const import PVE_AMB_DICT, PVE_MUSIC_DICT, DEFAULT_PVE_MUSIC_RES

class impPveAmbSound(object):

    def _init_pveambsound_from_dict(self, bdict):
        global_data.emgr.pve_enter_level_event += self.play_level_amb_sound
        self.sound_id = None
        major_level = bdict.get('major_level', 0)
        minor_level = bdict.get('minor_level', 0)
        if major_level or minor_level:
            self.play_level_amb_sound(major_level, minor_level, None)
        return

    def _init_pveambsound_completed(self, bdict):
        pass

    def _tick_pveambsound(self, delta):
        pass

    def _destroy_pveambsound(self, clear_cache):
        global_data.emgr.pve_enter_level_event -= self.play_level_amb_sound
        self.clear_sound()

    def play_level_amb_sound(self, major_level, minor_level, difficulty):
        self.clear_sound()
        level_amb_conf = PVE_AMB_DICT.get(int(major_level), {})
        if level_amb_conf:
            amb_sound = level_amb_conf.get(int(minor_level), level_amb_conf.get(-1))
            event = 'Play_%s_lp' % amb_sound
            self.sound_id = global_data.sound_mgr.post_event_2d_non_opt(event, None)
        return

    def clear_sound--- This code section failed: ---

  40       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'global_data'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_FALSE    43  'to 43'

  41      12  LOAD_GLOBAL           1  'global_data'
          15  LOAD_ATTR             2  'sound_mgr'
          18  LOAD_ATTR             3  'stop_playing_id'
          21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             4  'sound_id'
          27  CALL_FUNCTION_1       1 
          30  POP_TOP          

  42      31  LOAD_CONST            0  ''
          34  LOAD_FAST             0  'self'
          37  STORE_ATTR            4  'sound_id'
          40  JUMP_FORWARD          0  'to 43'
        43_0  COME_FROM                '40'
          43  LOAD_CONST            0  ''
          46  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def get_pve_bgm_path(self):
        env_key = self.get_env_key()
        path_list = PVE_MUSIC_DICT.get(env_key, DEFAULT_PVE_MUSIC_RES)
        return path_list