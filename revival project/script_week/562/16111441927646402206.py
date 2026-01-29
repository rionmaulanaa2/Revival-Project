# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LuckScore/LuckScoreRankBaseWidget.py
from common.const.uiconst import BASE_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import rank_const
from logic.gutils import role_head_utils
from logic.gcommon.common_const.luck_score_const import LUCK_SCORE_WEEK_TYPE, LUCK_SCORE_TOTAL_TYPE
from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_TEAM
from common.cfg import confmgr
import six
import cc
RANK_IMG_PATH = 'gui/ui_res_2/crew/img_crew_rank_{}.png'
RANK_PANEL_PATH = 'gui/ui_res_2/lottery/pnl_lottery_rank_{}.png'
RANK_MY_PANEL_PATH = 'gui/ui_res_2/lottery/pnl_lottery_rank_self.png'
RANK_NORMAL_PANEL_PATH = 'gui/ui_res_2/lottery/pnl_lottery_rank_others.png'

class LuckScoreRankBaseWidget(object):

    def __init__(self, panel, lottery_id=None, my_item=None, is_lottery_close=False):
        self.panel = panel
        self.lottery_id = lottery_id
        self._my_item = my_item
        self._is_lottery_close = is_lottery_close
        self.init_parameters()
        self.init_ui()
        self.init_event()
        self.refresh()

    def destroy(self):
        global_data.emgr.message_on_rank_data -= self.message_on_rank_data
        global_data.emgr.message_on_luck_rank_like_data -= self.on_likes_result
        self.panel.Destroy()
        self.panel = None
        self._cur_show_index = None
        self._data_list = []
        self._is_check_sview = None
        self._uid_2_item = {}
        self._my_item = None
        self._like_data_list = None
        return

    def setVisible(self, is_visible):
        if is_visible:
            self.show()
        else:
            self.hide()

    def hide(self):
        if self.panel:
            self.panel.setVisible(False)

    def show(self):
        self._cur_show_luck_type = self.luck_type
        global_data.player and global_data.player.request_rank_list(self.rank_type, 0, rank_const.RANK_ONE_REQUEST_MAX_COUNT, True)
        if self.panel:
            self.panel.setVisible(True)

    def init_parameters(self):
        self._cur_show_type = None
        self._cur_show_index = 0
        self._cur_select_item = None
        self._cur_select_index = None
        self._first_item = None
        self._data_list = []
        self._is_check_sview = False
        self._uid_2_item = {}
        continual_goods_id = confmgr.get('lottery_page_config', str(self.lottery_id), 'continual_goods_id')
        mall_conf = confmgr.get('mall_config', str(continual_goods_id), default={})
        loop_lottery_id = mall_conf.get('cGoodsInfo', {}).get('loop_lottery_id')
        self.item_no = int(loop_lottery_id) if loop_lottery_id else mall_conf.get('item_no')
        self._need_show_default = False
        self._like_data_list = {}
        return

    def init_ui(self):
        self.list_rank = self.panel.list_rank
        self.nd_empty = self.panel.nd_empty

        @self.list_rank.unique_callback()
        def OnScrolling(sender):
            if self._is_check_sview == False:
                self._is_check_sview = True
                self.panel.SetTimeOut(0.2, self.check_sview)

        self.list_rank.DeleteAllSubItem()
        self.list_rank_height = self.list_rank.getContentSize().height
        global_data.player and global_data.player.request_rank_list(self.rank_type, 0, rank_const.RANK_ONE_REQUEST_MAX_COUNT, True)

    def init_event(self):
        global_data.emgr.message_on_rank_data += self.message_on_rank_data
        global_data.emgr.message_on_luck_rank_like_data += self.on_likes_result

    def message_on_rank_data(self, rank_type):
        if self.rank_type == rank_type:
            self.refresh()

    def refresh(self):
        rank_data = global_data.message_data.get_rank_data(self.rank_type)
        if not rank_data:
            return
        if not rank_data['rank_list']:
            self.nd_empty.setVisible(True)
            self.list_rank.DeleteAllSubItem()
            self._my_item.setVisible(False)
            return
        self.nd_empty.setVisible(False)
        self._uid_2_item = {}
        self.refresh_my_item(rank_data['player_data'], rank_data['player_rank'])
        self.refresh_item_list(rank_data)
        if self._need_show_default:
            self.show_default_info()

    def show_default_info(self):
        rank_data = global_data.message_data.get_rank_data(self.rank_type)
        if not rank_data:
            self._need_show_default = True
            return
        rank_list = rank_data['rank_list']
        if len(rank_list) > 0:
            if self._cur_select_item and self._cur_select_item.isValid():
                self._cur_select_item.SetSelect(False)
            self._cur_select_index = 0
            first_data = rank_list[0]
            item_list, luck_score, timestamp, luck_intervene_weight, luck_exceed_percent = self._get_luck_data(first_data)
            player_data = {'uid': first_data[0],'name': str(first_data[1][0]),'frame_no': first_data[1][2],'photo_no': first_data[1][3]}
            self._show_record_open_box_widget(item_list, luck_score, timestamp, luck_intervene_weight, luck_exceed_percent, player_data, False)
            self._need_show_default = False

    def refresh_item_list(self, rank_data):
        self._data_list = rank_data['rank_list']
        self.list_rank.DeleteAllSubItem()
        data_count = len(self._data_list)
        self._cur_show_index = 0
        all_height = 0
        index = 0
        vert_indent = self.list_rank.GetVertIndent()
        while all_height < self.list_rank_height + 200 and index < data_count:
            data = self._data_list[index]
            item_widget = self.add_item_elem(data, index=index)
            all_height += item_widget.getContentSize().height + vert_indent
            index += 1

        self._cur_show_index = index - 1

    def refresh_my_item(self, data, rank):
        if not global_data.player:
            self._my_item.setVisible(False)
            return
        item_list = self.my_luck_dict.get('item_list', {})
        luck_score = self.my_luck_dict.get('luck_score', 0)
        timestamp = self.my_luck_dict.get('timestamp', 0)
        luck_intervene_weight = self.my_luck_dict.get('luck_intervene_weight', {})
        luck_exceed_percent = self.my_luck_dict.get('luck_exceed_percent', 0)
        if not item_list:
            self.list_rank.SetContentSize(472, 356)
            return
        self._my_item.setVisible(luck_score > 0)
        self.refresh_item_info(self._my_item, data, rank, True)
        player_data = {'uid': global_data.player.uid,'name': global_data.player.char_name,'frame_no': global_data.player.head_frame,'photo_no': global_data.player.head_photo}
        self.refresh_item_luck(self._my_item, item_list, luck_score, timestamp, luck_intervene_weight, luck_exceed_percent, player_data)
        self.refresh_item_likes(self._my_item, global_data.player.uid)
        self.init_ui_event(self._my_item, global_data.player.uid)
        self.list_rank.SetContentSize(472, 308)

    def check_sview(self):
        msg_count = len(self._data_list)
        self._cur_show_index = self.list_rank.AutoAddAndRemoveItem(self._cur_show_index, self._data_list, len(self._data_list), self.add_item_elem, 300, 300)
        self._is_check_sview = False
        if self._cur_show_index == msg_count - 1 and global_data.message_data.is_need_request_rank_data(self.rank_type):
            global_data.player and global_data.player.request_rank_list(self.rank_type, self._cur_show_index, self._cur_show_index + rank_const.RANK_ONE_REQUEST_MAX_COUNT, True)

    def add_item_elem(self, data, is_back_item=True, index=-1):
        if is_back_item:
            item = self.list_rank.AddTemplateItem(bRefresh=True)
        else:
            item = self.list_rank.AddTemplateItem(0, bRefresh=True)
        self._uid_2_item[data[0]] = item
        item.temp_red.setVisible(False)
        btn_choose = item.btn_choose
        btn_choose.EnableCustomState(True)
        if index == 0 and self._cur_select_index is None:
            btn_choose.SetSelect(True)
            self._cur_select_item = btn_choose
            self._cur_select_index = index
        elif self._cur_select_index == index:
            btn_choose.SetSelect(True)
            self._cur_select_item = btn_choose
        rank = int(data[3]) + 1
        self.refresh_item_info(item, data, rank, False)
        luck_data = data[1][self.luck_data_index]
        item_list, luck_score, timestamp, luck_intervene_weight, luck_exceed_percent = self._get_luck_data(data)
        uid = data[0]
        player_data = {'uid': uid,'name': str(data[1][0]),'frame_no': data[1][2],'photo_no': data[1][3]}
        self.refresh_item_luck(item, item_list, luck_score, timestamp, luck_intervene_weight, luck_exceed_percent, player_data, index)
        self.refresh_item_likes(item, uid)
        self.init_ui_event(item, uid)
        return item

    def _get_luck_data(self, data):
        luck_data = data[1][self.luck_data_index]
        item_list = luck_data.get(str(self.item_no), {}).get('item_list', {})
        luck_score = data[2][0]
        timestamp = luck_data.get(str(self.item_no), {}).get('timestamp', 0)
        luck_intervene_weight = luck_data.get(str(self.item_no), {}).get('luck_intervene_weight', {})
        luck_exceed_percent = luck_data.get(str(self.item_no), {}).get('luck_exceed_percent', 0)
        return (
         item_list, luck_score, timestamp, luck_intervene_weight, luck_exceed_percent)

    def init_ui_event(self, item, uid):

        @item.btn_like.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            luck_score_likes_list = global_data.player.get_luck_score_likes_data(self.item_no, self.luck_type)
            likes_data = luck_score_likes_list.get(uid, {'like_num': 0,'liked': False})
            if not likes_data['liked']:
                global_data.player.request_luck_rank_like(uid, self.item_no, self.luck_type)
                global_data.player.request_rank_all_likes([global_data.player.uid], self.item_no, self.luck_type)

    def refresh_item_info(self, item, data, rank, is_my):
        item.lab_player_name.setString(str(data[1][0]))
        role_head_utils.init_role_head(item.temp_head, data[1][2], data[1][3])
        self.add_player_simple_callback(item.temp_head, data[0], item.temp_head)
        if 1 <= rank <= 3:
            if is_my:
                item.bar_rank.SetDisplayFrameByPath('', RANK_MY_PANEL_PATH.format(rank))
            else:
                item.bar_rank.SetDisplayFrameByPath('', RANK_PANEL_PATH.format(rank))
            item.icon_rank.setVisible(True)
            item.icon_rank.SetDisplayFrameByPath('', RANK_IMG_PATH.format(rank))
            item.lab_rank.setVisible(False)
        else:
            if is_my:
                item.bar_rank.SetDisplayFrameByPath('', RANK_MY_PANEL_PATH.format(rank))
            else:
                item.bar_rank.SetDisplayFrameByPath('', RANK_NORMAL_PANEL_PATH)
            item.icon_rank.setVisible(False)
            item.lab_rank.setVisible(True)
            if rank == rank_const.RANK_DATA_OUTSIDE:
                text = get_text_by_id(15016)
            elif rank == rank_const.RANK_DATA_NONE:
                text = '-'
            else:
                text = str(rank)
            item.lab_rank.SetString(text)

    def refresh_item_luck(self, item, item_list, luck_score, timestamp, luck_intervene_weight, luck_exceed_percent, player_data, index=-1):
        item.lab_vale_lucky.SetString(str(int(luck_score)))

        @item.btn_choose.unique_callback()
        def OnClick(btn, touch):
            if self._cur_select_item and self._cur_select_item.isValid():
                self._cur_select_item.SetSelect(False)
            self._cur_select_item = item.btn_choose
            self._cur_select_item.SetSelect(True)
            self._cur_select_index = index
            self._show_record_open_box_widget(item_list, luck_score, timestamp, luck_intervene_weight, luck_exceed_percent, player_data, False)

        @item.btn_show.unique_callback()
        def OnClick(btn, touch):
            if self._cur_select_item and self._cur_select_item.isValid():
                self._cur_select_item.SetSelect(False)
            self._cur_select_item = item.btn_choose
            self._cur_select_item.SetSelect(True)
            self._cur_select_index = index
            self._show_record_open_box_widget(item_list, luck_score, timestamp, luck_intervene_weight, luck_exceed_percent, player_data, True)
            self._need_show_default = True

    def _show_record_open_box_widget(self, item_list, luck_score, timestamp, luck_intervene_weight, luck_exceed_percent, player_data, is_detail):
        if not item_list:
            global_data.game_mgr.show_tip(get_text_by_id(634790))
            return
        reward_list = []
        chips_data = {}
        for index, reward_dict in enumerate(item_list):
            item_dict = reward_dict.get('item_dict', {})
            chips_source = reward_dict.get('chips_source', {})
            for item_no, item_num in six.iteritems(item_dict):
                origin_data = []
                if chips_source and item_no in chips_source:
                    chip_source_data = chips_source[item_no]
                    for origin_item_no in six.iterkeys(chip_source_data):
                        origin_item_num, _ = chip_source_data[origin_item_no]
                        reward_list.append([origin_item_no, origin_item_num])
                        break

                else:
                    reward_list.append([item_no, item_num])

        extra_info = {'luck_score': luck_score,
           'luck_timestamp': timestamp,
           'luck_intervene_weight': luck_intervene_weight,
           'luck_exceed_percent': luck_exceed_percent
           }
        if is_detail:
            from logic.comsys.lottery.LotteryNew.LotteryResultUI import LotteryResultUI
            lottery_result_ui = LotteryResultUI(is_my=False)
            lottery_result_ui.set_box_items(reward_list, {}, extra_info, self.lottery_id, player_data)
        else:
            global_data.emgr.on_show_record_open_box_widget_event.emit(reward_list, {}, extra_info)

    def refresh_item_likes(self, item, uid, likes_data=None):
        if self._is_lottery_close:
            item.btn_like.setVisible(False)
            item.temp_red.setVisible(False)
            item.lab_vale_like.setVisible(False)
            return
        else:
            if likes_data == None:
                luck_score_likes_list = global_data.player.get_luck_score_likes_data(self.item_no, self.luck_type) if global_data.player else {}
                likes_data = luck_score_likes_list.get(uid, {'like_num': 0,'liked': False})
            icon_like = item.btn_like.icon_like
            red_dot = item.temp_red
            item.lab_vale_like.SetString(str(likes_data['like_num']))
            has_red_point = self.check_red_point()
            if likes_data['liked']:
                icon_like.SetDisplayFrameByPath('', 'gui/ui_res_2/lottery/btn_lottery_like_2.png')
                red_dot.setVisible(False)
            else:
                icon_like.SetDisplayFrameByPath('', 'gui/ui_res_2/lottery/btn_lottery_like_0.png')
                red_dot.setVisible(has_red_point)
            return

    def on_likes_result(self, luck_type):
        if not global_data.player:
            return
        if luck_type == self.luck_type:
            luck_score_likes_list = global_data.player.get_luck_score_likes_data(self.item_no, self.luck_type)
            for uid, item in self._uid_2_item.items():
                likes_data = luck_score_likes_list.get(uid)
                if item and item.isValid():
                    self.refresh_item_likes(item, uid, likes_data)

            if self._my_item and self._my_item.isValid():
                my_player_uid = global_data.player.uid
                self.refresh_item_likes(self._my_item, my_player_uid, luck_score_likes_list.get(my_player_uid))

    def add_player_simple_callback(self, panel, uid, pos_panel):

        @panel.unique_callback()
        def OnClick(*args):
            if global_data.player and uid == global_data.player.uid:
                return
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            if ui:
                ui.del_btn(BTN_TYPE_TEAM)
                ui.hide_btn_chat()
                ui.refresh_by_uid(uid)
                ui.need_close_history_ui = True
                w, h = pos_panel.GetContentSize()
                pos = pos_panel.ConvertToWorldSpace(w + 50, h)
                ui.set_position(cc.Vec2(pos.x, pos.y), cc.Vec2(0.0, 1.0))