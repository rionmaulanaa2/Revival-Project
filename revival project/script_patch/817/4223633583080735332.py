# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/intimacy/UseIntimacyGiftUI.py
from __future__ import absolute_import
import six
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import NORMAL_LAYER_ZORDER, NORMAL_LAYER_ZORDER_1
from logic.gcommon.const import INTIMACY_RELATION_TYPE_BESTIE, INTIMACY_RELATION_TYPE_PARTNER, INTIMACY_RELATION_TYPE_SET, INTIMACY_RELATION_TYPE_MECHAFRD, INTIMACY_RELATION_TYPE_LOVERS, INTIMACY_NAME_MAP
from logic.gutils.intimacy_utils import get_relation_by_uid, has_relation_with_uid_by_type
from common.const.property_const import *
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.item_utils import get_lobby_item_name, get_item_detail_desc
from logic.gcommon.cdata.intimacy_data import get_intimacy_pt
NO_FILTER = 'no_filter'
INTIMACY_RELATION_TYPE_NONE = 'none'
FILTER_OPTION_LIST = [
 (
  NO_FILTER, 12013),
 (
  INTIMACY_RELATION_TYPE_LOVERS, INTIMACY_NAME_MAP[INTIMACY_RELATION_TYPE_LOVERS]),
 (
  INTIMACY_RELATION_TYPE_MECHAFRD, INTIMACY_NAME_MAP[INTIMACY_RELATION_TYPE_MECHAFRD]),
 (
  INTIMACY_RELATION_TYPE_PARTNER, INTIMACY_NAME_MAP[INTIMACY_RELATION_TYPE_PARTNER]),
 (
  INTIMACY_RELATION_TYPE_BESTIE, INTIMACY_NAME_MAP[INTIMACY_RELATION_TYPE_BESTIE]),
 (
  INTIMACY_RELATION_TYPE_NONE, 80817)]

class UseIntimacyGiftUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'common/intimacy_send_gift'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {}
    USE_CNT_LIST = [
     1, 2, 5]
    TEMPLATE_NODE_NAME = 'temp_bg'

    def on_init_panel(self, *args, **kwargs):
        super(UseIntimacyGiftUI, self).on_init_panel()
        self.init_parameters()
        self.init_panel()

    def init_parameters(self):
        self._filter_type = NO_FILTER
        self._friend_list = global_data.message_data.get_friends()
        self._sort_reverse = False
        self.item_no = None
        return

    def init_panel(self):
        self.panel.btn_filter.BindMethod('OnClick', lambda *args: self.panel.filter_list.setVisible(True))
        self.panel.btn_filter.SetText(FILTER_OPTION_LIST[0][1])
        self.panel.filter_list.nd_close.BindMethod('OnClick', lambda *args: self.panel.filter_list.setVisible(False))
        option_list = self.panel.filter_list.option_list
        option_list.SetInitCount(len(FILTER_OPTION_LIST))
        for idx, option in enumerate(FILTER_OPTION_LIST):
            btn_item = option_list.GetItem(idx).button
            btn_item.SetText(option[1])

            @btn_item.callback()
            def OnClick(btn, touch, option=option):
                self._filter_type = option[0]
                self.panel.btn_filter.SetText(option[1])
                self.panel.filter_list.setVisible(False)
                self._refresh_player_list()

        @self.panel.btn_sort.callback()
        def OnClick(btn, touch):
            self._sort_reverse = not self._sort_reverse
            btn.img_sort.SetFlippedY(self._sort_reverse)
            self._refresh_player_list()

        self.init_temp_search()

    def init_temp_search(self):
        temp_search = self.panel.temp_search
        if global_data.is_pc_mode:

            def cb():
                if not temp_search.isValid():
                    return
                else:
                    if not temp_search.btn_search or not temp_search.btn_search.isValid():
                        return
                    temp_search.btn_search.OnClick(None)
                    return

            send_callback = cb
        else:
            send_callback = None
        import logic.comsys.common_ui.InputBox as InputBox
        self._input_box = InputBox.InputBox(temp_search, placeholder=get_text_by_id(19453), send_callback=send_callback)
        self._input_box.set_rise_widget(self.panel)

        @temp_search.btn_search.callback()
        def OnClick(*args):
            text = self._input_box.get_text()
            self.search_text = text
            self._refresh_player_list()

        return

    def _refresh_player_list(self):
        from logic.gcommon.cdata.intimacy_data import INTIMACY_DAY_GIFT_NUM_LIMIT_PER_FRD
        self.friend_list_to_show = []
        intimacy_data = global_data.player.intimacy_data
        limit_dict = global_data.player.intimacy_day_limit
        if getattr(self, 'search_text', None):
            friend_data_list = []
            try:
                search_id = int(self.search_text)
            except:
                for uid, data in six.iteritems(self._friend_list):
                    data['remark'] = global_data.player._frds_remark.get(int(uid), '')
                    if self.search_text in data[C_NAME] or self.search_text in data['remark']:
                        friend_data_list.append(data)

            else:
                if not G_IS_NA_USER:
                    search_id += global_data.uid_prefix
                friend_data_list.append(self._friend_list.get(search_id, None))

            for friend_data in friend_data_list:
                if not friend_data:
                    continue
                uid = friend_data[U_ID]
                intimacy_info = intimacy_data.get(str(uid), (0, None, None))
                send_limit = limit_dict.get(str(uid), {}).get(str(self.item_no), INTIMACY_DAY_GIFT_NUM_LIMIT_PER_FRD)
                self.friend_list_to_show.append({FRIEND_DATA: friend_data,INTIMACY_DATA: intimacy_info,'limit': send_limit})

        else:
            for uid, friend_data in six.iteritems(self._friend_list):
                if self._filter_type in INTIMACY_RELATION_TYPE_SET and not has_relation_with_uid_by_type(self._filter_type, uid):
                    continue
                if self._filter_type == INTIMACY_RELATION_TYPE_NONE and get_relation_by_uid(uid) is not None:
                    continue
                friend_data['remark'] = global_data.player._frds_remark.get(int(uid), '')
                intimacy_info = intimacy_data.get(str(uid), (0, None, None))
                send_limit = limit_dict.get(str(uid), {}).get(str(self.item_no), INTIMACY_DAY_GIFT_NUM_LIMIT_PER_FRD)
                self.friend_list_to_show.append({FRIEND_DATA: friend_data,INTIMACY_DATA: intimacy_info,'limit': send_limit})

        if len(self.friend_list_to_show) == 0:
            self.panel.nd_empty.setVisible(True)
            self.panel.list_player.setVisible(False)
            return
        else:
            self.panel.nd_empty.setVisible(False)
            self.panel.list_player.setVisible(True)

            def cmp_key--- This code section failed: ---

 154       0  LOAD_GLOBAL           0  'int'
           3  LOAD_FAST             0  'x'
           6  LOAD_GLOBAL           1  'FRIEND_DATA'
           9  BINARY_SUBSCR    
          10  LOAD_GLOBAL           2  'U_ID'
          13  BINARY_SUBSCR    
          14  CALL_FUNCTION_1       1 
          17  STORE_FAST            1  'uid'

 155      20  LOAD_GLOBAL           3  'global_data'
          23  LOAD_ATTR             4  'player'
          26  LOAD_ATTR             5  '_top_frds'
          29  STORE_FAST            2  'top_frds'

 156      32  LOAD_FAST             1  'uid'
          35  LOAD_FAST             2  'top_frds'
          38  COMPARE_OP            6  'in'
          41  POP_JUMP_IF_FALSE    59  'to 59'
          44  LOAD_FAST             2  'top_frds'
          47  LOAD_ATTR             6  'index'
          50  LOAD_FAST             1  'uid'
          53  CALL_FUNCTION_1       1 
          56  JUMP_FORWARD          3  'to 62'
          59  LOAD_CONST            1  -1
        62_0  COME_FROM                '56'
          62  STORE_FAST            3  'is_top'

 157      65  STORE_FAST            2  'top_frds'
          68  BINARY_SUBSCR    
          69  LOAD_CONST            3  ''
          72  COMPARE_OP            3  '!='
          75  STORE_FAST            4  'enable'

 158      78  LOAD_GLOBAL           7  'get_intimacy_pt'
          81  LOAD_FAST             0  'x'
          84  LOAD_GLOBAL           8  'INTIMACY_DATA'
          87  BINARY_SUBSCR    
          88  CALL_FUNCTION_1       1 
          91  STORE_FAST            5  'pt'

 159      94  LOAD_DEREF            0  'self'
          97  LOAD_ATTR             9  '_sort_reverse'
         100  POP_JUMP_IF_FALSE   113  'to 113'

 160     103  LOAD_FAST             5  'pt'
         106  UNARY_NEGATIVE   
         107  STORE_FAST            5  'pt'
         110  JUMP_FORWARD          0  'to 113'
       113_0  COME_FROM                '110'

 161     113  LOAD_FAST             3  'is_top'
         116  LOAD_FAST             4  'enable'
         119  LOAD_FAST             5  'pt'
         122  BUILD_LIST_3          3 
         125  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_FAST' instruction at offset 65

            self.friend_list_to_show.sort(key=cmp_key, reverse=True)
            self.uid_to_btn_dict = dict()
            self.panel.list_player.DeleteAllSubItem()
            data_count = len(self.friend_list_to_show)
            sview_height = self.panel.list_player.getContentSize().height
            all_height = 0
            index = 0
            while all_height < sview_height + 200:
                if data_count - index <= 0:
                    break
                data = self.friend_list_to_show[index]
                chat_pnl = self.add_friend_item(data, True)
                all_height += chat_pnl.getContentSize().height
                index += 1

            self.panel.list_player.ScrollToTop()
            self.panel.list_player._container._refreshItemPos()
            self.panel.list_player._refreshItemPos()
            self._cur_show_index = index - 1

            def scroll_callback(sender, eventType):
                if not getattr(self, '_is_check_sview', False):
                    self._is_check_sview = True
                    self.panel.list_player.SetTimeOut(0.001, self.check_sview)

            self.panel.list_player.addEventListener(scroll_callback)
            return

    def check_sview(self):
        self._cur_show_index = self.panel.list_player.AutoAddAndRemoveItem(self._cur_show_index, self.friend_list_to_show, len(self.friend_list_to_show), self.add_friend_item, 300, 400)
        self._is_check_sview = False

    def add_friend_item(self, data, is_back_item, index=-1, show_last_msg=False):
        if is_back_item:
            panel = self.panel.list_player.AddTemplateItem(bRefresh=True)
        else:
            panel = self.panel.list_player.AddTemplateItem(0, bRefresh=True)
        self.refresh_friend_item(panel, data, show_last_msg)
        self.uid_to_btn_dict[data[FRIEND_DATA][U_ID]] = panel
        return panel

    def refresh_friend_item(self, item, data, show_last_msg=False):
        from logic.gutils.intimacy_utils import init_intimacy_my_item, init_intimacy_build_item
        from logic.gcommon.cdata.intimacy_data import INTIMACY_DAY_GIFT_NUM_LIMIT_PER_FRD
        intimacy_data = global_data.player.intimacy_data
        limit_dict = global_data.player.intimacy_day_limit
        uid = data[FRIEND_DATA][U_ID]
        relation_type = get_relation_by_uid(uid)
        if relation_type is None:
            item.temp_normal.setVisible(True)
            item.temp_intimacy.setVisible(False)
            init_intimacy_build_item(item.temp_normal, data[FRIEND_DATA][U_ID], data[FRIEND_DATA], data[INTIMACY_DATA], show_btn=False, show_remark=True)
        else:
            item.temp_normal.setVisible(False)
            item.temp_intimacy.setVisible(True)
            init_intimacy_my_item(item.temp_intimacy, data[FRIEND_DATA][U_ID], data[FRIEND_DATA], data[INTIMACY_DATA], show_btn=False, show_remark=True)
        item.nd_top.setVisible(uid in global_data.player._top_frds)
        send_limit = limit_dict.get(str(uid), {}).get(str(self.item_no), INTIMACY_DAY_GIFT_NUM_LIMIT_PER_FRD)
        item.btn_send.btn_common.SetEnable(send_limit != 0)
        item.btn_send.btn_common.SetText(81191 if send_limit != 0 else 81920)
        if send_limit != 0:

            @item.btn_send.btn_common.unique_callback()
            def OnClick(btn, touch, data=data[FRIEND_DATA]):
                if self.item_no is None:
                    return
                else:
                    ui = global_data.ui_mgr.get_ui('IntimacyGiftUseConfirmUI')
                    if not ui:
                        ui = global_data.ui_mgr.show_ui('IntimacyGiftUseConfirmUI', 'logic.comsys.intimacy')
                    if ui:
                        ui.show_window(data, self.close)
                        ui.show_nd_quantity(self.item_no)
                    self.close()
                    return

        return

    def set_use_params(self, item_data, ui_args, ui_kwargs):
        item_no = item_data.get('item_no', None)
        if item_no is None:
            return
        else:
            self.item_no = item_no
            init_tempate_mall_i_item(self.panel.temp_item, item_no)
            self.panel.lab_name.SetString(get_lobby_item_name(item_no))
            self.panel.lab_detail.SetString(get_item_detail_desc(item_no))
            self._refresh_player_list()
            return