# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/observe_ui/JudgeObservationListWidget.py
from __future__ import absolute_import
import six_ex
from six.moves import range
import six
from functools import cmp_to_key
from common.utils.timer import CLOCK
OB_LIST_TYPE_NEARBY = 1
OB_LIST_TYPE_ALL_MAP = 2
from logic.comsys.common_ui.DeadSimpleTabList import DeadSimpleTabList
from logic.gutils import judge_utils
from logic.gcommon.common_utils import battle_utils
from logic.gutils.custom_ui_utils import get_cut_name
from logic.gcommon.common_const import mecha_const as mconst
from logic.client.const import game_mode_const

class JudgeObservationListWidget(object):

    def __init__(self, tab_list_node, team_list_node, on_camera_btn_click=None):
        super(JudgeObservationListWidget, self).__init__()
        self._tab_list_node = tab_list_node
        self._team_list_node = team_list_node
        self._team_list_node.SetItemSizeGetter(self._list_size_getter)
        self._on_camera_btn_click = on_camera_btn_click
        self._tab_data_list = (
         (
          OB_LIST_TYPE_NEARBY, 18023), (OB_LIST_TYPE_ALL_MAP, 19525))
        self.init_tab_list()
        self.process_event(True)
        self._team_ids = []
        self._nearby_team_info = {}
        self._pid_to_ui_node = {}
        self._click_start_pos = None
        self._nearby_view_refresher_timer = None
        if global_data.player:
            ob_list_type = global_data.player.get_ob_list_type()
        if ob_list_type is None:
            ob_list_type = OB_LIST_TYPE_NEARBY
        self._cur_ob_list_type = ob_list_type
        self.select_tab(ob_list_type)
        self._refresh_obing_mark(False)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'show_battle_report_event': self._on_show_battle_report,
           'judge_global_players_dead_state_changed': self._on_judge_global_players_dead_stage_changed,
           'ob_list_type_changed': self._on_ob_list_type_changed,
           'scene_observed_player_setted_event': self._on_switch_observe_target,
           'judge_cache_add_player': self._on_judge_cache_add_player,
           'judge_cache_player_dead': self._on_judge_cache_player_dead,
           'judge_global_player_bind_mecha_changed': self._on_judge_global_player_bind_mecha_changed,
           'judge_global_player_in_mecha_type_changed': self._on_judge_global_player_in_mecha_type_changed,
           'judge_global_player_mecha_cd_type_changed': self._on_judge_global_player_mecha_cd_type_changed,
           'judge_global_player_recall_cd_end_ts_changed': self._on_judge_global_player_recall_cd_left_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_show_battle_report(self, report_dict):
        self._refresh_list(self._cur_ob_list_type)

    def _on_judge_global_players_dead_stage_changed(self):
        self._refresh_list(self._cur_ob_list_type)

    def _on_switch_observe_target(self, observe_target):
        if self._cur_ob_list_type == OB_LIST_TYPE_NEARBY:
            self._nearby_view_refresher()
        self._refresh_obing_mark(True, observe_target.id if observe_target else None)
        return

    def _on_ob_list_type_changed(self, oldone, newone):
        self.select_tab(newone)

    def init_tab_list(self):

        def refresher(idx, tab_node, tab_data):
            tab_node.btn_tab.SetText(tab_data[1])

            def OnClick(btn, touch, idx):
                pass

            return (
             tab_node.btn_tab, OnClick)

        def on_selected(idx, tab_node):
            data = self._tab_data_list[idx]
            tab_type = data[0]
            self._cur_ob_list_type = tab_type
            if global_data.player:
                global_data.player.set_ob_list_type(tab_type)
            self._safely_stop_nearby_updater()
            if tab_type == OB_LIST_TYPE_ALL_MAP:
                self._refresh_list(OB_LIST_TYPE_ALL_MAP, change_tab=True)
            elif tab_type == OB_LIST_TYPE_NEARBY:
                self._nearby_view_refresher(change_tab=True)
                self._safely_stop_nearby_updater()
                self._start_nearby_updater()
            tab_node.btn_tab.SetSelect(True)

        def on_unselected(idx, tab_node):
            tab_node.btn_tab.SetSelect(False)

        self._tab_list_widget = DeadSimpleTabList(self._tab_list_node, refresher, on_selected, on_unselected)
        self._tab_list_widget.refresh(self._tab_data_list)

    def select_tab(self, tab_type):
        for i, val in enumerate(self._tab_data_list):
            if val[0] == tab_type:
                self._tab_list_widget.selectByIdx(i)
                break

    def _start_nearby_updater(self):
        self._safely_stop_nearby_updater()
        self._nearby_view_refresher_timer = global_data.game_mgr.register_logic_timer(func=self._nearby_view_refresher, times=-1, mode=CLOCK, interval=5)

    def _safely_stop_nearby_updater(self):
        if self._nearby_view_refresher_timer is not None:
            global_data.game_mgr.unregister_logic_timer(self._nearby_view_refresher_timer)
            self._nearby_view_refresher_timer = None
        return

    def _nearby_view_refresher(self, change_tab=False):
        self._refresh_list(OB_LIST_TYPE_NEARBY, change_tab)

    def _list_size_getter(self, idx, *args):
        team_data = self._get_team_info(self._team_ids[idx])
        team_size = len(team_data)
        return (
         440, float(50) * team_size)

    def _refresh_list(self, ob_list_type, change_tab=False):
        self._pid_to_ui_node = {}
        if ob_list_type == OB_LIST_TYPE_ALL_MAP:
            self._team_list_node.setVisible(True)
            self._update_all_map_team_data()
        elif ob_list_type == OB_LIST_TYPE_NEARBY:
            self._team_list_node.setVisible(True)
            self._update_nearby_team_data()
        else:
            self._team_list_node.setVisible(False)
        pos_before_adapt = self._team_list_node.GetContentOffset()
        first_time_populate = self._team_list_node.GetItemCount() == 0
        self._team_list_node.SetInitCount(len(self._team_ids))
        for idx, group_id in enumerate(self._team_ids):
            team_data = self._get_team_info(group_id)
            node = self._team_list_node.GetItem(idx)
            node.lab_team_no.SetString(str(group_id))
            node.img_team_bg.SetDisplayFrameByPath('', self.get_team_bg_img_path(group_id, False))
            team_size = len(team_data)
            node.pnl_team.SetInitCount(team_size)
            for j in range(team_size):
                pid = team_data[j]
                player_info = self._get_player_info(pid)
                player_info_node = node.pnl_team.GetItem(j)
                self._set_pid_to_ui_node(pid, player_info_node)
                char_name = player_info.get('char_name', '')
                player_info_node.lab_name.SetString(get_cut_name(six.text_type(char_name), 16))
                kill_player_num, kill_mecha_num = battle_utils.get_player_kill_num(pid)
                player_info_node.lab_kill_num.SetString(str(kill_player_num))
                player_info_node.lab_mech_num.SetString(str(kill_mecha_num))
                cur_ob_id = judge_utils.get_ob_target_id()
                player_info_node.nd_watching.setVisible(cur_ob_id is not None and cur_ob_id == pid)
                dead = judge_utils.is_player_dead_or_out(pid)
                player_info_node.nd_dead.setVisible(dead)
                self._refresh_mech_node(player_info_node.nd_mech, player_info.get('in_mecha_type', mconst.MECHA_TYPE_NONE) == mconst.MECHA_TYPE_NORMAL, player_info.get('mecha_id', 0), player_info.get('recall_cd_type', mconst.RECALL_CD_TYPE_NORMAL), player_info.get('recall_cd', 0), player_info.get('recall_cd_end_ts', 0))

                @player_info_node.btn_seat.unique_callback()
                def OnBegin(btn, touch):
                    wpos = touch.getLocation()
                    self._click_start_pos = self._tab_list_node.convertToNodeSpace(wpos)
                    return True

                player_info_node.btn_seat._my_secret_pid = pid

                @player_info_node.btn_seat.unique_callback()
                def OnClick(btn, touch):
                    wpos = touch.getLocation()
                    if not self._team_list_node.IsPointIn(wpos):
                        return
                    end_pos = self._tab_list_node.convertToNodeSpace(wpos)
                    if not self._click_start_pos:
                        return
                    dx = end_pos.x - self._click_start_pos.x
                    dy = end_pos.y - self._click_start_pos.y
                    if abs(dx) + abs(dy) > 0.05:
                        return
                    pid = btn._my_secret_pid
                    if judge_utils.is_player_dead_or_out(pid):
                        return
                    judge_utils.try_switch_ob_target(pid)

                @player_info_node.btn_watch.unique_callback()
                def OnClick(btn, touch):
                    if callable(self._on_camera_btn_click):
                        self._on_camera_btn_click()

            node.nd_team_num.ResizeAndPosition()

        if not first_time_populate:
            if change_tab:
                self._team_list_node.ScrollToTop()
            else:
                self._team_list_node.SetContentOffset(pos_before_adapt)
        else:
            self._team_list_node.ScrollToTop()
        return

    def _refresh_mech_node(self, mech_node, in_mecha, mecha_id, mecha_recall_cd_type, mecha_recall_cd, mecha_recall_cd_end_ts):
        show_cd = False
        if not mecha_id:
            show_mech_node = False
        elif in_mecha:
            show_mech_node = True
        else:
            show_mech_node = False
            if mecha_recall_cd_type == mconst.RECOVER_CD_TYPE_DISABLE:
                show_mech_node = True
            elif mecha_recall_cd_type == mconst.RECALL_CD_TYPE_NORMAL or mecha_recall_cd_type == mconst.RECALL_CD_TYPE_DIE:
                from logic.gcommon.time_utility import get_server_time_battle
                left_time = mecha_recall_cd_end_ts - get_server_time_battle()
                if left_time > 0:
                    show_mech_node = True
                    show_cd = True
        if show_mech_node:
            mech_node.setVisible(True)
            from logic.gcommon.common_const.battle_const import LOCATE_MECHA
            from logic.gutils.item_utils import get_locate_pic_path
            mech_node.img_mech.SetDisplayFrameByPath('', get_locate_pic_path(LOCATE_MECHA, None, mecha_id))
            mech_node.nd_ban.setVisible(mecha_recall_cd_type == mconst.RECOVER_CD_TYPE_DISABLE)
            if show_cd:
                mech_node.nd_cd.setVisible(True)

                def refresh_count_down(dt, _left_time=left_time):
                    if _left_time <= 0:
                        return
                    _left_time -= dt
                    if _left_time > 0:
                        mech_node.nd_cd.lab_cd.SetString('%.1f' % _left_time)
                    else:
                        self._refresh_mech_node(mech_node, in_mecha, mecha_id, mecha_recall_cd_type, mecha_recall_cd, 0)

                mech_node.nd_cd.StopTimerAction()
                mech_node.nd_cd.TimerAction(refresh_count_down, left_time, interval=0.05)
                refresh_count_down(0.0)
            else:
                mech_node.nd_cd.setVisible(False)
                mech_node.nd_cd.StopTimerAction()
        else:
            mech_node.setVisible(False)
        return

    def _get_team_info(self, group_id):
        if group_id is None:
            return []
        else:
            if self._cur_ob_list_type == OB_LIST_TYPE_ALL_MAP:
                return judge_utils.get_global_team_info(group_id)
            if self._cur_ob_list_type == OB_LIST_TYPE_NEARBY:
                return self._nearby_team_info.get(group_id, [])
            return judge_utils.get_global_team_info(group_id)
            return

    def _get_player_info(self, pid):
        if pid is None:
            return {}
        else:
            if self._cur_ob_list_type == OB_LIST_TYPE_ALL_MAP:
                return judge_utils.get_global_player_info(pid)
            if self._cur_ob_list_type == OB_LIST_TYPE_NEARBY:
                return judge_utils.get_global_player_info(pid)
            return judge_utils.get_global_player_info(pid)
            return

    def _on_judge_cache_add_player(self, pid):
        if self._cur_ob_list_type == OB_LIST_TYPE_ALL_MAP:
            if pid in self._pid_to_ui_node:
                return
            self._refresh_list(OB_LIST_TYPE_ALL_MAP)

    def _on_judge_cache_player_dead(self, pid, killer_id):
        ui_node = self._get_ui_node(pid)
        if ui_node and ui_node.isValid():
            ui_node.nd_dead.setVisible(True)

    def _on_judge_global_player_bind_mecha_changed(self, pid, mecha_id):
        ui_node = self._get_ui_node(pid)
        if ui_node and ui_node.isValid():
            player_info = self._get_player_info(pid)
            self._refresh_mech_node(ui_node.nd_mech, player_info.get('in_mecha_type', mconst.MECHA_TYPE_NONE) == mconst.MECHA_TYPE_NORMAL, mecha_id, player_info.get('recall_cd_type', mconst.RECALL_CD_TYPE_NORMAL), player_info.get('recall_cd', 0), player_info.get('recall_cd_end_ts', 0))

    def _on_judge_global_player_in_mecha_type_changed(self, pid, in_mecha_type):
        ui_node = self._get_ui_node(pid)
        if ui_node and ui_node.isValid():
            player_info = self._get_player_info(pid)
            self._refresh_mech_node(ui_node.nd_mech, in_mecha_type == mconst.MECHA_TYPE_NORMAL, player_info.get('mecha_id', 0), player_info.get('recall_cd_type', mconst.RECALL_CD_TYPE_NORMAL), player_info.get('recall_cd', 0), player_info.get('recall_cd_end_ts', 0))

    def _on_judge_global_player_mecha_cd_type_changed(self, pid, recall_cd_type):
        ui_node = self._get_ui_node(pid)
        if ui_node and ui_node.isValid():
            player_info = self._get_player_info(pid)
            self._refresh_mech_node(ui_node.nd_mech, player_info.get('in_mecha_type', mconst.MECHA_TYPE_NONE) == mconst.MECHA_TYPE_NORMAL, player_info.get('mecha_id', 0), recall_cd_type, player_info.get('recall_cd', 0), player_info.get('recall_cd_end_ts', 0))

    def _on_judge_global_player_recall_cd_left_changed(self, pid, left_time):
        ui_node = self._get_ui_node(pid)
        if ui_node and ui_node.isValid():
            player_info = self._get_player_info(pid)
            self._refresh_mech_node(ui_node.nd_mech, player_info.get('in_mecha_type', mconst.MECHA_TYPE_NONE) == mconst.MECHA_TYPE_NORMAL, player_info.get('mecha_id', 0), player_info.get('recall_cd_type', mconst.RECALL_CD_TYPE_NORMAL), player_info.get('recall_cd', 0), left_time)

    def _refresh_obing_mark(self, with_ob_target_id=False, ob_target_id=None):
        for group_node in self._team_list_node.GetAllItem():
            for player_node in group_node.pnl_team.GetAllItem():
                if not with_ob_target_id:
                    cur_ob_id = judge_utils.get_ob_target_id() if 1 else ob_target_id
                    player_node.nd_watching.setVisible(cur_ob_id is not None and cur_ob_id == player_node.btn_seat._my_secret_pid)

        return

    @staticmethod
    def get_team_bg_img_path--- This code section failed: ---

 379       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'game_mode'
           6  LOAD_ATTR             2  'is_mode_type'
           9  LOAD_GLOBAL           3  'game_mode_const'
          12  LOAD_ATTR             4  'GAME_MODE_GVG'
          15  LOAD_GLOBAL           3  'game_mode_const'
          18  LOAD_ATTR             5  'GAME_MODE_DUEL'
          21  BUILD_TUPLE_2         2 
          24  CALL_FUNCTION_1       1 
          27  POP_JUMP_IF_FALSE    71  'to 71'

 380      30  BUILD_MAP_2           2 
          33  LOAD_CONST            1  9
          36  LOAD_CONST            2  1
          39  STORE_MAP        
          40  LOAD_CONST            3  2
          43  LOAD_CONST            3  2
          46  STORE_MAP        
          47  STORE_FAST            2  'group_id_map'

 381      50  LOAD_FAST             2  'group_id_map'
          53  LOAD_ATTR             6  'get'
          56  LOAD_FAST             0  'group_id'
          59  LOAD_FAST             0  'group_id'
          62  CALL_FUNCTION_2       2 
          65  STORE_FAST            0  'group_id'
          68  JUMP_FORWARD          0  'to 71'
        71_0  COME_FROM                '68'

 383      71  JUMP_FORWARD          2  'to 76'
          74  BINARY_SUBTRACT  
          75  LOAD_CONST            4  20
          78  BINARY_MODULO    
          79  LOAD_CONST            2  1
          82  BINARY_ADD       
          83  STORE_FAST            3  'img_idx'

 384      86  LOAD_FAST             1  'circle'
          89  POP_JUMP_IF_FALSE   103  'to 103'

 385      92  LOAD_CONST            5  'gui/ui_res_2/observe/team_color_circle_%d.png'
          95  LOAD_FAST             3  'img_idx'
          98  BUILD_TUPLE_1         1 
         101  BINARY_MODULO    
         102  RETURN_END_IF    
       103_0  COME_FROM                '89'

 387     103  LOAD_CONST            6  'gui/ui_res_2/observe/team_color_cube_%d.png'
         106  LOAD_FAST             3  'img_idx'
         109  BUILD_TUPLE_1         1 
         112  BINARY_MODULO    
         113  RETURN_VALUE     

Parse error at or near `BINARY_SUBTRACT' instruction at offset 74

    def _update_all_map_team_data(self):
        self._team_ids = self._get_transformd_all_team_data()

    def _update_nearby_team_data(self):
        team_id_set = set()
        self._nearby_team_info = {}
        nearby_pids = judge_utils.get_readonly_nearby_pids()
        for pid in nearby_pids:
            player_info = judge_utils.get_global_player_info(pid)
            is_dead_or_out = player_info.get('is_dead_or_out', False)
            if is_dead_or_out:
                continue
            group_id = player_info.get('group', None)
            if group_id is None:
                continue
            team_id_set.add(group_id)
            if group_id not in self._nearby_team_info:
                self._nearby_team_info[group_id] = []
            self._nearby_team_info[group_id].append(pid)

        for group_id, pids in six.iteritems(self._nearby_team_info):
            pids.sort()

        team_ids = list(team_id_set)
        team_ids.sort()
        self._team_ids = team_ids
        return

    @staticmethod
    def all_team_sorter(a, b):
        if judge_utils.is_team_death(a) and not judge_utils.is_team_death(b):
            return 1
        if not judge_utils.is_team_death(a) and judge_utils.is_team_death(b):
            return -1
        return six_ex.compare(a, b)

    def _get_transformd_all_team_data(self):
        all_team_info = judge_utils.get_all_global_team_info()
        if not all_team_info:
            return []
        ret_team_ids = []
        for group_id in all_team_info:
            pids = all_team_info[group_id]
            if not pids:
                continue
            ret_team_ids.append(group_id)

        ret_team_ids.sort(key=cmp_to_key(self.all_team_sorter))
        return ret_team_ids

    def _set_pid_to_ui_node(self, pid, ui_node):
        self._pid_to_ui_node[pid] = ui_node

    def _get_ui_node(self, pid):
        return self._pid_to_ui_node.get(pid, None)

    def destroy(self):
        self.process_event(False)
        self._tab_list_widget.destroy()
        self._tab_list_widget = None
        self._safely_stop_nearby_updater()
        return