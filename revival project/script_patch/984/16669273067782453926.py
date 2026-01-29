# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryExchangeRewardWidget.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from logic.gcommon.item.lobby_item_type import MODEL_DISPLAY_TYPE, RP_SKIN_TYPE, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.mall_utils import get_mall_item_price, check_payment, get_goods_pic_path, is_good_opened, get_lottery_exchange_list, get_goods_item_no, get_goods_name, item_has_owned_by_goods_id, get_goods_limit_num_all, is_weapon, is_vehicle, buy_num_limit_by_all, get_special_goods_logic
from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI, item_skin_buy_confirmUI, groceries_buy_confirmUI
from logic.gutils.item_utils import get_lobby_item_type, get_item_rare_degree, REWARD_RARE_COLOR, get_skin_rare_path_by_rare, check_skin_tag
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import splice_price
import math
import cc
BIG_DISPLAY_ITEM_TYPE = {
 L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN}
NEED_ADJUST_RARE_DEGREE_PIC_MAP = {'mall/i_collection_activity/common_advanced_7times/i_lottery_advanced_7times_item_4': 'gui/ui_res_2/lottery/lottery_activity/common_7times/bar_lottery_item_4_{}.png'
   }

def default_empty_func(*args, **kwargs):
    pass


def init_top_tab_list(nd_list, data_list, click_cb):
    nd_list.DeleteAllSubItem()
    nd_list.SetInitCount(len(data_list))
    for idx, item in enumerate(nd_list.GetAllItem()):
        info = data_list[idx]
        text = info.get('text', '')
        if text:
            item.btn_tab.SetText(text)
        item.btn_tab.EnableCustomState(True)

        @item.btn_tab.callback()
        def OnClick(btn, touch, item=item, idx=idx):
            click_cb(item, idx)
            for _idx, _item in enumerate(nd_list.GetAllItem()):
                if _idx != idx:
                    _item.btn_tab.SetSelect(False)
                    if _item.img_vx:
                        _item.StopAnimation('click')
                        _item.PlayAnimation('unclick')
                        _item.img_vx.setVisible(False)
                else:
                    _item.btn_tab.SetSelect(True)
                    if _item.img_vx:
                        _item.StopAnimation('unclick')
                        _item.img_vx.setVisible(True)
                        _item.PlayAnimation('click')


class LotteryExchangeRewardWidget(object):

    def _trans_str_to_list(self, obj):
        if type(obj) == str:
            return [obj]
        return obj

    def _trans_nd_name_to_nd(self, nd_name_list):
        nd_list = []
        for nd_name in nd_name_list:
            single_name_list = nd_name.split('.')
            nd_level = len(single_name_list)
            nd = self.panel
            for i in range(0, nd_level):
                nd = getattr(nd, single_name_list[i], None)
                if nd is None:
                    print('Error: {}--{}'.format(nd_name, single_name_list[i]))
                    break

            nd and nd_list.append(nd)

        return nd_list

    def __init__(self, parent, panel, nd_visibility_bound, nd_visibility_opposite, lottery_id, on_change_show_reward, nd_visibility_opposite_relatively=(), pre_init_display_item=default_empty_func, play_display_item_anim=None, nd_directly_show_visible=(), nd_directly_show_invisible=(), nd_kind='temp_kind', nd_lab_name='lab_name', nd_btn_detail='btn_detail', price_color=None, tab_func=None):
        self.parent = parent
        self.panel = panel
        self.nd_visibility_bound = nd_visibility_bound
        self.nd_visibility_opposite = nd_visibility_opposite
        self.lottery_id = lottery_id
        self.on_change_show_reward = on_change_show_reward
        self.nd_visibility_opposite_relatively = self._trans_str_to_list(nd_visibility_opposite_relatively)
        self.pre_init_display_item = pre_init_display_item
        self.play_display_item_anim = play_display_item_anim if play_display_item_anim else self._play_display_item_anim
        self.nd_directly_show_visible = self._trans_nd_name_to_nd(self._trans_str_to_list(nd_directly_show_visible))
        self.nd_directly_show_invisible = self._trans_nd_name_to_nd(self._trans_str_to_list(nd_directly_show_invisible))
        self.nd_kind = self._trans_nd_name_to_nd(self._trans_str_to_list(nd_kind))
        self.nd_lab_name = self._trans_nd_name_to_nd(self._trans_str_to_list(nd_lab_name))
        self.nd_btn_detail = self._trans_nd_name_to_nd(self._trans_str_to_list(nd_btn_detail))
        self.tab_func = tab_func
        if price_color:
            self.price_color = []
            for color in price_color:
                if color.startswith('#'):
                    self.price_color.append(color)
                else:
                    self.price_color.append(int(color, base=16))

        else:
            self.price_color = None
        self.init_parameters()
        self.init_panel()
        self.process_event(True)
        return

    @property
    def visible(self):
        return self.is_visible

    @visible.setter
    def visible(self, flag):
        old_vis = self.is_visible
        if old_vis != flag:
            if flag:
                self.parent.panel.PlayAnimation('show_shop')
        self.is_visible = flag
        self.parent.set_exchange_reward_widget_visible_callback(flag)
        self.nd_visibility_bound.setVisible(flag)
        self.nd_visibility_opposite.setVisible(not flag)
        if flag:
            self.refresh_all_appearance()
            self._show_reward_info(self.visible_show_item_no or self.selected_item_no, force_show_chuchang=True)
            ani_names = self.panel.GetAnimationNameList()
            for anim_name in ani_names:
                anim_name = str(anim_name)
                if anim_name.startswith('show'):
                    self.panel.PlayAnimation(anim_name)

        else:
            global_data.emgr.set_lottery_reward_info_label_visible.emit(True)
        global_data.emgr.hide_lottery_main_ui_elements.emit(flag, self.nd_visibility_opposite_relatively, need_refresh_scene=True)

    def init_parameters(self):
        self.directly_show = False
        self.is_visible = False
        self.selected_item_index = 0
        self.selected_goods_id = None
        self.selected_item_no = None
        self.visible_show_item_no = None
        self.selected_item_widget = None
        self.big_display_goods_ids = []
        self.big_display_item_list = []
        self.big_display_item_count = 0
        self.small_display_goods_ids = []
        self.small_display_item_list = []
        self.small_display_item_count = 0
        self.tab_info_list = []
        _, exchange_lottery_map = get_lottery_exchange_list()
        exchange_goods_list = exchange_lottery_map[self.lottery_id]
        if self.tab_func:
            self.tab_info_list = self.tab_func(exchange_goods_list)
        else:
            for goods_id in exchange_goods_list:
                item_no = get_goods_item_no(goods_id)
                item_type = get_lobby_item_type(item_no)
                if item_type in BIG_DISPLAY_ITEM_TYPE:
                    self.big_display_item_list.append((goods_id, item_no))
                    self.big_display_goods_ids.append(goods_id)
                    self.big_display_item_count += 1
                else:
                    self.small_display_item_list.append((goods_id, item_no))
                    self.small_display_goods_ids.append(goods_id)
                    self.small_display_item_count += 1

            self.update_display_list()
        return

    def init_display_item(self, item_widget, item_index, goods_id, item_no, is_big_display_item=False):
        self.pre_init_display_item(item_widget, item_no=item_no)
        self.play_display_item_anim(item_widget, False, item_no=item_no)
        rare_degree = get_item_rare_degree(item_no)
        tag_img = get_skin_rare_path_by_rare(rare_degree)
        if tag_img:
            item_widget.img_class.SetDisplayFrameByPath('', tag_img)
        item_widget.lab_name.SetString(get_goods_name(goods_id))
        if not is_big_display_item:
            icon_path = get_goods_pic_path(goods_id)
            item_widget.img_pic.SetDisplayFrameByPath('', icon_path)
        pic_path = NEED_ADJUST_RARE_DEGREE_PIC_MAP.get(item_widget.GetTemplatePath(), None)
        if pic_path:
            color = REWARD_RARE_COLOR.get(rare_degree, 'orange')
            color_pic_path = pic_path.format(color)
            item_widget.SetFrames('', [color_pic_path, color_pic_path, color_pic_path], True, None)
        item_widget.SetClipObject(self.panel.list_item)
        item_widget.SetEnable(True)

        @item_widget.unique_callback()
        def OnClick(*args):
            self.on_click_display_item(item_widget, item_index, goods_id, item_no)

        return

    def adjust_list_view_size(self):
        first_node = self.panel.list_item.GetItem(0)
        list_0_item = first_node.list_0_item
        list_1_item = first_node.list_1_item
        if self.big_display_item_list:
            one_big_bar = list_0_item.GetItem(0)
            size1 = one_big_bar.GetConfSize()
        else:
            size1 = cc.Size(first_node.GetContentSize()[0], 0)
        if self.small_display_item_list:
            one_small_bar = list_1_item.GetItem(0)
            if one_small_bar:
                size2 = one_small_bar.GetConfSize()
            else:
                size2 = cc.Size(0, 0)
        else:
            size2 = cc.Size(0, 0)
        if self.small_display_item_count % 3 == 0:
            small_row = self.small_display_item_count / 3
        else:
            small_row = int(self.small_display_item_count / 3) + 1
        SMALL_AND_BIG_GAP = 18
        indents = list_0_item.GetVertIndent() * (self.big_display_item_count - 1) + list_1_item.GetVertIndent() * small_row
        size = cc.Size(size1.width, size1.height * self.big_display_item_count + size2.height * small_row + indents + SMALL_AND_BIG_GAP)
        first_node.setContentSize(size)
        first_node.ChildRecursionRePosition()
        self.panel.list_item.RefreshItemPos()

    def init_panel(self):
        if self.panel.HasAnimation('button_loop'):
            self.panel.RecordAnimationNodeState('button_loop')

        @self.panel.btn_close.unique_callback()
        def OnClick(*args):
            if self.directly_show:
                global_data.ui_mgr.close_ui('LotteryMainUI')
            else:
                self.visible = False

        @self.panel.btn_buy.unique_callback()
        def OnClick(*args):
            self.on_click_btn_buy()

        for btn_detail in self.nd_btn_detail:
            btn_detail.BindMethod('OnClick', lambda *args: jump_to_display_detail_by_item_no(self.selected_item_no))

        self.init_tab_list()

    def on_click_btn_buy(self):
        if not self.selected_goods_id or item_has_owned_by_goods_id(self.selected_goods_id):
            return
        specail_goods_logic = get_special_goods_logic(self.selected_goods_id)
        if specail_goods_logic and specail_goods_logic['buy_callback']:
            specail_goods_logic['buy_callback']()
            return
        item_type = get_lobby_item_type(self.selected_item_no)
        if item_type in [L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN]:
            role_or_skin_buy_confirmUI(self.selected_goods_id, close_after_jump=True)
        elif is_weapon(self.selected_goods_id) or is_vehicle(self.selected_goods_id):
            item_skin_buy_confirmUI(self.selected_goods_id)
        else:
            groceries_buy_confirmUI(self.selected_goods_id)

    def init_tab_list(self):
        if self.tab_info_list:
            data_list = self.tab_info_list
            init_top_tab_list(self.panel.list_tab, data_list, self.tab_click_cb)
            self.panel.list_tab.GetItem(0).btn_tab.OnClick(None)
        return

    def tab_click_cb(self, item, idx):
        info = self.tab_info_list[idx]
        exchange_goods_big_list = info.get('exchange_goods_big_list', [])
        exchange_goods_small_list = info.get('exchange_goods_small_list', [])
        self.big_display_item_list = []
        self.big_display_goods_ids = []
        self.big_display_item_count = 0
        self.small_display_item_list = []
        self.small_display_goods_ids = []
        self.small_display_item_count = 0
        for goods_id in exchange_goods_big_list:
            item_no = get_goods_item_no(goods_id)
            item_type = get_lobby_item_type(item_no)
            self.big_display_item_list.append((goods_id, item_no))
            self.big_display_goods_ids.append(goods_id)
            self.big_display_item_count += 1

        for goods_id in exchange_goods_small_list:
            item_no = get_goods_item_no(goods_id)
            self.small_display_item_list.append((goods_id, item_no))
            self.small_display_goods_ids.append(goods_id)
            self.small_display_item_count += 1

        self.update_display_list()

    def update_display_list(self):
        if self.big_display_item_list:
            nd_list = self.panel.list_item.GetItem(0).list_0_item
            nd_list.SetInitCount(self.big_display_item_count)
            for index, (goods_id, item_no) in enumerate(self.big_display_item_list):
                item_widget = nd_list.GetItem(index)
                self.init_display_item(item_widget, index, goods_id, item_no, is_big_display_item=True)
                self.refresh_display_item(item_widget, goods_id, item_no)

        else:
            nd_list = self.panel.list_item.GetItem(0).list_0_item
            nd_list.SetInitCount(0)
        if self.small_display_item_list:
            nd_list = self.panel.list_item.GetItem(0).list_1_item
            nd_list.SetInitCount(self.small_display_item_count)
            for index, (goods_id, item_no) in enumerate(self.small_display_item_list):
                item_widget = nd_list.GetItem(index)
                self.init_display_item(item_widget, index, goods_id, item_no, is_big_display_item=False)
                self.refresh_display_item(item_widget, goods_id, item_no)

        else:
            nd_list = self.panel.list_item.GetItem(0).list_1_item
            nd_list.SetInitCount(0)
        self.adjust_list_view_size()
        if self.selected_item_widget is None:
            if self.big_display_item_list:
                first_item_widget = self.panel.list_item.GetItem(0).list_0_item.GetItem(0)
                self.on_click_display_item(first_item_widget, 0, *self.big_display_item_list[0])
            elif self.small_display_item_list:
                first_item_widget = self.panel.list_item.GetItem(0).list_1_item.GetItem(0)
                self.on_click_display_item(first_item_widget, 0, *self.small_display_item_list[0])
        ani_names = self.panel.GetAnimationNameList()
        for anim_name in ani_names:
            anim_name = str(anim_name)
            if anim_name.startswith('loop'):
                self.panel.PlayAnimation(anim_name)

        return

    def process_event(self, flag):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.refresh_all_appearance,
           'buy_good_success': self.refresh_all_appearance
           }
        func = emgr.bind_events if flag else emgr.unbind_events
        func(econf)

    def destroy(self):
        self.parent = None
        self.panel = None
        self.on_change_show_reward = None
        self.selected_item_widget = None
        self.pre_init_display_item = None
        self.play_display_item_anim = None
        self.tab_func = None
        self.process_event(False)
        return

    def _show_reward_info(self, item_id, force_show_chuchang=False):
        item_type = get_lobby_item_type(item_id)
        show_model = item_type in MODEL_DISPLAY_TYPE
        if self.nd_lab_name:
            if show_model:
                global_data.emgr.set_lottery_reward_info_label_visible.emit(False)
            else:
                global_data.emgr.set_lottery_reward_info_label_visible.emit(True)
        for nd in self.nd_lab_name:
            nd.setVisible(show_model)

        for nd in self.nd_kind:
            nd.setVisible(show_model)

        self.on_change_show_reward(item_id, force_show_chuchang=force_show_chuchang, force_label_skin=self.visible_show_item_no)

    def _play_display_item_anim(self, item_widget, flag, **kwargs):
        if item_widget and not item_widget.IsDestroyed():
            return
        if flag:
            item_widget.setLocalZOrder(2)
            item_widget.StopAnimation('empty')
            item_widget.PlayAnimation('click')
        else:
            item_widget.setLocalZOrder(0)
            item_widget.StopAnimation('click')
            item_widget.PlayAnimation('empty')

    def on_click_display_item(self, item_widget, item_index, goods_id, item_no):
        if self.selected_item_widget and not self.selected_item_widget.IsDestroyed():
            self.play_display_item_anim(self.selected_item_widget, False, item_no=self.selected_item_no)
            self.selected_item_widget = None
        self.selected_item_index = item_index
        self.selected_goods_id = goods_id
        self.selected_item_no = item_no
        self.selected_item_widget = item_widget
        self.play_display_item_anim(self.selected_item_widget, True, item_no=item_no)
        self.update_select_goods_name_info()
        if self.visible:
            self._show_reward_info(self.selected_item_no)
        self.refresh_buy_btn()
        return

    def _get_item_state_text_id(self, goods_id, item_no=None):
        if item_no is None:
            item_no = get_goods_item_no(goods_id)
        limit_num_all = get_goods_limit_num_all(goods_id)
        bought_num = global_data.player.get_buy_num_all(goods_id)
        item_type = get_lobby_item_type(item_no)
        is_have = item_has_owned_by_goods_id(goods_id)
        if bought_num >= limit_num_all > 0:
            if item_type in RP_SKIN_TYPE:
                return 80451
            else:
                return 12127

        else:
            if is_have:
                return 80451
            return 12074
        return

    def refresh_display_item(self, item_widget, goods_id, item_no):
        price = get_mall_item_price(goods_id)
        splice_price(item_widget.temp_price, price, color=self.price_color)
        is_have = item_has_owned_by_goods_id(goods_id)
        sold_out, _, _ = buy_num_limit_by_all(goods_id)
        item_widget.pnl_get.setVisible(is_have or sold_out)
        item_widget.lab_get.SetString(self._get_item_state_text_id(goods_id, item_no))

    def _enable_buy_btn(self, flag):
        self.panel.btn_buy.SetShowEnable(flag)
        if self.panel.HasAnimation('button_loop'):
            if flag:
                self.panel.PlayAnimation('button_loop')
            else:
                self.panel.StopAnimation('button_loop')
                self.panel.RecoverAnimationNodeState('button_loop')
        if self.panel.HasAnimation('disappear'):
            if not flag:
                self.panel.PlayAnimation('disappear')

    def refresh_buy_btn(self):
        if not self.visible:
            return
        selected_goods_id = self.selected_goods_id
        item_price = get_mall_item_price(self.selected_goods_id)
        splice_price(self.panel.temp_price, item_price, color=['#SK', '#SR', '#DC'])
        has_owned = item_has_owned_by_goods_id(self.selected_goods_id)
        sold_out, _, _ = buy_num_limit_by_all(self.selected_goods_id)
        self._enable_buy_btn(True)
        if has_owned or not check_payment(item_price[0]['goods_payment'], item_price[0]['real_price'], pay_tip=False) or sold_out:
            self._enable_buy_btn(False)
        if not is_good_opened(self.selected_goods_id):
            self._enable_buy_btn(False)
            global_data.game_mgr.show_tip(get_text_by_id(12130).format(get_goods_name(self.selected_goods_id)))
        self.panel.lab_buy.SetString(self._get_item_state_text_id(self.selected_goods_id))

    def update_select_goods_name_info(self):
        item_type = get_lobby_item_type(self.selected_item_no)
        if item_type in MODEL_DISPLAY_TYPE:
            for nd in self.nd_kind:
                check_skin_tag(nd, self.selected_item_no)

            name = get_goods_name(self.selected_goods_id)
            for nd in self.nd_lab_name:
                nd.SetString(name)

    def refresh_all_appearance(self, *args, **kwargs):
        if not self.visible:
            return
        if self.big_display_item_list:
            nd_list = self.panel.list_item.GetItem(0).list_0_item
            nd_list.SetInitCount(self.big_display_item_count)
            for index, (goods_id, item_no) in enumerate(self.big_display_item_list):
                item_widget = nd_list.GetItem(index)
                self.refresh_display_item(item_widget, goods_id, item_no)

        if self.small_display_item_list:
            nd_list = self.panel.list_item.GetItem(0).list_1_item
            nd_list.SetInitCount(self.small_display_item_count)
            for index, (goods_id, item_no) in enumerate(self.small_display_item_list):
                item_widget = nd_list.GetItem(index)
                self.refresh_display_item(item_widget, goods_id, item_no)

        self.update_select_goods_name_info()
        self.refresh_buy_btn()

    def refresh_show_model(self, show_model_id=None):
        if not self.visible:
            return
        self._show_reward_info(self.visible_show_item_no or self.selected_item_no)

    def set_directly_show(self, flag, exclude_nd_visibility_opposite_relatively=()):
        self.directly_show = flag
        if type(exclude_nd_visibility_opposite_relatively) == str:
            exclude_nd_visibility_opposite_relatively = (
             exclude_nd_visibility_opposite_relatively,)
        if flag:
            if exclude_nd_visibility_opposite_relatively:
                for exclude_nd in exclude_nd_visibility_opposite_relatively:
                    if exclude_nd in self.nd_visibility_opposite_relatively:
                        self.nd_visibility_opposite_relatively.remove(exclude_nd)

        elif exclude_nd_visibility_opposite_relatively:
            for exclude_nd in exclude_nd_visibility_opposite_relatively:
                if exclude_nd not in self.nd_visibility_opposite_relatively:
                    self.nd_visibility_opposite_relatively.append(exclude_nd)

        for nd in self.nd_directly_show_visible:
            nd.setVisible(flag)

        for nd in self.nd_directly_show_invisible:
            nd.setVisible(not flag)

    def perform_click_big_display_item(self, idx):
        if not 0 <= idx < self.big_display_item_count:
            return
        item_widget = self.panel.list_item.GetItem(0).list_0_item.GetItem(idx)
        self.on_click_display_item(item_widget, idx, *self.big_display_item_list[idx])

    def perform_click_small_display_item(self, idx):
        if not 0 <= idx < self.small_display_item_count:
            return
        item_widget = self.panel.list_item.GetItem(0).list_1_item.GetItem(idx)
        self.on_click_display_item(item_widget, idx, *self.small_display_item_list[idx])

    def scroll_exchange_item_list(self, to_top):
        if to_top:
            self.panel.list_item.ScrollToTop()
        else:
            self.panel.list_item.ScrollToBottom()

    def set_show_item_no(self, item_no):
        if item_no == self.selected_item_no:
            return
        self.visible_show_item_no = item_no

    def set_show_goods_id(self, goods_id):
        item_no = get_goods_item_no(goods_id)
        self.set_show_item_no(item_no)
        target_tab_index = 0
        if self.tab_info_list:
            for idx, info in enumerate(self.tab_info_list):
                exchange_goods_big_list = info.get('exchange_goods_big_list', [])
                exchange_goods_small_list = info.get('exchange_goods_small_list', [])
                if goods_id in exchange_goods_small_list or goods_id in exchange_goods_big_list:
                    target_tab_index = idx
                    break

            self.panel.list_tab.GetItem(target_tab_index).btn_tab.OnClick(None)
        if goods_id in self.big_display_goods_ids:
            idx = self.big_display_goods_ids.index(goods_id)
            self.perform_click_big_display_item(idx)
            self.panel.list_item.TopWithNode(self.panel.list_item.GetItem(0).list_0_item.GetItem(idx))
        elif goods_id in self.small_display_goods_ids:
            idx = self.small_display_goods_ids.index(goods_id)
            self.perform_click_small_display_item(idx)
            self.panel.list_item.TopWithNode(self.panel.list_item.GetItem(0).list_1_item.GetItem(idx))
        return