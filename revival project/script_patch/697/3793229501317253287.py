# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impPve.py
from __future__ import absolute_import
import math
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Bool, Dict, List, Int, Uuid, Float, Str
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_const import pve_const
from logic.gcommon.time_utility import get_server_time, time_str_to_timestamp
from common.utils.timer import CLOCK
from common.cfg import confmgr
import six_ex
from logic.gutils.pve_utils import get_archive_key
from logic.gcommon.utility import nested_dict_add
from logic.gcommon.common_const.pve_const import DIFFICUTY_LIST, MATCH_AGAIN_TYPE_NONE, MATCH_AGAIN_TYPE_ARCHIVE, MATCH_AGAIN_TYPE_AUTO_MATCH
from logic.gcommon.common_const.team_const import TEAMMATE_MATCH_AGAIN_TYPE_NONE

class impPve(object):

    def _init_pve_from_dict(self, bdict):
        self._last_pve_difficulty = bdict.get('last_pve_difficulty', pve_const.NORMAL_DIFFICUTY)
        self._last_pve_chapter = bdict.get('last_pve_chapter', 1)
        self._last_pve_player_size = bdict.get('last_pve_player_size', 1)
        self._unlock_difficulty = bdict.get('unlock_difficulty', {'1': pve_const.NORMAL_DIFFICUTY})
        self._next_free_add_key_ts = bdict.get('next_free_add_key_ts', -1)
        self._pve_suggest_info = bdict.get('pve_suggest_info', {})
        self._pve_suggest_like_info_dict = {}
        self._cant_request_like_info = []
        self._pve_archive_dict = bdict.get('pve_archive_dict', {})
        self._pve_archive_read_data = bdict.get('pve_archive_read_data', {})
        self.pve_kill_monster_cnt = bdict.get('kill_monster_cnt', {})
        self.pve_choose_bless_cnt = bdict.get('choose_bless_cnt', {})
        self.pve_choose_break_cnt = bdict.get('choose_break_cnt', {})
        self.pve_chapter_kill_monster_cnt = {}
        self.set_pve_chapter_kill_monster_cnt()

    def get_chapter_unlock_difficulty(self, chapter):
        chapter = str(chapter)
        return self._unlock_difficulty.get(chapter, 0)

    def get_unlock_chapter(self):
        unlock_chapter_list = []
        for chapter, unlock_difficulty in six_ex.items(self._unlock_difficulty):
            if unlock_difficulty:
                unlock_chapter_list.append(int(chapter))

        return unlock_chapter_list

    def get_next_free_add_key_ts(self):
        return self._next_free_add_key_ts

    def get_last_pve_difficulty(self):
        return self._last_pve_difficulty

    def get_last_pve_chapter(self):
        return self._last_pve_chapter

    def get_last_pve_player_size(self):
        return self._last_pve_player_size

    def set_last_pve_chapter_info(self, difficulty, chapter, player_size):
        chapter_unlock_difficulty = self.get_chapter_unlock_difficulty(chapter)
        if difficulty > chapter_unlock_difficulty:
            difficulty = max(chapter_unlock_difficulty, pve_const.NORMAL_DIFFICUTY)
        self._last_pve_difficulty = difficulty
        self._last_pve_chapter = chapter
        self._last_pve_player_size = player_size

    def save_pve_archive(self):
        self.call_soul_method('save_pve_archive', ())

    def rematch_pve_battle(self):
        chapter = self.get_last_pve_chapter()
        difficulty = self.get_last_pve_difficulty()
        player_size = self.get_last_pve_player_size()
        if global_data.enable_pve_team and self.is_in_team():
            pve_battle_info = self.get_pve_battle_info()
            if pve_battle_info:
                chapter = pve_battle_info.get('chapter')
                difficulty = pve_battle_info.get('difficulty')
                player_size = pve_battle_info.get('pve_player_size')
        use_archive = global_data.rematch_pve_tag == MATCH_AGAIN_TYPE_ARCHIVE
        auto_match = global_data.rematch_pve_tag == MATCH_AGAIN_TYPE_AUTO_MATCH
        self.start_pve_battle(chapter, difficulty, use_archive, player_size, auto_match)

    def start_pve_battle(self, chapter, difficulty, use_archive=False, player_size=1, auto_match=False):
        if chapter > global_data.pve_max_chapter:
            return
        from ext_package.ext_decorator import has_pve_ext
        if not has_pve_ext(chapter):
            global_data.game_mgr.show_tip(get_text_by_id(83610))
            global_data.ui_mgr.show_ui('ExtDownloadInfoUI', 'logic.comsys.lobby.ExtNpk')
            return
        self.call_server_method('try_start_pve_battle', (chapter, difficulty, use_archive, player_size, auto_match))
        self.set_last_pve_chapter_info(difficulty, chapter, player_size)
        from logic.gcommon.common_const.team_const import TEAMMATE_MATCH_AGAIN_TYPE_NONE
        self.teammate_match_again_type = TEAMMATE_MATCH_AGAIN_TYPE_NONE
        global_data.rematch_pve_tag = MATCH_AGAIN_TYPE_NONE

    @rpc_method(CLIENT_STUB, (Int('chapter'), Int('difficulty'), Int('player_size'), Dict('archive')))
    def update_pve_archive(self, chapter, difficulty, player_size, archive):
        key = get_archive_key(chapter, difficulty, player_size)
        self._pve_archive_dict[key] = archive

    def get_pve_archive(self):
        return self._pve_archive_dict

    @rpc_method(CLIENT_STUB, (Int('chapter'), Int('difficulty'), Int('player_size'), Int('cnt')))
    def update_pve_archive_read_data(self, chapter, difficulty, player_size, cnt):
        key = get_archive_key(chapter, difficulty, player_size)
        self._pve_archive_read_data[key] = cnt

    def get_pve_archive_read_data(self):
        return self._pve_archive_read_data

    @rpc_method(CLIENT_STUB, (Int('chapter'), Int('difficulty'), Int('player_size')))
    def clear_pve_archive(self, chapter, difficulty, player_size):
        key = get_archive_key(chapter, difficulty, player_size)
        self._pve_archive_dict.pop(key, 0)
        self._pve_archive_read_data.pop(key, None)
        return

    @rpc_method(CLIENT_STUB, (Int('chapter'), Int('difficulty')))
    def new_difficulty_unlock(self, chapter, difficulty):
        self._unlock_difficulty[str(chapter)] = difficulty
        self._last_pve_difficulty = difficulty

    @rpc_method(CLIENT_STUB, (Dict('d_difficulty'),))
    def update_difficulty_unlock(self, d_difficulty):
        self._unlock_difficulty = d_difficulty

    def get_pve_suggest_is_open(self):
        conf = confmgr.get('pve_suggest_conf', 'SuggestPeriodConf', 'Content')
        cur_time_stamp = get_server_time()
        for period_id, period_info in conf.items():
            start_time = period_info.get('start_time', 0)
            start_time_stamp = time_str_to_timestamp(start_time, '%Y/%m/%d-%H:%M')
            end_time = period_info.get('end_time', 0)
            end_time_stamp = time_str_to_timestamp(end_time, '%Y/%m/%d-%H:%M')
            if start_time_stamp <= cur_time_stamp and cur_time_stamp <= end_time_stamp:
                return period_id

        return None

    def request_suggest_info(self, sheet_id):
        print (
         'request_suggest_info', sheet_id)
        if sheet_id not in self._cant_request_like_info:
            from logic.gutils import micro_webservice_utils
            micro_webservice_utils.micro_service_request('PveSuggestService', {'sheet_id': sheet_id}, self.request_suggest_info_callback)

    def request_suggest_info_callback(self, result, args):
        print ('request_suggest_info_callback', result)
        if not result:
            return
        data = result.get('data')
        if isinstance(result, dict) and result.get('code') == 200 and data:
            sheet_id = data.get('sheet_id')
            all_suggest_info = data.get('data')
            for suggest_info in all_suggest_info:
                suggest_id = suggest_info[0]
                like_count = suggest_info[1]
                self._pve_suggest_like_info_dict[suggest_id] = like_count

            global_data.emgr.message_on_suggest_info.emit(sheet_id, all_suggest_info)
            self._cant_request_like_info.append(sheet_id)
            self.request_timer = global_data.game_mgr.register_logic_timer(self.clear_request_suggest_info_timer, interval=60, times=1, mode=CLOCK)

    def clear_request_suggest_info_timer(self):
        self._cant_request_like_info.pop(0)
        if self.request_timer:
            global_data.game_mgr.unregister_logic_timer(self.request_timer)
            self.request_timer = None
        return

    def do_like_pve_suggest(self, sheet_id, suggest_id):
        self.call_server_method('do_like_pve_suggest', (sheet_id, suggest_id))

    @rpc_method(CLIENT_STUB, (Str('sheet_id'), Str('suggest_id')))
    def on_do_like_pve_suggest(self, sheet_id, suggest_id):
        if not self._pve_suggest_like_info_dict.get(suggest_id):
            self._pve_suggest_like_info_dict[suggest_id] = 0
        self._pve_suggest_like_info_dict[suggest_id] += 1
        if not self._pve_suggest_info.get(sheet_id):
            self._pve_suggest_info[sheet_id] = []
        self._pve_suggest_info[sheet_id].append(suggest_id)
        global_data.emgr.on_do_like_pve_suggest.emit(sheet_id, suggest_id)

    def get_pve_suggest_is_like(self, sheet_id, suggest_id):
        return suggest_id in self._pve_suggest_info.get(sheet_id, [])

    def get_pve_suggest_like_count(self, suggest_id):
        return self._pve_suggest_like_info_dict.get(suggest_id, 0)

    @rpc_method(CLIENT_STUB, (Dict('kill_data'), Dict('blesses_data'), Dict('breakthrough_data')))
    def update_pve_stat_data(self, kill_data, blesses_data, breakthrough_data):
        self.pve_kill_monster_cnt = nested_dict_add(self.pve_kill_monster_cnt, kill_data)
        self.pve_choose_bless_cnt = nested_dict_add(self.pve_choose_bless_cnt, blesses_data)
        self.pve_choose_break_cnt = nested_dict_add(self.pve_choose_break_cnt, breakthrough_data)
        self.set_pve_chapter_kill_monster_cnt()

    def get_all_pve_kill_monster_cnt(self):
        return self.pve_kill_monster_cnt

    def has_unlock_difficulty_monster_book(self, difficulty, monster_id):
        return self.get_kill_monster_cnt(difficulty, monster_id) > 0

    def has_unlock_monster_book(self, monster_id):
        for difficulty in DIFFICUTY_LIST:
            if self.has_unlock_difficulty_monster_book(difficulty, monster_id):
                return True

        return False

    def get_kill_monster_cnt(self, difficulty, monster_id):
        difficulty_monster_kill_data = self.pve_kill_monster_cnt.get(str(difficulty), {})
        return difficulty_monster_kill_data.get(str(monster_id), 0)

    def set_pve_chapter_kill_monster_cnt(self):
        if not self.pve_kill_monster_cnt:
            return
        self.pve_chapter_kill_monster_cnt = {}
        all_monster_conf = confmgr.get('pve_catalogue_conf', 'MonsterBookConf', 'Content', default={})
        for conf_id, monster_conf in six_ex.items(all_monster_conf):
            if monster_conf.get('is_inner', 0) == 1 and not G_CLIENT_TRUNK:
                continue
            monster_id = monster_conf.get('monster_id')
            belong_chapter = monster_conf.get('belong_chapter', 1)
            for difficulty, monster_kill_data in six_ex.items(self.pve_kill_monster_cnt):
                if type(monster_kill_data) != dict:
                    continue
                if not monster_kill_data:
                    continue
                for kill_monster_id, kill_monster_cnt in six_ex.items(monster_kill_data):
                    if monster_id == int(kill_monster_id):
                        if not self.pve_chapter_kill_monster_cnt.get(belong_chapter):
                            self.pve_chapter_kill_monster_cnt[belong_chapter] = {}
                        if not self.pve_chapter_kill_monster_cnt[belong_chapter].get(difficulty):
                            self.pve_chapter_kill_monster_cnt[belong_chapter][difficulty] = {}
                        self.pve_chapter_kill_monster_cnt[belong_chapter][difficulty][str(monster_id)] = kill_monster_cnt

    def get_pve_all_chapter_kill_monster_cnt(self):
        return self.pve_chapter_kill_monster_cnt

    def get_pve_chapter_kill_monster_cnt(self, chapter):
        return self.pve_chapter_kill_monster_cnt.get(int(chapter), {})

    def get_all_choose_blesses_cnt(self):
        return self.pve_choose_bless_cnt

    def has_unlock_bless_book(self, bless_id):
        return self.get_choose_blesses_cnt(bless_id) > 0

    def get_choose_blesses_cnt(self, bless_id):
        return self.pve_choose_bless_cnt.get(str(bless_id), 0)

    def get_all_choose_breakthrough_cnt(self):
        return self.pve_choose_break_cnt

    def has_unlock_breakthrough_book(self, mecha_id, slot_id):
        return self.get_choose_breakthrough_cnt(mecha_id, slot_id) > 0

    def get_choose_breakthrough_cnt(self, mecha_id, slot_id):
        break_data = self.pve_choose_break_cnt.get(str(mecha_id), {})
        return break_data.get(str(slot_id), 0)