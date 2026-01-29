# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impThirdPartyApp.py
from __future__ import absolute_import
from __future__ import print_function
import six
import game3d
import six.moves.urllib.request
import six.moves.urllib.parse
import six.moves.urllib.error
from logic.gcommon.common_const.third_party_app_const import ThridPartyAppManifest, TPA_PARAM_MATCH_TYPE, TPA_REES
from common.platform import third_part_app_utils
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str

class impThirdPartyApp(object):

    @rpc_method(CLIENT_STUB, (Str('content'), Str('deeplink')))
    def respon_third_party_app(self, content, deeplink):
        self.show_msg_imp(content)
        if deeplink:
            game3d.open_url(six.moves.urllib.parse.unquote(deeplink))

    def filter_and_report_new_tpa_data(self, deep_link_kwargs):
        if not deep_link_kwargs:
            return
        else:
            for tpa_type, keys in six.iteritems(ThridPartyAppManifest):
                this_app_modified_data_dict = None
                for key in keys:
                    if key in deep_link_kwargs:
                        param_val = deep_link_kwargs.get(key)
                        if this_app_modified_data_dict is None:
                            this_app_modified_data_dict = {}
                        this_app_modified_data_dict[key] = param_val

                if this_app_modified_data_dict is not None:
                    self.call_server_method('report_third_party_app', (tpa_type, this_app_modified_data_dict))

            return

    def on_deeplink_rewake(self, deep_link_kwargs):
        if not deep_link_kwargs:
            return
        else:
            is_rees_deeplink = 'rees_id' in deep_link_kwargs
            if is_rees_deeplink:
                global_data.stale_tpa_launch_data.add(TPA_REES)
                tpa_match_type = deep_link_kwargs.get(TPA_PARAM_MATCH_TYPE, None)
                if isinstance(tpa_match_type, six.string_types) and tpa_match_type.isdigit():
                    tpa_match_type = int(tpa_match_type)
                    self.perform_rees_auto_match_check(tpa_match_type)
            return

    def check_rees_auto_match_by_launch(self):
        if TPA_REES in global_data.stale_tpa_launch_data:
            return
        else:
            tpa_launch_data = self._get_tpa_launch_data()
            if not tpa_launch_data:
                return
            rees_param_dict = tpa_launch_data.get(TPA_REES, {})
            tpa_match_type = rees_param_dict.get(TPA_PARAM_MATCH_TYPE, None)
            if isinstance(tpa_match_type, six.string_types) and tpa_match_type.isdigit():
                tpa_match_type = int(tpa_match_type)
                self.perform_rees_auto_match_check(tpa_match_type)
                global_data.stale_tpa_launch_data.add(TPA_REES)
            return

    def perform_rees_auto_match_check(self, tpa_match_type):
        if tpa_match_type is None:
            return
        else:
            battle_tid = third_part_app_utils.tpa_match_type_2_battle_tid(tpa_match_type)
            if battle_tid is None:
                log_error('Match type failed to convert.', tpa_match_type)
                return
            if self.is_in_battle():
                print('Already in battle.')
                return
            if self.is_matching:
                print('Already in match queue.')
                return
            if self.get_self_ready():
                print('Already ready.')
                return
            if self.is_in_team():
                print('Already in team.')
                return
            if self.is_in_room():
                print('Already in room.')
                return
            lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
            if not lobby_ui:
                print('lobby_ui not exists.')
                return
            match_wg = lobby_ui.match_widget
            if not match_wg:
                print('lobby_ui not exists.')
                return
            from logic.gcommon.common_utils import battle_utils
            play_type = battle_utils.get_play_type_by_battle_id(battle_tid)
            battle_type, team_num = battle_utils.get_type_and_mode_by_battle_id(battle_tid)
            from logic.comsys.lobby.MatchMode import MatchMode
            if not MatchMode.will_show_mode(play_type, team_num):
                print('Not shown in MatchMode.')
                return
            from logic.comsys.lobby.LobbyMatchWidget import LobbyMatchWidget
            if not battle_utils.check_can_ready(battle_tid) or not LobbyMatchWidget.can_match(play_type, team_num):
                log_error('Failed ready common check.', tpa_match_type)
                return
            auto_flag = global_data.player.get_battle_auto_match()
            self.select_battle_tid(battle_tid)
            match_wg.update_battle_tid(battle_tid)
            self.get_ready(True, battle_tid, auto_flag)
            return

    def _get_tpa_launch_data(self):
        tpa_launch_data = global_data.tpa_launch_data
        return tpa_launch_data