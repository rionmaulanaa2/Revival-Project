# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/Team.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
import time
import math
from logic.gcommon import time_utility
from logic.gcommon.common_const import battle_const

class TeamMember(object):

    def __init__(self, uid, uinfo):
        self._uid = uid
        self._join_time = time.time()
        self._info = {}
        self._is_online = True
        self.set_uinfo(uinfo)

    def get_match_dict(self):
        mdict = {'mb': self._binary_mb,
           'eid': self._info.get('eid', None),
           'uid': self._uid,
           'char_name': self.get_char_name(),
           'role_id': self.get_role(),
           'role_skin': self._info.get('role_skin', 0),
           'lv': self.get_lv(),
           'nfc_lv': self._info.get('nfc_lv', 0),
           'last_beginer_battle': self._info.get('last_beginer_battle', 0),
           'match_score': self._info.get('match_score', 0),
           'death_match_score': self._info.get('death_match_score', 0),
           'head_frame': self._info.get('head_frame', None),
           'head_photo': self._info.get('head_photo', None),
           'afk_lv': self._info.get('afk_lv', 0),
           'battle_flag': self._info.get('battle_flag', {}),
           'usual_mecha_ids': self._info.get('usual_mecha_ids', []),
           'dan_info': self.get_dan_info(),
           'is_emulator': self._info.get('is_emulator', False),
           'is_cheater': self._info.get('is_cheater', False),
           'team_id': self._info.get('team_id', None),
           'exclude_scene': self._info.get('exclude_scene', ()),
           'mecha_skin': self._info.get('mecha_skin', 0),
           'intimacy_relation_lv_data': self._info.get('intimacy_relation_lv_data', {}),
           'island_role_charm': self._info.get('island_role_charm', 0),
           'island_mecha_charm': self._info.get('island_mecha_charm', 0),
           'role_skin_weapon_sfx': self._info.get('role_skin_weapon_sfx', 0),
           'mecha_skin_weapon_sfx': self._info.get('mecha_skin_weapon_sfx', 0),
           'priv_lv': self._info.get('priv_lv', 0),
           'priv_settings': self._info.get('priv_settings', {})
           }
        lst_rank5_game_id = self._info.get('lst_rank5_game_id', None)
        lst_rank5_ts = self._info.get('lst_rank5_ts', 0)
        if lst_rank5_game_id and lst_rank5_ts + battle_const.ILLEGAL_TEAM_TIME > time_utility.time():
            mdict['lst_rank5_game_id'] = lst_rank5_game_id
        return mdict

    def set_uinfo(self, uinfo):
        if self._info and 'team_idx' in self._info:
            uinfo['team_idx'] = self._info['team_idx']
        self._info.update(uinfo)
        self._mb = uinfo.get('mb', None)
        self._binary_mb = uinfo.get('bmb', None)
        self._eid = uinfo.get('eid', None)
        if not self._mb and 'mb' in self._info:
            del self._info['mb']
        return

    def get_mb(self):
        return self._mb

    def get_binary_mb(self):
        return self._binary_mb

    def get_info(self):
        return self._info

    def is_ready(self):
        return self._info.get('ready', False)

    def get_hang_up_ts(self):
        return self._info.get('hang_up_ts', 0)

    def get_uid(self):
        return self._uid

    def get_eid(self):
        return self._eid

    def get_team_idx(self):
        return self._info.get('team_idx', -1)

    def update_mb(self, mb, binary_mb):
        self._mb = mb
        self._binary_mb = binary_mb

    def set_ready_state(self, state):
        self._info['ready'] = state

    def get_ready_state(self):
        return self._info.get('ready', False)

    def get_match_queue_id(self):
        return self._info.get('match_queue_id', None)

    def get_battle_type(self):
        return self._info.get('battle_type', None)

    def dress_clothing(self, clothing_dict):
        for part, item_no in six.iteritems(clothing_dict):
            self._info['clothing_dict'][part] = item_no

    def undress_clothing(self, part_list):
        for part in part_list:
            if part in self._info['clothing_dict']:
                del self._info['clothing_dict'][part]

    def get_match_score(self):
        return self._info['match_score']

    def get_char_name(self):
        return self._info['char_name']

    def get_lv(self):
        return self._info['lv']

    def get_dan_info(self):
        return self._info['dan_info']

    def get_role(self):
        return self._info['role_id']

    def get_join_time(self):
        return self._join_time

    def set_head_frame(self, item_no):
        self._info['head_frame'] = item_no

    def get_head_frame(self):
        return self._info.get('head_frame', 0)

    def set_head_photo(self, item_no):
        self._info['head_photo'] = item_no

    def get_head_photo(self):
        return self._info.get('head_photo', 0)

    def get_afk_punish_left_time(self):
        afk_punish_time = self._info.get('afk_punish_time', 0)
        return max(int(math.ceil(afk_punish_time - time_utility.time())), 0)

    def get_imt_punish_left_time(self):
        imt_punish_time = self._info.get('imt_punish_time', 0)
        return max(int(math.ceil(imt_punish_time - time_utility.time())), 0)

    def get_allow_match_left_time(self):
        match_punish_ts = self._info.get('match_punish_ts', 0)
        return max(int(math.ceil(match_punish_ts - time_utility.time())), 0)

    def get_match_punish_reason(self):
        return self._info.get('match_punish_reason', None)

    def is_emulator(self):
        return self._info.get('is_emulator', False)

    def is_cheater(self):
        return self._info.get('is_cheater', False)

    def set_online(self, is_online):
        self._is_online = is_online

    def is_online(self):
        return self._is_online


class Team(object):

    def __init__(self, leader, team_id, battle_type, auto_match, max_size):
        self._teamer = {}
        self._max_size = max_size
        self._leader = leader
        self._team_id = team_id
        self._battle_type = battle_type
        self._auto_match = auto_match
        self._shard_mb = None
        self._public_info = {}
        self._idxs = [
         0] * max_size
        self._idx_sp = 0
        return

    def get_members(self):
        return self._teamer

    def get_size(self):
        return len(self._teamer)

    def get_next_idx(self, uid):
        cur = -1
        for i in range(0, self._max_size):
            cur = self._idx_sp
            self._idx_sp = (cur + 1) % self._max_size
            if not self._idxs[cur]:
                self._idxs[cur] = uid
                break

        return cur

    def get_publicteam_shard_mb(self):
        return self._shard_mb

    def is_public(self):
        return self._shard_mb is not None

    def get_public_info(self):
        return self._public_info

    def set_public_info(self, public_info):
        self._public_info = public_info

    def clear_idx(self, idx):
        self._idxs[idx] = 0

    def update_teamer_info(self, uid, uinfo):
        if uid in self._teamer:
            self._teamer[uid].set_uinfo(uinfo)

    def add_teammate(self, uid, uinfo):
        if len(self._teamer) >= self._max_size:
            return False
        if 'team_idx' not in uinfo:
            idx = self.get_next_idx(uid)
            uinfo['team_idx'] = idx
        self._teamer[uid] = TeamMember(uid, uinfo)
        return True

    def del_teammate(self, uid):
        if uid not in self._teamer:
            return None
        else:
            teammate = self._teamer.pop(uid)
            idx = teammate.get_team_idx()
            if idx >= 0:
                self.clear_idx(idx)
            if uid == self._leader and self._teamer:
                teamer_ids = six_ex.keys(self._teamer)
                sorted_teamer_ids = sorted(teamer_ids, key=lambda x: self._teamer[x].get_join_time())
                self._leader = sorted_teamer_ids[0]
            return teammate

    def get_teammate(self, uid):
        return self._teamer.get(uid, None)

    def update_teammate_uinfo(self, uid, uinfo, check_change=False):
        teamer = self.get_teammate(uid)
        if not teamer:
            return (False, None)
        else:
            cur_uinfo = teamer.get_info()
            if check_change:
                is_change = False
                for key, value in six.iteritems(uinfo):
                    if key not in cur_uinfo or cur_uinfo[key] != value:
                        cur_uinfo[key] = value
                        is_change = True

            else:
                is_change = True
                cur_uinfo.update(uinfo)
            return (
             is_change, cur_uinfo)

    def get_teammate_uinfo(self, uid):
        teamer = self.get_teammate(uid)
        if not teamer:
            return None
        else:
            return teamer.get_info()

    def get_team_dict(self, membs):
        result = {'leader': self._leader,
           'team_id': self._team_id,
           'battle_type': self._battle_type,
           'auto_match': self._auto_match,
           'members': {},'public_info': self._public_info
           }
        for uid in membs:
            result['members'][uid] = self.get_teammate_uinfo(uid)

        return result

    def get_leader(self):
        return self._leader

    def get_team_id(self):
        return self._team_id

    def get_all_binary_mb(self):
        all_mbs = {}
        for uid, teamer in six.iteritems(self._teamer):
            all_mbs[teamer.get_eid()] = teamer.get_binary_mb()

        return all_mbs

    def get_all_match_info(self):
        all_info = {}
        for uid, teamer in six.iteritems(self._teamer):
            all_info[teamer.get_eid()] = teamer.get_match_dict()

        return all_info

    def get_battle_type(self):
        return self._battle_type

    def set_battle_type(self, battle_type):
        self._battle_type = battle_type

    def get_auto_match(self):
        return self._auto_match

    def set_auto_match(self, auto_match):
        self._auto_match = auto_match

    def set_leader(self, leader):
        self._leader = leader

    def cal_avrg_score(self):
        total_score = 0
        for uid, teamer in six.iteritems(self._teamer):
            total_score += teamer.get_match_score()

        return int(total_score * 1.0 / len(self._teamer))

    def get_highest_score(self):
        highest_score = 0
        for uid, teamer in six.iteritems(self._teamer):
            cur_score = teamer.get_match_score()
            if cur_score > highest_score:
                highest_score = cur_score if 1 else highest_score

        return highest_score

    def is_emulator_team(self):
        if G_IS_NA_PROJECT:
            return False
        for uid, teamer in six.iteritems(self._teamer):
            if teamer.is_emulator():
                return True

        return False

    def is_cheater_team(self):
        for uid, teamer in six.iteritems(self._teamer):
            if teamer.is_cheater():
                return True

        return False

    def get_match_type(self):
        if self.is_emulator_team():
            return battle_const.BATTLE_MATCH_TYPE_EMULATOR
        else:
            if self.is_cheater_team():
                return battle_const.BATTLE_MATCH_TYPE_CHEATER
            return battle_const.BATTLE_MATCH_TYPE_NORMAL

    def set_publicteam_shard_mb(self, shard_mb):
        self._shard_mb = shard_mb