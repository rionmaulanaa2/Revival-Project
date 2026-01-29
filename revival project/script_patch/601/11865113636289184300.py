# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gevent/movie_event.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'movie_camera_prepare',
 'movie_model_set',
 'movie_model_anim',
 'movie_end',
 'movie_start',
 'movie_model_hidden',
 'movie_model_showed',
 'movie_model_set_var',
 'movie_sp_lobby_mecha_cam',
 'movie_model_move',
 'movie_sfx_restart',
 'movie_sfx_shutdown',
 'movie_screen_effect',
 'movie_sp_jet_scene_effect']
regist_event(EVENT_LIST)