# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/PlayerHistoryRecordsWidget.py
from __future__ import absolute_import
import six_ex
from six.moves import range
import six
from .PlayerTabBaseWidget import PlayerTabBaseWidget
from logic.comsys.battle.MutiOccupy.MutiOccupyEndStatisticsShareUI import MutiOccupyStatisticsShareUI
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import role_head_utils
from logic.gcommon.cdata import dan_data
from logic.gcommon.common_const import battle_const
import json
from common.cfg import confmgr
from logic.gutils import season_utils
from datetime import datetime
from logic.gcommon import time_utility
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.common_const.ui_operation_const import REVEAL_HISTORY_RECORD_DEFAULT
from logic.gutils.observe_utils import LiveObserveUIHelper
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from logic.gcommon.common_const.pve_const import DIFFICULTY_TEXT_LIST, DIFFICULTY_COLOR_LIST
from logic.gcommon.common_utils.text_utils import get_color_str
from logic.gcommon.item.item_const import FASHION_POS_SUIT
RANK_TEXT_MAP = {'1': '80330',
   'draw': '81105',
   '2': '81106',
   '3': '81105'
   }
TEAM_COUNT_MAP = {1: '2148',
   2: '2149',
   3: '2150'
   }
ICON_MECHA_PATH = 'gui/ui_res_2/role/icon_mech_{}.png'

class PlayerHistoryRecordsWidget(PlayerTabBaseWidget):
    PANEL_CONFIG_NAME = 'role/i_role_battle_historic_records'
    NORMAL_TYPE = 0
    PVE_TYPE = 1

    def __init__(self, panel):
        super(PlayerHistoryRecordsWidget, self).__init__(panel)
        self._init_params()
        self._init_event()
        self._init_history_record_bar()

    def _init_params(self):
        self.tab_widgets = {}
        self.tab_list = [{'type': self.NORMAL_TYPE,'text': 83515,'widget_func': self.init_normal_history_record,'template': 'role/i_role_battle_historic_records_list_normal'}, {'type': self.PVE_TYPE,'text': 83361,'widget_func': self.init_pve_history_record,'template': 'role/i_role_battle_historic_records_list_pve'}]
        self._panel_scroll = None
        self._panel_scroll_pve = None
        self._cur_type = None
        self.cur_uid = None
        self._battle_conf = confmgr.get('battle_config')
        self._reveal_his = REVEAL_HISTORY_RECORD_DEFAULT
        self._request_his_ever = False
        self.panel.lab_desc.setVisible(False)
        self.last_fight_record = None
        return

    def _init_event(self):
        global_data.emgr.message_on_player_history_game_result += self._on_recv_history_result
        global_data.emgr.on_close_end_share_ui += self._on_close_end_share_ui
        global_data.emgr.on_recover_player_info_ui += self.show_cached_history_record
        global_data.message_data.request_history_game_result(global_data.player.uid)

        @self.panel.btn_question.callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_local_content(10364), get_text_local_content(10363))

    def _init_history_record_bar(self):

        def init_history_record_btn(node, data):
            node.btn_tab.SetText(get_text_by_id(data.get('text', '')))

        def history_record_btn_click_cb(ui_item, data, index):
            self._cur_type = data.get('type')
            if index in self.tab_widgets:
                for _index in self.tab_widgets:
                    widget = self.tab_widgets[_index]
                    widget.setVisible(index == _index)

            else:
                template = data.get('template')
                _nd = global_data.uisystem.load_template_create(template, self.panel.nd_list_1)
                _nd.SetPosition('50%', '50%')
                widget_func = data.get('widget_func')
                widget_func(_nd)
                self.tab_widgets[index] = _nd
                for _index in self.tab_widgets:
                    cur_widget = self.tab_widgets[_index]
                    cur_widget.setVisible(index == _index)

        list_tab = self.panel.pnl_list_top_tab
        self._history_record_bar_wrapper = WindowTopSingleSelectListHelper()
        self._history_record_bar_wrapper.set_up_list(list_tab, self.tab_list, init_history_record_btn, history_record_btn_click_cb)
        default_type = self.NORMAL_TYPE
        ui = global_data.ui_mgr.get_ui('PVEMainUI')
        if ui:
            default_type = self.PVE_TYPE
        self._history_record_bar_wrapper.set_node_click(list_tab.GetItem(default_type))

    def init_normal_history_record(self, _nd):
        self._list_history = _nd
        self._panel_scroll = self._list_history.list_historic_pve
        self._on_recv_history_result(self.cur_uid)

    def init_pve_history_record(self, _nd):
        self._list_history_pve = _nd
        self._panel_scroll_pve = self._list_history_pve.list_historic_pve
        self._on_recv_history_result(self.cur_uid)

    def _refresh_pve_list(self, data, reveal_his):
        self._panel_scroll_pve.DeleteAllSubItem()
        for elem_data in data:
            self.add_pve_item(elem_data)

        nd_empty_visible = False if data else True
        nd_empty = self._list_history_pve.nd_empty
        nd_empty.setVisible(nd_empty_visible)
        nd_empty.lab_empty.setVisible(not reveal_his)

    def add_pve_item(self, elem_data):
        game_type = int(elem_data.get('game_type', '0'))
        battle_info = self._battle_conf.get(str(game_type))
        if not battle_info:
            return
        else:
            panel = self._panel_scroll_pve.AddTemplateItem(bRefresh=True)
            my_battle_data = {}
            teammate_settle_dict = {}
            member_results = elem_data.get('member_results', [])
            for member in member_results:
                if isinstance(member, (six.text_type, str)):
                    member = json.loads(member)
                if not isinstance(member, dict):
                    member = {}
                extra_detail = member.get('extra_detail', {})
                if isinstance(extra_detail, (six.text_type, str)):
                    extra_detail = json.loads(extra_detail)
                if not isinstance(extra_detail, dict):
                    extra_detail = {}
                settle_dict = {}
                settle_dict['head_photo'] = member.get('head_photo', None)
                settle_dict['head_frame'] = member.get('head_frame', None)
                settle_dict['role_name'] = member.get('role_name', '')
                settle_dict['mecha_id'] = int(extra_detail.get('selected_mecha', 8001))
                settle_dict['chossed_breakthrough'] = extra_detail.get('chossed_breakthrough', {})
                settle_dict['choosed_blesses'] = extra_detail.get('choosed_blesses', {})
                settle_dict['pve_mecha_base_info'] = extra_detail.get('pve_mecha_base_info', {})
                settle_dict['buy_item_cnt'] = extra_detail.get('buy_item_cnt', {})
                settle_dict['statistics'] = {}
                settle_dict['statistics']['survival'] = float(extra_detail.get('total_survival_time', member.get('survival_time', 0)))
                settle_dict['statistics']['kill_monster'] = int(extra_detail.get('kill_monster', 0))
                settle_dict['statistics']['total_damage'] = extra_detail.get('damage', 0)
                settle_dict['statistics']['pve_element_damage'] = extra_detail.get('pve_element_damage', {})
                teammate_settle_dict[member.get('role_id')] = settle_dict
                if member.get('role_id') == str(self.cur_uid):
                    my_battle_data = member

            extra_detail = my_battle_data.get('extra_detail', {})
            if isinstance(extra_detail, (six.text_type, str)):
                extra_detail = json.loads(extra_detail)
            if not isinstance(extra_detail, dict):
                extra_detail = {}
            rank = my_battle_data.get('game_rank', 0)
            is_win = rank == 1
            panel.img_win.setVisible(is_win)
            panel.img_lose.setVisible(not is_win)
            difficulty = extra_detail.get('difficulty', 1)
            difficulty_str = get_color_str(DIFFICULTY_COLOR_LIST[difficulty], get_text_by_id(DIFFICULTY_TEXT_LIST[difficulty]))
            panel.lab_difficulty.setString(difficulty_str)
            time_text = ''
            game_time_ts = elem_data.get('game_time_ts', None)
            if game_time_ts is not None:
                time_text = time_utility.get_server_time_str_from_ts(game_time_ts)
            else:
                time_str = elem_data.get('game_time', '')
                if isinstance(time_str, float) or isinstance(time_str, int):
                    time_text = time_utility.get_server_time_str_from_ts(time_str)
                elif isinstance(time_str, (six.text_type, str)):
                    if time_str:
                        time_text = time_str[0:-3]
                else:
                    time_text = ''
            panel.lab_date.setString(time_text)
            mecha_id = int(extra_detail.get('selected_mecha', 8001))
            panel.img_mech.SetDisplayFrameByPath('', ICON_MECHA_PATH.format(mecha_id))
            chapter = str(extra_detail.get('chapter', 1))
            end_level = extra_detail.get('end_level', 1)
            conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content', chapter)
            panel.lab_level.setString('{}:{}-{}'.format(get_text_by_id(conf.get('title_text')), chapter, end_level))
            survival_time = float(extra_detail.get('total_survival_time', my_battle_data.get('survival_time', 0)))
            clear_time_str = time_utility.get_delta_time_str(survival_time)
            panel.lab_time.setString('{}:{}'.format(get_text_by_id(393), clear_time_str))
            kill_monster = int(extra_detail.get('kill_monster', 0))
            panel.lab_kill.setString('{}:{}'.format(get_text_by_id(395), str(kill_monster)))

            @panel.callback()
            def OnClick(btn, touch):
                if global_data.player and str(self.cur_uid) == str(global_data.player.uid) or global_data.enable_history_share:
                    settle_dict = {}
                    settle_dict['rank'] = rank
                    settle_dict['mecha_id'] = mecha_id
                    settle_dict['difficulty'] = difficulty
                    settle_dict['normal_level_score'] = extra_detail.get('normal_level_score', 0)
                    settle_dict['elite_level_score'] = extra_detail.get('elite_level_score', 0)
                    settle_dict['boss_level_score'] = extra_detail.get('boss_level_score', 0)
                    settle_dict['mecha_fashion'] = extra_detail.get('mecha_fashion', {FASHION_POS_SUIT: 201800100})
                    settle_dict['chossed_breakthrough'] = extra_detail.get('chossed_breakthrough', {})
                    settle_dict['choosed_blesses'] = extra_detail.get('choosed_blesses', {})
                    settle_dict['buy_item_cnt'] = extra_detail.get('buy_item_cnt', {})
                    settle_dict['extra_detail'] = {}
                    settle_dict['extra_detail']['chapter'] = chapter
                    settle_dict['extra_detail']['end_level'] = end_level
                    settle_dict['statistics'] = {}
                    settle_dict['statistics']['survival'] = survival_time
                    settle_dict['statistics']['kill_monster'] = kill_monster
                    settle_dict['statistics']['total_damage'] = extra_detail.get('damage', 0)
                    settle_dict['statistics']['pve_element_damage'] = extra_detail.get('pve_element_damage', {})
                    from logic.comsys.battle.pve.PVEEndStatisticsUI import PVEEndStatisticsUI
                    PVEEndStatisticsUI(settle_dict=settle_dict, teammate_settle_dict=teammate_settle_dict)

            return

    def filter_pve_game_types(self, data, in_game_type_list):
        filtered_data = []
        for elem_data in data:
            game_type = int(elem_data.get('game_type', '0'))
            if game_type in in_game_type_list:
                filtered_data.append(elem_data)

        return filtered_data

    def on_select(self, player_inf):
        self.on_refresh_player_detail_inf(player_inf)

    def on_reset_states(self):
        self._request_his_ever = False

    def update_cur_uid(self, uid):
        self.cur_uid = uid

    def _request_his_result(self):
        global_data.message_data.request_history_game_result(self.cur_uid)
        self._request_his_ever = True

    def _on_close_end_share_ui(self):
        self.last_fight_record = None
        return

    def show_cached_history_record(self):
        if not self.last_fight_record:
            return
        elem_data, game_result_info = self.last_fight_record
        self.show_share_ui(elem_data, game_result_info=game_result_info)

    def on_refresh_player_detail_inf(self, player_inf):
        from common.const.property_const import DETAIL_INFO_REVEAL_HIS_REC_ID, U_ID
        if not global_data.player or not player_inf:
            return
        else:
            self.cur_uid = player_inf[U_ID]
            if self.cur_uid == global_data.player.uid:
                reveal_his = True
            else:
                val = player_inf.get(DETAIL_INFO_REVEAL_HIS_REC_ID, None)
                if val:
                    from logic.entities.avatarmembers.impUserSetting import deserialize_setting_2_val
                    reveal_his = deserialize_setting_2_val(val)
                    if not isinstance(reveal_his, bool):
                        reveal_his = REVEAL_HISTORY_RECORD_DEFAULT
                else:
                    reveal_his = REVEAL_HISTORY_RECORD_DEFAULT
            self._reveal_his = reveal_his
            if reveal_his:
                if not self._request_his_ever:
                    self._request_his_result()
            else:
                self._refresh_list([], False)
            return

    def _refresh_list(self, data, reveal_his):
        if not self._panel_scroll:
            return
        self._panel_scroll.DeleteAllSubItem()
        for elem_data in data:
            self.add_item(elem_data)

        nd_empty_visible = False if data else True
        nd_empty = self._list_history.nd_empty
        nd_empty.setVisible(nd_empty_visible)
        nd_empty.lab_empty.setVisible(not reveal_his)

    def _on_recv_history_result(self, uid):
        if uid != self.cur_uid:
            return
        history_data = global_data.message_data.get_history_game_result(self.cur_uid)
        data = history_data.get('data', [])
        if self._cur_type == self.NORMAL_TYPE:
            data = self.filter_game_types(data, [battle_const.KIZUNA_AI_CONCERT_TID, battle_const.DEFAULT_PVE_TID])
            self._refresh_list(data, self._reveal_his)
        elif self._cur_type == self.PVE_TYPE:
            data = self.filter_pve_game_types(data, [battle_const.DEFAULT_PVE_TID])
            self._refresh_pve_list(data, self._reveal_his)

    def filter_game_types(self, data, out_game_type_list):
        filtered_data = []
        for elem_data in data:
            game_type = int(elem_data.get('game_type', '0'))
            if game_type not in out_game_type_list:
                filtered_data.append(elem_data)

        return filtered_data

    def add_item(self, elem_data):
        game_type = int(elem_data.get('game_type', '0'))
        battle_info = self._battle_conf.get(str(game_type))
        if not battle_info:
            return
        else:
            panel = self._panel_scroll.AddTemplateItem(bRefresh=True)
            my_battle_data = {}
            member_results = elem_data.get('member_results', [])
            for member in member_results:
                if member.get('role_id') == str(self.cur_uid):
                    my_battle_data = member
                    break

            game_type_text_id = battle_info.get('cNameTID', None)
            cSettleShowMap = battle_info.get('cSettleShowMap', None)
            team_count_text_id = TEAM_COUNT_MAP.get(battle_info.get('cTeamNum', 1), None)
            team_count_text = None
            if team_count_text_id:
                team_count_text = get_text_by_id(team_count_text_id)
                if battle_info.get('bSupportCustom', 0) > 0:
                    team_count_text += '-' + get_text_by_id(80634)
            play_type = battle_info.get('play_type', 0)
            from logic.gcommon.common_utils import battle_utils
            bp_child_play_type = battle_utils.get_bp_child_play_type(game_type, elem_data.get('map_id'))
            if bp_child_play_type and bp_child_play_type > 0:
                play_type = bp_child_play_type
            if elem_data.get('map_id'):
                map_config = confmgr.get('map_config', str(elem_data.get('map_id')), default={})
                game_type_text_id_from_map = map_config.get('nameTID')
                if game_type_text_id_from_map:
                    game_type_text_id = game_type_text_id_from_map
            if game_type_text_id:
                panel.lab_game_mode.SetString(get_text_by_id(game_type_text_id))
            else:
                panel.lab_game_mode.setVisible(False)
            extra_detail = my_battle_data.get('extra_detail', {})
            if isinstance(extra_detail, (six.text_type, str)):
                extra_detail = json.loads(extra_detail)
            if not isinstance(extra_detail, dict):
                extra_detail = {}
            room_name = extra_detail.get('room_name', '')
            is_competition = extra_detail.get('is_competition', False)
            if is_competition and room_name:
                panel.lab_time_and_number.setString(room_name)
            elif team_count_text and not cSettleShowMap:
                panel.lab_time_and_number.setString(team_count_text)
            elif 'map_id' in elem_data and 'map_area_id' in elem_data:
                elem_data['battle_type'] = game_type
                battle_params = LiveObserveUIHelper.get_battle_params(elem_data)
                map_mode_text_id = battle_params['cMapModeTextId']
                game_text_id = battle_params['nameTID']
                panel.lab_game_mode.SetString(get_text_by_id(game_text_id))
                panel.lab_time_and_number.setString(get_text_by_id(map_mode_text_id))
            else:
                panel.lab_time_and_number.setVisible(False)
            game_rank = my_battle_data.get('game_rank', 100)
            is_escape = my_battle_data.get('is_escape', False)
            is_draw = elem_data.get('is_draw', 0) or 0
            is_draw = int(is_draw) > 0
            is_lore = elem_data.get('is_lore', False)
            mvp = my_battle_data.get('mvp', False)
            if isinstance(mvp, (six.text_type, str)):
                mvp = mvp == 'true'
            panel.img_mvp.setVisible(mvp)
            is_nbomb_exploded = extra_detail.get('is_nbomb_exploded', False)
            panel.nd_mode.setVisible(is_nbomb_exploded)
            game_result_info = {'game_rank': game_rank,'is_escape': is_escape,'is_draw': is_draw,'is_lore': is_lore}
            panel.img_win.setVisible(False)

            def hide_upper_left_tags():
                panel.img_champions.setVisible(False)
                panel.img_ten.setVisible(False)
                panel.img_win.setVisible(False)
                panel.img_draw.setVisible(False)
                panel.img_lose.setVisible(False)
                panel.img_win.setVisible(False)

            if is_escape:
                if play_type in (battle_const.PLAY_TYPE_ASSAULT,):
                    hide_upper_left_tags()
                else:
                    panel.img_escape.setVisible(True)
                    panel.img_champions.setVisible(False)
                    panel.img_ten.setVisible(False)
                    panel.lab_escape.setString(get_text_by_id(80740))
            else:
                panel.img_escape.setVisible(False)
                if play_type in (battle_const.PLAY_TYPE_ZOMBIEFFA, battle_const.PLAY_TYPE_ASSAULT):
                    hide_upper_left_tags()
                elif play_type == battle_const.PLAY_TYPE_CHICKEN:
                    panel.img_mvp.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_tdm/img_mvp_3.png')
                    if game_rank == 1:
                        panel.img_champions.setVisible(True)
                        panel.img_ten.setVisible(False)
                        panel.lab_title.setString(get_text_by_id(10235))
                        panel.img_mvp.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_tdm/img_mvp_4.png')
                    elif game_rank <= 10:
                        panel.img_ten.setVisible(True)
                        panel.img_champions.setVisible(False)
                        panel.lab_ten.setString(get_text_by_id(80283))
                    else:
                        panel.img_champions.setVisible(False)
                        panel.img_ten.setVisible(False)
                elif play_type in battle_const.PLAY_TYPE_TDMS:
                    panel.img_mvp.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_tdm/img_mvp_3.png')
                    hide_upper_left_tags()
                    if is_draw:
                        panel.img_draw.setVisible(True)
                    elif game_rank == 1:
                        panel.img_win.setVisible(True)
                        panel.img_mvp.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_tdm/img_mvp_4.png')
                    else:
                        panel.img_lose.setVisible(True)
                elif not is_draw and game_rank == 1:
                    panel.img_champions.setVisible(True)
                    panel.img_ten.setVisible(False)
                    panel.lab_title.setString(get_text_by_id(10235))
                    panel.img_mvp.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_tdm/img_mvp_4.png')
                else:
                    panel.img_champions.setVisible(False)
                    panel.img_ten.setVisible(False)
                    panel.img_mvp.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_tdm/img_mvp_3.png')
                if not G_IS_NA_PROJECT and play_type in battle_const.PLAY_TYPE_SURVIVALS and 1 < game_rank <= 5:
                    panel.img_win.setVisible(True)
                    panel.img_champions.setVisible(False)
                    panel.img_ten.setVisible(False)
                    panel.img_mvp.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_tdm/img_mvp_3.png')
            if play_type in battle_const.PLAY_TYPE_TDMS:
                if play_type == battle_const.PLAY_TYPE_ASSAULT:
                    text_id = ''
                    if my_battle_data and extra_detail:
                        group_point_dict = my_battle_data.get('group_points_dict', {})
                        if isinstance(group_point_dict, str):
                            group_point_dict = json.loads(group_point_dict)
                        if not isinstance(group_point_dict, dict):
                            group_point_dict = {}
                        my_group_id = elem_data.get('team_guid', 1)
                        my_group_id = extra_detail.get('group_id', my_group_id)
                        other_group_id = 0
                        other_group_point = 0
                        my_group_point = 0
                        for group_id, group_point in six.iteritems(group_point_dict):
                            if group_id == str(my_group_id):
                                my_group_point = group_point
                            else:
                                other_group_point = group_point
                                other_group_id = group_id

                        group_info = extra_detail.get('group_info', {}).get(str(my_group_id), {})
                        other_group_info = extra_detail.get('group_info', {}).get(str(other_group_id), {})
                        my_soul_id = group_info.get(str(self.cur_uid), 0)
                        if not my_soul_id:
                            self_group_info = extra_detail.get('join_score_dict', {}).keys()
                            my_soul_id = [ x for x in self_group_info if x not in group_info.values() and x not in other_group_info.values() ]
                            if my_soul_id:
                                my_soul_id = my_soul_id[0]
                            else:
                                my_soul_id = 0
                        join_score = extra_detail.get('join_score_dict', {}).get(str(my_soul_id), {})
                        for group_id, group_point in six.iteritems(join_score):
                            if group_id == str(my_group_id):
                                my_group_point -= group_point
                            else:
                                other_group_point -= group_point

                        if other_group_point > my_group_point:
                            text_id = RANK_TEXT_MAP.get('2')
                        elif other_group_point == my_group_point:
                            text_id = RANK_TEXT_MAP.get('3')
                        else:
                            text_id = RANK_TEXT_MAP.get('1')
                    if text_id:
                        rank_text = get_text_by_id(text_id)
                    else:
                        rank_text = ''
                else:
                    if is_draw:
                        text_id = RANK_TEXT_MAP.get('draw')
                    else:
                        text_id = RANK_TEXT_MAP.get(str(int(game_rank)), '')
                    if text_id:
                        rank_text = get_text_by_id(text_id)
                    else:
                        rank_text = ''
            elif play_type in (battle_const.PLAY_TYPE_ZOMBIEFFA,):
                if is_draw:
                    text_id = RANK_TEXT_MAP.get('draw')
                else:
                    text_id = RANK_TEXT_MAP.get('1') if elem_data.get('is_win', False) else RANK_TEXT_MAP.get('2')
                rank_text = get_text_by_id(text_id) if text_id else ''
            else:
                rank_text = str(int(game_rank))
            panel.lab_ranking.setString(rank_text)
            mecha_ids = my_battle_data.get('mecha_ids', [])
            if isinstance(mecha_ids, (six.text_type, str)):
                mecha_ids = json.loads(mecha_ids)
            if play_type in [battle_const.PLAY_TYPE_GVG, battle_const.PLAY_TYPE_DUEL]:
                if mecha_ids and len(mecha_ids) > 0:
                    for i in range(3):
                        _node_name = 'img_mech_' + str(i + 1)
                        _node = getattr(panel, _node_name, None)
                        if not _node:
                            continue
                        if i >= len(mecha_ids):
                            _node.setVisible(False)
                            continue
                        mecha_id = mecha_ids[i]
                        _node.setVisible(True)
                        res_path = 'gui/ui_res_2/role/icon_mech_%s.png' % mecha_id
                        _node.SetDisplayFrameByPath('', res_path)

                    panel.img_mech.setVisible(False)
                    panel.nd_3mech.setVisible(True)
                    panel.nd_mech_head.setVisible(True)
                    panel.nd_mech_head_no.setVisible(False)
                else:
                    panel.nd_mech_head.setVisible(False)
                    panel.nd_mech_head_no.setVisible(True)
            else:
                mecha_id = ''
                leng = len(mecha_ids) if mecha_ids else 0
                if leng > 0:
                    if play_type == battle_const.PLAY_TYPE_ZOMBIEFFA:
                        mecha_id = mecha_ids[leng - 1]
                    else:
                        mecha_id = mecha_ids[-1]
                if mecha_id and mecha_id != u'0':
                    res_path = 'gui/ui_res_2/role/icon_mech_%s.png' % mecha_id
                    panel.img_mech.SetDisplayFrameByPath('', res_path)
                    panel.img_mech.setVisible(True)
                    panel.nd_3mech.setVisible(False)
                    panel.nd_mech_head.setVisible(True)
                    panel.nd_mech_head_no.setVisible(False)
                else:
                    panel.nd_mech_head.setVisible(False)
                    panel.nd_mech_head_no.setVisible(True)
            if play_type in [battle_const.PLAY_TYPE_GVG, battle_const.PLAY_TYPE_DUEL]:
                panel.lab_kill.setVisible(False)
            else:
                panel.lab_kill.setVisible(True)
                panel.lab_kill.setString(str(int(my_battle_data.get('kill_human', 0))))
            panel.lab_destroy.setString(str(int(my_battle_data.get('kill_mecha', 0))))
            time_text = ''
            time_ts = elem_data.get('game_time_ts', None)
            if time_ts is not None:
                time_text = time_utility.get_server_time_str_from_ts(time_ts)
            else:
                time_str = elem_data.get('game_time', '')
                if isinstance(time_str, float) or isinstance(time_str, int):
                    time_text = time_utility.get_server_time_str_from_ts(time_str)
                elif isinstance(time_str, (six.text_type, str)):
                    if time_str:
                        time_text = time_str[0:-3]
                else:
                    time_text = ''
            panel.lab_date.setString(time_text)
            my_dan = my_battle_data.get('dan_info', {})
            if isinstance(my_dan, (six.text_type, str)):
                my_dan = json.loads(my_dan)
            survival_dan = my_dan.get('survival_dan', {})
            add_league_point = my_battle_data.get('add_league_point', 0)
            star_change = my_battle_data.get('star_change', 0) or 0
            league_text_ex = ''
            star_text_ex = ''
            if add_league_point > 0:
                league_text_ex = '+'
            if star_change > 0:
                star_text_ex = '+'
            panel.lab_tier_and_score.SetString(season_utils.get_dan_lv_name(survival_dan.get('dan', dan_data.BROZE), lv=survival_dan.get('lv', dan_data.get_lv_num(dan_data.BROZE))))
            panel.lab_score.SetString('%s:%d<color=0xff831aff>(%s%d)#N' % (get_text_by_id(608009), int(survival_dan.get('league_point', 0)), league_text_ex, int(add_league_point)))
            panel.lab_star.SetString('%d<color=0xff831aff>(%s%d)#N' % (int(survival_dan.get('star', 0)), star_text_ex, int(star_change)))
            role_head_utils.set_role_dan(panel.temp_tier, my_dan)

            @panel.callback()
            def OnClick(btn, touch):
                if global_data.player and str(self.cur_uid) == str(global_data.player.uid) or global_data.enable_history_share:
                    self.show_share_ui(elem_data, game_result_info=game_result_info)
                    self.last_fight_record = [elem_data, game_result_info]

            return panel

    def destroy(self):
        global_data.emgr.message_on_player_history_game_result -= self._on_recv_history_result
        self._battle_conf = None
        super(PlayerHistoryRecordsWidget, self).destroy()
        return

    def convert_game_end_time_str_to_ts(self, game_end_time_str):
        if isinstance(game_end_time_str, int) or isinstance(game_end_time_str, float):
            return game_end_time_str
        else:
            try:
                game_end_dt = datetime.strptime(game_end_time_str, '%Y-%m-%d %H:%M:%S')
                epoch_dt = datetime(1970, 1, 1)
                delta = game_end_dt - epoch_dt
                game_end_ts = delta.total_seconds()
                game_end_ts = game_end_ts - time_utility.ONE_HOUR_SECONS * 8
                return game_end_ts
            except Exception as e:
                log_error(e)
                return None

            return None

    def show_share_ui(self, data, **kwargs):
        game_type = int(data.get('game_type', '4'))
        from logic.gcommon.common_utils import battle_utils
        from logic.gcommon.common_const import battle_const
        play_type = battle_utils.get_play_type_by_battle_id(game_type)
        bp_child_play_type = battle_utils.get_bp_child_play_type(game_type, data.get('map_id'))
        if bp_child_play_type and bp_child_play_type > 0:
            play_type = bp_child_play_type
        if play_type in [battle_const.PLAY_TYPE_CHICKEN, battle_const.PLAY_TYPE_CHICKEN_FAST]:
            self.init_normal_share_ui(data)
        elif play_type == battle_const.PLAY_TYPE_GOOSEBEAR:
            self.init_goosebear_share_ui(data)
        elif play_type == battle_const.PLAY_TYPE_CONTROL:
            self.init_occupy_share_ui(data)
        elif play_type == battle_const.PLAY_TYPE_FLAG or play_type == battle_const.PLAY_TYPE_FLAG2:
            self.init_flag_share_ui(data)
        elif play_type == battle_const.PLAY_TYPE_MUTIOCCUPY:
            self.init_mutioccupy_share_ui(data)
        elif play_type == battle_const.PLAY_TYPE_TRAIN:
            self.init_train_share_ui(data)
        elif play_type == battle_const.PLAY_TYPE_ASSAULT:
            self.init_assault_share_ui(data)
        elif play_type in battle_const.PLAY_TYPE_DEATH_LIKE:
            if play_type == battle_const.PLAY_TYPE_CRYSTAL:
                self.init_crystal_share_ui(data)
            elif play_type == battle_const.PLAY_TYPE_ADCRYSTAL:
                self.init_adcrystal_share_ui(data)
            else:
                self.init_death_share_ui(data)
        elif play_type == battle_const.PLAY_TYPE_FFA:
            pass
        elif play_type in [battle_const.PLAY_TYPE_GVG, battle_const.PLAY_TYPE_DUEL]:
            self.init_gvg_share_ui(data, **kwargs)
        elif play_type == battle_const.PLAY_TYPE_IMPROVISE:
            self.init_improvise_share_ui(data, **kwargs)
        elif play_type == battle_const.PLAY_TYPE_ARMRACE:
            self.init_armrace_share_ui(data)
        elif play_type == battle_const.PLAY_TYPE_SNATCHEGG:
            self.init_snatchegg_share_ui(data)

    def init_normal_share_ui(self, data):
        is_new_format_data = False
        from logic.gcommon.common_const import statistics_const as sconst
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        game_type = int(data.get('game_type', 4))
        member_results = data.get('member_results', [])
        team_member_num = len(member_results)
        total_fighter_num = 99
        groupmate_info = {}
        team_settle_info = {}
        achievement_dict = {}
        player_info = {}
        for idx, mem_res in enumerate(member_results):
            eid = mem_res.get('role_id', None)
            team_settle_info[eid] = {}
            head_frame = mem_res.get('head_frame', '30100049')
            char_name = mem_res.get('role_name', '')
            statistics = {}
            survive_time = mem_res.get('survival_time', 0)
            kill_mecha = mem_res.get('kill_mecha', 0)
            kill_human = mem_res.get('kill_human', 0)
            damage = mem_res.get('damage', None)
            if damage is None or damage < 0:
                is_new_format_data = False
                global_data.game_mgr.show_tip(get_text_by_id(10347))
                return
            damage = int(damage)
            mecha_damage = 0
            human_damage = damage
            rank = mem_res.get('game_rank', 99)
            statistics[sconst.KILL_MECHA] = int(kill_mecha)
            statistics[sconst.KILL_HUMAN] = int(kill_human)
            statistics[sconst.HUMAN_DAMAGE] = human_damage
            statistics[sconst.MECHA_DAMAGE] = mecha_damage
            statistics[sconst.SURVIVAL_TIME] = survive_time
            team_settle_info[eid]['rank'] = int(rank)
            team_settle_info[eid]['statistics'] = statistics
            inner_total_fighter_num = mem_res.get('total_fighter_num', None)
            if inner_total_fighter_num is not None:
                total_fighter_num = int(inner_total_fighter_num)
            achievement_store = mem_res.get('achievement', [])
            if isinstance(achievement_store, (six.text_type, str)):
                achievement_store = json.loads(achievement_store)
            achievement_dict[eid] = achievement_store
            if eid == str(self.cur_uid):
                mecha_ids = mem_res.get('mecha_ids', [])
                fashion = mem_res.get('fashion', {})
                if isinstance(fashion, (six.text_type, str)):
                    fashion = json.loads(fashion)
                if fashion is None or type(fashion) is int and fashion < 0:
                    global_data.game_mgr.show_tip(get_text_by_id(10347))
                    return
                if isinstance(mecha_ids, (six.text_type, str)):
                    mecha_ids = json.loads(mecha_ids)
                mecha_id = ''
                if mecha_ids and len(mecha_ids) > 0:
                    mecha_id = int(mecha_ids[0])
                role = mem_res.get('role', '11')
                player_info = {'eid': eid,
                   'role_id': role,
                   'clothing_id': fashion.get(FASHION_POS_SUIT, None),
                   'mecha_id': mecha_id,
                   'head_frame': head_frame,
                   'char_name': char_name
                   }
            else:
                role = mem_res.get('role', '11')
                groupmate_info[eid] = {'head_frame': head_frame,
                   'role_id': role,
                   'char_name': char_name
                   }

        game_info = self.gen_game_info_from_history_data(data)
        from logic.comsys.battle.Settle.EndStatisticsShareUI import EndStatisticsShareUI
        global_data.ui_mgr.show_ui('KothEndFullScreenBg', 'logic.comsys.battle.Settle')
        EndStatisticsShareUI(None, team_settle_info, team_member_num, groupmate_info, achievement_dict, total_fighter_num, player_info, game_info)
        return

    def parse_my_group_entity_data(self, mem_res):
        eid = mem_res.get('role_id', None)
        char_name = mem_res.get('role_name', '')
        kill_mecha = int(mem_res.get('kill_mecha', 0))
        kill_human = int(mem_res.get('kill_human', 0))
        score_lv = 0
        self_id = None
        head_photo = mem_res.get('head_photo')
        head_frame = mem_res.get('head_frame', '30100049')
        role = mem_res.get('role', None)
        mvp = mem_res.get('mvp', False)
        if isinstance(mvp, (six.text_type, str)):
            mvp = mvp == 'true'
        is_mvp = mem_res.get('is_mvp', False) or mvp
        mecha_ids = mem_res.get('mecha_ids', [])
        if isinstance(mecha_ids, (six.text_type, str)):
            mecha_ids = json.loads(mecha_ids)
        mecha_id = ''
        if mecha_ids and len(mecha_ids) > 0:
            mecha_id = int(mecha_ids[-1])
        from logic.gutils.role_head_utils import get_role_default_photo, get_mecha_photo
        t_photo = get_mecha_photo(mecha_id)
        if not mecha_id:
            t_photo = get_role_default_photo(mem_res.get('role'))
        group_share = mem_res.get('group_share', [[0, 0], [0, 0], [0, 0]])
        if isinstance(group_share, (six.text_type, str)):
            group_share = json.loads(group_share)
        group_share = self.check_integer_data_format(group_share)
        score = mem_res.get('score', {})
        if isinstance(score, (six.text_type, str)):
            score = json.loads(score)
        score_point = self.check_integer_data_format(score.get('score', 0))
        assist_human = int(mem_res.get('assist_human', 0))
        assist_mecha = int(mem_res.get('assist_mecha', 0))
        control_point_time = mem_res.get('control_point_time', 0)
        plant_flag_score = mem_res.get('plant_flag_score', 0)
        extra_detail = mem_res.get('extra_detail', {})
        if isinstance(extra_detail, (six.text_type, str)):
            extra_detail = json.loads(extra_detail)
        extra_point = extra_detail.get('extra_points', 0)
        occupy_points = mem_res.get('occupy_personal_score', 0)
        train_push_dis = extra_detail.get('train_push_dis', 0)
        return (
         eid, char_name, kill_human, kill_mecha, score_lv, t_photo, head_frame, self_id, is_mvp, score_point,
         group_share, assist_human, assist_mecha, control_point_time, plant_flag_score, extra_point, occupy_points, train_push_dis, mecha_id, role)

    def parse_enemy_group_entity_data(self, mem_res):
        eid = mem_res.get('uid')
        char_name = mem_res.get('char_name', '')
        stat = mem_res.get('statistics', {})
        kill_mecha = int(stat.get('kill_mecha', 0))
        kill_human = int(stat.get('kill', 0))
        score_lv = 0
        self_id = None
        head_photo = mem_res.get('head_photo')
        head_frame = mem_res.get('head_frame', '30100049')
        role_id = mem_res.get('role_id')
        mvp = mem_res.get('mvp', False)
        if isinstance(mvp, (six.text_type, str)):
            mvp = mvp == 'true'
        is_mvp = mem_res.get('is_mvp', False) or mvp
        mecha_id = mem_res.get('mecha_id', 0)
        from logic.gutils.role_head_utils import get_role_default_photo, get_mecha_photo
        t_photo = get_mecha_photo(mecha_id)
        if not mecha_id:
            t_photo = get_role_default_photo(mem_res.get('role_id'))
        group_share = mem_res.get('group_share', [[0, 0], [0, 0], [0, 0]])
        if isinstance(group_share, (six.text_type, str)):
            group_share = json.loads(group_share)
        group_share = self.check_integer_data_format(group_share)
        settle_score = mem_res.get('settle_score', {})
        score_point = self.check_integer_data_format(settle_score.get('score', 0))
        assist_human = int(stat.get('assist_human', 0))
        assist_mecha = int(stat.get('assist_mecha', 0))
        control_point_time = mem_res.get('control_point_time', 0)
        plant_flag_score = mem_res.get('plant_flag_score', 0)
        extra_detail = mem_res.get('extra_detail', {})
        if isinstance(extra_detail, (six.text_type, str)):
            extra_detail = json.loads(extra_detail)
        extra_point = extra_detail.get('extra_points', 0)
        occupy_points = mem_res.get('occupy_personal_score', 0)
        train_push_dis = extra_detail.get('train_push_dis', 0)
        return (
         eid, char_name, kill_human, kill_mecha, score_lv, t_photo, head_frame, self_id, is_mvp, score_point,
         group_share, assist_human, assist_mecha, control_point_time, plant_flag_score, extra_point, occupy_points, train_push_dis, mecha_id, role_id)

    def init_death_share_ui(self, data):
        member_results = data.get('member_results', [])
        my_group_id = data.get('team_guid', 2)
        last_point_got_interval = data.get('last_point_got_interval', 9999)
        if last_point_got_interval is None:
            last_point_got_interval = 9999
        group_point_dict = {}
        enemy_results = []
        is_surrender = False
        if len(member_results) >= 1:
            enemy_results = member_results[0].get('enemy_info', None)
            if isinstance(enemy_results, (six.text_type, str)):
                enemy_results = json.loads(enemy_results)
            if enemy_results is None or last_point_got_interval < 0:
                global_data.game_mgr.show_tip(get_text_by_id(10347))
                return
            group_point_dict = member_results[0].get('group_points_dict', {})
            if isinstance(group_point_dict, (six.text_type, str)):
                group_point_dict = json.loads(group_point_dict)
            extra_detail = member_results[0].get('extra_detail', {})
            if isinstance(extra_detail, (six.text_type, str)):
                extra_detail = json.loads(extra_detail)
            is_surrender = extra_detail.get('is_surrender', False)
        my_group_list = []
        other_group_list = []
        settle_reason = data.get('settle_reason')
        settle_dict = {'my_group_id': my_group_id,'group_points_dict': group_point_dict,'is_surrender': is_surrender,'settle_reason': settle_reason,
           'last_point_got_interval': self.check_integer_data_format(last_point_got_interval)}
        for idx, mem_res in enumerate(member_results):
            our_group_info = self.parse_my_group_entity_data(mem_res)
            my_group_list.append(our_group_info)

        for mem_res in six.itervalues(enemy_results):
            our_group_info = self.parse_enemy_group_entity_data(mem_res)
            other_group_list.append(our_group_info)

        game_info = self.gen_game_info_from_history_data(data)
        game_type = int(data.get('game_type', '4'))
        play_type = battle_utils.get_play_type_by_battle_id(game_type)
        from logic.comsys.battle.MechaDeath.MechaDeathEndStatisticsShareUI import MechaDeathEndStatisticsShareUI
        from logic.comsys.battle.Death.DeathEndStatisticsShareUI import DeathStatisticsShareUI
        from logic.comsys.battle.Crown.CrownEndStatisticsShareUI import CrownStatisticsShareUI
        from logic.comsys.battle.Hunting.HuntingEndStatisticsShareUI import HuntingStatisticsShareUI
        from logic.comsys.battle.Settle.DeathEndTransitionUI import DeathEndTransitionUI
        from logic.comsys.battle.Crystal.CrystalEndStatisticsShareUI import CrystalEndStatisticsShareUI
        from logic.comsys.battle.ADCrystal.ADCrystalEndStatisticsShareUI import ADCrystalEndStatisticsShareUI
        from logic.comsys.battle.Train.TrainEndStatisticsShareUI import TrainEndStatisticsShareUI
        DeathEndTransitionUI()
        if play_type == battle_const.PLAY_TYPE_MECHA_DEATH:
            MechaDeathEndStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
        elif play_type == battle_const.PLAY_TYPE_CROWN:
            CrownStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
        elif play_type == battle_const.PLAY_TYPE_HUNTING:
            HuntingStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
        elif play_type == battle_const.PLAY_TYPE_CRYSTAL:
            CrystalEndStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
        elif play_type == battle_const.PLAY_TYPE_ADCRYSTAL:
            ADCrystalEndStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
        elif play_type == battle_const.PLAY_TYPE_TRAIN:
            TrainEndStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
        else:
            DeathStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
        return

    def init_flag_share_ui(self, data):
        member_results = data.get('member_results', [])
        my_group_id = data.get('team_guid', 2)
        last_point_got_interval = data.get('last_point_got_interval', 9999)
        if last_point_got_interval is None:
            last_point_got_interval = 9999
        group_point_dict = {}
        enemy_results = []
        if len(member_results) >= 1:
            enemy_results = member_results[0].get('enemy_info', None)
            if isinstance(enemy_results, (six.text_type, str)):
                enemy_results = json.loads(enemy_results)
            if enemy_results is None or last_point_got_interval < 0:
                global_data.game_mgr.show_tip(get_text_by_id(10347))
                return
            group_point_dict = member_results[0].get('group_points_dict', {})
            if isinstance(group_point_dict, (six.text_type, str)):
                group_point_dict = json.loads(group_point_dict)
        my_group_list = []
        other_group_list = []
        settle_reason = data.get('settle_reason')
        settle_dict = {'my_group_id': my_group_id,'group_points_dict': group_point_dict,'settle_reason': settle_reason,
           'last_point_got_interval': self.check_integer_data_format(last_point_got_interval)}
        for idx, mem_res in enumerate(member_results):
            our_group_info = self.parse_my_group_entity_data(mem_res)
            my_group_list.append(our_group_info)

        for mem_res in six.itervalues(enemy_results):
            our_group_info = self.parse_enemy_group_entity_data(mem_res)
            other_group_list.append(our_group_info)

        game_info = self.gen_game_info_from_history_data(data)
        game_type = int(data.get('game_type', '4'))
        play_type = battle_utils.get_play_type_by_battle_id(game_type)
        from logic.comsys.battle.MechaDeath.MechaDeathEndStatisticsShareUI import MechaDeathEndStatisticsShareUI
        from logic.comsys.battle.Death.FlagEndStatisticsShareUI import FlagStatisticsShareUI
        from logic.comsys.battle.Settle.DeathEndTransitionUI import DeathEndTransitionUI
        DeathEndTransitionUI()
        FlagStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
        return

    def init_occupy_share_ui(self, data):
        member_results = data.get('member_results', [])
        my_group_id = data.get('team_guid', 2)
        last_point_got_interval = data.get('last_point_got_interval', 9999)
        if last_point_got_interval is None:
            last_point_got_interval = 9999
        group_point_dict = {}
        enemy_results = []
        is_surrender = False
        if len(member_results) >= 1:
            enemy_results = member_results[0].get('enemy_info', None)
            if isinstance(enemy_results, (six.text_type, str)):
                enemy_results = json.loads(enemy_results)
            if enemy_results is None or last_point_got_interval < 0:
                global_data.game_mgr.show_tip(get_text_by_id(10347))
                return
            group_point_dict = member_results[0].get('group_points_dict', {})
            if isinstance(group_point_dict, (six.text_type, str)):
                group_point_dict = json.loads(group_point_dict)
            extra_detail = member_results[0].get('extra_detail', {})
            if isinstance(extra_detail, (six.text_type, str)):
                extra_detail = json.loads(extra_detail)
            is_surrender = extra_detail.get('is_surrender', False)
        my_group_list = []
        other_group_list = []
        settle_reason = data.get('settle_reason')
        settle_dict = {'my_group_id': my_group_id,'group_points_dict': group_point_dict,'settle_reason': settle_reason,
           'last_point_got_interval': self.check_integer_data_format(last_point_got_interval),
           'is_surrender': is_surrender
           }
        for idx, mem_res in enumerate(member_results):
            our_group_info = self.parse_my_group_entity_data(mem_res)
            my_group_list.append(our_group_info)

        for mem_res in six.itervalues(enemy_results):
            our_group_info = self.parse_enemy_group_entity_data(mem_res)
            other_group_list.append(our_group_info)

        game_info = self.gen_game_info_from_history_data(data)
        from logic.comsys.battle.Occupy.OccupyEndStatisticsShareUI import OccupyStatisticsShareUI
        from logic.comsys.battle.Settle.DeathEndTransitionUI import DeathEndTransitionUI
        DeathEndTransitionUI()
        OccupyStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
        return

    def init_ffa_share_ui(self, data):
        ok, group_rank_data = self._check_ffa_detail_data(data)
        if not ok:
            return
        else:
            game_info = self.gen_game_info_from_history_data(data)
            from logic.comsys.battle.Settle.DeathEndTransitionUI import DeathEndTransitionUI
            DeathEndTransitionUI()
            from logic.comsys.battle.ffa.FFAStatisticsShareUI import FFAStatisticsShareUI
            FFAStatisticsShareUI(None, group_rank_data, self.cur_uid, game_info)
            return

    def init_armrace_share_ui(self, data):
        ok, group_rank_data, armrace_max_lv = self._check_armrace_detail_data(data)
        if not ok:
            return
        else:
            game_info = self.gen_game_info_from_history_data(data)
            from logic.comsys.battle.Settle.DeathEndTransitionUI import DeathEndTransitionUI
            DeathEndTransitionUI()
            from logic.comsys.battle.ArmRace.ArmRaceStatisticsShareUI import ArmRaceStatisticsShareUI
            ArmRaceStatisticsShareUI(None, group_rank_data, self.cur_uid, game_info, armrace_max_lv)
            return

    def init_gvg_share_ui(self, data, **kwargs):
        ok, group_point_dict = self._check_group_points_dict(data)
        if not ok:
            return
        else:
            ok, settle_detail = self._check_gvg_settle_detail(data)
            if not ok:
                return
            reason = data.get('settle_reason', battle_const.BATTLE_SETTLE_REASON_NORMAL)
            my_group_id = data.get('team_guid', 1)
            game_info = self.gen_game_info_from_history_data(data)
            game_result_info = kwargs.get('game_result_info', {})
            member_results = data.get('member_results', [])
            extra_detail = member_results[0].get('extra_detail', {})
            if isinstance(extra_detail, (six.text_type, str)):
                extra_detail = json.loads(extra_detail)
            game_type = int(data.get('game_type', '4'))
            play_type = battle_utils.get_play_type_by_battle_id(game_type)
            if play_type == battle_const.PLAY_TYPE_DUEL:
                game_info['extra_detail'] = extra_detail
            from logic.comsys.battle.Settle.DeathEndTransitionUI import DeathEndTransitionUI
            DeathEndTransitionUI()
            from logic.comsys.battle.gvg.GVGStatisticsShareUI import GVGStatisticsShareUI
            GVGStatisticsShareUI(None, settle_detail, group_point_dict, reason, game_result_info, my_group_id, self.cur_uid, game_info)
            return

    def init_improvise_share_ui(self, data, **kwargs):
        ok, group_point_dict = self._check_group_points_dict(data)
        if not ok:
            return
        else:
            settle_detail = data.get('settle_detail', None)
            ok, settle_detail = self._check_settle_detail(data, (
             int, six.string_types, int, int, int, int, int, None, None, bool))
            if not ok:
                return
            my_group_id = data.get('team_guid', 1)
            game_info = self.gen_game_info_from_history_data(data)
            game_result_info = kwargs.get('game_result_info', {})
            from logic.comsys.battle.Settle.DeathEndTransitionUI import DeathEndTransitionUI
            DeathEndTransitionUI()
            from logic.comsys.battle.Improvise.ImproviseHistoryStatUI import ImproviseHistoryStatUI
            ImproviseHistoryStatUI(None, settle_detail, group_point_dict, game_result_info, my_group_id, self.cur_uid, game_info)
            return

    def init_crystal_share_ui(self, data):
        member_results = data.get('member_results', [])
        my_group_id = data.get('team_guid', 2)
        last_point_got_interval = data.get('last_point_got_interval', 9999)
        if last_point_got_interval is None:
            last_point_got_interval = 9999
        group_point_dict = {}
        enemy_results = []
        extra_detail = {}
        is_draw = False
        if len(member_results) >= 1:
            enemy_results = member_results[0].get('enemy_info', None)
            if isinstance(enemy_results, (six.text_type, str)):
                enemy_results = json.loads(enemy_results)
            if enemy_results is None or last_point_got_interval < 0:
                global_data.game_mgr.show_tip(get_text_by_id(10347))
                return
            group_point_dict = member_results[0].get('group_points_dict', {})
            if isinstance(group_point_dict, (six.text_type, str)):
                group_point_dict = json.loads(group_point_dict)
            extra_detail = member_results[0].get('extra_detail', {})
            if isinstance(extra_detail, (six.text_type, str)):
                extra_detail = json.loads(extra_detail)
            is_draw = member_results[0].get('is_draw')
        group_crystal_point_dict = extra_detail.get('group_crystal_point_dict', {})
        group_crystal_damage_dict = extra_detail.get('group_crystal_damage_dict', {})
        group_crystal_round = extra_detail.get('group_crystal_round', {})
        group_crystal_hp_percent = extra_detail.get('group_crystal_hp_percent', {})
        my_group_list = []
        other_group_list = []
        settle_reason = data.get('settle_reason')
        settle_dict = {'my_group_id': my_group_id,
           'group_points_dict': group_point_dict,
           'settle_reason': settle_reason,
           'group_crystal_point_dict': group_crystal_point_dict,
           'group_crystal_damage_dict': group_crystal_damage_dict,
           'group_crystal_round': group_crystal_round,
           'group_crystal_hp_percent': group_crystal_hp_percent,
           'is_draw': is_draw
           }
        for idx, mem_res in enumerate(member_results):
            our_group_info = self.parse_my_group_entity_data(mem_res)
            my_group_list.append(our_group_info)

        for mem_res in six.itervalues(enemy_results):
            our_group_info = self.parse_enemy_group_entity_data(mem_res)
            other_group_list.append(our_group_info)

        game_info = self.gen_game_info_from_history_data(data)
        from logic.comsys.battle.Settle.DeathEndTransitionUI import DeathEndTransitionUI
        from logic.comsys.battle.Crystal.CrystalEndStatisticsShareUI import CrystalEndStatisticsShareUI
        DeathEndTransitionUI()
        CrystalEndStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
        return

    def init_mutioccupy_share_ui(self, data):
        member_results = data.get('member_results', [])
        my_group_id = data.get('team_guid', 2)
        last_point_got_interval = data.get('last_point_got_interval', 9999)
        if last_point_got_interval is None:
            last_point_got_interval = 9999
        group_point_dict = {}
        enemy_results = []
        is_surrender = False
        if len(member_results) >= 1:
            enemy_results = member_results[0].get('enemy_info', None)
            if isinstance(enemy_results, (six.text_type, str)):
                enemy_results = json.loads(enemy_results)
            if enemy_results is None or last_point_got_interval < 0:
                global_data.game_mgr.show_tip(get_text_by_id(10347))
                return
            group_point_dict = member_results[0].get('group_points_dict', {})
            if isinstance(group_point_dict, (six.text_type, str)):
                group_point_dict = json.loads(group_point_dict)
            extra_detail = member_results[0].get('extra_detail', {})
            if isinstance(extra_detail, (six.text_type, str)):
                extra_detail = json.loads(extra_detail)
            is_surrender = extra_detail.get('is_surrender', False)
        my_group_list = []
        other_group_list = []
        settle_reason = data.get('settle_reason')
        settle_dict = {'my_group_id': my_group_id,'group_points_dict': group_point_dict,'settle_reason': settle_reason,
           'is_surrender': is_surrender,'last_point_got_interval': self.check_integer_data_format(last_point_got_interval)
           }
        for idx, mem_res in enumerate(member_results):
            our_group_info = self.parse_my_group_entity_data(mem_res)
            my_group_list.append(our_group_info)

        for mem_res in six.itervalues(enemy_results):
            our_group_info = self.parse_enemy_group_entity_data(mem_res)
            other_group_list.append(our_group_info)

        game_info = self.gen_game_info_from_history_data(data)
        from logic.comsys.battle.Occupy.OccupyEndStatisticsShareUI import OccupyStatisticsShareUI
        from logic.comsys.battle.Settle.DeathEndTransitionUI import DeathEndTransitionUI
        DeathEndTransitionUI()
        MutiOccupyStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
        return

    def init_adcrystal_share_ui(self, data):
        member_results = data.get('member_results', [])
        my_group_id = data.get('team_guid', 2)
        last_point_got_interval = data.get('last_point_got_interval', 9999)
        if last_point_got_interval is None:
            last_point_got_interval = 9999
        group_point_dict = {}
        enemy_results = []
        extra_detail = {}
        is_draw = False
        if len(member_results) >= 1:
            enemy_results = member_results[0].get('enemy_info', None)
            if isinstance(enemy_results, (six.text_type, str)):
                enemy_results = json.loads(enemy_results)
            if enemy_results is None or last_point_got_interval < 0:
                global_data.game_mgr.show_tip(get_text_by_id(10347))
                return
            group_point_dict = member_results[0].get('group_points_dict', {})
            if isinstance(group_point_dict, (six.text_type, str)):
                group_point_dict = json.loads(group_point_dict)
            extra_detail = member_results[0].get('extra_detail', {})
            if isinstance(extra_detail, (six.text_type, str)):
                extra_detail = json.loads(extra_detail)
            is_draw = member_results[0].get('is_draw')
        group_crystal_point_dict = extra_detail.get('group_crystal_point_dict', {})
        group_crystal_damage_dict = extra_detail.get('group_crystal_damage_dict', {})
        group_crystal_hp_percent = extra_detail.get('group_crystal_hp_percent', {})
        group_left_time_dict = extra_detail.get('group_left_time_dict', {})
        early_settle_flag = extra_detail.get('early_settle_flag')
        my_group_list = []
        other_group_list = []
        settle_reason = data.get('settle_reason')
        settle_dict = {'my_group_id': my_group_id,
           'group_points_dict': group_point_dict,
           'settle_reason': settle_reason,
           'group_crystal_point_dict': group_crystal_point_dict,
           'group_crystal_damage_dict': group_crystal_damage_dict,
           'group_crystal_hp_percent': group_crystal_hp_percent,
           'group_left_time_dict': group_left_time_dict,
           'is_draw': is_draw,
           'early_settle_flag': early_settle_flag
           }
        for idx, mem_res in enumerate(member_results):
            our_group_info = self.parse_my_group_entity_data(mem_res)
            my_group_list.append(our_group_info)

        for mem_res in six.itervalues(enemy_results):
            our_group_info = self.parse_enemy_group_entity_data(mem_res)
            other_group_list.append(our_group_info)

        game_info = self.gen_game_info_from_history_data(data)
        from logic.comsys.battle.Settle.DeathEndTransitionUI import DeathEndTransitionUI
        from logic.comsys.battle.ADCrystal.ADCrystalEndStatisticsShareUI import ADCrystalEndStatisticsShareUI
        DeathEndTransitionUI()
        ADCrystalEndStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
        return

    def init_train_share_ui(self, data):
        member_results = data.get('member_results', [])
        my_group_id = data.get('team_guid', 2)
        last_point_got_interval = data.get('last_point_got_interval', 9999)
        map_id = data.get('map_id', 99)
        map_area_id = data.get('map_area_id', 1)
        if last_point_got_interval is None:
            last_point_got_interval = 9999
        group_point_dict = {}
        enemy_results = []
        if len(member_results) >= 1:
            enemy_results = member_results[0].get('enemy_info', None)
            if isinstance(enemy_results, (six.text_type, str)):
                enemy_results = json.loads(enemy_results)
            if enemy_results is None or last_point_got_interval < 0:
                global_data.game_mgr.show_tip(get_text_by_id(10347))
                return
            group_point_dict = member_results[0].get('group_points_dict', {})
            extra_detail = member_results[0].get('extra_detail', {})
            if isinstance(extra_detail, (six.text_type, str)):
                extra_detail = json.loads(extra_detail)
            if isinstance(group_point_dict, (six.text_type, str)):
                group_point_dict = json.loads(group_point_dict)
            round_res_time = extra_detail.get('round_res_time', {})
        my_group_list = []
        other_group_list = []
        settle_reason = data.get('settle_reason')
        settle_dict = {'map_id': map_id,
           'map_area_id': map_area_id,
           'my_group_id': my_group_id,
           'group_points_dict': group_point_dict,
           'settle_reason': settle_reason,
           'last_point_got_interval': self.check_integer_data_format(last_point_got_interval),
           'round_res_time': round_res_time
           }
        for idx, mem_res in enumerate(member_results):
            our_group_info = self.parse_my_group_entity_data(mem_res)
            my_group_list.append(our_group_info)

        for mem_res in six.itervalues(enemy_results):
            our_group_info = self.parse_enemy_group_entity_data(mem_res)
            other_group_list.append(our_group_info)

        game_info = self.gen_game_info_from_history_data(data)
        from logic.comsys.battle.Train.TrainEndStatisticsShareUI import TrainEndStatisticsShareUI
        TrainEndStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
        return

    def init_snatchegg_share_ui(self, data):
        member_results = data.get('member_results', [])
        my_group_id = data.get('team_guid', 2)
        last_point_got_interval = data.get('last_point_got_interval', 9999)
        if last_point_got_interval is None:
            last_point_got_interval = 9999
        group_point_dict = {}
        my_group_list = []
        other_group_dict = {}
        enemy_results = []
        extra_detail = {}
        is_surrender = False
        if len(member_results) >= 1:
            enemy_results = member_results[0].get('enemy_info', None)
            if isinstance(enemy_results, (six.text_type, str)):
                enemy_results = json.loads(enemy_results)
            if enemy_results is None or last_point_got_interval < 0:
                global_data.game_mgr.show_tip(get_text_by_id(10347))
                return
            group_point_dict = member_results[0].get('group_points_dict', {})
            if isinstance(group_point_dict, (six.text_type, str)):
                group_point_dict = json.loads(group_point_dict)
            extra_detail = member_results[0].get('extra_detail', {})
            if isinstance(extra_detail, (six.text_type, str)):
                extra_detail = json.loads(extra_detail)
            is_surrender = extra_detail.get('is_surrender', False)
        settle_reason = data.get('settle_reason')
        settle_dict = {'my_group_id': my_group_id,'group_points_dict': group_point_dict,'is_surrender': is_surrender,'settle_reason': settle_reason,
           'extra_detail': extra_detail
           }
        for idx, mem_res in enumerate(member_results):
            our_group_info = self.parse_my_group_entity_data(mem_res)
            my_group_list.append(our_group_info)

        for key, mem_res in six.iteritems(enemy_results):
            our_group_info = self.parse_enemy_group_entity_data(mem_res)
            other_group_dict[key] = our_group_info

        game_info = self.gen_game_info_from_history_data(data)
        game_type = int(data.get('game_type', '4'))
        play_type = battle_utils.get_play_type_by_battle_id(game_type)
        from logic.comsys.battle.MechaDeath.MechaDeathEndStatisticsShareUI import MechaDeathEndStatisticsShareUI
        from logic.comsys.battle.SnatchEgg.GoldenEggEndStatisticsShareUI import GoldenEggEndStatisticsShareUI
        from logic.comsys.battle.Settle.DeathEndTransitionUI import DeathEndTransitionUI
        DeathEndTransitionUI()
        GoldenEggEndStatisticsShareUI(None, settle_dict, my_group_list, other_group_dict, self.cur_uid, game_info)
        return

    def init_goosebear_share_ui(self, data):
        member_results = data.get('member_results', [])
        my_group_id = data.get('team_guid', 2)
        last_point_got_interval = data.get('last_point_got_interval', 9999)
        if last_point_got_interval is None:
            last_point_got_interval = 9999
        group_point_dict = {}
        enemy_results = []
        is_surrender = False
        extra_detail = {}
        if len(member_results) >= 1:
            enemy_results = member_results[0].get('enemy_info', None)
            if isinstance(enemy_results, (six.text_type, str)):
                enemy_results = json.loads(enemy_results)
            if enemy_results is None or last_point_got_interval < 0:
                global_data.game_mgr.show_tip(get_text_by_id(10347))
                return
            group_point_dict = member_results[0].get('group_points_dict', {})
            if isinstance(group_point_dict, (six.text_type, str)):
                group_point_dict = json.loads(group_point_dict)
            extra_detail = member_results[0].get('extra_detail', {})
            if isinstance(extra_detail, (six.text_type, str)):
                extra_detail = json.loads(extra_detail)
            is_surrender = extra_detail.get('is_surrender', False)
        my_group_list = []
        other_group_list = []
        settle_reason = data.get('settle_reason')
        settle_dict = {'my_group_id': my_group_id,'group_points_dict': group_point_dict,'is_surrender': is_surrender,'settle_reason': settle_reason,
           'last_point_got_interval': self.check_integer_data_format(last_point_got_interval)
           }
        die_cnt = extra_detail.get('die_cnt', {})
        hit_rate_dict = extra_detail.get('hit_rate_dict', {})
        all_die_cnt = 0
        for idx, mem_res in enumerate(member_results):
            our_group_info = self.parse_my_group_entity_data(mem_res)
            tuid = mem_res.get('role_id')
            fire_hit, fire_cnt = hit_rate_dict.get(str(tuid), [{}, {}])
            mecha_hit = fire_hit.get('800502', 0) + fire_hit.get('802402', 0) + fire_hit.get('8024031', 0)
            all_fire_hit_cnt = fire_cnt.get('800502', 0) + fire_cnt.get('802402', 0) + fire_cnt.get('8024031', 0)
            t_die_cnt = die_cnt.get(str(tuid), 0)
            all_die_cnt += t_die_cnt
            our_group_info[10][1] = ['%d/%d' % (mecha_hit, all_fire_hit_cnt), 1.0 * mecha_hit / all_fire_hit_cnt if all_fire_hit_cnt else all_fire_hit_cnt]
            our_group_info[10][2] = [t_die_cnt, 0]
            my_group_list.append(our_group_info)

        for group in my_group_list:
            t_die_cnt, _ = group[10][2]
            if all_die_cnt:
                group[10][2][1] = 1.0 * t_die_cnt / all_die_cnt
            else:
                group[10][2][1] = 0.0

        all_die_cnt = 0
        for mem_res in six.itervalues(enemy_results):
            our_group_info = self.parse_enemy_group_entity_data(mem_res)
            tuid = mem_res.get('uid')
            fire_hit, fire_cnt = hit_rate_dict.get(str(tuid), [{}, {}])
            mecha_hit = fire_hit.get('800502', 0) + fire_hit.get('802402', 0) + fire_hit.get('8024031', 0)
            all_fire_hit_cnt = fire_cnt.get('800502', 0) + fire_cnt.get('802402', 0) + fire_cnt.get('8024031', 0)
            t_die_cnt = die_cnt.get(str(tuid), 0)
            all_die_cnt += t_die_cnt
            our_group_info[10][1] = ['%d/%d' % (mecha_hit, all_fire_hit_cnt), 1.0 * mecha_hit / all_fire_hit_cnt if all_fire_hit_cnt else all_fire_hit_cnt]
            our_group_info[10][2] = [t_die_cnt, 0]
            other_group_list.append(our_group_info)

        for group in other_group_list:
            t_die_cnt, _ = group[10][2]
            if all_die_cnt:
                group[10][2][1] = 1.0 * t_die_cnt / all_die_cnt
            else:
                group[10][2][1] = 0.0

        game_info = self.gen_game_info_from_history_data(data)
        from logic.comsys.battle.GooseBearHappyPush.GooseBearEndStatisticsShareUI import GooseBearEndStatisticsShareUI
        from logic.comsys.battle.Settle.DeathEndTransitionUI import DeathEndTransitionUI
        DeathEndTransitionUI()
        GooseBearEndStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
        return

    def init_assault_share_ui(self, data):
        member_results = data.get('member_results', [])
        my_group_id = data.get('team_guid', 2)
        last_point_got_interval = data.get('last_point_got_interval', 9999)
        if last_point_got_interval is None:
            last_point_got_interval = 9999
        group_point_dict = {}
        enemy_results = []
        is_surrender = False
        extra_detail = {}
        if len(member_results) >= 1:
            self_data = member_results[0]
            for mem_res in member_results:
                if str(mem_res.get('role_id', 0)) == str(self.cur_uid):
                    self_data = mem_res
                    break

            enemy_results = self_data.get('enemy_info', None)
            if isinstance(enemy_results, (six.text_type, str)):
                enemy_results = json.loads(enemy_results)
            if enemy_results is None or last_point_got_interval < 0:
                global_data.game_mgr.show_tip(get_text_by_id(10347))
                return
            group_point_dict = self_data.get('group_points_dict', {})
            if isinstance(group_point_dict, (six.text_type, str)):
                group_point_dict = json.loads(group_point_dict)
            extra_detail = self_data.get('extra_detail', {})
            if isinstance(extra_detail, (six.text_type, str)):
                extra_detail = json.loads(extra_detail)
            is_surrender = extra_detail.get('is_surrender', False)
        my_group_list = []
        other_group_list = []
        settle_reason = data.get('settle_reason')
        if extra_detail and not extra_detail.get('is_new_data'):
            return
        else:
            settle_dict = {'my_group_id': extra_detail.get('group_id', my_group_id),'group_points_dict': group_point_dict,
               'is_surrender': is_surrender,
               'settle_reason': settle_reason,
               'last_point_got_interval': self.check_integer_data_format(last_point_got_interval),
               'join_score_dict': extra_detail.get('join_score_dict', {}),
               'join_soul_dmg_dict': extra_detail.get('join_soul_dmg_dict', {}),
               'join_soul_score_dict': extra_detail.get('join_soul_score_dict', {}),
               'join_soul_assault_dict': extra_detail.get('join_soul_assault_dict', {}),
               'group_info': extra_detail.get('group_info', {})
               }
            teammate_info = extra_detail.get('teammate_info', {})
            if len(member_results) >= 1:
                my_group_list.append(self.parse_my_group_entity_data(self_data))
            for mem_res in six.itervalues(teammate_info):
                our_group_info = self.parse_enemy_group_entity_data(mem_res)
                my_group_list.append(our_group_info)

            for mem_res in six.itervalues(enemy_results):
                our_group_info = self.parse_enemy_group_entity_data(mem_res)
                other_group_list.append(our_group_info)

            game_info = self.gen_game_info_from_history_data(data)
            from logic.comsys.battle.Settle.DeathEndTransitionUI import DeathEndTransitionUI
            from logic.comsys.battle.Assault.AssaultEndStatisticsShareUI import AssaultEndStatisticsShareUI
            DeathEndTransitionUI()
            AssaultEndStatisticsShareUI(None, settle_dict, my_group_list, other_group_list, self.cur_uid, game_info)
            return

    def _history_data_assert(self, condition, log=None):
        if not condition:
            if log is None:
                log = 'history data assert failed.'
            raise ValueError(log)
        return

    def _check_settle_detail(self, data, indi_stat_type_specs):
        settle_detail = data.get('settle_detail', None)
        if settle_detail is None:
            return (False, None)
        else:
            try:
                if not isinstance(settle_detail, dict):
                    if not isinstance(settle_detail, (six.text_type, str)):
                        return (False, None)
                    settle_detail = json.loads(settle_detail)
                    if settle_detail is None or not isinstance(settle_detail, dict):
                        return (False, None)
                for group_id, group_settle_data in six.iteritems(settle_detail):
                    if not isinstance(group_id, six.string_types):
                        self._history_data_assert(False, 'key in settle_detail')
                    for eid, individual_settle_data in six.iteritems(group_settle_data):
                        if not isinstance(eid, six.string_types):
                            self._history_data_assert(False, 'key in settle_detail of group')
                        if len(individual_settle_data) != len(indi_stat_type_specs):
                            self._history_data_assert(False, 'size of individual_settle_data mismatch')
                        for i, type_spec in enumerate(indi_stat_type_specs):
                            if type_spec is None:
                                continue
                            val = individual_settle_data[i]
                            self._history_data_assert(isinstance(val, type_spec), 'value of idx %d in individual_settle_data' % i)

            except Exception as e:
                log_error(e)
                return (
                 False, None)

            return (True, settle_detail)

    def _check_group_points_dict(self, data):
        member_results = data.get('member_results', [])
        if len(member_results) >= 1:
            try:
                group_point_dict = member_results[0].get('group_points_dict', {})
                if isinstance(group_point_dict, (six.text_type, str)):
                    group_point_dict = json.loads(group_point_dict)
                return (True, group_point_dict)
            except Exception as e:
                log_error(e)
                return (
                 False, None)

        return (
         False, None)

    def _check_gvg_settle_detail(self, data):
        settle_detail = data.get('settle_detail', None)
        if settle_detail is None:
            return (False, None)
        else:
            try:
                if not isinstance(settle_detail, dict):
                    if not isinstance(settle_detail, (six.text_type, str)):
                        return (False, None)
                    settle_detail = json.loads(settle_detail)
                    if settle_detail is None or not isinstance(settle_detail, dict):
                        return (False, None)
                for group_id, group_settle_data in six.iteritems(settle_detail):
                    if not isinstance(group_id, (str, six.text_type)):
                        self._history_data_assert(False)
                    for eid, individual_settle_data in six.iteritems(group_settle_data):
                        individual_settle_data[6] = self._try_convert_to_number_type(individual_settle_data[6])
                        uid, name, head_frame, head_photo, kill_mecha, assist_mecha, score, mecha_data, mecha_dead_count = individual_settle_data
                        self._history_data_assert(isinstance(uid, int))
                        if not isinstance(name, (str, six.text_type)):
                            self._history_data_assert(False)
                        self._history_data_assert(isinstance(head_frame, int))
                        self._history_data_assert(isinstance(head_photo, int))
                        self._history_data_assert(isinstance(kill_mecha, int))
                        self._history_data_assert(isinstance(assist_mecha, int))
                        if not isinstance(score, (int, float)):
                            self._history_data_assert(False)
                        self._history_data_assert(isinstance(mecha_dead_count, int))
                        for mecha_id, damage, kill_num in mecha_data:
                            self._history_data_assert(isinstance(mecha_id, int))
                            self._history_data_assert(isinstance(damage, (int, float)), type(damage))
                            self._history_data_assert(isinstance(kill_num, int))

            except Exception as e:
                log_error(e)
                return (
                 False, None)

            return (True, settle_detail)

    def _try_convert_to_number_type(self, data):
        try:
            if isinstance(data, six.string_types):
                if '.' in data:
                    return float(data)
                else:
                    return int(data)

            else:
                return data
        except Exception as e:
            return data

    def _check_ffa_detail_data(self, data):
        if not data:
            return (False, None)
        else:
            try:
                group_rank_data = data.get('group_rank_data', None)
                if group_rank_data is None:
                    return (False, None)
                if not isinstance(group_rank_data, list):
                    if not isinstance(group_rank_data, (six.text_type, str)):
                        return (False, None)
                    group_rank_data = json.loads(group_rank_data)
                    if group_rank_data is None or not isinstance(group_rank_data, list):
                        return (False, None)
                for group_stat_data in group_rank_data:
                    rank, group_id, group_point, dict_data = group_stat_data
                    self._history_data_assert(isinstance(rank, int))
                    self._history_data_assert(isinstance(group_id, int))
                    self._history_data_assert(isinstance(group_point, int))
                    for e_index, eid in enumerate(six_ex.keys(dict_data)):
                        eid, uid, name, head_photo, head_frame, kill_num, kill_mecha_num, points, has_buff, mecha_id, human_damage, mecha_damage = dict_data[eid]
                        if isinstance(mecha_damage, float):
                            mecha_damage = int(mecha_damage)
                        if not isinstance(uid, int) and uid is not None:
                            self._history_data_assert(False)
                        if not isinstance(name, (str, six.text_type)):
                            self._history_data_assert(False)
                        self._history_data_assert(isinstance(head_photo, int))
                        self._history_data_assert(isinstance(head_frame, int))
                        self._history_data_assert(isinstance(kill_num, int))
                        self._history_data_assert(isinstance(kill_mecha_num, int))
                        self._history_data_assert(isinstance(points, int))
                        self._history_data_assert(isinstance(has_buff, bool))
                        self._history_data_assert(isinstance(mecha_id, int))
                        self._history_data_assert(isinstance(human_damage, int))
                        self._history_data_assert(isinstance(mecha_damage, int))

                return (
                 True, group_rank_data)
            except Exception as e:
                log_error(e)
                return (
                 False, None)

            return

    def _check_armrace_detail_data(self, data):
        if not data:
            return (False, None, None)
        else:
            try:
                group_rank_data = data.get('group_rank_data', None)
                armrace_max_lv = data.get('armrace_max_lv', 15)
                if group_rank_data is None:
                    return (False, None, None)
                if not isinstance(group_rank_data, list):
                    if not isinstance(group_rank_data, (six.text_type, str)):
                        return (False, None, None)
                    group_rank_data = json.loads(group_rank_data)
                    if group_rank_data is None or not isinstance(group_rank_data, list):
                        return (False, None, None)
                for group_stat_data in group_rank_data:
                    rank, group_id, group_point, dict_data = group_stat_data
                    self._history_data_assert(isinstance(rank, int))
                    self._history_data_assert(isinstance(group_id, int))
                    self._history_data_assert(isinstance(group_point, int))
                    for e_index, eid in enumerate(six_ex.keys(dict_data)):
                        eid, uid, name, armrace_lv, role_id, kill_num, kill_mecha_num, points, has_buff, human_damage, mecha_damage = dict_data[eid]
                        if not isinstance(uid, int) and uid is not None:
                            self._history_data_assert(False)
                        if not isinstance(name, (str, six.text_type)):
                            self._history_data_assert(False)
                        self._history_data_assert(isinstance(armrace_lv, int))
                        self._history_data_assert(isinstance(role_id, int))
                        self._history_data_assert(isinstance(kill_num, int))
                        self._history_data_assert(isinstance(kill_mecha_num, int))
                        self._history_data_assert(isinstance(points, int))
                        self._history_data_assert(isinstance(has_buff, bool))
                        self._history_data_assert(isinstance(human_damage, (int, float)))
                        self._history_data_assert(isinstance(mecha_damage, (int, float)))

                return (
                 True, group_rank_data, armrace_max_lv)
            except Exception as e:
                log_error(e)
                return (
                 False, None, None)

            return

    def check_integer_data_format(self, data):
        data_type = type(data)
        try:
            if data_type in [str, six.text_type]:
                if '.' in data:
                    return float(data)
                else:
                    return int(data)

            else:
                if data_type is list:
                    new_data = []
                    for idx, ele in enumerate(data):
                        new_data.append(self.check_integer_data_format(ele))

                    return new_data
                if data_type is type(None):
                    return -1
                return data
        except:
            return -1

        return

    def gen_game_info_from_history_data(self, data):
        if not data:
            return {}
        else:
            game_info = {}
            time_ts = data.get('game_time_ts', None)
            if time_ts is not None:
                game_info['game_end_ts'] = time_ts
            else:
                time_text = data.get('game_time', None)
                if time_text:
                    res = self.convert_game_end_time_str_to_ts(time_text)
                    if res:
                        game_info['game_end_ts'] = res
            game_id = data.get('fight_id', None)
            if game_id:
                game_info['game_id'] = game_id
            group_id = data.get('team_guid', None)
            if group_id:
                game_info['group_id'] = group_id
            battle_server_name = data.get('battle_server_name', None)
            if battle_server_name:
                game_info['battle_server_name'] = str(battle_server_name)
            game_type = data.get('game_type', None)
            if game_type:
                game_info['game_type'] = game_type
            return game_info