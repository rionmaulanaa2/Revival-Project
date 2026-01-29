# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chart_ui/EndSettlementChartUI.py
from __future__ import absolute_import
import six
from six.moves import range
import random
from common.cfg import confmgr
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from common.uisys.basepanel import BasePanel
from common.const import uiconst
import cc
import time
from logic.comsys.map.map_widget.MapScaleInterface import ChartLine
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.end_statics_utils import get_battle_achieve_text_id
from logic.gutils.role_head_utils import get_mecha_photo, get_role_default_photo, get_head_photo_res_path
SKIP_BUTTON = 1
RESTART_BUTTON = 2
DISPLAY_POINT_ZORDER = 1
SELF_SPECIAL_POINT_ZORDER = 0
SELF_NORMAL_POINT_ZORDER = -1
OTHER_POINT_ZORDER = -2

class EndSettlementChartUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/i_end_settlement_chart'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = BasePanel.UI_ACTION_EVENT.copy()
    UI_ACTION_EVENT.update({'btn_next.OnClick': 'on_click_btn_next',
       'btn_share.OnClick': 'on_click_btn_share',
       'btn_skip.OnClick': 'on_click_btn_double_speed_play',
       'nd_bg.OnClick': 'on_click_panel',
       'btn_skip_long.OnClick': 'on_click_btn_skip'
       })
    UI_COLOR = [
     'blue', 'green', 'yellow']
    UI_TEAMMATE_ICON_PATH = 'gui/ui_res_2/battle/icon/icon_teammate_num_%s.png'
    TEAMMATE_ICON_BACKGROUND_PATH = 'gui/ui_res_2/battle/settlement_chart/bar_end_chart_teammate_%s.png'
    EVENT_ICON_TEMPLATE_PATH = 'end/i_end_settlement_icon'
    EVENT_DESC_TEMPLATE_PATH = 'end/i_end_settlement_tips'
    SHARE_TEMPLATE_PATH = 'end/i_end_settlement_chart_achievement'
    ICON_END_CHART_PLAYER_INFO_PATH = {0: 'gui/ui_res_2/battle/settlement_chart/icon/icon_end_chart_event_kill.png',
       1: 'gui/ui_res_2/battle/settlement_chart/icon/icon_end_chart_event_mech.png'
       }
    SPECIAL_ICON = (
     battle_const.CHART_EVENT_WIN, battle_const.CHART_EVENT_DIE, battle_const.CHART_EVENT_LAND)
    UI_DOT_PATH = 'gui/ui_res_2/battle/settlement_chart/img_end_chart_dot_%s.png'
    SELF_LINE_PATH = 'end/i_end_settlement_chart_line_%s'
    OTHER_LINE_PATH = 'end/i_end_settlement_chart_line_%s2'
    SHARE_FONT_SIZE_MIN = 18
    SHARE_FONT_SIZE_MAX = 34
    DRAW_LINE_SPEED = 5

    def on_init_panel(self, settle_dict, teammate_info, reward, achievement_list):
        self.init_parameters(settle_dict, teammate_info, reward, achievement_list)
        self.panel.nd_content.btn_share.setVisible(global_data.is_share_show)
        self.init_panel()

    def on_finalize_panel(self):
        if self.screen_capture_helper:
            self.screen_capture_helper.destroy()
        if self.draw_line:
            self.draw_line.destroy()
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)

    def init_panel(self):
        self.init_map_img()
        from logic.gcommon.common_const.statistics_const import HUMAN_DAMAGE, MECHA_DAMAGE, MECHA_TRANS_DAMAGE
        player_statistics = self.settle_dict.get('statistics', {})
        move_dist = player_statistics.get('move_dist', 0.0)
        damage = player_statistics.get(HUMAN_DAMAGE, 0) + player_statistics.get(MECHA_DAMAGE, 0) + player_statistics.get(MECHA_TRANS_DAMAGE, 0)
        self.panel.nd_content.nd_map.bar_data.lab_data.SetString(get_text_by_id(284).format('%.0f' % damage))
        self.panel.nd_content.nd_map.bar_data.lab_data2.SetString(get_text_by_id(285).format('%.0fm' % move_dist))
        self.panel.nd_top_rank.lab_game_mode.SetString(318 + self.group_member_num)
        if self.rank <= 10:
            self.panel.bar_top_rank.setVisible(False)
            self.panel.nd_team_rank.setVisible(False)
            self.panel.bar_top_rank_yellow.setVisible(True)
            self.panel.nd_team_rank_yellow.setVisible(True)
            self.panel.lab_team_count_yellow.SetString(get_text_by_id(323).format(str(self.rank)))
            self.panel.lab_team_total_yellow.SetString('/{}'.format(str(self.total_fighter_num)))
        else:
            self.panel.bar_top_rank.setVisible(True)
            self.panel.nd_team_rank.setVisible(True)
            self.panel.bar_top_rank_yellow.setVisible(False)
            self.panel.nd_team_rank_yellow.setVisible(False)
            self.panel.lab_team_count.SetString(get_text_by_id(324).format(str(self.rank)))
            self.panel.lab_team_total.SetString('/{}'.format(str(self.total_fighter_num)))
        self.panel.lab_time.SetString(time.strftime('%Y.%m.%d'))
        self._draw_node = cc.DrawNode.create()
        self.draw_line = ChartLine(self.panel.nd_content.nd_map.list_map.GetContainer().img_map.line, 1)
        self.panel.nd_content.nd_map.list_map.GetContainer().img_map.line.addChild(self._draw_node)
        self.panel.nd_content.nd_info.bar_type.lab_type.SetString(288)
        self.init_player_info_list()
        self.init_share_panel()
        from logic.comsys.chart_ui.EndSettlementChartUIMapTouchLayerWidget import EndSettlementChartUIMapTouchLayerWidget
        self.touch_layer = EndSettlementChartUIMapTouchLayerWidget(self)
        self.panel.PlayAnimation('show')
        self.has_finish_draw = False
        self.begin_draw_event_on_map()

    def init_parameters(self, settle_dict, teammate_info, reward, achievement_list):
        self.settle_chart_info_dict = confmgr.get('c_settlement_chart')
        self.settle_chart_img_info = self.settle_chart_info_dict.get('SettlementChartImgInfo', {})
        self.settle_chart_based_info = self.settle_chart_info_dict.get('SettlementChartBasedInfo', {})
        self.time_mul = self.settle_chart_based_info.get('cTimeMul', 50)
        self.time_interval = self.settle_chart_based_info.get('cTimeInterval', 0.2)
        self.show_event_interval = self.settle_chart_based_info.get('cEventShowInterval', 0.5)
        self.map_img_width = None
        self.map_img_height = None
        self.settle_dict = settle_dict
        self.teammate_info = teammate_info
        self.total_fighter_num = self.settle_dict.get('total_fighter_num', 100)
        self.rank = self.settle_dict.get('rank', self.total_fighter_num)
        self.reward = reward
        self.group_member_num = len(self.teammate_info) + 1
        self.players_info_dic = {}
        self.player_seq = None
        self.timer_id = None
        self.char_name = global_data.player.logic.ev_g_char_name()
        self.achievement_list = []
        for achievement in achievement_list:
            self.achievement_list.append(get_text_by_id(get_battle_achieve_text_id(achievement)))

        self.screen_capture_helper = ScreenFrameHelper()
        self.icon_template = global_data.uisystem.load_template(self.EVENT_ICON_TEMPLATE_PATH)
        self.icon_container = self.panel.nd_content.nd_map.list_map.GetContainer().img_map.list_tips
        self.desc_template = global_data.uisystem.load_template(self.EVENT_DESC_TEMPLATE_PATH)
        self.desc_container = self.panel.nd_content.nd_map.list_map.GetContainer().img_map.list_current_event
        self.battle_begin_time = self.settle_dict.get('battle_start_time', time.time())
        self.draw_time = None
        self.fight_event = self.settle_dict.get('fight_event', [])
        self.skip_button_model = SKIP_BUTTON
        self.wait_show_tips = False
        self.if_is_skip = False
        self.bar_kill = self.panel.nd_content.nd_map.bar_kill
        self.has_finish_draw = False
        self.get_map_info()
        self.init_event_parameters()
        return

    def init_event_parameters(self):
        self.event_selected_index = None
        self.event_template_dict = {}
        self.event_icon_dict = {}
        self.event_desc_dict = {}
        self.event_kill_banner_dict = {}
        self.self_lst_line_container_index = None
        self.other_lst_line_container_index_dic = {}
        self.draw_line_by_time_self_index = 0
        self.draw_line_by_time_teammate_index_dic = {}
        return

    def get_players_info(self):
        if not self.players_info_dic:
            self.players_info_dic = {}
        keys_list = []
        object_id_list = []
        self.object_id_dic = {}
        self_object_id = str(global_data.player.id)
        object_id_list.append(self_object_id)
        for key in six.iterkeys(self.teammate_info):
            keys_list.append(key)
            object_id_list.append(str(key))

        object_id_list = sorted(object_id_list)
        for index, object_id in enumerate(object_id_list):
            self.object_id_dic[object_id] = index
            if object_id == self_object_id:
                self.player_seq = index

        for index in range(0, self.group_member_num):
            if object_id_list[index] == self_object_id:
                self.players_info_dic[index] = self.settle_dict
                self.players_info_dic[index]['char_name'] = self.char_name
                self.players_info_dic[index]['role_id'] = self.players_info_dic[index].get('role', 11)
                from logic.gcommon.cdata.dan_data import DAN_SURVIVAL
                cur_dan = global_data.player.get_dan(DAN_SURVIVAL)
                cur_lv = global_data.player.get_dan_lv(DAN_SURVIVAL)
                cur_star = global_data.player.get_dan_star(DAN_SURVIVAL)
                dan_info = {'dan': cur_dan,
                   'lv': cur_lv,
                   'star': cur_star
                   }
                self.players_info_dic[index]['dan_info'] = dan_info
            elif 0 < len(keys_list) and str(keys_list[0]) == object_id_list[index]:
                self.players_info_dic[index] = self.teammate_info[keys_list[0]]
            elif 1 < len(keys_list) and str(keys_list[1]) == object_id_list[index]:
                self.players_info_dic[index] = self.teammate_info[keys_list[1]]

    def init_player_info_list(self):
        self.get_players_info()
        list_player = self.nd_info.list_player
        for index in range(0, 3):
            list_player.GetItem(index).btn_player.nd_content.setVisible(False)

        from logic.gutils import role_head_utils
        for index in range(0, self.group_member_num):
            player_info = self.players_info_dic.get(index, {})
            player_name = player_info.get('char_name', '')
            player_info_template = list_player.GetItem(index)
            player_info_template.btn_player.nd_content.setVisible(True)
            player_info_template.lab_player_name.SetString(player_name)
            player_info_template.icon_sequence.SetDisplayFrameByPath('', self.UI_TEAMMATE_ICON_PATH % self.UI_COLOR[index])
            role_head_utils.set_role_dan(player_info_template.nd_content.temp_tier, player_info.get('dan_info', {}))
            if self.player_seq == index:
                created_mecha_id = player_info.get('created_mecha_ids', [])
                if created_mecha_id and len(created_mecha_id) > 0:
                    mecha_id = created_mecha_id[-1]
                else:
                    mecha_id = None
            else:
                mecha_id = player_info.get('mecha_id', None)
            role_id = player_info.get('role_id', 11)
            role_head_utils.set_role_head_photo(player_info_template.temp_role, self.get_phote_no(mecha_id, role_id))
            list_data = player_info_template.list_data
            statisitcs = player_info.get('statistics', {})
            kill_list_template = list_data.AddTemplateItem(0, bRefresh=True)
            kill_list_template.img_icon.SetDisplayFrameByPath('', self.ICON_END_CHART_PLAYER_INFO_PATH[0])
            kill_list_template.lab_value.SetString(str(statisitcs.get('kill', 0)))
            kill_list_template.lab_name.SetString(286)
            kill_list_template = list_data.AddTemplateItem(1, bRefresh=True)
            kill_list_template.img_icon.SetDisplayFrameByPath('', self.ICON_END_CHART_PLAYER_INFO_PATH[1])
            kill_list_template.lab_value.SetString(str(statisitcs.get('kill_mecha', 0)))
            kill_list_template.lab_name.SetString(287)
            if self.player_seq == index:
                player_info_template.btn_player.nd_content.lab_player_name.SetFontSize(22)
                player_info_template.btn_player.SetSelect(True)
                kill_list_len = list_data.GetItemCount()
                for index in range(kill_list_len):
                    lab_value = list_data.GetItem(index).lab_value
                    lab_value.SetFontSize(26)
                    lab_value.SetColor(5825279)
                    lab_value.EnableShadow(669266, 255, {'width': 2,'height': -2})

        return

    def init_map_img(self):
        size = self.panel.nd_content.nd_map.list_map.GetContainer().img_map.getContentSize()
        self.panel.nd_content.nd_map.list_map.GetContainer().img_map.SetDisplayFrameByPath('', self.map_img_path)
        self.panel.nd_content.nd_map.list_map.GetContainer().img_map.setContentSize(size)
        self.map_img_width = size.width
        self.map_img_height = size.height

    def add_event_list(self, index, player_seq, event):
        pos_list = event[2]
        if event[1] in (battle_const.CHART_EVENT_KILL_HUMAN, battle_const.CHART_EVENT_KILL_MECHA, battle_const.CHART_EVENT_KILL_GROUP):
            self.event_kill_banner_dict[index] = event[3]
            self.event_kill_banner_dict[index]['event_index'] = event[1]
        event_template = self.panel.nd_content.nd_info.list_event.AddTemplateItem(index=None, bRefresh=True)
        delta_time = event[0] - self.battle_begin_time
        event_template.lab_time_event.SetString('%02d:%02d' % (delta_time // 60, delta_time % 60))
        self.panel.nd_content.nd_info.list_event.jumpToBottom()
        event_template.PlayAnimation('show')
        btn = event_template.btn_event_data
        btn.SetText(self.settle_chart_img_info.get(str(event[1]), {}).get('iTextId', 301))
        btn.icon_event.SetDisplayFrameByPath('', self.settle_chart_img_info.get(str(event[1]), {}).get('cIconChartImgPath', ''))
        btn.SetEnable(False)
        btn.SetSelect(False)
        self.event_template_dict[index] = event_template
        img_pos_x, img_pos_z = self.trans_map_pos_to_img_pos(pos_list)
        self.add_map_mark(img_pos_x, img_pos_z, index, mark_type=event[1], player_seq=player_seq, is_self=True)
        self.add_event_desc(img_pos_x, img_pos_z, event[1], index)

        @btn.unique_callback()
        def OnClick(btn, touch, button_index=index):
            if self.event_kill_banner_dict.get(index, {}).get('event_index', -1) not in (battle_const.CHART_EVENT_KILL_HUMAN, battle_const.CHART_EVENT_KILL_MECHA, battle_const.CHART_EVENT_KILL_GROUP):
                self.show_kill_bar_disappear()
            else:
                self.init_kill_bar(index)
            if self.event_selected_index is not None:
                self.select_event(self.event_selected_index, False)
            self.select_event(button_index, True)
            self.event_selected_index = button_index
            return

        if not self.if_is_skip:
            self.show_event_on_map(index)
        return

    def select_event(self, button_index, selected):
        event_template = self.event_template_dict.get(button_index, None)
        event_icon = self.event_icon_dict.get(button_index, None)
        event_desc = self.event_desc_dict.get(button_index, None)
        if selected:
            if event_template is not None:
                event_template.img_choose.setVisible(True)
                event_template.btn_event_data.SetSelect(True)
            if event_icon is not None:
                event_icon.setLocalZOrder(DISPLAY_POINT_ZORDER)
                event_icon.nd_show.setVisible(True)
                event_icon.img_dot.setVisible(False)
                event_icon.PlayAnimation('show')
            if event_desc is not None:
                event_desc.setVisible(True)
                event_desc.PlayAnimation('show')
        else:
            if event_template is not None:
                event_template.btn_event_data.img_choose.setVisible(False)
                event_template.btn_event_data.SetSelect(False)
            if event_icon is not None:
                if button_index not in (0, len(self.fight_event) - 1):
                    event_icon.nd_show.setVisible(False)
                    event_icon.img_dot.setVisible(True)
                    event_icon.setLocalZOrder(SELF_NORMAL_POINT_ZORDER)
                else:
                    event_icon.setLocalZOrder(SELF_SPECIAL_POINT_ZORDER)
            if event_desc is not None:
                event_desc.setVisible(False)
        return

    def set_kill_bar(self, nd, photo_no, name):
        nd.lab_player_name.SetString(name)
        res_path = get_head_photo_res_path(photo_no)
        nd.cut_player.img_player.SetDisplayFrameByPath('', res_path)

    def init_kill_bar(self, index):
        extra_info = self.event_kill_banner_dict.get(index, {})
        event_index = extra_info.get('event_index', -1)
        killer_photo = extra_info.get('killer_photo', 11)
        victim_name = extra_info.get('victim_name', '')
        if event_index == -1:
            return
        else:
            self.bar_kill.lab_info.SetString(287 if event_index == battle_const.CHART_EVENT_KILL_MECHA else 286)
            if killer_photo > 8000:
                photo_no = self.get_phote_no(killer_photo, None)
            else:
                photo_no = self.get_phote_no(None, killer_photo)
            self.set_kill_bar(self.bar_kill.list_kill.GetItem(0), photo_no, self.char_name)
            if event_index == battle_const.CHART_EVENT_KILL_HUMAN or event_index == battle_const.CHART_EVENT_KILL_GROUP:
                victim_photo = extra_info.get('victim_photo', 11)
                photo_no = self.get_phote_no(None, victim_photo)
            else:
                victim_photo = extra_info.get('victim_photo', 8001)
                photo_no = self.get_phote_no(victim_photo, None)
            self.set_kill_bar(self.bar_kill.list_kill.GetItem(1), photo_no, victim_name)
            self.panel.PlayAnimation('show_kill')
            return

    def finish_draw_at_soon(self):
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)
            self.timer_id = None
        if self.event_selected_index is not None:
            self.select_event(self.event_selected_index, False)
        self.bar_kill.setVisible(False)
        self.draw_time = None
        self.has_finish_draw = False
        self.if_is_skip = True
        for key, value in six.iteritems(self.teammate_info):
            fight_event = value.get('fight_event', [])
            obj_id = str(key)
            player_seq = self.object_id_dic.get(obj_id, 0)
            lst_event = None
            if self.other_lst_line_container_index_dic.get(obj_id, None) is None:
                self.other_lst_line_container_index_dic[obj_id] = None
            if self.draw_line_by_time_teammate_index_dic.get(obj_id, None) is None:
                self.draw_line_by_time_teammate_index_dic[obj_id] = 0
            for index, event in enumerate(fight_event):
                if index != self.draw_line_by_time_teammate_index_dic[obj_id]:
                    continue
                now_event = event
                if index > 0:
                    lst_event = fight_event[index - 1]
                if now_event[1] != battle_const.CHART_EVENT_MOVE:
                    img_pos_x, img_pos_y = self.trans_map_pos_to_img_pos(now_event[2])
                    self.add_map_mark(img_pos_x, img_pos_y, index=index, mark_type=now_event[1], player_seq=player_seq, is_self=False)
                if lst_event is not None:
                    self.draw_all_line(lst_event, now_event, player_seq, False, 5, self.other_lst_line_container_index_dic[obj_id])
                self.other_lst_line_container_index_dic[obj_id] = None
                self.draw_line_by_time_teammate_index_dic[obj_id] += 1

        lst_event = None
        for index, event in enumerate(self.fight_event):
            if index != self.draw_line_by_time_self_index:
                continue
            now_event = event
            if index > 0:
                lst_event = self.fight_event[index - 1]
            if now_event[1] != battle_const.CHART_EVENT_MOVE:
                self.add_event_list(index, self.player_seq, now_event)
            if lst_event is not None:
                self.draw_all_line(lst_event, now_event, self.player_seq, True, 0, self.self_lst_line_container_index)
            self.self_lst_line_container_index = None
            self.draw_line_by_time_self_index += 1

        self.on_finish_draw()
        return

    def show_event_on_draw(self, button_index, show):
        if show:
            self.wait_show_tips = True
            self.event_selected_index = button_index
            self.select_event(button_index, show)
        else:
            self.wait_show_tips = False
            self.select_event(button_index, show)
            self.event_selected_index = None
        return

    def show_event_on_map(self, index):
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.show_event_on_draw(index, True)),
         cc.CallFunc.create(lambda : self.init_kill_bar(index)),
         cc.DelayTime.create(max(self.show_event_interval, self.panel.GetAnimationMaxRunTime('show_kill'))),
         cc.CallFunc.create(lambda : self.show_kill_bar_disappear()),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('disapear_kill')),
         cc.CallFunc.create(lambda : self.show_event_on_draw(index, False))]))

    def show_kill_bar_disappear(self):
        if self.bar_kill.isVisible():
            self.panel.PlayAnimation('disapear_kill')

    def add_map_mark(self, img_pos_x, img_pos_z, index, mark_type=0, player_seq=0, is_self=False):
        if mark_type in self.SPECIAL_ICON:
            icon_container_template = self.icon_container.AddItem(self.icon_template, None, bRefresh=False)
            icon_container_template.setAnchorPoint(cc.Vec2(0.5, 0.5))
            icon_container_template.setPosition(img_pos_x, img_pos_z)
            if mark_type == battle_const.CHART_EVENT_WIN:
                icon_container_template.icon_event.SetDisplayFrameByPath('', self.settle_chart_img_info.get(str(mark_type), {}).get('cIconMapImgPath', ''))
            else:
                icon_container_template.icon_event.SetDisplayFrameByPath('', self.settle_chart_img_info.get(str(mark_type), {}).get('cIconMapImgPath', '') % self.UI_COLOR[player_seq])
            if is_self:
                icon_container_template.setLocalZOrder(SELF_SPECIAL_POINT_ZORDER)
            else:
                icon_container_template.setLocalZOrder(OTHER_POINT_ZORDER)
            icon_container_template.setScale(1.0 / self.touch_layer.now_scale)
            icon_container_template.nd_icon.setVisible(False)
            icon_container_template.img_dot.setVisible(False)
            icon_container_template.nd_show.setVisible(True)
        else:
            if not is_self:
                return
            icon_container_template = self.icon_container.AddItem(self.icon_template, None, False)
            icon_container_template.setAnchorPoint(cc.Vec2(0.5, 0.5))
            icon_container_template.setPosition(img_pos_x, img_pos_z)
            icon_container_template.img_dot.SetDisplayFrameByPath('', self.UI_DOT_PATH % self.UI_COLOR[player_seq])
            icon_container_template.icon_event.SetDisplayFrameByPath('', self.settle_chart_img_info.get(str(mark_type), {}).get('cIconMapImgPath', ''))
            icon_container_template.bar_player.SetDisplayFrameByPath('', self.TEAMMATE_ICON_BACKGROUND_PATH % self.UI_COLOR[player_seq])
            icon_container_template.setScale(1.0 / self.touch_layer.now_scale)
            icon_container_template.img_dot.setVisible(True)
            icon_container_template.nd_show.setVisible(False)
            icon_container_template.setLocalZOrder(SELF_NORMAL_POINT_ZORDER)
        icon_container_template.setVisible(True)
        if is_self:
            self.event_icon_dict[index] = icon_container_template
        return

    def add_event_desc(self, img_pos_x, img_pos_z, event_num, index):
        desc_template = self.desc_container.AddItem(self.desc_template, None, False)
        desc_template.bar_tips.lab_event.SetString(self.settle_chart_img_info.get(str(event_num), {}).get('iTextId', 301))
        desc_template.bar_tips.lab_player_name.SetString(self.char_name)
        desc_template_size = desc_template.getContentSize()
        if img_pos_x + desc_template_size.width + 10 > self.panel.nd_content.nd_map.list_map.GetContainer().img_map.getPosition().x + self.map_img_width / 2:
            desc_template.setAnchorPoint(cc.Vec2(1, desc_template.getAnchorPoint().y))
        if img_pos_z < desc_template_size.height + 10:
            desc_template.setAnchorPoint(cc.Vec2(desc_template.getAnchorPoint().x, 0))
        desc_template.setPosition(img_pos_x, img_pos_z)
        desc_template.setScale(1.0 / self.touch_layer.now_scale)
        desc_template.setVisible(False)
        self.event_desc_dict[index] = desc_template
        return

    def add_line(self, start_pos, end_pos, player_seq=0, is_self=True, indent=0, line_index=0):
        if is_self:
            template_name = self.SELF_LINE_PATH % self.UI_COLOR[player_seq]
        else:
            template_name = self.OTHER_LINE_PATH % self.UI_COLOR[player_seq]
        return self.draw_line.draw(start_pos, end_pos, indent, template_name, line_index)

    def on_click_btn_next(self, *args):
        from logic.comsys.battle.Settle.SettleSystem import SettleSystem
        SettleSystem().show_settle_exp(self.settle_dict, self.reward)
        self.close()

    def on_click_btn_share(self, *args):
        self.finish_draw_at_soon()
        self.panel.DelayCall(0.2, self.on_click_btn_share_imp)

    def on_click_btn_share_imp(self):
        hide_ui_names = [
         self.__class__.__name__]
        if self.screen_capture_helper:

            def custom_cb(*args):
                self.panel.nd_content.nd_info.list_event.setVisible(True)
                self.panel.nd_content.nd_info.nd_share.setVisible(False)
                self.panel.nd_content.btn_next.setVisible(True)
                self.panel.nd_content.btn_share.setVisible(True and global_data.is_share_show)
                self.panel.nd_content.nd_info.bar_type.lab_type.SetString(288)

            self.panel.nd_content.btn_next.setVisible(False)
            self.panel.nd_content.btn_share.setVisible(False)
            self.screen_capture_helper.take_screen_shot(hide_ui_names, self.panel, custom_cb=custom_cb)

    def on_click_btn_skip(self, *args):
        self.panel.nd_content.nd_map.btn_skip.setVisible(False)
        self.if_is_skip = True
        self.finish_draw_at_soon()

    def on_click_btn_double_speed_play(self, *args):
        if self.skip_button_model == SKIP_BUTTON:
            self.panel.btn_skip.setVisible(False)
            self.time_mul *= 2
            self.show_event_interval /= 2.0
        else:
            self.skip_button_model = SKIP_BUTTON
            self.time_mul = self.settle_chart_based_info.get('cTimeMul', 50)
            self.show_event_interval = self.settle_chart_based_info.get('cEventShowInterval', 0.5)
            self.begin_draw_event_on_map()
            self.panel.nd_content.nd_map.btn_skip.lab_skip.SetString(332)

    def trans_map_pos_to_img_pos(self, pos_list):
        pos_x = pos_list[0]
        pos_z = pos_list[1]
        u = self.a_u * pos_x + self.b_u
        v = self.a_v * pos_z + self.b_v
        img_pos_x = u * self.map_img_width
        img_pos_z = v * self.map_img_height
        return (
         img_pos_x, img_pos_z)

    def init_share_panel(self):
        nd_share = self.panel.nd_share
        achievement_list_len = len(self.achievement_list)
        if achievement_list_len == 0:
            nd_share.img_empty.setVisible(True)
            nd_share.lab_empty.setVisible(True)
        else:
            share_template = global_data.uisystem.load_template(self.SHARE_TEMPLATE_PATH)
            for achievement in self.achievement_list:
                container = nd_share.cut_achievement.__getattribute__('list_achievement_%d' % random.randint(1, 4))
                template = container.AddItem(share_template, None, True)
                template.bar_achievement.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/settlement_chart/achievement/bar_end_chart_chievement_%d.png' % random.randint(1, 3))
                template.SetString(achievement)
                template.setFontSize(random.randint(18, 34))
                template.ChildResizeAndPosition()

        for index in range(1, 5):
            container = nd_share.cut_achievement.__getattribute__('list_achievement_%d' % index)
            for panel_cnt in range(0, 5):
                template = container.AddItem(share_template, None, True)
                template.bar_achievement.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/settlement_chart/achievement/bar_end_chart_chievement_%d.png' % random.randint(1, 3))
                template.SetString(self.achievement_list[random.randint(0, achievement_list_len - 1)])
                template.setFontSize(random.randint(18, 34))
                template.ChildResizeAndPosition()

            container.SetHorzIndent(random.randint(60, 70))
            container.SetHorzBorder(random.randint(-50, 5))
            container.RefreshItemPos()

        return

    def draw_line_event_by_time(self):
        next_event = False
        if not self.draw_time:
            self.draw_time = self.battle_begin_time
            if len(self.fight_event) > 0:
                self.draw_time = self.fight_event[0][0]
        if self.wait_show_tips and not self.if_is_skip:
            return
        else:
            self.draw_time += self.time_interval * self.time_mul
            for key, value in six.iteritems(self.teammate_info):
                fight_event = value.get('fight_event', [])
                obj_id = str(key)
                player_seq = self.object_id_dic.get(obj_id, 0)
                if self.other_lst_line_container_index_dic.get(obj_id, None) is None:
                    self.other_lst_line_container_index_dic[obj_id] = None
                if self.draw_line_by_time_teammate_index_dic.get(obj_id, None) is None:
                    self.draw_line_by_time_teammate_index_dic[obj_id] = 0
                index = self.draw_line_by_time_teammate_index_dic[obj_id]
                if index < len(fight_event):
                    next_event = True
                    now_event = fight_event[index]
                    if index > 0:
                        lst_event = fight_event[index - 1]
                        self.other_lst_line_container_index_dic[obj_id] = self.draw_part_line(lst_event, now_event, player_seq, False, 5, self.other_lst_line_container_index_dic[obj_id])
                    if self.draw_time > now_event[0]:
                        self.other_lst_line_container_index_dic[obj_id] = None
                        self.draw_line_by_time_teammate_index_dic[obj_id] += 1
                        if now_event[1] != battle_const.CHART_EVENT_MOVE:
                            img_pos_x, img_pos_y = self.trans_map_pos_to_img_pos(now_event[2])
                            self.add_map_mark(img_pos_x, img_pos_y, index=index, mark_type=now_event[1], player_seq=player_seq, is_self=False)

            if self.draw_line_by_time_self_index < len(self.fight_event):
                next_event = True
                now_event = self.fight_event[self.draw_line_by_time_self_index]
                index = self.draw_line_by_time_self_index
                if index > 0:
                    lst_event = self.fight_event[index - 1]
                    self.self_lst_line_container_index = self.draw_part_line(lst_event, now_event, self.player_seq, True, 0, self.self_lst_line_container_index)
                if self.draw_time >= now_event[0]:
                    self.self_lst_line_container_index = None
                    self.draw_line_by_time_self_index += 1
                    if now_event[1] != battle_const.CHART_EVENT_MOVE:
                        self.add_event_list(index, self.player_seq, now_event)
            if not next_event:
                self.on_finish_draw()
            return

    def draw_part_line(self, lst_event, now_event, player_seq, is_self, indent, line_index):
        start_pos_x, start_pos_z = self.trans_map_pos_to_img_pos(lst_event[2])
        next_end_pos_x, next_end_pos_z = self.trans_map_pos_to_img_pos(now_event[2])
        delta_time = now_event[0] - lst_event[0] + 1
        end_pos_x = start_pos_x + (next_end_pos_x - start_pos_x) * min((self.draw_time - lst_event[0]) / delta_time, 1.0)
        end_pos_z = start_pos_z + (next_end_pos_z - start_pos_z) * min((self.draw_time - lst_event[0]) / delta_time, 1.0)
        return self.add_line(cc.Vec2(start_pos_x, start_pos_z), cc.Vec2(end_pos_x, end_pos_z), player_seq, is_self, indent, line_index)

    def draw_all_line(self, lst_event, now_event, player_seq, is_self, indent, line_index=None):
        start_pos_x, start_pos_z = self.trans_map_pos_to_img_pos(lst_event[2])
        end_pos_x, end_pos_z = self.trans_map_pos_to_img_pos(now_event[2])
        return self.add_line(cc.Vec2(start_pos_x, start_pos_z), cc.Vec2(end_pos_x, end_pos_z), player_seq, is_self, indent, line_index)

    def on_finish_draw(self):
        self.has_finish_draw = True
        self.panel.nd_content.nd_map.btn_skip.lab_skip.SetString(316)
        self.if_is_skip = False
        self.panel.btn_skip_long.setVisible(False)
        self.panel.btn_next.setVisible(True)
        self.skip_button_model = RESTART_BUTTON
        self.panel.nd_content.nd_map.btn_skip.setVisible(True)
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)
            self.timer_id = None
        list_event = self.panel.nd_content.nd_info.list_event
        for index in range(0, list_event.GetItemCount()):
            list_event.GetItem(index).btn_event_data.SetEnable(True)

        return

    def get_map_info(self):
        scene_name = global_data.battle.get_scene_name()
        map_conf = self.settle_chart_info_dict.get('SettlementChartMapInfo', {}).get(scene_name, {})
        self.map_img_path = map_conf.get('cMapImgPath', 'gui/ui_res_2/battle/settlement_chart/img_end_chart_map.png')
        l_idx = map_conf.get('cLeftTrunkIndex', -32)
        r_idx = map_conf.get('cRightTrunkIndex', 31)
        btm_idx = map_conf.get('cBottomTrunkIndex', -32)
        up_idx = map_conf.get('cUpTrunkIndex', 31)
        trunk_size = map_conf.get('cTrunkSize', 832)
        self.a_u = 1.0 / trunk_size / (r_idx - l_idx + 1.0)
        self.b_u = -(l_idx - 0.5) / (r_idx - l_idx + 1.0)
        self.a_v = 1.0 / trunk_size / (up_idx - btm_idx + 1.0)
        self.b_v = -(btm_idx - 0.5) / (up_idx - btm_idx + 1.0)

    def get_phote_no(self, mecha_id, role_id):
        photo_no = get_mecha_photo(mecha_id)
        if not mecha_id:
            photo_no = get_role_default_photo(role_id)
        return photo_no

    def begin_draw_event_on_map(self):
        self.init_event_parameters()
        self.icon_container.DeleteAllSubItem()
        self.desc_container.DeleteAllSubItem()
        self.panel.nd_content.nd_info.list_event.DeleteAllSubItem()
        self.draw_line.delete_all_container()
        self.show_kill_bar_disappear()
        self.draw_time = None
        self.has_finish_draw = False
        self.panel.btn_next.setVisible(False)
        self.timer_id = global_data.game_mgr.register_logic_timer(self.draw_line_event_by_time, interval=self.time_interval, args=None, times=-1, mode=2)
        self.panel.btn_skip_long.setVisible(True)
        return

    def on_click_panel(self, *args):
        if self.event_selected_index is not None:
            self.select_event(self.event_selected_index, False)
            self.show_kill_bar_disappear()
            self.event_selected_index = None
        return