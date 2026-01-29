# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/third_part_app_utils.py
from __future__ import absolute_import
from __future__ import print_function
import six
from logic.gcommon.common_const.third_party_app_const import ThridPartyAppManifest

def gen_tpa_data_for_launch_report():
    url_scheme_way = False
    ios_scheme_deeplink = global_data.channel.get_prop_str('ios_scheme_deeplink')
    if ios_scheme_deeplink:
        url_scheme_way = True
        from logic.gutils import deeplink_utils
        url_scheme_params_dict = deeplink_utils.parse_ios_scheme_deeplink(ios_scheme_deeplink)
        if global_data.is_inner_server:
            print('gen_tpa_data_for_launch_report ios_scheme_deeplink', url_scheme_params_dict)
    else:
        url_scheme_params_dict = {}

    def get_param_val(key):
        if url_scheme_way:
            return url_scheme_params_dict.get(key, None)
        else:
            return global_data.channel.get_prop_str(key)
            return None

    ret_dict = {}
    for tpa_type, keys in six.iteritems(ThridPartyAppManifest):
        for key in keys:
            param_val = get_param_val(key)
            if param_val is not None and param_val != '':
                if tpa_type not in ret_dict:
                    ret_dict[tpa_type] = {}
                ret_dict[tpa_type][key] = param_val

    return ret_dict


def _tpa_match_type_2_battle_info_candidates(tpa_match_type):
    from logic.gcommon.common_const.third_party_app_const import TPA_MATCH_TYPE_CHICKEN_SOLO, TPA_MATCH_TYPE_DEATH_SOLO, TPA_MATCH_TYPE_GVG_SOLO
    from logic.gcommon.common_const import battle_const
    from logic.gcommon.common_utils import battle_utils
    if tpa_match_type == TPA_MATCH_TYPE_CHICKEN_SOLO:
        sorted_num_list = battle_utils.get_supported_teammate_num_by_play_mode_and_type(battle_const.PLAY_TYPE_CHICKEN, battle_const.BATTLE_TYPE_COMPETITION)
        return ((battle_const.PLAY_TYPE_CHICKEN, team_num, battle_const.BATTLE_TYPE_COMPETITION) for team_num in sorted_num_list)
    else:
        if tpa_match_type == TPA_MATCH_TYPE_DEATH_SOLO:
            sorted_num_list = battle_utils.get_supported_teammate_num_by_play_mode_and_type(battle_const.PLAY_TYPE_DEATH, battle_const.BATTLE_TYPE_COMPETITION)
            return ((battle_const.PLAY_TYPE_DEATH, team_num, battle_const.BATTLE_TYPE_COMPETITION) for team_num in sorted_num_list)
        if tpa_match_type == TPA_MATCH_TYPE_GVG_SOLO:
            sorted_num_list = battle_utils.get_supported_teammate_num_by_play_mode_and_type(battle_const.PLAY_TYPE_GVG, battle_const.BATTLE_TYPE_COMPETITION)
            return ((battle_const.PLAY_TYPE_GVG, team_num, battle_const.BATTLE_TYPE_COMPETITION) for team_num in sorted_num_list)
        print(('Match type mapping to be defined.', tpa_match_type))
        return None
        return None


def tpa_match_type_2_battle_tid(tpa_match_type):
    candidates = _tpa_match_type_2_battle_info_candidates(tpa_match_type)
    if candidates is None:
        return
    else:
        from logic.comsys.lobby.MatchMode import MatchMode
        from logic.gcommon.common_utils import battle_utils
        for battle_info in candidates:
            play_type, team_num, battle_type = battle_info
            if not MatchMode.will_show_mode(play_type, team_num):
                continue
            battle_tid = battle_utils.get_battle_id_by_player_mode_and_type(play_type, team_num, battle_type)
            if battle_tid is not None:
                return battle_tid
        else:
            print('tpa_match_type_2_battle_tid And then there were none.')
            return

        return