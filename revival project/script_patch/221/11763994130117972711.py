# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/audio/sound.py
from __future__ import absolute_import
import audio
_enable = True
_bluetooth_headset_connected = False

def init():
    global _bluetooth_headset_connected
    import game3d
    if not is_enable():
        return
    audio.limit_events(True)
    _bluetooth_headset_connected = game3d.is_bluetooth_headset_connected()


def init_check_bluetooth():
    if hasattr(audio, 'purge'):
        global_data.game_mgr.register_logic_timer(_check_bluetooth, 30)


def _check_bluetooth():
    global _bluetooth_headset_connected
    import game3d
    if _bluetooth_headset_connected != game3d.is_bluetooth_headset_connected():
        _bluetooth_headset_connected = not _bluetooth_headset_connected
        if _bluetooth_headset_connected:
            audio.purge()
            audio.init()
            init_user_setting()


def init_user_setting():
    pass


def is_enable():
    global _enable
    return _enable


def enable():
    global _enable
    _enable = True
    set_mute(_enable)


def disable():
    global _enable
    _enable = False
    set_mute(_enable)


def play_sound(event, volume=1.0, position=None):
    if is_enable():
        audio.play_event(event, volume, position)


def stop_group_volume_by_name(group_name):
    if is_enable():
        audio.stop_group_volume_by_name(group_name)


def play_music_not_stop(eventname):
    if is_enable():
        audio.play_music(eventname)


def stop_music(eventname):
    if is_enable():
        audio.stop_music(eventname)


def play_music(eventname):
    pass


def init_before_login():
    from logic.comsys.archive.archive_manager import ArchiveManager
    data_general = ArchiveManager().get_general_archive_data()
    if not data_general:
        return
    music_volume = data_general.get_field('last_user_music', 1.0)
    set_music_group_volume(music_volume, False)
    sound_volume = data_general.get_field('last_user_sound', 1.0)
    set_sound_group_volume(sound_volume, False)


def set_3d_listener(center, look_at, up_vector):
    if is_enable():
        audio.set_3d_listener(center, look_at, up_vector)


def stop_all_music():
    if is_enable():
        audio.stop_all_music()


def set_sound_group_volume(volume, persist=True):
    pass


def set_music_group_volume(volume, persist=True):
    pass


def set_voice_volume(volume, persist=True):
    pass


def get_music_group_volume():
    return audio.get_group_volume_by_name('music')


def set_mute(is_mute):
    if is_enable():
        audio.set_mute(is_mute)


is_weak = 0

def weak_all_voice(weak):
    global is_weak
    if weak:
        is_weak += 1
    else:
        is_weak -= 1
    if is_weak > 1:
        return
    music_volume = get_music_group_volume()
    sound_volume = audio.get_group_volume_by_name('ui')
    if is_weak == 1 and weak is True:
        music_volume = music_volume / 3.0
        sound_volume = sound_volume / 3.0
    elif is_weak == 0 and weak is False:
        music_volume = music_volume * 3.0
        sound_volume = sound_volume * 3.0
    set_music_group_volume(music_volume, False)
    set_sound_group_volume(sound_volume, False)
    is_weak = weak


def recover_weak_voice--- This code section failed: ---

 166       0  LOAD_GLOBAL           0  'get_music_group_volume'
           3  CALL_FUNCTION_0       0 
           6  STORE_FAST            0  'music_volume'

 167       9  LOAD_GLOBAL           1  'audio'
          12  LOAD_ATTR             2  'get_group_volume_by_name'
          15  LOAD_CONST            1  'ui'
          18  CALL_FUNCTION_1       1 
          21  STORE_FAST            1  'sound_volume'

 168      24  LOAD_GLOBAL           3  'is_weak'
          27  LOAD_CONST            2  ''
          30  COMPARE_OP            4  '>'
          33  POP_JUMP_IF_FALSE    82  'to 82'

 169      36  POP_JUMP_IF_FALSE     3  'to 3'
          39  BINARY_MULTIPLY  
          40  STORE_FAST            0  'music_volume'

 170      43  LOAD_FAST             1  'sound_volume'
          46  LOAD_CONST            3  3
          49  BINARY_MULTIPLY  
          50  STORE_FAST            1  'sound_volume'

 171      53  LOAD_GLOBAL           4  'set_music_group_volume'
          56  LOAD_FAST             0  'music_volume'
          59  LOAD_GLOBAL           5  'False'
          62  CALL_FUNCTION_2       2 
          65  POP_TOP          

 172      66  LOAD_GLOBAL           6  'set_sound_group_volume'
          69  LOAD_FAST             1  'sound_volume'
          72  LOAD_GLOBAL           5  'False'
          75  CALL_FUNCTION_2       2 
          78  POP_TOP          
          79  JUMP_FORWARD          0  'to 82'
        82_0  COME_FROM                '79'

 173      82  LOAD_CONST            2  ''
          85  STORE_GLOBAL          3  'is_weak'

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 36