# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/new_system_prompt_data.py
_reload_all = True
SYSTEM_CAREER = 1
SYSTEM_BATTLE_FLAG = 2
SYSTEM_INSCRIPTION = 3
cfg_data = {1: {'show_priority': 2,
       'promotion_begin_ts': 1595437200,
       'promotion_end_ts': 1596042000,
       'skipped': 1,
       'prompt_lv': 5
       },
   2: {'show_priority': 1,
       'promotion_begin_ts': 1596646800,
       'promotion_end_ts': 1597251600,
       'skipped': 1,
       'prompt_lv': 3
       },
   3: {'show_priority': 1,
       'promotion_begin_ts': 1596646800,
       'promotion_end_ts': 4121168400,
       'skipped': 1,
       'prompt_lv': 6,
       'sp_check_func_name': 'inscription_check'
       }
   }
SYS_TYPES = frozenset(cfg_data.keys())

def is_system_prompt(advance_id):
    return advance_id in cfg_data