# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/BattleReward.py
from __future__ import absolute_import
import six
import math
from random import randint
from ...gcommon import time_utility as tutil
from ..common_const import battle_const, statistics_const
from ..const import NEOX_UNIT_SCALE
import copy
from ...gcommon.item import item_const as iconst
from collections import defaultdict
from logic.gcommon.common_const import activity_const as acconst
from logic.gcommon.cdata import meow_capacity_config as meow_conf
from logic.gcommon.common_const import team_const

def calc_battle_score(rank, poison_level, stat):
    rank_to_score = {200: (1, 1),150: (2, 2),100: (3, 3),80: (5, 10),50: (11, 20),30: (21, 50),20: (51, 100)}
    total_score = 0
    for score, info in six.iteritems(rank_to_score):
        if info[0] <= rank <= info[1]:
            total_score += score
            break

    total_score += poison_level * 10
    if stat:
        damage = stat.get('damage', 0)
        pick_item = stat.get('pick_item', 0)
        move_dist = stat.get('move_dist', 0)
        total_score += int(damage / 20)
        total_score += pick_item
        total_score += int(move_dist / NEOX_UNIT_SCALE / 100)
    return total_score


class Reward(object):
    DUO_EXP_TIME = 1
    DUO_EXP_POINT = 2
    DUO_PROF_TIME = 3
    DUO_PROF_POINT = 4
    YUEKA_EXP = 5
    DECAY_EXP = 6
    WEEKLYCARD_EXP = 7
    RECRUIT_RATE = 8
    CREDIT_RATE = 9
    RETURN_BONUS = 10
    YUEKA_GOLD = 11
    WEEKLYCARD_GOLD = 12
    SUMMER_WELFARE = 13
    AGU_WELFARE = 14

    def __init__(self):
        self.exp = 0
        self.base_exp = 0
        self.gold = 0
        self.proficiency = {}
        self.base_proficiency = {}
        self.bond = {}
        self.extra_exp = []
        self.extra_gold = []
        self.extra_prof = []
        self.items = defaultdict(int)
        self._credit_rate = 0
        self.meow_coin_data = {}
        self.offer_data = {}
        self.settle_rate = 1

    def init_from_dict(self, bdict):
        self.exp = bdict.get('exp', 0)
        self.base_exp = self.exp
        self.gold = bdict.get('gold', 0)
        self.base_gold = self.gold
        self.proficiency.update(bdict.get('proficiency', {}))
        self.base_proficiency.update(self.proficiency)
        self.extra_exp = bdict.get('extra_exp', [])
        self.extra_gold = bdict.get('extra_gold', [])
        self.extra_prof = bdict.get('extra_prof', [])
        self.items = bdict.get('items', {})
        self._credit_rate = 0
        self.bond = bdict.get('bond', {}).copy()
        self.meow_coin_data = bdict.get('meow_coin_data', {})
        self.offer_data = bdict.get('offer_data', {})

    def get_persistent_dict(self):
        persistent_dict = {}
        if self.exp != 0:
            persistent_dict['exp'] = self.exp
        if self.gold > 0:
            persistent_dict['gold'] = self.gold
        if len(self.proficiency) > 0:
            persistent_dict['proficiency'] = self.proficiency
        if self.extra_exp:
            persistent_dict['extra_exp'] = self.extra_exp
        if self.extra_gold:
            persistent_dict['extra_gold'] = self.extra_gold
        if self.extra_prof:
            persistent_dict['extra_prof'] = self.extra_prof
        if self.items:
            persistent_dict['items'] = self.items
        if len(self.bond) > 0:
            persistent_dict['bond'] = self.bond
        if self.meow_coin_data:
            persistent_dict['meow_coin_data'] = self.meow_coin_data
        if self.offer_data:
            persistent_dict['offer_data'] = self.offer_data
        return persistent_dict

    def is_empty(self):
        return not self.get_persistent_dict()

    def set_settle_rate(self, rate):
        self.settle_rate = rate

    def _settle_base_bonus_factor(self, battle, soul_dict, rank, bonus_reward_conf):
        if not bonus_reward_conf:
            return 0
        else:
            bonus_factor = 0.0
            is_draw = soul_dict.get('is_draw', False)
            rank_bonus_conf = bonus_reward_conf.get('rank', None)
            if not is_draw and rank_bonus_conf:
                if soul_dict.get('disable_quit', False):
                    for bonus_rank, bonus in rank_bonus_conf:
                        if bonus_rank >= rank:
                            bonus_factor += bonus
                            break

                else:
                    team_num = battle.get_battle_people_size() / battle.get_battle_team_num()
                    for bonus_rank, bonus in rank_bonus_conf:
                        if int(math.ceil(team_num * bonus_rank / 100.0)) >= rank:
                            bonus_factor += bonus
                            break

            if is_draw:
                bonus_factor += bonus_reward_conf.get('draw', 0)
            elif rank == 1:
                bonus_factor += bonus_reward_conf.get('win', 0)
            else:
                bonus_factor += bonus_reward_conf.get('lose', 0)
            return bonus_factor

    def _settle_bonus_factor(self, battle, soul_dict, rank):
        return 1.0

    def _settle_decay_factor(self, battle, soul_dict, rank):
        match_type = battle.get_match_type()
        if match_type == battle_const.BATTLE_MATCH_TYPE_CHEATER:
            decay_factor = battle_const.ANTICHEAT_BATTLE_REWARD_RATE
        else:
            decay_factor = 1.0
        return decay_factor

    def settle(self, battle, soul_dict, rank):
        pass

    def cost(self, avatar, reason):
        for extra_type, extra_data in self.extra_exp:
            if extra_type == Reward.DUO_EXP_TIME and (avatar is None or avatar.is_duo_exp_time(extra_data, reason)):
                self.add_exp(self.base_exp)
            elif extra_type == Reward.DUO_EXP_POINT and (avatar is None or avatar.cost_duo_exp_point(extra_data, reason)):
                self.add_exp(self.base_exp)
            elif extra_type == Reward.YUEKA_EXP and (avatar is None or avatar.has_yueka()):
                self.add_exp(self.base_exp * iconst.YUEAKA_EXP_ADD)
            elif extra_type == Reward.WEEKLYCARD_EXP and (avatar is None or avatar.has_weeklycard()):
                self.add_exp(self.base_exp * iconst.WEEKLYCARD_EXP_ADD)
            elif extra_type == Reward.RECRUIT_RATE:
                self._credit_rate = extra_data
            elif extra_type == Reward.RETURN_BONUS and (avatar is None or avatar.is_return_buff_time(extra_data, reason)):
                self.add_exp(self.base_exp * iconst.RETURN_BONUS_ADD)

        has_summer_welfare = False
        for extra_type, extra_data in self.extra_gold:
            if extra_type == Reward.YUEKA_GOLD and (avatar is None or avatar.has_yueka()):
                self.add_gold(self.base_gold * iconst.YUEAKA_GOLD_ADD)
            elif extra_type == Reward.WEEKLYCARD_GOLD and (avatar is None or avatar.has_gold_weeklycard()):
                self.add_gold(self.base_gold * iconst.WEEKLYCARD_GOLD_ADD)
            elif extra_type == Reward.SUMMER_WELFARE:
                has_summer_welfare = True
            elif extra_type == Reward.AGU_WELFARE and avatar:
                extra_gold = avatar.get_gu_extra_gold()
                if extra_gold > 0:
                    self.add_gold(extra_gold)

        if has_summer_welfare:
            cur_gold = self.get_gold()
            if cur_gold > 0:
                self.add_gold(cur_gold)
        for extra_type, extra_data in self.extra_prof:
            if extra_type == Reward.DUO_PROF_TIME and (avatar is None or avatar.is_duo_prof_time(extra_data, reason)):
                self.add_proficiency(self.base_proficiency, 0.5)
            elif extra_type == Reward.DUO_PROF_POINT and (avatar is None or avatar.cost_duo_prof_point(extra_data, reason)):
                self.add_proficiency(self.base_proficiency, 0.5)
            elif extra_type == Reward.RETURN_BONUS and (avatar is None or avatar.is_return_buff_time(extra_data, reason)):
                self.add_proficiency(self.base_proficiency, iconst.RETURN_BONUS_ADD)
            elif extra_type == Reward.AGU_WELFARE:
                if avatar is None:
                    extra_proficiency = acconst.GU_EXTRA_PROF_DEFAULT_VAL
                else:
                    extra_proficiency = avatar.get_gu_extra_proficiency()
                if 0 < extra_proficiency < 1:
                    self.add_proficiency(self.base_proficiency, extra_proficiency)

        return

    def set_offer_data(self, offer_data):
        self.offer_data = offer_data

    def offer(self, avatar, reason, ext_data=None):
        reward_dict = {}
        if self.proficiency:
            reward_dict['proficiency'] = self.proficiency
        if self.bond:
            reward_dict['bond'] = self.bond
        item_dict = defaultdict(int)
        item_dict.update(self.items)
        if self.exp > 0:
            if self._credit_rate > 0:
                self.exp = int(self.exp * self._credit_rate / 100)
            item_dict[iconst.ITEM_NO_EXP] += self.exp
        if self.gold >= 0:
            self.gold = avatar.do_battle_gold_reward(self.gold)
            if self.gold > 0:
                item_dict[iconst.ITEM_NO_GOLD] += self.gold
        if item_dict:
            reward_dict['item_dict'] = item_dict
        force_mail = False
        mail_info = None
        if 'mail_info' in self.offer_data:
            force_mail = True
            mail_info = self.offer_data['mail_info']
        avatar.offer_reward_by_dict(reward_dict, reason, ext_data=ext_data, force_mail=force_mail, mail_info=mail_info)
        return

    def add_exp(self, exp):
        self.exp += int(exp * self.settle_rate)

    def add_gold(self, gold):
        if gold <= 0:
            return
        self.gold += int(gold * self.settle_rate)

    def get_gold(self):
        return self.gold

    def add_proficiency(self, proficiency_dict, rate=1.0):
        for mecha_type, prof in six.iteritems(proficiency_dict):
            self.proficiency.setdefault(mecha_type, 0)
            self.proficiency[mecha_type] += int(prof * rate * self.settle_rate)

    def add_bond(self, bond_dict, rate=1.0):
        for role_id, bond in six.iteritems(bond_dict):
            role_id_str = str(role_id)
            self.bond.setdefault(role_id_str, 0)
            self.bond[role_id_str] += int(bond * rate * self.settle_rate)

    def add_items(self, items):
        for item_id, cnt in six.iteritems(items):
            self.items[int(item_id)] += cnt

    def set_meow_coin_data(self, meow_coin_data):
        if meow_coin_data:
            self.meow_coin_data = meow_coin_data

    def add_extra_exp(self, extra_type, extra_data):
        self.extra_exp.append((extra_type, extra_data))

    def add_extra_gold(self, extra_type, extra_data):
        self.extra_gold.append((extra_type, extra_data))

    def add_extra_prof(self, extra_type, extra_data):
        self.extra_prof.append((extra_type, extra_data))


class ExpReward(Reward):

    def _settle_bonus_factor(self, battle, soul_dict, rank):
        map_data = battle.get_map_data()
        exp_reward_data = map_data.play_data.get('exp_reward', None)
        bonus_reward_conf = exp_reward_data['bonux_reward']
        bonus_factor = 1.0
        bonus_factor += self._settle_base_bonus_factor(battle, soul_dict, rank, bonus_reward_conf)
        return bonus_factor

    def settle(self, battle, soul_dict, rank):
        map_data = battle.get_map_data()
        exp_reward_data = map_data.play_data.get('exp_reward', None)
        if not exp_reward_data:
            return
        else:
            soul_id = soul_dict['id']
            statistics = battle.get_entity_statistics(soul_id)
            if not statistics:
                return
            base_reward = 0
            for prop, rate in six.iteritems(exp_reward_data['base_reward']):
                base_reward += statistics.get(prop, 0) * rate

            bonus_factor = self._settle_bonus_factor(battle, soul_dict, rank)
            decay_factor = self._settle_decay_factor(battle, soul_dict, rank)
            exp = max(1, int(base_reward * bonus_factor * decay_factor))
            const_reward_data = exp_reward_data['const_reward']
            if not G_IS_NA_PROJECT and soul_dict.get('lv', 2) <= 1:
                exp = max(exp, 210)
            max_exp = const_reward_data.get('max_exp', None)
            if max_exp:
                exp = min(exp, max_exp)
            now = tutil.time()
            if soul_dict['duo_exp_timestamp'] >= now:
                self.add_extra_exp(Reward.DUO_EXP_TIME, now)
            elif 'duo_exp_point' in const_reward_data and soul_dict['duo_exp_point'] >= const_reward_data['duo_exp_point']:
                self.add_extra_exp(Reward.DUO_EXP_POINT, const_reward_data['duo_exp_point'])
            if soul_dict.get('yueka_timestamp', 0) > now:
                self.add_extra_exp(Reward.YUEKA_EXP, now)
            if soul_dict.get('weeklycard_exp_timestamp', 0) > now:
                self.add_extra_exp(Reward.WEEKLYCARD_EXP, now)
            recruit_rate = soul_dict.get('recruit_group_exp_rate', 0)
            if recruit_rate > 0:
                self.add_extra_exp(Reward.RECRUIT_RATE, recruit_rate)
            credit_exp_rate = soul_dict.get('credit_exp_rate', 0)
            if credit_exp_rate > 0:
                self.add_extra_exp(Reward.CREDIT_RATE, credit_exp_rate)
            if soul_dict['return_buff_timestamp'] >= now:
                self.add_extra_exp(Reward.RETURN_BONUS, now)
            self.add_exp(exp)
            return


class ProficiencyReward(Reward):

    def _settle_bonus_factor(self, battle, soul_dict, rank):
        map_data = battle.get_map_data()
        prof_reward_data = map_data.play_data.get('proficiency_reward', None)
        bonus_reward_conf = prof_reward_data['bonux_reward']
        bonus_factor = 1.0
        bonus_factor += self._settle_base_bonus_factor(battle, soul_dict, rank, bonus_reward_conf)
        intimacy_extra_prof = soul_dict.get('intimacy_extra_prof', False)
        if intimacy_extra_prof:
            bonus_factor += bonus_reward_conf.get('intimacy', 0)
        return bonus_factor

    def settle(self, battle, soul_dict, rank):
        map_data = battle.get_map_data()
        prof_reward_data = map_data.play_data.get('proficiency_reward', None)
        if not prof_reward_data:
            return
        else:
            const_reward_data = prof_reward_data['const_reward']
            max_prof = const_reward_data.get('max_prof', None)
            soul_id = soul_dict['id']
            statistics = battle.get_entity_statistics(soul_id)
            if not statistics:
                return
            bonus_factor = self._settle_bonus_factor(battle, soul_dict, rank)
            decay_factor = self._settle_decay_factor(battle, soul_dict, rank)
            proficiency_dict = {}
            create_mecha_dict = statistics.get(statistics_const.HAS_CREATE_MECHA, {})
            create_mecha_num = len(create_mecha_dict)
            for mecha_type in six.iterkeys(create_mecha_dict):
                base_reward = 0
                for prop, rate in six.iteritems(prof_reward_data['base_reward']):
                    if prop == statistics_const.HAS_CREATE_MECHA:
                        rate = rate * 1.0 / create_mecha_num
                    base_reward += statistics.get(prop, {}).get(mecha_type, 0) * rate

                proficiency = max(0, int(base_reward * bonus_factor * decay_factor))
                if max_prof:
                    proficiency = min(proficiency, max_prof)
                proficiency_dict[mecha_type] = proficiency

            now = tutil.time()
            if soul_dict['duo_prof_timestamp'] >= now:
                self.add_extra_prof(Reward.DUO_PROF_TIME, now)
            elif 'duo_prof_point' in const_reward_data and soul_dict['duo_prof_point'] >= const_reward_data['duo_prof_point']:
                self.add_extra_prof(Reward.DUO_PROF_POINT, const_reward_data['duo_prof_point'])
            if soul_dict['return_buff_timestamp'] >= now:
                self.add_extra_prof(Reward.RETURN_BONUS, now)
            if soul_dict.get('gang_up_activity_open', False):
                self.add_extra_prof(Reward.AGU_WELFARE, None)
            self.add_proficiency(proficiency_dict)
            return


class FVictoryReward(Reward):

    def settle(self, battle, soul_dict, rank):
        from data import battle_config
        battle_type = battle.get_battle_type()
        if not battle_config.need_battle_career_stat(battle_config.get_stat_battle_type(battle_type)):
            return
        is_draw = soul_dict.get('is_draw', False)
        if not battle_config.is_victory_rank(battle_type, rank, is_draw):
            return
        if soul_dict.get('gang_up_activity_open', False):
            gang_victory_cnt = soul_dict['day_stat'].get(statistics_const.GANG_VICTORY_CNT, 0)
            if gang_victory_cnt == 0:
                from data.activity_data import get_extra_server_data
                extra_items = get_extra_server_data(acconst.GANG_UP_ACTICITY_ID).get(acconst.GU_EXTRA_ITEM, {})
                for item_no, item_num in six.iteritems(extra_items):
                    self.items.setdefault(str(item_no), 0)
                    self.items[str(item_no)] += item_num

        if soul_dict['day_stat'].get(statistics_const.VICTORY_CNT, 0) > 0:
            return
        map_data = battle.get_map_data()
        decay_factor = self._settle_decay_factor(battle, soul_dict, rank)
        exp_reward = map_data.play_data.get('exp_reward', {}).get('fixed_reward', {}).get('fvictory', 0)
        exp_reward = max(0, int(exp_reward * decay_factor))
        if exp_reward:
            self.add_exp(exp_reward)
        gold_reward = map_data.play_data.get('gold_reward', {}).get('fixed_reward', {}).get('fvictory', 0)
        gold_reward = max(0, int(gold_reward * decay_factor))
        if gold_reward:
            self.add_gold(gold_reward)
        if soul_dict.get('has_summer_gold_add', False) and 0 < acconst.SUMMER_WELFARE_GOLD_ADD_FACTOR <= 1:
            self.add_extra_gold(Reward.SUMMER_WELFARE, tutil.time())
        item_reward = map_data.play_data.get('item_reward', {}).get('fvictory', {})
        if item_reward:
            for item_no, (item_num, ext_info) in six.iteritems(item_reward):
                time_range_str = ext_info.get('time_range', '')
                if time_range_str:
                    now = tutil.time()
                    start_time_str, end_time_str = time_range_str.split('-')
                    start_time_stamp = tutil.time_str_to_timestamp(start_time_str, '%Y%m%d:%H%M')
                    end_time_stamp = tutil.time_str_to_timestamp(end_time_str, '%Y%m%d:%H%M')
                    if start_time_stamp > now or now >= end_time_stamp:
                        continue
                self.items.setdefault(str(item_no), 0)
                self.items[str(item_no)] += item_num


class GangReward(Reward):

    def settle(self, battle, soul_dict, rank):
        from data import battle_config
        if not soul_dict.get('gang_up', False):
            return
        else:
            map_data = battle.get_map_data()
            decay_factor = self._settle_decay_factor(battle, soul_dict, rank)
            exp_reward = map_data.play_data.get('exp_reward', {}).get('fixed_reward', {}).get('gang', 0)
            exp_reward = max(0, int(exp_reward * decay_factor))
            if exp_reward:
                self.add_exp(exp_reward)
            gold_reward = map_data.play_data.get('gold_reward', {}).get('fixed_reward', {}).get('gang', 0)
            gold_reward = max(0, int(gold_reward * decay_factor))
            if gold_reward:
                self.add_gold(gold_reward)
            if soul_dict.get('gang_up_activity_open', False):
                self.add_extra_gold(Reward.AGU_WELFARE, None)
            return


class ItemReward(Reward):

    def settle(self, battle, soul_dict, rank):
        all_items = soul_dict.get('item_reward', {})
        for item_no, cnt in six.iteritems(all_items):
            self.items[str(item_no)] = cnt

        map_data = battle.get_map_data()
        item_reward = map_data.play_data.get('item_reward', None)
        if not item_reward:
            return
        else:
            rand_num_conf = item_reward.get('rand_num', None)
            if not rand_num_conf:
                return
            from data.item_data import lobby_item_2_backpack_item, get_max_amount_weekly, is_item_time_valid
            pick_limit = soul_dict.get('pick_limit', {})
            for item_no, (min_num, max_num) in six.iteritems(rand_num_conf):
                backpack_item_no = lobby_item_2_backpack_item(item_no, None)
                if not backpack_item_no or not is_item_time_valid(backpack_item_no):
                    continue
                str_item_no = str(item_no)
                max_amount_weekly = get_max_amount_weekly(backpack_item_no, 0)
                if max_amount_weekly > 0:
                    left_num = max_amount_weekly - pick_limit.get(backpack_item_no, 0) - self.items.get(str_item_no, 0)
                    if left_num <= 0:
                        continue
                    else:
                        min_num = min(min_num, left_num)
                        max_num = min(max_num, left_num)
                item_num = randint(min_num, max_num)
                if item_num > 0:
                    self.items.setdefault(str_item_no, 0)
                    self.items[str_item_no] += item_num

            return


class BondReward(Reward):

    def _get_card_extra_reward(self, battle, soul_dict, bond_reward, statistics, rank):
        const_reward_data = bond_reward.get('const_reward')
        if not const_reward_data:
            return 0.0
        else:
            card_reward = 0.0
            yueka_bond_factor = const_reward_data.get('yueka_bond_factor', None)
            if yueka_bond_factor > 0 and soul_dict.get('yueka_timestamp', 0) > tutil.time():
                card_reward += yueka_bond_factor
            return card_reward

    def _settle_bonus_factor(self, battle, soul_dict, rank):
        map_data = battle.get_map_data()
        reward_conf = map_data.play_data.get('bond_reward', None)
        bonus_reward_conf = reward_conf.get('bonux_reward', {})
        bonus_factor = 1.0
        bonus_factor += self._settle_base_bonus_factor(battle, soul_dict, rank, bonus_reward_conf)
        return bonus_factor

    def settle(self, battle, soul_dict, rank):
        map_data = battle.get_map_data()
        bond_reward = map_data.play_data.get('bond_reward', None)
        if not bond_reward:
            return
        else:
            soul_id = soul_dict['id']
            role_id = soul_dict['role_id']
            soul_bond_data = soul_dict.get('bond_data', {})
            if not soul_bond_data:
                return
            statistics = battle.get_entity_statistics(soul_id)
            if not statistics:
                return
            base_reward = self._get_base_reward(battle, soul_dict, bond_reward, statistics, rank)
            bonus_factor = self._settle_bonus_factor(battle, soul_dict, rank)
            decay_factor = self._settle_decay_factor(battle, soul_dict, rank)
            card_extra_reward = self._get_card_extra_reward(battle, soul_dict, bond_reward, statistics, rank)
            bond = base_reward * bonus_factor * (1.0 + card_extra_reward) * decay_factor
            bond = max(int(bond), 0)
            const_reward_data = bond_reward.get('const_reward', {})
            max_bond = const_reward_data.get('max_bond', None)
            if max_bond:
                bond = min(bond, max_bond)
            bond_dict = {}
            bond_dict[role_id] = bond
            self.add_bond(bond_dict)
            return

    def _get_base_reward(self, battle, soul_dict, bond_reward, statistics, rank):
        return self._get_base_reward_common_part(battle, soul_dict, bond_reward, statistics, rank) + self._get_base_reward_special_part(battle, soul_dict, bond_reward, statistics, rank)

    def _get_base_reward_common_part(self, battle, soul_dict, bond_reward, statistics, rank):
        base_reward = 0
        base_mecha_reward_config = bond_reward.get('base_mecha_reward', {})
        if base_mecha_reward_config:
            create_mecha_dict = statistics.get(statistics_const.HAS_CREATE_MECHA, {})
            for mecha_type in six.iterkeys(create_mecha_dict):
                for prop, rate in six.iteritems(base_mecha_reward_config):
                    base_reward += statistics.get(prop, {}).get(mecha_type, 0) * rate

        base_human_reward_config = bond_reward.get('base_human_reward', {})
        for prop, rate in six.iteritems(base_human_reward_config):
            base_reward += statistics.get(prop, 0) * rate

        return base_reward

    def _get_base_reward_special_part(self, battle, soul_dict, bond_reward, statistics, rank):
        return 0


class GoldReward(Reward):

    def _settle_bonus_factor(self, battle, soul_dict, rank):
        map_data = battle.get_map_data()
        reward_conf = map_data.play_data.get('gold_reward', None)
        bonus_reward_conf = reward_conf.get('bonux_reward', {})
        bonus_factor = 1.0
        bonus_factor += self._settle_base_bonus_factor(battle, soul_dict, rank, bonus_reward_conf)
        intimacy_extra_gold = soul_dict.get('intimacy_extra_gold', False)
        if intimacy_extra_gold:
            bonus_factor += bonus_reward_conf.get('intimacy', 0)
        return bonus_factor

    def settle(self, battle, soul_dict, rank):
        map_data = battle.get_map_data()
        reward_conf = map_data.play_data.get('gold_reward', None)
        if not reward_conf:
            return
        else:
            soul_id = soul_dict['id']
            statistics = battle.get_entity_statistics(soul_id)
            if not statistics:
                return
            const_reward_conf = reward_conf.get('const_reward', {})
            base_reward = 0
            base_reward_conf = reward_conf.get('base_reward', {})
            if base_reward_conf:
                for prop, rate in six.iteritems(base_reward_conf):
                    base_reward += statistics.get(prop, 0) * rate

            base_reward = max(base_reward, 0)
            max_base_reward = const_reward_conf.get('max_base_gold', 0)
            if max_base_reward > 0:
                base_reward = min(base_reward, max_base_reward)
            bonus_factor = self._settle_bonus_factor(battle, soul_dict, rank)
            decay_factor = self._settle_decay_factor(battle, soul_dict, rank)
            gold_reward = max(base_reward * bonus_factor * decay_factor, 0)
            gold_reward = PrivilegeGangUpExtra.get_value_after_pgu(soul_dict, gold_reward, acconst.PGU_ADD_GOLD_FACTOR)
            max_reward = const_reward_conf.get('max_gold', 0)
            if max_reward > 0:
                gold_reward = min(gold_reward, max_reward)
            now = tutil.time()
            if soul_dict.get('yueka_timestamp', 0) > now:
                self.add_extra_gold(Reward.YUEKA_GOLD, now)
            now = tutil.time()
            if soul_dict.get('weeklycard_gold_timestamp', 0) > now:
                self.add_extra_gold(Reward.WEEKLYCARD_GOLD, now)
            if soul_dict.get('has_summer_gold_add', False) and 0 < acconst.SUMMER_WELFARE_GOLD_ADD_FACTOR <= 1:
                self.add_extra_gold(Reward.SUMMER_WELFARE, now)
            gold_reward = int(gold_reward)
            self.add_gold(gold_reward)
            return


class MeowRewardSoulData(object):

    def __init__(self):
        self.week_limit = 0
        self.week_left = 0
        self.week_carry_num = 0
        self.mail_total_num = 0
        self.safebox_size = 0
        self.bag_num = 0

    def parse(self, raw_data, week_limit):
        if not raw_data:
            return False
        self.week_limit = week_limit
        if self.week_limit <= 0:
            return False
        self.week_carry_num = raw_data.get('meow_week_carry_num', 0)
        self.mail_total_num = raw_data.get('meow_mail_total_num', 0)
        self.safebox_size = raw_data.get('meow_safebox_size', 0)
        self.bag_num = raw_data.get('meow_bag_num', 0)
        if self.week_carry_num < 0 or self.mail_total_num < 0 or self.safebox_size <= 0 or self.bag_num < 0:
            return False
        self.week_left = self.week_limit - self.week_carry_num - self.mail_total_num
        if self.week_left < 0 or self.week_left > self.week_limit:
            return False
        if meow_conf.meow_coin_one_battle_carry_max_num <= 0:
            return False
        return True


class MeowCoinReward(Reward):

    def settle(self, battle, soul_dict, rank):
        if not soul_dict or rank <= 0:
            return
        else:
            map_data = battle.get_map_data()
            no_meow_coin = map_data.play_data.get('no_meow_coin', None)
            if no_meow_coin:
                return
            from data.item_data import get_max_amount_weekly
            week_limit = get_max_amount_weekly(iconst.ITEM_NO_MEOW_COIN, 0)
            uid = soul_dict.get('uid')
            soul_id = soul_dict.get('id')
            meow_raw_data = soul_dict.get('meow_soul_data', {})
            try:
                meow_soul_data = MeowRewardSoulData()
                if not meow_soul_data.parse(meow_raw_data, week_limit):
                    self.meow_coin_data = {}
                    return
                self.meow_coin_data = {'week_limit': meow_soul_data.week_limit,
                   'this_total': 0,
                   'week_total': meow_soul_data.week_carry_num,
                   meow_conf.capacity_type_bag: 0,
                   meow_conf.capacity_type_safe_box: 0,
                   meow_conf.capacity_type_mail_box: 0
                   }
                battle.update_soul_sa_dict(soul_id, {'meow_coin_data': self.meow_coin_data})
                if meow_soul_data.week_left <= 0:
                    return
                if battle.get_play_type() in battle_const.PLAY_TYPE_SURVIVALS:
                    self._update_meow_chicken_carry_num(battle, soul_dict, rank, meow_soul_data)
                else:
                    self._update_meow_non_chicken_carry_num(battle, soul_dict, rank, meow_soul_data)
                coin_num = self.meow_coin_data.get('this_total', 0)
                if coin_num <= 0:
                    return
                if coin_num > meow_conf.meow_coin_one_battle_carry_max_num:
                    log_error('MeowCoinReward exceed max uid=%s, raw_data=%s coin_num=%s', uid, meow_raw_data, coin_num)
                    coin_num = meow_conf.meow_coin_one_battle_carry_max_num
                self.items[str(iconst.LOBBY_ITEM_NO_MEOW_COIN)] = coin_num
            except Exception as e:
                self.meow_coin_data = {}

            return

    def _update_meow_chicken_carry_num(self, battle, soul_dict, rank, meow_soul_data):
        self.meow_coin_data['this_total'] = meow_soul_data.mail_total_num
        self.meow_coin_data[meow_conf.capacity_type_mail_box] = meow_soul_data.mail_total_num
        bag_max_take = min(meow_soul_data.bag_num, meow_soul_data.week_left)
        if bag_max_take <= 0:
            return
        uid = soul_dict.get('uid')
        personal_rank = soul_dict.get('personal_rank', 0)
        force_quit = soul_dict.get('force_quit', False)
        if personal_rank <= 0:
            personal_rank = rank
        if (personal_rank == 1 or force_quit) and 0 < personal_rank <= meow_conf.battle_carry_all_max_rank:
            self.meow_coin_data[meow_conf.capacity_type_bag] = bag_max_take
            self.meow_coin_data[meow_conf.capacity_type_safe_box] = min(meow_soul_data.safebox_size, bag_max_take)
            self.meow_coin_data['this_total'] += self.meow_coin_data[meow_conf.capacity_type_bag]
        else:
            self.meow_coin_data[meow_conf.capacity_type_safe_box] = min(meow_soul_data.safebox_size, bag_max_take)
            self.meow_coin_data[meow_conf.capacity_type_bag] = self.meow_coin_data[meow_conf.capacity_type_safe_box]
            self.meow_coin_data['this_total'] += self.meow_coin_data[meow_conf.capacity_type_safe_box]
        self.meow_coin_data['week_total'] += self.meow_coin_data['this_total']

    def _update_meow_non_chicken_carry_num(self, battle, soul_dict, rank, meow_soul_data):
        soul_id = soul_dict.get('id')
        statistics = battle.get_entity_statistics(soul_id)
        if not statistics:
            return
        kill_num = statistics.get(statistics_const.KILL_HUMAN, 0) + statistics.get(statistics_const.KILL_MECHA, 0)
        assist_num = statistics.get(statistics_const.ASSIST_HUAMN, 0) + statistics.get(statistics_const.ASSIST_MECHA, 0)
        dead_num = statistics.get(statistics_const.DEAD_HUMAN, 0) + statistics.get(statistics_const.MECHA_DEAD, 0)
        damage = statistics.get(statistics_const.HUMAN_DAMAGE, 0) + statistics.get(statistics_const.MECHA_DAMAGE, 0)
        coin_num = int(1.7 * kill_num + 0.7 * assist_num - 0.2 * dead_num + damage / 5000.0)
        coin_num = min(coin_num, meow_soul_data.week_left)
        if coin_num > 0:
            self.meow_coin_data['this_total'] = coin_num
            self.meow_coin_data[meow_conf.capacity_type_bag] = coin_num
        self.meow_coin_data['week_total'] += self.meow_coin_data['this_total']


class BattleReward(Reward):
    EXP_REWARD = '1'
    FVICTORY_REWARD = '2'
    GANG_REWARD = '3'
    PROF_REWARD = '4'
    ITEM_REWARD = '5'
    BOND_REWARD = '6'
    GOLD_REWARD = '7'
    MEOW_COIN_REWARD = '8'

    def __init__(self):
        super(BattleReward, self).__init__()
        self._rewards = {BattleReward.EXP_REWARD: ExpReward(),
           BattleReward.FVICTORY_REWARD: FVictoryReward(),
           BattleReward.GANG_REWARD: GangReward(),
           BattleReward.PROF_REWARD: ProficiencyReward(),
           BattleReward.ITEM_REWARD: ItemReward(),
           BattleReward.BOND_REWARD: BondReward(),
           BattleReward.GOLD_REWARD: GoldReward(),
           BattleReward.MEOW_COIN_REWARD: MeowCoinReward()
           }

    def init_from_dict(self, bdict, avatar=None, reason=None):
        for reward_type, reward_dict in six.iteritems(bdict):
            reward = self._rewards.get(reward_type, None)
            if not reward:
                continue
            reward.init_from_dict(reward_dict)
            reward.cost(avatar, reason)
            self.extend(reward)

        self.offer_data = bdict.get('offer_data', {})
        return

    def get_persistent_dict(self):
        persistent_dict = {}
        for reward_type, reward in six.iteritems(self._rewards):
            reward_dict = reward.get_persistent_dict()
            if reward_dict:
                persistent_dict[reward_type] = reward_dict

        if self.offer_data:
            persistent_dict['offer_data'] = self.offer_data
        return persistent_dict

    def get_reward(self, reward_type):
        return self._rewards.get(reward_type, None)

    def extend(self, reward):
        self.add_exp(reward.exp)
        self.add_gold(reward.gold)
        self.add_proficiency(reward.proficiency)
        self.add_bond(reward.bond)
        self.add_items(reward.items)
        self.set_meow_coin_data(reward.meow_coin_data)

    def settle(self, battle, soul_dict, rank):
        if not battle:
            return
        if battle.is_from_custom_room() and not battle.is_inner_server_room():
            return
        settle_rate = battle.get_settle_reward_rate()
        for reward in six.itervalues(self._rewards):
            reward.set_settle_rate(settle_rate)
            reward.settle(battle, soul_dict, rank)

    def get_first_victory_gold(self):
        return self._rewards[BattleReward.FVICTORY_REWARD].gold


class SpringGangUpExtra(object):

    @staticmethod
    def get_value_after_sgu(soul_dict, source_value, add_key):
        if not soul_dict or source_value <= 0 or not add_key:
            return source_value
        spring_gu_enabled = soul_dict.get('spring_gu_enabled', False)
        if not spring_gu_enabled:
            return source_value
        add_factor = acconst.SPRING_GANG_UP_ADD_FACTOR_MAP.get(add_key, 0)
        if 1.0 > add_factor > 0:
            return int(source_value * (1.0 + add_factor))
        return source_value


class PrivilegeGangUpExtra(object):

    @staticmethod
    def get_value_after_pgu(soul_dict, source_value, add_key):
        if not soul_dict or source_value <= 0 or not add_key:
            return source_value
        privilege_gu_enabled = soul_dict.get('priv_extra_gold_info', [])
        if not privilege_gu_enabled:
            return source_value
        add_factor = acconst.PRIVILEGE_GANG_UP_ADD_FACTOR_MAP.get(add_key, 0)
        uid = soul_dict.get('uid')
        soul_id = soul_dict.get('id')
        if 1.0 > add_factor > 0:
            return int(source_value * (1.0 + add_factor))
        return source_value