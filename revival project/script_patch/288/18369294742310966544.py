# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/TeamHall/TeamRecruitUI.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gcommon import const
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2, FASHION_OTHER_PENDANT_LIST
from logic.comsys.clan.ClanPageBase import ClanPageBase
from logic.gutils import lobby_model_display_utils
from logic.gutils import team_utils
from logic.gcommon import time_utility as tutil
from data import c_recruit_data
from logic.gcommon.common_const.log_const import TEAM_MODE_RECOMMEND
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from logic.gcommon.common_const.battle_const import DEFAULT_PVE_TID

class TeamRecruitUI(ClanPageBase):
    DELAY_TIME = 0.5
    DELAY_TAG = 20210316
    NORMAL_TYPE = 0
    PVE_TYPE = 1

    def __init__(self, dlg):
        self.global_events = {'refresh_recommend_teammates': self.refresh_recommend_teammates,
           'team_invite_count_down_event': self.update_team_button,
           'message_on_player_simple_inf': self.on_refresh_player_inf,
           'message_on_players_detail_inf': self.team_change,
           'player_join_team_event': self.team_change,
           'player_leave_team_event': self.team_change,
           'player_add_teammate_event': self.team_change,
           'player_del_teammate_event': self.team_change
           }
        super(TeamRecruitUI, self).__init__(dlg)

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        del_keys = []
        for key, cb in six.iteritems(self._timer_cb):
            result = cb()
            if result == -1:
                del_keys.append(key)

        for key in del_keys:
            del self._timer_cb[key]

        if not self._timer_cb:
            self.unregister_timer()

    def get_activity_time(self):
        player = global_data.player
        if not player or not self.fate_group_start or not self.fate_group_end:
            return (-1, -1)
        server_time = tutil.get_server_time()
        return (
         self.fate_group_start - server_time, self.fate_group_end - server_time)

    def refresh_activity_time(self):
        start_left_time, end_left_time = self.get_activity_time()
        self.panel.lab_tips.SetString(13102)
        if start_left_time > 0:
            self.panel.lab_remind.setVisible(False)
            self.panel.lab_date.setVisible(False)
        elif end_left_time > 0:
            self.panel.lab_date.SetString(get_text_by_id(607014).format(tutil.get_readable_time_day_hour_minitue(end_left_time)))
            self.refresh_fate_group_time()
            self.panel.lab_remind.setVisible(True)
            self.panel.lab_date.setVisible(True)
        else:
            self.panel.lab_remind.setVisible(False)
            self.panel.lab_date.setVisible(False)
            self.panel.lab_tips.SetString(13111)
            return -1

    def on_init_panel(self):
        super(TeamRecruitUI, self).on_init_panel()
        self._timer = 0
        self._timer_cb = {}
        self.friend_list = []
        fate_group_info = c_recruit_data.GetFateGroupConf()
        self.fate_group_start = fate_group_info.get('fate_group_start', {}).get('value')
        self.fate_group_end = fate_group_info.get('fate_group_end', {}).get('value')
        self._cur_type = self.NORMAL_TYPE
        self.tab_widgets = {}
        self.tab_list = [{'type': self.NORMAL_TYPE,'text': 83515,'widget_func': self.init_normal_recruit,'template': 'lobby/i_team_recruit_player_list_normal'}, {'type': self.PVE_TYPE,'text': 83361,'widget_func': self.init_pve_recruit,'template': 'lobby/i_team_recruit_player_list_pve'}]
        self._change_scene()
        self._timer_cb[0] = lambda : self.refresh_activity_time()
        self.refresh_activity_time()
        self.register_timer()
        self._init_recruit_bar()

        @self.panel.btn_quit.unique_callback()
        def OnClick(btn, touch):
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_local_content(13027), confirm_callback=lambda : global_data.player.req_leave_team())

        @self.panel.btn_refresh.unique_callback()
        def OnClick(btn, touch):
            self.request_recommend_teammates(show_tips=True)

        @self.panel.btn_invite_all.unique_callback()
        def OnClick(btn, touch):
            self.invite_all_people()

        @self.panel.btn_help.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(13112, 13113)

    def init_normal_recruit(self, nd):
        self._list_player = nd.list_player
        self.set_show(True)

    def init_pve_recruit(self, nd):
        self._list_pve_player = nd.list_player
        self.set_show(True)

    def _init_recruit_bar(self):

        def init_recruit_btn(node, data):
            node.btn_tab.SetText(get_text_by_id(data.get('text', '')))

        def recruit_btn_click_cb(ui_item, data, index):
            self._cur_type = index
            if index in self.tab_widgets:
                self.set_show(True)
                for _index in self.tab_widgets:
                    widget = self.tab_widgets[_index]
                    if index == _index:
                        widget.setVisible(True)
                    else:
                        widget.setVisible(False)

            else:
                template = data.get('template')
                _nd = global_data.uisystem.load_template_create(template, self.panel.nd_list)
                _nd.SetPosition('50%', '50%')
                widget_func = data.get('widget_func')
                widget_func(_nd)
                self.tab_widgets[index] = _nd
                for _index in self.tab_widgets:
                    cur_widget = self.tab_widgets[_index]
                    if index != _index:
                        cur_widget.setVisible(False)

        list_tab = self.panel.list_tab
        self._recruit_bar_wrapper = WindowTopSingleSelectListHelper()
        self._recruit_bar_wrapper.set_up_list(list_tab, self.tab_list, init_recruit_btn, recruit_btn_click_cb)
        default_type = self.NORMAL_TYPE
        ui = global_data.ui_mgr.get_ui('PVEMainUI')
        if ui:
            default_type = self.PVE_TYPE
        self._recruit_bar_wrapper.set_node_click(list_tab.GetItem(default_type))

    def _do_pve_show_model(self):
        if not global_data.player:
            return
        else:
            if not self.panel or not self.panel.isVisible():
                return
            models = []
            boxs = []
            support_mirror = []
            friend_list = global_data.player.get_pve_recommend_players()[:3]
            self.friend_list = friend_list
            self._list_pve_player.SetInitCount(len(friend_list))
            for i, data in enumerate(friend_list):
                node = self._list_pve_player.GetItem(i)
                team_utils.init_pve_teamate_info(node, data)
                fashion_data = data.get('role_fashion')
                role_item_no = fashion_data.get(FASHION_POS_SUIT, 201001100)
                role_head_no = fashion_data.get(FASHION_POS_HEADWEAR, None)
                bag_id = fashion_data.get(FASHION_POS_BACK, None)
                suit_id = fashion_data.get(FASHION_POS_SUIT_2, None)
                other_pendants = [ fashion_data.get(pos) for pos in FASHION_OTHER_PENDANT_LIST ]
                if role_item_no <= 0:
                    continue
                role_model_data = lobby_model_display_utils.get_lobby_model_data(role_item_no, head_id=role_head_no, bag_id=bag_id, suit_id=suit_id, other_pendants=other_pendants)
                for data in role_model_data:
                    data['model_scale'] = data.get('model_scale', 1.0) * 3
                    data['show_anim'] = data['end_anim'] or 'idle'

                models.append(role_model_data)
                boxs.append('box_role_%d' % (i + 1))
                support_mirror.append(True)

            if models:
                global_data.emgr.change_model_display_scene_item_customized.emit(models, boxs, support_mirror, create_callback=self._on_load_model_success)
            else:
                global_data.emgr.close_model_display_scene.emit()
            count_down_data = global_data.player.get_count_down()
            self.update_team_button(count_down_data)
            self.refresh_add_friend()
            self.refresh_team()
            return

    def _change_scene(self):
        from logic.gcommon.common_const import scene_const
        from logic.client.const import lobby_model_display_const
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.TEAM_RECRUIT_SCENE, scene_content_type=scene_const.SCENE_TEAM_RECRUIT)

    def on_finalize_panel(self):
        super(TeamRecruitUI, self).on_finalize_panel()
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        self.unregister_timer()

    def refresh_panel(self):
        pass

    def set_show(self, show):
        super(TeamRecruitUI, self).set_show(show)
        if not show:
            global_data.emgr.close_model_display_scene.emit()
            self.request_recommend_teammates()
        else:
            if self._cur_type == self.NORMAL_TYPE:
                self._do_show_model()
                friend_list = global_data.player.get_recommend_players()
            elif self._cur_type == self.PVE_TYPE:
                self._do_pve_show_model()
                friend_list = global_data.player.get_pve_recommend_players()
            if global_data.player:
                if not friend_list:
                    self.request_recommend_teammates()
                self.refresh_fate_group_time()
                self.team_change()

    def refresh_fate_group_time(self):
        if global_data.player:
            time = global_data.player.get_fate_group_time()
            if time > 0:
                self.panel.lab_remind.SetString(13110)
                self.panel.lab_remind.SetColor('#SW')
            else:
                self.panel.lab_remind.SetString(13103)
                self.panel.lab_remind.SetColor(15879662)

    def request_recommend_teammates(self, *args, **kargs):
        show_tips = kargs.get('show_tips', False)
        cur_battle_tid = None
        lobby_ui = global_data.ui_mgr.get_ui('LobbyUI')
        if lobby_ui and lobby_ui.match_widget:
            cur_battle_tid = lobby_ui.match_widget.cur_battle_tid
        if cur_battle_tid is None and global_data.player:
            cur_battle_tid = global_data.player.get_battle_tid()
        if self._cur_type == self.PVE_TYPE:
            cur_battle_tid = DEFAULT_PVE_TID
        if cur_battle_tid and global_data.player:
            global_data.player.request_recommend_teammates(cur_battle_tid, show_tips)
        return

    def _show_model(self):
        self.panel.stopActionByTag(self.DELAY_TAG)
        if self._cur_type == self.NORMAL_TYPE:
            self.panel.DelayCallWithTag(self.DELAY_TIME, self._do_show_model, self.DELAY_TAG)
        elif self._cur_type == self.PVE_TYPE:
            self.panel.DelayCallWithTag(self.DELAY_TIME, self._do_pve_show_model, self.DELAY_TAG)

    def refresh_recommend_teammates(self, *args, **kargs):
        if self._cur_type == self.NORMAL_TYPE:
            self._do_show_model()
        elif self._cur_type == self.PVE_TYPE:
            self._do_pve_show_model()

    def _do_show_model(self):
        if not global_data.player:
            return
        else:
            if not self.panel or not self.panel.isVisible():
                return
            models = []
            boxs = []
            support_mirror = []
            friend_list = global_data.player.get_recommend_players()[:3]
            self.friend_list = friend_list
            self._list_player.SetInitCount(len(friend_list))
            for i, data in enumerate(friend_list):
                node = self._list_player.GetItem(i)
                team_utils.init_teamate_info(node, data)
                fashion_data = data.get('role_fashion')
                role_item_no = fashion_data.get(FASHION_POS_SUIT, 201001100)
                role_head_no = fashion_data.get(FASHION_POS_HEADWEAR, None)
                bag_id = fashion_data.get(FASHION_POS_BACK, None)
                suit_id = fashion_data.get(FASHION_POS_SUIT_2, None)
                other_pendants = [ fashion_data.get(pos) for pos in FASHION_OTHER_PENDANT_LIST ]
                if role_item_no <= 0:
                    continue
                role_model_data = lobby_model_display_utils.get_lobby_model_data(role_item_no, head_id=role_head_no, bag_id=bag_id, suit_id=suit_id, other_pendants=other_pendants)
                for data in role_model_data:
                    data['model_scale'] = data.get('model_scale', 1.0) * 3
                    data['show_anim'] = data['end_anim'] or 'idle'

                models.append(role_model_data)
                boxs.append('box_role_%d' % (i + 1))
                support_mirror.append(True)

            if models:
                global_data.emgr.change_model_display_scene_item_customized.emit(models, boxs, support_mirror, create_callback=self._on_load_model_success)
            else:
                global_data.emgr.close_model_display_scene.emit()
            count_down_data = global_data.player.get_count_down()
            self.update_team_button(count_down_data)
            self.refresh_add_friend()
            self.refresh_team()
            return

    def _on_load_model_success(self, model):
        pass

    def on_refresh_player_inf(self, player_inf):
        self.refresh_add_friend()

    def team_change(self, *args, **kargs):
        if global_data.player:
            count_down_data = global_data.player.get_count_down()
            self.update_team_button(count_down_data)
            self.refresh_team()

    def update_team_button(self, count_down_dict):
        btn_invite_enable = False
        if self._cur_type == self.NORMAL_TYPE:
            list_player = self._list_player
        else:
            if self._cur_type == self.PVE_TYPE:
                list_player = self._list_pve_player
            if not list_player:
                return
        for i, item in enumerate(list_player.GetAllItem()):
            player_inf = self.friend_list[i]
            uid = player_inf.get('uid')
            count_down = count_down_dict.get(uid, 0)
            item.btn_team.lab_time.setVisible(count_down > 0)
            item.btn_team.SetEnable(False)
            if count_down > 0:
                item.btn_team.lab_time.SetString('%ds' % count_down)
                item.btn_team.SetText('')
            elif global_data.player.is_team_full():
                item.btn_team.SetText(13114)
            elif global_data.player.is_teammate(uid):
                item.btn_team.SetText(800148)
            else:
                item.btn_team.SetText(10004)
                item.btn_team.SetEnable(True)
                btn_invite_enable = True

                @item.btn_team.unique_callback()
                def OnClick(btn, touch, player_inf=player_inf):
                    friend_online_state = global_data.message_data.get_player_online_state()
                    state = int(friend_online_state.get(int(player_inf.get('uid')), const.STATE_OFFLINE))
                    if state == const.STATE_TEAM:
                        team_utils.on_join_team(player_inf, TEAM_MODE_RECOMMEND)
                    else:
                        team_utils.on_team(player_inf, TEAM_MODE_RECOMMEND)

        self.panel.btn_invite_all.SetEnable(btn_invite_enable)
        self.panel.btn_invite_all.setVisible(not global_data.player.is_team_full())

    def refresh_add_friend(self):
        if not self.panel or not self.panel.isVisible():
            return
        if self._cur_type == self.NORMAL_TYPE:
            list_player = self._list_player
        elif self._cur_type == self.PVE_TYPE:
            list_player = self._list_pve_player
        for i, item in enumerate(list_player.GetAllItem()):
            player_inf = self.friend_list[i]
            uid = player_inf.get('uid')
            is_friend = global_data.message_data.is_friend(uid)
            item.btn_add.SetEnable(not is_friend)
            item.btn_add.setVisible(not is_friend)
            item.img_friend.setVisible(is_friend)

            @item.btn_add.unique_callback()
            def OnClick(btn, touch, uid=uid):
                if uid == global_data.player.uid:
                    return
                if global_data.message_data.is_black_friend(uid):
                    global_data.game_mgr.show_tip(get_text_by_id(10021), True)
                elif global_data.message_data.is_friend(uid):
                    pass
                else:
                    global_data.player.req_add_friend(uid)

    def refresh_team(self):
        from logic.gutils import role_head_utils
        team_info = global_data.player.get_team_info()
        if team_info is None:
            self.panel.nd_team.setVisible(False)
            self.panel.nd_noteam.setVisible(True)
            return
        else:
            self.panel.nd_team.setVisible(True)
            self.panel.nd_noteam.setVisible(False)
            size = global_data.player.get_team_size()
            max_size = global_data.player.get_max_team_size()
            self.panel.lab_myteam_num.SetString('[%d/%d]' % (size + 1, max_size))
            team_info = global_data.player.get_team_info()
            leader_id = team_info.get('leader', None)
            list_myteam_role = self.panel.list_myteam_role
            for i in range(max_size):
                ui_item = list_myteam_role.GetItem(i)
                ui_item.temp_head.setVisible(False)
                ui_item.temp_head.icon_leader.setVisible(False)
                ui_item.img_empty.setVisible(True)

            if team_info:
                team_dict = team_info.get('members', {})
                head_frame = global_data.player.get_head_frame()
                head_photo = global_data.player.get_head_photo()
                my_inf = {'head_frame': head_frame,'head_photo': head_photo}
                team_dict[global_data.player.uid] = my_inf
                list_myteam_role.SetInitCount(max_size)
                index = 0
                for uid, member in six.iteritems(team_dict):
                    if index >= max_size:
                        break
                    is_leader = uid == leader_id
                    if is_leader:
                        ui_item = list_myteam_role.GetItem(0)
                    else:
                        if index == 0:
                            index = 1
                        ui_item = list_myteam_role.GetItem(index)
                    ui_item.temp_head.setVisible(True)
                    ui_item.img_empty.setVisible(False)
                    is_self = global_data.player.uid == uid
                    if is_self:
                        head_frame = member.get('head_frame')
                        head_photo = member.get('head_photo')
                        role_head_utils.init_role_head(ui_item.temp_head, head_frame, head_photo)
                    else:
                        role_head_utils.init_role_head_auto(ui_item.temp_head, uid, 0, member, show_tips=True)
                    ui_item.temp_head.icon_leader.setVisible(is_leader)
                    index += 1

            return

    def invite_all_people(self):
        if self._cur_type == self.NORMAL_TYPE:
            list_player = self._list_player
        elif self._cur_type == self.PVE_TYPE:
            list_player = self._list_pve_player
        for i, item in enumerate(list_player.GetAllItem()):
            item.btn_team.OnClick(None)

        return

    def do_show_panel(self):
        self._change_scene()
        self.init_event()

    def do_hide_panel(self):
        global_data.emgr.unbind_events(self.global_events)