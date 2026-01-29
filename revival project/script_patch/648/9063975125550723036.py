# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/11001.py
_reload_all = True
version = '176298907'
from .pet_status_config import *
cover = {'11001': {PT_IDLE: set([PT_MOVE]),
             PT_MOVE: set([PT_IDLE]),
             PT_HIDE: set([PT_SHOW]),
             PT_SHOW: set([PT_HIDE])
             }
   }
forbid = {'11001': {PT_IDLE: set([]),
             PT_MOVE: set([]),
             PT_HIDE: set([]),
             PT_SHOW: set([])
             }
   }
behavior = {'11001': {PT_IDLE: {'custom_param': {'spec_inter': 3.0,'spec_anim': 'transform_second_shoot','idle_anim': 'transform_idle','start_follow_dist': 5.0,'spec_anim_len': 2.0},'action_state': 'PetIdle'},PT_SHOW: {'action_state': 'PetShow'},PT_HIDE: {'action_state': 'PetHide'},PT_MOVE: {'custom_param': {'follow_acc': 2.0,'end_follow_dist': 2.0,'follow_slow': 2.0,'reset_pos_dist': 100.0,'follow_pos': [13, 20, 6],'follow_speed': 5.0},'action_state': 'PetMove'}}}

def get_cover(npc_id):
    return cover[npc_id]


def get_forbid(npc_id):
    return forbid[npc_id]


def get_behavior(npc_id):
    return behavior[npc_id]