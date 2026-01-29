# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gevent/judge_event.py
from __future__ import absolute_import
from common.event.event_base import regist_event
EVENT_LIST = [
 'ob_list_type_changed',
 'judge_cache_add_player',
 'update_cur_observe_ui',
 'judge_cache_player_dead',
 'death_playback_ui_lifetime',
 'fight_plasma_weapon_ui_lifetime',
 'ob_state_set',
 'judge_global_players_dead_state_changed',
 'judge_global_player_bind_mecha_changed',
 'judge_global_player_in_mecha_type_changed',
 'judge_global_player_mecha_cd_type_changed',
 'judge_global_player_recall_cd_end_ts_changed',
 'judge_ob_destroy_all_entities',
 'switch_judge_scope_show_event',
 'judge_need_hide_details_event',
 'judge_global_player_attacking_changed']
regist_event(EVENT_LIST)