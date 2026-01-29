# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/sunshine_utils.py
from __future__ import absolute_import
import functools

def parse_args(args):
    ret = {}
    for pair in args.split(';'):
        pos = pair.find(':')
        if pos != -1:
            key = pair[:pos]
            value = pair[pos + 1:]
            ret[key] = value
        else:
            ret[pair] = None

    return ret


def execute_in_sunshine():

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not global_data.use_sunshine:
                return
            return func(*args, **kwargs)

        return wrapper

    return decorator


def refresh_mecha_cam_view():
    pos = global_data.cam_lplayer.ev_g_position()
    global_data.emgr.set_target_pos_for_special_logic.emit(pos)
    global_data.emgr.enable_special_target_pos_logic.emit(False)
    global_data.emgr.slerp_into_setupped_camera_event.emit(0.1)
    global_data.emgr.recover_observe_camera_event.emit()