# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/status_override_cover_config.py
_reload_all = True
from .status_config import *
special_2_basic_config = {ST_RELOAD_LOOP: ST_RELOAD,
   ST_DOWN_TRANSMIT_STAND: ST_DOWN,
   ST_CROUCH_MOVE: ST_MOVE,
   ST_CROUCH_RUN: ST_RUN
   }
data = {ST_STAND: set([ST_DOWN_TRANSMIT_STAND]),
   ST_CROUCH_RUN: set([ST_CROUCH_MOVE]),
   ST_LOAD: set([ST_RELOAD_LOOP]),
   ST_DEAD: set([ST_DOWN_TRANSMIT_STAND]),
   ST_ROLL: set([ST_DOWN_TRANSMIT_STAND]),
   ST_DOWN: set([ST_DOWN_TRANSMIT_STAND]),
   ST_FLY: set([ST_DOWN_TRANSMIT_STAND]),
   ST_MECH_EJECTION: set([ST_DOWN_TRANSMIT_STAND]),
   ST_CROUCH_MOVE: set([ST_CROUCH_RUN]),
   ST_CROUCH: set([ST_CROUCH_MOVE, ST_CROUCH_RUN]),
   ST_SHOOT: set([ST_RELOAD_LOOP]),
   ST_SKATE: set([ST_CROUCH_MOVE, ST_CROUCH_RUN]),
   ST_SWIM: set([ST_DOWN_TRANSMIT_STAND]),
   ST_PARACHUTE: set([ST_DOWN_TRANSMIT_STAND])
   }

def get_config_sets():
    return data