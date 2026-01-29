# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/debug/debug.py
from __future__ import absolute_import
import world

def init_object_count_output(gamemgr):
    if not hasattr(world, 'get_spaceobject_count'):
        return
    if not hasattr(world, 'get_sharedobject_count'):
        return

    def callback():
        pass

    timermgr = gamemgr.get_logic_timer()
    timermgr.register(func=callback, interval=60)


def goto_new_main_scene():
    global_data.game_mgr.load_scene('Main')


def goto_win_test_scene():
    global_data.game_mgr.load_scene('TestWin')