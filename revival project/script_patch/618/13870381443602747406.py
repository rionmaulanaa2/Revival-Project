# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/MallDisplayFragmentListWidget.py
from __future__ import absolute_import
import six
from logic.comsys.mall_ui.MallDisplayItemListWidget import MallDisplayItemListWidget
from logic.gutils.mall_utils import get_goods_pic_path, get_goods_name, get_goods_decs, show_model_display_scene, get_goods_item_no, get_special_goods_logic, is_valid_goods, get_goods_is_open, item_has_owned_by_goods_id, get_goods_belong_item_name, has_detail_info, is_weapon, is_vehicle, is_driver, is_mecha, mall_switch_detail, is_good_opened
from logic.client.const import mall_const
from common.cfg import confmgr
from logic.comsys.common_ui.WidgetExtModelPic import WidgetExtModelPic
from logic.gutils.template_utils import init_price_view, init_mall_item
from logic.gutils.lobby_model_display_utils import get_lobby_model_data
from logic.gutils.item_utils import check_skin_tag
from common.utils.timer import CLOCK, RELEASE
ROTATE_FACTOR = 850
MIN_LIST_NUM = 6
TIP_ARCHIVE_DATA_KEY = 'mall_fragment_show_tip'

class MallDisplayFragmentListWidget(WidgetExtModelPic):
    TIPS_KEY = TIP_ARCHIVE_DATA_KEY
    TIPS_TID = 609696
    TABLE_NAME = 'mall_mecha_fragment_config'
    TABLE_ERROR_MSG = '15.\xe5\x95\x86\xe5\x9f\x8e\xe8\xa1\xa8-\xe6\x9c\xba\xe7\x94\xb2\xe5\x85\x91\xe6\x8d\xa2\xe5\x95\x86\xe5\xba\x97\xe8\xa1\xa8   \xe7\x83\x82\xe4\xba\x86\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81\xef\xbc\x81'
    SETTING_KEY = mall_const.SETTING_NEW_FRAGMENT_GOODS

    def __init__(self, dlg):
        super(MallDisplayFragmentListWidget, self).__init__(dlg)
        self.panel = dlg
        self.init_parameters()
        self.process_event(True)
        self.init_widget()
        archive_data = global_data.achi_mgr.get_general_archive_data()
        show_tip = archive_data.get_field(self.TIPS_KEY, True)
        if show_tip:
            self.panel.nd_tips.setVisible(True)
            self.panel.lab_tips.SetString(self.TIPS_TID)
            self.panel.SetTimeOut(3, lambda : self.panel.nd_tips.setVisible(False))
            archive_data.set_field(self.TIPS_KEY, False)
        global_data.emgr.lobby_mall_red_point_update.emit()

    def on_finalize_panel(self):
        super(MallDisplayFragmentListWidget, self).destroy()
        self.process_event(False)

    def set_show(self, show):
        self.panel.setVisible(show)

    def init_parameters(self):
        self.goods_items = []
        self.goods_price_infos = {}
        self._selected_mall_widget = None
        self._select_index = 0
        self.select_goods_id = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_money_info_update_event': self._on_player_info_update,
           'receive_reward_info_from_server_event': self.reset_mall_list,
           'global_buy_info_updated_event': self.reset_mall_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_widget(self):
        self.init_buy_confirm()
        self.init_display()
        self.init_switch_detail()
        self.init_shop_rule()

    def init_shop_rule(self):

        @self.panel.btn_button.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(609694, 609696)

    def init_buy_confirm(self):

        @self.panel.btn_buy_all.unique_callback()
        def OnClick(btn, touch):
            if self.select_goods_id is None or self.is_item_has_bought(self.select_goods_id):
                return
            else:
                specail_goods_logic = get_special_goods_logic(self.select_goods_id)
                if specail_goods_logic and specail_goods_logic['buy_callback']:
                    specail_goods_logic['buy_callback']()
                    return
                self.buy_goods()
                return

    def is_item_has_bought(self, goods_id):
        return item_has_owned_by_goods_id(goods_id)

    def get_buy_ui(self):
        from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI, item_skin_buy_confirmUI, groceries_buy_confirmUI
        if is_driver(self.select_goods_id) or is_mecha(self.select_goods_id):
            ui = role_or_skin_buy_confirmUI(self.select_goods_id)
        elif is_weapon(self.select_goods_id) or is_vehicle(self.select_goods_id):
            ui = item_skin_buy_confirmUI(self.select_goods_id)
        else:
            ui = groceries_buy_confirmUI(self.select_goods_id)
        return ui

    def buy_goods(self):
        buy_ui = self.get_buy_ui()
        mall_ui = global_data.ui_mgr.get_ui('MallMainUI')
        if mall_ui:
            set_buttom_ui_price_nd = getattr(buy_ui, 'set_buttom_ui_price_nd', None)
            if set_buttom_ui_price_nd:
                set_buttom_ui_price_nd(mall_ui.panel.top)
        return

    def init_display(self):

        @self.panel.nd_touch.unique_callback()
        def OnDrag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def init_switch_detail(self):

        @self.panel.btn_check.unique_callback()
        def OnClick(btn, touch):
            mall_switch_detail(self.select_goods_id)

    def update_special_goods(self):
        if not self.special_goods_items:
            return False
        changed = False
        valid_goods = []
        for goods_id in self.special_goods_items:
            valid, _ = get_goods_is_open(str(goods_id))
            if valid:
                valid_goods.append(goods_id)
            else:
                changed = True

        self.special_goods_items = valid_goods
        return changed

    def timer_cb(self):
        if self.update_special_goods():
            self.reset_mall_list()
            if not self.special_goods_items:
                return RELEASE

    def init_mall_list(self, page_index, sub_page_index=None):
        from logic.gcommon.time_utility import check_in_time_range
        mecha_fragment_config = confmgr.get(self.TABLE_NAME, 'content', default=[])
        if not mecha_fragment_config or len(mecha_fragment_config) < 2:
            log_error(self.TABLE_ERROR_MSG)
            return
        self.special_goods_items = mecha_fragment_config[0]['goods_list']
        if type(self.special_goods_items) != list:
            self.special_goods_items = [
             self.special_goods_items]
        self.update_special_goods()
        self.goods_items = mecha_fragment_config[1]['goods_list']
        for line in mecha_fragment_config:
            time_range = line['date']
            if time_range and check_in_time_range((time_range,)):
                self.goods_items = line['goods_list']
                break

        self.special_goods_items = [ goods_id for goods_id in self.special_goods_items if is_good_opened(str(goods_id)) ]
        self.goods_items = [ goods_id for goods_id in self.goods_items if is_good_opened(str(goods_id)) ]
        self.panel.mall_list.set_asyncLoad_tick_time(0)
        self.panel.mall_list.set_asyncLoad_interval_time(0.05)
        self.reset_mall_list(is_init=True)

    def jump_to_goods_id(self, goods_id):
        if not goods_id:
            return
        index = 0
        goods_id = int(goods_id)
        if goods_id in self.special_goods_items:
            index = self.special_goods_items.index(goods_id)
        elif goods_id in self.goods_items:
            index = self.goods_items.index(goods_id) + len(self.special_goods_items)
        mall_list = self.panel.mall_list
        self.init_select_mall_item(index)
        mall_list.scroll_Load()

    def reset_mall_list(self, is_init=False):
        self._selected_mall_widget = None
        mall_list = self.panel.mall_list
        self.special_goods_items.sort(key=self.is_item_has_bought)
        self.goods_items.sort(key=self.is_item_has_bought)
        show_count = len(self.special_goods_items) + len(self.goods_items)

        @mall_list.unique_callback()
        def OnCreateItem(lv, index, item_widget):
            self.cb_create_item(index, item_widget)

        off_set = mall_list.GetContentOffset()
        mall_list.SetInitCount(show_count)
        all_items = mall_list.GetAllItem()
        for index, widget in enumerate(all_items):
            if type(widget) in [dict, six.text_type, str]:
                continue
            self.cb_create_item(index, widget)

        if len(self.goods_items):
            if is_init:
                self.init_select_mall_item(0)
            else:
                self.init_select_mall_item(self._select_index, off_set)
        else:
            global_data.emgr.change_model_display_scene_item.emit(None)
        mall_list.scroll_Load()
        return

    def init_select_mall_item(self, index, off_set=None):
        mall_list = self.panel.mall_list
        index = min(index, len(self.goods_items) - 1)
        if not off_set:
            mall_list.LocatePosByItem(index)
        else:
            mall_list.SetContentOffset(off_set)
        select_widget = mall_list.GetItem(index)
        if select_widget is None:
            select_widget = mall_list.DoLoadItem(index)
        select_widget and select_widget.bar.OnClick(None)
        return

    def cb_create_item(self, index, item_widget):
        is_special = False
        if index < len(self.special_goods_items):
            goods_id = self.special_goods_items[index]
            is_special = True
        elif index - len(self.special_goods_items) < len(self.goods_items):
            goods_id = self.goods_items[index - len(self.special_goods_items)]
        else:
            goods_id = None
        goods_id = str(goods_id)
        init_mall_item(item_widget, goods_id, show_open_time=is_special)
        if goods_id is None:
            item_widget.bar.SetEnable(False)
        else:
            item_widget.bar.SetEnable(True)
            if item_widget.img_red and is_special:
                recommendation_dict = global_data.message_data.get_seting_inf(self.SETTING_KEY) or {}
                is_read = recommendation_dict.get(str(goods_id), 0)
                item_widget.img_red.setVisible(not bool(is_read))

            @item_widget.bar.unique_callback()
            def OnClick(btn, touch, idx=index, gid=goods_id, widget=item_widget, is_sp=is_special):
                if gid is None:
                    return
                else:
                    self._select_index = idx
                    show_model_display_scene(gid)
                    item_no = get_goods_item_no(gid)
                    model_data = get_lobby_model_data(item_no)
                    is_show_model = bool(model_data)
                    self.select_product(widget, gid, is_show_model, is_sp)
                    if is_show_model:
                        self.ext_show_item_model(model_data, gid, item_no)
                    return

        return

    def select_product(self, mall_widget, goods_id, is_show_model=True, is_special=False):
        if is_special:
            recommendation_dict = global_data.message_data.get_seting_inf(self.SETTING_KEY) or {}
            is_read = recommendation_dict.get(str(goods_id), 0)
            if not is_read:
                recommendation_dict[str(goods_id)] = 1
                global_data.message_data.set_seting_inf(self.SETTING_KEY, recommendation_dict)
            mall_widget.img_red.setVisible(False)
        if not is_show_model:
            self.ext_not_show_no_model()
        global_data.emgr.select_mall_goods.emit(goods_id)
        if self._selected_mall_widget:
            self._selected_mall_widget.setLocalZOrder(0)
            self._selected_mall_widget.choose.setVisible(False)
            self._selected_mall_widget = None
        specail_goods_logic = get_special_goods_logic(goods_id)
        show_price = specail_goods_logic or True if 1 else specail_goods_logic['show_price']
        btn_buy_txt = specail_goods_logic or '' if 1 else specail_goods_logic['btn_buy_txt']
        is_valid = is_valid_goods(goods_id)
        btn_buy_txt = btn_buy_txt if is_valid else 81137
        is_open, _ = get_goods_is_open(goods_id)
        btn_buy_txt = btn_buy_txt if is_open else 81154
        self.select_goods_id = goods_id
        mall_widget.setLocalZOrder(2)
        self._selected_mall_widget = mall_widget
        self._selected_mall_widget.choose.setVisible(True)
        if show_price:
            init_price_view(self.panel.temp_price, goods_id, mall_const.DARK_PRICE_COLOR)
            self.panel.temp_price.setVisible(True)
            self.panel.btn_buy_all.SetTextOffset({'x': '50%90','y': '50%'})
        else:
            self.panel.temp_price.setVisible(False)
            self.panel.btn_buy_all.SetTextOffset({'x': '50%','y': '50%'})
        owned = self.is_item_has_bought(goods_id)
        self.panel.btn_buy_all.setVisible(not owned)
        self.panel.btn_buy_all.SetEnable(is_valid and is_open)
        if btn_buy_txt:
            self.panel.btn_buy_all.SetText(btn_buy_txt)
        else:
            self.panel.btn_buy_all.SetText(80166)
        self.panel.nd_item_describe.setVisible(is_show_model)
        self.panel.nd_item_check.setVisible(is_show_model)
        self.panel.nd_common_reward and self.panel.nd_common_reward.setVisible(not is_show_model)
        if is_show_model:
            belong_item_name = get_goods_belong_item_name(goods_id) or ''
            item_name = get_goods_name(goods_id) or ''
            if belong_item_name:
                self.panel.nd_item_describe.lab_name.SetString(''.join([belong_item_name, '\xc2\xb7', item_name]))
            else:
                self.panel.nd_item_describe.lab_name.SetString(item_name)
            check_skin_tag(self.panel.nd_item_describe.nd_kind, None, goods_id)
            self.refresh_detail_btn()
        elif self.panel.nd_common_reward:
            self.panel.img_item.SetDisplayFrameByPath('', get_goods_pic_path(goods_id))
            self.panel.nd_common_reward.lab_name.SetString(get_goods_name(goods_id))
            self.panel.nd_common_reward.lab_describe.SetString(get_goods_decs(goods_id))
        return

    def refresh_detail_btn(self):
        btn_check = self.panel.btn_check
        if not btn_check:
            return
        btn_check.setVisible(has_detail_info(self.select_goods_id))

    def _on_player_info_update(self, *args):
        init_price_view(self.panel.temp_price, self.select_goods_id, mall_const.DARK_PRICE_COLOR)

    @staticmethod
    def show_red_point(tip_archive_data_key=TIP_ARCHIVE_DATA_KEY, conf_name='mall_mecha_fragment_config', setting_key=mall_const.SETTING_NEW_FRAGMENT_GOODS):
        archive_data = global_data.achi_mgr.get_general_archive_data()
        if archive_data.get_field(tip_archive_data_key, True):
            return 1
        mecha_fragment_config = confmgr.get(conf_name, 'content', default=[])
        if not mecha_fragment_config:
            return 0
        special_goods_items = mecha_fragment_config[0]['goods_list']
        special_goods_items = [ goods_id for goods_id in special_goods_items if is_good_opened(str(goods_id)) ]
        if not special_goods_items:
            return 0
        recommendation_dict = global_data.message_data.get_seting_inf(setting_key) or {}
        for goods_id in special_goods_items:
            if recommendation_dict.get(str(goods_id), 0):
                continue
            if get_goods_is_open(str(goods_id))[0]:
                return 1

        return 0