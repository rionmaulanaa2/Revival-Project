# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/rank/PVERankDataObj.py
from __future__ import absolute_import
from logic.gcommon.common_const.pve_const import TYPE_PVE_RANK_MONTHLY, NORMAL_DIFFICUTY
from logic.gcommon.common_const.pve_rank_const import PVE_RANK_1_ALL, PVE_RANK_2_TEAM, PVE_RANK_3_TEAM, PVE_RANK_1_FRIEND, PVE_CONFIG_KEY_CHAPTER, PVE_CONFIG_KEY_MECHA_ID, PVE_CONFIG_KEY_DIFFICULTY, PVE_CONFIG_KEY_LIST_TYPE, PVE_CONFIG_KEY_IS_FRIEND, PVE_CONFIG_KEY_PLAYER_CNT, PVE_CONFIG_KEY_PLAYER_CNT_MODE

class PVERankDataObj(object):
    __slots__ = ('_chapter', '_difficulty', '_list_type', '_mecha_id', '_is_friend',
                 '_player_cnt', '_player_cnt_mode')

    def __init__(self, page_config):
        self.init_args(page_config)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.to_server() == self.to_server() or other.to_client() == self.to_client()
        if isinstance(other, str):
            return other == self.to_server() or other == self.to_client()
        return False

    def clone(self):
        config = {s_arg[1:]:getattr(self, s_arg) for s_arg in self.__slots__}
        return self.__class__(config)

    def __str__(self):
        s_args = [ '{}({})'.format(s_arg[1:], str(getattr(self, s_arg))) for s_arg in self.__slots__ ]
        return '_'.join(s_args)

    def to_server(self):
        if self._player_cnt > 1:
            rank_type = '_'.join([str(self._chapter), str(self._difficulty), str(self._list_type), str(self._mecha_id), str(self._player_cnt)])
        else:
            rank_type = '_'.join([str(self._chapter), str(self._difficulty), str(self._list_type), str(self._mecha_id)])
        return rank_type

    def to_client(self):
        return self.get_rank_key()

    def get_rank_key(self):
        rank_type = '_'.join([str(self._chapter), str(self._difficulty), str(self._list_type), str(self._mecha_id), str(self._player_cnt)])
        return rank_type

    def init_args(self, config):
        if isinstance(config, str):
            self.load_str_config(config)
        else:
            self.load_page_config(config)

    def load_str_config(self, rank_key):
        datas = rank_key.split('_')
        self._chapter = int(datas[0])
        self._difficulty = int(datas[1])
        self._list_type = int(datas[2])
        self._mecha_id = int(datas[3])
        self._player_cnt = int(datas[4]) if len(datas) > 4 else 1
        self._player_cnt_mode = -1
        self._is_friend = False

    def load_page_config(self, page_config):
        self._chapter = page_config.get(PVE_CONFIG_KEY_CHAPTER, 1)
        self._difficulty = page_config.get(PVE_CONFIG_KEY_DIFFICULTY, NORMAL_DIFFICUTY)
        self._list_type = page_config.get(PVE_CONFIG_KEY_LIST_TYPE, TYPE_PVE_RANK_MONTHLY)
        self._mecha_id = page_config.get(PVE_CONFIG_KEY_MECHA_ID, 0)
        self._is_friend = page_config.get(PVE_CONFIG_KEY_IS_FRIEND, False)
        self._player_cnt = page_config.get(PVE_CONFIG_KEY_PLAYER_CNT, 1)
        self._player_cnt_mode = page_config.get(PVE_CONFIG_KEY_PLAYER_CNT_MODE, -1)

    def modify_config_data(self, page_config):
        if page_config.get(PVE_CONFIG_KEY_CHAPTER) != None:
            self._chapter = page_config.get(PVE_CONFIG_KEY_CHAPTER)
        if page_config.get(PVE_CONFIG_KEY_DIFFICULTY) != None:
            self._difficulty = page_config.get(PVE_CONFIG_KEY_DIFFICULTY)
        if page_config.get(PVE_CONFIG_KEY_LIST_TYPE) != None:
            self._list_type = page_config.get(PVE_CONFIG_KEY_LIST_TYPE)
        if page_config.get(PVE_CONFIG_KEY_MECHA_ID) != None:
            self._mecha_id = page_config.get(PVE_CONFIG_KEY_MECHA_ID)
        if page_config.get(PVE_CONFIG_KEY_IS_FRIEND) != None:
            self._is_friend = page_config.get(PVE_CONFIG_KEY_IS_FRIEND)
        if page_config.get(PVE_CONFIG_KEY_PLAYER_CNT) != None:
            self._player_cnt = page_config.get(PVE_CONFIG_KEY_PLAYER_CNT)
        if page_config.get(PVE_CONFIG_KEY_PLAYER_CNT_MODE) != None:
            self._player_cnt_mode = page_config.get(PVE_CONFIG_KEY_PLAYER_CNT_MODE)
        return

    def get_cur_config(self):
        config = {PVE_CONFIG_KEY_CHAPTER: self._chapter,
           PVE_CONFIG_KEY_DIFFICULTY: self._difficulty,
           PVE_CONFIG_KEY_LIST_TYPE: self._list_type,
           PVE_CONFIG_KEY_MECHA_ID: self._mecha_id,
           PVE_CONFIG_KEY_IS_FRIEND: self._is_friend,
           PVE_CONFIG_KEY_PLAYER_CNT: self._player_cnt
           }
        return config

    def switch_choose_friend_rank(self, is_friend):
        self._is_friend = is_friend
        self._on_config_change(PVE_CONFIG_KEY_IS_FRIEND)

    def switch_choose_chapter(self, _chapter):
        self._chapter = _chapter
        self._on_config_change(PVE_CONFIG_KEY_CHAPTER)

    def switch_choose_player_cnt(self, num, is_friend):
        self._player_cnt = num
        self._is_friend = is_friend
        global_data.emgr.on_switch_pve_rank_player_cnt.emit(self.get_cur_config())

    def switch_choose_difficulty(self, _difficulty):
        self._difficulty = _difficulty
        self._on_config_change(PVE_CONFIG_KEY_DIFFICULTY)

    def switch_choose_list_type(self, _list_type):
        self._list_type = _list_type
        self._on_config_change(PVE_CONFIG_KEY_LIST_TYPE)

    def switch_choose_mecha(self, _mecha_id):
        self._mecha_id = _mecha_id
        self._on_config_change(PVE_CONFIG_KEY_MECHA_ID)

    def _on_config_change(self, source_key):
        self._emit_conifig_change(source_key)

    def _emit_conifig_change(self, source_key):
        global_data.emgr.on_change_pve_rank_condition.emit(source_key, self.get_cur_config())

    def is_friend_rank(self):
        return self._is_friend

    def get_chapter(self):
        return self._chapter

    def get_player_cnt(self):
        return self._player_cnt

    def get_player_cnt_mode(self):
        mode = None
        if self._player_cnt == 1:
            mode = PVE_RANK_1_FRIEND if self._is_friend else PVE_RANK_1_ALL
        elif self._player_cnt == 2:
            mode = PVE_RANK_2_TEAM
        elif self._player_cnt == 3:
            mode = PVE_RANK_3_TEAM
        return mode

    def get_difficulty(self):
        return self._difficulty

    def get_list_type(self):
        return self._list_type

    def get_mecha_id(self):
        return self._mecha_id