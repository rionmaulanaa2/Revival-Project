# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryNew/LotteryResultUI.py
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_CUSTOM
from logic.comsys.lottery.LotteryBuyWidget import LotteryBuyWidget
from logic.client.const.mall_const import SINGLE_LOTTERY_COUNT, CONTINUAL_LOTTERY_COUNT, DEF_PRICE_COLOR
from logic.gcommon.cdata.luck_score_config import NORMAL_LUCK_SCORE_EDGE, MIN_LUCK_SCORE_PERCENT, LOTTERY_COUNT_SHOW_BAODI
from logic.gcommon import time_utility
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.platform.dctool.interface import is_mainland_package
from logic.gcommon.common_const.chat_const import CHAT_FRIEND, CHAT_CLAN, CHAT_WORLD, MSG_TYPE_LUCKY_LOTTERY
from common.const.property_const import U_ID, U_LV, CLAN_ID, C_NAME
from .RecordOpenBoxWidgetNew import RecordOpenBoxWidgetNew, SHOW_CHIPS_TYPE_NONE, SHOW_CHIPS_TYPE_ANIM
from logic.gutils.role_head_utils import init_role_head
from logic.gutils import mall_utils
from common.cfg import confmgr
import six
TOTAL_COUNT = 10
FRIEND_SHARE = 0
CLAN_SHARE = 1
CHAT_SHARE = 2
SHARE_INFO = (
 (
  FRIEND_SHARE, 634662),
 (
  CLAN_SHARE, 634663),
 (
  CHAT_SHARE, 800150))
SHARE_TYPE_TO_CHAT_TYPE = {FRIEND_SHARE: CHAT_FRIEND,
   CLAN_SHARE: CHAT_CLAN,
   CHAT_SHARE: CHAT_WORLD
   }
SEND_CD = 60

class LotteryResultUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/open_box'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CUSTOM
    IS_FULLSCREEN = True

    def on_init_panel(self, is_my=True):
        self.init_params(is_my)
        self.init_ui()
        self.init_ui_event()

    def init_params(self, is_my):
        self._is_my = is_my
        self._can_close = False
        self._screen_capture_helper = None
        self._buy_widget = None
        self._friend_widget = None
        self._record_open_box_widget = None
        self._has_init_buy_widget = False
        self._chips_data = dict()
        self._reward_list = dict()
        self._player_data = None
        self._total_count = TOTAL_COUNT
        self._last_send_time_list = dict()
        return

    def init_ui(self):
        self._init_temp_lucky()
        self._init_lab()

    def init_ui_event(self):

        @self.panel.btn_sure.callback()
        def OnClick(btn, touch):
            if self._can_close:
                self.close()

    def _init_temp_lucky(self):
        temp_lucky = self.panel.temp_lucky
        temp_lucky.setVisible(True)
        temp_path = 'mall/luck/i_mall_luck_value_mine_new' if self._is_my else 'mall/luck/i_mall_luck_value_others_new'
        self._temp_lucky = global_data.uisystem.load_template_create(temp_path, parent=temp_lucky, name='lucky')
        self._record_open_box_widget = RecordOpenBoxWidgetNew(self._temp_lucky.temp_lucky_value)

    def _init_lab(self):
        self.panel.lab_tips.setVisible(False)
        self.panel.lab_tips2.setVisible(False)
        self.panel.lab_rule.setVisible(False)

    def _init_buy_widget(self):
        if self._has_init_buy_widget:
            return
        else:
            self._has_init_buy_widget = True

            def get_special_price_info(price_info, lottery_count):
                if lottery_count == SINGLE_LOTTERY_COUNT:
                    scene_type = confmgr.get('lottery_page_config', self._lottery_id, 'scene_type')
                    if scene_type == 'special':
                        return mall_utils.get_special_price_info_for_yueka_single_lottery(self._lottery_id, price_info)
                    if scene_type == 'art':
                        return mall_utils.get_special_price_info_for_half_art_collection_single_lottery(self._lottery_id, price_info)
                return False

            def check_buy_action_disabled(lottery_count):
                if is_mainland_package() and self._cur_lottery_count + lottery_count > self._max_lottery_count:
                    global_data.game_mgr.show_tip(get_text_by_id(82040))
                    return True
                return False

            def special_buy_logic_func(price_info, lottery_count):
                if lottery_count == SINGLE_LOTTERY_COUNT:
                    scene_type = confmgr.get('lottery_page_config', self._lottery_id, 'scene_type')
                    if scene_type == 'special':
                        return mall_utils.special_buy_logic_for_yueka_single_lottery(self._lottery_id, self.panel, price_info, lambda : self._buy_widget.do_use_ticket_buy_lottery(price_info, lottery_count))
                    if scene_type == 'art':
                        extra_info = {'lottery_id': self._lottery_id}
                        return mall_utils.special_buy_logic_for_half_art_collection_single_lottery(self._lottery_id, self.panel, price_info, lambda : self._buy_widget.do_use_ticket_buy_lottery(price_info, lottery_count), extra_info)
                return False

            def buying_callback(*args):
                import gc
                gc.collect()
                self.show_again_btn(False)
                result_item_ids = set()
                for item_info in self._reward_list:
                    item_no, item_num = item_info
                    result_item_ids.add(item_no)

                global_data.emgr.lottery_open_box_result.emit(result_item_ids)

            lottery_ui = global_data.ui_mgr.get_ui('LotteryMainUI')
            cur_lottery_widget = lottery_ui.get_lottery_widget(self._lottery_id) if lottery_ui else None
            if cur_lottery_widget:
                if hasattr(cur_lottery_widget, 'custom_get_special_price_info'):
                    custom_get_special_price_info = cur_lottery_widget.custom_get_special_price_info()
                else:
                    custom_get_special_price_info = get_special_price_info
                if hasattr(cur_lottery_widget, 'custom_money_need_spent_func'):
                    custom_money_need_spent_func = cur_lottery_widget.custom_money_need_spent_func()
                else:
                    custom_money_need_spent_func = None
            else:
                custom_get_special_price_info = get_special_price_info
                custom_money_need_spent_func = None
            self._buy_widget = LotteryBuyWidget(self, self.panel, self._lottery_id, price_color=DEF_PRICE_COLOR, buy_button_info={SINGLE_LOTTERY_COUNT: self.panel.btn_once,
               CONTINUAL_LOTTERY_COUNT: self.panel.btn_many_times
               }, buy_price_info={SINGLE_LOTTERY_COUNT: self.panel.btn_once.temp_price,
               CONTINUAL_LOTTERY_COUNT: self.panel.btn_many_times.temp_price
               }, check_buy_action_disabled=check_buy_action_disabled, get_special_price_info=custom_get_special_price_info, special_buy_logic_func=special_buy_logic_func, buying_callback=buying_callback, special_money_need_spent_func=custom_money_need_spent_func)
            return

    def show_again_btn(self, is_visible):
        self.panel.btn_once.setVisible(is_visible)
        self.panel.btn_many_times.setVisible(is_visible)
        self.panel.btn_sure.setVisible(is_visible)

    def set_box_items(self, reward_list, chips_data, extra_info, lottery_id, player_data=None):
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video()
        if global_data.video_list_player:
            global_data.video_list_player.clear()
        global_data.emgr.player_money_info_update_event.emit()
        global_data.ui_mgr.close_ui('ScreenLockerUI')
        if self._is_my:
            self.hide_main_ui()
        self.show()
        self._extra_info = extra_info
        self._lottery_id = lottery_id
        self._reward_list = reward_list
        self._chips_data = chips_data
        self._player_data = player_data
        self._total_count = len(reward_list)
        if self._is_my:
            conf = confmgr.get('lottery_page_config', default={})
            self._max_lottery_count = conf[self._lottery_id].get('day_limit', 0)
            self._cur_lottery_count = global_data.player.get_lottery_per_day_num(self._lottery_id) if global_data.player else 999
            self._init_buy_widget()
        if self._total_count > TOTAL_COUNT:
            self._total_count = TOTAL_COUNT
            self._reward_list = self._reward_list[:TOTAL_COUNT]
        self._update_panel()

    def _update_panel(self):
        self._update_reward_item()
        if self._is_my:
            self._update_temp_lucky()
            self._update_buy_widget()
        else:
            self._update_other_data()
            self.show_again_btn(False)

    def _update_reward_item(self):
        show_chips_type = SHOW_CHIPS_TYPE_ANIM if self._is_my else SHOW_CHIPS_TYPE_NONE
        self._record_open_box_widget.update_ui(self._reward_list, self._chips_data, self._extra_info, show_chips_type)

    def _update_buy_widget(self):
        self._buy_widget.refresh_lottery_price()
        self._buy_widget.refresh_buy_btn_enable(True)
        self.show_again_btn(True)

    def _update_temp_lucky(self):
        conf = confmgr.get('lottery_page_config', self._lottery_id)
        if self._total_count == CONTINUAL_LOTTERY_COUNT and 'luck_rank_list' in conf:
            self._temp_lucky.nd_share.setVisible(True)
            self._update_record()
        else:
            self._temp_lucky.nd_red_packet.setVisible(False)
            self._temp_lucky.nd_share.setVisible(False)
        self._can_close = True

    def _update_record(self):
        lucky_widget = self._temp_lucky
        lucky_widget.temp_lucky_value.PlayAnimation('show')
        nd_red_packet = lucky_widget.nd_red_packet
        if self._extra_info.get('send_red_packet'):
            nd_red_packet.setVisible(True)
            nd_red_packet_visible = True

            @nd_red_packet.btn_show.unique_callback()
            def OnClick(btn, touch):
                ui = global_data.ui_mgr.get_ui('MainChat')
                if not ui:
                    return
                from logic.comsys.chat.MainChat import UI_WORLD_INDEX
                ui.clear_show_count_dict()
                ui.show_main_chat_ui(channel=UI_WORLD_INDEX)
                ui.block_all_click()
                ui.set_need_show_btn(False)
                ui.show_btn_tab_by_index_list([UI_WORLD_INDEX])

        else:
            nd_red_packet_visible = False
            nd_red_packet.setVisible(False)
        btn_sure = self.panel.btn_sure
        btn_once = self.panel.btn_once
        btn_many_times = self.panel.btn_many_times
        nd_share = lucky_widget.nd_share
        nd_red_packet = lucky_widget.nd_red_packet

        def share_cb(*args):
            btn_sure.setVisible(True)
            btn_once.setVisible(True)
            btn_many_times.setVisible(True)
            nd_share.setVisible(True)
            nd_red_packet.setVisible(nd_red_packet_visible)

        lucky_widget.btn_share_2.setVisible(global_data.is_share_show)

        @lucky_widget.btn_share_2.unique_callback()
        def OnClick(btn, touch):
            btn_sure.setVisible(False)
            btn_once.setVisible(False)
            btn_many_times.setVisible(False)
            nd_share.setVisible(False)
            nd_red_packet.setVisible(False)
            if not self._screen_capture_helper:
                from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
                self._screen_capture_helper = ScreenFrameHelper()
            self._screen_capture_helper.take_screen_shot([self.__class__.__name__], self.panel, custom_cb=share_cb)

        list_share = nd_share.list_share
        btn_share = nd_share.btn_share

        def update_arrow():
            is_visible = list_share.isVisible()
            btn_share.img_icon.setRotation(0 if is_visible else 180)

        for i in range(3):
            share_type, img_text = SHARE_INFO[i]
            item = list_share.option_list.GetItem(i)
            item.button.SetText(img_text)

            @item.button.callback()
            def OnClick(btn, touch, share_type=share_type):

                def on_click_friend(f_data):
                    uid = f_data[U_ID]
                    lv = f_data[U_LV]
                    last_send_time = self._last_send_time_list.get(uid, 0)
                    pass_time = time_utility.time() - last_send_time
                    if pass_time > SEND_CD:
                        global_data.game_mgr.show_tip(get_text_by_id(2177))
                        self._last_send_time_list[uid] = time_utility.time()
                        extra_data = self._get_extra_data()
                        global_data.message_data.recv_to_friend_msg(uid, f_data[C_NAME], '', lv, extra=extra_data)
                        global_data.player and global_data.player.req_friend_msg(uid, lv, f_data.get(CLAN_ID, -1), '', extra=extra_data)
                    else:
                        global_data.game_mgr.show_tip(get_text_by_id(634638))

                def check_can_share--- This code section failed: ---

 309       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  '_last_send_time_list'
           6  LOAD_ATTR             1  'get'
           9  LOAD_ATTR             1  'get'
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            1  'last_send_time'

 310      18  LOAD_GLOBAL           2  'time_utility'
          21  LOAD_ATTR             3  'time'
          24  CALL_FUNCTION_0       0 
          27  LOAD_FAST             1  'last_send_time'
          30  BINARY_SUBTRACT  
          31  STORE_FAST            2  'pass_time'

 311      34  LOAD_FAST             2  'pass_time'
          37  LOAD_GLOBAL           4  'SEND_CD'
          40  COMPARE_OP            4  '>'
          43  POP_JUMP_IF_FALSE   146  'to 146'

 312      46  LOAD_GLOBAL           5  'global_data'
          49  LOAD_ATTR             6  'game_mgr'
          52  LOAD_ATTR             7  'show_tip'
          55  LOAD_GLOBAL           8  'get_text_by_id'
          58  LOAD_CONST            2  2177
          61  CALL_FUNCTION_1       1 
          64  CALL_FUNCTION_1       1 
          67  POP_TOP          

 313      68  LOAD_GLOBAL           2  'time_utility'
          71  LOAD_ATTR             3  'time'
          74  CALL_FUNCTION_0       0 
          77  LOAD_DEREF            0  'self'
          80  LOAD_ATTR             0  '_last_send_time_list'
          83  LOAD_FAST             0  'share_type'
          86  STORE_SUBSCR     

 314      87  LOAD_DEREF            0  'self'
          90  LOAD_ATTR             9  '_get_extra_data'
          93  CALL_FUNCTION_0       0 
          96  STORE_FAST            3  'extra_data'

 315      99  LOAD_GLOBAL          10  'SHARE_TYPE_TO_CHAT_TYPE'
         102  LOAD_FAST             0  'share_type'
         105  BINARY_SUBSCR    
         106  STORE_FAST            4  'chat_channel'

 316     109  LOAD_GLOBAL           5  'global_data'
         112  LOAD_ATTR            11  'player'
         115  JUMP_IF_FALSE_OR_POP   142  'to 142'
         118  LOAD_GLOBAL           5  'global_data'
         121  LOAD_ATTR            11  'player'
         124  LOAD_ATTR            12  'send_msg'
         127  LOAD_FAST             4  'chat_channel'
         130  LOAD_CONST            3  ''
         133  LOAD_CONST            4  'extra'
         136  LOAD_FAST             3  'extra_data'
         139  CALL_FUNCTION_258   258 
       142_0  COME_FROM                '115'
         142  POP_TOP          
         143  JUMP_FORWARD         22  'to 168'

 318     146  LOAD_GLOBAL           5  'global_data'
         149  LOAD_ATTR             6  'game_mgr'
         152  LOAD_ATTR             7  'show_tip'
         155  LOAD_GLOBAL           8  'get_text_by_id'
         158  LOAD_CONST            5  634638
         161  CALL_FUNCTION_1       1 
         164  CALL_FUNCTION_1       1 
         167  POP_TOP          
       168_0  COME_FROM                '143'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 12

                if not global_data.player:
                    return
                else:
                    if share_type == FRIEND_SHARE:
                        if self._friend_widget is None:
                            from logic.comsys.share.CommonFriendListWidget import CommonFriendListWidget
                            nd = global_data.uisystem.load_template_create('common/i_common_friend_list', parent=lucky_widget.nd_friend)
                            self._friend_widget = CommonFriendListWidget(self, nd)
                            self._friend_widget.set_select_friend_cb(on_click_friend)
                            self._friend_widget.panel.nd_content.nd_search.setVisible(False)
                        else:
                            is_visible = self._friend_widget.is_visible()
                            if is_visible:
                                self._friend_widget.hide()
                            else:
                                self._friend_widget.show()
                    elif share_type == CLAN_SHARE:
                        if global_data.player.get_clan_id() == -1:
                            global_data.game_mgr.show_tip(get_text_by_id(800098))
                            return
                        check_can_share(CLAN_SHARE)
                    elif share_type == CHAT_SHARE:
                        check_can_share(CHAT_SHARE)
                    list_share.setVisible(False)
                    update_arrow()
                    return

        @btn_share.callback()
        def OnClick(*args):
            list_share.setVisible(not list_share.isVisible())
            update_arrow()

        @list_share.nd_close.callback()
        def OnClick(*args):
            list_share.setVisible(False)
            update_arrow()

    def _get_extra_data(self):
        extra_data = {}
        extra_data['item_no'] = -1
        conf = mall_utils.get_lottery_conf(self._lottery_id)
        luck_share_items = conf.get('luck_share_items')
        for item_no in luck_share_items:
            for item_info in self._reward_list:
                result_item_no, _ = item_info
                if item_no == result_item_no:
                    extra_data['item_no'] = item_no
                    break

            if extra_data['item_no'] != -1:
                break

        lottery_result = {}
        for index, item_info in enumerate(self._reward_list):
            lottery_result[str(index)] = item_info

        extra_data['item_list'] = lottery_result
        extra_data['extra_info'] = self._extra_info
        extra_data['type'] = MSG_TYPE_LUCKY_LOTTERY
        extra_data['text_id'] = conf.get('text_id')
        extra_data['lottery_id'] = self._lottery_id
        return extra_data

    def _update_other_data(self):
        nd_player_info = self._temp_lucky.nd_player_info_1
        name = self._player_data.get('name', global_data.player.get_name())
        nd_player_info.lab_name.setString(name)
        frame_no = self._player_data.get('frame_no', global_data.player.get_head_frame())
        photo_no = self._player_data.get('photo_no', global_data.player.get_head_photo())
        init_role_head(nd_player_info.temp_head, frame_no, photo_no)
        uid = self._player_data.get('uid', global_data.player.uid)
        nd_player_info.lab_id.setString(get_text_by_id(80623) + str(uid))
        lab_day = self._temp_lucky.lab_day
        time_stamp = self._extra_info.get('luck_timestamp')
        if time_stamp is None:
            lab_day.setString('')
        else:
            from logic.gcommon import time_utility
            date_str = time_utility.get_date_str('%Y.%m.%d %H:%M:%S', int(time_stamp))
            lab_day.setString(get_text_by_id(634759).format(date_str))

        @self._temp_lucky.temp_btn_lottery.btn_major.callback()
        def OnClick(btn, touch):
            self._on_click_btn_lottery()

        @self._temp_lucky.btn_close.callback()
        def OnClick(btn, touch):
            self.close()

        return

    def _on_click_btn_lottery(self):
        lottery_id = self._lottery_id
        self.close()
        from logic.gutils import jump_to_ui_utils
        jump_to_ui_utils.jump_to_lottery(lottery_id)

    def on_finalize_panel(self):
        if self._is_my:
            self.show_main_ui()
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
        self._screen_capture_helper = None
        if self._buy_widget:
            self._buy_widget.destroy()
            self._buy_widget = None
        if self._friend_widget:
            self._friend_widget.destroy()
        self._friend_widget = None
        if self._record_open_box_widget:
            self._record_open_box_widget.destroy()
        self._record_open_box_widget = None
        self._lottery_id = None
        self._chips_data = None
        self._reward_list = None
        self._can_close = False
        global_data.career_badge_prompt_mgr.play()
        return