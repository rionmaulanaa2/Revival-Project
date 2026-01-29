# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/RoleSkinDecorationStoreUI.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gutils import mall_utils
from logic.client.const import mall_const
import cc
from common.const.uiconst import BATTLE_MESSAGE_ZORDER, UI_TYPE_MESSAGE
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
import logic.gcommon.const as gconst
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils import dress_utils
from logic.gutils import template_utils
from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
from common.const.uiconst import BG_ZORDER

class RoleSkinDecorationStoreUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/mall_role_define_all'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'player_item_update_event': '_on_item_update',
       'buy_good_success': '_on_buy_success'
       }

    def on_init_panel--- This code section failed: ---

  38       0  BUILD_LIST_0          0 
           3  STORE_FAST            4  'EXCEPT_HIDE_UI_LIST'

  39       6  LOAD_GLOBAL           0  'global_data'
           9  LOAD_ATTR             1  'ui_mgr'
          12  LOAD_ATTR             2  'create_simple_dialog'
          15  LOAD_CONST            1  'common/bg_full_screen_bg'
          18  LOAD_GLOBAL           3  'BG_ZORDER'
          21  CALL_FUNCTION_2       2 
          24  LOAD_FAST             0  'self'
          27  STORE_ATTR            4  'bg_ui'

  40      30  LOAD_FAST             0  'self'
          33  LOAD_ATTR             4  'bg_ui'
          36  LOAD_ATTR             5  'img_bg'
          39  LOAD_ATTR             6  'SetDisplayFrameByPath'
          42  LOAD_CONST            2  ''
          45  LOAD_CONST            3  'gui/ui_res_2/mall/img_role_define_bg.png'
          48  CALL_FUNCTION_2       2 
          51  POP_TOP          

  41      52  LOAD_FAST             0  'self'
          55  LOAD_ATTR             7  'add_associate_vis_ui'
          58  LOAD_FAST             0  'self'
          61  LOAD_ATTR             4  'bg_ui'
          64  LOAD_ATTR             8  '__class__'
          67  LOAD_ATTR             9  '__name__'
          70  CALL_FUNCTION_1       1 
          73  POP_TOP          

  42      74  LOAD_FAST             0  'self'
          77  LOAD_ATTR            10  'init_parameters'
          80  CALL_FUNCTION_0       0 
          83  POP_TOP          

  43      84  LOAD_CONST            0  ''
          87  LOAD_FAST             0  'self'
          90  STORE_ATTR           12  '_show_type_filter'

  44      93  LOAD_CONST            0  ''
          96  LOAD_FAST             0  'self'
          99  STORE_ATTR           13  '_role_filter'

  45     102  LOAD_CONST            0  ''
         105  LOAD_FAST             0  'self'
         108  STORE_ATTR           14  '_list_sview'

  46     111  LOAD_GLOBAL          15  'set'
         114  LOAD_GLOBAL          16  'dress_utils'
         117  LOAD_ATTR            17  'get_invisible_decoration_id_list'
         120  CALL_FUNCTION_0       0 
         123  CALL_FUNCTION_1       1 
         126  LOAD_FAST             0  'self'
         129  STORE_ATTR           18  '_invisible_decoration_id_list'

  48     132  LOAD_FAST             0  'self'
         135  LOAD_ATTR            19  'hide_main_ui'
         138  LOAD_CONST            4  'exceptions'
         141  LOAD_FAST             4  'EXCEPT_HIDE_UI_LIST'
         144  LOAD_CONST            5  'exception_types'
         147  LOAD_GLOBAL          20  'UI_TYPE_MESSAGE'
         150  BUILD_TUPLE_1         1 
         153  CALL_FUNCTION_512   512 
         156  POP_TOP          

  49     157  LOAD_GLOBAL          21  'PriceUIWidget'
         160  LOAD_GLOBAL           6  'SetDisplayFrameByPath'
         163  LOAD_FAST             0  'self'
         166  LOAD_ATTR            22  'close'
         169  CALL_FUNCTION_257   257 
         172  LOAD_FAST             0  'self'
         175  STORE_ATTR           23  'price_top_widget'

  51     178  LOAD_CONST            7  '%d_%d'
         181  LOAD_GLOBAL          24  'gconst'
         184  LOAD_ATTR            25  'SHOP_PAYMENT_ITEM'
         187  LOAD_GLOBAL          24  'gconst'
         190  LOAD_ATTR            26  'SHOP_ITEM_DEC_COIN'
         193  BUILD_TUPLE_2         2 
         196  BINARY_MODULO    

  53     197  LOAD_GLOBAL          24  'gconst'
         200  LOAD_ATTR            27  'SHOP_PAYMENT_YUANBAO'
         203  BUILD_LIST_2          2 
         206  LOAD_FAST             0  'self'
         209  STORE_ATTR           28  'money_type_list'

  55     212  LOAD_FAST             0  'self'
         215  LOAD_ATTR            23  'price_top_widget'
         218  LOAD_ATTR            29  'show_money_types'
         221  LOAD_FAST             0  'self'
         224  LOAD_ATTR            28  'money_type_list'
         227  CALL_FUNCTION_1       1 
         230  POP_TOP          

  57     231  LOAD_FAST             0  'self'
         234  LOAD_ATTR            30  'prepare_dec_group_member_ship'
         237  CALL_FUNCTION_0       0 
         240  UNPACK_SEQUENCE_2     2 
         243  LOAD_FAST             0  'self'
         246  STORE_ATTR           31  '_dec_member_dict'
         249  LOAD_FAST             0  'self'
         252  STORE_ATTR           32  '_dec_group_dict'

  58     255  LOAD_FAST             0  'self'
         258  LOAD_ATTR            33  'init_mode_list'
         261  CALL_FUNCTION_0       0 
         264  POP_TOP          

  59     265  LOAD_FAST             0  'self'
         268  LOAD_ATTR            34  'init_left_tab_list'
         271  CALL_FUNCTION_0       0 
         274  POP_TOP          

  60     275  LOAD_CONST            8  ''
         278  LOAD_FAST             0  'self'
         281  STORE_ATTR           35  'cur_tab_index'

  61     284  LOAD_FAST             0  'self'
         287  LOAD_ATTR            36  'left_tab_list'
         290  LOAD_ATTR            37  'set_tab_selected'
         293  LOAD_FAST             0  'self'
         296  LOAD_ATTR            35  'cur_tab_index'
         299  CALL_FUNCTION_1       1 
         302  POP_TOP          

  62     303  LOAD_CONST            8  ''
         306  LOAD_CONST            9  ('InfiniteScrollWidget',)
         309  IMPORT_NAME          38  'logic.gutils.InfiniteScrollWidget'
         312  IMPORT_FROM          39  'InfiniteScrollWidget'
         315  STORE_FAST            5  'InfiniteScrollWidget'
         318  POP_TOP          

  63     319  LOAD_FAST             5  'InfiniteScrollWidget'
         322  LOAD_FAST             0  'self'
         325  LOAD_ATTR            40  'panel'
         328  LOAD_ATTR            41  'list_item'
         331  LOAD_FAST             0  'self'
         334  LOAD_ATTR            40  'panel'
         337  LOAD_CONST           10  'up_limit'
         340  LOAD_CONST           11  1000
         343  LOAD_CONST           12  'down_limit'
         346  LOAD_CONST           11  1000
         349  CALL_FUNCTION_514   514 
         352  LOAD_FAST             0  'self'
         355  STORE_ATTR           14  '_list_sview'

  64     358  LOAD_FAST             0  'self'
         361  LOAD_ATTR            14  '_list_sview'
         364  LOAD_ATTR            42  'enable_item_auto_pool'
         367  LOAD_GLOBAL          43  'True'
         370  CALL_FUNCTION_1       1 
         373  POP_TOP          

  65     374  LOAD_FAST             0  'self'
         377  LOAD_ATTR            14  '_list_sview'
         380  LOAD_ATTR            44  'set_template_init_callback'
         383  LOAD_FAST             0  'self'
         386  LOAD_ATTR            45  'init_dec_item'
         389  CALL_FUNCTION_1       1 
         392  POP_TOP          

  66     393  LOAD_FAST             0  'self'
         396  LOAD_ATTR            46  'update_show'
         399  CALL_FUNCTION_0       0 
         402  POP_TOP          
         403  LOAD_CONST            0  ''
         406  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_257' instruction at offset 169

    def on_finalize_panel(self):
        self.price_top_widget and self.price_top_widget.on_finalize_panel()
        self.price_top_widget = None
        if self._list_sview:
            self._list_sview.destroy()
            self._list_sview = None
        self.show_main_ui()
        if self.left_tab_list:
            self.left_tab_list.destroy()
            self.left_tab_list = None
        if self.bg_ui:
            self.bg_ui.close()
            self.bg_ui = None
        return

    def get_short_show_name(self, name):
        start_symbols = [']', '\xe3\x80\x91']
        end_symbols = [', ', ',', ': ', ':', '- ', '-', '\xc2\xb7 ', '\xc2\xb7', '\xe3\x83\xbb']
        start_pos = 0
        end_pos = 0
        for c in start_symbols:
            if c in name:
                start_pos = max(name.index(c) + len(c), start_pos)

        for c in end_symbols:
            if c in name:
                end_pos = max(name.index(c) + len(c), end_pos)

        if start_pos > 0 and end_pos > 0:
            return name[0:start_pos] + name[end_pos:]
        else:
            return name

    def init_dec_item(self, ui_item, data):
        item_no = data
        res_path = item_utils.get_lobby_item_pic_by_item_no(item_no)
        ui_item.item.SetDisplayFrameByPath('', res_path)
        ui_item.lab_name.SetString(self.get_short_show_name(item_utils.get_lobby_item_name(item_no)))
        goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(item_no)
        price = mall_utils.get_mall_item_price(goods_id)
        own = global_data.player.has_item_by_no(item_no)
        ui_item.img_btn_grey.setVisible(own)
        ui_item.lab_useless.setVisible(own)
        ui_item.img_btn_yellow.setVisible(not own)
        ui_item.temp_price.setVisible(not own)
        ui_item.lab_go.setVisible(False)
        mall_utils.read_new_arrivals(goods_id)
        from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
        if not own:
            if price and not item_utils.is_jump_to_lottery(item_no):
                template_utils.init_price_view(ui_item.temp_price, goods_id, mall_const.USE_TEMPLATE_COLOR)
            else:
                ui_item.temp_price.setVisible(False)
                gain_method_text = item_utils.get_item_access(item_no)
                if gain_method_text:
                    ui_item.lab_go.setVisible(True)
                    ui_item.lab_go.SetString(gain_method_text)
                else:
                    ui_item.lab_go.SetString(81815)
        is_new_arrival = confmgr.get('c_mall_new_arrival_conf', goods_id, 'cShowNewHint', default=False)
        ui_item.nd_new.setVisible(bool(is_new_arrival))
        if bool(is_new_arrival):
            ui_item.PlayAnimation('new')
        else:
            ui_item.StopAnimation('new')
        role_id = item_utils.get_lobby_item_belong_no(item_no)
        rare_degree = item_utils.get_item_rare_degree(item_no)
        bg_pic = item_utils.get_skin_define_quality_pic(rare_degree)
        ui_item.img_item_bar.SetDisplayFrameByPath('', bg_pic)
        dec_skin_list = dress_utils.get_decoration_id_skin_list(item_no, top_skin_only=True)
        if len(dec_skin_list) > 1 or item_no in self._dec_group_dict or item_no in self._dec_member_dict:
            ui_item.lab_role_name.SetString(81799)
            default_val = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')[0]
            role_res_path = item_utils.get_lobby_item_pic_by_item_no(default_val)
            ui_item.img_role.SetDisplayFrameByPath('', role_res_path)
        elif len(dec_skin_list) == 1:
            ui_item.lab_role_name.SetString(item_utils.get_lobby_item_name(dec_skin_list[0]))
            role_res_path = item_utils.get_lobby_item_pic_by_item_no(dec_skin_list[0])
            ui_item.img_role.SetDisplayFrameByPath('', role_res_path)

        @ui_item.btn_buy.callback()
        def OnClick(btn, touch):
            own = global_data.player.has_item_by_no(item_no)
            if not own and price and not item_utils.is_jump_to_lottery(item_no):
                groceries_buy_confirmUI(goods_id)
            else:
                item_utils.jump_to_ui(item_no)

        @ui_item.btn_item.callback()
        def OnClick(btn, touch):
            dec_skin_list = dress_utils.get_decoration_id_skin_list(item_no, top_skin_only=False)
            other_skin_list = []
            if item_no in self._dec_member_dict:
                dec_id_list = self._dec_group_dict.get(self._dec_member_dict[item_no], [])
                if self._dec_member_dict[item_no] not in dec_id_list:
                    dec_id_list.append(self._dec_member_dict[item_no])
            elif item_no in self._dec_group_dict:
                dec_id_list = self._dec_group_dict[item_no]
            else:
                dec_id_list = []
            all_dec_id_list = list(dec_id_list)
            if item_no in dec_id_list:
                dec_id_list.remove(item_no)
            for dec_id in dec_id_list:
                if dec_id in self._invisible_decoration_id_list:
                    continue
                sk_list = dress_utils.get_decoration_id_skin_list(dec_id, top_skin_only=False)
                other_skin_list.extend(sk_list)

            jump_to_display_detail_by_item_no(item_no, {'adapt_skin_list': dec_skin_list + other_skin_list,'dec_no_list': all_dec_id_list})

    def init_tab_data(self):
        from logic.gcommon.item.item_const import FPOS_2_TAG_STR
        self.tab_list = [{'text': 12013,'sec_text': '','type': None}]
        from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_HEAD, L_ITEM_TYPE_BODY, L_ITEM_TYPE_SUIT, L_ITEM_TYPE_FACE_DEC, L_ITEM_TYPE_WAIST_DEC, L_ITEM_TYPE_LEG_DEC, L_ITEM_TYPE_HAIR_DEC, L_ITEM_TYPE_ARM_DEC
        dec_list = [{'text': 81229,'type': L_ITEM_TYPE_HEAD}, {'text': 860098,'type': L_ITEM_TYPE_FACE_DEC}, {'text': 81704,'type': L_ITEM_TYPE_HAIR_DEC}, {'text': 81926,'type': L_ITEM_TYPE_ARM_DEC}, {'text': 860099,'type': L_ITEM_TYPE_BODY}, {'text': 860100,'type': L_ITEM_TYPE_WAIST_DEC}, {'text': 860101,'type': L_ITEM_TYPE_LEG_DEC}, {'text': 81228,'type': L_ITEM_TYPE_SUIT}]
        for dec in dec_list:
            dec['type'] = FPOS_2_TAG_STR.get(dress_utils.get_lobby_type_fashion_pos(dec['type']), None)

        self.tab_list.extend(dec_list)
        return

    def init_left_tab_list(self):
        self.init_tab_data()

        def return_func():
            self.on_before_close(self.close)

        from logic.gutils.new_template_utils import CommonLeftTabList
        self.left_tab_list = CommonLeftTabList(self.panel.temp_left, self.tab_list, return_func, self.click_left_tab_btn)

    def click_left_tab_btn(self, index):
        if index == self.cur_tab_index:
            return
        else:
            self.cur_tab_index = index
            if index < len(self.tab_list):
                tab_data = self.tab_list[index]
                ty = tab_data.get('type')
                if ty:
                    self._show_type_filter = ty
                else:
                    self._show_type_filter = None
                self.update_show()
            return True

    def init_mode_list(self):
        from logic.gutils import template_utils
        from logic.gutils import item_utils, role_head_utils
        role_id_list = [ r_id for r_id in global_data.player.get_role_open_seq() if dress_utils.is_role_usable(r_id) ]
        role_profile_conf = confmgr.get('role_info', 'RoleProfile', 'Content', default={})
        role_id_list = sorted(role_id_list, key=lambda x: role_profile_conf.get(str(x), {}).get('sort_id'))
        mode_option = [ {'name': item_utils.get_lobby_item_name(role_id),'mode': int(role_id),'icon': role_head_utils.get_role_head_pic(role_id)} for role_id in role_id_list
                      ]
        mode_option.insert(0, {'name': 81797,'mode': None})

        @self.panel.btn_sort.unique_callback()
        def OnClick(btn, touch):
            if not self.panel.temp_list.isVisible():
                self.panel.temp_list.setVisible(True)
                self.panel.img_arrow.setRotation(180)
            else:
                self.panel.temp_list.setVisible(False)
                self.panel.img_arrow.setRotation(0)

        def call_back(index):
            option = mode_option[index]
            self._role_filter = option['mode']
            self.panel.lab_role_name.SetString(option['name'])
            pic_path = option.get('icon', '')
            self.panel.img_role.SetDisplayFrameByPath('', pic_path)
            self.panel.img_role.setVisible(bool(pic_path))
            self.panel.temp_list.setVisible(False)
            self.panel.img_arrow.setRotation(0)
            self.update_show()

        def close_callback():
            self.panel.img_arrow.setRotation(0)

        template_utils.init_common_choose_list(self.panel.temp_list, mode_option, call_back, max_height=354, close_cb=close_callback)
        call_back(0)
        return

    def on_before_close(self, callback):
        if callback:
            callback()

    def init_parameters(self):
        self.price_top_widget = None
        return

    def _on_item_update(self, *args):
        player = global_data.player
        if not player.requested_buy_goods:
            self.update_show()

    def _on_buy_success(self, *args, **kargs):
        player = global_data.player
        if player.requested_buy_goods:
            self.update_show()

    def _on_login_reconnected(self, *args):
        self.close()

    def update_show(self):
        if self._list_sview:
            new_data_list = self.get_store_pendant_list()
            self.on_update_item_list(new_data_list)

    def on_update_item_list(self, new_data_list):
        if len(new_data_list) <= 0:
            self.panel.nd_empty.setVisible(True)
            self.panel.list_item.setVisible(False)
        else:
            self.panel.nd_empty.setVisible(False)
            self.panel.list_item.setVisible(True)
            self._list_sview.update_data_list(new_data_list)
            self._list_sview.refresh_showed_item()
            self._list_sview.update_scroll_view()

    def get_store_pendant_list(self):
        pendant_conf = confmgr.get('pendant', 'SkinRestrict', default={})
        from logic.gcommon.cdata.pendant_data import data
        pendant_list = []
        role_dict_list = []
        if self._role_filter is None:
            role_dict_list = six_ex.values(data)
        else:
            role_dict_list.append(data.get(self._role_filter, {}))
        for role_dict in role_dict_list:
            if self._show_type_filter is None:
                for dec_id_list in six.itervalues(role_dict):
                    pendant_list.extend(dec_id_list)

            else:
                pendant_list.extend(role_dict.get(self._show_type_filter, []))

        to_be_removed_dec_list = []
        for dec_id in pendant_list:
            if dec_id in self._invisible_decoration_id_list:
                to_be_removed_dec_list.append(dec_id)

        for dec_id in to_be_removed_dec_list:
            pendant_list.remove(dec_id)

        pendant_set = set(pendant_list)
        pendant_list = [ p for p in pendant_list if self._dec_member_dict.get(p) not in pendant_set ]
        pendant_list = sorted(pendant_list, key=cmp_to_key(self.dec_cmp_func))
        return pendant_list

    def prepare_dec_group_member_ship(self):
        member_dict = {}
        group_dict = {}
        from logic.gcommon.cdata.pendant_data import data
        for role_dict in six.itervalues(data):
            for part_list in six.itervalues(role_dict):
                for dec_id in part_list:
                    show_group = confmgr.get('pendant', 'SkinRestrict', str(dec_id), 'show_group', default=None)
                    if show_group:
                        member_dict[dec_id] = show_group
                        group_dict.setdefault(show_group, [])
                        group_dict[show_group].append(dec_id)

        return (
         member_dict, group_dict)

    def dec_cmp_func(self, dec_no_1, dec_no_2):
        dec_info_1 = self.dec_key_func(dec_no_1)
        dec_info_2 = self.dec_key_func(dec_no_2)
        cmp_res = six_ex.compare(dec_info_1, dec_info_2)
        if cmp_res == 0:
            return -1 * six_ex.compare(dec_no_1, dec_no_2)
        else:
            return cmp_res

    def dec_key_func(self, dec_no):
        own = global_data.player.has_item_by_no(dec_no)
        goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(dec_no)
        is_new_arrival = bool(confmgr.get('c_mall_new_arrival_conf', goods_id, 'cShowNewHint', default=False))
        price = mall_utils.get_mall_item_price(goods_id)
        has_price = True if price and not item_utils.is_jump_to_lottery(dec_no) else False
        sort_id = confmgr.get('pendant', 'SkinRestrict', str(dec_no), 'sort_id', default=dec_no)
        belong_item_no = item_utils.get_lobby_item_belong_no(dec_no)
        if has_price:
            has_discount = 'discount_price' in price
        else:
            has_discount = False
        return (
         not is_new_arrival, own, not has_price, not has_discount, sort_id, belong_item_no)