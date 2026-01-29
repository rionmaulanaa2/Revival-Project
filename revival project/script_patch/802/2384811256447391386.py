# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/cinematic/cinecallback.py
from __future__ import absolute_import
from __future__ import print_function
dlgwnd_callback = None
subtitle_wnd_callback = None
get_player_model_callback = None
get_scene_offset_callback = None
light_callback = None

def default_dlgwnd_callback(text, typeid, model_name, duration):
    print('%d said: %s. last %d seconds' % (typeid, text, duration))


def default_subtitle_wnd_callback(text, duration):
    print('this is a subtitle: %s. last %d seconds' % (text, duration))


def default_scene_offset_callback(scn_file):
    print(scn_file)
    import math3d
    return math3d.vector(0, 0, 0)


def default_light_callback(scn):
    return scn.get_light('char')


dlgwnd_callback = default_dlgwnd_callback
subtitle_wnd_callback = default_subtitle_wnd_callback
get_scene_offset_callback = default_scene_offset_callback
light_callback = default_light_callback
INPUT_TYPE_MOUSE_KEY = 0
INPUT_TYPE_MOUSE_WHELL = 1
INPUT_TYPE_KEY = 2

def on_mouse_key(msg, key):
    default_input_callback(INPUT_TYPE_MOUSE_KEY, (msg, key))


def on_mouse_whell(msg, delta, key_state):
    default_input_callback(INPUT_TYPE_MOUSE_WHELL, (msg, delta, key_state))


def on_key(msg, key_code):
    default_input_callback(INPUT_TYPE_KEY, (msg, key_code))


def init_default_input():
    import game
    game.on_mouse_msg = on_mouse_key
    game.on_mouse_wheel = on_mouse_wheel
    game.on_key_msg = on_key


def on_input_callback(input_type, params):
    from . import cineaction
    cineaction.on_input_callback(input_type, params)