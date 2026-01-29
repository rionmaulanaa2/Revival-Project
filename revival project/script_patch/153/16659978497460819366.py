# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHitJudge.py
from __future__ import absolute_import
from six.moves import range
from ..UnitCom import UnitCom
import time
import data.hit_judge_arg as hit_judge_arg
import cc
from logic.gcommon.common_const import battle_const
MECHA_PREFIX = 'mecha_'
HUMAN_PREFIX = 'human_'

class ComHitJudge(UnitCom):
    BIND_EVENT = {'E_HIT_OTHER': 'hit_other',
       'E_LOAD_HIT_RANGE_CONFIG': 'load_range_config'
       }

    def __init__(self):
        super(ComHitJudge, self).__init__()
        self._last_target_id = 0
        self._start_time = 0
        self._damage_list = []
        self._damage_range = {}
        self._scale_range = {}

    def init_from_dict(self, unit_obj, bdict):
        super(ComHitJudge, self).init_from_dict(unit_obj, bdict)

    def on_post_init_complete(self, bdict):
        super(ComHitJudge, self).on_post_init_complete(bdict)
        self.load_range_config()

    def load_range_config(self):
        if not self.ev_g_is_avatar():
            return
        else:
            self._damage_range = {}
            self._scale_range = {}
            all_prefixes = (MECHA_PREFIX, HUMAN_PREFIX)
            for one_prefix in all_prefixes:
                for index in range(1, 20):
                    damage_key = one_prefix + 'damage_range_' + str(index)
                    one_damage_range = getattr(hit_judge_arg, damage_key, None)
                    scale_key = one_prefix + 'scale_range_' + str(index)
                    one_scale_range = getattr(hit_judge_arg, scale_key, None)
                    if not one_damage_range or not one_scale_range:
                        break
                    self._damage_range.setdefault(one_prefix, []).append(one_damage_range)
                    self._scale_range.setdefault(one_prefix, []).append(one_scale_range)

            return

    def hit_other(self, target_obj, damage_value, *args, **kwargs):
        if not self.ev_g_is_avatar():
            return
        if not self._damage_range:
            self.load_range_config()
        target_id = target_obj.id
        cur_time = time.time()
        if target_id != self._last_target_id:
            self._last_target_id = target_id
            self._damage_list = []
        while len(self._damage_list) > 0:
            add_time, _ = self._damage_list[0]
            pass_time = cur_time - add_time
            if pass_time <= hit_judge_arg.total_hit_time:
                break
            self._damage_list.pop(0)

        is_change_target = False
        if len(self._damage_list) <= 0:
            is_change_target = True
        self._damage_list.append((cur_time, damage_value))
        total_damage = 0
        for _, one_damage_value in self._damage_list:
            total_damage += one_damage_value

        prefix = MECHA_PREFIX
        if target_obj.ev_g_is_human():
            prefix = HUMAN_PREFIX
        one_type_damage_range = self._damage_range[prefix]
        one_type_scale_range = self._scale_range[prefix]
        range_index = 0
        if total_damage > one_type_damage_range[-1][1]:
            range_index = len(one_type_damage_range) - 1
        for index in range(len(one_type_damage_range)):
            one_damage_range = one_type_damage_range[index]
            if one_damage_range[0] <= total_damage and total_damage <= one_damage_range[1]:
                range_index = index
                break

        damage_range = one_type_damage_range[range_index]
        scale_range = one_type_scale_range[range_index]
        total_damage = min(total_damage, damage_range[1])
        damage_scale = (total_damage - damage_range[0]) / (damage_range[1] - damage_range[0])
        effect_scale = scale_range[0] + (scale_range[1] - scale_range[0]) * damage_scale
        ui = global_data.ui_mgr.get_ui('BattleHitFeedBack')
        is_change_target = False
        if ui:
            ui._handle_hit_other_event(hit_judge_arg.fade_out_time, effect_scale, is_change_target)