# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chart_ui/EndTDMSettlementChart.py
from __future__ import absolute_import
import six
from six.moves import range
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from common.uisys.basepanel import BasePanel
from common.const import uiconst
import cc
from logic.comsys.map.map_widget.MapScaleInterface import ChartLine
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from logic.gcommon.common_const.battle_const import BATTLE_SETTLE_REASON_NORMAL, TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL, BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT, BATTLE_SETTLE_REASON_SURRENDER
from logic.gcommon.common_utils.local_text import get_text_by_id
IS_TEAMMATE = 1
IS_ENEMY = 2

class EndTDMSettlementChartUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_tdm/i_tdm_settlement_chart'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = BasePanel.UI_ACTION_EVENT.copy()
    UI_ACTION_EVENT.update({'btn_next.OnClick': 'on_click_btn_next',
       'btn_share.OnClick': 'on_click_btn_share',
       'btn_details.OnClick': 'on_click_btn_details'
       })
    DELTA_TIME = 60
    DOT_TEMPLATE_PATH = 'battle_tdm/i_tdm_settlement_chart_dot_%s'
    LINE_TEMPLATE_PATH = 'battle_tdm/i_tdm_settlement_chart_line_blue'
    UI_COLOR = {IS_TEAMMATE: 'blue',
       IS_ENEMY: 'red'
       }

    def on_init_panel(self, settle_dict, all_info, reward):
        self.init_parameters(settle_dict, all_info, reward)
        self.init_panel()
        self.panel.btn_share.setVisible(global_data.is_share_show)

    def init_panel(self):
        self.init_group_info_chart()
        self.init_delta_point_table()
        self.init_score_title()

    def init_score_title(self):
        settle_dict = self.settle_dict
        self_group_id = self.get_self_group_id()
        group_dict = settle_dict.get('group_points_dict')
        team_score = group_dict.get(str(self_group_id), 0)
        enemy_score = 0
        for g_id in six.iterkeys(group_dict):
            if g_id != str(self_group_id):
                enemy_score = group_dict[g_id]

        self.panel.lab_score_blue.SetString(str(team_score))
        self.panel.lab_score_red.SetString(str(enemy_score))
        reason = self.settle_dict.get('settle_reason', BATTLE_SETTLE_REASON_NORMAL)
        last_point_got_interval = self.settle_dict.get('last_point_got_interval', TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL)
        if reason == BATTLE_SETTLE_REASON_SURRENDER:
            if self.settle_dict.get('extra_detail', {}).get('is_surrender', False):
                self.panel.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_fail.png')
            else:
                self.panel.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_win.png')
        elif team_score > enemy_score or reason == BATTLE_SETTLE_REASON_OTHER_GROUP_QUIT:
            if team_score - enemy_score == 1 and last_point_got_interval < TDM_KNOCKOUT_LAST_POINT_MAX_INTERVAL:
                self.panel.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_konckout.png')
            else:
                self.panel.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_win.png')
        elif team_score == enemy_score:
            self.panel.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_deuce.png')
        else:
            self.panel.img_result.SetDisplayFrameByPath('', 'gui/ui_res_2/txt_pic/text_pic_en/txt_tdm_fail.png')

    def init_parameters(self, settle_dict, all_info, reward):
        self.settle_dict = settle_dict
        self.all_info = all_info
        self._reward = reward
        self.our_group = self.all_info[0][1]
        self.other_group = self.all_info[1][1]
        self.group_id = self.settle_dict.get('group_id', 1)
        self.group_timing_point_dict = self.settle_dict.get('group_timing_point_dict', {})
        self.team_timing_point_dict = self.group_timing_point_dict.get(str(self.group_id), {})
        self.enemy_timing_point_dict = self.group_timing_point_dict.get(str(3 - self.group_id), {})
        self.max_delta_point = 0
        self.chart_content_size = self.panel.nd_content.nd_down.bar_down.nd_draw.nd_draw_line.getContentSize()
        self.chart_content_size_half_height = self.chart_content_size.height / 2
        self.screen_capture_helper = ScreenFrameHelper()
        self.draw_line = ChartLine(self.panel.nd_content.nd_down.bar_down.nd_draw.nd_draw_line, 1)
        self.has_init_time_list = False
        group_door_point_dict = self.settle_dict.get('group_door_point_dict', {})
        self.team_door_point = group_door_point_dict.get(str(self.group_id), 0)
        self.enemy_door_point = group_door_point_dict.get(str(3 - self.group_id), 0)

    def init_group_info_chart(self):
        our_info = self.get_group_info(self.our_group)
        other_info = self.get_group_info(self.other_group)
        our_info[1] = other_info[0]
        other_info[1] = our_info[0]
        list_data = self.panel.nd_content.nd_top.list_data
        for index in range(0, 4):
            list_data.AddTemplateItem(index, bRefresh=True)

        self.init_info_chart_single(list_data.GetItem(0), '{}/{}/{}'.format(our_info[0], our_info[1], our_info[2]), 297, '{}/{}/{}'.format(other_info[0], other_info[1], other_info[2]))
        self.init_info_chart_single(list_data.GetItem(1), '%d' % our_info[3], 298, '%d' % other_info[3])
        self.init_info_chart_single(list_data.GetItem(2), '%d' % our_info[4], 299, '%d' % other_info[4])
        self.init_info_chart_single(list_data.GetItem(3), str(self.team_door_point), 300, str(self.enemy_door_point))

    def get_group_info(self, group_info):
        info = [
         0, 0, 0, 0, 0, 0]
        for index in range(len(group_info)):
            our_group = group_info[index]
            if our_group[0] is None:
                continue
            info[0] += our_group[2] + our_group[3]
            info[2] += our_group[11] + our_group[12]
            scale = global_data.game_mode.get_mode_scale()
            info[3] += our_group[10][1][0] * scale
            info[4] += our_group[10][2][0] * scale

        return info

    def init_info_chart_single(self, nd, info1, info_name, info2):
        nd.lab_value.SetString(info1)
        nd.lab_type.SetString(info_name)
        nd.lab_value_2.SetString(info2)

    def init_delta_point_table(self):
        delta_point_list = []
        max_time = 0
        for key in six.iterkeys(self.team_timing_point_dict):
            max_time = max(max_time, int(key))

        for index in range(self.DELTA_TIME, 1000, self.DELTA_TIME):
            team_point = self.team_timing_point_dict.get(str(index), None)
            enemy_point = self.enemy_timing_point_dict.get(str(index), None)
            if team_point is not None and enemy_point is not None:
                delta_point = team_point - enemy_point
            else:
                break
            delta_point_list.append(delta_point)
            self.max_delta_point = max(self.max_delta_point, abs(delta_point))

        if max_time % 60 != 0:
            self.max_delta_point = max(abs(self.team_timing_point_dict.get(str(max_time), 0) - self.enemy_timing_point_dict.get(str(max_time), 0)), self.max_delta_point)
            delta_point_list.append(self.team_timing_point_dict.get(str(max_time), 0) - self.enemy_timing_point_dict.get(str(max_time), 0))
        chart_width = self.panel.nd_content.nd_down.bar_down.nd_draw.nd_draw_line.getContentSize().width
        point_cnt = len(delta_point_list)
        if point_cnt <= 1:
            time_indent = 0
        else:
            time_indent = chart_width / (point_cnt - 1)
        delta_height = self.chart_content_size_half_height / (self.max_delta_point + 1)
        draw_point = self.panel.list_dot
        start_pos = None
        if not self.has_init_time_list:
            self.init_time_axis(time_indent, len(delta_point_list), max_time)
        for index, value in enumerate(delta_point_list):
            pos_x = time_indent * index
            pos_y = value * delta_height
            self.add_dot(draw_point, value, pos_x, pos_y)
            if not start_pos:
                start_pos = cc.Vec2(pos_x, pos_y + self.chart_content_size_half_height)
            else:
                end_pos = cc.Vec2(pos_x, pos_y + self.chart_content_size_half_height)
                self.draw_line.draw(start_pos, end_pos, 0, self.LINE_TEMPLATE_PATH, None)
                start_pos = end_pos

        return

    def init_time_axis(self, time_indent, score_list_len, lst_time):
        self.has_init_time_list = True
        time = self.DELTA_TIME
        list_time = self.panel.list_time
        for index in range(score_list_len):
            template = list_time.AddTemplateItem()
            template.lab_time.SetString('%02d:%02d' % (time // 60, time % 60))
            time += self.DELTA_TIME

        template_size_width = 0
        if score_list_len > 0:
            template_size_width = list_time.GetItem(0).getContentSize().width
            list_time.GetItem(score_list_len - 1).lab_time.SetString('%02d:%02d' % (lst_time // 60, lst_time % 60))
        list_time.SetHorzIndent(time_indent - template_size_width)

    def add_dot(self, draw_point, value, pos_x, pos_y):
        point_template_name = global_data.uisystem.load_template(self.DOT_TEMPLATE_PATH % self.UI_COLOR[IS_TEAMMATE])
        if value < 0:
            point_template_name = global_data.uisystem.load_template(self.DOT_TEMPLATE_PATH % self.UI_COLOR[IS_ENEMY])
        point_template = draw_point.AddItem(point_template_name, None, bRefresh=False)
        if value >= 0:
            point_template.lab_score.SetString(get_text_by_id(318).format('%d' % abs(value)))
        else:
            point_template.lab_score.SetString(get_text_by_id(317).format('%d' % abs(value)))
        point_template.setAnchorPoint(cc.Vec2(0.5, 0.5))
        point_template.setPosition(pos_x, pos_y)
        return

    def on_click_btn_next(self, *args):
        if self._reward is not None:
            from logic.comsys.battle.Settle.SettleSystem import SettleSystem
            SettleSystem().show_settle_exp(self.settle_dict, self._reward)
        elif global_data.player:
            global_data.player.quit_battle(True)
        self.close()
        return

    def on_click_btn_share(self, *args):
        hide_ui_names = [
         self.__class__.__name__]
        if self.screen_capture_helper:

            def custom_cb(*args):
                self.panel.btn_next.setVisible(True)
                self.panel.btn_share.setVisible(True and global_data.is_share_show)

            self.panel.btn_next.setVisible(False)
            self.panel.btn_share.setVisible(False)
            self.screen_capture_helper.take_screen_shot(hide_ui_names, self.panel, custom_cb=custom_cb)

    def on_click_btn_details(self, btn, touch):
        from logic.comsys.battle.Settle.SettleSystem import SettleSystem
        SettleSystem().show_settlement_tdm_chart2_ui(self.settle_dict, self.all_info, self._reward)
        self.close()

    def get_self_group_id(self):
        if self.is_ob_settle():
            return self.settle_dict.get('ob_data', {}).get('watching_group_id', None)
        else:
            return global_data.player.logic.ev_g_group_id()
            return None

    def is_ob_settle(self):
        from logic.gutils import judge_utils
        return judge_utils.is_ob()