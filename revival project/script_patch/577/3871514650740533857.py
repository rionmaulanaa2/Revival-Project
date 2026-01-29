# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/RecordOpenBoxUI.py
import cc
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_CUSTOM
from logic.gcommon.common_const import scene_const
from logic.client.const import lobby_model_display_const
from common.utils.cocos_utils import neox_pos_to_cocos
from logic.gutils.reward_item_ui_utils import refresh_item_info, smash_item_info
from logic.gcommon.item.item_const import ITEM_NO_EXP, ITEM_NO_BATTLEPASS_POINT
from logic.client.const.mall_const import CONTINUAL_LOTTERY_COUNT
from common.utils.timer import LOGIC
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon import time_utility
from common.cfg import confmgr
from logic.gutils import role_head_utils
from logic.gcommon.cdata.luck_score_config import NORMAL_LUCK_SCORE_EDGE, MIN_LUCK_SCORE_PERCENT, LOTTERY_COUNT_SHOW_BAODI
BOX_WIDGET_PATH = 'mall/i_lottery_reward_item'
TOTAL_COUNT = 10
FRIEND_SHARE = 0
CLAN_SHARE = 1
CHAT_SHARE = 2
SHARE_INFO = (
 (
  FRIEND_SHARE, 601014),
 (
  CLAN_SHARE, 601015),
 (
  CHAT_SHARE, 601016))
SEND_CD = 60

class RecordOpenBoxUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/open_box'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CUSTOM
    IS_FULLSCREEN = True

    def hide(self, *args):
        super(RecordOpenBoxUI, self).hide()

    def show(self, *args):
        super(RecordOpenBoxUI, self).show()
        self._reset_box_widgets_position()

    def on_init_panel(self):
        self.box_widget = dict()
        self.init_parameters()

    def init_parameters(self):
        self._player_data = None
        self._luck_score = None
        self._timestamp = None
        self._luck_intervene_weight = None
        self._luck_exceed_percent = None
        self._lottery_id = None
        self.model_list = list()
        self.lottery_result = dict()
        self.total_count = TOTAL_COUNT
        self._last_send_time_list = dict()
        return

    def on_resolution_changed(self):
        self._reset_box_widgets_position()

    def _reset_box_widgets_position(self):
        if not self.box_widget or not self.model_list:
            return
        camera = self.scene.active_camera
        for i in range(self.total_count):
            model = self.model_list[i]
            widget = self.box_widget[i]
            if model.valid:
                x, y = camera.world_to_screen(model.world_position)
                x, y = neox_pos_to_cocos(x, y)
                pos = self.panel.convertToNodeSpace(cc.Vec2(x, y))
                widget.SetPosition(pos.x, pos.y)

    def _init_box_widget(self, cur_id):
        dlg = self.box_widget.get(cur_id) or global_data.uisystem.load_template_create(BOX_WIDGET_PATH, parent=self.panel)
        self.box_widget[cur_id] = dlg

        @dlg.temp_reward.btn_choose.unique_callback()
        def OnBegin(btn, touch, *args):
            self.on_begin_box_widget(touch, cur_id)

        @dlg.temp_reward.btn_choose.unique_callback()
        def OnEnd(*args):
            self.on_end_box_widget()

        @dlg.nd_smash_item.btn_choose.unique_callback()
        def OnBegin(btn, touch, *args):
            self.on_begin_box_widget(touch, cur_id)

        @dlg.nd_smash_item.btn_choose.unique_callback()
        def OnEnd(*args):
            self.on_end_box_widget()

    def on_begin_box_widget--- This code section failed: ---

 104       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'False'
           6  LOAD_GLOBAL           1  'False'
           9  CALL_FUNCTION_3       3 
          12  POP_JUMP_IF_FALSE    19  'to 19'

 105      15  LOAD_CONST            0  ''
          18  RETURN_END_IF    
        19_0  COME_FROM                '12'

 106      19  LOAD_GLOBAL           2  'True'
          22  LOAD_FAST             0  'self'
          25  STORE_ATTR            3  'item_desc_showing'

 107      28  LOAD_FAST             0  'self'
          31  LOAD_ATTR             4  'lottery_result'
          34  LOAD_FAST             2  'box_id'
          37  BINARY_SUBSCR    
          38  LOAD_CONST            2  ''
          41  BINARY_SUBSCR    
          42  STORE_FAST            3  'item_id'

 108      45  LOAD_FAST             1  'touch'
          48  LOAD_ATTR             5  'getLocation'
          51  CALL_FUNCTION_0       0 
          54  STORE_FAST            4  'position'

 109      57  LOAD_GLOBAL           6  'global_data'
          60  LOAD_ATTR             7  'emgr'
          63  LOAD_ATTR             8  'show_item_desc_ui_event'
          66  LOAD_ATTR             9  'emit'
          69  LOAD_FAST             3  'item_id'
          72  LOAD_CONST            0  ''
          75  LOAD_CONST            3  'directly_world_pos'
          78  LOAD_FAST             4  'position'
          81  LOAD_CONST            4  'extra_info'
          84  BUILD_MAP_1           1 
          87  LOAD_GLOBAL           1  'False'
          90  LOAD_CONST            5  'show_jump'
          93  STORE_MAP        
          94  CALL_FUNCTION_514   514 
          97  POP_TOP          

 110      98  LOAD_FAST             0  'self'
         101  LOAD_ATTR            11  'panel'
         104  LOAD_ATTR            12  'nd_bg'
         107  LOAD_ATTR            13  'setTouchEnabled'
         110  LOAD_GLOBAL           1  'False'
         113  CALL_FUNCTION_1       1 
         116  POP_TOP          
         117  LOAD_CONST            0  ''
         120  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9

    def on_end_box_widget(self):
        global_data.emgr.hide_item_desc_ui_event.emit()
        self.panel.nd_bg.setTouchEnabled(True)
        self.item_desc_showing = False

    def on_finalize_panel(self):
        global_data.emgr.leave_current_scene.emit()
        self.show_main_ui()
        for index, model in enumerate(self.model_list):
            if model.valid:
                model.visible = True

        self._player_data = None
        self._luck_score = None
        self._timestamp = None
        self._luck_intervene_weight = None
        self._luck_exceed_percent = None
        self._lottery_id = None
        self.box_widget = None
        self.lottery_result = None
        return

    def set_box_items(self, temp_items, luck_score, extra_info, player_data, lottery_id):
        items = {}
        for index, value in temp_items.items():
            items[int(index)] = value

        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video()
        self.hide_main_ui()
        self._luck_score = int(luck_score)
        self._player_data = player_data
        self._timestamp = extra_info.get('luck_timestamp')
        self._luck_intervene_weight = extra_info.get('luck_intervene_weight')
        self._luck_exceed_percent = extra_info.get('luck_exceed_percent')
        self._lottery_id = lottery_id
        ui = global_data.ui_mgr.get_ui('LuckScoreRankListUI')
        if ui:
            ui.hide()
        global_data.ui_mgr.close_ui('ScreenLockerUI')
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_LOTTERY, lobby_model_display_const.LOTTERY)
        self.total_count = len(items)
        if self.total_count > TOTAL_COUNT:
            self.total_count = TOTAL_COUNT
        for i in range(TOTAL_COUNT):
            if i >= self.total_count:
                break
            self.lottery_result[i] = items[i]
            self._init_box_widget(i)
            refresh_item_info(self.box_widget[i], max_len=11, *self.lottery_result[i])

        for i in range(1, 11):
            model = self.scene.get_model('niudan_%02d' % i)
            if model and model.valid:
                model.visible = False
                self.model_list.append(model)

        global_data.game_mgr.register_logic_timer(self._reset_box_widgets_position, times=1, interval=2, mode=LOGIC)
        self._update_panel()

    def _update_panel(self):
        self.panel.lab_rule.setVisible(False)
        self.panel.lab_tips.setVisible(False)
        self.panel.lab_tips2.setVisible(False)
        self.panel.btn_sure.setVisible(False)
        self.panel.btn_once.setVisible(False)
        self.panel.btn_many_times.setVisible(False)
        if len(self.lottery_result) == CONTINUAL_LOTTERY_COUNT:
            self.panel.temp_lucky.setVisible(True)
            temp_path = 'mall/luck/i_mall_luck_value_others'
            temp_lucky = global_data.uisystem.load_template_create(temp_path, parent=self.panel.temp_lucky, name='lucky')
            self.panel.temp_lucky.setLocalZOrder(100)
            self._update_other_record(temp_lucky)

    def _update_other_record(self, widget):
        nd_player_info = widget.nd_player_info_1
        name = self._player_data.get('name', global_data.player.get_name())
        nd_player_info.lab_name.setString(name)
        frame_no = self._player_data.get('frame_no', global_data.player.get_head_frame())
        photo_no = self._player_data.get('photo_no', global_data.player.get_head_photo())
        role_head_utils.init_role_head(nd_player_info.temp_head, frame_no, photo_no)
        uid = self._player_data.get('uid', global_data.player.uid)
        nd_player_info.lab_id.setString(get_text_by_id(80623) + str(uid))
        bar_value = widget.temp_lucky_value.nd_tips.bar_value
        lab_lucky = bar_value.lab_lucky
        lab_lucky.setVisible(True)
        lab_value_lucky = lab_lucky.nd_auto_fit.lab_value_lucky
        lab_value_lucky.setString(str(self._luck_score))
        lab_value_lucky.SetColor(16772438 if self._luck_score >= NORMAL_LUCK_SCORE_EDGE else 4650239)
        lab_value_lucky.setVisible(True)
        lab_tips_lottery = bar_value.lab_tips_lottery
        luck_intervene_weight_list = self._luck_intervene_weight
        luck_exceed_percent = self._luck_exceed_percent
        if luck_intervene_weight_list:
            value = next(iter(luck_intervene_weight_list.values()))
            if value <= LOTTERY_COUNT_SHOW_BAODI:
                lab_tips_lottery.setString(get_text_by_id(634637).format(value))
                lab_tips_lottery.setVisible(True)
            elif value > LOTTERY_COUNT_SHOW_BAODI or luck_exceed_percent >= MIN_LUCK_SCORE_PERCENT:
                lab_tips_lottery.setString(get_text_by_id(634753).format(luck_exceed_percent))
                lab_tips_lottery.setVisible(True)
            else:
                lab_tips_lottery.setVisible(False)
        elif luck_exceed_percent >= MIN_LUCK_SCORE_PERCENT:
            lab_tips_lottery.setString(get_text_by_id(634753).format(luck_exceed_percent))
            lab_tips_lottery.setVisible(True)
        else:
            lab_tips_lottery.setVisible(False)
        lab_day = widget.lab_day
        if self._timestamp is None:
            lab_day.setString('')
        else:
            from logic.gcommon import time_utility
            date_str = time_utility.get_date_str('%Y.%m.%d %H:%M:%S', int(self._timestamp))
            lab_day.setString(get_text_by_id(634759).format(date_str))

        @widget.btn_close.callback()
        def OnClick(btn, touch):
            self._on_click_close()

        @widget.temp_btn_lottery.btn_major.callback()
        def OnClick(btn, touch):
            self._on_click_btn_lottery()

        return

    def _on_click_close(self):
        ui = global_data.ui_mgr.get_ui('LuckScoreRankListUI')
        if ui:
            ui.show()
        self.close()

    def _on_click_btn_lottery(self):
        lottery_id = self._lottery_id
        self.close()
        ui = global_data.ui_mgr.get_ui('LuckScoreRankListUI')
        if ui:
            ui.close()
        from logic.gutils import jump_to_ui_utils
        jump_to_ui_utils.jump_to_lottery(lottery_id)