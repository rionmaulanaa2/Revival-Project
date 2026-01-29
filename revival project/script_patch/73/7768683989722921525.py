# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/battle_sound_ai_proto.py
from __future__ import absolute_import

def on_play_ai_sound(synchronizer, a_position, b_position, battle_type, a_sound_type, b_sound_type, kill_point_time, random_seed):
    from logic.gcommon.common_utils.math3d_utils import tp_to_v3d
    a_pos = tp_to_v3d(a_position)
    b_pos = tp_to_v3d(b_position)
    global_data.emgr.play_ai_sound.emit(a_pos, b_pos, battle_type, a_sound_type, b_sound_type, kill_point_time, random_seed)


def on_play_ai_sound_type(synchronizer, position, battle_type, random_seed):
    from logic.gcommon.common_utils.math3d_utils import tp_to_v3d
    pos = tp_to_v3d(position)
    global_data.emgr.play_ai_sound_type.emit(pos, battle_type, random_seed)


def on_force_stop_ai_sound(synchronizer):
    global_data.emgr.force_stop_ai_sound.emit()