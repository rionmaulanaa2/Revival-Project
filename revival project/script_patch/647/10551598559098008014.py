# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/PlayerBattleInfoWidget.py
from __future__ import absolute_import
from six.moves import zip
from six.moves import range
from common.const.property_const import *
from logic.client.const import player_battle_info_const as battle_const
from logic.gcommon.common_const import statistics_const as sconst
from .PlayerTabBaseWidget import PlayerTabBaseWidget
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.utils.time_utils import ONE_MINUTE_SECONDS, ONE_HOUR_SECONS
import time
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from logic.gutils.share_utils import check_share_tips_wrapper
TYPE_SINGLE = 1
TYPE_DOUBLE = 2
TYPE_SQUAD = 3
TYPE_KOTH = 4
TYPE_DEATH = 5
CHICKEN_MODE_TYPE = (
 TYPE_SINGLE, TYPE_DOUBLE, TYPE_SQUAD)
TYPE_MODES = [
 TYPE_SINGLE, TYPE_DOUBLE, TYPE_SQUAD, TYPE_DEATH]
SHOW_MODES = {TYPE_SINGLE: [battle_const.RANK_MODE_SINGLE, battle_const.CUSTOM_MODE_SINGLE],TYPE_DOUBLE: [
               battle_const.RANK_MODE_DOUBLE, battle_const.CUSTOM_MODE_DOUBLE],
   TYPE_SQUAD: [
              battle_const.RANK_MODE_SQUAD, battle_const.CUSTOM_MODE_SQUAD],
   TYPE_KOTH: [
             battle_const.RANK_MODE_KOTH, battle_const.CUSTOM_MODE_KOTH],
   TYPE_DEATH: [
              battle_const.RANK_MODE_DEATH, battle_const.CUSTOM_MODE_DEATH]
   }

class PlayerBattleInfoWidget(PlayerTabBaseWidget):
    PANEL_CONFIG_NAME = 'role/i_role_battle_detail'

    def __init__(self, panel):
        super(PlayerBattleInfoWidget, self).__init__(panel)
        self.personal_info = {}
        self.init_parameters()
        self._my_uid = global_data.player.uid
        self._show_battle_season_id = global_data.player.get_battle_season()
        self._cur_battle_season_id = global_data.player.get_battle_season()
        self._cur_uid = None
        self._cur_mode = TYPE_MODES[0]
        self._change_tab_flag_info = [True, time.time()]
        self._share_content = None
        self._screen_capture_helper = ScreenFrameHelper()
        from logic.comsys.share.ShareTipsWidget import ShareTipsWidget
        self._share_tips_widget = ShareTipsWidget(self, self.panel, self.panel.btn_share, pos=('50%-45',
                                                                                               '50%-20'), json_path='share/i_share_tips_sp')
        self.init_event()
        self._player_stat_inf = {}
        self._history_season_ids = []
        self._draw_node = None
        self.init_radar_draw_node()
        self.init_top()
        self.init_season()
        self.init_buttons()
        return

    def init_parameters(self):
        self.TOP_INFO = [
         (
          sconst.TOTAL_CNT, 10234, '%d'), (sconst.WIN_CNT, 10235, '%d'),
         (
          sconst.KILL_MECHA, 10236, '%d'), (sconst.KILL_HUMAN, 10237, '%d')]
        self.DEAD_RATE = (15025, '%.2f')
        self.DETAIL_INFO = [
         (
          sconst.SURVIVAL_TIME, 10239, get_text_by_id(10255).format(data='%.1f')),
         (
          sconst.WIN_CNT, 10240, '%.1f'),
         (
          sconst.TOP10_CNT, 10241, '%.1f'),
         (
          sconst.MAX_SURVIVAL_TIME, 10242, get_text_by_id(10256).format(data='%.1f')),
         (
          sconst.MAX_KILL_HUMAN, 10243, '%d'),
         (
          sconst.MAX_KILL_MECHA, 10244, '%d'),
         (
          sconst.HUMAN_KILL_MECHA, 10245, '%d'),
         (
          sconst.SAVE_CNT, 10246, '%d')]
        self.ONCE_BATTLE_INFO = [
         (
          sconst.MOVE_DIST, 10247, get_text_by_id(10257).format(data='%d')),
         (
          sconst.SURVIVAL_TIME, 10248, get_text_by_id(10256).format(data='%.1f')),
         (
          sconst.MECHA_DAMAGE, 10249, '%.1f'),
         (
          sconst.HUMAN_DAMAGE, 10250, '%.1f'),
         (
          sconst.KILL_MONSTER, 10251, '%.1f'),
         (
          sconst.MECHA_HURT, 10252, '%.1f'),
         (
          sconst.MECHA_CURE, 10253, '%.1f'),
         (
          sconst.ASSIST_MECHA, 10254, '%.1f'),
         (
          sconst.FIRST_BLOOD, 7058, '%d'),
         (
          sconst.FIGHT_BACK, 7042, '%d'),
         (
          sconst.TERMINATOR, 7044, '%d'),
         (
          sconst.PERFECT_ATK, 7045, '%d'),
         (
          sconst.RIGHT_ON_TARGET, 7043, '%d'),
         (
          sconst.GOAL_POACHER, 7046, '%d'),
         (
          sconst.GET_MVP, 80689, '%d')]
        self.DETAIL_IGNORE = {TYPE_SINGLE: [
                       sconst.SAVE_CNT],
           TYPE_KOTH: [
                     sconst.TOP10_CNT, sconst.MAX_SURVIVAL_TIME, sconst.TOP5_CNT],
           TYPE_DEATH: [
                      sconst.TOP10_CNT, sconst.MAX_SURVIVAL_TIME, sconst.SAVE_CNT, sconst.TOP5_CNT]
           }
        self.ONCE_BATTLE_IGNORE = {TYPE_SINGLE: [
                       sconst.ASSIST_MECHA, sconst.FIRST_BLOOD, sconst.FIGHT_BACK, sconst.TERMINATOR, sconst.PERFECT_ATK, sconst.RIGHT_ON_TARGET, sconst.GOAL_POACHER, sconst.GET_MVP],
           TYPE_DOUBLE: [
                       sconst.FIRST_BLOOD, sconst.FIGHT_BACK, sconst.TERMINATOR, sconst.PERFECT_ATK, sconst.RIGHT_ON_TARGET, sconst.GOAL_POACHER, sconst.GET_MVP],
           TYPE_SQUAD: [
                      sconst.FIRST_BLOOD, sconst.FIGHT_BACK, sconst.TERMINATOR, sconst.PERFECT_ATK, sconst.RIGHT_ON_TARGET, sconst.GOAL_POACHER, sconst.GET_MVP],
           TYPE_KOTH: [
                     sconst.SURVIVAL_TIME, sconst.FIRST_BLOOD, sconst.FIGHT_BACK, sconst.TERMINATOR, sconst.PERFECT_ATK, sconst.RIGHT_ON_TARGET, sconst.GOAL_POACHER, sconst.GET_MVP],
           TYPE_DEATH: [
                      sconst.MOVE_DIST, sconst.SURVIVAL_TIME, sconst.KILL_MONSTER, sconst.MECHA_CURE]
           }

    def init_event(self):
        global_data.emgr.player_first_success_share_event += self.on_first_success_share

    def destroy(self):
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
        self._screen_capture_helper = None
        if self._share_content:
            self._share_content.destroy()
        self._share_content = None
        if self._share_tips_widget:
            self._share_tips_widget.destroy()
        self._share_tips_widget = None
        super(PlayerBattleInfoWidget, self).destroy()
        self.personal_info = {}
        self._cur_player_history_stat_inf = {}
        return

    def init_top(self):
        top_tab = self.panel.pnl_list_top_tab
        self.top_tab_data_dict = {TYPE_SINGLE: {'text': get_text_by_id(19005)},TYPE_DOUBLE: {'text': get_text_by_id(19006)},TYPE_SQUAD: {'text': get_text_by_id(13021)},TYPE_KOTH: {'text': get_text_by_id(10282)},TYPE_DEATH: {'text': get_text_by_id(10296)}}
        self.panel.pnl_list_top_tab.SetInitCount(len(TYPE_MODES))
        for item in top_tab.GetAllItem():
            item.setVisible(False)

        for idx, itype in enumerate(TYPE_MODES):
            info = self.top_tab_data_dict[itype]
            item = top_tab.GetItem(idx)
            item.setVisible(True)
            text = info.get('text', '')
            item.btn_tab.SetText(text)
            item.btn_tab.EnableCustomState(True)
            self.add_mode_touch(item, itype)

        self.on_select_top_btn(self._cur_mode)
        self.refresh_player_stat_inf()

    def on_select_top_btn(self, mode):
        top_tab = self.panel.pnl_list_top_tab
        for idx, itype in enumerate(TYPE_MODES):
            item = top_tab.GetItem(idx)
            info = self.top_tab_data_dict[itype]
            if mode != itype:
                item.btn_tab.SetSelect(False)
            else:
                item.btn_tab.SetSelect(True)

    def add_mode_touch(self, item, itype):

        @item.btn_tab.callback()
        def OnClick(*args):
            self._cur_mode = itype
            self.on_select_top_btn(self._cur_mode)
            self.refresh_player_stat_inf()

    def init_buttons(self):
        if self._cur_uid == self._my_uid:
            self.panel.btn_share.setVisible(True and global_data.is_share_show)
        else:
            self.panel.btn_share.setVisible(False)

        @self.panel.btn_share.callback()
        def OnClick(btn, touch):
            if not self._share_content:
                self._share_content = self.generate_share_content()
            if self._share_content:
                share_data = self.get_share_data()
                battle_mode_str = self.top_tab_data_dict.get(self._cur_mode, {}).get('text', '')
                modes = SHOW_MODES.get(self._cur_mode, [])
                if modes:
                    rank = global_data.player.get_avg_settle_score_grade(modes[0])
                else:
                    rank = 'C'
                self._share_content.refresh_player_stat_inf(rank, battle_mode_str, share_data)
            player_ui = global_data.ui_mgr.get_ui('PlayerInfoUI')
            if player_ui:
                from logic.comsys.role.PlayerInfoUI import TAB_BATTLE_INFO
                player_ui.share_page_require_model_show(TAB_BATTLE_INFO)
            from logic.comsys.share.ShareUI import ShareUI
            ShareUI()

    def _real_capture(self):
        ui_names = [
         'LobbyFullScreenBgUI']
        player_ui = global_data.ui_mgr.get_ui('PlayerInfoUI')
        if player_ui:
            player_ui.panel.temp_btn_back.setVisible(False)

        def cb(*args):
            self.panel.btn_share.setVisible(True and global_data.is_share_show)
            if player_ui:
                player_ui.panel.temp_btn_back.setVisible(True)
            if player_ui:
                player_ui.share_page_require_model_show(None)
            return

        if self._screen_capture_helper:
            self.panel.btn_share.setVisible(False)
            self._screen_capture_helper.set_custom_share_content(self._share_content)
            self._screen_capture_helper.take_screen_shot(ui_names, self.panel, custom_cb=cb)

    def generate_share_content(self):
        from logic.comsys.share.RoleBattleShareCreator import RoleBattleShareCreator
        share_creator = RoleBattleShareCreator()
        share_creator.create()
        share_content = share_creator
        return share_content

    def on_player_stat_inf(self, stat_inf):
        self._cur_uid = stat_inf[U_ID]
        self._player_stat_inf = stat_inf
        self._history_season_ids = list(self._player_stat_inf.get(HISTORY_SEASON_IDS, []))
        self.refresh_player_stat_inf()
        self.init_season_list()
        self.init_buttons()
        if self._change_tab_flag_info[0]:
            if time.time() - self._change_tab_flag_info[1] <= 0.1:
                idx = self._get_longest_gametime_type_mode_idx()
                if idx != -1:
                    item = self.panel.pnl_list_top_tab.GetItem(idx)
                    item.btn_tab.OnClick()
            self._change_tab_flag_info[0] = False

    def _get_longest_gametime_type_mode_idx(self):
        ret_idx = -1
        min_val = -233
        for idx, itype in enumerate(TYPE_MODES):
            if self.get_battle_stat_prop(itype, sconst.SURVIVAL_TIME) > min_val:
                min_val = self.get_battle_stat_prop(itype, sconst.SURVIVAL_TIME)
                ret_idx = idx

        return ret_idx

    def on_refresh_player_detail_inf(self, player_battle_inf):
        self.show_radar()

    def refresh_player_stat_inf(self):
        self.refresh_top_info(self._cur_mode)
        self.refresh_detail_info(self._cur_mode)

    def refresh_top_info(self, battle_mode):
        is_mainland_chicken = battle_mode in CHICKEN_MODE_TYPE and not G_IS_NA_USER
        intend = 20 if is_mainland_chicken else 54
        self.panel.list_data.SetHorzIndent(intend)
        TOP_INFO = self.TOP_INFO
        self.panel.list_data.SetInitCount(len(TOP_INFO))
        for idx, data in enumerate(TOP_INFO):
            state, txt_id, cnt_format = data
            if state == sconst.WIN_CNT and is_mainland_chicken:
                txt_id = 81998
            cnt = self.get_battle_stat_prop(battle_mode, state)
            nd = self.panel.list_data.GetItem(idx)
            nd and nd.lab_data.SetString(cnt_format % cnt)
            nd and nd.lab_title.SetString(get_text_by_id(txt_id))

        item = self.panel.list_data.AddTemplateItem()
        txt_id, cnt_format = self.DEAD_RATE
        battle_cnt = self.get_battle_stat_prop(battle_mode, sconst.TOTAL_CNT)
        if battle_cnt == 0:
            text = '-'
        else:
            kill_human_cnt = self.get_battle_stat_prop(battle_mode, sconst.KILL_HUMAN)
            kill_mecha_cnt = self.get_battle_stat_prop(battle_mode, sconst.KILL_MECHA)
            kill_total = kill_human_cnt + kill_mecha_cnt
            text = cnt_format % (kill_total / float(battle_cnt))
        nd = item
        nd and nd.lab_data.SetString(text)
        nd and nd.lab_title.SetString(get_text_by_id(txt_id))
        if is_mainland_chicken:
            five_top_item = self.panel.list_data.AddTemplateItem()
            top_five_cnt = self.get_battle_stat_prop(battle_mode, sconst.TOP5_CNT)
            five_top_item.lab_title.SetString(81999)
            five_top_item.lab_data.SetString(str(top_five_cnt))

    def refresh_detail_info(self, battle_mode):
        max_count = 16
        total_cnt = self.get_battle_stat_prop(battle_mode, sconst.TOTAL_CNT)
        index = 0
        is_mainland_chicken = battle_mode in CHICKEN_MODE_TYPE and not G_IS_NA_USER
        is_chicken = battle_mode in CHICKEN_MODE_TYPE
        for data in self.DETAIL_INFO:
            if index >= max_count:
                break
            state, txt_id, cnt_format = data
            if state == sconst.WIN_CNT:
                if is_mainland_chicken:
                    txt_id = 82000
                elif is_chicken:
                    txt_id = 83446
            if state == sconst.TOP10_CNT and is_mainland_chicken:
                txt_id = 10240
                state = sconst.TOP5_CNT
            if state in self.DETAIL_IGNORE.get(self._cur_mode, []):
                continue
            cnt = float(self.get_battle_stat_prop(battle_mode, state))
            if state in [sconst.SURVIVAL_TIME]:
                cnt /= ONE_HOUR_SECONS
            elif state in [sconst.MAX_SURVIVAL_TIME]:
                cnt /= ONE_MINUTE_SECONDS
            if state in [sconst.WIN_CNT, sconst.TOP10_CNT, sconst.TOP5_CNT]:
                if total_cnt == 0:
                    cnt_txt = '-'
                else:
                    cnt_txt = cnt_format % (cnt / total_cnt * 100) + '%'
            else:
                cnt_txt = cnt_format % cnt
            self.set_nd_string(index, cnt_txt, txt_id)
            index += 1

        for data in self.ONCE_BATTLE_INFO:
            if index >= max_count:
                break
            state, txtid, cnt_format = data
            if state in self.ONCE_BATTLE_IGNORE.get(self._cur_mode, []):
                continue
            cnt = float(self.get_battle_stat_prop(battle_mode, state))
            if state in [sconst.SURVIVAL_TIME]:
                cnt /= ONE_MINUTE_SECONDS
            if state in [sconst.FIRST_BLOOD, sconst.FIGHT_BACK, sconst.TERMINATOR, sconst.PERFECT_ATK, sconst.RIGHT_ON_TARGET, sconst.GOAL_POACHER, sconst.GET_MVP]:
                cnt_txt = cnt_format % cnt
            elif total_cnt == 0:
                cnt_txt = '-'
            else:
                cnt_txt = cnt_format % (cnt / total_cnt)
            self.set_nd_string(index, cnt_txt, txtid)
            index += 1

        for index in range(index, max_count):
            nd = self.get_detail_node(index)
            nd and nd.setVisible(False)

    def set_nd_string(self, index, cnt_txt, txtid):
        nd = self.get_detail_node(index)
        nd and nd.lab_num.SetString(cnt_txt)
        nd and nd.lab_title.SetString(get_text_by_id(txtid))
        nd and nd.setVisible(True)
        nd and nd.img_highlight.setVisible(index % 2 == 0)

    def get_detail_node(self, index):
        list_item_count = 8
        nd_details = self.panel.nd_details
        idx = index / list_item_count + 1
        nd_list = getattr(nd_details, 'nd_list_%d' % idx)
        if nd_list:
            list_nd_sec = getattr(nd_list, 'pnl_list_%d' % idx)
            if list_nd_sec:
                return list_nd_sec.GetItem(index % list_item_count)

    def get_battle_stat_prop(self, battle_mode, battle_prop, season=None):
        stat_inf = self._player_stat_inf.get(season if season is not None else self._show_battle_season_id, {})
        modes = SHOW_MODES.get(battle_mode, [])
        value = 0
        for mode in modes:
            prop = sconst.CAREER_STATISTICS_BATTLE_PROP(mode, battle_prop)
            value += stat_inf.get(prop, 0)

        return value

    def show_radar(self, score_list=(0, 50, 89, 100, 24)):
        self.set_radar_score(score_list)
        NUM = 5
        import cc
        import math
        radar = self.panel.temp_radar
        LINE_WIDTH = 2
        FILL_COLOR = cc.Color4F(14 / 255.0, 150 / 255.0, 236 / 255.0, 0.35)
        LINE_COLOR = cc.Color4F(1, 1, 1, 1)
        PER_ANGLE = 360 / NUM
        START_ANGLE = 90
        angles = [ math.radians(START_ANGLE - PER_ANGLE * idx) for idx in range(5) ]
        scale = 2.0
        MAX_LINE_LENGTH = 110 * scale
        lengths = [ score / 100.0 * MAX_LINE_LENGTH for score in score_list ]
        verts = [ cc.Vec2(math.cos(ang) * length, math.sin(ang) * length) for ang, length in zip(angles, lengths) ]
        self._draw_node.drawPolygon(verts, FILL_COLOR, LINE_WIDTH * scale, LINE_COLOR)
        self._draw_node.setScale(1 / scale)

    def set_radar_score(self, score_list):
        for idx, score in enumerate(score_list):
            nd = getattr(self.panel.temp_radar, 'nd_data%d' % (idx + 1))
            if nd:
                nd.lab_num.SetString(str(score))

    def init_radar_draw_node(self):
        from common.utils.cocos_utils import ccp
        radar = self.panel.temp_radar.nd_radar
        from common.uisys.uielment.CCDrawNode import CCDrawNode
        if not self._draw_node:
            _draw_node = CCDrawNode.Create()
            _draw_node.setAnchorPoint(ccp(0.5, 0.5))
            radar.AddChild('', _draw_node, 10, -1)
            _draw_node.SetPosition('50%', '50%')
            self._draw_node = _draw_node

    def get_share_data(self):
        win_cnt = self.get_battle_stat_prop(self._cur_mode, sconst.WIN_CNT, self._cur_battle_season_id)
        total_cnt = self.get_battle_stat_prop(self._cur_mode, sconst.TOTAL_CNT, self._cur_battle_season_id)
        kill_mecha_cnt = self.get_battle_stat_prop(self._cur_mode, sconst.KILL_MECHA, self._cur_battle_season_id)
        kill_human_cnt = self.get_battle_stat_prop(self._cur_mode, sconst.KILL_HUMAN, self._cur_battle_season_id)
        txt_id, cnt_format = self.DEAD_RATE
        battle_cnt = self.get_battle_stat_prop(self._cur_mode, sconst.TOTAL_CNT, self._cur_battle_season_id)
        if battle_cnt == 0:
            avg_kda = '-'
        else:
            kill_human_cnt = self.get_battle_stat_prop(self._cur_mode, sconst.KILL_HUMAN, self._cur_battle_season_id)
            kill_mecha_cnt = self.get_battle_stat_prop(self._cur_mode, sconst.KILL_MECHA, self._cur_battle_season_id)
            kill_total = kill_human_cnt + kill_mecha_cnt
            avg_kda = cnt_format % (kill_total / float(battle_cnt))
        if total_cnt == 0:
            win_rate = '0%'
        else:
            win_rate = '%.2f' % (win_cnt * 100.0 / total_cnt) + '%'
        return (
         total_cnt, win_cnt, kill_mecha_cnt, kill_human_cnt, avg_kda, win_rate)

    def on_click_btn_share(self, btn, touch):
        from logic.comsys.share.PersonInfoShareCreator import PersonInfoShareCreator
        from logic.comsys.share.ShareUI import ShareUI
        share_ui = ShareUI()
        if not self._share_content:
            share_creator = PersonInfoShareCreator()
            share_creator.create()
            self._share_content = share_creator
        battle_data = self.get_share_data()
        if self._cur_mode == TYPE_SINGLE:
            battle_mode_str = get_text_by_id(10049)
        elif self._cur_mode == TYPE_DOUBLE:
            battle_mode_str = get_text_by_id(10050)
        else:
            battle_mode_str = get_text_by_id(10051)
        self._share_content.refresh_player_stat_inf(battle_mode_str, battle_data)
        share_ui.set_share_content_raw(self._share_content.get_render_texture(), share_content=self._share_content)

    def on_first_success_share(self):
        pass

    def init_season(self):

        @self.panel.btn_season.unique_callback()
        def OnClick(btn, touch):
            if self.panel.season_list.isVisible():
                self.hide_season_list()
            else:
                self.show_season_list()

    def show_season_list(self):
        self.panel.season_list.setVisible(True)
        self.panel.btn_season.img_icon.setRotation(180)

    def hide_season_list(self):
        self.panel.season_list.setVisible(False)
        self.panel.btn_season.img_icon.setRotation(0)

    def init_season_list(self):
        from logic.gutils import template_utils
        seasons_list = self._history_season_ids
        if self._cur_battle_season_id not in seasons_list:
            seasons_list.append(self._cur_battle_season_id)
        mode_option = [ {'name': self.get_season_name(s_id),'mode': s_id} for s_id in seasons_list
                      ]

        def call_back(index):
            option = mode_option[index]
            self.on_need_show_show_battle_season_id(option['mode'])
            self.hide_season_list()
            self.panel.btn_season.SetText(option['name'])

        def close_callback():
            self.hide_season_list()

        template_utils.init_common_choose_list(self.panel.season_list, mode_option, call_back, close_cb=close_callback)

    def get_season_name(self, season_id):
        if str(season_id) == '0':
            return get_text_by_id(10293)
        else:
            if season_id == self._cur_battle_season_id:
                return get_text_by_id(10294)
            return get_text_by_id(10295, (str(season_id),))

    def on_need_show_show_battle_season_id(self, season_id):
        self._show_battle_season_id = season_id
        stat_inf = global_data.message_data.get_player_stat_inf(self._cur_uid)
        if season_id in stat_inf:
            self.on_player_stat_inf(stat_inf)
        else:
            global_data.player.request_player_stat_info(self._cur_uid, season_id)

    def on_share_model_loaded(self):
        self._real_capture()