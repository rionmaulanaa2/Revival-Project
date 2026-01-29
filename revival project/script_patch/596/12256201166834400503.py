# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/SandTableUI.py
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from common.uisys.basepanel import BasePanel
from common.const import uiconst
import cc
from logic.comsys.common_ui import InputBox
from logic.comsys.map.map_widget.MapScaleInterface import ChartLine
from common.cfg import confmgr
import json

class SandtableUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/sandtable_chart/sandtable_chart'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = BasePanel.UI_ACTION_EVENT.copy()
    UI_ACTION_EVENT.update({'input_confirm_btn.OnClick': 'on_click_input_confirm_btn',
       'btn_close.OnClick': 'on_click_btn_close',
       'btn_play.OnClick': 'on_click_btn_play',
       'btn_set_cheat.OnClick': 'on_click_btn_set_cheat',
       'btn_remove_inspect.OnClick': 'on_remove_inspect',
       'btn_next.OnClick': 'on_click_btn_next'
       })
    UI_COLOR = [
     'blue', 'green', 'yellow', 'pink', 'gray']
    UI_TEXT_COLOR = ['#SB', '#SG', '#SO', '#SP', '#DC']
    SELF_LINE_PATH = 'end/i_end_settlement_chart_line_%s'
    OTHER_LINE_PATH = 'end/i_end_settlement_chart_line_%s2'
    PLAY_STEP = 10
    PLAY_INTV = 0.5

    def on_init_panel(self):
        self._init_parameters()
        self.damage_info_list = self.panel.nd_damage_view.player_damage_info_list
        self.record = None
        self.record_scene_name = None
        self.battle_id = None
        self.cheat_mark_record = None
        self.record_list = []
        self.record_dict = {}
        self.record_num = 0
        self.now_record_idx = 0
        self.cheat_mark_record_dict = {}
        self.cheat_mark_record = {}
        self._init_cheat_mark_record()
        self.idx_to_uid = {}
        self.uid_to_idx = {}
        self._draw_node = cc.DrawNode.create()
        self.draw_line = ChartLine(self.panel.nd_content.nd_map.list_map.GetContainer().img_map.line, 1)
        self.panel.nd_content.nd_map.list_map.GetContainer().img_map.line.addChild(self._draw_node)
        self.record_input_box = InputBox.InputBox(self.panel.nd_input.record_input, max_length=999999, placeholder='\xe8\xbe\x93\xe5\x85\xa5record')
        self._init_damage_view()
        self._init_input()
        self._init_solve()
        return

    def _init_parameters(self):
        self.map_img_width = None
        self.map_img_height = None
        self.settle_chart_info_dict = confmgr.get('c_settlement_chart')
        self.settle_chart_img_info = self.settle_chart_info_dict.get('SettlementChartImgInfo', {})
        self.settle_chart_based_info = self.settle_chart_info_dict.get('SettlementChartBasedInfo', {})
        self.selected_idx = -1
        self.time_mul = self.settle_chart_based_info.get('cTimeMul', 50)
        self.time_interval = self.settle_chart_based_info.get('cTimeInterval', 0.2)
        self.show_event_interval = self.settle_chart_based_info.get('cEventShowInterval', 0.5)
        self.record_start_time = 0
        self.record_end_time = 0
        self.record_time_stamps = []
        return

    def _init_cheat_mark_record(self):
        self.cheat_mark_record.update({0: False,
           1: False,
           2: False,
           3: False,
           4: False
           })

    def _init_damage_view(self):
        for idx in range(5):
            self.damage_info_list.GetItem(idx).setVisible(False)
            btn = self.damage_info_list.GetItem(idx).player_btn
            btn.btn_text.SetString(str(idx))
            btn.btn_text.SetColor(self.UI_TEXT_COLOR[idx])
            damage = self.damage_info_list.GetItem(idx).damage
            damage.mecha_damage.SetColor(self.UI_TEXT_COLOR[idx])
            damage.human_damage.SetColor(self.UI_TEXT_COLOR[idx])
            hurt = self.damage_info_list.GetItem(idx).hurt
            hurt.mecha_hurt.SetColor(self.UI_TEXT_COLOR[idx])
            hurt.human_hurt.SetColor(self.UI_TEXT_COLOR[idx])
            self.set_btn_idx(btn, idx)

    def _init_cheat_mark_icon(self):
        for idx in range(5):
            self.damage_info_list.GetItem(idx).cheat_mark.setVisible(False)

    def set_btn_idx(self, btn, idx):

        @btn.callback()
        def OnClick(*args):
            self.on_click_player_btn(idx)

    def _init_input(self):
        pass

    def _init_solve(self):
        pass

    def decode_record(self, record):
        if not record:
            return
        record_list = record.split('[SAND_TABLE_RECORD]')[1:]
        self.record_dict = {}
        self.record_num = len(record_list)
        self.now_record_idx = 0
        self._init_cheat_mark_record()
        self._init_cheat_mark_icon()
        for idx, record in enumerate(record_list):
            self.record_dict[idx] = record

        global_data.game_mgr.show_tip('\xe8\xa7\xa3\xe6\x9e\x90\xe5\xae\x8c\xe6\xaf\x95\xef\xbc\x8c\xe5\x85\xb1{}\xe6\x9d\xa1\xe8\xae\xb0\xe5\xbd\x95'.format(self.record_num))

    def decode_child_record(self, idx):
        record = self.record_dict.get(idx, {})
        if not record:
            return False
        battle_id = record.split('battle:')[1].split('_')[0]
        scene_name = record.split(',scene:')[1].split('_')[0]
        js_dict = record.split(',record:')[1]
        self.record = json.loads(js_dict)
        self.record_scene_name = scene_name
        self.battle_id = battle_id
        self.now_record_idx = idx
        idx = 0
        self.idx_to_uid = {}
        self.uid_to_idx = {}
        for uid in self.record.keys():
            if uid in self.idx_to_uid:
                continue
            self.idx_to_uid[idx] = uid
            self.uid_to_idx[uid] = idx
            idx += 1

        self.record_start_time, self.record_end_time, self.record_time_stamps = self.get_timestamp()
        self.draw_record()
        self.on_click_player_btn(0)
        return True

    def on_click_btn_next(self, *args):
        self.cheat_mark_record_dict[self.now_record_idx] = self.cheat_mark_record
        idx = self.now_record_idx + 1
        if idx >= self.record_num:
            global_data.game_mgr.show_tip('\xe8\xae\xb0\xe5\xbd\x95\xe5\xae\x8c\xe6\xaf\x95')
            self.panel.nd_content.nd_result.setVisible(True)
            result_txt = self.panel.nd_content.nd_result.result_lable
            result_txt.SetString('\xe7\xbb\x93\xe6\x9e\x9c\xef\xbc\x9a{}'.format(self.cheat_mark_record_dict))
        elif not self.decode_child_record(idx):
            global_data.game_mgr.show_tip('\xe8\xa7\xa3\xe6\x9e\x90\xe5\xa4\xb1\xe8\xb4\xa5')

    def on_click_input_confirm_btn(self, *args):
        self.panel.nd_content.nd_result.setVisible(False)
        self.cheat_mark_record_dict = {}
        self.decode_record(self.record_input_box.get_text())
        if self.record_num <= 0:
            global_data.game_mgr.show_tip('\xe6\xb2\xa1\xe6\x9c\x89\xe6\x9c\x89\xe6\x95\x88\xe7\x9a\x84\xe8\xae\xb0\xe5\xbd\x95')
            return
        if not self.decode_child_record(0):
            global_data.game_mgr.show_tip('\xe8\xa7\xa3\xe6\x9e\x90\xe5\xa4\xb1\xe8\xb4\xa5')
            return
        if not self.record:
            return

    def get_timestamp(self):
        if not self.record:
            return (0, 0, [])
        else:
            min_stamp = None
            max_stamp = None
            for uid, record in self.record.items():
                fight_event = record.get('fight_event', [])
                for event in fight_event:
                    if min_stamp is None or max_stamp is None:
                        min_stamp = event[0]
                        max_stamp = event[0]
                    else:
                        min_stamp = min(event[0], min_stamp)
                        max_stamp = max(event[0], max_stamp)

            time_gap = max_stamp - min_stamp
            play_gap = time_gap / self.PLAY_STEP
            time_stamps = []
            for i in range(self.PLAY_STEP):
                if i == self.PLAY_STEP - 1:
                    time_stamps.append(max_stamp + 1)
                else:
                    time_stamps.append(min_stamp + i * play_gap)

            return (
             min_stamp, max_stamp, time_stamps)

    def on_click_btn_play(self, *args):
        self.play_to_timestamp(0)

    def play_to_timestamp(self, idx):
        self.draw_part_record(self.record_time_stamps[idx])
        if idx + 1 < self.PLAY_STEP:
            self.panel.DelayCall(self.PLAY_INTV, lambda : self.play_to_timestamp(idx + 1))

    def on_click_player_btn(self, s_idx):
        s_uid = self.idx_to_uid[s_idx]
        self.selected_idx = s_idx
        global_data.game_mgr.show_tip('uid:{}'.format(s_uid))
        for idx in range(5):
            if idx not in self.idx_to_uid:
                self.damage_info_list.GetItem(idx).setVisible(False)
                continue
            self.damage_info_list.GetItem(idx).setVisible(True)
            if s_idx == idx:
                self.damage_info_list.GetItem(idx).player_btn.SetSelect(True)
                self.damage_info_list.GetItem(idx).damage.setVisible(False)
                self.damage_info_list.GetItem(idx).hurt.setVisible(False)
            else:
                self.damage_info_list.GetItem(idx).player_btn.SetSelect(False)
                self.damage_info_list.GetItem(idx).damage.setVisible(True)
                self.damage_info_list.GetItem(idx).hurt.setVisible(True)
                uid = self.idx_to_uid[idx]
                damage_msg = self.record[uid]['hurt_msg'].get(s_uid, {})
                self.damage_info_list.GetItem(idx).damage.mecha_damage.SetString('\xe6\x9c\xba\xe7\x94\xb2\xe9\x80\xa0\xe4\xbc\xa4:{}'.format(int(damage_msg.get('mecha_damage', 0))))
                self.damage_info_list.GetItem(idx).damage.human_damage.SetString('\xe5\xb0\x8f\xe4\xba\xba\xe9\x80\xa0\xe4\xbc\xa4:{}'.format(int(damage_msg.get('human_damage', 0))))
                hurt_msg = self.record[s_uid]['hurt_msg'][uid]
                self.damage_info_list.GetItem(idx).hurt.mecha_hurt.SetString('\xe6\x9c\xba\xe7\x94\xb2\xe6\x89\xbf\xe4\xbc\xa4:{}'.format(int(hurt_msg.get('mecha_damage', 0))))
                self.damage_info_list.GetItem(idx).hurt.human_hurt.SetString('\xe5\xb0\x8f\xe4\xba\xba\xe6\x89\xbf\xe4\xbc\xa4:{}'.format(int(hurt_msg.get('human_damage', 0))))

        self.draw_record(s_idx)

    def on_click_btn_set_cheat(self, *args):
        idx = self.selected_idx
        self.cheat_mark_record[idx] = False if self.cheat_mark_record[idx] is True else True
        self.damage_info_list.GetItem(idx).cheat_mark.setVisible(self.cheat_mark_record[idx])

    def on_click_btn_close(self, *args):
        self.close()

    def draw_record(self, s_idx=-1):
        self.get_map_info()
        self._init_map_img()
        self.draw_line.delete_all_container()
        for player_idx, player_uid in self.idx_to_uid.items():
            _record = self.record.get(player_uid, None)
            if not _record:
                continue
            last_event = None
            self.line_idx_dict.setdefault(player_idx, None)
            fight_event_list = _record.get('fight_event', [])
            for idx, value in enumerate(fight_event_list):
                if idx == 0:
                    last_event = value
                else:
                    new_event = value
                    self.draw_all_line(last_event, new_event, player_idx, player_idx == s_idx, 0, self.line_idx_dict[player_idx])
                    last_event = value

        return

    def draw_part_record(self, time_stamp=-1):
        self.get_map_info()
        self._init_map_img()
        self.draw_line.delete_all_container()
        for player_idx, player_uid in self.idx_to_uid.items():
            _record = self.record.get(player_uid, None)
            if not _record:
                continue
            last_event = None
            self.line_idx_dict.setdefault(player_idx, None)
            fight_event_list = _record.get('fight_event', [])
            for idx, value in enumerate(fight_event_list):
                if value[0] > time_stamp:
                    continue
                if idx == 0:
                    last_event = value
                else:
                    new_event = value
                    self.draw_all_line(last_event, new_event, player_idx, player_idx == self.selected_idx, 0, self.line_idx_dict[player_idx])
                    last_event = value

        return

    def _init_map_img(self):
        img_map = self.panel.nd_content.nd_map.list_map.GetContainer().img_map
        size = img_map.getContentSize()
        img_map.SetDisplayFrameByPath('', self.map_img_path)
        img_map.setContentSize(size)
        self.map_img_width = size.width
        self.map_img_height = size.height
        self.line_idx_dict = {}

    def get_map_info(self):
        scene_name = self.record_scene_name
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

    def trans_map_pos_to_img_pos(self, pos_list):
        pos_x = pos_list[0]
        pos_z = pos_list[1]
        u = self.a_u * pos_x + self.b_u
        v = self.a_v * pos_z + self.b_v
        img_pos_x = u * self.map_img_width
        img_pos_z = v * self.map_img_height
        return (
         img_pos_x, img_pos_z)

    def draw_all_line(self, lst_event, now_event, player_seq, is_self, indent, line_index=None):
        start_pos_x, start_pos_z = self.trans_map_pos_to_img_pos(lst_event[2])
        end_pos_x, end_pos_z = self.trans_map_pos_to_img_pos(now_event[2])
        return self.add_line(cc.Vec2(start_pos_x, start_pos_z), cc.Vec2(end_pos_x, end_pos_z), player_seq, is_self, indent, line_index)

    def add_line(self, start_pos, end_pos, player_seq=0, is_self=True, indent=0, line_index=0):
        if is_self:
            template_name = self.SELF_LINE_PATH % self.UI_COLOR[player_seq]
        else:
            template_name = self.OTHER_LINE_PATH % self.UI_COLOR[player_seq]
        return self.draw_line.draw(start_pos, end_pos, indent, template_name, line_index)